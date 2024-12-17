# To learn more, see https://ballistica.net/wiki/meta-tag-system
# ba_meta require api 8

from __future__ import annotations

from typing import TYPE_CHECKING

import math
import babase
from bauiv1lib.popup import PopupWindow
from bauiv1lib.playlist import mapselect
from bauiv1lib import characterpicker, confirm
import bauiv1 as bui

if TYPE_CHECKING:
	from typing import Any, Callable, Sequence
	import bascenev1 as bs


class ModLang:
	def __init__(self) -> None:
		lang = babase.app.lang.language
		if lang == 'Spanish':
			self.more = 'Obtener Más Mods...'
			self.web = (
				'¿Estás seguro?\n'
				'Te llevará a una página web.'
			)
		elif lang == 'Chinese':
			self.more = '获取更多mod...'
			self.web = (
				'你确定吗？\n'
				'它将带您到网站。'
			)
		else:
			self.more = 'Get More Mods...'
			self.web = (
				'Are you sure?\n'
				'It will take you to a website.'
			)
				

class PlaylistMapSelectWindow(mapselect.PlaylistMapSelectWindow):
	"""Window to select a map."""

	def __init__(
		self,
		gametype: type[bs.GameActivity],
		sessiontype: type[bs.Session],
		config: dict[str, Any],
		edit_info: dict[str, Any],
		completion_call: Callable[[dict[str, Any] | None], Any],
		transition: str = 'in_right',
	):
		from bascenev1 import get_filtered_map_name

		self._gametype = gametype
		self._sessiontype = sessiontype
		self._config = config
		self._completion_call = completion_call
		self._edit_info = edit_info
		self._maps: list[tuple[str, bui.Texture]] = []
		try:
			self._previous_map = get_filtered_map_name(
				config['settings']['map']
			)
		except Exception:
			self._previous_map = ''

		assert bui.app.classic is not None
		uiscale = bui.app.ui_v1.uiscale
		width = 1080
		height = 640

		bui.Window.__init__(self,
			root_widget=bui.containerwidget(
				size=(width, height),
				transition=transition,
				scale=1.3
			)
		)

		self._cancel_button = btn = bui.buttonwidget(
			parent=self._root_widget,
			position=(138, height - 67 - 45),
			size=(140, 50),
			scale=0.9,
			text_scale=1.0,
			autoselect=True,
			label=bui.Lstr(resource='cancelText'),
			on_activate_call=self._cancel,
		)

		bui.containerwidget(edit=self._root_widget, cancel_button=btn)
		bui.textwidget(
			parent=self._root_widget,
			position=(width * 0.5, height - 46 - 45),
			size=(0, 0),
			maxwidth=260,
			scale=1.1,
			text=bui.Lstr(
				resource='mapSelectTitleText',
				subs=[('${GAME}', self._gametype.get_display_string())],
			),
			color=bui.app.ui_v1.title_color,
			h_align='center',
			v_align='center',
		)
		v = height - 120
		self._scroll_width = width - (80 + 2) - 130
		self._scroll_height = height - 190

		self._scrollwidget = bui.scrollwidget(
			parent=self._root_widget,
			position=(106, v - self._scroll_height),
			size=(self._scroll_width, self._scroll_height),
		)
		bui.containerwidget(
			edit=self._root_widget, selected_child=self._scrollwidget
		)
		bui.containerwidget(edit=self._scrollwidget, claims_left_right=True)

		self._subcontainer: bui.Widget | None = None
		self._refresh()

	def _refresh(self, select_get_more_maps_button: bool = False) -> None:
		# pylint: disable=too-many-statements
		# pylint: disable=too-many-branches
		# pylint: disable=too-many-locals
		from bascenev1 import (
			get_map_class,
			get_map_display_string,
		)

		assert bui.app.classic is not None
		store = bui.app.classic.store
		# Kill old.
		if self._subcontainer is not None:
			self._subcontainer.delete()

		mesh_opaque = bui.getmesh('level_select_button_opaque')
		mesh_transparent = bui.getmesh('level_select_button_transparent')

		self._maps = []
		map_list = self._gametype.get_supported_maps(self._sessiontype)
		map_list_sorted = list(map_list)
		map_list_sorted.sort()
		unowned_maps = store.get_unowned_maps()

		for mapname in map_list_sorted:
			# Disallow ones we don't own.
			if mapname in unowned_maps:
				continue
			map_tex_name = get_map_class(mapname).get_preview_texture_name()
			if map_tex_name is not None:
				try:
					map_tex = bui.gettexture(map_tex_name)
					self._maps.append((mapname, map_tex))
				except Exception:
					print(f'Invalid map preview texture: "{map_tex_name}".')
			else:
				print('Error: no map preview texture for map:', mapname)

		uiscale = bui.app.ui_v1.uiscale

		count = len(self._maps)
		columns = 4 if uiscale is bui.UIScale.SMALL else 5
		rows = int(math.ceil(float(count) / columns))
		button_width = 192 if uiscale is bui.UIScale.SMALL else 150
		button_height = button_width * 0.5
		button_buffer_h = 7
		button_buffer_v = 15
		self._sub_width = self._scroll_width * 0.95
		self._sub_height = (
			5 + rows * (button_height + 2 * button_buffer_v) +
			85 if uiscale is bui.UIScale.SMALL else 495
		)
		self._subcontainer = bui.containerwidget(
			parent=self._scrollwidget,
			size=(self._sub_width, self._sub_height),
			background=False,
		)
		index = 0
		mask_texture = bui.gettexture('mapPreviewMask')
		h_offs = 130 if len(self._maps) == 1 else 0
		for y in range(rows):
			for x in range(columns):
				pos = (
					x * (button_width + 2 * button_buffer_h)
					+ button_buffer_h
					+ h_offs
					+ 13,
					self._sub_height
					- (y + 1) * (button_height + 2 * button_buffer_v)
					+ 12,
				)
				btn = bui.buttonwidget(
					parent=self._subcontainer,
					button_type='square',
					size=(button_width, button_height),
					autoselect=True,
					texture=self._maps[index][1],
					mask_texture=mask_texture,
					mesh_opaque=mesh_opaque,
					mesh_transparent=mesh_transparent,
					label='',
					color=(1, 1, 1),
					on_activate_call=bui.Call(
						self._select_with_delay, self._maps[index][0]
					),
					position=pos,
				)
				if x == 0:
					bui.widget(edit=btn, left_widget=self._cancel_button)
				if y == 0:
					bui.widget(edit=btn, up_widget=self._cancel_button)
				if x == columns - 1 and bui.app.ui_v1.use_toolbars:
					bui.widget(
						edit=btn,
						right_widget=bui.get_special_widget('party_button'),
					)

				bui.widget(edit=btn, show_buffer_top=60, show_buffer_bottom=60)
				if self._maps[index][0] == self._previous_map:
					bui.containerwidget(
						edit=self._subcontainer,
						selected_child=btn,
						visible_child=btn,
					)
				name = get_map_display_string(self._maps[index][0])
				bui.textwidget(
					parent=self._subcontainer,
					text=name,
					position=(pos[0] + button_width * 0.5, pos[1] - 12),
					size=(0, 0),
					scale=0.5,
					maxwidth=button_width,
					draw_controller=btn,
					h_align='center',
					v_align='center',
					color=(0.8, 0.8, 0.8, 0.8),
				)
				index += 1

				if index >= count:
					break
			if index >= count:
				break
		self._get_more_maps_button = btn = bui.buttonwidget(
			parent=self._subcontainer,
			size=(self._sub_width * 0.48,
	 			55 if uiscale is bui.UIScale.SMALL else 40),
			position=(self._sub_width * 0.032, 15),
			label=bui.Lstr(resource='mapSelectGetMoreMapsText'),
			on_activate_call=self._on_store_press,
			color=(0.6, 0.53, 0.63),
			textcolor=(0.75, 0.7, 0.8),
			autoselect=True,
			text_scale=1.0 if uiscale is bui.UIScale.SMALL else 0.75,
		)
		self._get_more_mods_button = btn = bui.buttonwidget(
			parent=self._subcontainer,
			size=(self._sub_width * 0.48,
	 			55 if uiscale is bui.UIScale.SMALL else 40),
			position=(self._sub_width * 0.522, 15),
			label=ModLang().more,
			on_activate_call=self._on_mods_press,
			color=(0.2, 0.6, 0.8),
			textcolor=(0.8, 0.8, 0.8),
			autoselect=True,
			text_scale=1.0 if uiscale is bui.UIScale.SMALL else 0.75,
		)
		bui.buttonwidget(
			edit=self._get_more_maps_button,
			right_widget=self._get_more_mods_button,
		)
		bui.buttonwidget(
			edit=self._get_more_mods_button,
			left_widget=self._get_more_maps_button,
		)
		bui.widget(edit=btn, show_buffer_top=30, show_buffer_bottom=30)
		if select_get_more_maps_button:
			bui.containerwidget(
				edit=self._subcontainer, selected_child=btn, visible_child=btn
			)

	def _on_mods_press(self) -> None:
		confirm.ConfirmWindow(
			ModLang().web,
			action=self._open_url,
			width=380,
			height=120,
			origin_widget=self._get_more_mods_button,
		)

	def _open_url(self) -> None:
		bui.open_url('https://agelgzman.wixsite.com/bombsquad-mods/mapas')


