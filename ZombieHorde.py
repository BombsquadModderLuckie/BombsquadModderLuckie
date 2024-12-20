# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 8

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import copy
import random
import babase
import _babase
import _bascenev1
import bascenev1 as bs
from babase import _math
from bascenev1._coopsession import CoopSession
from bascenev1._messages import PlayerDiedMessage, StandMessage
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.scoreboard import Scoreboard
from bascenev1lib.game.elimination import Icon, Player
from bascenev1lib.actor.spaz import PickupMessage, Spaz
from bascenev1lib.actor.spazbot import SpazBotSet, BrawlerBot, SpazBotDiedMessage
from bascenev1lib.actor.spazfactory import SpazFactory


if TYPE_CHECKING:
    from typing import Any, Sequence


class PlayerSpaz_Zom(PlayerSpaz):

    def __init__(
        self,
        player: bs.Player,
        color: Sequence[float] = (1.0, 1.0, 1.0),
        highlight: Sequence[float] = (0.5, 0.5, 0.5),
        character: str = 'Spaz',
        powerups_expire: bool = True,
        fire_friend: bool = False,
        enable_pickup: bool = False,
    ):
        super().__init__(player, color, highlight, character, powerups_expire)
        self._fire_friend = fire_friend
        self._enable_pickup = enable_pickup

    def handlemessage(self, m: Any) -> Any:
        if isinstance(m, bs.HitMessage):
            if not self.node:
                return
            if not m._source_player is None:
                if self._fire_friend:
                    super().handlemessage(m)
                else:
                    try:
                        playa = m._source_player.getname(True, False)
                        if not playa is None:
                            if m._source_player.lives < 1:
                                super().handlemessage(m)
                    except:
                        super().handlemessage(m)
            else:
                super().handlemessage(m)

        elif isinstance(m, bs.FreezeMessage):
            pass

        elif isinstance(m, PickupMessage):
            if not self.node:
                return None
            if self._enable_pickup:
                try:
                    collision = bs.getcollision()
                    opposingnode = collision.opposingnode
                    opposingbody = collision.opposingbody
                except bs.NotFoundError:
                    return True

                try:
                    if opposingnode.invincible:
                        return True
                except Exception:
                    pass

                try:
                    playa = opposingnode._source_player.getname(True, False)
                    if not playa is None:
                        if opposingnode._source_player.lives > 0:
                            return True
                except  Exception:
                    pass

                if (opposingnode.getnodetype() == 'spaz'
                        and not opposingnode.shattered and opposingbody == 4):
                    opposingbody = 1

                held = self.node.hold_node
                if held and held.getnodetype() == 'flag':
                    return True

                self.node.hold_body = opposingbody
                self.node.hold_node = opposingnode
        else:
            return super().handlemessage(m)
        return None


class PlayerZombie(PlayerSpaz):
    def handlemessage(self, m: Any) -> Any:
        if isinstance(m, bs.HitMessage):
            if not self.node:
                return None
            if not m._source_player is None:
                try:
                    playa = m._source_player.getname(True, False)
                    if playa is None:
                        pass
                    else:
                        super().handlemessage(m)
                except:
                    super().handlemessage(m)
            else:
                super().handlemessage(m)
        else:
            super().handlemessage(m)


class zBotSet(SpazBotSet):
    def start_moving(self) -> None:
        """Start processing bot AI updates so they start doing their thing."""
        self._bot_update_timer = bs.Timer(
            0.05, bs.WeakCall(self.zUpdate), repeat=True)

    def zUpdate(self) -> None:

        try:
            bot_list = self._bot_lists[self._bot_update_list] = ([
                b for b in self._bot_lists[self._bot_update_list] if b
            ])
        except Exception:
            bot_list = []
            bs.print_exception('Error updating bot list: ' +
                               str(self._bot_lists[self._bot_update_list]))
        self._bot_update_list = (
            self._bot_update_list + 1) % self._bot_list_count

        player_pts = []
        for player in bs.getactivity().players:
            assert isinstance(player, bs.Player)
            try:
                if player.is_alive():
                    assert isinstance(player.actor, Spaz)
                    assert player.actor.node
                    if player.lives > 0:
                        player_pts.append(
                            (bs.Vec3(player.actor.node.position),
                             bs.Vec3(player.actor.node.velocity)))
            except Exception:
                bs.print_exception('Error on bot-set _update.')

        for bot in bot_list:
            bot.set_player_points(player_pts)
            bot.update_ai()


