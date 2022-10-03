from Process import Process
import numpy as n
from random import *
import time as t
processes,time,incomingProcesses,runningProcess=[],0,[],None
averageWaitingTime=0
types ={
    'FCFS': 'FCFS',
    'SJF': 'SJF'
}
file=open('Algorithms_out_test.txt','a')
# generate array of processes with random burst and arrival times
def generate(length = 6, averageBurstTime = 5, standardDeviation = 1):
    global file
    #generate array of random numbers with given mean and standard deviation
    burstTimes=n.random.normal(averageBurstTime,standardDeviation,length)
    processes.append(Process(0,round(burstTimes[0]),1))#first process with arrivalTime 0
    for number,time in enumerate(n.delete(burstTimes,0)):
        processes.append(Process(
            randint(1,length-1),
            round(time),
            number+2
        ))
    for x in processes:
        file.write("\nProcess {}, arrivalTime: {}ms, burstTime: {}ms\n".format(x.number,x.arrivalTime,x.burstTime))
    file.write('****************************************\n\n')
    return processes

def helper(process):
    global incomingProcesses
    #check if some processes are coming, if yes - push to incoming processes and remove from processes 
    if (process.burstTime<=0): raise Exception('Burst time of process must be more than 0')
    if (process.arrivalTime == time): incomingProcesses.append(process)
    return process.arrivalTime != time

#Simulations
def simulation(type = types['FCFS']):
    global processes,averageWaitingTime,runningProcess,time,incomingProcesses,file
    length=len(processes)
    if (type==types['FCFS']): file.write('\n\"FCFS\"\n')
    else: file.write('\n\"SJF\"\n')
    
    while (len(processes) or len(incomingProcesses)):
        processes=list(filter(helper,processes))
        
        if(type==types['SJF']):#sort by burst time if type equal SJF
           incomingProcesses.sort(key=lambda x: x.burstTime )
        #if the array of runningProcess is free - start run first process from incoming processes
        if (not runningProcess and len(incomingProcesses)):
            runningProcess = {
                'process': incomingProcesses[0],
                'waitingTime': time - incomingProcesses[0].arrivalTime,
                'startTime': time
            }

            averageWaitingTime+=runningProcess['waitingTime']
            printProcess(runningProcess)

        time+=1#plus 1s to real time
        t.sleep(1)#sleep for 1s
        #If running process is ended - remove from incoming processes and make ruuningProcess free
        if (runningProcess and (time - runningProcess['startTime'])==runningProcess['process'].burstTime):
             printProcess(runningProcess,False)
             incomingProcesses.remove(runningProcess['process'])
             runningProcess=None
    file.write("\nTotal processes time: {} ms".format(time))
    file.write("\nTotal waiting time of processes: {} ms".format(averageWaitingTime))
    averageWaitingTime/=length
    file.write("\nAn average waiting time of all processes: {} ms\n\n".format(round(averageWaitingTime,2)))
    file.close()
    
def printProcess(process,isStart=True):#prints the final parametrs of all processes
    sign="\n****************************************\n"
    answer='Start' if isStart else 'Finish'
    answer+=' process {},'.format(process['process'].number)
    answer+=' time: {} ms,'.format(time)
    answer+=' waitingTime: {} ms\n'.format(process['waitingTime']) if isStart else ' burstTime: {} ms{}\n'.format(time-process['startTime'],sign)
    file.write(answer)
    
