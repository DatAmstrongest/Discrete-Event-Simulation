
BUSY = 1

class Teller ():
    def __init__(self,name):
        self.name = name
        self.isBusy = 0
        self.customer = None

    def setCustomer(self,customer):
        self.customer = customer

    def getDepartureTime(self):
        return self.customer.getDepartureTime()

    def getIsBusy(self):
        return self.isBusy

    def setIsBusy(self,value):
        self.isBusy = value


