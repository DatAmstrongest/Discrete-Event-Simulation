
from Simulation import Simulation
import csv

def customer_to_tuple(customer):
    return (customer.getTellers(), customer.getArrivalTimes(), customer.getServiceTimes(), customer.getDepartureTimes(), customer.getWaitingTimes())


simulation = Simulation(4)
results = simulation.startSimulation(240)


customerHeader = ['TellerName', 'ArrivalTimes', 'ServiceTimes', 'DepartureTimes','WaitingTimes']
with open("customers.csv", "w") as streamCustomer:
    writer = csv.writer(streamCustomer)
    writer.writerow(customerHeader)
    for result in results:
        for customer in result:
            if customer != None:
                row = customer_to_tuple(customer)
                writer.writerow(row)

streamCustomer.close()