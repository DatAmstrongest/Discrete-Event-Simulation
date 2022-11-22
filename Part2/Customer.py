import numpy as np

TYPES = [[1,0,3,2],[3,1,2,0],[0,2,3,1],[2,1,0,3]]
class Customer ():

    def __init__(self, type, clock, numInSystem, remainingTime):
        self.type = type
        self.arrivalTimes = []
        self.departureTimes = []
        self.waitingTimes = []
        self.serviceTimes = []
        self.tellers = []
        self.finishedJobs = 0
        self.numInSystemOnArrive = numInSystem
        self.remainingTimeOnArrive = remainingTime
        self.generateArrivalTime(clock)


    def getRemainingTimeOnArrive(self):
        return self.remainingTimeOnArrive
        

    def  getNumInSystemOnArrive(self):
        return self.numInSystemOnArrive
    

    def getType(self):
        return self.type


    def getNextTeller(self):
        return self.type[self.finishedJobs]
        

    def getCurrentArrivalTime(self):
        return self.arrivalTimes[self.finishedJobs]

    def getArrivalTimes(self):
        return self.arrivalTimes

    def addArrivalTime(self, arrivalTime):
        self.arrivalTimes.append(arrivalTime)

    def generateArrivalTime(self, clock):                                             #function to generate arrival times using inverse trnasform
        arrivalTime = clock + (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 3)
        self.addArrivalTime(arrivalTime)
    

    def getCurrentDepartureTime(self):
        return self.departureTimes[self.finishedJobs]

    def getDepartureTimes(self):
        return self.departureTimes
    
    def addDepartureTime(self, departureTime):
        self.departureTimes.append(departureTime)

    
    def getCurrentWaitingTime(self):
        return self.waitingTimes[self.finishedJobs]

    def getWaitingTimes(self):
        return self.waitingTimes
    
    def addWaitingTime(self, waitingTime):
        self.waitingTimes.append(waitingTime)


    def getCurrentServiceTime(self):
        return self.serviceTimes[self.finishedJobs]

    def getServiceTimes(self):
        return self.serviceTimes

    def addServiceTime(self, serviceTime):
        self.serviceTimes.append(serviceTime)


    def getTellers(self):
        return self.tellers

    def addTeller(self, teller):
        self.tellers.append(teller)

    
    def getFinishedJobs(self):
        return self.finishedJobs

    def increaseFinishedJobs(self):
        self.finishedJobs += 1



    





        