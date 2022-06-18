import os
import pathlib
from functools import partial
from typing import Optional

import amulet
from amulet_editor.data import build, minecraft, paths
from amulet_editor.data.build import PUBLIC_DATA
from amulet_editor.interface.components import QElidedLabel, QPixCard
from amulet_editor.models.minecraft import LevelData
from amulet_editor.tools.startup._components import QIconButton, QIconCard
from PySide6.QtCore import QCoreApplication, QSize, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SelectPackagesPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi()

        self.btn_next.setEnabled(False)

    def setupUi(self):
        # Create 'Inner Container' frame
        self.frm_inner_container = QFrame(self)
        self.frm_inner_container.setFrameShape(QFrame.NoFrame)
        self.frm_inner_container.setFrameShadow(QFrame.Raised)
        self.frm_inner_container.setMaximumWidth(750)
        self.frm_inner_container.setProperty("borderLeft", "surface")
        self.frm_inner_container.setProperty("borderRight", "surface")

        # Create 'Header' frame
        self.frm_header = QFrame(self.frm_inner_container)

        self.lbl_header = QLabel(self.frm_header)
        self.lbl_header.setProperty("heading", "h3")
        self.lbl_header.setProperty("subfamily", "semi_light")

        lyt_header = QHBoxLayout(self.frm_header)
        lyt_header.addWidget(self.lbl_header)
        lyt_header.setAlignment(Qt.AlignLeft)
        lyt_header.setContentsMargins(0, 0, 0, 10)
        lyt_header.setSpacing(5)

        self.frm_header.setFrameShape(QFrame.NoFrame)
        self.frm_header.setFrameShadow(QFrame.Raised)
        self.frm_header.setLayout(lyt_header)
        self.frm_header.setProperty("borderBottom", "surface")
        self.frm_header.setProperty("borderTop", "background")

        # Create 'Level Data' frame
        lyt_level_data = QGridLayout(self.frm_inner_container)

        self.frm_level_data = QFrame(self.frm_inner_container)
        self.frm_level_data.setFixedHeight(105)
        self.frm_level_data.setFrameShape(QFrame.NoFrame)
        self.frm_level_data.setFrameShadow(QFrame.Raised)
        self.frm_level_data.setLayout(lyt_level_data)
        self.frm_level_data.setProperty("backgroundColor", "primary")
        self.frm_level_data.setProperty("border", "surface")
        self.frm_level_data.setProperty("borderRadiusVisible", True)

        # Create 'Page Options' frame
        self.frm_page_options = QFrame(self)

        # Configure 'Page Options' widgets
        self.btn_cancel = QPushButton(self.frm_page_options)
        self.btn_cancel.setFixedHeight(30)

        self.btn_back = QPushButton(self.frm_page_options)
        self.btn_back.setFixedHeight(30)

        self.btn_next = QPushButton(self.frm_page_options)
        self.btn_next.setFixedHeight(30)
        self.btn_next.setProperty("backgroundColor", "secondary")

        # Create 'Page Options' layout
        lyt_page_options = QHBoxLayout(self.frm_inner_container)
        lyt_page_options.addWidget(self.btn_cancel)
        lyt_page_options.addStretch()
        lyt_page_options.addWidget(self.btn_back)
        lyt_page_options.addWidget(self.btn_next)
        lyt_page_options.setContentsMargins(0, 10, 0, 5)
        lyt_page_options.setSpacing(5)

        # Configure 'Page Options' frame
        self.frm_page_options.setFrameShape(QFrame.NoFrame)
        self.frm_page_options.setFrameShadow(QFrame.Raised)
        self.frm_page_options.setLayout(lyt_page_options)
        self.frm_page_options.setProperty("borderTop", "surface")

        # Create 'Inner Frame' layout
        lyt_inner_frame = QVBoxLayout(self.frm_inner_container)
        lyt_inner_frame.addWidget(self.frm_header)
        lyt_inner_frame.addSpacing(10)
        lyt_inner_frame.addWidget(self.frm_level_data)
        lyt_inner_frame.addStretch()
        lyt_inner_frame.addWidget(self.frm_page_options)
        lyt_inner_frame.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        lyt_inner_frame.setSpacing(5)

        # Configure 'Page' layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.frm_inner_container)
        layout.setAlignment(Qt.AlignHCenter)

        self.setLayout(layout)

        # Translate widget text
        self.retranslateUi()

    def retranslateUi(self):
        # Disable formatting to condense tranlate functions
        # fmt: off
        self.lbl_header.setText(QCoreApplication.translate("NewProjectTypePage", "Packages", None))
        self.btn_cancel.setText(QCoreApplication.translate("NewProjectTypePage", "Cancel", None))
        self.btn_back.setText(QCoreApplication.translate("NewProjectTypePage", "Back", None))
        self.btn_next.setText(QCoreApplication.translate("NewProjectTypePage", "Next", None))
        # fmt: on
