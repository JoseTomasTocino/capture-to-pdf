import sys
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox, \
    QPushButton, QCheckBox, QGridLayout
import os
import pyautogui
from PIL import ImageGrab
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1280 1393
REGION_LEFT = (280, 115, 1000, 1280)
REGION_RIGHT = (1280, 115, 1000, 1280)

NEXT_PAGE_LOCATION = (2295, 750)

app = QApplication(sys.argv)


def hide_while_running(f):
    def deco(self, *args, **kwargs):
        self.hide()
        f(self, *args, **kwargs)
        self.show()

    return deco


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.build_ui()
        self.set_ui_values()

    def build_ui(self):
        self.resize(500, 200)
        self.setWindowTitle("Captura de páginas en PDF")

        global_layout = QVBoxLayout(self)

        l = QHBoxLayout()
        global_layout.addLayout(l)

        wdg = QLabel("Ubicación del archivo PDF:", self)
        l.addWidget(wdg)

        self.file_location_txt = QLineEdit(self)
        l.addWidget(self.file_location_txt)

        grp = QGroupBox("Captura manual", self)
        global_layout.addWidget(grp)

        l = QGridLayout(grp)

        self.capture_left_btn = QPushButton("Capturar izquierda", self)
        self.capture_left_btn.clicked.connect(lambda:self.capture(region=REGION_LEFT, advance=self.skip_page_chb.isChecked()))
        l.addWidget(self.capture_left_btn, 0, 0)

        self.capture_right_btn = QPushButton("Capturar derecha", self)
        self.capture_right_btn.clicked.connect(lambda: self.capture(region=REGION_RIGHT, advance=self.skip_page_chb.isChecked()))
        l.addWidget(self.capture_right_btn, 0, 1)

        self.capture_both_btn = QPushButton("Capturar ambas", self)
        self.capture_both_btn.clicked.connect(lambda: self.capture_both(advance=self.skip_page_chb.isChecked()))
        l.addWidget(self.capture_both_btn, 0, 2)

        self.skip_page_chb = QCheckBox("Pasar página automáticamente tras capturar", self)
        l.addWidget(self.skip_page_chb, 1, 0, 1, 3)

        grp = QGroupBox("Captura automática", self)
        global_layout.addWidget(grp)

        l = QGridLayout(grp)

        wdg = QLabel("Número de páginas a capturar:", self)
        l.addWidget(wdg, 0, 0)

        self.auto_capture_count_txt = QLineEdit(self)
        l.addWidget(self.auto_capture_count_txt, 0, 1)

        wdg = QLabel("Milisegundos entre capturas:", self)
        l.addWidget(wdg, 1, 0)

        self.auto_capture_wait_txt = QLineEdit(self)
        l.addWidget(self.auto_capture_wait_txt, 1, 1)

        self.auto_capture_left_chb = QCheckBox("Autocapturar página izquierda", self)
        l.addWidget(self.auto_capture_left_chb, 2, 0, 1, 2)

        self.auto_capture_right_chb = QCheckBox("Autocapturar página derecha", self)
        l.addWidget(self.auto_capture_right_chb, 3, 0, 1, 2)

        self.start_auto_capture_btn = QPushButton("Comenzar autocaptura", self)
        self.start_auto_capture_btn.clicked.connect(lambda:self.auto_capture())
        l.addWidget(self.start_auto_capture_btn, 4, 0, 1, 2)

        global_layout.addStretch(1)

        self.status_lbl = QLabel("", self)
        global_layout.addWidget(self.status_lbl)

    def set_ui_values(self):
        self.file_location_txt.setText(r"C:\Users\Jose\Desktop\PRUEBAS.pdf")
        self.auto_capture_left_chb.setChecked(True)
        self.auto_capture_right_chb.setChecked(True)
        self.auto_capture_count_txt.setText("10")
        self.auto_capture_wait_txt.setText("500")

        self.status_lbl.setText("Estado: a la espera")

    def advance(self):
        logger.info(f"Haciendo click en {NEXT_PAGE_LOCATION}")
        pyautogui.click(*NEXT_PAGE_LOCATION)

    def capture_both(self, advance=False):
        self.capture(REGION_LEFT)
        self.capture(REGION_RIGHT)

        if advance:
            self.advance()

        # current_mouse_x, current_mouse_y = pyautogui.position()

        # logger.info(f"Moviendo el ratón de vuelta a {current_mouse_x}, {current_mouse_y}")
        # pyautogui.move(current_mouse_x, current_mouse_y)

    @hide_while_running
    def capture(self, region=None, advance=False):
        logger.info(f"Capturando region {region}")

        im = ImageGrab.grab()

        if region is not None:
            assert len(region) == 4, 'region argument must be a tuple of four ints'
            region = [int(x) for x in region]
            im = im.crop((region[0], region[1], region[2] + region[0], region[3] + region[1]))

        im.save(self.file_location_txt.text(), append=os.path.isfile(self.file_location_txt.text()), subsampling=1, quality=85)

        if advance:
            self.advance()

    def auto_capture(self):
        capture_count = int(self.auto_capture_count_txt.text())

        for i in range(capture_count):
            logger.info(f"Capturando página {i}")
            self.capture_both(advance=True)

            pyautogui.sleep(int(self.auto_capture_wait_txt.text()) / 1000.0)


def main():
    w = Window()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