class CharacterPicker(characterpicker.CharacterPicker):
	"""Popup window for selecting characters."""

	def __init__(
		self,
		parent: bui.Widget,
		position: tuple[float, float] = (0.0, 0.0),
		delegate: Any = None,
		scale: float | None = None,
		offset: tuple[float, float] = (0.0, 0.0),
		tint_color: Sequence[float] = (1.0, 1.0, 1.0),
		tint2_color: Sequence[float] = (1.0, 1.0, 1.0),
		selected_character: str | None = None,
	):
		# pylint: disable=too-many-locals
		from bascenev1lib.actor import spazappearance

		assert bui.app.classic is not None

		del parent  # unused here
		uiscale = bui.app.ui_v1.uiscale
		if scale is None:
			scale = (
				1.85
				if uiscale is bui.UIScale.SMALL
				else 1.65
				if uiscale is bui.UIScale.MEDIUM
				else 1.23
			)

		self._delegate = delegate
		self._transitioning_out = False

		# make a list of spaz icons
		self._spazzes = spazappearance.get_appearances()
		self._spazzes.sort()
		self._icon_textures = [
			bui.gettexture(bui.app.classic.spaz_appearances[s].icon_texture)
			for s in self._spazzes
		]
		self._icon_tint_textures = [
			bui.gettexture(
				bui.app.classic.spaz_appearances[s].icon_mask_texture
			)
			for s in self._spazzes
		]

		count = len(self._spazzes)

		uiscale = bui.app.ui_v1.uiscale

		columns = 7 if uiscale is bui.UIScale.SMALL else 10
		rows = int(math.ceil(float(count) / columns))

		button_width = 100
		button_height = 100
		button_buffer_h = 10
		button_buffer_v = 15

		self._width = 10 + columns * (button_width + 2 * button_buffer_h) * (
			1.0 / 0.95
		) * (1.0 / 0.8)
		self._height = self._width * 0.57

		self._scroll_width = self._width * 0.8
		self._scroll_height = self._height * 0.8
		self._scroll_position = (
			(self._width - self._scroll_width) * 0.5,
			(self._height - self._scroll_height) * 0.5,
		)

		# Creates our _root_widget.
		PopupWindow.__init__(self,
			position=position,
			size=(self._width, self._height),
			scale=scale,
			bg_color=(0.5, 0.5, 0.5),
			offset=offset,
			focus_position=self._scroll_position,
			focus_size=(self._scroll_width, self._scroll_height),
		)

		self._scrollwidget = bui.scrollwidget(
			parent=self.root_widget,
			size=(self._scroll_width, self._scroll_height),
			color=(0.55, 0.55, 0.55),
			highlight=False,
			position=self._scroll_position,
		)
		bui.containerwidget(edit=self._scrollwidget, claims_left_right=True)

		self._sub_width = self._scroll_width * 0.95
		self._sub_height = (
			5 + rows * (button_height + 2 * button_buffer_v) + 100
		)
		self._subcontainer = bui.containerwidget(
			parent=self._scrollwidget,
			size=(self._sub_width, self._sub_height),
			background=False,
		)
		index = 0
		mask_texture = bui.gettexture('characterIconMask')
		for y in range(rows):
			for x in range(columns):
				pos = (
					x * (button_width + 2 * button_buffer_h) + button_buffer_h + 25,
					self._sub_height
					- (y + 1) * (button_height + 2 * button_buffer_v)
					+ 4,
				)
				btn = bui.buttonwidget(
					parent=self._subcontainer,
					button_type='square',
					size=(button_width, button_height),
					autoselect=True,
					texture=self._icon_textures[index],
					tint_texture=self._icon_tint_textures[index],
					mask_texture=mask_texture,
					label='',
					color=(1, 1, 1),
					tint_color=tint_color,
					tint2_color=tint2_color,
					on_activate_call=bui.Call(
						self._select_character, self._spazzes[index]
					),
					position=pos,
				)
				bui.widget(edit=btn, show_buffer_top=60, show_buffer_bottom=60)
				if self._spazzes[index] == selected_character:
					bui.containerwidget(
						edit=self._subcontainer,
						selected_child=btn,
						visible_child=btn,
					)
				name = bui.Lstr(
					translate=('characterNames', self._spazzes[index])
				)
				bui.textwidget(
					parent=self._subcontainer,
					text=name,
					position=(pos[0] + button_width * 0.5, pos[1] - 12),
					size=(0, 0),
					scale=0.5,
					maxwidth=button_width,
					draw_controller=btn,
					h_align='center',
					v_align='center',
					color=(0.8, 0.8, 0.8, 0.8),
				)
				index += 1

				if index >= count:
					break
			if index >= count:
				break
		self._get_more_characters_button = btn = bui.buttonwidget(
			parent=self._subcontainer,
			size=(self._sub_width * 0.48, 60),
			position=(self._sub_width * 0.035, 15),
			label=bui.Lstr(resource='editProfileWindow.getMoreCharactersText'),
			on_activate_call=self._on_store_press,
			color=(0.6, 0.6, 0.6),
			textcolor=(0.8, 0.8, 0.8),
			autoselect=True,
		)
		self._get_more_mods_button = btn = bui.buttonwidget(
			parent=self._subcontainer,
			size=(self._sub_width * 0.48, 60),
			position=(self._sub_width * 0.525, 15),
			label=ModLang().more,
			on_activate_call=self._on_mods_press,
			color=(0.2, 0.6, 0.8),
			textcolor=(0.8, 0.8, 0.8),
			autoselect=True,
		)
		bui.buttonwidget(
			edit=self._get_more_characters_button,
			right_widget=self._get_more_mods_button,
		)
		bui.buttonwidget(
			edit=self._get_more_mods_button,
			left_widget=self._get_more_characters_button,
		)
		bui.widget(edit=btn, show_buffer_top=30, show_buffer_bottom=30)

	def _on_mods_press(self) -> None:
		confirm.ConfirmWindow(
			ModLang().web,
			action=self._open_url,
			width=380,
			height=120,
			origin_widget=self._get_more_mods_button,
		)

	def _open_url(self) -> None:
		bui.open_url('https://agelgzman.wixsite.com/bombsquad-mods/personajes')


# ba_meta export plugin
class ModPlugin(babase.Plugin):
	mapselect.PlaylistMapSelectWindow = PlaylistMapSelectWindow
	characterpicker.CharacterPicker = CharacterPicker