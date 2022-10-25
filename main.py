from Queue import Queue


myQueue = Queue(20)
myQueue.enqueueCustomer(10)
print(myQueue.dequeueCustomer())
print(myQueue.dequeueCustomer())