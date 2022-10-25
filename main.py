from SimulationFactory import SimulationFactory 
import csv

def customer_to_tuple(customer):
    return (customer.getTeller(), customer.getArrivalTime(), customer.getServingTime(),customer.getDepartureTime(), customer.getWaitingTime(), customer.getIsLeft())


simulation = SimulationFactory()
simulation.startSimulation(240)

with open("customers.csv", "w") as stream:
    customerHeader = ['TellerName', 'ArrivalTime', 'ServingTime', 'DepartureTime','WaitingTime',"IsLeft"]
    writer = csv.writer(stream)
    writer.writerow(customerHeader)
    for customer in simulation.getQueue():
        row = customer_to_tuple(customer)
        writer.writerow(row)
