import pathlib
from distutils.version import StrictVersion
from functools import partial

import amulet
from amulet_editor.data import build, minecraft
from amulet_editor.interface import appearance
from amulet_editor.interface.appearance import Theme
from amulet_editor.interface.components import QPixCard
from amulet_editor.interface.windows._ui_file_dialog import Ui_FileDialog
from amulet_editor.models.minecraft import LevelData
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QWidget


class OpenFileDialog(QWidget, Ui_FileDialog):
    file_selected = Signal(str)

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent=parent, f=Qt.Window)

        self.setupUi(self)

        self.spl_search.setSizes([0, 1])
        self.spl_search.handle(1).setEnabled(False)

        self.ln_vertical_1.setMaximumWidth(1)
        self.ln_vertical_2.setMaximumWidth(1)

        self.ln_vertical_1.setObjectName("vertical_separator")
        self.ln_vertical_2.setObjectName("vertical_separator")

        self._world_cards: list[QPixCard] = []
        self._world_cards_filtered: list[QPixCard] = []

        self.load_world_cards()

        # Connect events
        self.cbx_edition.currentIndexChanged.connect(self.filter_cards)
        self.cbx_sort_by.currentIndexChanged.connect(self.sort_cards)
        self.cbx_version.currentIndexChanged.connect(self.filter_cards)
        self.le_search_box.textChanged.connect(self.filter_cards)
        self.tbtn_sort_order.clicked.connect(self.toggle_sort)

        # Connect restyle signal and apply current theme
        appearance.changed.connect(self.style_ui)
        self.style_ui(appearance.theme())

    def card_clicked(self, clicked_card: QPixCard, path: str):
        if clicked_card.pushButton().isChecked():
            for world_card in self._world_cards:
                if not world_card.pushButton() == clicked_card.pushButton():
                    world_card.pushButton().setChecked(False)
        else:
            self.file_selected.emit(clicked_card.level_data.path)
            self.close()

    def load_world_cards(self) -> None:
        self._sort_descending = False
        level_paths = minecraft.locate_worlds(minecraft.save_directories())

        world_versions = []
        unknown_version_present = False
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

            world_card = QPixCard(level_icon, self.wgt_search_results)
            world_card.addLabel(level_name)
            world_card.addLabel(file_name)
            world_card.addLabel(version)
            world_card.addLabel(last_played)
            world_card.pushButton().setCheckable(True)
            world_card.pushButton().setFocusPolicy(Qt.NoFocus)
            world_card.pushButton().clicked.connect(
                partial(self.card_clicked, world_card, path)
            )
            world_card.level_data = level_data

            self._world_cards.append(world_card)

            if not any(c.isalpha() for c in level_data.version):
                world_versions.append("{}.{}".format(*level_data.version.split(".")))
            elif level_data.version == "Unknown":
                unknown_version_present = True

        world_versions = list(set(world_versions))
        world_versions.sort(key=StrictVersion, reverse=True)
        for version in world_versions:
            self.cbx_version.addItem(version)
        if unknown_version_present:
            self.cbx_version.addItem("Unknown")

        self._world_cards_filtered = self._world_cards
        self.sort_cards()

    def style_ui(self, theme: Theme) -> None:
        self.setStyleSheet(theme.get_style_sheet("open_file_dialog.qss"))

    def toggle_sort(self) -> None:
        self._sort_descending = not self._sort_descending

        if self._sort_descending:
            self.tbtn_sort_order.setArrowType(Qt.DownArrow)
        else:
            self.tbtn_sort_order.setArrowType(Qt.UpArrow)

        self.sort_cards()

    # Methods for filtering and sorting world cards
    def filter_cards(self) -> None:
        search_text = self.le_search_box.text()
        edition = self.cbx_edition.currentText()
        version = self.cbx_version.currentText()

        self._world_cards_filtered = []
        for world_card in self._world_cards:
            if (
                search_text.lower()
                in world_card.level_data.name.get_plain_text().lower()
                and (edition == "Any" or edition == world_card.level_data.edition)
                and (version == "Any" or version in world_card.level_data.version)
            ):
                self._world_cards_filtered.append(world_card)

        self.sort_cards()

    def sort_cards(self):
        sort_by = self.cbx_sort_by.currentText()

        if sort_by == "Name":
            self._world_cards_filtered.sort(
                key=lambda card: "".join(
                    char
                    for char in card.level_data.name.get_plain_text()
                    if char.isalnum()
                ),
                reverse=self._sort_descending,
            )
        elif sort_by == "Last Played":
            self._world_cards_filtered.sort(
                key=lambda card: card.level_data.last_played,
                reverse=self._sort_descending,
            )

        for world_card in self.wgt_search_results.children():
            if isinstance(world_card, QPixCard):
                world_card.hide()
                self.wgt_search_results.layout().removeWidget(world_card)

        for world_card in self._world_cards_filtered:
            self.wgt_search_results.layout().insertWidget(
                self.wgt_search_results.layout().count() - 1, world_card
            )
            world_card.show()
