"""
Settings loader carga los settings presentes en cada yaml del módulo settings.
"""

import yaml
import pathlib
import importlib.util


class SettingsLoader:
    def __init__(self, module_name=None):
        self.settings_path = None
        self.settings = {}
        if module_name is not None:
            self.load_settings(module_name)

    def load_settings(self, module_name):
        module = importlib.import_module(module_name)
        settings_path = pathlib.Path(module.__file__).parent

        if not settings_path.exists() or not settings_path.is_dir():
            raise FileNotFoundError(f"No se encontró el directorio de settings en: {settings_path}")

        for setting_file in settings_path.glob('*.yaml'):
            with open(setting_file, 'r') as file:
                settings = yaml.load(file, Loader=yaml.FullLoader)
                self.settings.update(settings)
                self.settings_path = setting_file

        return self.settings

    def pretty_print(self):
        print(yaml.dump(self.settings, default_flow_style=False, sort_keys=False, allow_unicode=True))

    def save_settings(self, settings):
        with open(self.settings_path, 'w') as file:
            yaml.dump(settings, file, default_flow_style=False, sort_keys=False, allow_unicode=True)


if __name__ == '__main__':
    loader = SettingsLoader()
    loader.load_settings('settings.hewo')
    loader.pretty_print()
