#include <iostream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

// === PROCESS CLASS

class Process {
public:
    Process(string name, int burst, int newTime, int priority);

    string name;

    int cpuBurst; // number of CPU cycles left
    int maxBurst; // number of CPU cycles it has (shouldn't change)
    int priority; // priority (lower is higher priority)

    int maxNewTime; // number of cycles to go from new to ready

    int timeNew; // store the number of cycles for new to ready time here
    int timeWait; // store the number of cycles for wait time here
    int timeResponse; // store the number of cycles for response time here
    int timeTurnaround; // store the number of cycles for response time here

    void Reset();
    void Delay();
    void Burst();
    void Wait();

    int state;

    enum states {STATE_NEW, STATE_READY, STATE_RUNNING, STATE_WAITING, STATE_DONE};
};

Process::Process(string Name="",int burst=1, int newTime=1, int priority=0) {
    cpuBurst = burst;
    maxBurst = burst;
    priority = priority;
    name = Name;

    maxNewTime = newTime;
    timeNew = 0;
    timeWait = 0;
    timeResponse = 0;
    timeTurnaround = 0;

    state = STATE_READY;
}

void Process::Reset() {
    cpuBurst = maxBurst;

    timeNew = 0;
    timeWait = 0;
    timeResponse = 0;
    timeTurnaround = 0;

    state = STATE_NEW;
}

void Process::Delay() {
    timeNew++;
    //timeWait++;
    timeResponse++;
    timeTurnaround++;
}

void Process::Burst() {
    cpuBurst--;
    timeTurnaround++;
}

void Process::Wait() {
    timeWait++;
    timeTurnaround++;
    if (cpuBurst == maxBurst) timeResponse++;
}

// === VARIABLES

const int NUM_PROCESS = 5;
Process* P[NUM_PROCESS];

double sumWait = 0;
double sumResponse = 0;
double sumTurnaround = 0;

int currentCycle = -2; // DON'T ASK ME WHY

Process** currentProcess = nullptr;

int numProcessesDone = 0;

vector<Process*> processQueue;

// === OUTPUT DISPLAY
void displayOutput() {
    for (int i=0; i<NUM_PROCESS; i++) {
        cout << "=== " << P[i]->name << " ===" << endl;
        cout << "Wait time:\t\t" << P[i]->timeWait << endl;
        sumWait += P[i]->timeWait;
        cout << "Response time:\t\t" << P[i]->timeResponse << endl;
        sumResponse += P[i]->timeResponse;
        cout << "Turnaround time:\t" << P[i]->timeTurnaround << endl << endl;
        sumTurnaround += P[i]->timeTurnaround;
    }

    cout << "Total cycles used:\t" << currentCycle << endl;
    cout << "Ave. wait time:\t\t" << sumWait/NUM_PROCESS << endl;
    cout << "Ave. response time:\t" << sumResponse/NUM_PROCESS << endl;
    cout << "Ave. turnaround time:\t" << sumTurnaround/NUM_PROCESS << endl;
    cout << "Throughput:\t\t" << "[redacted]" << endl;
    cout << "CPU utilization:\t" << "[redacted]" << endl;
}

// === RESET "CPU"
void resetCPU() {
    currentCycle = -2; // AGAIN, DON'T ASK ME WHY
    sumResponse = 0;
    sumTurnaround = 0;
    sumWait = 0;
    for (int i=0; i<NUM_PROCESS; i++) {
        P[i]->Reset();
    }
    currentProcess = nullptr;
    numProcessesDone = 0;
    processQueue.clear();
}

// SORT PROCESSES ASC
// source: http://www.cplusplus.com/reference/algorithm/sort/
bool sortAsc(Process* a, Process* b) {
    return (a->cpuBurst < b->cpuBurst);
}

// === MAIN LOOP

