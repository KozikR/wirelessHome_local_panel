from time import time
__author__ = 'Rafał'


class Device:
    def __init__(self, UUID, name, location, time):
        self.UUID = UUID
        self.UUID_string = "".join(str(x) for x in self.UUID)
        self.name = name
        self.location = location
        self.time = time
        self.maxTime = 100

    def __str__(self):
        if self.name == "":
            return "UUID: " + str(self.UUID) + "\n"
        else:
            return self.name + "\t\tUUID: " + str(self.UUID) + "\n"

    def to_JSON(self):
        pass

    def compare(self, device):
        return True

    def compare_UUID(self, device):
        if len(self.UUID) != len(device.UUID):
            return False
        for i in range(0, len(self.UUID)-1):
            if self.UUID[i] != device.UUID[i]:
                return False
        return True

    def update(self, device):
        self.time = device.time

    def json_update_device_status(self):
        status = 1
        if time()-self.time > self.maxTime:
            status = 0
        return {"deviceUuid": self.UUID, 'status': status}

    def json_update_device_value(self):
        pass

    def json_update_devices(self):
        pass

    @staticmethod
    def json_update_device_type():
        return {
                    "settings": {
                        "deviceTypeCode": "device",
                        "deviceTypeName": "Device"
                    },
                    "devices": []
               }


