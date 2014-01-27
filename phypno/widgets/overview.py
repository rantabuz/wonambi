from logging import getLogger
lg = getLogger(__name__)

from PySide.QtCore import Qt, QSettings, Slot
from PySide.QtGui import (QBrush,
                          QPen,
                          QGraphicsLineItem,
                          QGraphicsRectItem,
                          QGraphicsScene,
                          QGraphicsView,
                          )

config = QSettings('phypno', 'scroll_data')


# bookmark
# event
# state
# available
current_line_height = 10

bars = {'bookmark': {'pos0': 15, 'pos1': 10, 'tip': 'Bookmarks'},
        'event': {'pos0': 30, 'pos1': 10, 'tip': 'Events'},
        'state': {'pos0': 45, 'pos1': 50, 'tip': 'Brain State'},
        'available': {'pos0': 100, 'pos1': 10, 'tip': 'Available Recordings'},
        }
total_height = 115


class Overview(QGraphicsView):
    """Show an overview of data, such as hypnogram and data in memory.

    Attributes
    ----------
    window_start : int or float
        start time of the window being plotted (in s).
    window_length : int or float
        length of the window being plotted (in s).
    maximum : int or float
        maximum length of the window (in s).
    scene : instance of QGraphicsScene
        to keep track of the objects.
    item : dict
        all the items, to keep track of

    Notes
    -----
    TODO: maybe use minimum more often, don't assume it's zero

    """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.window_start = config.value('window_start')
        self.window_length = config.value('window_page_length')
        self.minimum = 0
        self.maximum = None
        self.scene = None
        self.item = {}
        self.scale(1 / config.value('ratio_second_overview'), 1)

    def update_overview(self):
        """Read full duration and update maximum.

        Notes
        -----
        TODO: change unit of maximum.

        """
        header = self.parent.info.dataset.header
        maximum = header['n_samples'] / header['s_freq']  # in s
        self.maximum = maximum
        self.display_overview()

    def display_overview(self):
        self.scene = QGraphicsScene(0, 0,
                                    self.maximum,
                                    total_height)
        self.setScene(self.scene)

        self.item['current'] = QGraphicsLineItem(self.window_start, 0,
                                                 self.window_start,
                                                 current_line_height)
        self.item['current'].setPen(QPen(Qt.red))
        self.scene.addItem(self.item['current'])

        for name, pos in bars.items():
            self.item[name] = QGraphicsRectItem(0, pos['pos0'],
                                                self.maximum, pos['pos1'])
            self.item[name].setToolTip(pos['tip'])
            self.scene.addItem(self.item[name])

    def update_position(self, new_position=None):
        """If value changes, call scroll functions."""
        if new_position is not None:
            self.window_start = new_position
            self.item['current'].setPos(self.window_start, 0)
        else:
            pass
            # self.window_start = self.scrollbar.value()
        self.parent.scroll.update_scroll()
        self.parent.scroll.display_scroll()

    @Slot(float, float)
    def more_download(self, start_value, end_value):
        """Set the value of the progress bar.

        Parameters
        ----------

        """
        avail = self.scene.addRect(start_value,
                                   bars['available']['pos0'],
                                   end_value,
                                   bars['available']['pos1'])
        avail.stackBefore(self.item['available'])
        avail.setPen(Qt.NoPen)
        avail.setBrush(QBrush(Qt.green))