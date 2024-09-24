import pygame
import numpy as np
from scipy.interpolate import make_interp_spline
from hewo_bot_module_display.settings.settings_loader import SettingsLoader

eye_settings = SettingsLoader().load_settings("settings.hewo")['eye']


class Pupil:
    def __init__(self, size, position, settings):
        # TODO: Shrink the pupil to extract new emotions.
        self.size = size
        self.position = position
        self.color = settings['color'].values()

    def update(self):
        pass

    def set_size(self, size):
        self.size = size

    def set_position(self, position):
        self.position = position

    def handle_event(self, event):
        pass

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, (0, 0, self.size[0], self.size[1]))


class EyeLash:
    def __init__(self, size, position, settings):
        self.size = size
        self.position = position
        self.color = settings['color'].values()
        self.max_emotion = self.size[1]
        self.emotion_pcts = settings['emotion'].values()
        x, y = position
        w, h = size
        self.polygon_points = [
            [0 + x, 0 + y],
            [0 + x, h + y],
            [w / 2 + x, h + y],
            [w + x, h + y],
            [w + x, 0 + y],
            [w / 2 + x, 0 + y]
        ]
        self.flip = settings['flip']
        self.set_points_by_pct(self.emotion_pcts)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def set_points_by_pct(self, emotion):
        self.set_emotion_pcts(emotion)
        indices = [1, 2, 3]
        if self.flip:
            self.emotion_pcts = [100 - e for e in self.emotion_pcts]
            indices = [0, 5, 4]

        for i, tup in enumerate(zip(indices, self.emotion_pcts)):
            self.polygon_points[tup[0]][1] = self.position[1] + self.size[1] * (tup[1] / 100)

    def draw(self, surface):
        points = self.polygon_points[1:4]
        if self.flip:
            points = [self.polygon_points[0], self.polygon_points[5], self.polygon_points[4]]
        ############################
        x_points = np.array([p[0] for p in points])
        y_points = np.array([p[1] for p in points])
        spline = make_interp_spline(x_points, y_points, k=2)
        x_range = np.linspace(min(x_points), max(x_points), 500)
        interpolated_points = [(int(x), int(spline(x))) for x in x_range]
        ############################
        polygon = [self.polygon_points[0]] + interpolated_points + self.polygon_points[4:]
        if self.flip:
            interpolated_points.reverse()
            polygon = self.polygon_points[1:4] + interpolated_points
        pygame.draw.polygon(surface, self.color, polygon)

    def set_emotion_pcts(self, emotion):
        for i, e in enumerate(emotion):
            self.emotion_pcts[i] = max(0, min(e, 100))

    def get_emotion(self):
        return self.emotion_pcts

    def set_emotion(self, emotion):
        self.set_emotion_pcts(emotion)
        self.set_points_by_pct(emotion)


class Eye:
    # Here I should initialize all the elements that make up the eye
    def __init__(self, size, position, settings):
        self.size = size
        self.position = position
        self.BG_COLOR = settings['bg_color'].values()

        # Sizes are in proportion to the eye size
        self.lash_size = (self.size[0], self.size[1] / 2)
        self.t_pos = (0, 0)
        self.b_pos = (0, self.size[1] / 2)

        # Declare the elements that make up the eye
        self.top_lash = EyeLash(
            size=self.lash_size,
            position=self.t_pos,
            settings=settings['top_lash']
        )
        self.pupil = Pupil(
            size=self.size,
            position=self.position,
            settings=settings['pupil']
        )
        self.bot_lash = EyeLash(
            size=self.lash_size,
            position=self.b_pos,
            settings=settings['bot_lash']
        )

        # And initialize the surface of it
        self.eye_surface = pygame.Surface(self.size)

    def handle_event(self, event):
        self.top_lash.handle_event(event)
        self.pupil.handle_event(event)
        self.bot_lash.handle_event(event)

    def draw(self, surface):
        self.eye_surface = pygame.surface.Surface(self.size)
        self.eye_surface.fill(self.BG_COLOR)
        self.pupil.draw(self.eye_surface)
        self.top_lash.draw(self.eye_surface)
        self.bot_lash.draw(self.eye_surface)
        surface.blit(self.eye_surface, self.position)

    def update(self):
        self.top_lash.update()
        self.pupil.update()
        self.bot_lash.update()

    def set_emotion(self, t_emotion, b_emotion):
        self.top_lash.set_emotion(t_emotion)
        self.bot_lash.set_emotion(b_emotion)

    def get_emotion(self):
        return self.top_lash.get_emotion(), self.bot_lash.get_emotion()


if __name__ == '__main__':
    eye_settings = SettingsLoader().load_settings("settings.hewo")['eye']
