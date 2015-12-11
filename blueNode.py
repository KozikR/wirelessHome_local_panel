__author__ = 'Rafał'
from PySide import QtCore
from socketIO_client import SocketIO, LoggingNamespace
import json


class BlueNode(QtCore.QThread):
    new_data = QtCore.Signal(object)

    def __init__(self, login, password):
        QtCore.QThread.__init__(self, parent=None)
        self.login = {'email': login, 'password': password}
        self.socketIO = None
        self.running = True
        self.connect_to_server()

    def connect_to_server(self):
        self.socketIO = SocketIO('http://arhiweb.pl', 80, LoggingNamespace)
        self.socketIO.on('auth_error', self.on_auth_error)
        self.socketIO.on('device_error', self.on_device_error)
        self.socketIO.on('device_type_error', self.on_device_type_error)
        self.socketIO.on('attribute_error', self.on_attribute_error)
        self.socketIO.on('attribute_error', self.on_attribute_error)
        self.start()
        login_data = json.dumps(self.login)
        print(login_data)
        self.socketIO.emit('authorization', login_data, self.callbacks_authorization)

    def callbacks_authorization(self, *args):
        print('callbacks_authorization', args)

    def send(self, data):
        self.socketIO.emit('my other event', data)

    def send_device(self, device):
        data = json.dumps(device)
        print(data)
        self.socketIO.emit('update_devices_list', data, self.callbacks_device)

    def callbacks_device(self, *args):
        print('callbacks_device ', args)

    def send_update_device_value(self, data):
        json_data = json.dumps(data)
        print(json_data)
        self.socketIO.emit('update_device_value', json_data, self.callback_update_device_value)

    def callback_update_device_value(self, *args):
        print('callback_update_device_value ', args)

    def send_update_devices_status(self, data):
        self.socketIO.emit('update_devices_status', json.dumps(data), self.callback_update_devices_status)

    def callback_update_devices_status(self, *args):
        print('update_devices_status ', args)

    def on_auth_error(self, *args):
        print('on auth ', args)

    def on_device_error(self, *args):
        print('on device error ', args)

    def on_device_type_error(self, *args):
        print('device_type_error ', args)

    def on_attribute_error(self, *args):
        print('attribute_error ', args)

    def run(self):
        self.socketIO.wait_for_callbacks(seconds=1)

    def stop(self):
        self.running = False