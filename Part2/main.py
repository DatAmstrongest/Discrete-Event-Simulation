
from Simulation import Simulation
from Customer import TYPES
import csv



simulation = Simulation(4)
results = simulation.startSimulation(240)


customerHeader = ['JobType', 'ArrivalTime', 'CompletionTime',"flowTime", 'SumOfProcessTimes', "ENumInSys","TotalRemainingTimeOnArrive",'k']
with open("customers.csv", "w") as streamCustomer:
    writer = csv.writer(streamCustomer)
    writer.writerow(customerHeader)
    for result in results:
        for customer in result:
            if customer != None and len(customer.getDepartureTimes()) == len(TYPES):
                jobType = TYPES.index(customer.getType())+1
                arrivalTime = customer.getArrivalTimes()[0]
                completionTime = customer.getDepartureTimes()[-1]
                flowTime = completionTime - arrivalTime
                theoreticalMinimumFlowTime = sum(customer.getType())
                eNumInSys = customer.getNumInSystemOnArrive()
                totalRemainingTime = customer.getRemainingTimeOnArrive()
                k = flowTime/theoreticalMinimumFlowTime
                writer.writerow((jobType, arrivalTime, completionTime, flowTime, theoreticalMinimumFlowTime, eNumInSys, totalRemainingTime, k))

streamCustomer.close()