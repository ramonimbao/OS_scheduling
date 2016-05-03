class Process():
    STATE_NEW = 0
    STATE_READY = 1
    STATE_RUNNING = 2
    STATE_WAITING = 3
    STATE_DONE = 4
    
    def __init__(self, name, cpuBursts, arrivalTime):
        self.name = name
        
        self.cpuBursts = cpuBursts
        self.cpuBurstsLeft = cpuBursts
        
        self.arrivalTime = arrivalTime
        self.arrivalCurrent = 0

        self.processTimeQuantum = 0
        
        self.responseTime = 0
        self.waitingTime = 0
        self.turnaroundTime = 0

        self.state = Process.STATE_READY

    def reset(self):
        self.cpuBurstsLeft = self.cpuBursts

        self.responseTime = 0
        self.waitingTime = 0
        self.turnaroundTime = 0

        self.state = Process.STATE_NEW

    def delay(self):
        self.arrivalCurrent += 1
        self.responseTime += 1
        self.turnaroundTime += 1

    def burst(self):
        self.cpuBurstsLeft -= 1
        self.turnaroundTime += 1

    def wait(self):
        self.waitingTime += 1
        self.turnaroundTime += 1
        if (self.cpuBurstsLeft == self.cpuBursts):
            self.responseTime += 1

def displayOutput(p):
    numProcesses = len(p)
    sumWaitingTime = 0
    sumResponseTime = 0
    sumTurnaroundTime = 0
    
    for i in range(len(p)):
        print(p[i].name)
        print("Waiting time:\t\t" + str(p[i].waitingTime))
        sumWaitingTime += p[i].waitingTime
        print("Response time:\t\t" + str(p[i].responseTime))
        sumResponseTime += p[i].responseTime
        print("Turnaround time:\t" + str(p[i].turnaroundTime))
        sumTurnaroundTime += p[i].turnaroundTime

    print("\nAve. waiting time:\t" + str(sumWaitingTime/float(numProcesses)))
    print("Ave. response time:\t" + str(sumResponseTime/float(numProcesses)))
    print("Ave. turnaround time:\t" + str(sumTurnaroundTime/float(numProcesses)))

def initProcesses():
    p = [Process("P1", 22, 5),
         Process("P2", 18, 5),
         Process("P3", 9, 5),
         Process("P4", 10, 5),
         Process("P5", 5, 5)]
    return p

def FCFS():
    print("/======== FCFS ========/\n")
    p = initProcesses()
    numProcesses = len(p)
    for i in range(numProcesses):
        p[i].reset()
    numProcessesDone = 0
    q = []      # ready queue
    r = None    # currently running process
    currentCycle = 0

    while (numProcessesDone != numProcesses):
        numProcessesDone = 0
        # DEBUG print("STATE CHECK " + p[i].name + ": " + str(p[i].state))
        for i in range(numProcesses):
            if (p[i].state == Process.STATE_NEW):
                if (p[i].arrivalCurrent < p[i].arrivalTime):
                    # DEBUG print(p[i].name + " delayed... " + str(p[i].arrivalTime - p[i].arrivalCurrent) + " cycles left.")
                    p[i].delay()
                else:
                    p[i].state = Process.STATE_READY
                    q.append(p[i])
            if (p[i].state == Process.STATE_DONE):
                # DEBUG print(p[i].name + " done... numProcessesDone: " + str(numProcessesDone))
                numProcessesDone += 1

        for i in range(len(q)):
            if (q[i].state == Process.STATE_READY):
                if (r == None):
                    r = q[i]
                    r.state = Process.STATE_RUNNING
                else:
                    if (r != q[i]):
                        q[i].state = Process.STATE_WAITING

            if (q[i].state == Process.STATE_WAITING):
                if (r == None):
                    r = q[i]
                    r.state = Process.STATE_RUNNING
                else:
                    q[i].wait()
                    # DEBUG print(q[i].name + " waiting... " + str(q[i].waitingTime) + " cycles passed.")

            if (r != None):
                if (r == q[i] and r.cpuBurstsLeft > 0):
                    r.burst()
                    # DEBUG print(r.name + " running... " + str(r.cpuBurstsLeft) + " cycles left.")
                elif (r == q[i] and r.cpuBurstsLeft == 0):
                    r.state = Process.STATE_DONE
                    r = None
        currentCycle += 1
    # DEBUG print("Current cycle: " + str(currentCycle))
    displayOutput(p)

# Execute FCFS
FCFS()

