import pathlib
import webbrowser
from dataclasses import dataclass
from functools import partial
from typing import Optional

import amulet
from amulet_editor.data import build, minecraft, project
from amulet_editor.data.build import PUBLIC_DATA, get_resource
from amulet_editor.interface.components import QLinkCard, QPixCard
from amulet_editor.models.minecraft import LevelData
from amulet_editor.models.package import AmuletTool, AmuletView
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QScrollArea, QVBoxLayout, QWidget


@dataclass
class LinkData:
    name: str
    icon: str
    url: str


class HomePage(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)

        self.lbl_recent = QLabel("Recent Projects")
        self.lbl_recent.setProperty("heading", "h4")
        self.scr_recent = QScrollArea()
        self.wgt_recent = QWidget(self.scr_recent)
        self.lyt_recent = QVBoxLayout()

        self.lyt_recent.addStretch()
        self.lyt_recent.setContentsMargins(0, 0, 5, 0)
        self.wgt_recent.setLayout(self.lyt_recent)
        self.wgt_recent.setProperty("style", "background")
        self.scr_recent.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scr_recent.setProperty("style", "background")
        self.scr_recent.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scr_recent.setWidgetResizable(True)
        self.scr_recent.setWidget(self.wgt_recent)

        layout_recent = QVBoxLayout()
        layout_recent.addWidget(self.lbl_recent)
        layout_recent.addWidget(self.scr_recent)
        layout_recent.setAlignment(Qt.AlignTop)
        self.frm_recent_projects = QFrame()
        self.frm_recent_projects.setLayout(layout_recent)

        self.lbl_start = QLabel("Getting Started")
        self.lbl_start.setProperty("heading", "h4")

        layout_start = QVBoxLayout()
        layout_start.setAlignment(Qt.AlignTop)
        layout_start.addWidget(self.lbl_start)
        self.frm_start_project = QFrame()
        self.frm_start_project.setLayout(layout_start)

        amulet_logo = QPixmap(QImage(get_resource("images/amulet_logo.png")))
        amulet_logo = amulet_logo.scaledToHeight(128)
        self.lbl_app_icon = QLabel()
        self.lbl_app_icon.setAlignment(Qt.AlignCenter)
        self.lbl_app_icon.setPixmap(amulet_logo)

        self.lbl_app_name = QLabel("Amulet Editor")
        self.lbl_app_name.setAlignment(Qt.AlignCenter)
        self.lbl_app_name.setProperty("heading", "h1")
        self.lbl_app_name.setProperty("subfamily", "semi_light")

        self.lbl_app_version = QLabel(f"Version {PUBLIC_DATA['version']}")
        self.lbl_app_version.setAlignment(Qt.AlignCenter)
        self.lbl_app_version.setProperty("color", "secondary")
        self.lbl_app_version.setProperty("heading", "h5")
        self.lbl_app_version.setProperty("subfamily", "semi_light")

        layout_header = QVBoxLayout()
        layout_header.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout_header.addWidget(self.lbl_app_icon)
        layout_header.addWidget(self.lbl_app_name)
        layout_header.addWidget(self.lbl_app_version)
        self.frm_header = QFrame()
        self.frm_header.setLayout(layout_header)

        layout = QVBoxLayout(self)
        layout.addWidget(self.frm_header)
        layout.addWidget(self.frm_recent_projects)
        self.setLayout(layout)

        self._world_cards: list[QPixCard] = []

        self.load_world_cards()

    def card_clicked(self, clicked_card: QPixCard):
        for card in self._world_cards:
            card.pushButton().setChecked(False)

        clicked_card.pushButton().setChecked(True)

        project.set_root(clicked_card.level_data.path)

    def load_world_cards(self) -> None:
        self._sort_descending = False
        level_paths = minecraft.locate_worlds(minecraft.save_directories())

        for path in level_paths:
            level_data = LevelData(amulet.load_format(path))

            icon_path = (
                level_data.icon_path
                if level_data.icon_path is not None
                else build.get_resource("images/missing_world_icon.png")
            )
            level_icon = QPixmap(QImage(icon_path))
            level_icon = level_icon.scaledToHeight(80)

            level_name = level_data.name.get_html(font_weight=600)
            file_name = pathlib.PurePath(level_data.path).name
            version = f"{level_data.edition} - {level_data.version}"
            last_played = (
                level_data.last_played.astimezone(tz=None)
                .strftime("%B %d, %Y %I:%M %p")
                .replace(" 0", " ")
            )

            world_card = QPixCard(level_icon, self.wgt_recent)
            world_card.addLabel(level_name)
            world_card.addLabel(file_name)
            world_card.addLabel(version)
            world_card.addLabel(last_played)
            world_card.pushButton().setCheckable(True)
            world_card.pushButton().setFocusPolicy(Qt.NoFocus)
            world_card.pushButton().clicked.connect(
                partial(self.card_clicked, world_card)
            )
            world_card.level_data = level_data

            self.lyt_recent.insertWidget(self.lyt_recent.count() - 1, world_card)
            world_card.show()

            self._world_cards.append(world_card)


class HomePanel(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent=parent)

        self.frm_links = QFrame(self)
        self.frm_links.setFrameShape(QFrame.NoFrame)
        self.frm_links.setFrameShadow(QFrame.Raised)

        self.lyt_links = QVBoxLayout(self.frm_links)
        self.lyt_links.setAlignment(Qt.AlignTop)
        self.lyt_links.setSpacing(0)

        self.setLayout(QVBoxLayout(self))
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.frm_links)

        links: list[LinkData] = [
            LinkData(
                "Website",
                "world.svg",
                "https://www.amuletmc.com/",
            ),
            LinkData(
                "GitHub",
                "brand-github.svg",
                "https://github.com/Amulet-Team/Amulet-Map-Editor",
            ),
            LinkData(
                "Discord",
                "brand-discord.svg",
                "https://www.amuletmc.com/discord",
            ),
            LinkData(
                "Feedback",
                "flag.svg",
                "https://github.com/Amulet-Team/Amulet-Map-Editor/issues/new/choose",
            ),
        ]

        for link in links:
            link_card = QLinkCard(
                link.name, build.get_resource(f"icons/{link.icon}"), self.frm_links
            )
            link_card.pushButton().clicked.connect(partial(webbrowser.open, link.url))
            self.frm_links.layout().addWidget(link_card)


class Home(AmuletTool):
    def __init__(self) -> None:
        self.pkg_pages = (HomePage(),)
        self.pkg_panels = (HomePanel(),)

    def page(self) -> AmuletView:
        return self.pkg_pages[0]

    def panel(self) -> AmuletView:
        return self.pkg_panels[0]

    @property
    def name(self) -> str:
        return "Home"

    @property
    def icon_name(self) -> str:
        return "home.svg"
