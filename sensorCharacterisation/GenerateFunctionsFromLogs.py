from os import listdir
from os.path import isfile, join
import numpy as np
from scipy.optimize import curve_fit
import csv

import json

allData = []
allForces = []
allDataName = []
allDataPosition = []
allDataZero = []


def getPositionInFilename(fileName):
    test = fileName.split("_")
    posX = int(test[1])
    posY = int(test[2].split(".")[0])
    return posX, posY


def loadAllData():
    onlyFiles = [f for f in listdir("./logging/logs") if isfile(join("./logging/logs", f))]

    for file in onlyFiles:
        with open('logging/logs/' + file, newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            currentForce = []
            currentData = []
            firstRow = True

            for row in csvReader:
                force = float(row[0])
                a = np.matrix(row[1:])
                a = a.astype(float)
                b = np.reshape(a, (7, 4))

                if firstRow:
                    allDataZero.append(b)
                    firstRow = False
                currentForce.append(force)
                currentData.append(b)

            allForces.append(currentForce)
            allDataName.append(file)
            allDataPosition.append(getPositionInFilename(file))
            allData.append(currentData)


def zeroAllData(zero, leData):
    test = np.array(zero)
    test = np.mean(test, axis=0)

    data = []
    for i in range(len(leData)):
        d = np.array(leData[i])
        a = np.array(zero[i])
        d = d - a
        data.append(d)

    return test, data


def fun(x, a, b, c, d, e, f):
    return a * x + b * x ** 2 + c * x ** 3 + d * x ** 4 + e * x ** 5 + f


def generateFunction(data, force):
    columnX = []
    for i in range(7):
        rowY = []
        for ii in range(4):
            t = np.array(force)
            y = data[:, i, ii]

            res_robust, _ = curve_fit(fun, t, y)

            t_test = np.linspace(t.min(), t.max(), 300)
            a, b, c, d, e, f = res_robust
            result = fun(t_test, a, b, c, d, e, f)

            rowY.append([a, b, c, d, e, f])

        columnX.append(rowY)
    return columnX


def saveFunctionParameter(functionsParam):
    with open('param.json', 'w') as f:
        json.dump(functionsParam, f, indent=2)


if __name__ == '__main__':
    loadAllData()
    t, d = zeroAllData(allDataZero, allData)

    taxelFunctions = dict()

    for i in range(len(d)):
        functions = generateFunction(d[i], allForces[i])
        taxelFunctions[str(allDataPosition[i][0]) + ":" + str(allDataPosition[i][1])] = functions

    saveFunctionParameter(taxelFunctions)
