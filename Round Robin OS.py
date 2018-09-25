from decimal import Decimal as D

Name = []
Arrival_Time = {}
Execution_Time = {}
IO_Interrupt = {}    
IO_Period = {}

#Import the data from txt file
file = open("processes.txt" , 'r')
for line in file :
    l = line.strip().split(" ")
    if(l[0] != "x") :
        Name.append(l[0])
        Arrival_Time[l[0]] = float(l[1])
        Execution_Time[l[0]] = float(l[2])
        IO_Interrupt[l[0]] = float(l[3])
        IO_Period[l[0]] = float(l[4])
file.close()

Processes_Number = len(Name)

#Modfy the refrence from previous process to 0 sec
for i in range(1,4) :
    Arrival_Time[Name[i]] += Arrival_Time[Name[i-1]]


Time = -0.1             #Total Time
                        #Time slice = 0.1 sec
                        #Note : This initial value as the Time variable is updated at the first of the while loop

Queue = []              #List has the processes that arrived and still in progress

Execution_Done = {}     #How much time has each process been in CPU ( Total Time in CPU )
IO_Done = {}            #How much time has each process been in I\O ( Only the current time in IO )
CPU_IO = {}             #Flag for each process ( 1 -> In CPU \\ 0 -> In I\O )
First_Execute = {}      #The time at which each process entered the CPU for the first time
Finish = {}             #The time at which each process is terminated 
#Intializing the first 3 Dictionaries
for P in Name :
    Execution_Done[P] = 0
    IO_Done[P] = 0
    CPU_IO[P] = 1


def Check_Arrival() :
    for P in Arrival_Time :
        if Time == Arrival_Time[P] :
            Queue.append(P)
            #print("-------------------------------------")     #For Debugging
            #print("Time : " + str(Time))                       #For Debugging
            #print(P + " has been arrived.")                    #For Debugging
            #print("-------------------------------------")     #For Debugging

def Execution() :
    for P in Queue :
        if CPU_IO[P] == 1 and Time != Arrival_Time[P]:
            if P not in First_Execute :
                First_Execute[P] = round(Time-0.1 , 1)
                
            #print("Process in progress : " + P)                        #For Debugging
            Execution_Done[P] = round(Execution_Done[P]+0.1 , 1)
            #print(P + " Execution time : " + str(Execution_Done[P]))   #For Debugging
            Queue.remove(P)
            Queue.append(P)
            

            if Execution_Done[P] == Execution_Time[P] :
                print("-------------------------------------")
                print("Process " + P + " has been completed after " + str(Time) + " sec.")
                print("-------------------------------------")
                Index = Queue.index(P)
                del Queue[Index]
                Finish[P] = Time
                global Processes_Number
                Processes_Number -= 1

            if round(D(str(Execution_Done[P])) % D(str(IO_Interrupt[P])) , 1) == 0 and Execution_Done[P] != 0 and P in Queue:
                
                #print("Process " + P + " is triggered to I\O state at Time : " + str(Time))        #For Debugging
                IO_Done[P] = round(IO_Done[P]-0.1 , 1)
                CPU_IO[P] = 0
                
            break

def IO() :
    for P in Queue :
        if CPU_IO[P] == 0:
            IO_Done[P] = round(IO_Done[P]+0.1 , 1)
            #print(P + " I\O time : " + str(IO_Done[P]))        #For Debugging

            if IO_Done[P] - IO_Period[P] == 0 and IO_Done[P] != 0 :
                    #print("Process " + P + " is triggered to CPU state at Time : " + str(Time))        #For Debugging
                    IO_Done[P] = 0
                    CPU_IO[P] = 1

while Processes_Number != 0 :
    Time = round(Time+0.1 , 1)
    #print("\nTime : " + str(Time))     #For Debugging
    
    Check_Arrival()

    Execution()

    IO()
