# Released under the MIT License. See LICENSE for details.
# ba_meta require api 8

from __future__ import annotations

from typing import TYPE_CHECKING
from bascenev1._coopsession import CoopSession
from bascenev1lib.actor.powerupbox import PowerupBox, PowerupBoxFactory
from bascenev1lib.actor.spazfactory import SpazFactory
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.bomb import Blast
from bascenev1lib.actor.onscreentimer import OnScreenTimer
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.game.elimination import Icon
from babase import _math

import bascenev1 as bs
import babase
import random

if TYPE_CHECKING:
    from typing import Any, Sequence


"""
BombSquad Mods: API 8
—————————————————————————
• バブルブラスターv0.1
• バグを報告するために私に連絡してください

クレジットは不要ですが、非常に高く評価されているジェスチャーです。お客様の謝辞
クレジットを通じて、サポートを示すための素晴らしい方法です:)

@不和: ajinomoto_yan#8997
@ヤン_改造を行います
—————————————————————————
"""

class BubbleSpaz(PlayerSpaz):

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.HitMessage):
            super().handlemessage(msg)
            if self.shield is not None:
                shieldsize = 1.5
                bs.animate(self.shield, 'radius', {0.0: shieldsize, 0.15: shieldsize+0.85, 0.24: shieldsize})
            if self.node:
                if (self.shield_hitpoints == 0 or self.shield is None) and not self.node.dead:
                    self.handlemessage(bs.DieMessage())
                    self.shatter(True)
                    pos = self.node.position; color = self.node.color
                    Blast(position=pos, blast_type='normal',blast_radius=2.0).autoretain()
                    bs.emitfx(
                        position=pos,
                        velocity=(0,0,0),
                        count=30,
                        spread=1.0,
                        scale=1.3,
                        chunk_type='spark',
                        emit_type='stickers',
                    )
                    flash = bs.newnode(
                        'flash',
                        attrs={
                            'position': (pos[0], pos[1]+0.3, pos[2]),
                            'size': 0.0,
                            'color': (color[0]+0.1, color[1]+0.1, color[2]+0.1),
                        },
                    )
                    scorch = bs.newnode(
                        'scorch',
                        attrs={
                            'position': pos,
                            'color': (color[0]+0.1, color[1]+0.1, color[2]+0.1),
                            'size': 2.36,
                            'big': False,
                        },
                    )
                    bs.animate(flash, 'size', {0.0: 0, 0.3:2.5})
                    bs.animate(scorch, 'presence', {3.000: 1, 23.000: 0})
                    bs.timer(0.43, flash.delete)
                    bs.timer(23.0, scorch.delete)
        else:
            return super().handlemessage(msg)
        return None

class Player(bs.Player['Team']):
    """Our player type for this game."""

    def __init__(self) -> None:
        self.lives = 0
        self.icons: list[Icon] = []
        self.death_time: float | None = None

