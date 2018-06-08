# coding=utf-8

"""Simplifies the way images are sent between processes"""

import numpy as np
import multiprocessing as mp
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc
from Misc.GlobalVars import IMG_DISP_UPDATE_MS


class SyncableMPArray(object):
    """Sharable MP Array with Built in Sync Event"""
    def __init__(self, dims):
        self.array = mp.Array('B', int(np.prod(dims)), lock=mp.Lock())
        self.array_dims = dims
        self.sync_event = mp.Event()
        self.sync_event.clear()

    def generate_np_array(self):
        """Create an NP Array referencing self.mp_array"""
        return SyncableNPArray(self)


class SyncableNPArray(np.ndarray):
    """Numpy array that references supplied mp_array"""
    def __new__(cls, mp_array):
        array = np.frombuffer(mp_array.array.get_obj(), dtype='uint8').reshape(mp_array.array_dims).view(cls)
        array.array_dims = mp_array.array_dims
        array.sync_event = mp_array.sync_event
        return array

    def __array_finalize__(self, array):
        self.array_dims = getattr(array, 'array_dims', None)
        self.sync_event = getattr(array, 'sync_event', None)

    def update_img_array(self, data):
        """Sends an image to the mp array"""
        self[:] = data

    @property
    def can_send(self):
        """Report if receiving party is ready for new frame"""
        return not self.sync_event.is_set()

    @property
    def can_recv(self):
        """report if image has been sent by sending party"""
        return self.sync_event.is_set()

    def set_can_send(self):
        """Set ready to receive to True"""
        self.sync_event.clear()

    def set_can_recv(self):
        """set img sent to True"""
        self.sync_event.set()


# Array associated objects
class __WidgetWithArray__(object):
    """Generic Object with attached SyncableMP/NPArray"""
    def __init__(self, mp_array):
        self.mp_array = mp_array
        self.np_array = mp_array.generate_np_array()

    def start_timer(self):
        """Start the timer to refresh object"""
        timer = qc.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(IMG_DISP_UPDATE_MS)

    def update(self):
        """Updates object"""
        if self.np_array.can_recv:
            img = qg.QImage(self.np_array.data, self.np_array.shape[1], self.np_array.shape[0], qg.QImage.Format_RGB888)
            self.setPixmap(qg.QPixmap.fromImage(img))
            self.np_array.set_can_send()


class PixmapWithArray(__WidgetWithArray__, qw.QGraphicsPixmapItem):
    """QPixmap that displays images from supplied mp_array. Must be used in a QGraphicsView; can add additional func"""
    def __init__(self, scene, mp_array):
        qw.QGraphicsPixmapItem.__init__(scene=scene)
        __WidgetWithArray__.__init__(mp_array)
        self.start_timer()


class LabelWithArray(__WidgetWithArray__, qw.QLabel):
    """QLabel displaying images from supplied array. Use as standalone widget"""
    def __init__(self, mp_array, size=None):
        qw.QLabel.__init__()
        __WidgetWithArray__.__init__(mp_array)
        if not size:
            size = mp_array.array_dims[1], mp_array.array_dims[0]
        self.setMinimumSize(*size)
        self.setMaximumSize(*size)
        self.start_timer()
