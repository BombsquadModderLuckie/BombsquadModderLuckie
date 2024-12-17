# ba_meta require api 8
from __future__ import annotations
from typing import TYPE_CHECKING

import bascenev1 as bs
import bauiv1 as bui

import random, time, datetime, weakref, json, os
from bauiv1lib.settings.allsettings import AllSettingsWindow as Asw
from bauiv1lib.popup import PopupWindow
from urllib import request

if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any
    
modz_list = dict()
URL = "https://github.com/PatronModz/Modz1.7.20"
URL2 = "https://github.com/PatronModz"
STATUS = '    <div class="user-status-message-wrapper f6 color-fg-default no-wrap " >'

def getlanguage(text):
    lang = bs.app.lang.language
    setphrases = {"Name":
                      {"Spanish": "Nombre",
                       "English": "Name",
                       "Portuguese": "Nome"},
                  "Creator":
                      {"Spanish": "Creador",
                       "English": "Creator",
                       "Portuguese": "Criador"},
                  "No Creator":
                      {"Spanish": "Desconocido",
                       "English": "Unknown",
                       "Portuguese": "Desconhecido"},
                  "Connection Error":
                    {"Spanish": "No tienes conexión en este momento.",
                     "English": "You have no connection at this time.",
                     "Portuguese": "Você não tem nenhuma conexão no momento."
                    },
                  "Mod Downloaded":
                    {"Spanish": "¡Plugin descargado e instalado con éxito!",
                     "English": "Plugin successfully downloaded and installed!",
                     "Portuguese": "O plugin foi baixado e instalado com sucesso!"
                    },
                  "New Online Plugin":
                    {"Spanish": "** Nuevos plugins online **",
                     "English": "** New plugins online **",
                     "Portuguese": "** Novos plugins online **"
                    },
                 }
                 
    language = ["Spanish", "English", "Portuguese"]
    if lang not in language:
        lang = "English"
        
    if text not in setphrases:
        return text
    return setphrases[text][lang]

def az_call(self) -> None:
    global modz_list
    newlist = sorted(modz_list, reverse=Sys.data['bear_modz_view'])
    modz_list = {k: modz_list[k] for k in newlist}
    
    if self is not None:
        self._set_plugins()

def cloud_mods() -> list:
    plugins = Sys.data.get('mods', [])
    
    def recent():
        bs.screenmessage(
            getlanguage('New Online Plugin'),
            color=(0.0, 1.0, 0.0))
        bui.getsound('ding').play()
    
    try:
        with request.urlopen(URL) as response:
            data = response.read()
            pag = str(data.decode())
    except Exception:
        bui.screenmessage(getlanguage('Connection Error'), color=(1.0, 0.0, 0.0))
        return []
        
    pag_list = pag.replace('"', '/').split('/')
    new_list = list(set(pag_list))
    mods = []
    
    for pag in new_list:
        if ('Delete') not in pag and ('>') not in pag:
            if ('.py') in pag:
                mods.append(pag)
    
    mods = list(set(mods))

    for mod in mods:
        if mod not in plugins:
            bs.apptimer(0.0, recent)
            break

    return mods

def talk() -> None:
    try:
        with request.urlopen(URL2) as response:
            data = response.read()
            web = str(data.decode()).strip()
    except Exception:
        return
        
    webs = list(web.split('\n'))
    if STATUS in webs:
        _id = (webs.index(STATUS) + 1)
        status = webs[_id].replace('<div>', '').replace('</div>', '').strip()
        all = status.split('%n')
        Sys.talk = list(all)
        
        for m in all:
            bs.apptimer(1.5, bs.Call(bs.screenmessage, m.strip(), color=(0.0, 1.0, 1.0)))
            
        bs.apptimer(1.5, bui.getsound('gunCocking').play)

