import subprocess
from PySide import QtCore


class Beacon:
    def __init__(self, MAC, UUID, major, minor, power):
        self.MAC = MAC
        self.UUID = UUID
        self.minor = minor
        self.major = major
        self.power = power

    def __str__(self):
        return "UUID: " + str(self.UUID) + " Major:" + str(self.major) + " Minor:" + str(self.minor)


class Bt(QtCore.QThread):
    new_beacon = QtCore.Signal(object)

    def __init__(self):
        QtCore.QThread.__init__(self, parent=None)
        subprocess.call("sudo hciconfig hci0 up", shell=True)
        subprocess.call("sudo hciconfig hci0 reset", shell=True)
        self.scan_proc = subprocess.Popen("sudo hcitool lescan --duplicates", stdout=subprocess.PIPE, shell=True)
        self.data_proc = subprocess.Popen("sudo hcidump --raw", stdout=subprocess.PIPE, shell=True)
        self.running = True
        print("Kot jest niebieski")
        self.start()

    def run(self):
        frame = []
        next_byte = 0
        counter = 0
        counter_byte = 3
        while self.running:
            new_data = str(self.data_proc.stdout.read(1), 'utf-8')
            if new_data == '>':
                counter = 0
                if frame != [] and len(frame) >= 44:
                    if frame[0] == 0x04 and frame[1] == 0x3e and frame[2] == 0x2a and frame[3] == 0x02:
                        b = Beacon(frame[7:12], frame[23:38], frame[39]*256+frame[40],
                                   frame[41]*256+frame[42], frame[43])
                        self.new_beacon.emit(b)
                    frame = []
            elif new_data == ' ':
                counter_byte = 0
                next_byte = 0
            elif counter_byte == 0:
                try:
                    next_byte = int(new_data, 16)*16
                    counter_byte = 1
                except ValueError:
                    counter = 0
                    counter_byte = 0
            elif counter_byte == 1:
                try:
                    next_byte += int(new_data, 16)
                    frame.append(next_byte)
                    counter_byte = 3
                    counter += 1
                except ValueError:
                    counter = 0

    def stop(self):
        self.running = False
        self.data_proc.terminate()
        self.scan_proc.terminate()
