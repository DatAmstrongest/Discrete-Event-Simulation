
BUSY = 1
NOT_BUSY = 0
class Teller ():
    def __init__(self,name):
        self.name = name
        self.isBusy = 0
        self.customer = None

    def setCustomer(self,customer):
        self.customer = customer
        if customer == None:
            self.setIsBusy(NOT_BUSY)
        else:
            self.setIsBusy(BUSY)

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
    


