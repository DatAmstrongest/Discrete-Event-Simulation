LEFT = 1
JOB_DONE = 1

class Customer():
    def __init__(self,arrivalTime):
        self.teller = ""
        self.arrivalTime = arrivalTime
        self.servingTime = 0
        self.departureTime = 0
        self.waitingTime  = 0
        self.isLeft = 0 
        self.isJobDone = 0
        self.inQueueArrive = -1
        self.inQueueLeft = -1

    def getServingTime(self):
        return self.servingTime

    def setServingTime(self,servingTime):
        self.servingTime = servingTime

    def getArrivalTime(self):
        return self.arrivalTime

    def getWaitingTime(self):
        return self.waitingTime

    def setWaitingTime(self,clock):
        self.waitingTime = clock - self.arrivalTime
        self.setDepartureTime()

    def getDepartureTime(self):
        return self.departureTime

    def setDepartureTime(self):
        self.departureTime = self.arrivalTime + self.waitingTime + self.servingTime

    def getTeller(self):
        return self.teller
    
    def setTeller(self,teller):
        self.teller = teller

    def getIsLeft(self):
        return self.isLeft

    def setIsLeft(self,isLeft) :
        self.isLeft = isLeft

    def getIsJobDone(self):
        return self.isJobDone
    
    def setIsJobDone(self,value):
        self.isJobDone = value

    def getInQueueArrive(self):
        return self.inQueueArrive

    def setInQueueArrive(self, value):
        self.inQueueArrive = value
    
    def getInQueueLeft(self):
        return self.inQueueLeft

    def setInQueueLeft(self, value):
        self.inQueueLeft = value
      
        
        