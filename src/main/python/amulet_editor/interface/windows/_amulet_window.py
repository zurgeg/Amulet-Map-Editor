from functools import partial

from amulet_editor.data import project
from amulet_editor.interface import appearance
from amulet_editor.interface.appearance import Theme
from amulet_editor.interface.components import (
    QDragContainer,
    QDragIconButton,
    QIconButton,
)
from amulet_editor.interface.windows._file_dialog import OpenFileDialog
from amulet_editor.models.package import AmuletPlugin
from amulet_editor.tools.packages import Packages
from amulet_editor.tools.settings import Settings
from amulet_editor.tools.startup import Startup
from PySide6.QtCore import QCoreApplication, QRect, QSize, Qt
from PySide6.QtGui import QAction, QKeyEvent, QMouseEvent
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class AmuletWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi()

        # Setup side menu
        self.btng_menus = QButtonGroup(self)
        self._active_plugin = Startup()

        self._load_dynamic_menu(self._active_plugin, False)
        self._load_static_menu(Packages())
        self._load_static_menu(Settings())

        self.btng_menus.buttons()[0].setChecked(True)
        self._show_menu_item(self._active_plugin)

        # Connect restyle signal and apply current theme
        appearance.changed.connect(self._theme_changed)

        # Connect menu options
        self.act_open.triggered.connect(self._open_world)
        for theme_name in appearance.list_themes():
            action = QAction(self.mn_appearance)

            action.setCheckable(True)
            if theme_name == appearance.theme().name:
                action.setChecked(True)
            action.setText(theme_name)

            action.triggered.connect(partial(appearance.set_theme, theme_name))

            self.mn_appearance.addAction(action)

    def _get_dynamic_menu_button(self, plugin: AmuletPlugin) -> QDragIconButton:
        icon_button = QDragIconButton(self.wgt_dynamic_menu)
        icon_button.clicked.connect(partial(self._show_menu_item, plugin))
        icon_button.setAutoRaise(True)
        icon_button.setCheckable(True)
        icon_button.setData(plugin.name)
        icon_button.setFixedSize(QSize(40, 40))
        icon_button.toolTip().setText(plugin.name)
        icon_button.setIconSize(QSize(30, 30))
        icon_button.setIcon(plugin.icon_name)

        self.btng_menus.addButton(icon_button)

        return icon_button

    def _get_static_menu_button(self, plugin: AmuletPlugin) -> QIconButton:
        icon_button = QIconButton(self.wgt_dynamic_menu)
        icon_button.clicked.connect(partial(self._show_menu_item, plugin))
        icon_button.setAutoRaise(True)
        icon_button.setCheckable(True)
        icon_button.setFixedSize(QSize(40, 40))
        icon_button.toolTip().setText(plugin.name)
        icon_button.setIconSize(QSize(30, 30))
        icon_button.setIcon(plugin.icon_name)

        self.btng_menus.addButton(icon_button)

        return icon_button

    def _load_dynamic_menu(self, plugin: AmuletPlugin, draggable: bool = True) -> None:
        icon_button = (
            self._get_dynamic_menu_button(plugin)
            if draggable
            else self._get_static_menu_button(plugin)
        )
        self.wgt_dynamic_menu.addItem(icon_button)

        plugin.page.changed.connect(partial(self._change_page, plugin))
        plugin.panel.changed.connect(partial(self._change_left_panel, plugin))

    def _load_static_menu(self, plugin: AmuletPlugin) -> None:
        icon_button = self._get_static_menu_button(plugin)
        self.lyt_static_menu.addWidget(icon_button)

        plugin.page.changed.connect(partial(self._change_page, plugin))
        plugin.panel.changed.connect(partial(self._change_left_panel, plugin))

    def _clear_dynamic_menu(self) -> None:
        # TODO: This should also clear corresponding panels and pages
        for index in range(len(self.wgt_dynamic_menu.layout().children()) + 1):
            item = self.wgt_dynamic_menu.layout().takeAt(index)
            item.widget().deleteLater()

    def _show_menu_item(self, plugin: AmuletPlugin) -> None:
        self._active_plugin = plugin
        self.lbl_left_panel_title.setText(plugin.name)
        self._show_page(plugin.page.widget())
        self._show_left_panel(plugin.panel.widget())

    def _change_page(self, plugin: AmuletPlugin, widget: QWidget) -> None:
        if self._active_plugin == plugin:
            self._show_page(widget)

    def _change_left_panel(self, plugin: AmuletPlugin, widget: QWidget) -> None:
        if self._active_plugin == plugin:
            self._show_left_panel(widget)

    def _show_page(self, page: QWidget) -> None:
        if page not in self.swgt_pages.children():
            self.swgt_pages.addWidget(page)
        self.swgt_pages.setCurrentWidget(page)

    def _show_left_panel(self, panel: QWidget) -> None:
        if panel not in self.swgt_left_panel.children():
            self.swgt_left_panel.addWidget(panel)
        self.swgt_left_panel.setCurrentWidget(panel)

    def _open_world(self):
        self.open_file_dialog = OpenFileDialog(self)
        self.open_file_dialog.file_selected.connect(project.set_root)
        self.open_file_dialog.show()

    def _theme_changed(self, theme: Theme) -> None:
        for theme_action in self.mn_appearance.actions():
            if theme_action.text() == theme.name:
                theme_action.setChecked(True)
            else:
                theme_action.setChecked(False)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        focused = QApplication.focusWidget()
        if event.key() == Qt.Key_Escape and focused is not None:
            focused.clearFocus()

        return super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        focused = QApplication.focusWidget()
        if not focused is None:
            focused.clearFocus()

        return super().mousePressEvent(event)

    def setupUi(self):
        # Create 'Application' widget
        self.wgt_application = QWidget(self)

        # Create 'Application' layout
        self.lyt_application = QGridLayout(self.wgt_application)

        # Configure frame for 'Static Menu' items
        self.frm_static_menu = QFrame(self.wgt_application)
        self.frm_static_menu.setFixedWidth(40)

        # Configure widget for 'Dynamic Menu' items
        self.wgt_dynamic_menu = QDragContainer(self.frm_static_menu)
        self.wgt_dynamic_menu.layout().setAlignment(Qt.AlignTop)
        self.wgt_dynamic_menu.layout().setContentsMargins(0, 0, 0, 0)
        self.wgt_dynamic_menu.layout().setSpacing(0)

        # Configure 'Static Menu' layout
        self.lyt_static_menu = QVBoxLayout(self.frm_static_menu)
        self.lyt_static_menu.setSpacing(0)
        self.lyt_static_menu.setContentsMargins(0, 0, 0, 0)
        self.lyt_static_menu.addWidget(self.wgt_dynamic_menu)

        # Create splitter for 'Application' page and panels
        self.spl_horizontal = QSplitter(self.wgt_application)

        # Configure 'Left Panel' frame
        self.frm_left_panel = QFrame(self.spl_horizontal)
        self.frm_left_panel.setFrameShape(QFrame.NoFrame)
        self.frm_left_panel.setFrameShadow(QFrame.Raised)

        # Create 'Left Panel' layout
        self.lyt_left_panel = QVBoxLayout(self.frm_left_panel)

        # Configure 'Left Panel' header
        self.frm_left_panel_header = QFrame(self.frm_left_panel)
        self.frm_left_panel_header.setMinimumSize(QSize(0, 25))
        self.frm_left_panel_header.setFrameShape(QFrame.NoFrame)
        self.frm_left_panel_header.setFrameShadow(QFrame.Raised)

        # Create title for 'Left Panel'
        self.lbl_left_panel_title = QLabel(self.frm_left_panel_header)

        # Configure 'Left Panel' header layout
        self.lyt_left_panel_header = QHBoxLayout(self.frm_left_panel_header)
        self.lyt_left_panel_header.addWidget(self.lbl_left_panel_title)
        self.lyt_left_panel_header.setSpacing(0)
        self.lyt_left_panel_header.setContentsMargins(9, 0, 9, 0)

        # Configure 'Left Panel' stacked widget (container for 'Left Panel' widgets)
        self.swgt_left_panel = QStackedWidget(self.frm_left_panel)
        spol_pkg_left_panel = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        spol_pkg_left_panel.setHorizontalStretch(0)
        spol_pkg_left_panel.setVerticalStretch(0)
        self.swgt_left_panel.setSizePolicy(spol_pkg_left_panel)
        self.swgt_left_panel.setMinimumSize(QSize(250, 0))

        # Configure 'Left Panel' layout
        self.lyt_left_panel.addWidget(self.frm_left_panel_header)
        self.lyt_left_panel.addWidget(self.swgt_left_panel)
        self.lyt_left_panel.setSpacing(0)
        self.lyt_left_panel.setContentsMargins(0, 0, 0, 0)

        # Configure 'Pages' stacked widget (container for 'Page' widgets)
        self.swgt_pages = QStackedWidget(self.spl_horizontal)
        spol_pages = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        spol_pages.setHorizontalStretch(1)
        spol_pages.setVerticalStretch(0)
        self.swgt_pages.setSizePolicy(spol_pages)
        self.swgt_pages.setMinimumSize(QSize(300, 200))

        # Configure splitter for 'Application' page and panels
        self.spl_horizontal.addWidget(self.frm_left_panel)
        self.spl_horizontal.addWidget(self.swgt_pages)
        self.spl_horizontal.setOrientation(Qt.Horizontal)
        self.spl_horizontal.setHandleWidth(0)

        # Configure 'Application' layout
        self.lyt_application.addWidget(self.frm_static_menu, 0, 0, 1, 1)
        self.lyt_application.addWidget(self.spl_horizontal, 0, 1, 1, 1)
        self.lyt_application.setSpacing(0)
        self.lyt_application.setContentsMargins(0, 0, 0, 0)

        # Create 'Menu Bar'
        self.mnb_amulet = QMenuBar(self)
        self.mnb_amulet.setGeometry(QRect(0, 0, 720, 25))
        self.mnb_amulet.setMinimumSize(QSize(0, 25))

        # Create menus
        self.mn_file = QMenu(self.mnb_amulet)
        self.mn_preferences = QMenu(self.mn_file)
        self.mn_open_recent = QMenu(self.mn_file)
        self.mn_edit = QMenu(self.mnb_amulet)
        self.mn_view = QMenu(self.mnb_amulet)
        self.mn_appearance = QMenu(self.mn_view)

        # Configure 'Open Recent' menu
        self.act_none = QAction(self.mn_open_recent)
        self.act_clear_recently_opened = QAction(self.mn_open_recent)
        self.act_none.setEnabled(False)

        self.mn_open_recent.addAction(self.act_none)
        self.mn_open_recent.addSeparator()
        self.mn_open_recent.addAction(self.act_clear_recently_opened)

        # Configure 'Preferences' menu
        self.act_settings = QAction(self.mn_preferences)
        self.act_keyboard_shortcuts = QAction(self.mn_preferences)

        self.mn_preferences.addAction(self.act_settings)
        self.mn_preferences.addAction(self.act_keyboard_shortcuts)

        # Configure 'File' menu
        self.act_new_window = QAction(self.mn_file)
        self.act_open = QAction(self.mn_file)
        self.act_save = QAction(self.mn_file)
        self.act_save_as = QAction(self.mn_file)
        self.act_save_all = QAction(self.mn_file)

        self.mn_file.addAction(self.act_new_window)
        self.mn_file.addSeparator()
        self.mn_file.addAction(self.act_open)
        self.mn_file.addAction(self.mn_open_recent.menuAction())
        self.mn_file.addSeparator()
        self.mn_file.addAction(self.act_save)
        self.mn_file.addAction(self.act_save_as)
        self.mn_file.addAction(self.act_save_all)
        self.mn_file.addSeparator()
        self.mn_file.addAction(self.mn_preferences.menuAction())

        # Configure 'Edit' menu
        self.act_undo = QAction(self.mn_edit)
        self.act_redo = QAction(self.mn_edit)
        self.act_cut = QAction(self.mn_edit)
        self.act_copy = QAction(self.mn_edit)
        self.act_paste = QAction(self.mn_edit)
        self.act_new_project = QAction(self.mn_edit)

        self.mn_edit.addAction(self.act_undo)
        self.mn_edit.addAction(self.act_redo)
        self.mn_edit.addSeparator()
        self.mn_edit.addAction(self.act_cut)
        self.mn_edit.addAction(self.act_copy)
        self.mn_edit.addAction(self.act_paste)

        # Configure 'View' menu
        self.mn_view.addAction(self.mn_appearance.menuAction())

        # Configure 'Menu Bar'
        self.mnb_amulet.addAction(self.mn_file.menuAction())
        self.mnb_amulet.addAction(self.mn_edit.menuAction())
        self.mnb_amulet.addAction(self.mn_view.menuAction())

        self.spl_horizontal.setCollapsible(1, False)
        self.spl_horizontal.setSizes([250])

        # Create 'Status Bar'
        self.sbar_amulet_status = QStatusBar(self)

        # Configure style properties
        self.frm_static_menu.setProperty("border", "none")
        self.frm_static_menu.setProperty("backgroundColor", "surface")

        self.frm_left_panel_header.setProperty("backgroundColor", "primary")
        self.frm_left_panel_header.setProperty("borderBottom", "surface")
        self.frm_left_panel_header.setProperty("color", "on_surface")

        self.frm_left_panel.setProperty("backgroundColor", "primary")
        self.frm_left_panel.setProperty("borderRight", "surface")
        self.frm_left_panel.setProperty("color", "on_primary")

        # Configure 'Application' window
        self.resize(720, 480)
        self.setCentralWidget(self.wgt_application)
        self.setMenuBar(self.mnb_amulet)
        self.setMinimumSize(QSize(720, 480))
        self.setObjectName("AmuletWindow")
        self.setStatusBar(self.sbar_amulet_status)

        # Translate widget text
        self.retranslateUi()

    def retranslateUi(self):
        # Disable formatting to condense tranlate functions
        # fmt: off
        self.setWindowTitle(QCoreApplication.translate("AmuletWindow", "Amulet Editor", None))
        self.act_open.setText(QCoreApplication.translate("AmuletWindow", "Open Project...", None))
        self.act_open.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+O", None))
        self.act_save.setText(QCoreApplication.translate("AmuletWindow", "Save", None))
        self.act_save.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+S", None))
        self.act_save_as.setText(QCoreApplication.translate("AmuletWindow", "Save As...", None))
        self.act_save_as.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+Shift+S", None))
        self.act_save_all.setText(QCoreApplication.translate("AmuletWindow", "Save All", None))
        self.act_settings.setText(QCoreApplication.translate("AmuletWindow", "Settings", None))
        self.act_settings.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+,", None))
        self.act_keyboard_shortcuts.setText(QCoreApplication.translate("AmuletWindow", "Keyboard Shortcuts", None))
        self.act_keyboard_shortcuts.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+K, Ctrl+S", None))
        self.act_undo.setText(QCoreApplication.translate("AmuletWindow", "Undo", None))
        self.act_undo.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+Z", None))
        self.act_redo.setText(QCoreApplication.translate("AmuletWindow", "Redo", None))
        self.act_redo.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+Y", None))
        self.act_cut.setText(QCoreApplication.translate("AmuletWindow", "Cut", None))
        self.act_cut.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+X", None))
        self.act_copy.setText(QCoreApplication.translate("AmuletWindow", "Copy", None))
        self.act_copy.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+C", None))
        self.act_paste.setText(QCoreApplication.translate("AmuletWindow", "Paste", None))
        self.act_paste.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+V", None))
        self.act_none.setText(QCoreApplication.translate("AmuletWindow", "None", None))
        self.act_clear_recently_opened.setText(QCoreApplication.translate("AmuletWindow", "Clear Recently Opened", None))
        self.act_new_window.setText(QCoreApplication.translate("AmuletWindow", "New Window", None))
        self.act_new_window.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+Shift+N", None))
        self.act_new_project.setText(QCoreApplication.translate("AmuletWindow", "New Project...", None))
        self.act_new_project.setShortcut(QCoreApplication.translate("AmuletWindow", "Ctrl+N", None))
        self.lbl_left_panel_title.setText(QCoreApplication.translate("AmuletWindow", "App Name", None))
        self.mn_file.setTitle(QCoreApplication.translate("AmuletWindow", "File", None))
        self.mn_preferences.setTitle(QCoreApplication.translate("AmuletWindow", "Preferences", None))
        self.mn_open_recent.setTitle(QCoreApplication.translate("AmuletWindow", "Open Recent", None))
        self.mn_edit.setTitle(QCoreApplication.translate("AmuletWindow", "Edit", None))
        self.mn_view.setTitle(QCoreApplication.translate("AmuletWindow", "View", None))
        self.mn_appearance.setTitle(QCoreApplication.translate("AmuletWindow", "Appearance", None))
        # fmt: on
