import webbrowser
from dataclasses import dataclass
from functools import partial
from typing import Optional

from amulet_editor.data import build
from amulet_editor.interface.components import QLinkCard
from amulet_editor.models.package import AmuletPlugin
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget


@dataclass
class LinkData:
    name: str
    icon: str
    url: str


class StartupPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

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
            link_card.setMaximumWidth(250)
            self.frm_links.layout().addWidget(link_card)
