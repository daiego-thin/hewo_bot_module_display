import os
import pygame
import screeninfo
from hewo_bot_module_display.display.hewo.face import Face
from hewo_bot_module_display.settings.settings_loader import SettingsLoader


class MainWindow:
    def __init__(self, layouts=None, active_layout=None):
        # Cargar configuración
        pygame.init()
        self.settings = SettingsLoader().load_settings('settings.window')
        monitor_id = self.settings['monitor_id']
        monitor_specs = screeninfo.get_monitors()[monitor_id]
        self.window_size = (monitor_specs.width, monitor_specs.height)
        if self.settings['fullscreen']:
            flags = pygame.RESIZABLE
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor_specs.x},{monitor_specs.y}"
        else:
            flags = pygame.RESIZABLE
            os.environ['SDL_VIDEO_WINDOW_POS'] = "540, 130"
        self.screen = pygame.display.set_mode(
            size=self.window_size,
            display=monitor_id,
            flags=flags,
            vsync=True
        )

        pygame.display.set_caption(self.settings['window_title'])
        self.layouts = layouts
        self.clock = pygame.time.Clock()
        self.background_color = self.settings['bg_color']
        self.active_layout = active_layout

    def handle_events(self):
        for event in pygame.event.get():
            # Define window events
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()
                exit()

            # Pass the event_handler to the active canvas
            if self.active_layout is not None:
                self.layouts[self.active_layout].draw(self.screen)

    def set_active_layout(self, layout_index):
        if layout_index < len(self.layouts):
            self.active_layout = layout_index
        else:
            self.active_layout = None
            print(f'Index {layout_index} out of range')

    def update(self):
        if self.active_layout is not None:
            self.layouts[self.active_layout].draw(self.screen)

    def draw(self):
        self.screen.fill(self.background_color)
        if self.active_layout is not None:
            self.layouts[self.active_layout].draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == '__main__':
    main_window = MainWindow(layouts=[Face()], active_layout=0)
    main_window.run()
