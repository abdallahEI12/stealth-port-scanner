from PySide6.QtWidgets import (
QApplication,QLabel,QLineEdit,QPushButton,QMainWindow,QMenuBar,QStatusBar,
QVBoxLayout,QHBoxLayout,QGridLayout,QCheckBox,QWidget,QDialog
)
from PySide6.QtCore import Qt,QSize
from helpers import Color,Label

from PortScanner import Packet

import binascii

def check_if_open(port, response):
    if response == None:
        print("Port " + str(port) + " is: closed")
        return False
    cont = binascii.hexlify(response)
    if cont[65:68] == b"012":
        return True
    else:
        return False

class scan_dialog(QDialog):
    def __init__(self,sndr_ip,rcvr_ip,Port,From,To):
        super().__init__()
        self.setWindowTitle("scanning...")
        self.setMinimumSize(QSize(400,400))

        dialog_layout = QVBoxLayout()
        self.sndr_ip = sndr_ip
        self.rcvr_ip = rcvr_ip
        self.prt = Port
        self.From = From
        self.To = To
        self.results_lbl = QLabel()

        if self.prt != None:
            packet = Packet(sndr_ip,rcvr_ip,int(self.prt))
            packet.generate_packet()
            result = packet.send_packet()
            if check_if_open(self.prt, result):
                self.results_lbl.setText(f"port: {self.prt} is open.")
            else:
                self.results_lbl.setText(f"port: {self.prt} is closed.")
        else:
            for port in range(int(self.From),int(self.To)):
                packet = Packet(sndr_ip,rcvr_ip,port)
                packet.generate_packet()
                result = packet.send_packet()
                if check_if_open(port,result):
                    self.results_lbl.setText(
                        f"{self.results_lbl.text()}port:{port} is open\n"
                    )
                else:
                    self.results_lbl.setText(
                        f"{self.results_lbl.text()}port:{port} is closed\n"
                    )

        dialog_layout.addWidget(self.results_lbl)
        self.setLayout(dialog_layout)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # put main window settings
        self.setWindowTitle("port scanner")
        self.setMinimumSize(QSize(400,400))

        # make the layout of the program
        main_layout  = QVBoxLayout()

        self.sndr_ip_lbl = Label("sender ip")
        self.sndr_ip = QLineEdit()
        self.sndr_ip.setPlaceholderText("sender ip addresss")
        self.rcvr_ip_lbl = Label("target IP")
        self.rcvr_ip = QLineEdit()
        self.rcvr_ip.setPlaceholderText("target IP Address")

        #make check box for single port scanning
        self.sngl_port_lbl = Label("Port")
        self.sngl_port = QLineEdit()
        self.sngl_port.setPlaceholderText("Ex. 80")

        #make check box for ranged port scanning
        self.rng_prt_lbl = Label("scan range of ports")
        rng_prt_layout = QHBoxLayout()
        self.rng_prt_chbx = QCheckBox()
        self.rng_prt_chbx.setCheckState(Qt.CheckState.Unchecked)
        self.rng_prt_chbx.stateChanged.connect(self.toggle_range_port_scanning)
        self.rng_prt_from = QLineEdit()
        self.rng_prt_from.setPlaceholderText("from")
        self.rng_prt_from.setDisabled(True)
        self.rng_prt_to = QLineEdit()
        self.rng_prt_to.setPlaceholderText("to")
        self.rng_prt_to.setDisabled(True)
        rng_prt_layout.addWidget(self.rng_prt_chbx)
        rng_prt_layout.addWidget(self.rng_prt_from)
        rng_prt_layout.addWidget(self.rng_prt_to)

        #button to start scanning
        self.scan_btn = QPushButton("press to start scanning")
        self.scan_btn.clicked.connect(self.start_scanning)


        #add widget to the main layout
        main_layout.addWidget(self.sndr_ip_lbl)
        main_layout.addWidget(self.sndr_ip)
        main_layout.addWidget(self.rcvr_ip_lbl)
        main_layout.addWidget(self.rcvr_ip)
        main_layout.addWidget(self.sngl_port_lbl)
        main_layout.addWidget(self.sngl_port)
        main_layout.addWidget(self.rng_prt_lbl)
        main_layout.addLayout(rng_prt_layout)
        main_layout.addWidget(self.scan_btn)

        #add the main layout to a container
        main_container = QWidget()
        main_container.setLayout(main_layout)

        self.setCentralWidget(main_container)

    def toggle_range_port_scanning(self):
        if self.rng_prt_chbx.isChecked():
            self.rng_prt_from.setDisabled(False)
            self.rng_prt_to.setDisabled(False)
            self.sngl_port.setDisabled(True)
        else:
            self.rng_prt_from.setDisabled(True)
            self.rng_prt_to.setDisabled(True)
            self.sngl_port.setDisabled(False)

    def start_scanning(self):
        sndr_ip = self.sndr_ip.text()
        rcvr_ip = self.rcvr_ip.text()
        if self.sngl_port.isEnabled():
            port = self.sngl_port.text()
        else:
            port = None
        if self.rng_prt_to.isEnabled():
            rng_to = self.rng_prt_to.text()
            rng_from = self.rng_prt_from.text()
        else:
            rng_to = None
            rng_from = None

        scan_dlg = scan_dialog(sndr_ip,rcvr_ip,port,rng_from,rng_to)
        scan_dlg.exec()

if "__main__" in __name__:
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

