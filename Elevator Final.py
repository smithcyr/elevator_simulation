import Queue
from random import randint,random
from operator import mul
from time import clock

# Run the simulation how many times?
Trials = 1000
FilePath = "/home/smithcyr/Courses/MAT 306/Project 5/Specific Runs/"
# Constants
###############
#~ ElevatorGroups = [range(1,26),range(25,51)]
#~ FloorSpecification = [1,1,1,1,2,2,2,2]
ArrivalSeparation = (1,30) # the time between passenger arrivals (min, max) seconds
#~ floors = 50  # number of floors in the building
#~ Elevator_Wait_Time = 5 # number of seconds an elevator waits before leaving
#~ TransitionTime = 4 # how long it takes for the elevator to rise one floor
#~ CAPACITY = 12 # number of people an elevator can hold
DOORTIME = 5 # the amount of time it takes to open or close the doors of the elevator
LOADINGTIME = 3 # the time it takes to get in or out of an elevator
#~ FloorProbability = [1]*(floors-1)#[1,1,1,1,1,1,1,1,2,3,4] # Probability of going to each floor from min + 1 to max
#~ NumElevators = len(FloorSpecification)# number of elevators in the building (USELESS RIGHT NOW)
STARTTIME = clock() # used for judging time to complete trials
###############
ITERCOUNTER = 0


# CLASS passenger has four variables
# arrival - the arrival time in seconds
# elevatorTime - the amount of time spent in an elevator
# destination - the destination floor
# floor - the person's current floor
# Initialized via command passenger(arrival, destination)
class passenger:
    elevatorTime = 0
    def __init__ (self,arrivaltime,destinationfloor,startingfloor,passengernumber):
        self.arrival = arrivaltime
        self.destination = destinationfloor
        self.floor = startingfloor
        self.number = passengernumber

# CLASS elevator has six variables
# unused - time the elevator is unused
# state - the state of the elevator (loading 'l', waiting 'w', going up 'u', going down 'd', exiting 'e')
# doors - whether the elevator doors are open (0) or closed (1)
# counter - a time counter for events (e.g. floor transition, waiting with an empty queue, etc.)
# basefloor - the lowest floor the elevator can go to
# topfloor  - the highest floor the elevator can go to
# currentfloor - the current floor the elevator is at
# passengers - the number of passengers on the elevator
# queue - where each passenger needs to go
# stops - number of stops the elevator has made
# availablefloors - a set of floors the elevator can service 
# Initialized via elevator(Storage array, floor group, array of groups):

class Elevator:
    def __call__(self,queuearray,group,BottomQueues):
        global floors
        global ElevatorGroups
        global CAPACITY
        self.counter = 0
        self.unused = 0
        self.doors = 0
        self.stops = 0
        self.state = 'w'
        self.queue = queuearray
        self.availablefloors = ElevatorGroups[group-1]
        self.feedqueue = BottomQueues[group-1]
        self.basefloor = min(ElevatorGroups[group-1])
        self.currentfloor = self.basefloor
        self.topfloor = max(ElevatorGroups[group-1])
        for i in range(floors):
            self.queue.append(Queue.LifoQueue(CAPACITY))
    def __init__(self,queuearray,group,BottomQueues):
        global floors
        global ElevatorGroups
        global CAPACITY
        self.counter = 0
        self.unused = 0
        self.doors = 0
        self.stops = 0
        self.state = 'w'
        self.queue = queuearray
        self.availablefloors = ElevatorGroups[group-1]
        self.feedqueue = BottomQueues[group-1]
        self.basefloor = min(ElevatorGroups[group-1])
        self.currentfloor = self.basefloor
        self.topfloor = max(ElevatorGroups[group-1])
        for i in range(floors):
            self.queue.append(Queue.LifoQueue(CAPACITY))
    def SuperReset(self):
        self.counter = 0
        self.unused = 0
        self.doors = 0
        self.state = 'w'
        self.stops = 0
        self.currentfloor = self.basefloor
    def countunused(self):
        self.unused = self.unused + 1
    def changestate(self,s):
        self.state = s
    def opendoors(self):
        self.doors = 0
    def closedoors(self):
        self.doors = 1
    def reset(self):
        self.counter = 0
    def count(self):
        self.counter = self.counter + 1
    def checkabove(self):
        for i in queue[self.currentfloor-1:self.topfloor]:
            if not i.empty():
                return 1
        return 0
    def passengers(self):
        return sum([e.qsize() for e in self.queue])

