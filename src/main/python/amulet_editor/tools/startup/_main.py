from functools import partial
from typing import Optional

from amulet_editor.models.package import AmuletTool, AmuletView
from amulet_editor.tools.startup.pages._import_level import ImportLevelPage
from amulet_editor.tools.startup.pages._new_project import NewProjectPage
from amulet_editor.tools.startup.pages._open_world import OpenWorldPage
from amulet_editor.tools.startup.pages._select_packages import SelectPackagesPage
from amulet_editor.tools.startup.pages._startup import StartupPage
from amulet_editor.tools.startup.panels._startup import StartupPanel
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget


class Startup(AmuletTool):
    def __init__(self) -> None:

        self._page = AmuletView(StartupPage())
        self._panel = AmuletView(StartupPanel())

        self.view_manager = StartupViewManager(self)

    def set_page(self, widget: QWidget):
        self._page.setWidget(widget)

    def set_panel(self, widget: QWidget):
        self._panel.setWidget(widget)

    @property
    def page(self) -> AmuletView:
        return self._page

    @property
    def primary_panel(self) -> AmuletView:
        return self._panel

    @property
    def secondary_panel(self) -> AmuletView:
        return self._panel

    @property
    def name(self) -> str:
        return "Startup"

    @property
    def icon_name(self) -> str:
        return "hexagons.svg"


class StartupViewManager(QObject):
    def __init__(self, plugin: AmuletTool) -> None:
        super().__init__()

        self.plugin = plugin

        self.startup_page = StartupPage()
        self.open_world_page: Optional[OpenWorldPage] = None
        self.new_project_page: Optional[NewProjectPage] = None
        self.import_level_page: Optional[ImportLevelPage] = None
        self.select_packages_page: Optional[SelectPackagesPage] = None

        self.startup_panel = StartupPanel()

        self.set_startup_page()
        self.set_startup_panel()

    def set_startup_page(self) -> None:
        if self.open_world_page is not None:
            self.open_world_page.deleteLater()
        if self.new_project_page is not None:
            self.new_project_page.deleteLater()
        if self.import_level_page is not None:
            self.import_level_page.deleteLater()
        if self.select_packages_page is not None:
            self.select_packages_page.deleteLater()

        self.open_world_page = OpenWorldPage()
        self.new_project_page = NewProjectPage()
        self.import_level_page = ImportLevelPage()
        self.select_packages_page = SelectPackagesPage()

        # Connect signals
        self.startup_page.crd_open_level.pushButton().clicked.connect(
            partial(self.set_open_world_page)
        )
        self.startup_page.crd_new_project.pushButton().clicked.connect(
            partial(self.set_new_project_page)
        )

        # Set page
        self.plugin.set_page(self.startup_page)

    def set_open_world_page(self) -> None:
        # Connect signals
        self.open_world_page.btn_cancel.clicked.connect(partial(self.set_startup_page))
        self.open_world_page.btn_next.clicked.connect(
            partial(self.set_select_packages_page)
        )

        # Set page
        self.plugin.set_page(self.open_world_page)

    def set_new_project_page(self) -> None:
        def enable_next(project_name: str) -> None:
            project_name = project_name.strip()

            self.new_project_page.btn_next.setEnabled(len(project_name) > 0)

        # Connect signals
        self.new_project_page.lne_project_name.textChanged.connect(enable_next)
        self.new_project_page.btn_cancel.clicked.connect(partial(self.set_startup_page))
        self.new_project_page.btn_next.clicked.connect(
            partial(self.set_import_level_page)
        )

        # Set page
        self.plugin.set_page(self.new_project_page)

    def set_import_level_page(self) -> None:
        # Connect signals
        self.import_level_page.btn_cancel.clicked.connect(
            partial(self.set_startup_page)
        )
        self.import_level_page.btn_back.clicked.connect(
            partial(self.set_new_project_page)
        )

        # Set page
        self.plugin.set_page(self.import_level_page)

    def set_select_packages_page(self) -> None:
        # Connect signals
        self.select_packages_page.btn_cancel.clicked.connect(
            partial(self.set_startup_page)
        )
        self.select_packages_page.btn_back.clicked.connect(
            partial(self.set_open_world_page)
        )

        # Set page
        self.plugin.set_page(self.select_packages_page)

    def set_startup_panel(self) -> None:
        self.plugin.set_panel(self.startup_panel)
