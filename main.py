from Customer import JOB_DONE, LEFT
from SimulationFactory import SimulationFactory 
import csv

def customer_to_tuple(customer):
    return (customer.getTeller(), customer.getArrivalTime(), customer.getServingTime(),customer.getDepartureTime(), customer.getWaitingTime(), customer.getIsLeft(), customer.getInQueueArrive(), customer.getInQueueLeft())


simulation = SimulationFactory()
simulation.startSimulation(240)

customerHeader = ['TellerName', 'ArrivalTime', 'ServingTime', 'DepartureTime','WaitingTime',"IsLeft","InQueueArrive","InQueueLeft"]
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

averageHeader = ["Average Interarrival Time", "Average Waiting Time", "Average Service Time", "Average Total time in System", "Utilization of Teller1", "Utilization of Teller2"]

with open("average.csv","w") as streamAverage:
    writer = csv.writer(streamAverage)
    writer.writerow(averageHeader)
    for i in range(10):
        simulation = SimulationFactory()
        simulation.startSimulation(240)

        customerQueue = simulation.getCustomerQueue()

        totalInterarrival = 0
        totalWaitingTime = 0
        totalTimeInSystem = 0
        totalCustomers = len(customerQueue)


        for index in range(totalCustomers):

            customer = customerQueue[index]
            if index == 0:
                totalInterarrival += customer.getArrivalTime()
            else:
                previousCustomer = customerQueue[index-1]
                totalInterarrival +=  customer.getArrivalTime() - previousCustomer.getArrivalTime()
            
            totalWaitingTime += customer.getWaitingTime()
            totalTimeInSystem += customer.getDepartureTime() - customer.getArrivalTime()
    
    averageInterarrivalTime = totalInterarrival/totalCustomers
    averageWaitingTime = totalWaitingTime/totalCustomers
    averageServiceTime = (simulation.getTeller1ServingTime()+simulation.getTeller2ServingTime())/totalCustomers
    averageTimeInSystem = totalTimeInSystem/totalCustomers
    
    teller1Utilization = simulation.getTeller1ServingTime()/240
    teller2Utilization = simulation.getTeller2ServingTime()/240

    writer.writerow((averageInterarrivalTime, averageWaitingTime, averageServiceTime, averageTimeInSystem, teller1Utilization, teller2Utilization))




