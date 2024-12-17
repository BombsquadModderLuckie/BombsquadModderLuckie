#Super colors plugin by Froshlee14
# ba_meta require api 8

from __future__ import annotations

import babase as ba
import bauiv1 as bui
import _babase as _ba
import bascenev1 as bs

import random, json

from bauiv1lib.popup import PopupWindow
from bascenev1lib.actor.bomb import Blast, BombFactory
from bascenev1lib.actor.spaz import Spaz
from bascenev1lib.gameutils import SharedObjects
from bascenev1lib.actor.playerspaz import PlayerSpaz
from bascenev1lib.actor.spazbot import SpazBot
from bascenev1._gameutils import animate, animate_array
from bauiv1lib.config import ConfigNumberEdit

from typing import TYPE_CHECKING, TypeVar, overload

if TYPE_CHECKING:
    from typing import Any, Sequence, Literal
    
    
app = _ba.app
path = app.python_directory_user +'\SuperColorsConfig.txt'

default_data = {
        "players":True,
        "bots":False,
        "bombs":True,
        "timer":0.5,
        "glow_scale":1.0,
}

def saveData(dict):
    import json
    with open(path, 'w') as file:
        file.write(json.dumps(dict))
    

def getData():
    try:
        with open(path) as f:
            data = f.read()
            js = json.loads(data)
            #print(js)
            return js
    except Exception:
        output = None

if getData() == None:
    saveData(default_data)
    
def updateData():
    try:
        with open(path) as f:
            data = f.read()
            stored_data = json.loads(data)

        changes_made = False

        for key, value in default_data.items():
            if key not in stored_data:
                stored_data[key] = value
                changes_made = True
                print(f"Added: '{key}': {value}")

        keys_to_remove = []
        for key in stored_data.keys():
            if key not in default_data:
                keys_to_remove.append(key)
                changes_made = True
                print(f"Removed: '{key}'")

        for key in keys_to_remove:
            del stored_data[key]

        if changes_made:
            with open(path, 'w') as f:
                f.write(json.dumps(stored_data))
            ba.screenmessage("Super colors config updated.")

    except Exception as e:
        print("Error:", e)

updateData()
    

def getTranslation(text):
    actLan = _ba.app.lang.language
    colorsModsLan = {
        "title":{
            "Spanish":'Ajustes de Super Colors',
            "English":'Super Colors Settings'
        },
        "description":{
            "Spanish":'Aplicar efectos de color a:',
            "English":'Apply color effects to:'
        },
        "players":{
            "Spanish":'Jugadores',
            "English":'Players'
        },
        "bots":{
            "Spanish":'Maquinas',
            "English":'  Bots  '
        },
        "bombs":{
            "Spanish":'Bombas',
            "English":'Bombs'
        },
        "timer":{
            "Spanish":'Tiempo',
            "English":'Timer'
        },
        "glow":{
            "Spanish":'Brillo',
            "English":'Glow scale'
        },
        "apply":{
            "Spanish":'Aplicar',
            "English":'Apply'
        },
    }
    lans = ["Spanish","English"]
    if actLan not in lans:
        actLan = "English"
    return colorsModsLan[text][actLan]

def get_random_color(glow_scale=1.0):
    while True:
        red = random.random() 
        green = random.random()
        blue = random.random()
        
        brightness = (red + green + blue) / 3
        dark_threshold = 0.4
        
        if brightness > dark_threshold:
            return red* glow_scale, green* glow_scale, blue* glow_scale
    

PlayerSpaz.old_init_ = PlayerSpaz.__init__

def _new_player_init_(self,
        player: bs.Player,
        color: Sequence[float] = (1.0, 1.0, 1.0),
        highlight: Sequence[float] = (0.5, 0.5, 0.5),
        character: str = 'Spaz',
        powerups_expire: bool = True,
    ):
        
        self.old_init_(player, color, highlight, character, powerups_expire)
        
        data = getData()
        time = data["timer"]
        glow =data["glow_scale"]
        allow_players =data["players"]
        
        if not allow_players:
            return
        
        color = self.node.color
        self.node.color = (color[0]*glow,color[1]*glow,color[2]*glow)
        
        def change_color():
            if self.is_alive():
                old_color = self.node.color
                new_color = get_random_color(glow)
                bs.animate_array(self.node,'color',3,
                    {
                    0: old_color,
                    time: new_color,
                    },
                )
            else:
                self.update_timer = None
                   
        self._update_timer = bs.Timer(time,change_color, repeat=True)
        
        
