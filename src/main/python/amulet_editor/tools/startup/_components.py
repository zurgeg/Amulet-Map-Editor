from typing import Optional

from amulet_editor.data import build
from amulet_editor.interface import appearance
from amulet_editor.interface.appearance import Color, Theme
from amulet_editor.interface.components._icon import QSvgIcon
from amulet_editor.interface.components._label import QElidedLabel
from PySide6.QtCore import QEvent, QSize, Qt
from PySide6.QtGui import QEnterEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QToolButton, QWidget
from QtDesign6.QtdWidgets import QCard


class QIconButton(QToolButton):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self._icon_name = "question-mark"

        appearance.changed.connect(self.retheme)

    def setIcon(self, icon_name: Optional[str] = None) -> None:
        self._icon_name = icon_name

        self.repaint(appearance.theme().on_surface)

    def repaint(self, color: Color) -> None:
        super().setIcon(
            QSvgIcon(
                build.get_resource(f"icons/{self._icon_name}"),
                self.iconSize(),
                color.get_qcolor(),
            )
        )
        self.setStyleSheet(f"color: {color.get_hex()}")

    def retheme(self, theme: Theme) -> None:
        self.repaint(theme.on_surface)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.repaint(appearance.theme().on_primary)
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.repaint(appearance.theme().on_surface)
        return super().leaveEvent(event)


class QIconCard(QCard):
    def __init__(
        self,
        icon: str,
        icon_size: QSize,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent=parent)

        self.icon_path = icon
        self.icon_size = icon_size

        self.lbl_icon = QLabel()
        self.lbl_description = QElidedLabel()

        self.lbl_icon.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_icon.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.lbl_description.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        layout = QHBoxLayout()
        layout.addWidget(self.lbl_icon)
        layout.addWidget(self.lbl_description)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.setLayout(layout)

        self.repaint(appearance.theme().on_surface)

        appearance.changed.connect(self.retheme)

    def setText(self, text: str, heading: Optional[str]):
        if heading is not None:
            self.lbl_description.setProperty("heading", heading)

        self.lbl_description.setProperty("subfamily", "semi_light")
        self.lbl_description.setText(text)

    def setIcon(self, icon_path: str) -> None:
        if self.icon_path is None:
            layout: QHBoxLayout = self.layout()
            layout.insertWidget(0, self.lbl_icon)
        self.icon_path = icon_path
        self.repaint(appearance.theme().on_surface)

    def repaint(self, color: Color) -> None:
        if self.icon_path is not None:
            self.lbl_icon.setPixmap(
                QSvgIcon(self.icon_path, self.icon_size, color.get_qcolor()).pixmap(
                    self.icon_size
                )
            )
        self.setStyleSheet(f"color: {color.get_hex()}")

    def retheme(self, theme: Theme) -> None:
        self.repaint(theme.on_surface)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.repaint(appearance.theme().on_primary)
        return super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.repaint(appearance.theme().on_surface)
        return super().leaveEvent(event)
