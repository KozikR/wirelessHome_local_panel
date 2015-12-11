__author__ = 'Rafał'
from PySide import QtCore, QtGui
import sys
import signal
from gui import Ui_MainWindow
from bt import *
from blueNode import *
from device import *
from time import time

"""
GUI creat:  pyside-uic MainWindow.ui -o gui.py
"""


class blueCat(QtGui.QMainWindow):
    def __init__(self, app, parent=None):
        super(blueCat, self).__init__(parent)
        print("Ala ma kota")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.bt = Bt()
        self.bt.new_beacon.connect(self.receive_beacon)

        self.blueNode = BlueNode('login', 'password')   # add your login 
        self.blueNode.new_data.connect(self.receive_node)

        self.detected_devices = []
        self.monitored_devices = []

        self.devices_live_time = 10  # after this amount of seconds of inactivity device is lost....
        self.timer_delete_old_devices = QtCore.QTimer()
        QtCore.QObject.connect(self.timer_delete_old_devices, QtCore.SIGNAL('timeout()'), self.delete_old_devices)
        # self.timer_delete_old_devices.start(self.devices_live_time*1000)

        # GUI
        QtCore.QObject.connect(self.ui.pushButton_add, QtCore.SIGNAL('clicked()'), self.button_add)
        QtCore.QObject.connect(self.ui.pushButton_connect, QtCore.SIGNAL('clicked()'), self.button_connect)

        self.ui.lineEdit_name.setText("Beacon1")
        self.ui.lineEdit_location.setText("Reaktor")


    def button_add(self):
        selected = self.ui.list_detected_devices.selectedItems()
        #print(selected)
        #print(len(selected))
        if len(selected) > 0:
            index = self.ui.list_detected_devices.row(selected[0])
            self.detected_devices[index].name = self.ui.lineEdit_name.text()
            self.detected_devices[index].location = self.ui.lineEdit_location.text()
            self.monitored_devices.append(self.detected_devices[index])
            self.ui.list_monitored_devices.addItem(self.detected_devices[index].__str__())
            self.ui.list_detected_devices.takeItem(index)
            del self.detected_devices[index]
            self.blueNode.send_device(self.JSON_create_devices_list())

    def button_connect(self):
        pass

    @QtCore.Slot(object)
    def delete_old_devices(self):
        current_time = time()
        detected_devices_temp = []
        number_of_deleted = 0
        for i in range(0, len(self.detected_devices)):
            if current_time - self.detected_devices[i].time < self.devices_live_time:
                detected_devices_temp.append(self.detected_devices[i])
            else:
                self.ui.list_detected_devices.takeItem(i-number_of_deleted)
                number_of_deleted += 1
        if number_of_deleted > 0:
            self.detected_devices = detected_devices_temp
        # print('Current time: ' + str(current_time) + ' Remove: '  + str(number_of_deleted))

    @QtCore.Slot(object)
    def receive_beacon(self, b):
        if b.UUID[0] == 1:  # Window sensor
            t = WindowDevice(b.UUID, "", "", time(), b.minor, ((b.major & 255)+200)*10, (b.major & 256)/256)
        elif b.UUID[0] == 2:
            t = DoorDevice(b.UUID, "", "", time(), b.minor, ((b.major & 255)+200)*10, (b.major & 256)/256)
        else:
            t = BeaconDevice(b.UUID, "", "", time(), b.minor, b.major, 0)
        # print(t)
        done = False
        for i in range(0, len(self.monitored_devices)):
            if self.monitored_devices[i].compare_UUID(t):
                done = True
                if not self.monitored_devices[i].compare(t):
                    self.monitored_devices[i].update(t)
                    self.ui.list_monitored_devices.item(i).setText(self.monitored_devices[i].__str__())
                    self.blueNode.send_update_device_value({"values": self.monitored_devices[i].json_update_device_value()})
                break
        if not done:
            for i in range(0, len(self.detected_devices)):
                if self.detected_devices[i].compare_UUID(t):
                    done = True
                    if not self.detected_devices[i].compare(t):
                        self.detected_devices[i] = t
                        self.ui.list_detected_devices.item(i).setText(self.detected_devices[i].__str__())
                    break
        if not done:
            self.detected_devices.append(t)
            self.ui.list_detected_devices.addItem(t.__str__())
        self.delete_old_devices()
        #print(self.detected_devices)
        #print(self.monitored_devices)

    @QtCore.Slot(object)
    def receive_node(self, data):
        print(data)

    def sigint_handler(self, *args):
        """
        Stop thread before end
        """
        self.bt.stop()
        self.blueNode.stop()
        QtGui.QApplication.quit()

    def JSON_create_devices_list(self):
        data = {"device_types": []}
        data['device_types'].append(BeaconDevice.json_update_device_type())
        data['device_types'].append(WindowDevice.json_update_device_type())
        data['device_types'].append(DoorDevice.json_update_device_type())
        for device in self.monitored_devices:
            if type(device) is BeaconDevice:
                data['device_types'][0]["devices"].append(device.json_update_devices())
            elif type(device) is WindowDevice:
                data['device_types'][1]["devices"].append(device.json_update_devices())
            elif type(device) is DoorDevice:
                data['device_types'][2]["devices"].append(device.json_update_devices())
        return data


if __name__ == "__main__":
    signal.signal(signal.SIGINT, blueCat.sigint_handler)  # clean end app
    app = QtGui.QApplication(sys.argv)
    mySW = blueCat(app)
    mySW.show()
    sys.exit(app.exec_())