Blast.old_init = Blast.__init__

def _new_blast_init_(self,
        position = (0.0, 1.0, 0.0),
        velocity = (0.0, 0.0, 0.0),
        blast_radius = 2.0,
        blast_type = 'normal',
        source_player = None,
        hit_type = 'explosion',
        hit_subtype = 'normal',
    ):

        self.old_init(position,velocity,blast_radius,blast_type,source_player,hit_type,hit_subtype)
        
        data = getData()
        allow_bombs = data["bombs"]
        
        if not allow_bombs:
            return
        
        new_color = get_random_color(1.0)
        lcolor = new_color 
        scl = random.uniform(0.6, 0.9)
        scorch_radius = light_radius = self.radius
        iscale = 1.6
        
        if self.blast_type == 'ice' or self.blast_type == 'tnt' :
            return
        
        light = bs.newnode('light',
            attrs={
                'position': position,
                'volume_intensity_scale': 10.0,
                'color': lcolor,
            },
        )
        
        bs.animate( light,'intensity',
            {
                0: 2.0 * iscale,
                scl * 0.02: 0.1 * iscale,
                scl * 0.025: 0.2 * iscale,
                scl * 0.05: 17.0 * iscale,
                scl * 0.06: 5.0 * iscale,
                scl * 0.08: 4.0 * iscale,
                scl * 0.2: 0.6 * iscale,
                scl * 2.0: 0.00 * iscale,
                scl * 3.0: 0.0,
            },
        )
        bs.animate(light,'radius',
            {
                0: light_radius * 0.2,
                scl * 0.05: light_radius * 0.55,
                scl * 0.1: light_radius * 0.3,
                scl * 0.3: light_radius * 0.15,
                scl * 1.0: light_radius * 0.05,
            },
        )
        bs.timer(scl * 3.0, light.delete)

        for i in range(2):
            scorch = bs.newnode('scorch',
                attrs={
                    'position': position,
                    'size': scorch_radius * 0.5,
                    'big': (self.blast_type == 'tnt'),
                },
            )
            scorch.color = new_color

            bs.animate(scorch, 'presence', {3.000: 1, 13.000: 0})
            bs.timer(13.0, scorch.delete)

SpazBot.old_init = SpazBot.__init__
def _new_bot_init_(self):
        self.old_init()
        
        data = getData()
        time = data["timer"]
        glow =data["glow_scale"]
        allow_bots =data["bots"]
        
        if not allow_bots:
            return
        
        color = self.node.highlight
        self.node.highlight = (color[0]*glow,color[1]*glow,color[2]*glow)
        
        def change_color():
            if self.is_alive():
                old_color = self.node.highlight
                new_color = get_random_color(glow)
                bs.animate_array(self.node,'highlight',3,
                    {
                    0: old_color,
                    time: new_color,
                    },
                )
            else:
                self.update_timer = None
                   
        self._update_timer = bs.Timer(time,change_color, repeat=True)

  
