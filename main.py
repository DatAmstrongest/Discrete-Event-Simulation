from Queue import Queue
from Customer import Customer


myQueue = Queue()
myCustomer = Customer(1,5)

myCustomer.setTeller("Ahmet")
print(myCustomer.getTeller())
myCustomer.setWaitingTime(5)
print(myCustomer.getWaitingTime())
print(myCustomer.getDepartureTime())
myQueue.enqueueCustomer(myCustomer)
print(myQueue.dequeueCustomer().getTeller())