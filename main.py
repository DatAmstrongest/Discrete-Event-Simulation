from Customer import JOB_DONE, LEFT
from SimulationFactory import SimulationFactory 
import csv

def customer_to_tuple(customer):
    return (customer.getTeller(), customer.getArrivalTime(), customer.getServingTime(),customer.getDepartureTime(), customer.getWaitingTime(), customer.getIsLeft())


simulation = SimulationFactory()
simulation.startSimulation(240)

customerHeader = ['TellerName', 'ArrivalTime', 'ServingTime', 'DepartureTime','WaitingTime',"IsLeft"]
with open("customers.csv", "w") as streamCustomer:
    writer = csv.writer(streamCustomer)
    writer.writerow(customerHeader)
    for customer in simulation.getCustomerQueue():
        if customer.getIsJobDone() == JOB_DONE:
            row = customer_to_tuple(customer)
            writer.writerow(row)
    for customer in simulation.getLeftQueue():
        row = customer_to_tuple(customer)
        writer.writerow(row)
streamCustomer.close()


countedHeader = ["# Arrived", "# Lost", "# Attended the Queue", "# in Queue", "# in System","served"]


with open("counted.csv","w") as streamCounted:
    writer = csv.writer(streamCounted)
    writer.writerow(countedHeader)
    for i in range(10):
        simulation = SimulationFactory()
        simulation.startSimulation(240)
        arrived = 0
        lost = 0
        inQueue = 0
        served = 0
        inService = 0
        for customer in simulation.getCustomerQueue():
            arrived +=1
            if customer.getIsJobDone() == JOB_DONE:
                served += 1
            elif customer.getDepartureTime() > 240:
                inService += 1
            else:
                inQueue += 1

        for customer in simulation.getLeftQueue():
            arrived +=1
            lost += 1

        attendedTheQueue = arrived - lost
        inSystem = inQueue + inService
        writer.writerow((arrived, lost, attendedTheQueue, inQueue, inSystem,served))
            