def SJF_NP():
    print("\n/======== SJF NP ========/\n")
    p = initProcesses()
    numProcesses = len(p)
    for i in range(numProcesses):
        p[i].reset()
    numProcessesDone = 0
    q = []      # ready queue
    r = None    # currently running process
    currentCycle = 0

    while (numProcessesDone != numProcesses):
        numProcessesDone = 0
        # DEBUG print("STATE CHECK " + p[i].name + ": " + str(p[i].state))
        for i in range(numProcesses):
            if (p[i].state == Process.STATE_NEW):
                if (p[i].arrivalCurrent < p[i].arrivalTime):
                    # DEBUG print(p[i].name + " delayed... " + str(p[i].arrivalTime - p[i].arrivalCurrent) + " cycles left.")
                    p[i].delay()
                else:
                    p[i].state = Process.STATE_READY
                    q.append(p[i])
            if (p[i].state == Process.STATE_DONE):
                # DEBUG print(p[i].name + " done... numProcessesDone: " + str(numProcessesDone))
                numProcessesDone += 1

        q.sort(key = lambda x: x.cpuBurstsLeft)

        for i in range(len(q)):
            if (q[i].state == Process.STATE_READY):
                if (r == None):
                    r = q[i]
                    r.state = Process.STATE_RUNNING
                else:
                    if (r != q[i]):
                        q[i].state = Process.STATE_WAITING

            if (q[i].state == Process.STATE_WAITING):
                if (r == None):
                    r = q[i]
                    r.state = Process.STATE_RUNNING
                else:
                    q[i].wait()
                    # DEBUG print(q[i].name + " waiting... " + str(q[i].waitingTime) + " cycles passed.")

            if (r != None):
                if (r == q[i] and r.cpuBurstsLeft > 0):
                    r.burst()
                    # DEBUG print(r.name + " running... " + str(r.cpuBurstsLeft) + " cycles left.")
                elif (r == q[i] and r.cpuBurstsLeft == 0):
                    r.state = Process.STATE_DONE
                    r = None
        currentCycle += 1
    # DEBUG print("Current cycle: " + str(currentCycle))
    displayOutput(p)

# Execute SJF_NP
SJF_NP()

def RR(timeQuantum = 5):
    print("\n/======== RR (TQ = " + str(timeQuantum) + ") ========/\n")
    p = initProcesses()
    numProcesses = len(p)
    for i in range(numProcesses):
        p[i].reset()
    numProcessesDone = 0
    q = []      # ready queue
    r = None    # currently running process
    pr = None   # previously running process
    currentCycle = 0

    while (numProcessesDone != numProcesses):
        numProcessesDone = 0
        # DEBUG print("STATE CHECK " + p[i].name + ": " + str(p[i].state))
        for i in range(numProcesses):
            if (p[i].state == Process.STATE_NEW):
                if (p[i].arrivalCurrent < p[i].arrivalTime):
                    # DEBUG print(p[i].name + " delayed... " + str(p[i].arrivalTime - p[i].arrivalCurrent) + " cycles left.")
                    p[i].delay()
                else:
                    p[i].state = Process.STATE_READY
                    p[i].processTimeQuantum = timeQuantum
                    q.append(p[i])
            if (p[i].state == Process.STATE_DONE):
                # DEBUG print(p[i].name + " done... numProcessesDone: " + str(numProcessesDone))
                numProcessesDone += 1

        for i in range(len(q)):
            if (q[i].state == Process.STATE_READY):
                if (r == None):
                    if (pr == None):
                        r = q[i]
                        r.state = Process.STATE_RUNNING
                        r.processTimeQuantum = timeQuantum
                    else:
                        if (pr != q[i]):
                            if (numProcessesDone < numProcesses):
                                pr = r
                            else:
                                r = None
                            r = q[i]
                            r.state = Process.STATE_RUNNING
                else:
                    if (r != q[i]):
                        q[i].state = Process.STATE_WAITING
                        
            if (q[i].state == Process.STATE_WAITING):
                if (r == None):
                    r = q[i]
                    r.state = Process.STATE_RUNNING
                    r.processTimeQuantum = timeQuantum
                else:
                    q[i].wait()
                    # DEBUG print(q[i].name + " waiting... " + str(q[i].waitingTime) + " cycles passed.")

            if (r != None):
                if (r == q[i] and r.cpuBurstsLeft > 0):
                    if (r.processTimeQuantum > 0):
                        r.burst()
                        r.processTimeQuantum -= 1
                        # DEBUG print(r.name + " running... " + str(r.cpuBurstsLeft) + " cycles left.")
                    else:
                        r.state = Process.STATE_WAITING
                        r = None
                elif (r == q[i] and r.cpuBurstsLeft == 0):
                    r.state = Process.STATE_DONE
                    r = None
        currentCycle += 1
    # DEBUG print("Current cycle: " + str(currentCycle))
    displayOutput(p)

# Execute RR with TQ=5
RR(5)