int main() {
    P[0] = new Process("P1", 22, 5);
    P[1] = new Process("P2", 18, 5);
    P[2] = new Process("P3", 9, 5);
    P[3] = new Process("P4", 10, 5);
    P[4] = new Process("P5", 5, 5);

    // === FCFS
    cout << "First Come First Serve" << endl;
    cout << "======================" << endl;
    resetCPU();
    while (numProcessesDone != NUM_PROCESS) {
        numProcessesDone = 0;
        for(int i=0; i<NUM_PROCESS; i++) {
            if (P[i]->state == Process::STATE_NEW) {
                if (P[i]->timeNew < P[i]->maxNewTime) {
                    P[i]->Delay();
#ifdef DEBUG
                    cout << P[i]->name << " delayed... " << P[i]->maxNewTime-P[i]->timeNew << " cycles left." << endl;
#endif
                }
                else {
                    P[i]->state = Process::STATE_READY;
                    processQueue.push_back(P[i]);
                }
            }

            if (P[i]->state == Process::STATE_DONE) numProcessesDone++;
        }

        for (int i=0; i<processQueue.size(); i++) {

            if (processQueue[i]->state == Process::STATE_READY) {
                if (currentProcess == nullptr) {
                    currentProcess = &processQueue[i];
                    (*(currentProcess))->state = Process::STATE_RUNNING;
                }
                else {
                    if (currentProcess != &processQueue[i]) processQueue[i]->state = Process::STATE_WAITING;
                }
            }

            if (processQueue[i]->state == Process::STATE_WAITING) {
#ifdef DEBUG
                cout << processQueue[i]->name << " waiting... " << processQueue[i]->timeWait << " cycles passed." << endl;
#endif
                if (currentProcess == nullptr) {
                    currentProcess = &processQueue[i];
                    (*(currentProcess))->state = Process::STATE_RUNNING;
                }
                else {
                    processQueue[i]->Wait();
                }
            }

            if (currentProcess != nullptr) {
                if (currentProcess == &processQueue[i] && (*(currentProcess))->cpuBurst > 0) {
                    (*(currentProcess))->Burst();
#ifdef DEBUG
                    cout << (*(currentProcess))->name << " running... " << (*(currentProcess))->cpuBurst << " cycles left." << endl;
#endif
                }
                else if (currentProcess == &processQueue[i]  && (*(currentProcess))->cpuBurst == 0) {
                    (*(currentProcess))->state = Process::STATE_DONE;
                    currentProcess = nullptr;
                }
            }
        }
#ifdef DEBUG
        cout << endl;
#endif
    currentCycle++;
    }
    displayOutput();

    // === SJF (NP)
    cout << "Shortest Job First (NP)" << endl;
    cout << "=======================" << endl;
    resetCPU();
    while (numProcessesDone != NUM_PROCESS) {
        numProcessesDone = 0;
        for(int i=0; i<NUM_PROCESS; i++) {
            if (P[i]->state == Process::STATE_NEW) {
                if (P[i]->timeNew < P[i]->maxNewTime) {
                    P[i]->Delay();
#ifdef DEBUG
                    cout << P[i]->name << " delayed... " << P[i]->maxNewTime-P[i]->timeNew << " cycles left." << endl;
#endif
                }
                else {
                    P[i]->state = Process::STATE_READY;
                    processQueue.push_back(P[i]);
                }
            }

            if (P[i]->state == Process::STATE_DONE) numProcessesDone++;
        }

        sort(processQueue.begin(), processQueue.end(), sortAsc);

        for (int i=0; i<processQueue.size(); i++) {

            if (processQueue[i]->state == Process::STATE_READY) {
                if (currentProcess == nullptr) {
                    currentProcess = &processQueue[i];
                    (*(currentProcess))->state = Process::STATE_RUNNING;
                }
                else {
                    if (currentProcess != &processQueue[i]) processQueue[i]->state = Process::STATE_WAITING;
                }
            }

            if (processQueue[i]->state == Process::STATE_WAITING) {
#ifdef DEBUG
                cout << processQueue[i]->name << " waiting... " << processQueue[i]->timeWait << " cycles passed." << endl;
#endif
                if (currentProcess == nullptr) {
                    currentProcess = &processQueue[i];
                    (*(currentProcess))->state = Process::STATE_RUNNING;
                }
                else {
                    processQueue[i]->Wait();
                }
            }

            if (currentProcess != nullptr) {
                if (currentProcess == &processQueue[i] && (*(currentProcess))->cpuBurst > 0) {
                    (*(currentProcess))->Burst();
#ifdef DEBUG
                    cout << (*(currentProcess))->name << " running... " << (*(currentProcess))->cpuBurst << " cycles left." << endl;
#endif
                }
                else if (currentProcess == &processQueue[i]  && (*(currentProcess))->cpuBurst == 0) {
                    (*(currentProcess))->state = Process::STATE_DONE;
                    currentProcess = nullptr;
                }
            }
        }
#ifdef DEBUG
        cout << endl;
#endif
    currentCycle++;
    }
    displayOutput();

    return 0;
}