class Team(bs.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0
        self.spawn_order: list[Player] = []


# ba_meta export bascenev1.GameActivity
class ZombieHorde(bs.TeamGameActivity[Player, Team]):

    name = 'Zombie Horde'
    description = 'Kill walkers for points!'
    scoreconfig = bs.ScoreConfig(
        label='Score',
        scoretype=bs.ScoreType.POINTS,
        none_is_winner=False,
        lower_is_better=False,
        )
    # Show messages when players die since it's meaningful here.
    announce_player_deaths = True
    allow_mid_activity_joins = False

    @classmethod
    def get_available_settings(
            cls, sessiontype: type[bs.Session]) -> list[bs.Setting]:
        settings = [
            bs.IntSetting(
                'Lives Per Player',
                default=1,
                min_value=1,
                max_value=10,
                increment=1,
            ),
            bs.IntSetting(
                'Max Zombies',
                default=10,
                min_value=5,
                max_value=200,
                increment=5,
            ),
            bs.IntChoiceSetting(
                'Time Limit',
                choices=[
                    ('None', 0),
                    ('1 Minute', 60),
                    ('2 Minutes', 120),
                    ('5 Minutes', 300),
                    ('10 Minutes', 600),
                    ('20 Minutes', 1200),
                ],
                default=0,
            ),
            bs.FloatChoiceSetting(
                'Respawn Times',
                choices=[
                    ('Shorter', 0.25),
                    ('Short', 0.5),
                    ('Normal', 1.0),
                    ('Long', 2.0),
                    ('Longer', 4.0),
                ],
                default=1.0,
            ),
            bs.BoolSetting('Fire Friend', default=False),
            bs.BoolSetting('Enable Pickup', default=False),
            bs.BoolSetting('Epic Mode', default=False),
        ]
        if issubclass(sessiontype, bs.DualTeamSession):
            settings.append(
                bs.BoolSetting('Balance Total Lives', default=False))
        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return issubclass(sessiontype, bs.DualTeamSession) or issubclass(
            sessiontype, bs.FreeForAllSession
        )

    @classmethod
    def get_supported_maps(cls, sessiontype: type[bs.Session]) -> list[str]:
        return bs.app.classic.getmaps('melee')

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._start_time: float | None = None
        self._vs_text: bs.Actor | None = None
        self._round_end_timer: bs.Timer | None = None
        self._epic_mode = bool(settings['Epic Mode'])
        self._lives_per_player = int(settings['Lives Per Player'])
        self._max_zombies = int(settings['Max Zombies'])
        self._time_limit = float(settings['Time Limit'])
        self._balance_total_lives = bool(
            settings.get('Balance Total Lives', False))
        self._fire_friend = bool(settings['Fire Friend'])
        self._enable_pickup = bool(settings['Enable Pickup'])
        self.setup_zombies()

        # Base class overrides:
        self.slow_motion = self._epic_mode
        self.default_music = (bs.MusicType.EPIC
                              if self._epic_mode else bs.MusicType.SURVIVAL)

    def setup_zombies(self) -> None:
        self.spazList = []
        self.zombieQ = 0

        activity = bs.getactivity()
        my_factory = SpazFactory.get()

        appears = ['Kronk','Zoe','Pixel','Agent Johnson',
                   'Bones','Frosty','Kronk2']
        myAppear = copy.copy(bs.app.classic.spaz_appearances['Kronk'])
        myAppear.name = 'Kronk2'
        bs.app.classic.spaz_appearances['Kronk2'] = myAppear
        for appear in appears:
            my_factory.get_media(appear)
        med = my_factory.spaz_media
        med['Kronk2']['head_mesh'] = med['Zoe']['head_mesh']
        med['Kronk2']['color_texture'] = med['Agent Johnson']['color_texture']
        med['Kronk2']['color_mask_texture']=med['Pixel']['color_mask_texture']
        med['Kronk2']['torso_mesh'] = med['Bones']['torso_mesh']
        med['Kronk2']['pelvis_mesh'] = med['Pixel']['pelvis_mesh']
        med['Kronk2']['upper_arm_mesh'] = med['Frosty']['upper_arm_mesh']
        med['Kronk2']['forearm_mesh'] = med['Frosty']['forearm_mesh']
        med['Kronk2']['hand_mesh'] = med['Bones']['hand_mesh']
        med['Kronk2']['upper_leg_mesh'] = med['Bones']['upper_leg_mesh']
        med['Kronk2']['lower_leg_mesh'] = med['Pixel']['lower_leg_mesh']
        med['Kronk2']['toes_mesh'] = med['Bones']['toes_mesh']

    def get_instance_description(self) -> str | Sequence:
        return ('Kill walkers for points! ',
                'Dead player walker: 2 points!') if isinstance(
            self.session, bs.DualTeamSession) else (
                'Kill walkers for points! Dead player walker: 2 points!')

    def get_instance_description_short(self) -> str | Sequence:
        return ('Kill walkers for points! ',
                'Dead player walker: 2 points!') if isinstance(
            self.session, bs.DualTeamSession) else (
                'Kill walkers for points! Dead player walker: 2 points!')

    def on_player_join(self, player: Player) -> None:
        player.lives = self._lives_per_player

        player.icons = [Icon(player, position=(0, 50), scale=0.8)]
        if player.lives > 0:
            self.spawn_player(player)

        if self.has_begun():
            self._update_icons()

        self._update_scoreboard()

    def on_begin(self) -> None:
        super().on_begin()
        self._start_time = bs.time()
        self.setup_standard_time_limit(self._time_limit)
        self.setup_standard_powerup_drops()
        self.zombieQ = 1

        # If balance-team-lives is on, add lives to the smaller team until
        # total lives match.
        if (isinstance(self.session, bs.DualTeamSession)
                and self._balance_total_lives and self.teams[0].players
                and self.teams[1].players):
            if self._get_total_team_lives(
                    self.teams[0]) < self._get_total_team_lives(self.teams[1]):
                lesser_team = self.teams[0]
                greater_team = self.teams[1]
            else:
                lesser_team = self.teams[1]
                greater_team = self.teams[0]
            add_index = 0
            while (self._get_total_team_lives(lesser_team) <
                   self._get_total_team_lives(greater_team)):
                lesser_team.players[add_index].lives += 1
                add_index = (add_index + 1) % len(lesser_team.players)

        self._bots = zBotSet()

        #Set colors and character for ToughGuyBot to be zombie
        setattr(BrawlerBot, 'color', (0.4,0.1,0.05))
        setattr(BrawlerBot, 'highlight', (0.2,0.4,0.3))
        setattr(BrawlerBot, 'character', 'Kronk2')
        # start some timers to spawn bots
        thePt = self.map.get_ffa_start_position(self.players)

        self._update_icons()

        # We could check game-over conditions at explicit trigger points,
        # but lets just do the simple thing and poll it.
        bs.timer(1.0, self._update, repeat=True)

    def _update_icons(self) -> None:
        # pylint: disable=too-many-branches

        # In free-for-all mode, everyone is just lined up along the bottom.
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

        # In teams mode we split up teams.
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

    def spawn_player(self, player: Player) -> bs.Actor:
        position = self.map.get_ffa_start_position(self.players)
        angle = 20
        name = player.getname()

        light_color = _math.normalized_color(player.color)
        display_color = _babase.safecolor(player.color, target_intensity=0.75)
        spaz = PlayerSpaz_Zom(color=player.color,
                              highlight=player.highlight,
                              character=player.character,
                              player=player,
                              fire_friend=self._fire_friend,
                              enable_pickup=self._enable_pickup)
        player.actor = spaz
        assert spaz.node
        self.spazList.append(spaz)

        if isinstance(self.session, CoopSession) and self.map.getname() in [
                'Courtyard', 'Tower D'
        ]:
            mat = self.map.preloaddata['collide_with_wall_material']
            assert isinstance(spaz.node.materials, tuple)
            assert isinstance(spaz.node.roller_materials, tuple)
            spaz.node.materials += (mat, )
            spaz.node.roller_materials += (mat, )

        spaz.node.name = name
        spaz.node.name_color = display_color
        spaz.connect_controls_to_player()
        factory = SpazFactory()

        # Move to the stand position and add a flash of light.
        spaz.handlemessage(
            StandMessage(
                position,
                angle if angle is not None else random.uniform(0, 360)))
        self._spawn_sound.play(1, position=spaz.node.position)
        light = _bascenev1.newnode('light', attrs={'color': light_color})
        spaz.node.connectattr('position', light, 'position')
        bs.animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})
        _bascenev1.timer(0.5, light.delete)

        bs.timer(0.3, bs.Call(self._print_lives, player))

        for icon in player.icons:
            icon.handle_player_spawned()
        return spaz

    def respawn_player_zombie(self,
                              player: Player,
                              respawn_time: float | None = None) -> None:
        # pylint: disable=cyclic-import

        assert player
        if respawn_time is None:
            teamsize = len(player.team.players)
            if teamsize == 1:
                respawn_time = 3.0
            elif teamsize == 2:
                respawn_time = 5.0
            elif teamsize == 3:
                respawn_time = 6.0
            else:
                respawn_time = 7.0

        # If this standard setting is present, factor it in.
        if 'Respawn Times' in self.settings_raw:
            respawn_time *= self.settings_raw['Respawn Times']

        # We want whole seconds.
        assert respawn_time is not None
        respawn_time = round(max(1.0, respawn_time), 0)

        if player.actor and not self.has_ended():
            from bascenev1lib.actor.respawnicon import RespawnIcon
            player.customdata['respawn_timer'] = _bascenev1.Timer(
                respawn_time, bs.WeakCall(
                    self.spawn_player_if_exists_as_zombie, player))
            player.customdata['respawn_icon'] = RespawnIcon(
                player, respawn_time)

    def spawn_player_if_exists_as_zombie(self, player: Player) -> None:
        """
        A utility method which calls self.spawn_player() *only* if the
        bs.Player provided still exists; handy for use in timers and whatnot.

        There is no need to override this; just override spawn_player().
        """
        if player:
            self.spawn_player_zombie(player)

    def spawn_player_zombie(self, player: Player) -> bs.Actor:
        position = self.map.get_ffa_start_position(self.players)
        angle = 20
        name = player.getname()

        light_color = _math.normalized_color(player.color)
        display_color = _babase.safecolor(player.color, target_intensity=0.75)
        spaz = PlayerZombie(color=player.color,
                              highlight=player.highlight,
                              character='Kronk2',
                              player=player)
        player.actor = spaz
        assert spaz.node
        self.spazList.append(spaz)

        if isinstance(self.session, CoopSession) and self.map.getname() in [
                'Courtyard', 'Tower D'
        ]:
            mat = self.map.preloaddata['collide_with_wall_material']
            assert isinstance(spaz.node.materials, tuple)
            assert isinstance(spaz.node.roller_materials, tuple)
            spaz.node.materials += (mat, )
            spaz.node.roller_materials += (mat, )

        spaz.node.name = name
        spaz.node.name_color = display_color
        spaz.connect_controls_to_player(enable_punch=True,
                                        enable_bomb=False,
                                        enable_pickup=False)

        # Move to the stand position and add a flash of light.
        spaz.handlemessage(
            StandMessage(
                position,
                angle if angle is not None else random.uniform(0, 360)))
        self._spawn_sound.play(1, position=spaz.node.position)
        light = _bascenev1.newnode('light', attrs={'color': light_color})
        spaz.node.connectattr('position', light, 'position')
        bs.animate(light, 'intensity', {0: 0, 0.25: 1, 0.5: 0})
        _bascenev1.timer(0.5, light.delete)

        bs.timer(0.3, bs.Call(self._print_lives, player))

        for icon in player.icons:
            icon.handle_player_spawned()
        return spaz

    def _print_lives(self, player: Player) -> None:
        from bascenev1lib.actor import popuptext

        # We get called in a timer so it's possible our player has left/etc.
        if not player or not player.is_alive() or not player.node:
            return

        try:
            pos = player.actor.node.position
        except Exception as e:
            print('EXC getting player pos in bsElim',e)
            return
        if player.lives > 0:
            popuptext.PopupText('x' + str(player.lives - 1),
                                color=(1, 1, 0, 1),
                                offset=(0, -0.8, 0),
                                random_offset=0.0,
                                scale=1.8,
                                position=pos).autoretain()
        else:
            popuptext.PopupText('Dead!',
                                color=(1, 1, 0, 1),
                                offset=(0, -0.8, 0),
                                random_offset=0.0,
                                scale=1.8,
                                position=pos).autoretain()

    def on_player_leave(self, player: Player) -> None:
        super().on_player_leave(player)
        player.icons = []

        # Update icons in a moment since our team will be gone from the
        # list then.
        bs.timer(0, self._update_icons)

    def _get_total_team_lives(self, team: Team) -> int:
        return sum(player.lives for player in team.players)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):

            # Augment standard behavior.
            super().handlemessage(msg)
            player: Player = msg.getplayer(Player)

            if player.lives > 0:
                player.lives -= 1
            else:
                if msg._killerplayer:
                    if msg._killerplayer.lives > 0:
                        msg._killerplayer.team.score += 2
                        self._update_scoreboard()

            if msg._player in self.spazList:
                self.spazList.remove(msg._player)
            if player.lives < 0:
                player.lives = 0

            # If we have any icons, update their state.
            for icon in player.icons:
                icon.handle_player_died()

            # If we hit zero lives, we're dead (and our team might be too).
            if player.lives == 0:
                self.respawn_player_zombie(player)
            else:
                # Otherwise, in regular mode, respawn.
                self.respawn_player(player)

        elif isinstance(msg, SpazBotDiedMessage):
            self._onSpazBotDied(msg)
            super().handlemessage(msg)#bs.PopupText("died",position=self._position,color=popupColor,scale=popupScale).autoRetain()
        else:
            super().handlemessage(msg)

    def _update(self) -> None:
        if self.zombieQ > 0:
            self.zombieQ -= 1
            self.spawn_zombie()

        # If we're down to 1 or fewer living teams, start a timer to end
        # the game (allows the dust to settle and draws to occur if deaths
        # are close enough).
        teamsRemain = self._get_living_teams()
        if len(teamsRemain) < 2:
            if len(teamsRemain) == 1:
                theScores = []
                for team in self.teams:
                    theScores.append(team.score)
                if teamsRemain[0].score < max(theScores):
                    pass
                elif teamsRemain[0].score == max(
                        theScores) and theScores.count(max(theScores)) > 1:
                    pass
                else:
                    self._round_end_timer = bs.Timer(0.5, self.end_game)
            else:
                self._round_end_timer = bs.Timer(0.5, self.end_game)

    def spawn_zombie(self) -> None:
        #We need a Z height...
        thePt = list(self.get_random_point_in_play())
        thePt2 = self.map.get_ffa_start_position(self.players)
        thePt[1] = thePt2[1]
        bs.timer(0.1, bs.Call(
            self._bots.spawn_bot, BrawlerBot, pos=thePt, spawn_time=1.0))

    def _onSpazBotDied(self,DeathMsg) -> None:
        #Just in case we are over max...
        if len(self._bots.get_living_bots()) < self._max_zombies:
            self.zombieQ += 1

            if DeathMsg.killerplayer is None:
                pass
            else:
                player = DeathMsg.killerplayer
                if not player:
                    return
                if player.lives < 1:
                    return
                player.team.score += 1
                self.zombieQ += 1
                self._update_scoreboard()

    def get_random_point_in_play(self) -> None:
        myMap = self.map.getname()
        if myMap == 'Doom Shroom':
            while True:
                x = random.uniform(-1.0,1.0)
                y = random.uniform(-1.0,1.0)
                if x*x+y*y < 1.0: break
            return ((8.0*x,8.0,-3.5+5.0*y))
        elif myMap == 'Rampage':
            x = random.uniform(-6.0,7.0)
            y = random.uniform(-6.0,-2.5)
            return ((x, 8.0, y))
        elif myMap == 'Hockey Stadium':
            x = random.uniform(-11.5,11.5)
            y = random.uniform(-4.5,4.5)
            return ((x, 5.0, y))
        elif myMap == 'Courtyard':
            x = random.uniform(-4.3,4.3)
            y = random.uniform(-4.4,0.3)
            return ((x, 8.0, y))
        elif myMap == 'Crag Castle':
            x = random.uniform(-6.7,8.0)
            y = random.uniform(-6.0,0.0)
            return ((x, 12.0, y))
        elif myMap == 'Big G':
            x = random.uniform(-8.7,8.0)
            y = random.uniform(-7.5,6.5)
            return ((x, 8.0, y))
        elif myMap == 'Football Stadium':
            x = random.uniform(-12.5,12.5)
            y = random.uniform(-5.0,5.5)
            return ((x, 8.0, y))
        else:
            x = random.uniform(-5.0,5.0)
            y = random.uniform(-6.0,0.0)
            return ((x, 8.0, y))

    def _update_scoreboard(self) -> None:
        for team in self.teams:
            self._scoreboard.set_team_value(team, team.score)

    def _get_living_teams(self) -> list[Team]:
        return [
            team for team in self.teams
            if len(team.players) > 0 and any(player.lives > 0
                                             for player in team.players)
        ]

    def end_game(self) -> None:
        if self.has_ended():
            return
        setattr(BrawlerBot, 'color', (0.6, 0.6, 0.6))
        setattr(BrawlerBot, 'highlight', (0.6, 0.6, 0.6))
        setattr(BrawlerBot, 'character', 'Kronk')
        results = bs.GameResults()
        self._vs_text = None  # Kill our 'vs' if its there.
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)