class BeaconDevice(Device):
    def __init__(self, UUID, name, location, time, minor, major, distance):
        Device.__init__(self, UUID, name, location, time)
        self.minor = minor
        self.major = major
        self.distance = distance

    def update(self, device):
        self.time = device.time
        self.minor = device.minor
        self.major = device.major
        self.distance = device.distance

    def compare(self, device):
        if self.minor == device.minor and self.major == device.major and self.distance == device.distance and self.time == device.time:
            return True
        else:
            return False

    def __str__(self):
        if self.name == "":
            return "B UUID:\t" + str(self.UUID) + "\t " + str(self.major) + " " + str(self.minor) + "\n"
        else:
            return self.name + "\t\tUUID: " + str(self.UUID) + "\t " + str(self.major) + " " + str(self.minor) + "\n"

    def json_update_device_value(self):
        return [{"deviceUuid": self.UUID_string, "attributeCode": "minor", "value": self.minor, "createdAt": round(self.time)},
                {"deviceUuid": self.UUID_string, "attributeCode": "major", "value": self.major, "createdAt": round(self.time)},
                {"deviceUuid": self.UUID_string, "attributeCode": "distance", "value": self.distance, "createdAt": round(self.time)},
                ]

    def json_update_devices(self):
        return {
            "settings": {
                          "deviceUuid": self.UUID_string,
                          "deviceName": self.name,
                          "localizationId": 0,
                          "status": "1"
            },
            "attributes": [
                {
                    "settings": {
                      "attributeName": "minor",
                      "attributeCode": "minor",
                      "isConfigurable": "0",
                      "input": "input",
                      "suffixText": "",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                },
                {
                    "settings": {
                      "attributeName": "major",
                      "attributeCode": "major",
                      "isConfigurable": "0",
                      "input": "input",
                      "suffixText": "",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                },
                {
                    "settings": {
                      "attributeName": "distance",
                      "attributeCode": "distance",
                      "isConfigurable": "0",
                      "input": "input",
                      "suffixText": "m",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                }
            ]
        }

    @staticmethod
    def json_update_device_type():
        return {
                    "settings": {
                        "deviceTypeCode": "beacon",
                        "deviceTypeName": "Beacon"
                    },
                    "devices": []
               }


class WindowDevice(Device):
    def __init__(self, UUID, name, location, time, temperature, battery, window):
        Device.__init__(self, UUID, name, location, time)
        self.temperature = temperature
        self.battery = battery
        self.window = window

    def update(self, device):
        self.time = device.time
        self.temperature = device.temperature
        self.battery = device.battery
        self.window = device.window

    def compare(self, device):
        if self.temperature == device.temperature and self.battery == device.battery and self.window == device.window:
            return True
        else:
            return False

    def __str__(self):
        window_state = ""
        if self.window == 1:
            window_state = "otwarte"
        else:
            window_state = "zamknięte"
        if self.name == "":
            return "Okno " + window_state + "\n" #+ "\t Temperatura " + str(self.temperature) + "\t Bateria " + str(self.battery) + "\n"
        else:
            return self.name + "\t\tUUID: " + str(self.UUID) + "\t " + str(self.window) + " " + \
                str(self.temperature) + "C " + str(self.battery) + "\n"

    def json_update_device_value(self):
        return [{"deviceUuid": self.UUID_string, "attributeCode": "window", "value": self.window, "createdAt": round(self.time)},
                {"deviceUuid": self.UUID_string, "attributeCode": "temperature", "value": self.temperature, "createdAt": round(self.time)},
                {"deviceUuid": self.UUID_string, "attributeCode": "battery", "value": self.battery, "createdAt": round(self.time)},
                ]

    def json_update_devices(self):
        return {
            "settings": {
                          "deviceUuid": self.UUID_string,
                          "deviceName": self.name,
                          "localizationId": 0,
                          "status": "1"
            },
            "attributes": [
                {
                    "settings": {
                      "attributeName": "window",
                      "attributeCode": "window",
                      "isConfigurable": "0",
                      "input": "checkbox",
                      "suffixText": "",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                },
                {
                    "settings": {
                      "attributeName": "temperature",
                      "attributeCode": "temperature",
                      "isConfigurable": "0",
                      "input": "input",
                      "suffixText": "C",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                },
                {
                    "settings": {
                      "attributeName": "battery",
                      "attributeCode": "battery",
                      "isConfigurable": "0",
                      "input": "input",
                      "suffixText": "V",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                }
            ]
        }

    @staticmethod
    def json_update_device_type():
        return {
                    "settings": {
                        "deviceTypeCode": "window_sensor",
                        "deviceTypeName": "Window Sensor"
                    },
                    "devices": []
               }


class DoorDevice(Device):
    def __init__(self, UUID, name, location, time, temperature, battery, window):
        Device.__init__(self, UUID, name, location, time)
        self.temperature = temperature
        self.battery = battery
        self.window = window

    def update(self, device):
        self.time = device.time
        self.temperature = device.temperature
        self.battery = device.battery
        self.window = device.window

    def compare(self, device):
        if self.temperature == device.temperature and self.battery == device.battery and self.window == device.window:
            return True
        else:
            return False

    def __str__(self):
        window_state = ""
        if self.window == 1:
            window_state = "zamknięte"
        else:
            window_state = "otwarte"
        if self.name == "":
            return "Drzwi " + window_state + "\n" # + "\t Temperatura " + str(self.temperature) + "\t Bateria " + str(self.battery) + "\n"
        else:
            return self.name + "\t\tUUID: " + str(self.UUID) + "\t " + str(self.window) + " " + \
                str(self.temperature) + "C " + str(self.battery) + "\n"

    def json_update_device_value(self):
        return [{"deviceUuid": self.UUID_string, "attributeCode": "door", "value": 1-self.window, "createdAt": round(self.time)},
                {"deviceUuid": self.UUID_string, "attributeCode": "temperature", "value": self.temperature, "createdAt": round(self.time)},
                {"deviceUuid": self.UUID_string, "attributeCode": "battery", "value": self.battery, "createdAt": round(self.time)},
                ]

    def json_update_devices(self):
        return {
            "settings": {
                          "deviceUuid": self.UUID_string,
                          "deviceName": self.name,
                          "localizationId": 0,
                          "status": "1"
            },
            "attributes": [
                {
                    "settings": {
                      "attributeName": "door",
                      "attributeCode": "door",
                      "isConfigurable": "0",
                      "input": "checkbox",
                      "suffixText": "",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                },
                {
                    "settings": {
                      "attributeName": "temperature",
                      "attributeCode": "temperature",
                      "isConfigurable": "0",
                      "input": "slider",
                      "suffixText": "C",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                },
                {
                    "settings": {
                      "attributeName": "battery",
                      "attributeCode": "battery",
                      "isConfigurable": "0",
                      "input": "input",
                      "suffixText": "V",
                      "options": "",
                      "minRange": "",
                      "maxRange": ""
                    }
                }
            ]
        }

    @staticmethod
    def json_update_device_type():
        return {
                    "settings": {
                        "deviceTypeCode": "door_sensor",
                        "deviceTypeName": "Door Sensor"
                    },
                    "devices": []
               }

