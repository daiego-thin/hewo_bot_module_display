"""
From the dimensions and position of the main surface
of the hewo, dimension and position of the other
"""

from hewo_bot_module_display.settings.settings_loader import SettingsLoader
import math

HEART = (1 + math.sqrt(5)) / 2  # Heart of hewo is golden ratio

DISPLAY = SettingsLoader('hewo.settings.display')
display = DISPLAY.settings
HEWO = SettingsLoader('hewo.settings.hewo')

w, h = display['width'], display['height']

hewo = HEWO.settings
l_eye = hewo['elements']['left_eye']
r_eye = hewo['elements']['right_eye']
mouth = hewo['elements']['mouth']

Wf, Hf = w / HEART, h / HEART
# HEWO FACE SETTINGS
hewo['surface']['size'] = {
    'width': Wf,
    'height': Hf
}
hewo['surface']['position'] = {
    'x': 0,
    'y': 0
}
# General eye settings
# Eye and lashes sizes
We, He = (Wf / 5, Hf / 5 * 4)
Wl, Hl = We, He / 2
########### LEFT EYE
l_eye['surface']['size'] = {
    'width': We,
    'height': He
}
l_eye['surface']['position'] = {
    'x': 0,
    'y': 0
}
l_eye['elements']['pupil']['size'] = {
    'width': We / 2,
    'height': He / 2
}
l_eye['elements']['pupil']['position'] = {
    'x': 0,
    'y': 0
}
l_eye['elements']['top_lash']['size'] = {
    'width': Wl,
    'height': Hl
}
l_eye['elements']['top_lash']['position'] = {
    'x': 0,
    'y': 0
}
l_eye['elements']['bot_lash']['size'] = {
    'width': Wl,
    'height': Hl
}
l_eye['elements']['bot_lash']['position'] = {
    'x': 0,
    'y': He / 2
}

########## RIGHT EYE

############## MOUTH
mouth['surface']['size'] = {
    'width': (3 / 5) * Wf,
    'height': (1 / 5) * Hf
}
mouth['surface']['position'] = {
    'x': (1 / 5) * Wf,
    'y': (4 / 5) * Hf
}

# rebuild and save the settings
hewo['elements']['left_eye'] = l_eye
hewo['elements']['right_eye'] = r_eye
hewo['elements']['mouth'] = mouth
HEWO.save_settings(hewo)
