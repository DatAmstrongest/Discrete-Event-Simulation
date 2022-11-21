from Queue import Queue
from Customer import Customer,TYPES

import numpy as np
class Teller():
    
    def __init__(self, name, processingTimes):

        self.name = name
        self.queue = Queue()
        self.currentCustomer = None
        self.processingTimes = processingTimes

    def __lt__(self, U):
        if (self.getDepartureTime() < U.getDepartureTime()):
            return True
        return False
    

    def getDepartureTime(self):
        if self.currentCustomer == None:

            return float("inf")
        return self.currentCustomer.getCurrentDepartureTime()


    def setCustomer(self, customer, clock):
        
        serviceTime = self.generateServingTime(customer)
        waitingTime = clock - customer.getCurrentArrivalTime()
        departureTime = clock + serviceTime

        customer.addWaitingTime(waitingTime)
        customer.addServiceTime(serviceTime)
        customer.addDepartureTime(departureTime)

        self.currentCustomer = customer
    
    def leaveCustomer(self):
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
        customer.addTeller(self.name)
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

    
    


