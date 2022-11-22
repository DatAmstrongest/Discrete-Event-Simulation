from Queue import Queue
from Customer import Customer,TYPES

import numpy as np
class Teller():
    
    def __init__(self, name, processingTimes):

        self.name = name
        self.queue = Queue()
        self.currentCustomer = None
        self.processingTimes = processingTimes
        self.totalRemainingTime = 0

    def __lt__(self, U):
        if (self.getDepartureTime() < U.getDepartureTime()):
            return True
        return False
    
    def getTotalRemainingTime(self):
        return self.totalRemainingTime


    def getDepartureTime(self):
        if self.currentCustomer == None:

            return float("inf")
        return self.currentCustomer.getCurrentDepartureTime()


    def setCustomer(self, customer, clock):
        
        waitingTime = clock - customer.getCurrentArrivalTime()
        departureTime = clock + customer.getCurrentServiceTime()

        customer.addWaitingTime(waitingTime)
        customer.addDepartureTime(departureTime)

        self.currentCustomer = customer
    
    def leaveCustomer(self):
        self.totalRemainingTime -= self.currentCustomer.getCurrentServiceTime()
        self.currentCustomer.increaseFinishedJobs()
        leftCustomer = self.currentCustomer
        self.currentCustomer = None
        return leftCustomer

    def getCustomerFromQueue(self,clock):
        if self.getIsBusy() == False:
            customer = self.queue.dequeueCustomer()
            if customer != None:
                
                self.setCustomer(customer, clock)
            else:
                return
            

    
    def addCustomerToQueue(self, customer):
        serviceTime = self.generateServingTime(customer)

        customer.addServiceTime(serviceTime)
        customer.addTeller(self.name)

        self.totalRemainingTime += serviceTime

        self.queue.enqueueCustomer(customer)


    def getIsBusy(self):
        return self.currentCustomer != None


    def getName(self):
        return self.name


    def generateServingTime(self, customer):   
                         #function to generate service time for teller 1 using inverse trnasform
        return self.processingTimes[TYPES.index(customer.getType())]

    def getQueue(self):
        return self.queue.getQueue()

    
    


