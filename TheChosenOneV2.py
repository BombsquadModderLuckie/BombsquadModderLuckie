
# ba_meta require api 7
from __future__ import annotations
from typing import TYPE_CHECKING

import ba, _ba, random
from bastd.ui.popup import PopupWindow
from bastd.gameutils import SharedObjects

if TYPE_CHECKING:
    from typing import List, Sequence, Optional, Dict, Any

class MyMapPoints:
    # This file was automatically generated from "hockey_stadium.ma"
    # pylint: disable=all
    points = {}
    # noinspection PyDictCreation
    boxes = {}
    boxes['area_of_interest_bounds'] = (0.0, 0.7956858119, 0.0) + (
        0.0, 0.0, 0.0) + (30.80223883, 0.5961646365, 13.88431707)
    boxes['map_bounds'] = (0.0, 0.7956858119, -0.4689020853) + (0.0, 0.0, 0.0) + (
        35.16182389, 12.18696164, 21.52869693)
    points['ffa_spawn1'] = (-9.5, 0.5, -8.0)
    points['ffa_spawn2'] = (9.5, 0.5, -8.0)
    points['ffa_spawn3'] = (3.5, 0.5, -8.0)
    points['ffa_spawn4'] = (-3.5, 0.5, -8.0)
    points['ffa_spawn5'] = (-9.5, 0.5, -1.5)
    points['ffa_spawn6'] = (9.5, 0.5, -1.5)
    points['spawn1'] = (-9.5, 0.5, 4.0)
    points['spawn2'] = (9.5, 0.5, 4.0)
    points['powerup_spawn1'] = (0.0, 0.5, -8.0)
    points['powerup_spawn2'] = (9.5, 0.5, 5.5)
    points['powerup_spawn3'] = (-9.5, 0.5, 5.5)
    points['powerup_spawn4'] = (9.5, 0.5, -5.0)
    points['powerup_spawn5'] = (-9.5, 0.5, -5.0)
    points['powerup_spawn6'] = (3.5, -0.5, 2.0)
    points['powerup_spawn7'] = (-3.5, -0.5, 2.0)
    points['powerup_spawn8'] = (0.0, -0.5, 6.0)
    points['flag_default'] = (0.0, -0.5, 0.0)
    points['tnt1'] = (-4.5, 0.0, -3.0)
    points['tnt2'] = (4.5, 0.0, -3.0)
    points['tnt3'] = (-2.5, -0.5, 4.0)
    points['tnt4'] = (2.5, -0.5, 4.0)
    points['flag1'] = (-9.5, 0.5, 4.0)
    points['flag2'] = (9.5, 0.5, 4.0)
    