class Sys:
    data: dict[Any, Any] = {}
    dir = bs.app.python_directory_user
    folder = dir + '/Configs'
    file = folder + '/AllSeenMods.json'
    talk: list[str] | None = None

    @classmethod
    def make_scripts(cls) -> None:
        if not os.path.exists(cls.folder):
            os.mkdir(cls.folder)
            
        if not os.path.exists(cls.file):
            with open(cls.file, 'w') as f1:
                f1.write('{}')
                
        with open(cls.file) as f1: 
            r = f1.read()
            cls.data = json.loads(r)
            
        cls.new()

    @classmethod
    def save(cls) -> None:
        if os.path.exists(cls.file):
            with open(cls.file, 'w') as f1:
                w = json.dumps(cls.data, indent=4)
                f1.write(w)
          
    @classmethod
    def new(cls) -> None:
        if len(cls.data) < 2:
            cls.data = dict(mods=[], bear_modz_view=False)
            cls.save()


class BearPlugin:
    def __init__(self,
                 icon: str = 'nub',
                 creator: str = '',
                 plugin: Any = None,
                 window: bui.Window = None,
                 icon_color: Sequence[float] = (1.0, 1.0, 1.0),
                 button_color: Sequence[float] = (0.9, 0.2, 0.2),
                 window_color: Sequence[float] = (0.1, 0.4, 0.7)):
        self.plugin = plugin
        
        if creator == '':
            creator = getlanguage('No Creator')
        
        if plugin:
            name = plugin.__name__
            data = dict(
                icon=icon,
                plugin=plugin,
                window=window,
                creator=creator,
                icon_color=icon_color,
                button_color=button_color,
                window_color=window_color)
            modz_list[name] = data
    
    def getname(self):
        plugin = str(self.plugin)
        plugin = plugin.split("'")[1]
        return plugin

def plugins_window(self):
    bui.containerwidget(edit=self._root_widget,transition='out_left')
    ModzWindow()

salls = Asw.__init__
def new_init_alls(self, *args, **kwargs):
    salls(self, *args, **kwargs)

    uiscale = bs.app.ui_v1.uiscale
    width = (100 if uiscale is
             bui.UIScale.SMALL else -14)
    position = (width, 180) #(width+628, 180)
    
    self.bm_button = bui.buttonwidget(parent=self._root_widget,
                     autoselect=True,position=position,
                     size=(70,70),button_type='square',
                     label='',on_activate_call=bui.Call(plugins_window, self))
                  
    self.bm_text = bui.textwidget(parent=self._root_widget,
                   position=(position[0]+35,position[1]+20),
                   size=(0, 0),scale=0.6,color=(0.7,0.9,0.7,1.0),
                   draw_controller=self.bm_button,maxwidth=100,
                   text=("Modz"),h_align='center',v_align='center')
                  
    self.bm_image = bui.imagewidget(parent=self._root_widget,
                    size=(40,40),draw_controller=self.bm_button,
                    position=(position[0]+15,position[1]+30),
                    color=(0.9,0.8,0.0),texture=bui.gettexture('folder'))

