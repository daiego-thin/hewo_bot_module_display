import pygame
import numpy as np
from scipy.interpolate import make_interp_spline
from hewo_bot_module_display.settings.settings_loader import SettingsLoader

settings = SettingsLoader().load_settings("settings.hewo")
mouth = settings['elements']['mouth']


class Lip:
    LIP_WIDTH = 5

    def __init__(self, size, position, color, id=None):
        self.id = id
        self.size = size
        self.position = position
        self.color = color
        self.lip_points = {
            'left_commissure': [0, 0],
            'center': [self.size[0] / 2, 0],
            'right_commissure': [self.size[0], 0]
        }
        self.increments = {
            'left_commissure': [0, 0],
            'center': 0,
            'right_commissure': [0, 0]
        }

    def lip_shape(self):
        x_points = []
        for key, point in self.lip_points.items():
            if key == 'right_commissure':
                increment_x = self.increments[key][0]
                adjusted_x = self.clamp(self.size[0] - increment_x, min_value=self.size[0]/2, max_value=self.size[0])
            else:
                increment_x = self.increments[key][0] if key != 'center' else 0
                adjusted_x = self.clamp(point[0] + increment_x, min_value=0, max_value=self.size[0])
            x_points.append(adjusted_x)

        x_points = np.array(x_points)

        y_points = []
        for key, point in self.lip_points.items():
            increment_y = self.increments[key][1] if key != 'center' else self.increments[key]
            adjusted_y = self.clamp(point[1] + increment_y, min_value=self.LIP_WIDTH,
                                    max_value=self.size[1] - self.LIP_WIDTH)
            y_points.append(adjusted_y)

        y_points = np.array(y_points)
        spline = make_interp_spline(x_points, y_points, k=2)
        x_range = np.linspace(min(x_points), max(x_points), 500)
        return [(int(x), int(spline(x))) for x in x_range]

    def clamp(self, value, min_value, max_value):
        return max(min_value, min(value, max_value))

    def set_increments(self, increments):
        for key in increments:
            if key == 'left_commissure':
                x_increment, y_increment = increments[key]
                self.increments[key][0] = self.clamp(int(x_increment / 100 * (self.size[0] / 2)),
                                                     min_value=0,
                                                     max_value=self.size[0] / 2)
                self.increments[key][1] = self.clamp(y_increment, 0, self.size[1])
            elif key == 'right_commissure':
                x_increment, y_increment = increments[key]
                self.increments[key][0] = self.clamp(int(x_increment / 100 * (self.size[0] / 2)),
                                                     min_value=1,
                                                     max_value=self.size[0]/2)
                self.increments[key][1] = self.clamp(y_increment, 0, self.size[1])
            else:
                self.increments[key] = self.clamp(increments[key], 0, self.size[1])

    def update(self):
        pass

    def draw(self, surface):
        points = self.lip_shape()
        pygame.draw.lines(surface, self.color, False, points, self.LIP_WIDTH)

    def handle_event(self, event):
        pass


class Mouth:
    COLOR = (
        mouth['surface']['color']['r'],
        mouth['surface']['color']['g'],
        mouth['surface']['color']['b']
    )
    TOP_LIP = (
        mouth['elements']['top_lip']['color']['r'],
        mouth['elements']['top_lip']['color']['g'],
        mouth['elements']['top_lip']['color']['b']
    )
    BOT_LIP = (
        mouth['elements']['bot_lip']['color']['r'],
        mouth['elements']['bot_lip']['color']['g'],
        mouth['elements']['bot_lip']['color']['b']
    )

    def __init__(self, size, position, color=COLOR, init_emotion=None):
        if init_emotion is None:
            init_emotion = [[0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0]]

        self.size = size
        self.position = position
        self.surface = pygame.Surface(self.size)
        self.color = color

        self.top_lip_emotion = init_emotion[0]
        self.bot_lip_emotion = init_emotion[1]
        self.top_lip = Lip(self.size, self.position, self.TOP_LIP, id='top')
        self.bot_lip = Lip(self.size, self.position, self.BOT_LIP, id='bottom')
        self.increments = self.get_emotion()

    def draw(self, surface):
        self.surface.fill(self.color)
        self.top_lip.draw(self.surface)
        self.bot_lip.draw(self.surface)
        surface.blit(self.surface, self.position)

    def update(self):
        self.top_lip.update()
        self.bot_lip.update()

    def handle_event(self, event):
        pass

    def set_emotion(self, top_lip_percentages, bot_lip_percentages):
        """
        Set the emotions of the lips using percentage values (0% to 100%).
        """
        # top_lip_percentages and bot_lip_percentages will have tuples (x_percentage, y_percentage) for left and right commissures
        self.top_lip.set_increments({
            'left_commissure': (top_lip_percentages[0], top_lip_percentages[1]),  # x_increment, y_increment
            'center': top_lip_percentages[2],
            'right_commissure': (top_lip_percentages[3], top_lip_percentages[4])  # x_increment, y_increment
        })
        self.bot_lip.set_increments({
            'left_commissure': (bot_lip_percentages[0], bot_lip_percentages[1]),  # x_increment, y_increment
            'center': bot_lip_percentages[2],
            'right_commissure': (bot_lip_percentages[3], bot_lip_percentages[4])  # x_increment, y_increment
        })

    def get_emotion(self):
        """
        Get the emotions of the lips as percentage values (0% to 100%).
        """
        # Retrieve the x and y percentages for left and right commissures
        top_lip_percentages = (
            self.top_lip.increments['left_commissure'][0] / (self.size[0] / 2) * 100,
            self.top_lip.increments['left_commissure'][1] / self.size[1] * 100,
            self.top_lip.increments['center'] / self.size[1] * 100,
            self.top_lip.increments['right_commissure'][0] / (self.size[0] / 2) * 100,
            self.top_lip.increments['right_commissure'][1] / self.size[1] * 100
        )
        bot_lip_percentages = (
            self.bot_lip.increments['left_commissure'][0] / (self.size[0] / 2) * 100,
            self.bot_lip.increments['left_commissure'][1] / self.size[1] * 100,
            self.bot_lip.increments['center'] / self.size[1] * 100,
            self.bot_lip.increments['right_commissure'][0] / (self.size[0] / 2) * 100,
            self.bot_lip.increments['right_commissure'][1] / self.size[1] * 100
        )
        return top_lip_percentages, bot_lip_percentages

    def percentage_to_pixel(self, percentages):
        return [int(val / 100 * self.size[1]) for val in percentages]

    def pixel_to_percentage(self, pixels):
        return [(val / self.size[1]) * 100 for val in pixels]
