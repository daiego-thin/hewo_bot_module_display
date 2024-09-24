"""
Sandbox is the main scene where you can playtest with your game components
"""

import screeninfo
import pygame
import os
import sys
from hewo_bot_module_display.display.hewo.face import Face
from hewo_bot_module_display.settings.settings_loader import SettingsLoader


class SandBox:

    def __init__(self, elements=None, fullscreen=False, display=None):
        pygame.init()
        self.WINDOW_SIZE = (
            display['width'],
            display['height']
        )
        self.BACKGROUND_COLOR = (display['bg_color']['r'],
                                 display['bg_color']['g'],
                                 display['bg_color']['b'])
        self.find_and_set_display(display)
        pygame.display.set_caption("Testing Sandbox")
        print("Press F to toggle fullscreen.")
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_fullscreen = fullscreen
        self.elements = elements

        if self.is_fullscreen:
            flags = pygame.FULLSCREEN
        else:
            flags = pygame.RESIZABLE

        self.screen = pygame.display.set_mode(size=self.WINDOW_SIZE,
                                              flags=flags,
                                              display=self.HEWO_DISPLAY,
                                              vsync=True)

    def find_and_set_display(self, display):
        print("Looking for HeWo's display...")
        found = False
        for i, monitor in enumerate(screeninfo.get_monitors()):
            if display['width'] == monitor.width and display['height'] == monitor.height:
                self.HEWO_DISPLAY = i
                self.WINDOW_SIZE = monitor.width, monitor.height
                os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor.x},{monitor.y}"
                print("HeWo's display found at:", self.HEWO_DISPLAY)
                found = True
                break

        if not found:
            self.HEWO_DISPLAY = display['id']
            print("Desired HeWo display not found. Using display:", self.HEWO_DISPLAY)
            print("Full screen will be disabled.")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick()
        self.quit()

    def handle_events(self):
        # To Do: Also use the handle events method to publish and suscribe to topics
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.HEWO_DISPLAY != 0:
                        self.toggle_fullscreen()
                if event.key == pygame.K_F2:
                    self.running = False
            if self.elements is not None:
                for elem in self.elements:
                    elem.handle_event(events)

    def update(self):
        # To Do: Use update method to publish and suscribe to the corresponding topics
        if self.elements is not None:
            for elem in self.elements:
                elem.update()

    def draw(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        if self.elements is not None:
            for elem in self.elements:
                elem.draw(self.screen)
        pygame.display.flip()

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode(size=self.WINDOW_SIZE,
                                                  flags=pygame.RESIZABLE,
                                                  display=self.HEWO_DISPLAY,
                                                  vsync=True)
            self.is_fullscreen = False
        else:
            self.screen = pygame.display.set_mode(size=self.WINDOW_SIZE,
                                                  flags=pygame.FULLSCREEN,
                                                  display=self.HEWO_DISPLAY,
                                                  vsync=True)
            self.is_fullscreen = True
        pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    layout_settings = 'test'
    display = SettingsLoader().load_settings(f'settings.layouts.{layout_settings}')

    if layout_settings == 'main':
        max_size = (display['width'], display['height'])
        pos = [display['width'] // 5, display['height'] // 5]
        elements = [
            Face(position=pos, enable_controls=False, max_size=max_size),
        ]
    elif layout_settings == 'test':
        max_size = (display['width'], display['height'])
        pos = [display['width'] // 5 + 425, display['height'] // 5]
        elements = [
            Face(position=pos, enable_controls=True, max_size=max_size),
        ]
    else:
        elements = None
    sandbox = SandBox(elements, fullscreen=False, display=display)
    sandbox.run()
