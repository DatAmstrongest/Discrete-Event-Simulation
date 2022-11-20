
from Simulation import Simulation
import csv

def customer_to_tuple(customer):
    return (customer.getTellers(), customer.getArrivalTimes(), customer.getServiceTimes(), customer.getDepartureTimes(), customer.getWaitingTimes())


simulation = Simulation()
teller1Queue, teller2Queue = simulation.startSimulation(240)


customerHeader = ['TellerName', 'ArrivalTimes', 'ServiceTimes', 'DepartureTimes','WaitingTimes']
with open("customers.csv", "w") as streamCustomer:
    writer = csv.writer(streamCustomer)
    writer.writerow(customerHeader)
    for customer in teller1Queue:
        if customer != None:
            row = customer_to_tuple(customer)
            writer.writerow(row)
    for customer in teller2Queue:
        if customer != None:
            row = customer_to_tuple(customer)
            writer.writerow(row)
streamCustomer.close()