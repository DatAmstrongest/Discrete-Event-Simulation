from Teller import Teller
from Customer import Customer,TYPE1,TYPE2

import numpy as np
class Simulation ():

    def __init__(self):

        self.clock = 0
        self.teller1 = Teller("Metehan")
        self.teller2 = Teller("Ahmet")
        self.idleCustomer = None
    
    def startSimulation(self,simulationTime):
        while self.clock <= simulationTime:
            self.advanceTime()
    
    def advanceTime(self): 
        if self.idleCustomer == None:
            type = np.random.choice([TYPE1,TYPE2]) 
            self.idleCustomer = Customer(type,self.clock)
        if self.idleCustomer.getCurrentArrivalTime() < self.teller1.getDepartureTime() and self.idleCustomer.getArrivalTime() < self.teller2.getDepartureTime(): 
            self.clock = self.idleCustomer.getCurrentArrivalTime()
            if self.idleCustomer.getType() == TYPE1:
                self.teller1.addCustomerToQueue(self.idleCustomer)
            else:
                self.teller2.addCustomerToQueue(self.idleCustomer)
            self.idleCustomer = None
        else:
            if self.teller1.getDepartureTime() < self.idleCustomer.getCurrentArrivalTime() and self.teller1.getDepartureTime() < self.teller2.getDepartureTime() :
                self.clock = self.teller1.getDepartureTime()
                customer = self.teller1.leaveCustomer()
                if customer.getFinishedJobs() < 2:
                    self.teller2.addCustomerToQueue(customer)
            else:
                self.clock = self.teller2.getDepartureTime()
                customer = self.teller2.leaveCustomer()
                if customer.getFinishedJobs() < 2:
                    self.teller1.addCustomerToQueue(customer)
        self.teller1.getCustomerFromQueue()
        self.teller2.getCustomerFromQueue()

    def getQueueOfTeller(self, teller):
        return teller.getQueue()

                
        