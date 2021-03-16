# !/usr/bin/env python
import rospy
from threading import Thread
import time
from tactilesensors4.msg import StaticData


class TactileSensorSubscriber:

    def __init__(self, sensor="Sensor1"):
        self.__sensor = sensor
        self.__active = True
        self.values = None

        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber("/TactileSensor4/" + self.__sensor + "/StaticData", StaticData, self.__callback)

        self.__commThread = Thread(target=self.__startListening)
        self.__commThread.daemon = True
        self.__commThread.start()

    def __del__(self):
        self.__active = False
        if self.__commThread.is_alive():
            self.__commThread.join()

    def __callback(self, data):
        self.values = data.value

    def __startListening(self):
        rospy.spin()


if __name__ == "__main__":
    test = TactileSensorSubscriber()
    for i in range(100):
        if test.values is not None:
            print(test.values[0])
        time.sleep(0.1)