class ModzWindow(PopupWindow):
    def __init__(self,
                 transition: str ='in_right',
                 download_mode: bool = False,
                 ) -> None:
                     
        columns = 2
        self._width = width = 1200
        self._height = height = 500
        self._sub_height = 200
        self._scroll_width = self._width*0.90
        self._scroll_height = self._height - 180
        self._sub_width = self._scroll_width*0.95;
        self._dlmode = download_mode
        self._cmods = None

        if download_mode:
            apply_text = 'Online Modz'
            self._cmods = cloud_mods()
        else:
            apply_text = 'Modz / Plugins'

        app = bs.app.ui_v1
        uiscale = app.uiscale

        self._root_widget = bui.containerwidget(size=(width+90,height+80),transition=transition,
                           scale=1.5 if uiscale is bui.UIScale.SMALL else 1.0,
                           stack_offset=(0,-30) if uiscale is bui.UIScale.SMALL else  (0,0))
        
        self._backButton = b = bui.buttonwidget(parent=self._root_widget,autoselect=True,
                                               position=(200,self._height-15),size=(130,60),
                                               scale=0.8,text_scale=1.2,label=bui.Lstr(resource='backText'),
                                               button_type='back',on_activate_call=bui.Call(self._back))
        bui.buttonwidget(edit=self._backButton, button_type='backSmall',size=(60, 60),label=bui.charstr(bui.SpecialChar.BACK))
        bui.containerwidget(edit=self._root_widget,cancel_button=b)
        
        self.titletext = bui.textwidget(parent=self._root_widget,position=(30, height-15),size=(width,50),
                          h_align="center",color=(0,1,0), text=apply_text, v_align="center",maxwidth=width*1.3)
        
        self._scrollwidget = bui.scrollwidget(parent=self._root_widget,
            position=(self._width*0.17,51*1.8),size=(self._sub_width -140,self._scroll_height +60*1.2))

        if not download_mode:
            self._chang_button = bui.buttonwidget(parent=self._root_widget,
                 autoselect=True,position=(880, 490),
                 size=(60,60),button_type='square',color=(0.4, 0.5, 0.6),
                 label='A-Z',on_activate_call=self._az_call_button)

            i = bui.charstr(bui.SpecialChar.DOWN_ARROW)
            self._dwl_button = bui.buttonwidget(parent=self._root_widget,
                 autoselect=True,position=(880*1.10, 490),
                 size=(60,60),button_type='square',color=(0.4, 0.5, 0.6),
                 label=i,on_activate_call=self._dwl_button_call)

            i = bui.charstr(bui.SpecialChar.REWIND_BUTTON)
            if Sys.talk is not None:
                self._dwl_button = bui.buttonwidget(parent=self._root_widget,
                     autoselect=True,position=(880*0.40, 490),
                     size=(60,60),button_type='square',color=(0.4, 0.5, 0.6),
                     label=i,on_activate_call=self._talk_button)

        self._tab_container = None
        
        if download_mode:
            self._set_cloud_mods()
        else:
            self._set_plugins()
    
    def _talk_button(self) -> None:
        for t in Sys.talk:
            bs.chatmessage(t)
    
    def _dwl_button_call(self) -> None:
        bui.containerwidget(edit=self._root_widget,transition='out_left')
        ModzWindow(transition='none', download_mode=True)
    
    def _set_cloud_mods(self) -> None:
        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()
    
        len_modz = len(self._cmods)
        sub_height = max(len_modz * 126, 0)
        v = sub_height - 55
        width = 300
        pos = (110, v-8)
        i = 0

        if Sys.data.get('mods') is not None:
            Sys.data['mods'] = self._cmods
            Sys.save()

        self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
            size=(self._sub_width,sub_height),
            background=False,selection_loops_to_parent=True)

        for mod in self._cmods:
            bui.containerwidget(parent=c,position=(pos[0]*1.6-140,pos[1]-50-i),
                color=(0.25, 0.25, 0.75),scale=1.3,size=(600,80),background=True)
            
            txt = 'Plugin: ' + mod
            t = bui.textwidget(parent=c,position=(pos[0], pos[1]-i),size=(width,50),
                      scale=1.4,color=(0.2,1.2,0.2),h_align="left",v_align="center",
                      text=txt,maxwidth=400)
                      
            txt = '> v1.7.20+'
            t = bui.textwidget(parent=c,position=(pos[0], pos[1]-40-i),size=(width,50),
                      scale=1.4,h_align="center",v_align="center",
                      color=bui.app.ui_v1.title_color,text=txt,maxwidth=300)
                      
            
            pos2 = (pos[0]+560, pos[1]-32)
            b = bui.buttonwidget(parent=c,
                     autoselect=True,position=(pos2[0], pos2[1]-i),
                     size=(70,70),button_type='square',color=(1, 0.1, 0.5), text_scale=1.4,
                     label=bui.charstr(bui.SpecialChar.DOWN_ARROW),on_activate_call=bs.Call(self.download_plugin, mod))

            i += 126
            
    def download_plugin(self, mod: str = '', msg: bool = True) -> None:
        root = bs.app.python_directory_user + '/' + mod
        link = "https://raw.githubusercontent.com/PatronModz/Modz1.7.20/main/" + mod
        
        with request.urlopen(link) as r:
            plugin = str(r.read().decode())

        with open(root, 'w') as f:
            f.write(plugin)
            
        if msg:
            bs.screenmessage(getlanguage('Mod Downloaded'), color=(0,1,0))
            bui.screenmessage(
                bui.Lstr(resource='settingsWindowAdvanced.mustRestartText'),
                color=(1.0, 0.5, 0.0))

