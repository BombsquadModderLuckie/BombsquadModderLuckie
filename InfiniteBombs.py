# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 8

from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

import babase
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib import popup
from bauiv1lib import confirm
from bascenev1lib.actor import playerspaz
from bascenev1lib.actor.bomb import Bomb, BombFactory, ExplodeMessage
from bascenev1lib.actor.spaz import BombDiedMessage
from bascenev1lib.actor.spazfactory import SpazFactory
from bascenev1lib.mainmenu import MainMenuSession

if TYPE_CHECKING:
	from typing import Any, Callable


class ModInfo:
	cfgname = 'Infinite Bombs' # config name
	cfglist = {
		'tnt': False,
		'tnt_explosive': False,
		'enable_mod': True,
	} # config list
	url = 'https://youtu.be/Q2GlQ3lFF0U' # video


class ModLang:
	lang = babase.app.lang.language
	if lang == 'Spanish':
		title = 'Opciones del Mod'
		youtube = (
			'¿Estás seguro?\n'
			'Te llevará a un vídeo de YouTube.'
		)
		enable = 'Bombas Infinitas'
		tnt = 'Usar TNT como bomba'
		tnt_explosive = 'Usar TNT explosiva como bomba'
	elif lang == 'Chinese':
		title = '模组设置'
		youtube = (
			'你确定吗？\n'
			'它将带您观看 YouTube 视频。'
		)
		enable = '无限炸弹'
		tnt = '用TNT作为泵'
		tnt_explosive = '使用爆炸性TNT作为泵'
	elif lang == 'Portuguese':
		title = 'Configurações de mod'
		youtube = (
			'Tem certeza?\n'
			'Isso o levará a um vídeo do YouTube.'
		)
		enable = 'Bombas infinitas'
		tnt = 'Use TNT como uma bomba'
		tnt_explosive = 'Use TNT explosivo como uma bomba'
	elif lang == 'French':
		title = 'Paramètres du mod'
		youtube = (
			'Es-tu sûr?\n'
			'Cela vous emmènera dans une vidéo YouTube.'
		)
		enable = 'Bombes infinies'
		tnt = 'Utilisez TNT comme bombe'
		tnt_explosive = 'Utilisez un TNT explosif comme bombe'
	elif lang == 'Russian':
		title = 'Мод настройки'
		youtube = (
			'Вы уверены?\n'
			'Это перенесет вас на видео на YouTube.'
		)
		enable = 'Бесконечные бомбы'
		tnt = 'Используйте TNT в качестве бомбы'
		tnt_explosive = 'Используйте взрывной TNT в качестве бомбы'
	else:
		title = 'Mod Settings'
		youtube = (
			'Are you sure?\n'
			'It will take you to a YouTube video.'
		)
		enable = 'Infinite Bombs'
		tnt = 'Use TNT as a bomb'
		tnt_explosive = 'Use explosive TNT as a bomb'
		

