# Better replay controls by Froshlee14
# ba_meta require api 8

import babase as ba
import bauiv1 as bui
import bascenev1 as bs
from bauiv1lib.confirm import QuitWindow
from bauiv1lib.store.button import StoreButton
from bauiv1lib.mainmenu import MainMenuWindow

MainMenuWindow._old_refresh = MainMenuWindow._refresh
def _new_refresh(self) -> None:

        self._old_refresh()
        
        if bs.is_in_replay():
            
            positions: list[tuple[float, float, float]] = []
            self._p_index = 2
        
            h, v, scale = self._refresh_in_game(positions)
            
            children = self._root_widget.get_children()
            for child in children:
                child.delete()
            
            width = 380
            height = 100
            b_size = 50.0
            b_buffer = 10.0
            t_scale = 0.75
            spacing = 25
            assert bui.app.classic is not None
            uiscale = bui.app.ui_v1.uiscale
            if uiscale is bui.UIScale.SMALL:
                width *= 0.6
                height *= 0.6
                b_size *= 0.6
                b_buffer *= 1.0
                v_offs = -40
                t_scale = 0.5
                spacing = 15
            elif uiscale is bui.UIScale.MEDIUM:
                v_offs = -70
                spacing = 20
            else:
                v_offs = -100
                
            self._subContainer = bui.containerwidget(parent=self._root_widget,
                                                size=(width,height),
                                                position=((self._width*0.5)-(width*0.5), v - b_size + v_offs - b_buffer ),
                                                background=False)
            
            btn = bui.buttonwidget(
                    parent=self._subContainer,
                    position=(0,0),
                    size=(width, height),
                    enable_sound=False,
                    color=(0.53, 0.45, 0.58),
                    selectable=False,
                    enabled=False,
                    label='')
                
                
            self._replay_speed_text = bui.textwidget( parent=self._subContainer,
                text=bui.Lstr(
                    resource='watchWindow.playbackSpeedText',
                    subs=[('${SPEED}', str(1.23))],
                ),
                position=(0,height+10),
                h_align='center',
                v_align='center',
                size=(width, 0),
                scale=t_scale,
            )

            # Update to current value.
            self._change_replay_speed(0)

            # Keep updating in a timer in case it gets changed elsewhere.
            self._change_replay_speed_timer = bui.AppTimer(
                0.25, bui.WeakCall(self._change_replay_speed, 0), repeat=True
            )
            
            h2 = v2 = spacing
            
            backbtn = bui.buttonwidget(
                parent=self._subContainer,
                position=(h2,v2),
                button_type='square',
                size=(b_size, b_size),
                label='',
                autoselect=True,
                on_activate_call=self._confirm_end_replay,
            )
            bui.containerwidget(edit=self._root_widget, cancel_button=backbtn)
            
            bui.imagewidget(parent=self._subContainer,
                size=(b_size*0.9, b_size*0.9),
                draw_controller=backbtn, 
                #color=(1,0,0),
                position=(h2+3, v2+2),
                texture=bui.gettexture('textClearButton'))
            
            h2 += b_size + spacing*0.8
            
            minusbtn = bui.buttonwidget(
                parent=self._subContainer,
                position=(h2,v2),
                button_type='square',
                size=(b_size, b_size),
                label='',
                autoselect=True,
                on_activate_call=bui.Call(self._change_replay_speed, -1),
            )
            
            bui.imagewidget(parent=self._subContainer,
                size=(b_size, b_size),
                draw_controller=minusbtn, 
                #color=(1,0,0),
                position=(h2, v2),
                texture=bui.gettexture('leftButton'))
            
            h2 += b_size + spacing*0.8
            
            minusbtn = bui.buttonwidget(
                parent=self._subContainer,
                position=(h2,v2),
                button_type='square',
                size=(b_size, b_size),
                label='',
                autoselect=True,
                on_activate_call=self._resume,
            )
            
            bui.imagewidget(parent=self._subContainer,
                size=(b_size, b_size),
                draw_controller=minusbtn, 
                #color=(1,0,0),
                position=(h2, v2),
                texture=bui.gettexture('startButton'))
            
            h2 += b_size + spacing*0.8


            plusbtn = bui.buttonwidget(
                parent=self._subContainer,
                position=(h2,v2),
                button_type='square',
                size=(b_size, b_size),
                label='',
                autoselect=True,
                on_activate_call=bui.Call(self._change_replay_speed, 1),
            )
            
            bui.imagewidget(parent=self._subContainer,
                size=(b_size, b_size),
                draw_controller=plusbtn, 
                #color=(1,0,0),
                position=(h2, v2),
                texture=bui.gettexture('rightButton'))
            
            h2 += b_size + spacing*0.8
            
            self._settings_button =setbtn = bui.buttonwidget(
                parent=self._subContainer,
                position=(h2,v2),
                button_type='square',
                size=(b_size, b_size),
                label='',
                color = (0.2,0.5,1),
                autoselect=True,
                on_activate_call=self._settings,
            )
            
            bui.imagewidget(parent=self._subContainer,
                size=(b_size, b_size),
                draw_controller=setbtn, 
                #color=(1,0,0),
                position=(h2, v2),
                texture=bui.gettexture('settingsIcon'))

            bui.containerwidget(edit=self._root_widget,background=False)

# ba_meta export plugin

class BetterReplayControls(ba.Plugin):
    logo_tex = "tv"

    def on_app_running(self) -> None:
        MainMenuWindow._refresh = _new_refresh

    