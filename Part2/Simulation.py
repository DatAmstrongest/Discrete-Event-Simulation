from Teller import Teller
from Customer import Customer,TYPES

import heapq
import numpy as np
import random
class Simulation ():

    def __init__(self, tellerNum):

        self.clock = 0
        self.tellers = []
        self.sortedTellers = []
        self.servingTimes = [[1,2,1,3],[2,1,1,2],[1,3,3,2],[2,3,2,3]]
        for i in range(tellerNum):
            servingTime = self.servingTimes[i]
            teller = Teller(str(i), servingTime)
            self.tellers.append(teller)
            self.sortedTellers.append(teller)
         
        self.idleCustomer = None
        self.tellerNum = tellerNum
        self.totalInSystem = 0
    
    def startSimulation(self,simulationTime):
        while self.clock <= simulationTime:
            self.advanceTime()
        result = []
        for teller in self.tellers:
            result.append(self.getQueueOfTeller(teller))
        return result
    
    def advanceTime(self): 
        if self.idleCustomer == None:
            type = random.sample(TYPES,1)[0]
            totalRemainingTime = 0
            for teller in self.tellers:
                totalRemainingTime += teller.getTotalRemainingTime()
            self.idleCustomer = Customer(type,self.clock, self.totalInSystem, totalRemainingTime)
        heapq.heapify(self.sortedTellers)

        if self.idleCustomer.getCurrentArrivalTime() < self.sortedTellers[0].getDepartureTime(): 
            self.clock = self.idleCustomer.getCurrentArrivalTime()
            nextTeller = self.idleCustomer.getNextTeller()
            self.tellers[nextTeller].addCustomerToQueue(self.idleCustomer)
            self.totalInSystem += 1
            self.idleCustomer = None
        else:
            self.clock = self.sortedTellers[0].getDepartureTime()
            customer = self.sortedTellers[0].leaveCustomer()
            self.totalInSystem -= 1
            if customer.getFinishedJobs() < self.tellerNum:
                customer.addArrivalTime(self.clock)
                nextTeller = customer.getNextTeller()

                self.tellers[nextTeller].addCustomerToQueue(customer)
                self.totalInSystem += 1
            
        for teller in self.tellers:
            teller.getCustomerFromQueue(self.clock)

    def getQueueOfTeller(self, teller):
        return teller.getQueue()

                
        