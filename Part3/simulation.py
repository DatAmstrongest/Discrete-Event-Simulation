# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 10:31:38 2022

Author: Tevhide Altekin

"""
import numpy as np
import pandas as pd
# Importing other required libraries
from math import ceil


#A. Define job shop problem parameters
num_machines = 4               #given number of machines
num_job_types = 4              #given number of job types
sequence = {}                  #given sequences of job types op#: m/c#
sequence[1] = {1: 2, 2: 1, 3: 4, 4: 3}
sequence[2] = {1: 4, 2: 2, 3: 3, 4: 1}
sequence[3] = {1: 1, 2: 3, 3: 4, 4: 2}
sequence[4] = {1: 3, 2: 2, 3: 1, 4: 4}
ptime = {}                     #given process times of job types on machines
ptime[1] = {1: 1, 2: 2, 3: 1, 4: 2} #paperdeki {1: 1, 2: 2, 3: 1, 4: 2}
ptime[2] = {1: 2, 2: 1, 3: 2, 4: 1} #paperdaki {1: 2, 2: 1, 3: 3, 4: 3}
ptime[3] = {1: 1, 2: 1, 3: 2, 4: 2} #paperdaki {1: 1, 2: 1, 3: 3, 4: 2}
ptime[4] = {1: 2, 2: 2, 3: 1, 4: 2} #paperdaki {1: 2, 2: 2, 3: 2, 4: 3}
utilization = 0.8              #given utilization level
       
#Given utilization calculate mean interarrival time for problem
t_ptime = 0                    #total process time
t_num_ops = 0                  #total number of operations
for j in range(1, num_job_types+1):
    t_num_ops += len(sequence[j])
    for s in range(1, len(sequence[j]) + 1):
        t_ptime += ptime[j][s]
m_ptime = 0.0                  #mean process time per operation
m_ptime = float(t_ptime)/float(t_num_ops)
m_num_op_per_job = 0.0         #mean number of operations per job
m_num_op_per_job = float(t_num_ops)/float(num_job_types)
Mean_i = 0.0                   #calculated mean inter-arrival 
Mean_i = float(m_ptime * m_num_op_per_job)/float(utilization * num_machines)
del j, s, m_ptime, m_num_op_per_job, t_ptime, t_num_ops

class Job_Shop:
    def __init__(self): 
                
        #A. Initialization for simulation
        
        #A1. Set simulation parameters
        self.clock = 0.0                    #simulation clock set to 0
        self.jobs_total = 11000              #number of total jobs simulated
        self.jobs_warmup = 1000              #number of jobs for warm up
        
        #A2. Initalize system state
        self.num_in_system = 0              #current number in system
        self.m1_state = 0                   #current state of machine 1 (0-1)
        self.m2_state = 0                   #current state of machine 2 (0-1)
        self.m3_state = 0                   #current state of machine 3 (0-1)
        self.m4_state = 0                   #current state of machine 4 (0-1)
        self.m1_queue = []                  #current queue of machine 1
        self.m2_queue = []                  #current queue of machine 2
        self.m3_queue = []                  #current queue of machine 3
        self.m4_queue = []                  #current queue of machine 4
        self.m1_num_in_q = 0                #current number in queue of m/c 1
        self.m2_num_in_q = 0                #current number in queue of m/c 2
        self.m3_num_in_q = 0                #current number in queue of m/c 3
        self.m4_num_in_q = 0                #current number in queue of m/c 4
        self.m1_current_job = 0             #current job no processed in m/c 1
        self.m2_current_job = 0             #current job no processed in m/c 2
        self.m3_current_job = 0             #current job no processed in m/c 3
        self.m4_current_job = 0             #current job no processed in m/c 4
        self.current_job_completed = 0      #current job no completed
        
        #A3. Initialize statistical counters/variables
        self.num_departures = 0             #number of jobs finished 
        self.num_arrivals = 0               #total number of arrivals
        self.sum_ptime_m1 = 0               #sum of process times by machine 1
        self.sum_ptime_m2 = 0               #sum of process times by machine 2
        self.sum_ptime_m3 = 0               #sum of process times by machine 3
        self.sum_ptime_m4 = 0               #sum of process times by machine 4
        self.total_wtime_q_m1 = 0.0         #total wait time in queue of m/c 1
        self.total_wtime_q_m2 = 0.0         #total wait time in queue of m/c 2
        self.total_wtime_q_m3 = 0.0         #total wait time in queue of m/c 3
        self.total_wtime_q_m4 = 0.0         #total wait time in queue of m/c 4
        self.num_completed_m1 = 0        #number of jobs comleted by m/c 1
        self.num_completed_m2 = 0        #number of jobs comleted by m/c 2
        self.num_completed_m3 = 0        #number of jobs comleted by m/c 3
        self.num_completed_m4 = 0        #number of jobs comleted by m/c 4
        
        #A4. Initialize job shop related variables for data mining
        self.sum_of_remain_time = 0       #sum of remaining process time
        self.sum_of_remain_time_m1 = 0    #sum of remaining process time m1
        self.sum_of_remain_time_m2 = 0    #sum of remaining process time m2
        self.sum_of_remain_time_m3 = 0    #sum of remaining process time m3
        self.sum_of_remain_time_m4 = 0    #sum of remaining process time m4
                   
        #A5. Generate the initial events and put them in event list
        self.t_arrival = self.gen_int_arr() #time of next arrival
        self.t_departure1 = float('inf')    #departure time from machine 1
        self.t_departure2 = float('inf')    #departure time from machine 2
        self.t_departure3 = float('inf')    #departure time from machine 3
        self.t_departure4 = float('inf')    #departure time from machine 4
                
        #A6. Initialize statistical counters/variables for warm_up period
        self.num_departures_w = 0        #number of jobs finished 
        self.num_arrivals_w = 0             #total number of arrivals
        self.sum_ptime_m1_w = 0             #sum of process times by machine 1
        self.sum_ptime_m2_w = 0             #sum of process times by machine 2
        self.sum_ptime_m3_w = 0             #sum of process times by machine 3
        self.sum_ptime_m4_w = 0             #sum of process times by machine 4
        self.total_wait_time_q_m1_w = 0.0   #total wait time in queue of m/c 1
        self.total_wait_time_q_m2_w = 0.0   #total wait time in queue of m/c 2
        self.total_wait_time_q_m3_w = 0.0   #total wait time in queue of m/c 3
        self.total_wait_time_q_m4_w = 0.0   #total wait time in queue of m/c 4
        self.num_completed_m1_w = 0      #number of jobs comleted by m/c 1
        self.num_completed_m2_w = 0      #number of jobs comleted by m/c 2
        self.num_completed_m3_w = 0      #number of jobs comleted by m/c 3
        self.num_completed_m4_w = 0      #number of jobs comleted by m/c 4
        
        #B. Define dictionary for attributes of entities/jobs
        self.jobs = {}
        for j in range(1, ceil(self.jobs_total*(1.01))+1):
            self.jobs[j] = {}
            #Job related attributes
            self.jobs[j]['JobNumber'] = j
            self.jobs[j]['TimeIn'] = 0.0
            self.jobs[j]['Type'] = 0
            self.jobs[j]['m1_PrTime'] = 0.0
            self.jobs[j]['m2_PrTime'] = 0.0
            self.jobs[j]['m3_PrTime'] = 0.0
            self.jobs[j]['m4_PrTime'] = 0.0
            self.jobs[j]['ThMinFlowTime'] = 0.0 
            self.jobs[j]['CompletedNumOps'] = 0
            self.jobs[j]['NextOp'] = 0
            #Job shop related attributes at the time of the arrival
            self.jobs[j]['JS_SumOfRemainTime'] = 0.0
            self.jobs[j]['JS_SumOfRemainTime_m1'] = 0.0
            self.jobs[j]['JS_SumOfRemainTime_m2'] = 0.0
            self.jobs[j]['JS_SumOfRemainTime_m3'] = 0.0
            self.jobs[j]['JS_SumOfRemainTime_m4'] = 0.0
            self.jobs[j]['JS_LenQueue_m1'] = 0.0
            self.jobs[j]['JS_LenQueue_m2'] = 0.0
            self.jobs[j]['JS_LenQueue_m3'] = 0.0
            self.jobs[j]['JS_LenQueue_m4'] = 0.0
            self.jobs[j]['WIP'] = 0.0
            #Attributes tallied as the job is completed
            self.jobs[j]['FlowTime'] = 0.0
            self.jobs[j]['k'] = 0.0
            #print(self.jobs[j])
        
    def time_adv(self):      
        
        #Find the time of imminent event
        next_events = []
        next_events.append(self.t_arrival)
        next_events.append(self.t_departure1)
        next_events.append(self.t_departure2)
        next_events.append(self.t_departure3)
        next_events.append(self.t_departure4)
        t_next_event = min(next_events)
        #print(next_events, t_next_event)
        
        #Find the imminent event (0: arrival, 1: departure from m/c 1, ...)
        next_event = next_events.index(t_next_event) 
                                                         
        #Update time-weighted statistics
        self.total_wtime_q_m1 += (self.m1_num_in_q*(t_next_event - self.clock))
        self.total_wtime_q_m2 += (self.m2_num_in_q*(t_next_event - self.clock))
        self.total_wtime_q_m3 += (self.m3_num_in_q*(t_next_event - self.clock))
        self.total_wtime_q_m4 += (self.m4_num_in_q*(t_next_event - self.clock))
        
        #Advance simulation clock to the time of the imminent event
        self.clock = t_next_event
             
        #Execute the imminent event
        #print(self.clock, next_event,next_events)# self.t_arrival,self.t_departure1,self.t_departure2,self.t_departure3,self.t_departure4)
        #print(self.m1_state, self.m1_queue, self.m2_state, self.m2_queue, self.m3_state, self.m3_queue, self.m4_state, self.m4_queue)
        if next_event == 0:
           self.arrival()
        if next_event == 1:
           self.machine1()
        if next_event == 2:
           self.machine2()
        if next_event == 3:
           self.machine3()
        if next_event == 4:
           self.machine4()
        
    def arrival(self):   
        
        #Update system state   
        self.num_in_system += 1

        #Update statistical counter for arrivals      
        self.num_arrivals += 1
        
        j = self.num_arrivals #Set job number using number of jobs arrived
        #print('------', j)
        
        #Determine job type and the machine of its first operation attributes           
        self.jobs[j]['Type'] = np.random.choice([1,2,3,4])
        #random.choice(array, size=None for 1, replace=True, p=None for equal)
        self.jobs[j]['NextOp'] = sequence[self.jobs[j]['Type']][1]
        m = self.jobs[j]['NextOp']
        
        #Assign other job related attributes
        self.jobs[j]['JobNumber'] = j
        self.jobs[j]['TimeIn'] = self.clock
        self.jobs[j]['m1_PrTime'] = ptime[self.jobs[j]['Type']][1]
        self.jobs[j]['m2_PrTime'] = ptime[self.jobs[j]['Type']][2]
        self.jobs[j]['m3_PrTime'] = ptime[self.jobs[j]['Type']][3]
        self.jobs[j]['m4_PrTime'] = ptime[self.jobs[j]['Type']][4]
        self.jobs[j]['ThMinFlowTime'] = ptime[self.jobs[j]['Type']][1] \
                                      + ptime[self.jobs[j]['Type']][2] \
                                      + ptime[self.jobs[j]['Type']][3] \
                                      + ptime[self.jobs[j]['Type']][4] 
        self.jobs[j]['CompletedNumOps'] = 0
        
        #Assign job shop related attributes at the time of the arrival
        self.jobs[j]['JS_SumOfRemainTime'] = self.sum_of_remain_time
        self.jobs[j]['JS_SumOfRemainTime_m1']= self.sum_of_remain_time_m1
        self.jobs[j]['JS_SumOfRemainTime_m2']= self.sum_of_remain_time_m2
        self.jobs[j]['JS_SumOfRemainTime_m3']= self.sum_of_remain_time_m3
        self.jobs[j]['JS_SumOfRemainTime_m4']= self.sum_of_remain_time_m4
        self.jobs[j]['JS_LenQueue_m1'] = len(self.m1_queue) 
        self.jobs[j]['JS_LenQueue_m2'] = len(self.m2_queue)
        self.jobs[j]['JS_LenQueue_m3'] = len(self.m3_queue)
        self.jobs[j]['JS_LenQueue_m4'] = len(self.m4_queue)
        
        WIP = self.m1_state + self.m3_state + self.m3_state + self.m4_state
        WIP += len(self.m1_queue) + len(self.m2_queue)
        WIP += len(self.m3_queue) + len(self.m3_queue)
        
        self.jobs[j]['WIP'] = WIP
        
        #Update job shop variables due to new arriving job
        self.sum_of_remain_time += self.jobs[j]['ThMinFlowTime']
        self.sum_of_remain_time_m1 += self.jobs[j]['m1_PrTime']
        self.sum_of_remain_time_m2 += self.jobs[j]['m2_PrTime']
        self.sum_of_remain_time_m3 += self.jobs[j]['m3_PrTime']
        self.sum_of_remain_time_m4 += self.jobs[j]['m4_PrTime']
        
        #Schedule next departure depending on state of job shop
        if m == 1:
           if self.m1_state == 0:        #If machine 1 is idle
              self.m1_state = 1          #Set status of machine as busy
              self.m1_current_job = self.jobs[j]['JobNumber'] #Set current job
              self.sum_ptime_m1 += self.jobs[j]['m1_PrTime'] 
              self.t_departure1 = self.clock + self.jobs[j]['m1_PrTime'] 
           else: #If machine 1 is busy add to the queue
              self.m1_num_in_q += 1 #Actually redundant but let's keep it
              self.m1_queue.append(self.jobs[j]['JobNumber'])
        
        if m == 2:
           if self.m2_state == 0:        #If machine 2 is idle
              self.m2_state = 1          #Set status of machine as busy
              self.m2_current_job = self.jobs[j]['JobNumber'] #Set current job
              self.sum_ptime_m2 += self.jobs[j]['m2_PrTime'] 
              self.t_departure2 = self.clock + self.jobs[j]['m2_PrTime'] 
           else: #If machine 2 is busy add to the queue
              self.m2_num_in_q += 1  #Actually redundant but let's keep it
              self.m2_queue.append(self.jobs[j]['JobNumber'])
        
        if m == 3:
           if self.m3_state == 0:        #If machine 3 is idle
              self.m3_state = 1          #Set status of machine as busy
              self.m3_current_job = self.jobs[j]['JobNumber'] #Set current job
              self.sum_ptime_m3 += self.jobs[j]['m3_PrTime'] 
              self.t_departure3 = self.clock + self.jobs[j]['m3_PrTime'] 
           else: #If machine 3 is busy add to the queue
              self.m3_num_in_q += 1  #Actually redundant but let's keep it
              self.m3_queue.append(self.jobs[j]['JobNumber'])
        
        if m == 4:
           if self.m4_state == 0:        #If machine 4 is idle
              self.m4_state = 1          #Set status of machine as busy
              self.m4_current_job = self.jobs[j]['JobNumber'] #Set current job
              self.sum_ptime_m4 += self.jobs[j]['m4_PrTime'] 
              self.t_departure4 = self.clock + self.jobs[j]['m4_PrTime'] 
           else: #If machine 4 is busy add to the queue
              self.m4_num_in_q += 1  #Actually redundant but let's keep it
              self.m4_queue.append(self.jobs[j]['JobNumber'])
              
        #Schedule next arrival
        self.t_arrival = self.clock + self.gen_int_arr()
        
 
           
    #Completion of job on machine 1            
    def machine1(self): 
        
        self.num_completed_m1 += 1
        
        j = self.m1_current_job
       
        self.sum_of_remain_time -= self.jobs[j]['m1_PrTime']
        self.sum_of_remain_time_m1 -= self.jobs[j]['m1_PrTime']
        self.jobs[j]['CompletedNumOps'] += 1
        n = self.jobs[j]['CompletedNumOps']
        
        if self.jobs[j]['CompletedNumOps'] < len(sequence[self.jobs[j]['Type']]):
           
           self.jobs[j]['NextOp'] = sequence[self.jobs[j]['Type']][n+1]
           m = self.jobs[j]['NextOp']
           """ 
           if m == 1:
              if self.m1_state == 0:        #If machine 1 is idle
                 self.m1_state = 1          #Set status of machine as busy
                 self.m1_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m1 += self.jobs[j]['m1_PrTime'] 
                 self.t_departure1 = self.clock + self.jobs[j]['m1_PrTime'] 
              else: #If machine 1 is busy add to the queue
                 self.m1_num_in_q += 1 #Actually redundant but let's keep it
                 self.m1_queue.append(self.jobs[j]['JobNumber'])
           """
           if m == 2:
              if self.m2_state == 0:        #If machine 2 is idle
                 self.m2_state = 1          #Set status of machine as busy
                 self.m2_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m2 += self.jobs[j]['m2_PrTime'] 
                 self.t_departure2 = self.clock + self.jobs[j]['m2_PrTime'] 
              else: #If machine 2 is busy add to the queue
                 self.m2_num_in_q += 1  #Actually redundant but let's keep it
                 self.m2_queue.append(self.jobs[j]['JobNumber'])
           
           if m == 3:
              if self.m3_state == 0:        #If machine 3 is idle
                 self.m3_state = 1          #Set status of machine as busy
                 self.m3_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m3 += self.jobs[j]['m3_PrTime'] 
                 self.t_departure3 = self.clock + self.jobs[j]['m3_PrTime'] 
              else: #If machine 3 is busy add to the queue
                 self.m3_num_in_q += 1  #Actually redundant but let's keep it
                 self.m3_queue.append(self.jobs[j]['JobNumber'])
           
           if m == 4:
              if self.m4_state == 0:        #If machine 4 is idle
                 self.m4_state = 1          #Set status of machine as busy
                 self.m4_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m4 += self.jobs[j]['m4_PrTime'] 
                 self.t_departure4 = self.clock + self.jobs[j]['m4_PrTime'] 
              else: #If machine 4 is busy add to the queue
                 self.m4_num_in_q += 1  #Actually redundant but let's keep it
                 self.m4_queue.append(self.jobs[j]['JobNumber'])
           
        else:
           self.jobs[j]['NextOp'] = 999
           self.current_job_completed = j
           self.departure() 
        
        #Depending on the existence of queue process next job or become idle
        #if self.m1_num_in_q > 0:
        if len(self.m1_queue) > 0:
            j = self.m1_queue[0]
            self.m1_queue.remove(j)
            self.m1_num_in_q -= 1
            self.m1_current_job = self.jobs[j]['JobNumber'] 
            self.sum_ptime_m1 += self.jobs[j]['m1_PrTime']
            self.t_departure1 = self.clock + self.jobs[j]['m1_PrTime']         
        else:
            self.t_departure1 = float('inf') 
            self.m1_state = 0    
            self.m1_current_job = 0              
    
    #Completion of job on machine 2            
    def machine2(self): 
        
        self.num_completed_m2 += 1
        
        j = self.m2_current_job
        self.sum_of_remain_time -= self.jobs[j]['m2_PrTime']
        self.sum_of_remain_time_m2 -= self.jobs[j]['m2_PrTime']
        self.jobs[j]['CompletedNumOps'] += 1
        n = self.jobs[j]['CompletedNumOps']
        #print(j, n)
        if self.jobs[j]['CompletedNumOps'] < len(sequence[self.jobs[j]['Type']]):
           
           self.jobs[j]['NextOp'] = sequence[self.jobs[j]['Type']][n+1]
           m = self.jobs[j]['NextOp']
           #print(j, n, sequence[self.jobs[j]['Type']], self.m1_queue, self.14_state)
           if m == 1:
              if self.m1_state == 0:        #If machine 1 is idle
                 self.m1_state = 1          #Set status of machine as busy
                 self.m1_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m1 += self.jobs[j]['m1_PrTime'] 
                 self.t_departure1 = self.clock + self.jobs[j]['m1_PrTime'] 
              else: #If machine 1 is busy add to the queue
                 self.m1_num_in_q += 1 #Actually redundant but let's keep it
                 self.m1_queue.append(self.jobs[j]['JobNumber'])
           #print(self.clock, j, n, sequence[self.jobs[j]['Type']], self.m1_queue, self.m1_state, self.m2_queue, self.m2_state, self.m3_queue, self.m3_state, self.m4_queue, self.m4_state)
           """
           if m == 2:
              if self.m2_state == 0:        #If machine 2 is idle
                 self.m2_state = 1          #Set status of machine as busy
                 self.m2_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m2 += self.jobs[j]['m2_PrTime'] 
                 self.t_departure2 = self.clock + self.jobs[j]['m2_PrTime'] 
              else: #If machine 2 is busy add to the queue
                 self.m2_num_in_q += 1  #Actually redundant but let's keep it
                 self.m2_queue.append(self.jobs[j]['JobNumber'])
           """
           if m == 3:
              if self.m3_state == 0:        #If machine 3 is idle
                 self.m3_state = 1          #Set status of machine as busy
                 self.m3_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m3 += self.jobs[j]['m3_PrTime'] 
                 self.t_departure3 = self.clock + self.jobs[j]['m3_PrTime'] 
              else: #If machine 3 is busy add to the queue
                 self.m3_num_in_q += 1  #Actually redundant but let's keep it
                 self.m3_queue.append(self.jobs[j]['JobNumber'])
           
           if m == 4:
              if self.m4_state == 0:        #If machine 4 is idle
                 self.m4_state = 1          #Set status of machine as busy
                 self.m4_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m4 += self.jobs[j]['m4_PrTime'] 
                 self.t_departure4 = self.clock + self.jobs[j]['m4_PrTime'] 
              else: #If machine 4 is busy add to the queue
                 self.m4_num_in_q += 1  #Actually redundant but let's keep it
                 self.m4_queue.append(self.jobs[j]['JobNumber'])
           
        else:
           self.jobs[j]['NextOp'] = 999
           self.current_job_completed = j
           self.departure() 
        
        #Depending on the existence of queue process next job or become idle
        #if self.m2_num_in_q > 0:
        if len(self.m2_queue) > 0:
            j = self.m2_queue[0]
            self.m2_queue.remove(j)
            self.m2_num_in_q -= 1
            self.m2_current_job = self.jobs[j]['JobNumber'] 
            self.sum_ptime_m2 += self.jobs[j]['m2_PrTime']
            self.t_departure2 = self.clock + self.jobs[j]['m2_PrTime']         
        else:
            self.t_departure2 = float('inf') 
            self.m2_state = 0    
            self.m2_current_job = 0                      
    
    #Completion of job on machine 3            
    def machine3(self): 
        
        self.num_completed_m3 += 1
        
        j = self.m3_current_job
        self.sum_of_remain_time -= self.jobs[j]['m3_PrTime']
        self.sum_of_remain_time_m3 -= self.jobs[j]['m3_PrTime']
        self.jobs[j]['CompletedNumOps'] += 1
        n = self.jobs[j]['CompletedNumOps']
        
        if self.jobs[j]['CompletedNumOps'] < len(sequence[self.jobs[j]['Type']]):
           
           self.jobs[j]['NextOp'] = sequence[self.jobs[j]['Type']][n+1]
           m = self.jobs[j]['NextOp']
           
           if m == 1:
              if self.m1_state == 0:        #If machine 1 is idle
                 self.m1_state = 1          #Set status of machine as busy
                 self.m1_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m1 += self.jobs[j]['m1_PrTime'] 
                 self.t_departure1 = self.clock + self.jobs[j]['m1_PrTime'] 
              else: #If machine 1 is busy add to the queue
                 self.m1_num_in_q += 1 #Actually redundant but let's keep it
                 self.m1_queue.append(self.jobs[j]['JobNumber'])
           
           if m == 2:
              if self.m2_state == 0:        #If machine 2 is idle
                 self.m2_state = 1          #Set status of machine as busy
                 self.m2_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m2 += self.jobs[j]['m2_PrTime'] 
                 self.t_departure2 = self.clock + self.jobs[j]['m2_PrTime'] 
              else: #If machine 2 is busy add to the queue
                 self.m2_num_in_q += 1  #Actually redundant but let's keep it
                 self.m2_queue.append(self.jobs[j]['JobNumber'])
           """
           if m == 3:
              if self.m3_state == 0:        #If machine 3 is idle
                 self.m3_state = 1          #Set status of machine as busy
                 self.m3_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m3 += self.jobs[j]['m3_PrTime'] 
                 self.t_departure3 = self.clock + self.jobs[j]['m3_PrTime'] 
              else: #If machine 3 is busy add to the queue
                 self.m3_num_in_q += 1  #Actually redundant but let's keep it
                 self.m3_queue.append(self.jobs[j]['JobNumber'])
           """
           if m == 4:
              if self.m4_state == 0:        #If machine 4 is idle
                 self.m4_state = 1          #Set status of machine as busy
                 self.m4_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m4 += self.jobs[j]['m4_PrTime'] 
                 self.t_departure4 = self.clock + self.jobs[j]['m4_PrTime'] 
              else: #If machine 4 is busy add to the queue
                 self.m4_num_in_q += 1  #Actually redundant but let's keep it
                 self.m4_queue.append(self.jobs[j]['JobNumber'])
           
        else:
           self.jobs[j]['NextOp'] = 999
           self.current_job_completed = j
           self.departure() 
        
        #Depending on the existence of queue process next job or become idle
        #if self.m3_num_in_q >0:
        if len(self.m3_queue) > 0:
            j = self.m3_queue[0]
            self.m3_queue.remove(j)
            self.m3_num_in_q -= 1
            self.m3_current_job = self.jobs[j]['JobNumber'] 
            self.sum_ptime_m3 += self.jobs[j]['m3_PrTime']
            self.t_departure3 = self.clock + self.jobs[j]['m3_PrTime']         
        else:
            self.t_departure3 = float('inf') 
            self.m3_state = 0    
            self.m3_current_job = 0    
    
    #Completion of job on machine 4            
    def machine4(self): 
        
        self.num_completed_m4 += 1
        
        j = self.m4_current_job
        self.sum_of_remain_time -= self.jobs[j]['m4_PrTime']
        self.sum_of_remain_time_m4 -= self.jobs[j]['m4_PrTime']
        self.jobs[j]['CompletedNumOps'] += 1
        n = self.jobs[j]['CompletedNumOps']
        
        if self.jobs[j]['CompletedNumOps'] < len(sequence[self.jobs[j]['Type']]):
           
           self.jobs[j]['NextOp'] = sequence[self.jobs[j]['Type']][n+1]
           m = self.jobs[j]['NextOp']
           
           if m == 1:
              if self.m1_state == 0:        #If machine 1 is idle
                 self.m1_state = 1          #Set status of machine as busy
                 self.m1_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m1 += self.jobs[j]['m1_PrTime'] 
                 self.t_departure1 = self.clock + self.jobs[j]['m1_PrTime'] 
              else: #If machine 1 is busy add to the queue
                 self.m1_num_in_q += 1 #Actually redundant but let's keep it
                 self.m1_queue.append(self.jobs[j]['JobNumber'])
           
           if m == 2:
              if self.m2_state == 0:        #If machine 2 is idle
                 self.m2_state = 1          #Set status of machine as busy
                 self.m2_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m2 += self.jobs[j]['m2_PrTime'] 
                 self.t_departure2 = self.clock + self.jobs[j]['m2_PrTime'] 
              else: #If machine 2 is busy add to the queue
                 self.m2_num_in_q += 1  #Actually redundant but let's keep it
                 self.m2_queue.append(self.jobs[j]['JobNumber'])
           
           if m == 3:
              if self.m3_state == 0:        #If machine 3 is idle
                 self.m3_state = 1          #Set status of machine as busy
                 self.m3_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m3 += self.jobs[j]['m3_PrTime'] 
                 self.t_departure3 = self.clock + self.jobs[j]['m3_PrTime'] 
              else: #If machine 3 is busy add to the queue
                 self.m3_num_in_q += 1  #Actually redundant but let's keep it
                 self.m3_queue.append(self.jobs[j]['JobNumber'])
           """
           if m == 4:
              if self.m4_state == 0:        #If machine 4 is idle
                 self.m4_state = 1          #Set status of machine as busy
                 self.m4_current_job = self.jobs[j]['JobNumber'] #Set cur job
                 self.sum_ptime_m4 += self.jobs[j]['m4_PrTime'] 
                 self.t_departure4 = self.clock + self.jobs[j]['m4_PrTime'] 
              else: #If machine 4 is busy add to the queue
                 self.m4_num_in_q += 1  #Actually redundant but let's keep it
                 self.m4_queue.append(self.jobs[j]['JobNumber'])
           """
        else:
           self.jobs[j]['NextOp'] = 999
           self.current_job_completed = j
           self.departure() 
        
        #Depending on the existence of queue process next job or become idle
        #if self.m4_num_in_q > 0:
        if len(self.m4_queue) > 0:
            j = self.m4_queue[0]
            self.m4_queue.remove(j)
            self.m4_num_in_q -= 1
            self.m4_current_job = self.jobs[j]['JobNumber'] 
            self.sum_ptime_m4 += self.jobs[j]['m4_PrTime']
            self.t_departure4 = self.clock + self.jobs[j]['m4_PrTime']         
        else:
            self.t_departure4 = float('inf') 
            self.m4_state = 0    
            self.m4_current_job = 0    
    
    def departure(self):
        
        self.num_in_system -= 1
        self.num_departures += 1
        
        if self.num_departures == self.jobs_warmup:
           self.num_departures_w = self.num_departures       
           self.num_arrivals_w = self.num_arrivals           
           self.sum_ptime_m1_w = self.sum_ptime_m1
           self.sum_ptime_m2_w = self.sum_ptime_m2
           self.sum_ptime_m3_w = self.sum_ptime_m3
           self.sum_ptime_m4_w = self.sum_ptime_m4
           self.total_wtime_q_m1_w = self.total_wtime_q_m1
           self.total_wtime_q_m2_w = self.total_wtime_q_m2
           self.total_wtime_q_m3_w = self.total_wtime_q_m3
           self.total_wtime_q_m4_w = self.total_wtime_q_m4
           self.num_completed_m1_w = self.num_completed_m1
           self.num_completed_m2_w = self.num_completed_m2
           self.num_completed_m3_w = self.num_completed_m3
           self.num_completed_m4_w = self.num_completed_m4
      
        
        j = self.current_job_completed
        self.jobs[j]['FlowTime'] = self.clock - self.jobs[j]['TimeIn']
        
        self.jobs[j]['k'] = float(self.jobs[j]['FlowTime']) /   \
                            float(self.jobs[j]['ThMinFlowTime'])
        self.current_job_completed = 0
        
        
        
        #print(j, self.jobs[j]['JobNumber'],self.jobs[j]['Type'])     
        #if (self.num_departures > self.jobs_warmup):
        fdm = open("filefordatamining.dat","a")
        if(self.num_departures > self.jobs_warmup):
            print('{18:4d} {17:11.2f} {0:6d} {1:11.2f} '
                      '{2:3d} {3:7d} '                  
                      '{4:5d} {5:5d} '
                      '{6:5d} {7:5d} '
                      '{8:4d} {9:6d} '
                      '{10:11d} '
                      '{11:11d} '
                      '{12:11d} '
                      '{13:11d} '
                      '{14:11d} '
                      '{15:11.2f} {16:14.4f} '
                      '{19:6d} {20:6d} '
                      '{21:6d} {22:6d} '
                      '{23:7d}'.format(
                      self.jobs[j]['JobNumber'], self.jobs[j]['TimeIn'],
                      self.jobs[j]['Type'], self.jobs[j]['ThMinFlowTime'],
                      self.jobs[j]['m1_PrTime'], self.jobs[j]['m2_PrTime'],
                      self.jobs[j]['m3_PrTime'], self.jobs[j]['m4_PrTime'],
                      self.jobs[j]['CompletedNumOps'], self.jobs[j]['NextOp'],
                      self.jobs[j]['JS_SumOfRemainTime'],
                      self.jobs[j]['JS_SumOfRemainTime_m1'],
                      self.jobs[j]['JS_SumOfRemainTime_m2'],
                      self.jobs[j]['JS_SumOfRemainTime_m3'],
                      self.jobs[j]['JS_SumOfRemainTime_m4'],
                      self.jobs[j]['FlowTime'], self.jobs[j]['k'],
                      self.clock, rep_num,
                      self.jobs[j]['JS_LenQueue_m1'],  
                      self.jobs[j]['JS_LenQueue_m2'],
                      self.jobs[j]['JS_LenQueue_m3'],
                      self.jobs[j]['JS_LenQueue_m4'],
                      self.jobs[j]['WIP']), file = fdm)
             
        fdm.close()
          
    #Function to generate arrival times using inverse transform of exponential
    def gen_int_arr(self): 
        return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * Mean_i)
        #return (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 3)
        
    
s=Job_Shop()
df=pd.DataFrame(columns=['Average interarrival time',
                         'Average time on m/c 1',
                         'Average time on m/c 2',
                         'Average time on m/c 3',
                         'Average time on m/c 4',
                         'Utilization of m/c 1',
                         'Utilization of m/c 2',
                         'Utilization of m/c 3',
                         'Utilization of m/c 4'])

fdm = open("filefordatamining.dat","a")
print('RepN    SimClock JobNum      TimeIn Type ThMinT    m1    m2    m3    m4\
   CO  NextO         SRT        SRT1        SRT2        SRT3        SRT4\
          FT              k    nQ1    nQ2    nQ3    nQ4     WIP', file = fdm)
fdm.close()
num_replication = 10

for rep_num in range(num_replication):
    np.random.seed(rep_num)
    s.__init__()
    #while s.clock <= 240 :
    #    s.time_adv() 
    
    while s.num_departures < s.jobs_total:
       s.time_adv()
    #print(s.num_completed_m1,s.num_completed_m2,s.num_completed_m3,s.num_completed_m4)   
    #print(s.m1_queue, s.m2_queue, s.m3_queue, s.m4_queue)
    a=pd.Series([s.clock/s.num_arrivals,
                 s.sum_ptime_m1/s.num_completed_m1,
                 s.sum_ptime_m2/s.num_completed_m2,
                 s.sum_ptime_m3/s.num_completed_m3,
                 s.sum_ptime_m4/s.num_completed_m4,
                 s.sum_ptime_m1/s.clock,
                 s.sum_ptime_m2/s.clock,
                 s.sum_ptime_m3/s.clock,
                 s.sum_ptime_m4/s.clock],
                index=df.columns)
    df=df.append(a,ignore_index=True)   

    
df.to_excel('results.xlsx')   
