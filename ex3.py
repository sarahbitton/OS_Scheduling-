import sys


def extract_data(filename):
    f = open(filename, "r")
    Num_of_files = int(f.readline())
    Arrival_Time = []
    CPU_time = []

    for i in range(0, Num_of_files):
        line = f.readline()
        line = line.split(',')
        Arrival_Time.append(int(line[0]))
        CPU_time.append(int(line[1].rstrip()))

    return Num_of_files, Arrival_Time, CPU_time


def FcfsFunc(Num_of_files, process_data):
    at = [process_data[i][1] for i in range(Num_of_files)]
    cput = [process_data[i][2] for i in range(Num_of_files)]
    res = []
    Num_of_files2 = Num_of_files
    time = 0
    while (Num_of_files != 0):
        process = min(at)
        start = process
        if(time< process):
            time = process

        index = at.index(process)
        time = time + cput[index]
        end = time
        at.pop(index)
        cput.pop(index)
        Num_of_files -= 1
        res.append([start,end])

    TA = [proc[1] -proc[0] for proc in res]
    average = sum(TA) / Num_of_files2
    print("FCFS: mean turnaround = ",average)


def LcFsNp(Num_of_files,process_data):

    at = [process_data[i][1] for i in range(Num_of_files)]
    cput = [process_data[i][2] for i in range(Num_of_files)]

    numFile = Num_of_files
    complete = numFile
    pick = min(at)
    betweenWhichProcessToChoose = []
    res=[]
    time = min(at)
    indexes = [i for i,v in enumerate(at) if v == time ]
    while(complete != 0):
        if ((time == 0) | (betweenWhichProcessToChoose == [])):
            time = min(at)
            indexes = [i for i, v in enumerate(at) if v == time]
            index = max(indexes)
            start = time
        else:
            pick = max(betweenWhichProcessToChoose)
            if time < pick:
                indexes = [i for i, v in enumerate(at) if v == time]
                index = max(indexes)
            else:
                indexes = [i for i, v in enumerate(at) if v == pick]
                index = max(indexes)
            start = pick

        time += cput[index]
        end = time
        res.append([start,time])
        at.pop(index)
        cput.pop(index)
        betweenWhichProcessToChoose = pickerProcess(time,at)
        complete -= 1

    TA = [proc[1] - proc[0] for proc in res]
    average = sum(TA) / numFile
    print("LCFS (NP): mean turnaround = ",average)

def pickerProcess(time,Arrival_time):
    res = [process for process in Arrival_time if process <= time]
    return  res


def findWaitingTimeLcfsPre(n, at, cput,wt):
    rt = [0] * n


    complete = 0
    for i in range(n):
        rt[i] = cput[i]
        if(cput[i] == 0):
            complete += 1

    lastCome = 0
    time = 0
    pick_index = 0
    check = False
    while(complete != n):
        for i in range(n):
            if((at[i] <= time) and  (at[i] >= lastCome)  and (rt[i] > 0)):
                pick_index = i
                lastCome = at[i]
                check = True
        if(check == False):
            time += 1
            continue
        rt[pick_index] -= 1
        if (rt[pick_index] == 0):
            lastCome = 0
            complete += 1
            check = False
            fint = time + 1
            wt[pick_index] = (fint - cput[pick_index] - at[pick_index])
            if (wt[pick_index] < 0):
                wt[pick_index] = 0
        time += 1
def findTurnAroundTimeLcfsPre(n,process_data):
    wt = [0] * n
    tat = [0] * n
    at = [process_data[i][1] for i in range(n)]
    cput = [process_data[i][2] for i in range(n)]
    findWaitingTimeLcfsPre(n, at, cput,wt)
    for i in range(n):
        tat[i] = cput[i] + wt[i]

    average = sum(tat) / n
    print("LCFS (P): mean turnaround = ",average)


