from Customer import JOB_DONE
from SimulationFactory import SimulationFactory 
import csv

def customer_to_tuple(customer):
    return (customer.getTeller(), customer.getArrivalTime(), customer.getServingTime(),customer.getDepartureTime(), customer.getWaitingTime(), customer.getIsLeft())


simulation = SimulationFactory()
simulation.startSimulation(240)

customerHeader = ['TellerName', 'ArrivalTime', 'ServingTime', 'DepartureTime','WaitingTime',"IsLeft"]
with open("customers.csv", "w") as stream1:
    writer = csv.writer(stream1)
    writer.writerow(customerHeader)
    for customer in simulation.getCustomerQueue():
        if customer.getIsJobDone() == JOB_DONE:
            row = customer_to_tuple(customer)
            writer.writerow(row)
    for customer in simulation.getLeftQueue():
        row = customer_to_tuple(customer)
        writer.writerow(row)

