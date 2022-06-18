from amulet_editor.models.package import AmuletPlugin, AmuletView
from amulet_editor.tools.packages._pages import PackagesPage
from amulet_editor.tools.packages._panels import PackagesPanel


class Packages(AmuletPlugin):
    def __init__(self) -> None:
        self._page = AmuletView(PackagesPage())
        self._panel = AmuletView(PackagesPanel())

    @property
    def page(self) -> AmuletView:
        return self._page

    @property
    def panel(self) -> AmuletView:
        return self._panel

    @property
    def name(self) -> str:
        return "Packages"

    @property
    def icon_name(self) -> str:
        return "package.svg"
