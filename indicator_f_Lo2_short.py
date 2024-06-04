import numpy
import datetime

class KBar():
    def __init__(self, date, type='time', cycle=1):
        if type == 'time':
            self.Cycle = datetime.timedelta(minutes=cycle)
            self.StartTime = datetime.datetime.strptime(date+'084500', '%Y%m%d%H%M%S') - (self.Cycle * 2)
            self.Time = numpy.array([self.StartTime])
            self.Open = numpy.array([0])
            self.High = numpy.array([0])
            self.Low = numpy.array([10000000000000])
            self.Close = numpy.array([0])
            self.Volume = numpy.array([0])
            self.Prod = numpy.array([''])
            self.flag = 0
        elif type == 'volume':
            self.Cycle = cycle
            self.Amount = 0
            self.Open = numpy.array([])
            self.High = numpy.array([])
            self.Low = numpy.array([])
            self.Close = numpy.array([])

    def TimeAdd(self, time, price, qty, prod):
        while self.flag == 0 and time >= self.StartTime:
            self.Time[-1] = self.StartTime
            self.StartTime += self.Cycle
        self.flag = 1
        if time < self.Time[-1] + self.Cycle:
            self.Close[-1] = price
            self.Volume[-1] += qty
            if price > self.High[-1]:
                self.High[-1] = price
            elif price < self.Low[-1]:
                self.Low[-1] = price
            return 0
        elif time >= self.Time[-1] + self.Cycle:
            self.Time = numpy.append(self.Time, self.Time[-1] + self.Cycle)
            self.Open = numpy.append(self.Open, price)
            self.High = numpy.append(self.High, price)
            self.Low = numpy.append(self.Low, price)
            self.Close = numpy.append(self.Close, price)
            self.Volume = numpy.append(self.Volume, qty)
            self.Prod = numpy.append(self.Prod, prod)
            return 1

    def VolumeAdd(self, price, amount):
        if self.Amount == 0:
            self.Open = numpy.append(self.Open, price)
            self.High = numpy.append(self.High, price)
            self.Low = numpy.append(self.Low, price)
            self.Close = numpy.append(self.Close, price)
            self.Amount = amount
        elif amount - self.Amount <= self.Cycle:
            self.Close[-1] = price
            if price > self.High[-1]:
                self.High[-1] = price
            elif price < self.Low[-1]:
                self.Low[-1] = price
            return 0
        elif amount - self.Amount >= self.Cycle:
            self.Open = numpy.append(self.Open, price)
            self.High = numpy.append(self.High, price)
            self.Low = numpy.append(self.Low, price)
            self.Close = numpy.append(self.Close, price)
            self.Amount = amount
            return 1

class BSPower():
    def __init__(self):
        self.BP = 0
        self.SP = 0
        self.LastPrice = None

    def Add(self, price, qty):
        if self.LastPrice is None:
            self.LastPrice = price
        else:
            if price > self.LastPrice:
                self.BP += qty
            elif price < self.LastPrice:
                self.SP += qty
            self.LastPrice = price

    def Get(self):
        return [self.BP, self.SP]

class BigOrder():
    def __init__(self, num):
        self.BigFlag = num
        self.B = 0
        self.S = 0
        self.BC = 0
        self.SC = 0
        self.OnceB = 0
        self.OnceS = 0

    def Add(self, qty, bc, sc):
        if qty > self.BigFlag:
            BuyCntDiff = bc - self.BC
            SellCntDiff = sc - self.SC
            if BuyCntDiff == 1 and BuyCntDiff < SellCntDiff:
                self.B += qty
                self.OnceB = qty
                self.OnceS = 0
            elif SellCntDiff == 1 and BuyCntDiff > SellCntDiff:
                self.S += qty
                self.OnceB = 0
                self.OnceS = qty
        self.BC = bc
        self.SC = sc

    def Get(self):
        return [self.OnceB, self.OnceS, self.B, self.S]

class CommissionDiff():
    def __init__(self, date, cycle):
        self.DataList = [[datetime.datetime.strptime(date+'084500', '%Y%m%d%H%M%S'), 0, 0, 0, 0]]
        self.Cycle = datetime.timedelta(minutes=cycle)

    def Add(self, time, BC, BO, SC, SO):
        self.DataList.append([time, BC, BO, SC, SO])
        while self.DataList[-1][0] > self.DataList[0][0] + self.Cycle:
            self.DataList = self.DataList[1:]

    def GetOrderDiff(self):
        BODiff = self.DataList[-1][2] - self.DataList[0][2]
        SODiff = self.DataList[-1][4] - self.DataList[0][4]
        return [BODiff, SODiff]

class AccVol():
    def __init__(self, date, cycle):
        self.DataList = [[datetime.datetime.strptime(date+'084500', '%Y%m%d%H%M%S'), 0]]
        self.Cycle = datetime.timedelta(minutes=cycle)

    def Get(self):
        volume = self.DataList[-1][1] - self.DataList[0][1]
        return volume

    def Add(self, Time, Amount):
        self.DataList.append([Time, Amount])
        while self.DataList[-1][0] > self.DataList[0][0] + self.Cycle:
            self.DataList = self.DataList[1:]
            
        