class SuperColorsWindow(PopupWindow):
    def __init__(self,transition='in_right'):
        self._width = width = 400
        self._height = height = 320
        self.imgScale = 230
        
        uiscale = ba.app.ui_v1.uiscale
        self.baseScale = 1.0 
        self.popupScale = self.baseScale* (2.4 if uiscale is ba.UIScale.SMALL else 1.5 if uiscale is ba.UIScale.MEDIUM else 1.0)

        self._img = None
        self._subContainer = None
        self._update_timer = None
        self._back_button = None
        
        self._lineup_tex = bui.gettexture('playerLineup')
        self._angry_computer_transparent_model = bui.getmesh( 'angryComputerTransparent')
        self._eyes_model = bui.getmesh('plasticEyesTransparent')

        self.data = getData()
        self._players = self.data["players"]
        self._bots = self.data["bots"]
        self._bombs = self.data["bombs"]
        self._timer = self.data["timer"]
        self._timer = self.data["glow_scale"]

        self._root_widget = bui.containerwidget(size=(width,height),transition=transition,
                                              scale=1.9 if uiscale is ba.UIScale.SMALL else 1.0,
                                              stack_offset=(0,-5) if uiscale is ba.UIScale.SMALL else (0,0))
                                              
        self._back_button = btn = bui.buttonwidget(
                parent=self._root_widget,
                autoselect=True,
                position=(25, height - 55),
                scale=0.8,
                text_scale=1.2,
                button_type='backSmall',
                size=(40, 40),
                label=bui.charstr(bui.SpecialChar.BACK),
                on_activate_call=self._back,
            )
        bui.containerwidget(edit=self._root_widget, cancel_button=btn)
                                              
        t = bui.textwidget(parent=self._root_widget,position=(0,height-60),size=(width,30),
                          text=getTranslation("title"),
                          h_align="center",color=ba.app.ui_v1.title_color,
                          v_align="center",maxwidth=260)
                          
        t2 = bui.textwidget(parent=self._root_widget,position=(0,height-105),size=(width,30),
                          text=getTranslation("description"),
                          h_align="center",color=ba.app.ui_v1.infotextcolor,
                          v_align="center",maxwidth=220)

        self.update()

    def update(self):

        if self._subContainer is not None and self._subContainer.exists():
            self._subContainer.delete()

        self._subContainer = bui.containerwidget(parent=self._root_widget,
                                                size=(self._width,self._height),
                                                background=False,
                                                selection_loops_to_parent=True)

        uiscale = ba.app.ui_v1.uiscale
        width = self._width
        height = self._height
        imgScale = self.imgScale
        
        bttnSize = 80
        bttnSpacing = 25
        v =  height - 110 - bttnSize
        h = 60
        iconSize = bttnSize*0.58
        
        textcolor = (1,1,1)
        disabled_color = 0.63, 0.55, 0.78
        
        self.users_button = users_button = bui.buttonwidget(parent=self._subContainer,position=(h,v),size=(bttnSize,bttnSize),
                        autoselect=True,button_type='square',color=disabled_color,label='',on_activate_call=self._set_players )
                        
        bui.imagewidget(parent=self._subContainer, size=(iconSize, iconSize),
                       draw_controller=users_button, #color=(1,0,0),
                       position=(h+0.35*iconSize, v+0.33*bttnSize),
                       texture=bui.gettexture('usersButton'))

        bui.textwidget(parent=self._subContainer,
                      position=(h+(bttnSize*0.5), v+(bttnSize*0.25)),
                      size=(0, 0),
                      color=textcolor,
                      draw_controller=users_button,
                      maxwidth=bttnSize*0.7,
                      text=getTranslation("players"),
                      h_align='center', v_align='center')
                      
        h += bttnSize + bttnSpacing
        
        self.bots_button = bots_button = bui.buttonwidget(parent=self._subContainer,position=(h,v),size=(bttnSize,bttnSize),
                        autoselect=True,button_type='square',color=disabled_color,label='', on_activate_call=self._set_bots,)
                        
        bui.imagewidget(parent=self._subContainer, size=(iconSize, iconSize),
                       draw_controller=bots_button, #color=(1,0,0),
                       position=(h+0.35*iconSize, v+0.33*bttnSize),
                       texture=self._lineup_tex,
                       mesh_transparent=self._angry_computer_transparent_model)

        bui.textwidget(parent=self._subContainer,
                      position=(h+(bttnSize*0.5), v+(bttnSize*0.25)),
                      size=(0, 0),
                      color=textcolor,
                      draw_controller=bots_button,
                      maxwidth=bttnSize*0.7,
                      text=getTranslation("bots"),
                      h_align='center', v_align='center')
                      
        h += bttnSize + bttnSpacing

        self.bombs_button = bombs_button = bui.buttonwidget(parent=self._subContainer,position=(h,v),size=(bttnSize,bttnSize),
                        autoselect=True,button_type='square',color=disabled_color,label='',on_activate_call=self._set_bombs )
                        
        bui.imagewidget(parent=self._subContainer, size=(iconSize, iconSize),
                       draw_controller=bombs_button, #color=(1,0,0),
                       position=(h+0.35*iconSize, v+0.33*bttnSize),
                       texture=bui.gettexture('buttonBomb'))

        bui.textwidget(parent=self._subContainer,
                      position=(h+(bttnSize*0.5), v+(bttnSize*0.25)),
                      size=(0, 0),
                      color=textcolor,
                      draw_controller=bombs_button,
                      maxwidth=bttnSize*0.7,
                      text=getTranslation("bombs"),
                      h_align='center', v_align='center')
                      
        #h += bttnSize + bttnSpacing
        
        v -= 50
        h = 60
        
        self._timer = svne = CustomConfigNumberEdit(
            parent=self._subContainer,
            position=(h, v),
            xoffset=-70,
            configkey='timer',
            displayname=getTranslation("timer"),
            minval=0.1,
            maxval=2.0,
            increment=0.1,
        )
        
        v-= 50
        
        self._glow = svne = CustomConfigNumberEdit(
            parent=self._subContainer,
            position=(h, v),
            xoffset=-70,
            configkey='glow_scale',
            displayname=getTranslation("glow"),
            minval=1.0,
            maxval=3.0,
            increment=0.1,
        )
        
        self._update_colors()
        
    def _update_colors(self):
        new_color = (0.2,0.5,1)
        if self._players:
            bui.buttonwidget(edit=self.users_button,color=new_color)
        if self._bots:
            bui.buttonwidget(edit=self.bots_button,color=new_color)
        if self._bombs:
            bui.buttonwidget(edit=self.bombs_button,color=new_color)
        
    def _set_players(self):
        self._players = not self._players
        self.save()
        
    def _set_bots(self):
        self._bots = not self._bots
        self.save()
        
    def _set_bombs(self):
        self._bombs = not self._bombs
        self.save()
        
    def save(self):
        self.data["players"] = self._players
        self.data["bots"] = self._bots
        self.data["bombs"] = self._bombs
        saveData(self.data)
        self.update()
        
    def _back(self):
        self._update_timer = None
        bui.containerwidget(edit=self._root_widget,transition='out_right')
        
