from Customer import Customer,LEFT 
from Teller import Teller,BUSY,NOT_BUSY
from Queue import Queue 
import numpy as np

class SimulationFactory():
    def __init__(self):
        self.clock = 0
        self.teller1 = Teller("Metehan")
        self.teller2 = Teller("Ahmet")
        self.customerQueue = Queue()
        self.leftQueue = Queue()
        self.idleCustomer = None

    def startSimulation(self,simulationTime):
        while self.clock <= simulationTime:
            self.advanceTime()

    def advanceTime(self):
        if self.idleCustomer == None:
            arrivalTime = self.generateArrivalTime()
            self.idleCustomer = Customer(arrivalTime)
        if self.idleCustomer.getArrivalTime() < self.teller1.getDepartureTime() and self.idleCustomer.getArrivalTime() < self.teller2.getDepartureTime(): 
            self.addCustomer()
        else:
            if self.teller1.getDepartureTime() < self.idleCustomer.getArrivalTime() and self.teller1.getDepartureTime() < self.teller2.getDepartureTime() :
                self.makeTellerIdle(self.teller1)
            else:
                self.makeTellerIdle(self.teller2)

    def makeTellerIdle(self,teller):
        self.clock = teller.getDepartureTime()
        teller.setCustomer(None)
        teller.setIsBusy(NOT_BUSY)

    def addCustomer(self):
        self.clock = self.idleCustomer.getArrivalTime()
        if self.customerQueue.getSize() >= 5: 
            if np.random.choice([0,1],p=[0.4,0.6])==1:
                self.idleCustomer.setIsLeft(LEFT)
                self.leftQueue.enqueueCustomer(self.idleCustomer)
                self.idleCustomer = None
            else:
                self.customerQueue.enqueueCustomer(self.idleCustomer)
                self.idleCustomer = None
                
        elif self.customerQueue.getSize() == 4:
            if np.random.choice([0,1])==1:
                self.idleCustomer.setIsLeft(LEFT)
                self.leftQueue.enqueueCustomer(self.idleCustomer)
                self.idleCustomer = None
            else:
                self.customerQueue.enqueueCustomer(self.idleCustomer)
                self.idleCustomer = None
        else:
            self.customerQueue.enqueueCustomer(self.idleCustomer)
            self.idleCustomer = None


        self.assignCustomerToTeller()

    def assignCustomerToTeller(self):
        while (self.customerQueue.getSize() > 0):
            if self.teller1.getIsBusy() == NOT_BUSY and self.teller2.getIsBusy() == NOT_BUSY:
                if np.random.choice([0,1])==1:
                    servingTime = self.generateServingTimeForTeller1()
                    newCustomer = self.customerQueue.dequeueCustomer()
                    newCustomer.setTeller(self.teller1.getName())
                    newCustomer.setServingTime(servingTime)
                    newCustomer.setWaitingTime(self.clock)
                    self.teller1.setCustomer(newCustomer)
                else:
                    servingTime = self.generateServingTimeForTeller2()
                    newCustomer = self.customerQueue.dequeueCustomer()
                    newCustomer.setTeller(self.teller2.getName())
                    newCustomer.setServingTime(servingTime)
                    newCustomer.setWaitingTime(self.clock)
                    self.teller2.setCustomer(newCustomer)

            elif self.teller1.getIsBusy() == NOT_BUSY:
                servingTime = self.generateServingTimeForTeller1()
                newCustomer = self.customerQueue.dequeueCustomer()
                newCustomer.setTeller(self.teller1.getName())
                newCustomer.setServingTime(servingTime)
                newCustomer.setWaitingTime(self.clock)
                self.teller1.setCustomer(newCustomer)
            elif self.teller2.getIsBusy() == NOT_BUSY:
                servingTime = self.generateServingTimeForTeller1()
                newCustomer = self.customerQueue.dequeueCustomer()
                newCustomer.setTeller(self.teller2.getName())
                newCustomer.setServingTime(servingTime)
                newCustomer.setWaitingTime(self.clock)
                self.teller2.setCustomer(newCustomer)
            else:
                break

    def generateArrivalTime(self):                                             #function to generate arrival times using inverse trnasform
        return self.clock + (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 3)
    
    def generateServingTimeForTeller1(self):                                #function to generate service time for teller 1 using inverse trnasform
        return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 1.2)

    def generateServingTimeForTeller2(self):                                #function to generate service time for teller 1 using inverse trnasform
        return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 1.5)

    def getCustomerQueue(self):
        return self.customerQueue.getQueue()
    def getLeftQueue(self):
        return self.leftQueue.getQueue()