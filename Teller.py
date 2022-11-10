from Customer import JOB_DONE, Customer
BUSY = 1
NOT_BUSY = 0
class Teller ():
    def __init__(self,name):
        self.name = name
        self.isBusy = NOT_BUSY
        self.customer = None
        self.totalServingTime = 0

    def setCustomer(self,customer):
        self.customer = customer
        if customer == None:
            self.setIsBusy(NOT_BUSY)
        else:
            self.setIsBusy(BUSY)

    def leaveCustomer(self,queueSize):
        self.isBusy = NOT_BUSY
        self.customer.setIsJobDone(JOB_DONE)
        self.customer.setInQueueLeft(queueSize)
        self.customer = None

    def getDepartureTime(self):
        if self.customer == None:
            return float("inf")
        return self.customer.getDepartureTime()

    def getIsBusy(self):
        return self.isBusy

    def setIsBusy(self,value):
        self.isBusy = value

    def getName(self):
        return self.name

    def getTotalServingTime(self):
        return self.totalServingTime

    def increaseServingTime(self):
        self.totalServingTime += self.customer.getServingTime()
    


