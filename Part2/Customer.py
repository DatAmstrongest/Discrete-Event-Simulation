TYPE1 = [0,1]
TYPE2 = [1,0]
class Customer ():

    def __init__(self, type, arrivalTime):
        self.type = type
        self.arrivalTimes = [arrivalTime]
        self.departureTimes = []
        self.waitingTimes = []
        self.serviceTimes = []
        self.tellers = []
        self.finishedJobs = 0
        
    def getType(self):
        return self.type
    
    def getArrivalTimes(self):
        return self.arrivalTimes

    def addArrivalTime(self, arrivalTime):
        self.arrivalTimes.append(arrivalTime)
    
    def getDepartureTimes(self):
        return self.departureTimes
    
    def addDepartureTime(self, departureTime):
        self.departureTimes.append(departureTime)
    
    def getWaitingTimes(self):
        return self.waitingTimes
    
    def addWaitingTimes(self, waitingTime):
        self.waitingTimes.append(waitingTime)

    def getTellers(self):
        return self.tellers

    def addTeller(self, teller):
        self.tellers.append(teller)
    
    def getFinishedJobs(self):
        return self.finishedJobs

    def increaseFinishedJobs(self):
        self.finishedJobs += 1

    





        