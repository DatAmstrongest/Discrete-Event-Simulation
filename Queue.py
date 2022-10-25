class Queue ():
    
    def __init__(self,capacity):
        self.queue = []
        self.startIndex = -1
        self.sizeOfQueue = 0

    def enqueueCustomer (self,customer):
        self.queue.append(customer)
        self.sizeOfQueue += 1

    # If there is not customer, method will return -1.
    def dequeueCustomer(self):
        if self.sizeOfQueue == 0:
            return - 1
        previousIndex = self.startIndex
        self.startIndex += 1
        self.sizeOfQueue -= 1
        return self.queue[previousIndex]

    def getSize(self):
        return self.sizeOfQueue