# ba_meta export bascenev1.GameActivity
class ZombieHordeCoop(ZombieHorde):

    name = 'Zombie Horde'

    @classmethod
    def get_supported_maps(cls, sessiontype: type[bs.Session]) -> list[str]:
        return ['Football Stadium']

    @classmethod
    def supports_session_type(cls, sessiontype: type[bs.Session]) -> bool:
        return (issubclass(sessiontype, bs.CoopSession))

    def _update(self) -> None:
        if self.zombieQ > 0:
            self.zombieQ -= 1
            self.spawn_zombie()

        if not any(player.is_alive() for player in self.teams[0].players):
            self._round_end_timer = bs.Timer(0.5, self.end_game)

    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, bs.PlayerDiedMessage):
            # Augment standard behavior.
            bs.TeamGameActivity.handlemessage(self, msg)
            player: Player = msg.getplayer(Player)
            # If we have any icons, update their state.
            for icon in player.icons:
                icon.handle_player_died()
        else:
            super().handlemessage(msg)


# ba_meta export plugin
class ZombieHordeLevel(babase.Plugin):
    def on_app_running(self) -> None:
        bs.app.classic.add_coop_practice_level(
            bs.Level(
                'Zombie Horde',
                gametype=ZombieHordeCoop,
                settings={},
                preview_texture_name='footballStadiumPreview',
            )
        )
        bs.app.classic.add_coop_practice_level(
            bs.Level(
                'Zombie Horde Epic',
                gametype=ZombieHordeCoop,
                settings={'Epic Mode': True},
                preview_texture_name='footballStadiumPreview',
            )
        )