def findWaitingTimeSJF(at,cput, n, wt): #process = (
    rt = [0] * n
    complete = 0
    for i in range(n):
        rt[i] = cput[i]
        if (cput[i] == 0):
            complete += 1

    t = 0
    minm = 999999999
    short = 0
    check = False
    #(process id, burts time, arrival time)
    while (complete != n):
        for j in range(n):
            if ((at[j] <= t) and
                    (rt[j] < minm) and rt[j] > 0):
                minm = rt[j]
                short = j
                check = True
        if (check == False):
            t += 1
            continue

        rt[short] -= 1
        minm = rt[short]
        if (minm == 0):
            minm = 999999999
        if (rt[short] == 0):
            complete += 1
            check = False
            fint = t + 1
            wt[short] = (fint - cput[short] -
                         at[short])
            if (wt[short] < 0):
                wt[short] = 0
        t += 1
def findTurnAroundTimeSJF(n,process_data):

    wt = [0] * n
    tat =[0] * n
    at = [process_data[i][1] for i in range(n)]
    cput = [process_data[i][2] for i in range(n)]
    findWaitingTimeSJF(at,cput, n, wt)
    for i in range(n):
        tat[i] = cput[i] + wt[i]


    average = sum(tat) / n
    print("SJF: mean turnaround = ", average)







def findTurnArroundTimeRR(no_of_processes,Arrival_Time, CPU_time, time_slice):
    process_data = []
    for i in range(no_of_processes):
        temporary = []
        temporary.extend([i, Arrival_Time[i], CPU_time[i], 0, CPU_time[i]])
        '''
        '0' is the state of the process. 0 means not executed and 1 means execution complete

        '''
        process_data.append(temporary)

    start_time = []
    exit_time = []
    executed_process = []
    ready_queue = []
    s_time = 0
    process_data.sort(key=lambda x: x[1])
    '''
    Sort processes according to the Arrival Time
    '''
    while 1:
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][3] == 0:
                present = 0
                if len(ready_queue) != 0:
                    for k in range(len(ready_queue)):
                        if process_data[i][0] == ready_queue[k][0]:
                            present = 1
                '''
                The above if loop checks that the next process is not a part of ready_queue
                '''
                if present == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                '''
                The above if loop adds a process to the ready_queue only if it is not already present in it
                '''
                if len(ready_queue) != 0 and len(executed_process) != 0:
                    for k in range(len(ready_queue)):
                        if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                            ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                '''
                The above if loop makes sure that the recently executed process is appended at the end of ready_queue
                '''
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            if ready_queue[0][2] > time_slice:
                '''
                If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                '''
                start_time.append(s_time)
                s_time = s_time + time_slice
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(ready_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - time_slice
                ready_queue.pop(0)
            elif ready_queue[0][2] <= time_slice:
                '''
                If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                '''
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(ready_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
                ready_queue.pop(0)
        elif len(ready_queue) == 0:
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            if normal_queue[0][2] > time_slice:
                '''
                If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                '''
                start_time.append(s_time)
                s_time = s_time + time_slice
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(normal_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - time_slice
            elif normal_queue[0][2] <= time_slice:
                '''
                If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                '''
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(normal_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
    calculateTurnaroundTimeRR(process_data)

def calculateTurnaroundTimeRR(process_data):
    total_turnaround_time = 0
    for i in range(len(process_data)):
        turnaround_time = process_data[i][5] - process_data[i][1]
        '''
        turnaround_time = completion_time - arrival_time
        '''
        total_turnaround_time = total_turnaround_time + turnaround_time
        process_data[i].append(turnaround_time)
    average_turnaround_time = total_turnaround_time / len(process_data)
    '''
    average_turnaround_time = total_turnaround_time / no_of_processes
    '''
    print("RR: mean turnaround = ",average_turnaround_time)













def main():
    if (len(sys.argv) != 2):
        print("Error in the input program")
        return

    Num_of_files, Arrival_Time, CPU_time = extract_data(sys.argv[1])

    process_data = []
    for i in range(Num_of_files):
        temporary = []
        temporary.extend([i, Arrival_Time[i], CPU_time[i], 0, CPU_time[i]])
        process_data.append(temporary)
    process_data.sort(key=lambda x: x[1])



    FcfsFunc(Num_of_files,process_data)
    LcFsNp(Num_of_files,process_data)
    findTurnAroundTimeLcfsPre( Num_of_files,process_data)
    findTurnAroundTimeSJF( Num_of_files,process_data)
    findTurnArroundTimeRR(Num_of_files, Arrival_Time, CPU_time, 2)

    return



if __name__ == "__main__":
    main()