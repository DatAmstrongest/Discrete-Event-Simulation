from Queue import Queue
from Customer import Customer

import numpy as np
class Teller():
    
    def __init__(self, name):

        self.name = name
        self.queue = Queue()
        self.currentCustomer = None
    

    def getDepartureTime(self):
        if self.customer == None:
            return float("inf")
        return self.currentCustomer.getCurrentDepartureTime()


    def setCustomer(self, customer, clock):
        
        serviceTime = self.generateServingTime()
        waitingTime = clock - self.getCurrentArrivalTime()
        departureTime = clock + serviceTime

        customer.addWaitingTime(waitingTime)
        customer.addServiceTime(serviceTime)
        customer.addDepartureTime = departureTime

        self.currentCustomer = customer
    
    def leaveCustomer(self):
        self.currentCustomer.increaseFinishedJobs()
        leftCustomer = self.currentCustomer
        self.currentCustomer = None
        return leftCustomer

    def getCustomerFromQueue(self):

        customer = self.queue.dequeueCustomer()
        if customer == None:
            return None
        else:
            self.setCustomer(customer)
    
    def addCustomerToQueue(self, customer):
        self.queue.enqueueCustomer(customer)


    def getIsBusy(self):
        return self.customer == None


    def getName(self):
        return self.name


    def generateServingTime(self):                                #function to generate service time for teller 1 using inverse trnasform
        return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 12)

    def getQueue(self):
        return self.queue.getQueue()

    
    


