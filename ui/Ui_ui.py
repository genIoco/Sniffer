# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QGridLayout, QHBoxLayout, QHeaderView, QLayout,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSplitter, QTableWidget, QTableWidgetItem,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1148, 751)
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 1131, 701))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ifaces = QComboBox(self.layoutWidget)
        self.ifaces.setObjectName(u"ifaces")
        self.ifaces.setFrame(False)

        self.horizontalLayout_2.addWidget(self.ifaces)

        self.start = QPushButton(self.layoutWidget)
        self.start.setObjectName(u"start")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy)
        self.start.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.start)

        self.stop = QPushButton(self.layoutWidget)
        self.stop.setObjectName(u"stop")
        self.stop.setEnabled(False)
        sizePolicy.setHeightForWidth(self.stop.sizePolicy().hasHeightForWidth())
        self.stop.setSizePolicy(sizePolicy)
        self.stop.setCheckable(True)

        self.horizontalLayout_2.addWidget(self.stop)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.filter = QLineEdit(self.layoutWidget)
        self.filter.setObjectName(u"filter")
        self.filter.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.filter, 1, 0, 1, 1)

        self.splitter_2 = QSplitter(self.layoutWidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.info = QTableWidget(self.splitter_2)
        if (self.info.columnCount() < 5):
            self.info.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.info.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.info.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.info.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.info.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.info.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.info.setObjectName(u"info")
        self.info.setFont(font)
        self.info.setFocusPolicy(Qt.ClickFocus)
        self.info.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.info.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.info.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.info.setDragDropOverwriteMode(False)
        self.info.setAlternatingRowColors(True)
        self.info.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.info.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.info.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.info.setSortingEnabled(False)
        self.splitter_2.addWidget(self.info)
        self.info.horizontalHeader().setCascadingSectionResizes(True)
        self.info.horizontalHeader().setStretchLastSection(True)
        self.info.verticalHeader().setVisible(True)
        self.info.verticalHeader().setCascadingSectionResizes(True)
        self.info.verticalHeader().setProperty("showSortIndicator", True)
        self.info.verticalHeader().setStretchLastSection(False)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.detail = QTreeWidget(self.splitter)
        self.detail.setObjectName(u"detail")
        self.detail.setTextElideMode(Qt.ElideRight)
        self.splitter.addWidget(self.detail)
        self.detail.header().setVisible(False)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.horizontalLayout = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.nums = QTextEdit(self.layoutWidget1)
        self.nums.setObjectName(u"nums")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.nums.sizePolicy().hasHeightForWidth())
        self.nums.setSizePolicy(sizePolicy1)
        self.nums.setMinimumSize(QSize(43, 0))
        self.nums.setMaximumSize(QSize(43, 16777215))
        self.nums.setStyleSheet(u"background-color: rgb(232, 232, 232);")
        self.nums.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nums.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.horizontalLayout.addWidget(self.nums)

        self.raw = QTextEdit(self.layoutWidget1)
        self.raw.setObjectName(u"raw")
        sizePolicy1.setHeightForWidth(self.raw.sizePolicy().hasHeightForWidth())
        self.raw.setSizePolicy(sizePolicy1)
        self.raw.setMinimumSize(QSize(400, 0))
        self.raw.setMaximumSize(QSize(400, 16777215))
        self.raw.setSizeIncrement(QSize(20, 0))
        self.raw.setBaseSize(QSize(0, 0))
        self.raw.setAcceptDrops(False)
        self.raw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.raw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.raw.setReadOnly(True)
        self.raw.setAcceptRichText(False)

        self.horizontalLayout.addWidget(self.raw)

        self.string = QTextEdit(self.layoutWidget1)
        self.string.setObjectName(u"string")
        sizePolicy1.setHeightForWidth(self.string.sizePolicy().hasHeightForWidth())
        self.string.setSizePolicy(sizePolicy1)
        self.string.setMinimumSize(QSize(162, 0))
        self.string.setMaximumSize(QSize(162, 16777215))
        self.string.setSizeIncrement(QSize(20, 0))
        self.string.setBaseSize(QSize(0, 0))
        self.string.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.string.setLineWrapMode(QTextEdit.WidgetWidth)
        self.string.setLineWrapColumnOrWidth(0)
        self.string.setReadOnly(True)

        self.horizontalLayout.addWidget(self.string)

        self.splitter.addWidget(self.layoutWidget1)
        self.splitter_2.addWidget(self.splitter)

        self.gridLayout.addWidget(self.splitter_2, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1148, 24))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.start.clicked.connect(MainWindow.StartInface)
        self.stop.clicked.connect(MainWindow.StopInface)
        self.info.itemClicked.connect(MainWindow.Showdetail)
        self.filter.returnPressed.connect(MainWindow.SetFilter)
        self.string.textChanged.connect(MainWindow.UpdateLineNums)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        ___qtablewidgetitem = self.info.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Source", None));
        ___qtablewidgetitem1 = self.info.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Destination", None));
        ___qtablewidgetitem2 = self.info.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Protocol", None));
        ___qtablewidgetitem3 = self.info.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Length", None));
        ___qtablewidgetitem4 = self.info.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"info", None));
        ___qtreewidgetitem = self.detail.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"detail", None));
    # retranslateUi

