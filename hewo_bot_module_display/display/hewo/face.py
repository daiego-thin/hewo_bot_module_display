import pygame
import math
from hewo_bot_module_display.display.hewo.eye import Eye
from hewo_bot_module_display.display.hewo.mouth import Mouth
from hewo_bot_module_display.settings.settings_loader import SettingsLoader

PHI = (1 + math.sqrt(5)) / 2
settings = SettingsLoader().load_settings("settings.hewo")


class Face:
    COLOR = (
        settings['surface']['color']['r'],
        settings['surface']['color']['g'],
        settings['surface']['color']['b']
    )

    def __init__(self, position=None, color=COLOR, factor=350, enable_controls=True, max_size=(960, 640)):
        if position is None:
            position = [0, 0]
        self.size = [PHI * factor, factor]
        self.position = position
        self.color = color
        self.face_surface = pygame.surface.Surface(self.size)
        self.max_size = max_size

        self.face_surface = pygame.surface.Surface(self.size)
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]

        self.left_eye_pos = [0, 0]
        self.right_eye_pos = [self.eye_size[0] * 4, 0]
        self.mouth_pos = [self.eye_size[0], self.eye_size[1]]

        self.left_eye = Eye(self.eye_size, self.left_eye_pos)
        self.right_eye = Eye(self.eye_size, self.right_eye_pos)
        self.mouth = Mouth(self.mouth_size, self.mouth_pos)
        self.set_face_elements()
        self.enable_controls = enable_controls

    def set_face_elements(self):
        self.face_surface = pygame.surface.Surface(self.size)
        self.eye_size = [self.size[0] / 5, self.size[1] / 5 * 4]
        self.mouth_size = [self.size[0] / 5 * 3, self.size[1] / 5]

        self.left_eye_pos = [0, 0]  # in the canvas
        self.right_eye_pos = [self.eye_size[0] * 4, 0]
        self.mouth_pos = [self.eye_size[0], self.eye_size[1]]

        emotion = self.left_eye.get_emotion()
        self.left_eye = Eye(self.eye_size, self.left_eye_pos, init_emotion=emotion)
        emotion = self.right_eye.get_emotion()
        self.right_eye = Eye(self.eye_size, self.right_eye_pos, init_emotion=emotion)
        emotion = self.mouth.get_emotion()
        self.mouth = Mouth(self.mouth_size, self.mouth_pos, init_emotion=emotion)

    def set_size(self, size):
        self.size[0] = max(PHI, min(size[0], self.max_size[0]))
        self.size[1] = max(1, min(size[1], self.max_size[1]))

    def set_position(self, pos):
        self.position[0] = max(0, min(pos[0], self.max_size[0] - self.size[0]))
        self.position[1] = max(0, min(pos[1], self.max_size[1] - self.size[1]))

    def update(self):
        self.left_eye.update()
        self.right_eye.update()
        self.mouth.update()
        self.handle_input()
        self.update_emotion()

    def handle_event(self, event):
        self.left_eye.handle_event(event)
        self.right_eye.handle_event(event)
        self.mouth.handle_event(event)

    def draw(self, surface):
        self.face_surface.fill(self.color)
        self.left_eye.draw(self.face_surface)
        self.right_eye.draw(self.face_surface)
        self.mouth.draw(self.face_surface)
        # self.face_surface = pixelate(self.face_surface, 100, self.size)
        surface.blit(self.face_surface, dest=self.position)

    def get_emotion(self):
        letl = self.left_eye.top_lash.get_emotion()
        lebl = self.left_eye.bot_lash.get_emotion()
        retl = self.right_eye.top_lash.get_emotion()
        rebl = self.right_eye.bot_lash.get_emotion()
        tl, bl = self.mouth.get_emotion()
        emotions = [letl, lebl, retl, rebl, tl, bl]
        emotions = [int(item) for sublist in emotions for item in sublist]
        return emotions

    def set_emotions(self, edict):
        letl = [edict['letl_a'], edict['letl_b'], edict['letl_c']]
        lebl = [edict['lebl_a'], edict['lebl_b'], edict['lebl_c']]
        retl = [edict['retl_a'], edict['retl_b'], edict['retl_c']]
        rebl = [edict['rebl_a'], edict['rebl_b'], edict['rebl_c']]
        tl = [edict['tl_a'], edict['tl_b'], edict['tl_c'], edict['tl_d'], edict['tl_e']]
        bl = [edict['bl_a'], edict['bl_b'], edict['bl_c'], edict['bl_d'], edict['bl_e']]
        self.left_eye.set_emotion(letl, lebl)
        self.right_eye.set_emotion(retl, rebl)
        self.mouth.set_emotion(tl, bl)

    def update_emotion(self):
        pass

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.set_face_elements()


# Surface Effects

def pixelate(surface, pixels_factor=128, size=None):
    surface = pygame.transform.scale(surface, [PHI * pixels_factor, pixels_factor])
    surface = pygame.transform.scale(surface, size)
    return surface