class MyMap(ba.Map):

    defs = MyMapPoints
    name = '☣️TheChosenOneV2'

    @classmethod
    def get_play_types(cls) -> List[str]:
        return ['melee', 'keep_away', 'team_flag', 'king_of_the_hill']

    @classmethod
    def get_preview_texture_name(cls) -> str:
        return 'eggTex3'

    @classmethod
    def on_preload(cls) -> Any:
        data: Dict[str, Any] = {}
        return data

    def __init__(self) -> None:
        super().__init__()
        shared = SharedObjects.get()
        self.locs = []
        self.regions = []
        
        self.collision = ba.Material()
        self.collision.add_actions(
            actions=(('modify_part_collision', 'collide', True)))

        set = [
              dict(position=(0.0, -1.0, 0.0), color=(1.0, 1.0, 0.0), size=(3.0, 0.5, 3.0)),
              dict(position=(0.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(15.0, 0.5, 4.0)),
              dict(position=(9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 17.0)),
              dict(position=(-9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 17.0)),
              dict(position=(-6.5, -0.5, -5.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(-5.5, -0.5, -4.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(-4.5, -0.5, -3.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(-3.5, -0.5, -2.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(-2.5, -0.5, -1.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(6.5, -0.5, -5.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(5.5, -0.5, -4.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(4.5, -0.5, -3.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(3.5, -0.5, -2.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(2.5, -0.5, -1.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(4.0, -1.5, 1.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(5.0, -1.5, 0.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(3.0, -1.5, 2.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(2.0, -1.5, 2.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-2.0, -1.5, 2.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-3.0, -1.5, 2.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-4.0, -1.5, 1.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-5.0, -1.5, 0.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(0.0, -1.5, 4.0), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-1.0, -1.5, 4.0), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(1.0, -1.5, 4.0), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(0.0, -1.0, 0.0), color=(1.0, 1.0, 0.0), size=(3.0, 0.5, 3.0)),
              dict(position=(0.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(15.0, 0.5, 4.0)),
              dict(position=(9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 17.0)),
              dict(position=(-9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 17.0)),
              dict(position=(-6.5, -0.5, -5.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(-5.5, -0.5, -4.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(-4.5, -0.5, -3.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(-3.5, -0.5, -2.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(-2.5, -0.5, -1.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(6.5, -0.5, -5.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(5.5, -0.5, -4.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(4.5, -0.5, -3.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(3.5, -0.5, -2.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(2.5, -0.5, -1.0), color=(1.0, 0.30000001192092896, 0.5), size=(2.0, 0.5, 2.0)),
              dict(position=(4.0, -1.5, 1.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(5.0, -1.5, 0.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(3.0, -1.5, 2.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(2.0, -1.5, 2.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-2.0, -1.5, 2.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-3.0, -1.5, 2.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-4.0, -1.5, 1.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-5.0, -1.5, 0.5), color=(0.12999999523162842, 0.12999999523162842, 0.12999999523162842), size=(1.0, 0.5, 6.0)),
              dict(position=(-0.5, -1.0, 0.0), color=(1.0, 1.0, 0.0), size=(1.0, 0.5, 3.0)),
              dict(position=(0.0, -1.0, 0.0), color=(1.0, 1.0, 0.0), size=(1.0, 0.5, 3.0)),
              dict(position=(0.5, -1.0, 0.0), color=(1.0, 1.0, 0.0), size=(1.0, 0.5, 3.0)),
              dict(position=(0.0, -1.0, 0.0), color=(1.0, 1.0, 0.0), size=(3.0, 0.5, 1.0)),
              dict(position=(0.0, -1.0, 0.5), color=(1.0, 1.0, 0.0), size=(3.0, 0.5, 1.0)),
              dict(position=(0.0, -1.0, -0.5), color=(1.0, 1.0, 0.0), size=(3.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(-8.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(-9.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(-10.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(-10.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(8.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(9.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(10.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(10.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 17.0)),
              dict(position=(0.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 1.0)),
              dict(position=(0.0, 0.0, -8.5), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 1.0)),
              dict(position=(0.0, 0.0, -9.0), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 1.0)),
              dict(position=(0.0, 0.0, -7.5), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 1.0)),
              dict(position=(0.0, 0.0, -7.0), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 1.0)),
              dict(position=(0.0, 0.0, -6.5), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 6.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 5.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 5.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 4.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 4.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 3.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 3.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 2.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 2.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 1.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 0.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 0.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -0.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -1.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -2.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -2.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -3.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -3.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -4.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -4.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, -5.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -5.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -5.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -4.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -4.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -3.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -3.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -2.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -2.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -1.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, -0.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 0.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 0.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 1.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 2.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 2.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 3.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 3.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 4.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 4.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 5.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(9.5, 0.0, 5.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 1.0)),
              dict(position=(-9.5, 0.0, 6.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 5.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 5.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 4.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 4.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 3.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 3.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 2.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 2.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 1.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 0.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, 0.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -0.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -1.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -2.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -2.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -3.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -3.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -4.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -4.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -5.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -5.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -6.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -6.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -7.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -7.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -8.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -9.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(-9.5, 0.0, -9.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 6.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 5.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 5.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 4.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 4.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 3.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 3.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 2.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 2.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 1.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 0.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, 0.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -0.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -1.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -2.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -2.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -3.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -3.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -4.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -4.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -5.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -5.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -6.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -6.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -7.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -7.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -8.5), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(9.5, 0.0, -9.0), color=(0.20000000298023224, 1.0, 1.0), size=(4.0, 0.5, 0.5)),
              dict(position=(0.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-0.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-1.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-1.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-2.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-2.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-3.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-3.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-4.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-4.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-5.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-5.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-6.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-6.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(0.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(1.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(1.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(2.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(2.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(3.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(4.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(4.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(5.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(6.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(6.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(5.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(7.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(1.0, 0.5, 4.0)),
              dict(position=(-6.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-6.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-5.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-5.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-4.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-4.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-3.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-3.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-2.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-2.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-1.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-1.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(-0.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(0.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(0.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(1.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(1.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(2.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(2.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(3.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(3.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(4.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(4.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(5.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(5.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(6.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(6.5, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 4.0)),
              dict(position=(9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(10.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(10.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(11.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(9.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(8.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(8.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(-8.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(-8.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(-9.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(-9.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(-10.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(-10.5, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(-11.0, 0.0, -1.5), color=(0.20000000298023224, 1.0, 1.0), size=(0.5, 0.5, 17.0)),
              dict(position=(0.0, 0.0, -8.0), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 0.5)),
              dict(position=(0.0, 0.0, -8.5), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 0.5)),
              dict(position=(0.0, 0.0, -9.0), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 0.5)),
              dict(position=(0.0, 0.0, -9.5), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 0.5)),
              dict(position=(0.0, 0.0, -7.5), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 0.5)),
              dict(position=(0.0, 0.0, -7.0), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 0.5)),
              dict(position=(0.0, 0.0, -6.5), color=(0.20000000298023224, 1.0, 1.0), size=(23.0, 0.5, 0.5)),
              ]

        for i, map in enumerate(set):
            self.locs.append(
                ba.newnode('locator',
                    attrs={'shape': 'box',
                           'position': set[i]['position'],
                           'color': set[i]['color'],
                           'opacity': 1.0,
                           'draw_beauty': True,
                           'size': set[i]['size'],
                           'additive': False}))
                           
            self.regions.append(
                ba.newnode('region',
                    attrs={'scale': tuple(set[i]['size']),
                           'type': 'box',
                           'materials': [self.collision,
                                         shared.footing_material]}))
            self.locs[-1].connectattr('position', self.regions[-1], 'position')

        self.background = ba.newnode(
            'terrain',
            attrs={
                'model': ba.getmodel('tipTopBG'),
                'lighting': False,
                'background': True,
                'color_texture': ba.gettexture('black')})

        gnode = ba.getactivity().globalsnode
        gnode.tint = (0.8, 0.9, 1.3)
        gnode.ambient_color = (0.8, 0.9, 1.3)
        gnode.vignette_outer = (0.79, 0.79, 0.69)
        gnode.vignette_inner = (0.97, 0.97, 0.99)
        
# ba_meta export plugin
class MapMaker(ba.Plugin):
    def __init__(self) -> None:
        ba._map.register_map(MyMap)
    