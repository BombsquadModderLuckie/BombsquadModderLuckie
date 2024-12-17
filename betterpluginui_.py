# Better plugin UI by Froshle14
# ba_meta require api 8

import babase as ba
import bauiv1 as bui
from bauiv1lib.settings.plugins import PluginWindow, Category

def _new_show_plugins(self) -> None:
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-statements
        plugspecs = bui.app.plugins.plugin_specs
        plugstates: dict[str, dict] = bui.app.config.setdefault('Plugins', {})
        assert isinstance(plugstates, dict)

        plug_line_height = 90
        sub_width = self._scroll_width
        num_enabled = 0
        num_disabled = 0

        plugspecs_sorted = sorted(plugspecs.items())

        for _classpath, plugspec in plugspecs_sorted:
            # counting number of enabled and disabled plugins
            # plugstate = plugstates.setdefault(plugspec[0], {})
            if plugspec.enabled:
                num_enabled += 1
            else:
                num_disabled += 1

        if self._category is Category.ALL:
            sub_height = len(plugspecs) * plug_line_height
            bui.containerwidget(
                edit=self._subcontainer, size=(self._scroll_width, sub_height)
            )
        elif self._category is Category.ENABLED:
            sub_height = num_enabled * plug_line_height
            bui.containerwidget(
                edit=self._subcontainer, size=(self._scroll_width, sub_height)
            )
        elif self._category is Category.DISABLED:
            sub_height = num_disabled * plug_line_height
            bui.containerwidget(
                edit=self._subcontainer, size=(self._scroll_width, sub_height)
            )
        else:
            # Make sure we handle all cases.
            assert_never(self._category)
            sub_height = 0

        num_shown = 0
        for classpath, plugspec in plugspecs_sorted:
            plugin = plugspec.plugin
            enabled = plugspec.enabled

            if self._category is Category.ALL:
                show = True
            elif self._category is Category.ENABLED:
                show = enabled
            elif self._category is Category.DISABLED:
                show = not enabled
            else:
                assert_never(self._category)
                show = False

            if not show:
                continue
            
            displayName = str(classpath)
            splitter = displayName.split('.')
            file = splitter[0]
            plugin_name = splitter[1]
            filename = file +'.py'

            item_y = sub_height - (num_shown + 1) * plug_line_height
            item_x = 10
            
            buttomWidth = self._scroll_width - 40
            logowitdh = plug_line_height - 40
            
            if hasattr(plugin, 'logo_tex'):
                logo_tex = plugin.logo_tex
            else:
                logo_tex = "file"
                
            if hasattr(plugin, 'logo_color'):
                logo_color= plugin.logo_color
            else:
                logo_color = (1,1,1)
                
            btn_color = (0.63, 0.55, 0.78)
            
            btn = bui.buttonwidget(
                    parent=self._subcontainer,
                    position=(item_x, item_y),
                    size=(buttomWidth, plug_line_height),
                    enable_sound=False,
                    color=btn_color,
                    selectable=False,
                    enabled=False,
                    label='')
                    
            logoImg = bui.imagewidget(parent=self._subcontainer,
                    position=(item_x+20, item_y+20),
                    size=(logowitdh,logowitdh),
                    color = logo_color,
                    texture=bui.gettexture(logo_tex))
            
            check = bui.checkboxwidget(
                parent=self._subcontainer,
                text=plugin_name,
                autoselect=True,
                value=enabled,
                maxwidth=self._scroll_width - 200,
                position=(item_x+logowitdh+25, item_y+plug_line_height-55),
                size=(self._scroll_width - 40, 50),
                on_value_change_call=bui.Call(
                    self._check_value_changed, plugspec
                ),
                textcolor=(
                    (0.8, 0.3, 0.3)
                    if (plugspec.attempted_load and plugspec.plugin is None)
                    else (0.6, 0.6, 0.6)
                    if plugspec.plugin is None
                    else (0, 1, 0)
                ),
            )
            
            filepath = bui.textwidget(parent=self._subcontainer,
                                         position=(item_x+logowitdh+35, item_y+15),
                                         size=(buttomWidth - 200, 10),
                                         maxwidth=buttomWidth - 200,
                                         text=filename,
                                         scale=0.8,
                                         color=(0.7,0.7,0.7),
                                         h_align='left',
                                         v_align='bottom')
            
            # noinspection PyUnresolvedReferences
            if plugin is not None and plugin.has_settings_ui():
                button = bui.buttonwidget(
                    parent=self._subcontainer,
                    button_type="square",
                    label=None,
                    size=(45, 45),
                    color=(0.2,0.5,1),
                    iconscale=1.25,
                    icon=bui.gettexture("settingsIcon"),
                    autoselect=True,
                    position=(sub_width-115, item_y+25),
                )
                # noinspection PyUnresolvedReferences
                bui.buttonwidget(
                    edit=button,
                    on_activate_call=bui.Call(plugin.show_settings_ui, button),
                )
            else:
                button = None

            # Allow getting back to back button.
            if num_shown == 0:
                bui.widget(
                    edit=check,
                    up_widget=self._back_button,
                    left_widget=self._back_button,
                    right_widget=self._settings_button,
                )
                if button is not None:
                    bui.widget(edit=button, up_widget=self._back_button)

            # Make sure we scroll all the way to the end when using
            # keyboard/button nav.
            bui.widget(edit=check, show_buffer_top=40, show_buffer_bottom=40)
            num_shown += 1

# ba_meta export plugin

class BetterPluginUI(ba.Plugin):
    
    logo_tex = "graphicsIcon"

    def on_app_running(self) -> None:
        PluginWindow._show_plugins = _new_show_plugins

    