class ModSettingsPopup(popup.PopupWindow):

	def __init__(self):
		uiscale = bui.app.ui_v1.uiscale
		self._transitioning_out = False
		self._width = 480
		self._height = 260
		bg_color = (0.4, 0.37, 0.49)

		# creates our _root_widget
		super().__init__(
			position=(0.0, 0.0),
			size=(self._width, self._height),
			scale=(
				2.06
				if uiscale is bui.UIScale.SMALL
				else 1.4
				if uiscale is bui.UIScale.MEDIUM
				else 1.0
			),
			bg_color=bg_color,
		)

		self._cancel_button = bui.buttonwidget(
			parent=self.root_widget,
			position=(34, self._height - 48),
			size=(50, 50),
			scale=0.7,
			label='',
			color=bg_color,
			on_activate_call=self._on_cancel_press,
			autoselect=True,
			icon=bui.gettexture('crossOut'),
			iconscale=1.2)
		bui.containerwidget(edit=self.root_widget,
						   cancel_button=self._cancel_button)

		if ModInfo.url != '':
			url_button = bui.buttonwidget(
				parent=self.root_widget,
				position=(self._width - 86, self._height - 51),
				size=(82, 82),
				scale=0.5,
				label='',
				color=(1.1, 0.0, 0.0),
				on_activate_call=self._youtube,
				autoselect=True,
				icon=bui.gettexture('startButton'),
				iconscale=1.83,
				icon_color=(1.3, 1.3, 1.3))

		title = bui.textwidget(
			parent=self.root_widget,
			position=(self._width * 0.49, self._height - 27 - 5),
			size=(0, 0),
			h_align='center',
			v_align='center',
			scale=1.0,
			text=ModLang.title,
			maxwidth=self._width * 0.6,
			color=bui.app.ui_v1.title_color)

		checkbox_size = (self._width * 0.73, 50)
		checkbox_maxwidth = 310
		checkbox_posx = self._width * 0.13
		checkbox_space = 52
		
		v = 0
		v += 125
		bui.checkboxwidget(
			parent=self.root_widget,
			position=(checkbox_posx, self._height - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=bui.app.config[ModInfo.cfgname]['tnt'],
			text=ModLang.tnt,
			on_value_change_call=self._tnt,
		)
		v += checkbox_space
		bui.checkboxwidget(
			parent=self.root_widget,
			position=(checkbox_posx, self._height - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=bui.app.config[ModInfo.cfgname]['tnt_explosive'],
			text=ModLang.tnt_explosive,
			on_value_change_call=self._tnt_explosive,
		)
		v += checkbox_space
		bui.checkboxwidget(
			parent=self.root_widget,
			position=(checkbox_posx, self._height - v),
			size=checkbox_size,
			autoselect=True,
			maxwidth=checkbox_maxwidth,
			scale=1.0,
			textcolor=(0.8, 0.8, 0.8),
			value=bui.app.config[ModInfo.cfgname]['enable_mod'],
			text=ModLang.enable,
			on_value_change_call=self._enable_mod,
		)

	def _tnt(self, val: bool) -> None:
		bui.app.config[ModInfo.cfgname]['tnt'] = val
		bui.app.config.apply_and_commit()
		self._update_mod()

	def _tnt_explosive(self, val: bool) -> None:
		bui.app.config[ModInfo.cfgname]['tnt_explosive'] = val
		bui.app.config.apply_and_commit()
		self._update_mod()

	def _enable_mod(self, val: bool) -> None:
		bui.app.config[ModInfo.cfgname]['enable_mod'] = val
		bui.app.config.apply_and_commit()
		self._update_mod()
		
	def _update_mod(self) -> None:
		activity = bs.get_foreground_host_activity()
		session = bs.get_foreground_host_session()
		if not isinstance(session, MainMenuSession):
			with activity.context:
				if not activity.players:
					return
				for player in activity.players:
					if not player.is_alive():
						continue
					if player.actor.triple_bombs:
						player.actor.set_bomb_count(3)
					else:
						player.actor.set_bomb_count(1)

	def _youtube(self) -> None:
		confirm.ConfirmWindow(
			ModLang.youtube,
			action=self._open_url,
			width=380,
			height=120,
		)

	def _open_url(self) -> None:
		bui.open_url(ModInfo.url)

	def _on_cancel_press(self) -> None:
		self._transition_out()

	def _transition_out(self) -> None:
		if not self._transitioning_out:
			self._transitioning_out = True
			bui.containerwidget(edit=self.root_widget, transition='out_scale')

	def on_popup_cancel(self) -> None:
		bui.getsound('swish').play()
		self._transition_out()


class CustomMod:
	def __init__(self) -> None:
		playerspaz.PlayerSpaz = NewPlayerSpaz


# ba_meta export plugin
class ModPlugin(babase.Plugin):

	def on_app_running(self) -> None:
		self.setup_config()
		#self.custom_mod()
		class NewPlayerSpaz(playerspaz.PlayerSpaz):

			def __init__(self, **kwargs):
				super().__init__(**kwargs)
				self.triple_bombs: bool = False

			def drop_bomb(self) -> Bomb | None:
				tnt = babase.app.config[ModInfo.cfgname]['tnt']
				tnt_explosive = babase.app.config[ModInfo.cfgname]['tnt_explosive']
				if tnt or tnt_explosive:
					if (self.land_mine_count <= 0 and self.bomb_count <= 0) or self.frozen:
						return None
					assert self.node
					pos = self.node.position_forward
					vel = self.node.velocity

					dropping_bomb = True
					bomb_type = 'tnt'

					bomb = Bomb(
						position=(pos[0], pos[1] - 0.0, pos[2]),
						velocity=(vel[0], vel[1], vel[2]),
						bomb_type=bomb_type,
						blast_radius=self.blast_radius,
						source_player=self.source_player,
						owner=self.node,
					).autoretain()

					assert bomb.node
					if dropping_bomb:
						if not babase.app.config[ModInfo.cfgname]['enable_mod']:
							self.bomb_count -= 1
						bomb.node.add_death_action(
							bs.WeakCall(self.handlemessage, BombDiedMessage())
						)
					self._pick_up(bomb.node)

					for clb in self._dropped_bomb_callbacks:
						clb(self, bomb)

					factory = BombFactory.get()
					def _handle_impact() -> None:
						node = bs.getcollision().opposingnode
						node_delegate = node.getdelegate(object)
						if node:
							if bomb.bomb_type == 'tnt' and (
								node is bomb.owner
								or (
									isinstance(node_delegate, Bomb)
									and node_delegate.bomb_type == 'tnt'
									and node_delegate.owner is bomb.owner
								)
							):
								return
							bomb.handlemessage(ExplodeMessage())
					
					if tnt_explosive:
						bomb._add_material(factory.impact_blast_material)
						bomb._handle_impact = _handle_impact
				else:
					super().drop_bomb()
				if babase.app.config[ModInfo.cfgname]['enable_mod']:
					if self.land_mine_count > 0:
						self.set_land_mine_count(3)
					else:
						self.bomb_count = 1

			def _multi_bomb_wear_off(self) -> None:
				super()._multi_bomb_wear_off()
				self.triple_bombs = False
			
			def handlemessage(self, msg: Any) -> Any:
				if isinstance(msg, bs.PowerupMessage):
					bombs = ['impact_bombs','impact_bombs','sticky_bombs','ice_bombs']
					if msg.poweruptype in bombs:
						super().handlemessage(msg)
						if babase.app.config[ModInfo.cfgname]['enable_mod']:
							self.set_land_mine_count(0)
					elif msg.poweruptype == 'triple_bombs':
						super().handlemessage(msg)
						self.triple_bombs = True
					else:
						super().handlemessage(msg)
				elif isinstance(msg, BombDiedMessage):
					super().handlemessage(msg)
					if not babase.app.config[ModInfo.cfgname]['enable_mod']:
						if self.triple_bombs:
							if self.bomb_count > 3:
								old_count = self.bomb_count - 3
								self.bomb_count -= old_count
						else:
							if self.bomb_count > 1:
								old_count = self.bomb_count - 1
								self.bomb_count -= old_count
				else:
					super().handlemessage(msg)
		playerspaz.PlayerSpaz = NewPlayerSpaz

	def custom_mod(self) -> None:
		CustomMod()

	def installcfg(self) -> None:
		babase.app.config[ModInfo.cfgname] = ModInfo.cfglist
		babase.app.config.apply_and_commit()

	def setup_config(self) -> None:
		if ModInfo.cfgname in babase.app.config:
			for key in ModInfo.cfglist.keys():
				if not key in babase.app.config[ModInfo.cfgname]:
					self.installcfg()
					break
		else:
			self.installcfg()

	def has_settings_ui(self) -> bool:
		return True

	def show_settings_ui(self, source_widget: babase.Widget | None) -> None:
		ModSettingsPopup()