class Team(bs.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.survival_seconds: int | None = None
        self.spawn_order: list[Player] = []


# ba_meta export bascenev1.GameActivity
class BubbleBlastersGame(bs.TeamGameActivity[Player, Team]):
    """Game type where last bubble(s) left win."""

    name = 'Bubble Blasters'
    description = 'Break all opponents\' bubbles while protecting yours to win.'
    scoreconfig = bs.ScoreConfig(
        label='Survived', scoretype=bs.ScoreType.MILLISECONDS, version='B',none_is_winner=True,
    )
    announce_player_deaths = False
    allow_mid_activity_joins = False

    @classmethod
    def get_available_settings(
        cls, sessiontype: type[bs.Session]
    ) -> list[bs.Setting]:
        settings = [
            bs.IntChoiceSetting(
                'Time Limit',
                choices=[
                    ('None', 0),
                    ('1 Minute', 60),
                    ('2 Minutes', 120),
                    ('3 Minutes', 180),
                    ('4 Minutes', 240),
                    ('5 Minutes', 300),
                ],
                default=180,
            ),
            bs.IntChoiceSetting(
                'Bubble HP',
                choices=[
                    ('1000', 1000),
                    ('2000', 2000),
                    ('3000', 3000),
                    ('4000', 4000),
                    ('5000', 5000),
                ],
                default=3000,
            ),
            bs.BoolSetting('Epic Mode', default=False),
        ]
        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.DualTeamSession) or issubclass(
            sessiontype, bs.FreeForAllSession
        )

    @classmethod
    def get_supported_maps(cls, sessiontype: type[bs.Session]) -> list[str]:
        assert bs.app.classic is not None
        return bs.app.classic.getmaps('melee')

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._start_time: float | None = None
        self._vs_text: bs.Actor | None = None
        self._last_player_death_time: float | None = None
        self._round_end_timer: bs.Timer | None = None
        self._epic_mode = bool(settings['Epic Mode'])
        self._time_limit = float(settings['Time Limit'])
        self._bubble_hp = float(settings['Bubble HP'])
        self._timer: OnScreenTimer | None = None

        # Base class overrides:
        self.slow_motion = self._epic_mode
        self.default_music = (
            bs.MusicType.EPIC if self._epic_mode else bs.MusicType.SURVIVAL
        )

    def get_instance_description(self) -> str | Sequence:
        return (
            'Break all opponent\'s bubbles, last team standing wins.'
            if isinstance(self.session, bs.DualTeamSession)
            else 'Break all opponent\'s bubbles, last one standing wins.'
        )

    def get_instance_description_short(self) -> str | Sequence:
        return (
            'Break all enemies\' bubbles'
            if isinstance(self.session, bs.DualTeamSession)
            else 'Break all enemies\' bubbles'
        )

    def on_begin(self) -> None:
        super().on_begin()
        self._start_time = bs.time()
        self._excluded_powerups = ['shield', 'health']
        self.setup_standard_time_limit(self._time_limit)
        self.setup_standard_powerup_drops()
        self._timer = OnScreenTimer()
        self._timer.start()
        self._update_icons()

        bs.timer(5.0, self._check_end_game)

    def _standard_drop_powerup(self, index: int, expire: bool = True) -> None:
        from bascenev1lib.actor.powerupbox import PowerupBox, PowerupBoxFactory
        poweruptype = PowerupBoxFactory.get().get_random_powerup_type(
            forcetype=[],excludetypes=self._excluded_powerups
        )
        PowerupBox(
            position=self.map.powerup_spawn_points[index],
            poweruptype=poweruptype,
            expire=expire,
        ).autoretain()

    def _drop_powerup(self, index: int, poweruptype: str | None = None) -> None:
        poweruptype = PowerupBoxFactory.get().get_random_powerup_type(
            forcetype=[], excludetypes=self._excluded_powerups
        )
        PowerupBox(
            position=self.map.powerup_spawn_points[index],
            poweruptype=poweruptype,
        ).autoretain()

    def _update_icons(self) -> None:
        if isinstance(self.session, bs.FreeForAllSession):
            count = len(self.teams)
            x_offs = 85
            xval = x_offs * (count - 1) * -0.5
            for team in self.teams:
                if len(team.players) == 1:
                    player = team.players[0]
                    for icon in player.icons:
                        icon.set_position_and_scale((xval, 30), 0.7)
                        icon.update_for_lives()
                    xval += x_offs

        else:
            for team in self.teams:
                if team.id == 0:
                    xval = -50
                    x_offs = -85
                else:
                    xval = 50
                    x_offs = 85
                for player in team.players:
                    for icon in player.icons:
                        icon.set_position_and_scale((xval, 30), 0.7)
                        icon.update_for_lives()
                    xval += x_offs

    def on_player_join(self, player: Player) -> None:
        player.lives = 1
        player.icons = [Icon(player, position=(0, 50), scale=0.8)]
        self.spawn_player(player)

        if self.has_begun():
            self._update_icons()

    def on_player_leave(self, player: Player) -> None:
        super().on_player_leave(player)
        player.icons = []

        bs.timer(0, self._update_icons)

        if self._get_total_team_lives(player.team) == 0:
            assert self._start_time is not None
            player.team.survival_seconds = int(bs.time() - self._start_time)
        self._check_end_game()

    def spawn_player(self, player: Player) -> bs.Actor:
        actor = self.spawn_player_spaz(player)

        # If we have any icons, update their state.
        for icon in player.icons:
            icon.handle_player_spawned()
        return actor

    def spawn_player_spaz(self, player: PlayerType) -> bs.Actor:
        factory = SpazFactory.get()

        position = self.map.get_ffa_start_position(self.players) 
        spaz = BubbleSpaz(color=player.color,
                         highlight=player.highlight,
                         character=player.character,
                         player=player
                        )
        player.actor = spaz
        assert spaz.node
        spaz.node.name = player.getname()
        spaz.node.name_color = babase.safecolor(player.color, target_intensity=0.75)
        
        self._spawn_sound.play(1, position=spaz.node.position)
        light_color = _math.normalized_color(player.color)
        light = bs.newnode('light', attrs={'color': light_color})
        spaz.node.connectattr('position', light, 'position')
        bs.animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})
        bs.timer(0.5, light.delete)

        spaz.handlemessage(
            bs.StandMessage(
                position, random.uniform(0, 360)
            )
        )

        # -- add shield --
        spaz.equip_shields(False)
        spaz.shield_hitpoints = self._bubble_hp
        spaz.shield_hitpoints_max = self._bubble_hp
        spaz.shield.color = spaz.node.color
        spaz.shield.radius = 1.5
        spaz.connect_controls_to_player(enable_pickup=False)
        return spaz

    def _get_total_team_lives(self, team: Team) -> int:
        return sum(player.lives for player in team.players)

    def _print_lives(self, player: Player) -> None:
        from bascenev1lib.actor import popuptext
        if not player or not player.is_alive() or not player.node:
            return

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            super().handlemessage(msg)
            player: Player = msg.getplayer(Player)
            curtime = bs.time()
            player.lives = 0

            for icon in player.icons:
                icon.handle_player_died()

            SpazFactory.get().single_player_death_sound.play()

            if self._get_total_team_lives(player.team) == 0:
                assert self._start_time is not None
                player.team.survival_seconds = int(
                    bs.time() - self._start_time
                )

            msg.getplayer(Player).death_time = curtime
            bs.timer(1.0, self._check_end_game)

    def _check_end_game(self) -> None:
        living_team_count = 0
        for team in self.teams:
            for player in team.players:
                if player.is_alive():
                    living_team_count += 1
                    break

        if living_team_count <= 1:
            self.end_game()

    def end_game(self) -> None:
        cur_time = bs.time()
        assert self._timer is not None
        start_time = self._timer.getstarttime()

        for team in self.teams:
            for player in team.players:
                survived = False

                if player.death_time is None:
                    survived = True
                    player.death_time = cur_time + 1

                score = int(player.death_time - self._timer.getstarttime())
                if survived:
                    score += 21
                self.stats.player_scored(player, score, screenmessage=False)

        self._timer.stop(endtime=self._last_player_death_time)

        results = bs.GameResults()

        for team in self.teams:
            longest_life = 0.0
            for player in team.players:
                assert player.death_time is not None
                longest_life = max(longest_life, player.death_time - start_time)

            results.set_team_score(team, int(1000.0 * longest_life))

        self._vs_text = None
        self.end(results=results)