# Create the queue on floor 1
class floorQueue:
    loading = 0
    def __init__(self,FLOORS,S):
        self.availablefloors = FLOORS
        self.downstairs = Queue.Queue()
        self.servicefloor = S

def QUEUESIZE(F):
    total = 0
    for i in F:
        if i.servicefloor == 1:
            total = total + i.downstairs.qsize()
    return total

def TotalAvailableFloors(floors):
    T = floors
    global ElevatorGroups
    for F in floors[1:len(floors)]:
        for Q in ElevatorGroups:
            if F == min(Q):
                T = T + Q
    return list(set(T))

def floorchooser(I):
    global FloorProbability
    M = 1
    C = len(FloorProbability)
    while M > I:
        M = M - FloorProbability[C-1]
        C = C - 1
    return C + 2

for numfloors in [(50,[8,10,12],[10,6,4]),(75,[10,12,14],[10,5,3])]:
    floors = numfloors[0]
    for EGROUPS in [("split",[range(1,floors/2+1),range(floors/2,floors+1)]),("evenodd",[[1]+map(lambda x: x*2+1,range(1,(floors+1)/2)),[1]+map(lambda x: x*2,range(1,((floors)/2))+[floors/2])]),("normal",[range(1,floors+1)])]:
        ElevatorGroups = EGROUPS[1]
        for els in numfloors[1]:
            FloorSpecification = [1] * (els/2) + [len(ElevatorGroups)] * (els/2)
            NumElevators = els
            for TransitionTime in numfloors[2]:
                for Elevator_Wait_Time in [15,10,5]:
                    for CAPACITY in [20,16,12]:
                        for FloorProbability in [[1]*(floors-1)]:
                            FileName = str(floors)+"_"+EGROUPS[0]+"_"+str(els)+"_"+str(TransitionTime)+"_"+str(Elevator_Wait_Time)+"_"+str(CAPACITY)
                            # DATA VARIABLES
                            # Creating the data stucture to hold our info so we can analyze it
                            #Storage = open("/home/smithcyr/Courses/MAT 306/Project 5/data.csv","w")
                            #Storage = open("/home/cyrus/Mathlan/Courses/MAT 306/Project 5/dataHighDensity.csv","w")
                            #Stats = open("/home/cyrus/Mathlan/Courses/MAT 306/Project 5/statdataHighDensity.csv","w")
                            Storage = open(FilePath+"data"+FileName+".csv","w")
                            Stats = open(FilePath+"statdata"+FileName+".csv","w")
                            f = ""
                            for i in range(NumElevators):
                                f = f + ",Elevator " + str(i+1) + "Usage %,Elevator "+str(i+1)+" Stops"
                            Stats.write("Max Waiting Time,Mean Waiting Time,Max Elevator Time,Mean Elevator Time,Max Total Time,Mean Total Time"+f+",Max Queue Size\n")
                            Storage.write("Waiting Time in Queue,Time Spent in Elevator,Delivery Time,Destination Floor,Enter Time\n")
                            #~ print "storage started" # DEBUGGING
                            FLOORQUEUES = []
                            for group in ElevatorGroups:
                                FLOORQUEUES.append(floorQueue(TotalAvailableFloors(group),min(group)))
                            #~ print "queue's created" # DEBUGGING
                            S = float(sum(FloorProbability))
                            FloorProbability = map(lambda x: x/S,FloorProbability)
                            #~ print "Floor probability created"  # DEBUGGING
                            # Create the Elevator array
                            E = []
                            QUEUES = []
                            #~ print "Elevator and queue arrays reset" # DEBUGGING
                            
                            Size = 0
                            for i in range(NumElevators):
                                QUEUES.append([])
                                E.append(Elevator(QUEUES[i],FloorSpecification[i],FLOORQUEUES))  # create the elevators
                            #~ print "elevator objects created",len(E),"of them" # DEBUGGING
                            #~ ### DEBUGGING
                            #~ for elevator in E:
                                #~ print "Elevator",E.index(elevator),elevator.availablefloors,elevator.feedqueue.availablefloors
                            #~ ###
                            
                            for iterations in range(Trials):
                                Time_Spent_In_Elevator = [] # array for storing info
                                Total_Time = [] # array for info
                                Waiting_Time = [] # info
                                Destination_Floor = [] # destination floor
                                Enter_Time = []
                                stoptime = 0
                                # FUNCTIONING VARIABLES
                                # Randomly choosing the arrival times
                                i = 0 # time counter for arrival time initialization
                                ArrivalTimes = [] # array of arrival times
                                while i < 4800:   # create the random array of arrival times
                                    R = randint(ArrivalSeparation[0],ArrivalSeparation[1])
                                    if i + R > 4800:
                                        break
                                    ArrivalTimes.append(i+R)
                                    i = i + R
                                #~ PASSENGERSET = []
                                #~ print "Arrival Times randomized" # DEBUGGING
                                ArrivalTimes = set(ArrivalTimes) # convert to set for efficient checking
                                endlen = len(ArrivalTimes)
                                #~ print "number of passengers",endlen
                                MaxSize = 0 # maximum queue size
                                #stoptime = 0 # the time at which all elevators return to the starting position
                                ## debugging
                                #~ for elevator in E:#
                                    #~ print len(elevator.queue)#
                                #~ print "T  | S1 f1 p1 c1 | S2 f2 p2 c2 | S3 f3 p3 c3 | S4 f4 p4 c4 | Queue Size"
                                ##
                                PassengerCount = 0
                                #~ print "Starting the simulation" # DEBUGGING
                                for time in range(0,8000):
                                ### debugging
                                    #~ print " "
                                    #~ print time,"|",
                                    #~ for elevator in E:
                                        #~ print elevator.state," ",elevator.currentfloor," ",elevator.passengers()," ",elevator.counter,"|",
                                    #~ for q in FLOORQUEUES:
                                        #~ print q.downstairs.qsize(),
                                ###
                                    #~ # Passenger arrival
                                    if time in ArrivalTimes:   # if a passenger arrives at this time
                                        PassengerCount = PassengerCount + 1
                                        person = passenger(time,floorchooser(random()),1,PassengerCount)
                                        #~ print person.destination,
                                        for I in FLOORQUEUES:
                                            if person.destination in I.availablefloors and I.servicefloor == person.floor:
                                                I.downstairs.put(person)
                                                #~ print I.availablefloors
                                                break
                                        #~ print "Passenger",person.number,",arriving, getting in queue for floor",person.destination
                                        Size = QUEUESIZE(FLOORQUEUES)
                                        if Size > MaxSize:
                                            MaxSize = Size # record a new maximum if so
                                    #~ print "person arrives"
                                    # The stop conditions
                                    if len(Time_Spent_In_Elevator) == endlen and reduce(mul,[e.state == 'w' for e in E]) and reduce(mul,[not e.doors for e in E]):
                                        stoptime = time # record the time the simulation ends at
                                        break
                                    
                                    # the simulation loop
                                    for elevator in E:
                                        if elevator.state == 'w':   # if waiting at the base floor
                                            if elevator.doors:      # open the doors if closed
                                                elevator.count()
                                                if elevator.counter == DOORTIME: # count until DOORTIME
                                                    elevator.opendoors()             # open the doors
                                                    elevator.reset()                 # reset the counter
                                            elif elevator.feedqueue.downstairs.empty():
                                                if elevator.passengers() > 0: # the cars with passengers should leave after Elevator_Wait_Time seconds
                                                    elevator.count()
                                                    if elevator.counter == Elevator_Wait_Time: # if the elevator has waited Elevator_Wait_Time seconds
                                                        elevator.changestate('u') # go up
                                                        elevator.reset()        # reset the counter
                                                else:
                                                    elevator.countunused()      # count the unused time
                                            else:
                                                if not elevator.feedqueue.loading: # if no elevator is loading and there are people waiting to load
                                                    elevator.changestate('l')
                                                    elevator.reset()
                                                    elevator.feedqueue.loading = 1
                                                else:           # if an elevator is already loading
                                                    if elevator.passengers() > 0:  # if the elevator has passengers
                                                        elevator.count()
                                                        if elevator.counter == Elevator_Wait_Time:  # wait till Elevator_Wait_Time and leave
                                                            elevator.changestate('u')
                                                            elevator.reset()
                                                    else:
                                                        elevator.countunused()      # count the unused time
                                        elif elevator.state == 'l':   # the loading state
                                            if elevator.feedqueue.downstairs.empty():  # with no one to load, the elevator is waiting
                                                elevator.changestate('w')
                                                elevator.reset()
                                                elevator.count()
                                                elevator.feedqueue.loading = 0
                                            else:
                                                elevator.count()
                                                if elevator.counter == LOADINGTIME: # it takes 3 seconds for someone to enter the elevator
                                                    #print "before loading", elevator.feedqueue.downstairs.qsize(),elevator.passengers(), # DEBUGGING
                                                    person = elevator.feedqueue.downstairs.get() # take the person out of the queue
                                                    #print "after loading", elevator.feedqueue.downstairs.qsize(),elevator.passengers(), # DEBUGGING
                                                    person.elevatorTime = time # record the time the person entered the elevator
                                                    #print person.destination-1 # DEBUGGING
                                                    buff = elevator.availablefloors[1]
                                                    for i in elevator.availablefloors:
                                                        if person.destination >= i:
                                                            buff = i
                                                        else:
                                                            break
                                                    elevator.queue[buff-1].put(person) # add the person to their destination queue
                                                    #~ print "Psng # ",person.number,", Destination", person.destination, ", exiting at floor",buff,"Of elevator ",E.index(elevator)
                                                    elevator.reset()
                                                    if elevator.passengers() == CAPACITY: # if the elevator is full go up
                                                        elevator.changestate('u')
                                                        elevator.feedqueue.loading = 0
                                                    elif elevator.feedqueue.downstairs.empty():  # with no one to load, the elevator is waiting
                                                        elevator.changestate('w')
                                                        elevator.reset()
                                                        elevator.count()
                                                        elevator.feedqueue.loading = 0
                                        elif elevator.state == 'u':   # going up 
                                            if not elevator.doors: # if the elevator doors are open
                                                elevator.count()
                                                if elevator.counter == DOORTIME: # wait DOORTIME seconds
                                                    elevator.closedoors()
                                                    elevator.reset()
                                            else: 
                                                elevator.count()
                                                if elevator.counter == TransitionTime: # after TransitionTime seconds the floor has changed
                                                    elevator.currentfloor = elevator.currentfloor + 1
                                                    elevator.reset()
                                                    elevator.changestate('e')
                                        elif elevator.state == 'e':   # arriving at a floor and letting people exit if needed       
                                            if elevator.queue[elevator.currentfloor-1].empty():
                                                if elevator.topfloor > elevator.currentfloor and elevator.passengers(): # if no one gets off at this level
                                                    elevator.changestate('u') # and there are still passengers go up
                                                    elevator.count()
                                                else:
                                                    elevator.changestate('d')
                                                    elevator.count()
                                            else:
                                                if elevator.doors:  # if the doors are closed
                                                    #print "doors opening"  #DEBUGGING
                                                    elevator.count()
                                                    if elevator.counter == DOORTIME:
                                                        elevator.reset()
                                                        elevator.opendoors()
                                                        elevator.stops = elevator.stops + 1 # when the elevator opens the doors, record the stop
                                                else:
                                                    elevator.count()
                                                    #print "person exiting," #DEBUGGING
                                                    if elevator.counter == LOADINGTIME:
                                                        #print "Before exiting:",elevator.queue[elevator.currentfloor-1].qsize(),elevator.passengers(), # DEBUGGING
                                                        person = elevator.queue[elevator.currentfloor-1].get()
                                                        person.floor = elevator.currentfloor
                                                        #~ print ""
                                                        #~ print "passenger",person.number,"getting off at floor",person.floor,"heading to floor",person.destination,
                                                        #print "After exiting:",elevator.queue[elevator.currentfloor-1].qsize(),elevator.passengers(),  # DEBUGGING
                                                        #print "Number of people in queue: ",elevator.queue[elevator.currentfloor-1].qsize()
                                                        elevator.reset()
                                                        
                                                        if person.destination == person.floor:
                                                            Enter_Time.append(person.elevatorTime)
                                                            Time_Spent_In_Elevator.append(time - person.elevatorTime) # Data collection
                                                            Total_Time.append(time - person.arrival) # Data collection
                                                            Waiting_Time.append(person.elevatorTime - person.arrival) # Data collection
                                                            Destination_Floor.append(person.destination) # Data collection
                                                            #~ PASSENGERSET.append(person.number)
                                                            #~ print len(Time_Spent_In_Elevator),"/",endlen
                                                        else:
                                                            for I in FLOORQUEUES:
                                                                if I.servicefloor == person.floor and person.destination in I.availablefloors:
                                                                    I.downstairs.put(person)
                                                                    #~ print "entering queue",
                                                                    break
                                                                    
                                        elif elevator.state == 'd':
                                            if not elevator.doors: # if the doors are open
                                                elevator.count()
                                                if elevator.counter == DOORTIME: # close the doors after DOORTIME seconds
                                                    elevator.closedoors() 
                                                    elevator.reset()
                                            elif elevator.currentfloor != elevator.basefloor: 
                                                elevator.count()
                                                if elevator.counter == TransitionTime:
                                                    elevator.currentfloor = elevator.currentfloor - 1
                                                    elevator.reset()
                                            else:
                                                elevator.changestate('w')
                                                elevator.count()
                                                elevator.stops = elevator.stops + 1
                                #print endlen, len(Waiting_Time)
                                f = ""
                                #print time,stoptime                                
                                #~ print set(range(1,endlen)).difference(set(PASSENGERSET))
                                for elevator in E:
                                    f = f + "," + str(1- elevator.unused / float(stoptime))+","+str(elevator.stops)
                                for (i,j,k,l,m) in zip(Waiting_Time,Time_Spent_In_Elevator,Total_Time,Destination_Floor,Enter_Time):
                                    Storage.write(str(i)+","+str(j)+","+str(k)+","+str(l)+","+str(m)+"\n")
                                Stats.write(str(max(Waiting_Time))+","+str(sum(Waiting_Time)/float(len(Waiting_Time)))+","+str(max(Time_Spent_In_Elevator))+","+str(sum(Time_Spent_In_Elevator)/float(len(Time_Spent_In_Elevator)))+","+str(max(Total_Time))+","+str(sum(Total_Time)/float(len(Total_Time)))+f+","+str(MaxSize)+"\n")
                                for elevator in E:
                                    elevator.SuperReset()
                                #~ if not (iterations+1) % 100:
                                    #~ print iterations+1,clock()-STARTTIME
                            ITERCOUNTER = ITERCOUNTER + 1
                            print FileName, "Written",clock() - STARTTIME,"    ", ITERCOUNTER,"out of (",1944,")"
                        
