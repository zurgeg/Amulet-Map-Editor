from amulet_editor.models.package import AmuletPlugin, AmuletView
from amulet_editor.tools.settings._pages import SettingsPage
from amulet_editor.tools.settings._panels import SettingsPanel


class Settings(AmuletPlugin):
    def __init__(self) -> None:
        self._page = AmuletView(SettingsPage())
        self._panel = AmuletView(SettingsPanel())

    @property
    def page(self) -> AmuletView:
        return self._page

    @property
    def panel(self) -> AmuletView:
        return self._panel

    @property
    def name(self) -> str:
        return "Settings"

    @property
    def icon_name(self) -> str:
        return "settings.svg"