########################################################
        
    def _set_plugins(self) -> None:
        if self._tab_container is not None and self._tab_container.exists():
            self._tab_container.delete()
    
        len_modz = len(modz_list)
        sub_height = max(len_modz * 126, 0)
        v = sub_height - 55
        width = 300
        pos = (110, v-8)
        i = 0
        
        self._tab_container = c = bui.containerwidget(parent=self._scrollwidget,
            size=(self._sub_width,sub_height),
            background=False,selection_loops_to_parent=True)

        for mod in modz_list:
            info = modz_list[mod]
            
            bui.containerwidget(parent=c,position=(pos[0]*1.6-140,pos[1]-50-i),
                color=info['window_color'],scale=1.3,size=(600,80),background=True)
            
            txt = 'Plugin: ' + mod
            t = bui.textwidget(parent=c,position=(pos[0], pos[1]-i),size=(width,50),
                      scale=1.4,color=(0.2,1.2,0.2),h_align="left",v_align="center",
                      text=txt,maxwidth=400)
                      
            txt = getlanguage('Creator') + ': ' + info['creator']
            t = bui.textwidget(parent=c,position=(pos[0], pos[1]-40-i),size=(width,50),
                      scale=1.4,h_align="center",v_align="center",
                      color=bui.app.ui_v1.title_color,text=txt,maxwidth=300)
                      
            if info['window'] is not None:
                pos2 = (pos[0]+560, pos[1]-32)
                b = bui.buttonwidget(parent=c,
                         autoselect=True,position=(pos2[0], pos2[1]-i),
                         size=(70,70),button_type='square',color=info['button_color'],
                         label='',on_activate_call=bui.Call(self.open_mod_window, info['window']))
    
                ic = bui.imagewidget(parent=c,
                        size=(60,60),draw_controller=b,
                        position=(pos2[0]+5, pos2[1]+8-i),
                        color=info['icon_color'],
                        texture=bui.gettexture(info['icon']))
            i += 126
        
    def _az_call_button(self) -> None:
        if Sys.data['bear_modz_view']:
            Sys.data['bear_modz_view'] = False
        else:
            Sys.data['bear_modz_view'] = True
        Sys.save()
        az_call(self)
        
    def open_mod_window(self, window: bui.Window):
        self.button_mod_back(window)
        bui.containerwidget(edit=self._root_widget,transition='out_left')
        window()

    def button_mod_back(self, window: bui.Window):
        """Esto es importante para regresar a la ventana principal.
           Asegúrese de usar 'self._back' como llamada."""
        """This is important to return to the main window.
           Be sure to use 'self._back' as the callback."""
           
        window._back = ModzWindow._back_mod
        
    def _back_mod(self):
        bui.containerwidget(edit=self._root_widget,transition='out_left')
        ModzWindow()

    def _back(self):
        if self._dlmode:
            self._root_widget.delete()
            ModzWindow(transition='none')
        else:
            bui.containerwidget(edit=self._root_widget,transition='out_left')
            Asw()

# ba_meta export plugin
class Plugins(bui.Plugin):
    def __init__(self) -> None:
        Asw.__init__ = new_init_alls
        Sys.make_scripts()
        bs.apptimer(0.1, talk)
        bs.apptimer(0.1, bs.Call(az_call, None))
        