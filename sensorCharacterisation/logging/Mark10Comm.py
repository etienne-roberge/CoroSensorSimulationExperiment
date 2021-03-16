import time
import threading

import serial


class Mark10Communication:

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600):
        self.__port = port
        self.__baudrate = baudrate
        self.__active = True
        self.force = 0.0

        self.__commThread = threading.Thread(target=self.__askMark10)
        self.__commThread.daemon = True
        self.__commThread.start()

    def __del__(self):
        self.__active = False
        if self.__commThread.is_alive():
            self.__commThread.join()

    def __askMark10(self):
        with serial.Serial(self.__port, self.__baudrate, timeout=1) as ser:
            while self.__active:
                readCommand = "?"
                ser.write(readCommand.encode())
                ser.write("\r\n".encode())
                try:
                    self.force = float(ser.readline(100))
                except ValueError:
                    print("force over 50 newton!")
                    self.force = -1.0
                time.sleep(0.05)


if __name__ == "__main__":
    test = Mark10Communication()
    while True:
        print(test.force)
        time.sleep(0.1)