class CustomConfigNumberEdit(ConfigNumberEdit):
    def __init__(
        self,
        parent: bui.Widget,
        configkey: str,
        position: tuple[float, float],
        minval: float = 0.0,
        maxval: float = 100.0,
        increment: float = 1.0,
        xoffset: float = 0.0,
        displayname: str | bui.Lstr | None = None,
        changesound: bool = True,
        textscale: float = 1.0,
    ):
        if displayname is None:
            displayname = configkey

        self._configkey = configkey
        self._minval = minval
        self._maxval = maxval
        self._increment = increment
        self._value = getData()[configkey]

        self.nametext = bui.textwidget(
            parent=parent,
            position=position,
            size=(100, 30),
            text=displayname,
            maxwidth=160 + xoffset,
            color=(0.8, 0.8, 0.8, 1.0),
            h_align='left',
            v_align='center',
            scale=textscale,
        )
        self.valuetext = bui.textwidget(
            parent=parent,
            position=(246 + xoffset, position[1]),
            size=(60, 28),
            editable=False,
            color=(0.3, 1.0, 0.3, 1.0),
            h_align='right',
            v_align='center',
            text=str(self._value),
            padding=2,
        )
        self.minusbutton = bui.buttonwidget(
            parent=parent,
            position=(330 + xoffset, position[1]),
            size=(28, 28),
            label='-',
            autoselect=True,
            on_activate_call=bui.Call(self._down),
            repeat=True,
            enable_sound=changesound,
        )
        self.plusbutton = bui.buttonwidget(
            parent=parent,
            position=(380 + xoffset, position[1]),
            size=(28, 28),
            label='+',
            autoselect=True,
            on_activate_call=bui.Call(self._up),
            repeat=True,
            enable_sound=changesound,
        )
        # Complain if we outlive our widgets.
        bui.uicleanupcheck(self, self.nametext)
        self._update_display()
    
    def _changed(self) -> None:
        self._update_display()
        self.data = getData()
        self.data[self._configkey] = self._value
        saveData(self.data)
      
# Tell the app about our Plugin.
# ba_meta export plugin

class SuperColorsPlugin(ba.Plugin):

    def has_settings_ui (self):
        return True

    def show_settings_ui(self, button):
        SuperColorsWindow()

    def on_app_running(self) -> None:
        PlayerSpaz.__init__ = _new_player_init_
        Blast.__init__ = _new_blast_init_
        SpazBot.__init__ = _new_bot_init_
    