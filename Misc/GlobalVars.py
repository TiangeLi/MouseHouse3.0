# coding=utf-8

"""Common Variables/Names used across modules"""

import os
import struct
from PyCapture2 import FRAMERATE
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
import multiprocessing as mp

# -- USER EDITABLE VALUES -- #
CAMERA_FRAMERATE = 30  # num frames / second - valid values: 7.5, 15, 30, 60
IMG_DISP_UPDATE_MS = 5  # num ms between each image display update


# -- DO NOT MESS WITH THE FOLLOWING -- #
# Forbidden Chars that cannot be used in file naming
FORBIDDEN_CHARS = ['<', '>', '*', '|', '?', '"', '/', ':', '\\']

# Camera Framerate
PYCAP_FRAMERATE = getattr(FRAMERATE, 'FR_{}'.format(CAMERA_FRAMERATE))
CAMERA_ABS_FRAMERATE_INT = struct.unpack('<I', struct.pack('<f', CAMERA_FRAMERATE))[0]
# Hardware Registers
# -- Writing Registers
CMR_REG_BRIGHTNESS = int(0x800)
CMR_REG_EXPOSURE = int(0x804)
CMR_REG_SHUTTER = int(0x81C)
CMR_REG_GAIN = int(0x820)
CMR_REG_FRAMERATE = int(0x83C)
CMR_REG_FRAMERATE_ABS = int(0x968)  # This is an Absolute Value Register! works differently from above regs
# -- Convert Writing Register to Reading Register
CMR_REG_READ_VALS = int(0x300)
# -- Commonly used values
CMR_SET_REG_MANUAL_LOW = int(0x82000000)  # Value that sets a register to Manual Control + LOW value
CMR_SET_REG_ABS_MANUAL = int(0xC2000000)  # Sets register to accept Absolute Value control; manual control
CMR_MAX_VALUE_MASK = int(0b111111111111)  # Mask that we apply to obtain last 12 digits from a binary num
# Camera Properties
CAMERA = 'camera'
VID_DIM = (480, 640)  # Rows, Cols
VID_DIM_RGB = (*VID_DIM, 3)  # Rows, Cols, RGB
DISP_DIM = VID_DIM[0]//2, VID_DIM[1]//2

# Concurrency
MASTER_DUMP_QUEUE = mp.Queue()
PROC_HANDLER_QUEUE = mp.Queue()
EXP_START_EVENT = mp.Event()
# Process Names
PROC_CMR = 'proc_cmr'
PROC_CMR_VIDREC = 'proc_cmr_vidrec'
PROC_GUI = 'proc_gui'
# Queue Commands
CMD_START = 'cmd_start'
CMD_STOP = 'cmd_stop'
CMD_EXIT = 'cmd_exit'
# Queue Messages
MSG_RECEIVED = 'msg_received'
MSG_STARTED = 'msg_started'
MSG_FINISHED = 'msg_finished'
MSG_VIDREC_SAVING = 'msg_vidrec_saving'
MSG_VIDREC_FINISHED = 'msg_vidrec_finished'

# Directories and Saving
HOME_DIR = os.path.expanduser('~')

# Var names for Misc.CustomFunctions
DAY = 'day'
TIME = 'time'
HOUR = 'Hour'
MINS = 'Mins'
SECS = 'Secs'

# PyQt4
# Colors
qBlack = qg.QColor(0, 0, 0)
qWhite = qg.QColor(255, 255, 255)
qYellow = qg.QColor(255, 255, 0)
qBlue = qg.QColor(0, 0, 255)
qRed = qg.QColor(255, 0, 0)
qClear = qg.QColor(255, 255, 255, 0)
qSemi = qg.QColor(255, 255, 255, 128)
# Background Colors
qBgRed = 'background-color: rgb(255, 0, 0)'
qBgWhite = 'background-color: rgb(255, 255, 255)'
qBgCyan = 'background-color: cyan'
qBgOrange = 'background-color: orange'
# Selectable
qSelectable = qw.QGraphicsItem.ItemIsSelectable
# Layout
qAlignCenter = qc.Qt.AlignCenter
qAlignLeft = qc.Qt.AlignLeft
qAlignRight = qc.Qt.AlignRight
qStyleSunken = qw.QFrame.Sunken
qStylePanel = qw.QFrame.StyledPanel
# Keypresses
qKey_k = qc.Qt.Key_K
qKey_del = qc.Qt.Key_Delete
qKey_backspace = qc.Qt.Key_Backspace
# Key Modifiers
qMod_shift = qc.Qt.ShiftModifier
qMod_cntrl = qc.Qt.ControlModifier
qMod_alt = qc.Qt.AltModifier
