from logging import getLogger
lg = getLogger(__name__)

from math import floor
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from PySide.QtCore import QSettings
from PySide.QtGui import (QComboBox,
                          QFormLayout,
                          QPushButton,
                          QLabel,
                          QListWidget,
                          QTableView,
                          QWidget,
                          )

config = QSettings('phypno', 'scroll_data')


class Bookmarks(QListWidget):
    """

    """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

    def update_overview(self):
        """

        """
        self.display_overview()

    def display_overview(self):
        pass


class Events(QWidget):
    """

    """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.combobox = QComboBox()
        self.table = QTableView()

        layout = QFormLayout()
        layout.addRow('Events: ', self.combobox)
        layout.addRow('List: ', self.table)
        self.setLayout(layout)

    def update_overview(self):
        """

        """
        self.display_overview()

    def display_overview(self):
        pass


class Stages(QWidget):
    """Widget that contains about sleep scoring.

    Attributes
    ----------
    parent : instance of QMainWindow
        the main window.
    scores : instance of xml.etree.ElementTree.Element
        xml structure with information about sleep staging
    filename : str
        path to .xml file
    file_button : instance of QPushButton
        push button to open a new file
    rater : instance of QLabel
        widget wit the name of the rater
    combobox : instance of QComboBox
        widget with the possible sleep stages

    """
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.scores = None
        self.filename = None
        self.file_button = QPushButton('Click to choose file')
        self.file_button.clicked.connect(parent.action_open_stages)
        self.rater = QLabel()
        self.combobox = QComboBox()

        layout = QFormLayout()
        layout.addRow('Filename: ', self.file_button)
        layout.addRow('Rater: ', self.rater)
        layout.addRow('Stage: ', self.combobox)
        self.setLayout(layout)

    def update_overview(self, xml_file):
        """Update information about the sleep scoring.

        Parameters
        ----------
        xml_file : str
            file of the new or existing .xml file

        """
        self.filename = xml_file

        try:
            # read existing file
            raise FileNotFoundError
        except FileNotFoundError:
            self.scores = self.create_empty_xml()

        self.display_overview()

    def display_overview(self):
        """Update the widgets of the sleep scoring."""
        self.file_button.setText(self.filename)

    def create_empty_xml(self):
        """Create a new empty xml file, to keep the sleep scoring.

        It's organized with sleep_stages (and filename of the dataset), rater
        (with the name of the rater), epochs (with id equal to the start_time),
        which have start_time, end_time, and stage.

        """
        minimum = floor(self.parent.overview.minimum)
        maximum = floor(self.parent.overview.maximum)
        window_length = config.value('stage_scoring_window')

        main = Element('sleep_stages')
        main.set('filename', self.parent.info.filename)
        rated = SubElement(main, 'rater')
        rated.set('name', 'TODO')

        for t in range(minimum, maximum, window_length):
            epoch = SubElement(rated, 'epoch')
            epoch.set('id', str(t))  # use start_time as id

            start_time = SubElement(epoch, 'start_time')
            start_time.text = str(t)

            end_time = SubElement(epoch, 'end_time')
            end_time.text = str(t + window_length)

            stage = SubElement(epoch, 'stage')
            stage.text = 'Unknown'

        return main

    def save_xml_to_file(self):
        """Save xml to file."""
        xml = parseString(tostring(self.scores))
        with open(self.filename, 'w+') as f:
            f.write(xml.toprettyxml())