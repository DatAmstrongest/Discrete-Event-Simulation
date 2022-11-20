class Queue ():
    
    def __init__(self):
        self.queue = []
        self.startIndex = 0
        self.sizeOfQueue = 0

    def enqueueCustomer (self,customer):
        self.queue.append(customer)
        self.sizeOfQueue += 1

    # If there is not customer, method will return -1.
    def dequeueCustomer(self):
        if self.sizeOfQueue == 0:
            return None
        previousIndex = self.startIndex
        self.startIndex += 1
        self.sizeOfQueue -= 1
        customer = self.queue[previousIndex]
        if customer.getFinishedJobs() > 0:
            self.queue[previousIndex] = None
        return customer 

    def getSize(self):
        return self.sizeOfQueue
        
    def getQueue(self):
        return self.queue