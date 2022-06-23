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
from amulet_editor.models.package import AmuletTool
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QVBoxLayout, QWidget


@dataclass
class LinkData:
    name: str
    icon: str
    url: str


class StartupPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()

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
