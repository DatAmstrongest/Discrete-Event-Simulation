LEFT = 1

class Customer():
    def __init__(self,arrivalTime):
        self.teller = ""
        self.arrivalTime = arrivalTime
        self.servingTime = 0
        self.departureTime = 0
        self.waitingTime  = 0
        self.isLeft = 0 # 0 means customer didn't leave the bank

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
        self.setDepartureTime(clock)

    def getDepartureTime(self,):
        return self.departureTime

    def setDepartureTime(self,clock):
        self.departureTime = self.arrivalTime + self.waitingTime + self.servingTime


    def setTeller(self,teller):
        self.teller = teller

    def getTeller(self):
        return self.teller

    def getIsLeft(self):
        return self.isLeft

    def setIsLeft(self,isLeft) :
        self.isLeft = isLeft



    
        
        
        