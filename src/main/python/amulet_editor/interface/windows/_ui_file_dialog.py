# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_file_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QSplitter,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class Ui_FileDialog(object):
    def setupUi(self, FileDialog):
        if not FileDialog.objectName():
            FileDialog.setObjectName(u"FileDialog")
        FileDialog.setWindowModality(Qt.WindowModal)
        FileDialog.resize(720, 480)
        FileDialog.setMinimumSize(QSize(720, 480))
        self.gridLayout = QGridLayout(FileDialog)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frm_search_actions = QFrame(FileDialog)
        self.frm_search_actions.setObjectName(u"frm_search_actions")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.frm_search_actions.sizePolicy().hasHeightForWidth()
        )
        self.frm_search_actions.setSizePolicy(sizePolicy)
        self.frm_search_actions.setFrameShape(QFrame.NoFrame)
        self.frm_search_actions.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frm_search_actions)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frm_sort = QFrame(self.frm_search_actions)
        self.frm_sort.setObjectName(u"frm_sort")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frm_sort.sizePolicy().hasHeightForWidth())
        self.frm_sort.setSizePolicy(sizePolicy1)
        self.frm_sort.setFrameShape(QFrame.NoFrame)
        self.frm_sort.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frm_sort)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tbtn_sort_order = QToolButton(self.frm_sort)
        self.tbtn_sort_order.setObjectName(u"tbtn_sort_order")
        self.tbtn_sort_order.setMinimumSize(QSize(24, 24))
        self.tbtn_sort_order.setFocusPolicy(Qt.NoFocus)
        self.tbtn_sort_order.setArrowType(Qt.UpArrow)

        self.horizontalLayout_2.addWidget(self.tbtn_sort_order)

        self.cbx_sort_by = QComboBox(self.frm_sort)
        self.cbx_sort_by.addItem("")
        self.cbx_sort_by.addItem("")
        self.cbx_sort_by.setObjectName(u"cbx_sort_by")
        self.cbx_sort_by.setMinimumSize(QSize(0, 24))
        self.cbx_sort_by.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_2.addWidget(self.cbx_sort_by)

        self.gridLayout_2.addWidget(self.frm_sort, 1, 3, 1, 1)

        self.lbl_version = QLabel(self.frm_search_actions)
        self.lbl_version.setObjectName(u"lbl_version")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbl_version.sizePolicy().hasHeightForWidth())
        self.lbl_version.setSizePolicy(sizePolicy2)
        self.lbl_version.setMinimumSize(QSize(125, 0))
        self.lbl_version.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.lbl_version, 0, 1, 1, 1)

        self.lbl_edition = QLabel(self.frm_search_actions)
        self.lbl_edition.setObjectName(u"lbl_edition")
        sizePolicy2.setHeightForWidth(self.lbl_edition.sizePolicy().hasHeightForWidth())
        self.lbl_edition.setSizePolicy(sizePolicy2)
        self.lbl_edition.setMinimumSize(QSize(125, 0))
        self.lbl_edition.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.lbl_edition, 0, 0, 1, 1)

        self.ln_vertical_1 = QFrame(self.frm_search_actions)
        self.ln_vertical_1.setObjectName(u"ln_vertical_1")
        self.ln_vertical_1.setFrameShape(QFrame.VLine)
        self.ln_vertical_1.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.ln_vertical_1, 0, 2, 2, 1)

        self.lbl_sort_by = QLabel(self.frm_search_actions)
        self.lbl_sort_by.setObjectName(u"lbl_sort_by")
        sizePolicy2.setHeightForWidth(self.lbl_sort_by.sizePolicy().hasHeightForWidth())
        self.lbl_sort_by.setSizePolicy(sizePolicy2)
        self.lbl_sort_by.setMinimumSize(QSize(150, 0))

        self.gridLayout_2.addWidget(self.lbl_sort_by, 0, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 5, 1, 1)

        self.cbx_version = QComboBox(self.frm_search_actions)
        self.cbx_version.addItem("")
        self.cbx_version.setObjectName(u"cbx_version")
        self.cbx_version.setMinimumSize(QSize(0, 24))
        self.cbx_version.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.cbx_version, 1, 1, 1, 1)

        self.cbx_edition = QComboBox(self.frm_search_actions)
        self.cbx_edition.addItem("")
        self.cbx_edition.addItem("")
        self.cbx_edition.addItem("")
        self.cbx_edition.setObjectName(u"cbx_edition")
        self.cbx_edition.setMinimumSize(QSize(0, 24))
        self.cbx_edition.setFocusPolicy(Qt.NoFocus)

        self.gridLayout_2.addWidget(self.cbx_edition, 1, 0, 1, 1)

        self.ln_vertical_2 = QFrame(self.frm_search_actions)
        self.ln_vertical_2.setObjectName(u"ln_vertical_2")
        self.ln_vertical_2.setFrameShape(QFrame.VLine)
        self.ln_vertical_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.ln_vertical_2, 0, 4, 2, 1)

        self.gridLayout.addWidget(self.frm_search_actions, 0, 0, 1, 1)

        self.frm_search = QFrame(FileDialog)
        self.frm_search.setObjectName(u"frm_search")
        sizePolicy.setHeightForWidth(self.frm_search.sizePolicy().hasHeightForWidth())
        self.frm_search.setSizePolicy(sizePolicy)
        self.frm_search.setFrameShape(QFrame.NoFrame)
        self.frm_search.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frm_search)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 9)
        self.le_search_box = QLineEdit(self.frm_search)
        self.le_search_box.setObjectName(u"le_search_box")
        self.le_search_box.setMinimumSize(QSize(0, 26))
        self.le_search_box.setClearButtonEnabled(False)

        self.horizontalLayout.addWidget(self.le_search_box)

        self.pbtn_browse = QPushButton(self.frm_search)
        self.pbtn_browse.setObjectName(u"pbtn_browse")
        self.pbtn_browse.setMinimumSize(QSize(0, 26))

        self.horizontalLayout.addWidget(self.pbtn_browse)

        self.gridLayout.addWidget(self.frm_search, 1, 0, 1, 1)

        self.spl_search = QSplitter(FileDialog)
        self.spl_search.setObjectName(u"spl_search")
        self.spl_search.setOrientation(Qt.Horizontal)
        self.spl_search.setHandleWidth(0)
        self.swgt_search_panel = QStackedWidget(self.spl_search)
        self.swgt_search_panel.setObjectName(u"swgt_search_panel")
        sizePolicy1.setHeightForWidth(
            self.swgt_search_panel.sizePolicy().hasHeightForWidth()
        )
        self.swgt_search_panel.setSizePolicy(sizePolicy1)
        self.swgt_search_panel.setMinimumSize(QSize(200, 0))
        self.swgt_search_panel.setFrameShape(QFrame.NoFrame)
        self.swgt_search_panel.setFrameShadow(QFrame.Raised)
        self.spl_search.addWidget(self.swgt_search_panel)
        self.scr_search_results = QScrollArea(self.spl_search)
        self.scr_search_results.setObjectName(u"scr_search_results")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.scr_search_results.sizePolicy().hasHeightForWidth()
        )
        self.scr_search_results.setSizePolicy(sizePolicy3)
        self.scr_search_results.setMinimumSize(QSize(200, 0))
        self.scr_search_results.setFocusPolicy(Qt.NoFocus)
        self.scr_search_results.setFrameShape(QFrame.NoFrame)
        self.scr_search_results.setFrameShadow(QFrame.Plain)
        self.scr_search_results.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scr_search_results.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scr_search_results.setWidgetResizable(True)
        self.wgt_search_results = QWidget()
        self.wgt_search_results.setObjectName(u"wgt_search_results")
        self.wgt_search_results.setGeometry(QRect(0, 0, 342, 370))
        self.verticalLayout_2 = QVBoxLayout(self.wgt_search_results)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scr_search_results.setWidget(self.wgt_search_results)
        self.spl_search.addWidget(self.scr_search_results)

        self.gridLayout.addWidget(self.spl_search, 2, 0, 1, 1)

        self.retranslateUi(FileDialog)

        QMetaObject.connectSlotsByName(FileDialog)

    # setupUi

    def retranslateUi(self, FileDialog):
        FileDialog.setWindowTitle(
            QCoreApplication.translate("FileDialog", u"Open World", None)
        )
        self.tbtn_sort_order.setText(
            QCoreApplication.translate("FileDialog", u"...", None)
        )
        self.cbx_sort_by.setItemText(
            0, QCoreApplication.translate("FileDialog", u"Name", None)
        )
        self.cbx_sort_by.setItemText(
            1, QCoreApplication.translate("FileDialog", u"Last Played", None)
        )

        self.lbl_version.setText(
            QCoreApplication.translate("FileDialog", u"Minecraft Version", None)
        )
        self.lbl_edition.setText(
            QCoreApplication.translate("FileDialog", u"Minecraft Edition", None)
        )
        self.lbl_sort_by.setText(
            QCoreApplication.translate("FileDialog", u"Sort By", None)
        )
        self.cbx_version.setItemText(
            0, QCoreApplication.translate("FileDialog", u"Any", None)
        )

        self.cbx_edition.setItemText(
            0, QCoreApplication.translate("FileDialog", u"Any", None)
        )
        self.cbx_edition.setItemText(
            1, QCoreApplication.translate("FileDialog", u"Bedrock", None)
        )
        self.cbx_edition.setItemText(
            2, QCoreApplication.translate("FileDialog", u"Java", None)
        )

        self.le_search_box.setPlaceholderText(
            QCoreApplication.translate("FileDialog", u"Search", None)
        )
        self.pbtn_browse.setText(
            QCoreApplication.translate("FileDialog", u"Browse...", None)
        )

    # retranslateUi