def OptiRR(timeQuantum = 5, multiplier = 2):
    print("\n/======== Optimized RR (TQ = " + str(timeQuantum) + ") ========/\n")
    p = initProcesses()
    numProcesses = len(p)
    for i in range(numProcesses):
        p[i].reset()
    numProcessesDone = 0
    q = [] # Ready queue
    qfcfs = [] # Backup
    r = None # currently running process
    pr = None # previously running process
    currentCycle = 0

    while (numProcessesDone != numProcesses):
        # Restore the backup queue
        #q = qfcfs[:]
        
        # PHASE 1: Run it like a normal RR with specified TQ
        print("PHASE 1")
        for cycle in range(numProcesses * timeQuantum):
            numProcessesDone = 0
            #print("STATE CHECK " + p[i].name + ": " + str(p[i].state))
            for i in range(numProcesses):
                if (p[i].state == Process.STATE_NEW):
                    if (p[i].arrivalCurrent < p[i].arrivalTime):
                        # DEBUG print(p[i].name + " delayed... " + str(p[i].arrivalTime - p[i].arrivalCurrent) + " cycles left.")
                        p[i].delay()
                    else:
                        p[i].state = Process.STATE_READY
                        p[i].processTimeQuantum = timeQuantum
                        q.append(p[i])
                if (p[i].state == Process.STATE_DONE):
                    # DEBUG print(p[i].name + " done... numProcessesDone: " + str(numProcessesDone))
                    numProcessesDone += 1

            for i in range(len(q)):
                if (q[i].state == Process.STATE_READY):
                    if (r == None):
                        if (pr == None):
                            r = q[i]
                            r.state = Process.STATE_RUNNING
                            r.processTimeQuantum = timeQuantum
                        else:
                            if (pr != q[i]):
                                if (numProcessesDone < numProcesses):
                                    pr = r
                                else:
                                    pr = None
                                r = q[i]
                                r.state = Process.STATE_RUNNING
                    else:
                        if (r != q[i]):
                            q[i].state = Process.STATE_WAITING
                            
                if (q[i].state == Process.STATE_WAITING):
                    if (r == None):
                        r = q[i]
                        r.state = Process.STATE_RUNNING
                        r.processTimeQuantum = timeQuantum
                    else:
                        q[i].wait()
                        # DEBUG print(q[i].name + " waiting... " + str(q[i].waitingTime) + " cycles passed.")

                if (r != None):
                    #print("R: " + r.name)
                    if (r == q[i] and r.cpuBurstsLeft > 0):
                        if (r.processTimeQuantum > 0):
                            r.burst()
                            r.processTimeQuantum -= 1
                            # DEBUG print(r.name + " running... " + str(r.cpuBurstsLeft) + " cycles left.")
                        else:
                            r.state = Process.STATE_WAITING
                            pr = r
                            r = None
                    elif (r == q[i] and r.cpuBurstsLeft == 0):
                        r.state = Process.STATE_DONE
                        pr = r
                        r = None

                
            currentCycle += 1

        # make a backup of the FCFS queue
        #qfcfs = q[:]
        # sort the processes with SJF
        qbackup = q[:]
        
        for i in range(len(q)):
            if q[i].cpuBurstsLeft == 0:
                qbackup.remove(q[i])

        #q = qbackup[:]
        #print ("Sorting...")
        q.sort(key = lambda x: x.cpuBurstsLeft)
        #for i in range(len(q)):
            #print q[i].name

        # PHASE 2: RUN IT LIKE SJF
        print("PHASE 2")
        
        for cycle in range(numProcesses * timeQuantum):
            numProcessesDone = 0
            for i in range(numProcesses):
                if (p[i].state == Process.STATE_DONE):
                    # DEBUG print(p[i].name + " done... numProcessesDone: " + str(numProcessesDone))
                    numProcessesDone += 1
            
            for i in range(len(q)):
                if (q[i].state == Process.STATE_READY):
                    if (r == None):
                        if (pr == None):
                            r = q[i]
                            r.state = Process.STATE_RUNNING
                            r.processTimeQuantum = timeQuantum
                        else:
                            if (pr != q[i]):
                                if (numProcessesDone < numProcesses):
                                    pr = r
                                    
                                else:
                                    r = None
                                r = q[i]
                                r.state = Process.STATE_RUNNING
                                #pr.wait()
                    else:
                        if (r != q[i]):
                            q[i].state = Process.STATE_WAITING
                            
                if (q[i].state == Process.STATE_WAITING):
                    if (r == None):
                        r = q[i]
                        r.state = Process.STATE_RUNNING
                        r.processTimeQuantum = timeQuantum
                    else:
                        q[i].wait()
                        # DEBUG print(q[i].name + " waiting... " + str(q[i].waitingTime) + " cycles passed.")

                if (r != None):
                    if (r == q[i] and r.cpuBurstsLeft > 0):
                        if (r.processTimeQuantum > 0):
                            r.burst()
                            r.processTimeQuantum -= 1
                            # DEBUG print(r.name + " running... " + str(r.cpuBurstsLeft) + " cycles left.")
                        else:
                            r.state = Process.STATE_WAITING
                            pr = r
                            r = None
                    elif (r == q[i] and r.cpuBurstsLeft == 0):
                        r.state = Process.STATE_DONE
                        pr = r
                        r = None

                
            currentCycle += 1


        timeQuantum *= multiplier
    
    # DEBUG print("Current cycle: " + str(currentCycle))
    displayOutput(p)

# Execute Optimized RR with TQ=5 and multiplier=2
OptiRR(5)
# Execute Optimized RR with TQ=5 and multiplier=3
OptiRR(5,3)
