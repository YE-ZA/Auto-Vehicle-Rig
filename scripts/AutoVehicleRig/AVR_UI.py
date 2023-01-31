# -*- coding: UTF-8 -*-
import AutoVehicleRig.AVR_Base as avr
import maya.cmds as cmds
import maya.OpenMaya as om
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtCore, QtGui
import re


MAIN_QSS = '''QLabel{
                font-style: oblique;
                font-weight: bold;
                background: #222222
              }'''
NOTE_QSS = '''QLabel{
                color: #000000;
                font-style: oblique;
                font-weight: bold;
                font-size: 13px;
                background: #FF8000;
                padding: 10px 20px 10px 20px;
                margin-bottom: 6px
              }'''


class AVR(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    def __init__(self):
        super(AVR, self).__init__()

        # Delete existing UI
        try:
            cmds.deleteUI('AVRWorkspaceControl')
        except RuntimeError:
            pass

        self.setWindowTitle('Auto Vehicle Rig')
        self.resize(429, 702)
        self.build_ui()
        self.setObjectName('AVR')
        self.show(dockable=True)

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Create notice of vehicle orientation
        note = QtWidgets.QLabel(self)
        layout.addWidget(note)
        note.setAlignment(QtCore.Qt.AlignCenter)
        note.setWordWrap(True)  # Allow text to automatically wrap
        note.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)  # Allow Scaling freely
        note.setText('NOTICE : Make sure the vehicle is facing the positive X axis')
        note.setStyleSheet(NOTE_QSS)

        # Group and clean up models, then rename groups
        step1 = QtWidgets.QLabel(self)
        layout.addWidget(step1)
        step1.setAlignment(QtCore.Qt.AlignCenter)
        step1.setFixedHeight(30)
        step1.setText('Step1 : Model Optimization')
        step1.setStyleSheet(MAIN_QSS)
        step1.setToolTip('Group and clean up models, and rename each group with a custom name')

        # Set pivot policy
        pivot_widget = QtWidgets.QWidget(self)
        pivot_layout = QtWidgets.QFormLayout(pivot_widget)
        layout.addWidget(pivot_widget)

        pivot_text = QtWidgets.QLabel("Center VehicleBody's pivot to : ", self)
        self.pivot_cb = QtWidgets.QComboBox(self)
        self.pivot_cb.addItem('World')
        self.pivot_cb.addItem('Object')
        pivot_layout.addRow(pivot_text, self.pivot_cb)

        item_2w = ['VehicleBody', 'Wheel_F', 'Wheel_B']
        item_4w = ['VehicleBody', 'Wheel_FL', 'Wheel_FR', 'Wheel_BL', 'Wheel_BR']
        item_6w = ['VehicleBody', 'Wheel_FL', 'Wheel_FR', 'Wheel_ML', 'Wheel_MR', 'Wheel_BL', 'Wheel_BR']

        # 2W setup
        step1_widget_2w = QtWidgets.QWidget(self)
        step1_layout_2w = QtWidgets.QFormLayout(step1_widget_2w)
        layout.addWidget(step1_widget_2w)

        for item in item_2w:
            exec('self.{}_text_2 = QtWidgets.QLineEdit(item, self)'.format(item))
            exec('{}_rename_btn_2 = QtWidgets.QPushButton("Rename {}", self)'.format(item, item))
            step1_layout_2w.addRow(locals()['{}_rename_btn_2'.format(item)], eval('self.{}_text_2'.format(item)))
            eval('self.{}_text_2'.format(item)).setFixedHeight(23)
            locals()['{}_rename_btn_2'.format(item)].setFixedWidth(130)
            exec('{}_rename_btn_2.clicked.connect(self.rename_group_{}_2)'.format(item, item))

        # 4W setup
        step1_widget_4w = QtWidgets.QWidget(self)
        step1_layout_4w = QtWidgets.QFormLayout(step1_widget_4w)
        layout.addWidget(step1_widget_4w)

        # Use exec(), eval(), and locals() to dynamically generate variables
        for item in item_4w:
            exec('self.{}_text_4 = QtWidgets.QLineEdit(item, self)'.format(item))
            exec('{}_rename_btn_4 = QtWidgets.QPushButton("Rename {}", self)'.format(item, item))
            step1_layout_4w.addRow(locals()['{}_rename_btn_4'.format(item)], eval('self.{}_text_4'.format(item)))
            eval('self.{}_text_4'.format(item)).setFixedHeight(23)
            locals()['{}_rename_btn_4'.format(item)].setFixedWidth(130)
            exec('{}_rename_btn_4.clicked.connect(self.rename_group_{}_4)'.format(item, item))

        # 6W setup
        step1_widget_6w = QtWidgets.QWidget(self)
        step1_layout_6w = QtWidgets.QFormLayout(step1_widget_6w)
        layout.addWidget(step1_widget_6w)

        for item in item_6w:
            exec('self.{}_text_6 = QtWidgets.QLineEdit(item, self)'.format(item))
            exec('{}_rename_btn_6 = QtWidgets.QPushButton("Rename {}", self)'.format(item, item))
            step1_layout_6w.addRow(locals()['{}_rename_btn_6'.format(item)], eval('self.{}_text_6'.format(item)))
            eval('self.{}_text_6'.format(item)).setFixedHeight(23)
            locals()['{}_rename_btn_6'.format(item)].setFixedWidth(130)
            exec('{}_rename_btn_6.clicked.connect(self.rename_group_{}_6)'.format(item, item))

        # Put 2W, 4W, 6W in different tabs
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)
        self.tab_widget.addTab(step1_widget_2w, '2-Wheeled')
        self.tab_widget.addTab(step1_widget_4w, '4-Wheeled')
        self.tab_widget.addTab(step1_widget_6w, '6-Wheeled')
        self.tab_widget.setCurrentIndex(1)  # Set '4-Wheeled' tab as default tab

        # Skeleton setup module
        step2 = QtWidgets.QLabel(self)
        layout.addWidget(step2)
        step2.setAlignment(QtCore.Qt.AlignCenter)
        step2.setFixedHeight(30)
        step2.setText('Step2 : Skeleton Setup')
        step2.setStyleSheet(MAIN_QSS)
        step2.setToolTip('Create joints with correct orientation and rename them with custom prefix or suffix')

        # Add prefix or suffix
        rename_widget = QtWidgets.QWidget(self)
        rename_layout = QtWidgets.QHBoxLayout(rename_widget)
        layout.addWidget(rename_widget)
        prefix = QtWidgets.QLabel('Prefix:', self)
        suffix = QtWidgets.QLabel('Suffix:', self)
        self.pre_text = QtWidgets.QLineEdit(self)
        self.suf_text = QtWidgets.QLineEdit('_Jnt', self)
        rename_layout.addWidget(prefix)
        rename_layout.addWidget(self.pre_text)
        rename_layout.addWidget(suffix)
        rename_layout.addWidget(self.suf_text)

        # Add a horizontal line
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        layout.addWidget(line)

        # Create joints
        step2_widget = QtWidgets.QWidget(self)
        step2_layout = QtWidgets.QHBoxLayout(step2_widget)
        layout.addWidget(step2_widget)
        create_btn = QtWidgets.QPushButton('Create Joint', self)
        create_btn.clicked.connect(self.create_joints)
        snap_btn = QtWidgets.QPushButton('Snap Joint', self)
        snap_btn.clicked.connect(avr.snap_joint)
        step2_layout.addWidget(create_btn)
        step2_layout.addWidget(snap_btn)

        # Bind Skin
        step3 = QtWidgets.QLabel(self)
        layout.addWidget(step3)
        step3.setAlignment(QtCore.Qt.AlignCenter)
        step3.setFixedHeight(30)
        step3.setText('Step3 : Skinning')
        step3.setStyleSheet(MAIN_QSS)
        step3.setToolTip('One click to bind all skins and create controllers')

        step3_widget = QtWidgets.QWidget(self)
        step3_layout = QtWidgets.QVBoxLayout(step3_widget)
        layout.addWidget(step3_widget)
        bind_btn = QtWidgets.QPushButton('Bind All Skins', self)
        bind_btn.clicked.connect(self.bind_skin)
        step3_layout.addWidget(bind_btn)

        controller_btn = QtWidgets.QPushButton('Create Controllers', self)
        controller_btn.clicked.connect(self.create_controllers)
        step3_layout.addWidget(controller_btn)

        # Add spacer to implement adaptive scaling at the bottom
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        layout.addItem(spacer)

        author = QtWidgets.QLabel('© 2021 YE-ZA', self)
        layout.addWidget(author)
        author.setAlignment(QtCore.Qt.AlignCenter)

    def rename_group_VehicleBody_2(self):
        cmds.undoInfo(openChunk=True)

        vb_name = self.VehicleBody_text_2.text()
        if self.pivot_cb.currentIndex() == 0:
            avr.rename_group_model_world(vb_name)
        elif self.pivot_cb.currentIndex() == 1:
            avr.rename_group_model_object(vb_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_VehicleBody_4(self):
        cmds.undoInfo(openChunk=True)

        vb_name = self.VehicleBody_text_4.text()
        if self.pivot_cb.currentIndex() == 0:
            avr.rename_group_model_world(vb_name)
        elif self.pivot_cb.currentIndex() == 1:
            avr.rename_group_model_object(vb_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_VehicleBody_6(self):
        cmds.undoInfo(openChunk=True)

        vb_name = self.VehicleBody_text_6.text()
        if self.pivot_cb.currentIndex() == 0:
            avr.rename_group_model_world(vb_name)
        elif self.pivot_cb.currentIndex() == 1:
            avr.rename_group_model_object(vb_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_F_2(self):
        cmds.undoInfo(openChunk=True)

        wf_name = self.Wheel_F_text_2.text()
        avr.rename_group_model_object(wf_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_B_2(self):
        cmds.undoInfo(openChunk=True)

        wb_name = self.Wheel_B_text_2.text()
        avr.rename_group_model_object(wb_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_FL_4(self):
        cmds.undoInfo(openChunk=True)

        wfl_name = self.Wheel_FL_text_4.text()
        avr.rename_group_model_object(wfl_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_FL_6(self):
        cmds.undoInfo(openChunk=True)

        wfl_name = self.Wheel_FL_text_6.text()
        avr.rename_group_model_object(wfl_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_FR_4(self):
        cmds.undoInfo(openChunk=True)

        wfr_name = self.Wheel_FR_text_4.text()
        avr.rename_group_model_object(wfr_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_FR_6(self):
        cmds.undoInfo(openChunk=True)

        wfr_name = self.Wheel_FR_text_6.text()
        avr.rename_group_model_object(wfr_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_ML_6(self):
        cmds.undoInfo(openChunk=True)

        wml_name = self.Wheel_ML_text_6.text()
        avr.rename_group_model_object(wml_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_MR_6(self):
        cmds.undoInfo(openChunk=True)

        wmr_name = self.Wheel_MR_text_6.text()
        avr.rename_group_model_object(wmr_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_BL_4(self):
        cmds.undoInfo(openChunk=True)

        wbl_name = self.Wheel_BL_text_4.text()
        avr.rename_group_model_object(wbl_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_BL_6(self):
        cmds.undoInfo(openChunk=True)

        wbl_name = self.Wheel_BL_text_6.text()
        avr.rename_group_model_object(wbl_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_BR_4(self):
        cmds.undoInfo(openChunk=True)

        wbr_name = self.Wheel_BR_text_4.text()
        avr.rename_group_model_object(wbr_name)

        cmds.undoInfo(closeChunk=True)

    def rename_group_Wheel_BR_6(self):
        cmds.undoInfo(openChunk=True)

        wbr_name = self.Wheel_BR_text_6.text()
        avr.rename_group_model_object(wbr_name)

        cmds.undoInfo(closeChunk=True)

    def create_joints(self):
        cmds.undoInfo(openChunk=True)

        prefix = self.pre_text.text()
        suffix = self.suf_text.text()
        if not prefix and not suffix:
            om.MGlobal.displayWarning('Please enter a prefix or a suffix!')
            return

        rule = re.compile(r'^[a-zA-Z_].*$')

        if prefix and not rule.match(prefix):
            om.MGlobal.displayWarning("Prefix name should start with 'a-z', 'A-Z', or'_'")
            return

        if self.tab_widget.currentIndex() == 0:
            vb_name = self.VehicleBody_text_2.text()
            wf_name = self.Wheel_F_text_2.text()
            wb_name = self.Wheel_B_text_2.text()
            avr.create_joints_2w(vb_name, wf_name, wb_name, prefix, suffix)
        elif self.tab_widget.currentIndex() == 1:
            vb_name = self.VehicleBody_text_4.text()
            wfl_name = self.Wheel_FL_text_4.text()
            wfr_name = self.Wheel_FR_text_4.text()
            wbl_name = self.Wheel_BL_text_4.text()
            wbr_name = self.Wheel_BR_text_4.text()
            avr.create_joints_4w(vb_name, wfl_name, wfr_name, wbl_name, wbr_name, prefix, suffix)
        elif self.tab_widget.currentIndex() == 2:
            vb_name = self.VehicleBody_text_6.text()
            wfl_name = self.Wheel_FL_text_6.text()
            wfr_name = self.Wheel_FR_text_6.text()
            wml_name = self.Wheel_ML_text_6.text()
            wmr_name = self.Wheel_MR_text_6.text()
            wbl_name = self.Wheel_BL_text_6.text()
            wbr_name = self.Wheel_BR_text_6.text()
            avr.create_joints_6w(vb_name, wfl_name, wfr_name, wml_name, wmr_name, wbl_name, wbr_name, prefix, suffix)

        cmds.undoInfo(closeChunk=True)

    def bind_skin(self):
        cmds.undoInfo(openChunk=True)

        try:
            prefix = self.pre_text.text()
            suffix = self.suf_text.text()
            if self.tab_widget.currentIndex() == 0:
                vb_name = self.VehicleBody_text_2.text()
                wf_name = self.Wheel_F_text_2.text()
                wb_name = self.Wheel_B_text_2.text()
                avr.bind_skin_2w(vb_name, wf_name, wb_name, prefix, suffix)
            elif self.tab_widget.currentIndex() == 1:
                vb_name = self.VehicleBody_text_4.text()
                wfl_name = self.Wheel_FL_text_4.text()
                wfr_name = self.Wheel_FR_text_4.text()
                wbl_name = self.Wheel_BL_text_4.text()
                wbr_name = self.Wheel_BR_text_4.text()
                avr.bind_skin_4w(vb_name, wfl_name, wfr_name, wbl_name, wbr_name, prefix, suffix)
            elif self.tab_widget.currentIndex() == 2:
                vb_name = self.VehicleBody_text_6.text()
                wfl_name = self.Wheel_FL_text_6.text()
                wfr_name = self.Wheel_FR_text_6.text()
                wml_name = self.Wheel_ML_text_6.text()
                wmr_name = self.Wheel_MR_text_6.text()
                wbl_name = self.Wheel_BL_text_6.text()
                wbr_name = self.Wheel_BR_text_6.text()
                avr.bind_skin_6w(vb_name, wfl_name, wfr_name, wml_name, wmr_name, wbl_name, wbr_name, prefix, suffix)
        except ValueError:
            om.MGlobal.displayWarning('Please make sure that each part of the model and joints are named correctly!')
            return
        except RuntimeError:
            om.MGlobal.displayWarning('Unknown RuntimeError: Please check the scene or bind the skin manually!')
            return

        cmds.undoInfo(closeChunk=True)

    def create_controllers(self):
        cmds.undoInfo(openChunk=True)

        prefix = self.pre_text.text()
        suffix = self.suf_text.text()
        if self.tab_widget.currentIndex() == 0:
            vb_name = self.VehicleBody_text_2.text()
            wf_name = self.Wheel_F_text_2.text()
            wb_name = self.Wheel_B_text_2.text()
            avr.create_controllers_2w(vb_name, wf_name, wb_name, prefix, suffix)
        elif self.tab_widget.currentIndex() == 1:
            vb_name = self.VehicleBody_text_4.text()
            wfl_name = self.Wheel_FL_text_4.text()
            wfr_name = self.Wheel_FR_text_4.text()
            wbl_name = self.Wheel_BL_text_4.text()
            wbr_name = self.Wheel_BR_text_4.text()
            avr.create_controllers_4w(vb_name, wfl_name, wfr_name, wbl_name, wbr_name, prefix, suffix)
        elif self.tab_widget.currentIndex() == 2:
            vb_name = self.VehicleBody_text_6.text()
            wfl_name = self.Wheel_FL_text_6.text()
            wfr_name = self.Wheel_FR_text_6.text()
            wml_name = self.Wheel_ML_text_6.text()
            wmr_name = self.Wheel_MR_text_6.text()
            wbl_name = self.Wheel_BL_text_6.text()
            wbr_name = self.Wheel_BR_text_6.text()
            avr.create_controllers_6w(vb_name, wfl_name, wfr_name, wml_name, wmr_name, wbl_name, wbr_name, prefix, suffix)

        cmds.undoInfo(closeChunk=True)


ui = AVR()
