import csv
from TactileSensorSubscriber import TactileSensorSubscriber
from Mark10Comm import Mark10Communication
import time
import threading

xPos = 0.0
yPos = 0.0

recording = False
ts = TactileSensorSubscriber()
mc = Mark10Communication()

def createLogFile():
    with open("logging/log_"+str(xPos)+"_"+str(yPos)+".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        titles = ['force']
        for i in range(28):
            titles.append("t" + str(i))
        writer.writerow(titles)

def logData():
    with open("logging/log_" + str(xPos) + "_" + str(yPos) + ".csv", 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        while recording:
            line = [mc.force]
            for i in range(28):
                line.append(ts.values[i])
            writer.writerow(line)
            time.sleep(0.2)


if __name__ == "__main__":

    while True:
        value = input("Enter next values (posX posY) to start recording - q to exit: ")
        values = value.split()

        if value == "q":
            break
        if len(values) == 2:
            isValid = True

            try:
                xPos = int(values[0])
            except ValueError:
                isValid = False
                print("xPos is not a float")

            try:
                yPos = int(values[1])
            except ValueError:
                isValid = False
                print("yPos is not a float")

            if isValid:
                recording = True
                t = threading.Thread(target=logData)
                t.daemon = True
                t.start()

                value = input("Press any key to stop...")

                recording = False
                t.join()
        else:
            print("Wrong number of values...")