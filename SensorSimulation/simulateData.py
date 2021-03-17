import json
import numpy as np

import math
import ctypes
import pathlib
import time

from threading import Thread

data = np.zeros((7, 4), dtype=np.int16)
theThread = 0

def loadCharacterisation(filename):
    with open(filename, 'r') as f:
        characterisation = json.load(f)

    return characterisation

fList = loadCharacterisation("../sensorCharacterisation/param.json")

def getTaxelsValueFromCharacterisation(fList, force, closestPosX, closestPosY):
    taxelValues = np.zeros((7, 4))

    for pos in fList:
        posString = pos.split(":")
        if closestPosX == float(posString[0]) and closestPosY == float(posString[1]):

            for i in range(len(fList[pos])):
               for ii in range(len(fList[pos][i])):
                   [a, b, c, d, e, f] = fList[pos][i][ii]
                   taxelValues[i, ii] = fun(force, a, b, c, d, e, f)
            return taxelValues

    #Error, no data at that point
    return []


def getGlobalTaxelValuesFromSpecificPosition(force, posX, posY):
    global fList
    base = 4.0

    #Get the square
    x0 = base * math.floor(posX/base)
    x1 = x0 + base
    y0 = base * math.floor(posY/base)
    y1 = y0 + base

    #GetTheRatios
    x0_r = (posX-x0)/(x1-x0)
    x1_r = 1.0 - x0_r
    y0_r = (posY-y0)/(y1-y0)
    y1_r = 1.0 - y0_r

    x0y0_r = x0_r * y0_r
    x1y0_r = x1_r * y0_r
    x0y1_r = x0_r * y1_r
    x1y1_r = x1_r * y1_r

    #getResultsOfEachTaxel
    x0y0_v = getTaxelsValueFromCharacterisation(fList, force, x0, y0)
    x1y0_v = getTaxelsValueFromCharacterisation(fList, force, x1, y0)
    x0y1_v = getTaxelsValueFromCharacterisation(fList, force, x0, y1)
    x1y1_v = getTaxelsValueFromCharacterisation(fList, force, x1, y1)

    #ultimateResult
    taxelValue = (x0y0_r * x0y0_v) + (x1y0_r * x1y0_v) + (x0y1_r * x0y1_v) + (x1y1_r * x1y1_v)
    global data
    data = taxelValue.astype('int16')


def fun(x, a, b, c, d, e, f):
    return a * x + b * x ** 2 + c * x ** 3 + d * x ** 4 + e * x ** 5 + f


def startStreaming():
    global theThread
    theThread = Thread(target=stream)
    theThread.daemon = True
    theThread.start()


def stream():

    libname = pathlib.Path().absolute() / "libTactileSensorSimulationComm.so"
    c_lib = ctypes.CDLL(libname)

    net = ctypes.c_int32()
    c_lib.createPseudoTerminal(ctypes.byref(net))

    streaming = True
    global data
    while streaming:
        start = time.time()
        data = np.random.randint(100, size=(7, 4))
        arr = (ctypes.c_int16 * len(data.flatten().tolist()))(*data.flatten().tolist())
        c_lib.sendStaticData(0, ctypes.byref(arr))
        #c_lib.sendStaticData(0, ctypes.byref(arr))
        timing = time.time() - start
        time.sleep(0.01)
        #print(time.time() - start)


if __name__ == '__main__':
    startStreaming()
    while True:
        a = 18**23
        time.sleep(0.0001)