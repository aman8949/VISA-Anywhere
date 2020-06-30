import random,math

a = 1 # average number of arrivals per minute
b = 1.5 # average number of people served per minute
ncust = 1000 # number of customers

AT = [ ] # list of arrival times of a person joining the queue
ST = [ ] # list of service times once they reach the front
FT = [ ] # list of finish times after waiting and being served

AT = [0 for i in range(ncust)]
FT = [0 for i in range(ncust)]
# Generate inter-arrival times
randomnums = [random.random() for i in range(ncust)]
interAT = [-1/a*math.log(r) for r in randomnums]

AT[0] = interAT[0]# Arrival time of first customer
for i in range(1,ncust):
    print(AT[i-1])
    AT[i] = AT[i − 1] + interAT[i] # Arrival time of ith customer

# Generate random service times for each customer
randomnums = [random.random() for i in range(ncust)]
ST = [-1/b*math.log(r) for r in randomnums]

FT[0] = AT[0] + ST[0] # Finish time for first customer
for i in range(1,ncust):
    FT[i] = max(AT[i], FT[i − 1]) + ST[i]

totalTime = [FT[i]-AT[i] for i in range(ncust)] # Total time spent by each customer
waitTime = [totalTime[i] - ST[i] for i in range(ncust)] # Time spent waiting before being served

aveServiceTime = sum(ST)/ncust
aveWaitTime = sum(waitTime)/ncust
aveTotalTime = sum(totalTime)/ncust # Keep track of average ser