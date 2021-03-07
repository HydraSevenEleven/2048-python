from enum import Enum
from os import path
import json

class SettingsEnum(str, Enum):    
    with open(path.join(path.dirname(path.abspath(__file__)), 'settings.json'), 'r') as f:
        settings = json.load(f)
    BACKGROUND_COLOR_CELL_EMPTY = settings["background_color_cell_empty"]
    SIZE = settings["size"]
    GRID_PADDING = settings["grid_padding"]
    BACKGROUND_COLOR_GAME = settings["background_color_game"]
    FONT = settings["font"]
    BACKGROUND_COLOR_DICT = json.dumps(settings["background_color_dict"])
    CELL_COLOR_DICT = json.dumps(settings["cell_color_dict"])
    KEY_UP_ALT = settings["key_up_alt"]
    KEY_DOWN_ALT = settings["key_down_alt"]
    KEY_LEFT_ALT = settings["key_left_alt"]
    KEY_RIGHT_ALT = settings["key_right_alt"]
    KEY_UP = settings["key_up"]
    KEY_DOWN = settings["key_down"]
    KEY_LEFT = settings["key_left"]
    KEY_RIGHT = settings["key_right"]
    KEY_BACK = settings["key_back"]
    KEY_J = settings["key_j"]
    KEY_K = settings["key_k"]
    KEY_L = settings["key_l"]
    KEY_H = settings["key_h" ]