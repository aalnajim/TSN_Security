
import random
import networkx as nx
import matplotlib.pyplot as plt
import TSNFlow
import TSNHost
import Path
import operation
import TimeSlot
import myThread
import myThread2
import math
from timeit import default_timer as timer
from itertools import islice
from TSNHost import TSNHost
import sys
from itertools import combinations
from myThread import myThread
from myThread2 import myThread2
#import queue



W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
def rand(G,hosts, n):
    transmissionDelays = {}
    for i in G.nodes:
        tranmissionDelay = random.randint(1,90)
        transmissionDelays[i] = {'transmissionDelay':tranmissionDelay}

    linkMeasurments = {}
    for i in nx.edges(G,G.nodes):
        processingDelay = random.randint(1,3)
        nbOfTSN = 0
        bandwidth = 0
        linkMeasurments[i] = {'processingDelay': processingDelay, 'nbOfTSN': nbOfTSN, 'bandwidth':bandwidth}


    temp = []
    for i in G.nodes:
        temp.append(i)
    hostsList = []
    for i in range(hosts):
        linkedNode = random.choice(temp)
        id = n + i
        host = TSNHost(id,linkedNode)
        hostsList.append(host)

    return transmissionDelays,linkMeasurments, hostsList

# def findHost(hostsList, id):
#     for h in hostsList:
#         if (h.id == id):
#             return h




##############################
# this method is to calcualte the overall delay for each link based on (the link delay and the switch delays) 0 to split and 1 to combine
def convertProcDelayToComulativeDelay(G,x):
    #x has to be 0 or 1
    if (x ==0):
        for i in nx.edges(G, G.nodes):
            transmissionDelay = G.nodes[i[0]]['transmissionDelay']
            processingAndPropDelay = G[i[0]][i[1]]['processingDelay']
            G[i[0]][i[1]]['processingDelay'] = processingAndPropDelay - transmissionDelay

    elif(x==1):
        for i in nx.edges(G, G.nodes):
            transmissionDelay = G.nodes[i[0]]['transmissionDelay']
            processingAndPropDelay = G[i[0]][i[1]]['processingDelay']
            G[i[0]][i[1]]['processingDelay'] = transmissionDelay + processingAndPropDelay

    else:
        print('You have to enter 1 to combine or 0 to split')


#this method is added recently to find k shortest paths
def k_shortest_paths(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))


#this method is added recently to enhance K shortest path and use multithreading
# def findKthPathP(G,hostsList,k): speed
#     allPaths = {}  # all the paths between all the hosts
#
#     # Create new threads
#     thread1 = myThread(allPaths, G,hostsList,k, (0 * math.floor(len(hostsList) / 10)), ((1 * math.floor(len(hostsList) / 10))))
#     thread2 = myThread(allPaths, G,hostsList,k, (1 * math.floor(len(hostsList) / 10)), (2 * math.floor(len(hostsList) / 10)))
#     thread3 = myThread(allPaths, G,hostsList,k, (2 * math.floor(len(hostsList) / 10)), (3 * math.floor(len(hostsList) / 10)))
#     thread4 = myThread(allPaths, G,hostsList,k, (3 * math.floor(len(hostsList) / 10)), (4 * math.floor(len(hostsList) / 10)))
#     thread5 = myThread(allPaths, G,hostsList,k, (4 * math.floor(len(hostsList) / 10)), (5 * math.floor(len(hostsList) / 10)))
#     thread6 = myThread(allPaths, G,hostsList,k, (5 * math.floor(len(hostsList) / 10)), (6 * math.floor(len(hostsList) / 10)))
#     thread7 = myThread(allPaths, G,hostsList,k, (6 * math.floor(len(hostsList) / 10)), (7 * math.floor(len(hostsList) / 10)))
#     thread8 = myThread(allPaths, G,hostsList,k, (7 * math.floor(len(hostsList) / 10)), (8 * math.floor(len(hostsList) / 10)))
#     thread9 = myThread(allPaths, G,hostsList,k, (8 * math.floor(len(hostsList) / 10)), (9 * math.floor(len(hostsList) / 10)))
#     thread10 = myThread(allPaths, G,hostsList,k, (9 * math.floor(len(hostsList) / 10)), ((10 * math.floor(len(hostsList) / 10)) + len(hostsList) % 10))
#
#     # Start new Threads
#     thread1.start()
#     thread2.start()
#     thread3.start()
#     thread4.start()
#     thread5.start()
#     thread6.start()
#     thread7.start()
#     thread8.start()
#     thread9.start()
#     thread10.start()
#
#     # join new Threads
#     thread1.join()
#     thread2.join()
#     thread3.join()
#     thread4.join()
#     thread5.join()
#     thread6.join()
#     thread7.join()
#     thread8.join()
#     thread9.join()
#     thread10.join()
#
#     print("done!")
#     return allPaths


#this method is added recently to enhance K shortest path and use multithreading
# def findKthPathP2(G,hostsList,k): speed
#     allPaths = {}  # all the paths between all the hosts
#
#     # Create new threads
#     thread1 = myThread2(allPaths, G,hostsList,k, (0 * math.floor(len(hostsList) / 10)), ((1 * math.floor(len(hostsList) / 10))))
#     thread2 = myThread2(allPaths, G,hostsList,k, (1 * math.floor(len(hostsList) / 10)), (2 * math.floor(len(hostsList) / 10)))
#     thread3 = myThread2(allPaths, G,hostsList,k, (2 * math.floor(len(hostsList) / 10)), (3 * math.floor(len(hostsList) / 10)))
#     thread4 = myThread2(allPaths, G,hostsList,k, (3 * math.floor(len(hostsList) / 10)), (4 * math.floor(len(hostsList) / 10)))
#     thread5 = myThread2(allPaths, G,hostsList,k, (4 * math.floor(len(hostsList) / 10)), (5 * math.floor(len(hostsList) / 10)))
#     thread6 = myThread2(allPaths, G,hostsList,k, (5 * math.floor(len(hostsList) / 10)), (6 * math.floor(len(hostsList) / 10)))
#     thread7 = myThread2(allPaths, G,hostsList,k, (6 * math.floor(len(hostsList) / 10)), (7 * math.floor(len(hostsList) / 10)))
#     thread8 = myThread2(allPaths, G,hostsList,k, (7 * math.floor(len(hostsList) / 10)), (8 * math.floor(len(hostsList) / 10)))
#     thread9 = myThread2(allPaths, G,hostsList,k, (8 * math.floor(len(hostsList) / 10)), (9 * math.floor(len(hostsList) / 10)))
#     thread10 = myThread2(allPaths, G,hostsList,k, (9 * math.floor(len(hostsList) / 10)), ((10 * math.floor(len(hostsList) / 10)) + len(hostsList) % 10))
#
#     # Start new Threads
#     thread1.start()
#     thread2.start()
#     thread3.start()
#     thread4.start()
#     thread5.start()
#     thread6.start()
#     thread7.start()
#     thread8.start()
#     thread9.start()
#     thread10.start()
#
#     # join new Threads
#     thread1.join()
#     thread2.join()
#     thread3.join()
#     thread4.join()
#     thread5.join()
#     thread6.join()
#     thread7.join()
#     thread8.join()
#     thread9.join()
#     thread10.join()
#
#     print("done!")
#     return allPaths

##############################



#def findAllPath(G,hostsList):
def findKthPath(G,hostsList,k):
    allPaths = {}  # all the paths between all the hosts
    for s in hostsList:
        for d in hostsList:
            paths = []
            paths2=[]
            if (s.id == d.id):
                continue
            if (s.accessPoint == d.accessPoint):
                tempNodes = [s, s.accessPoint,
                             d]  ############################################################################
                tempNodes2 = [d, d.accessPoint, s]
                tempDelay = s.transmissonDelay + s.processingDelay + G.nodes[s.accessPoint][
                    'transmissionDelay'] + d.processingDelay
                tempDelay2 = d.transmissonDelay + d.processingDelay + G.nodes[d.accessPoint][
                    'transmissionDelay'] + s.processingDelay
                tempPath = Path.Path(tempNodes, tempDelay)
                tempPath2 = Path.Path(tempNodes2, tempDelay2)
                paths.append(tempPath)
                paths2.append(tempPath2)
                allPaths[s.id, d.id] = paths
                allPaths[d.id, s.id] = paths2
                continue
            else:
                tempList = list(
                    islice(nx.shortest_simple_paths(G, s.accessPoint, d.accessPoint, weight='processingDelay'),
                           k))
                for path in tempList:
                    if (len(path) < 8):
                        path2 = path.copy()
                        path2.reverse()

                        tempNodes = [
                            s]  ############################################################################
                        tempNodes2 = [d]
                        tempDelay = s.transmissonDelay + s.processingDelay
                        tempDelay2 = d.transmissonDelay + d.processingDelay
                        i = 1
                        for n in range(len(path)):
                            tempNodes.append(list(path).__getitem__(n))
                            tempNodes2.append(list(path2).__getitem__(n))
                            tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
                            tempDelay2 = tempDelay2 + G.nodes[list(path2).__getitem__(n)]['transmissionDelay']
                            if (i < len(path)):
                                tempDelay = tempDelay + \
                                            G[list(path).__getitem__(n)][list(path).__getitem__(n + 1)][
                                                'processingDelay'] - G.nodes[list(path).__getitem__(n)][
                                                'transmissionDelay']
                                tempDelay2 = tempDelay2 + \
                                             G[list(path2).__getitem__(n)][list(path2).__getitem__(n + 1)][
                                                 'processingDelay'] - G.nodes[list(path2).__getitem__(n)][
                                                 'transmissionDelay']
                            i = i + 1
                        tempNodes.append(
                            d)  ############################################################################
                        tempNodes2.append(
                            s)
                        tempDelay = tempDelay + d.processingDelay
                        tempDelay2 = tempDelay2 + s.processingDelay
                        tempPath = Path.Path(tempNodes, tempDelay)
                        tempPath2 = Path.Path(tempNodes2, tempDelay2)
                        paths.append(tempPath)
                        paths2.append(tempPath2)
                        allPaths[s.id, d.id] = paths
                        allPaths[d.id, s.id] = paths2

                # for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
                #     if (len(path) < 8):
                #         tempNodes = [s] ############################################################################
                #         tempDelay = s.transmissonDelay + s.processingDelay
                #         i = 1
                #         for n in range(len(path)):
                #             tempNodes.append(list(path).__getitem__(n))
                #             tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
                #             if(i < len(path)):
                #                 tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']
                #             i = i + 1
                #         tempNodes.append(d) ############################################################################
                #         tempDelay = tempDelay + d.processingDelay
                #         tempPath = Path.Path(tempNodes,tempDelay)
                #         paths.append(tempPath)
                #         allPaths[s.id, d.id] = paths

    return allPaths



# #def findAllPath(G,hostsList): speed
# def findKthPath2(G,hostsList,k):
#     allPaths = {}  # all the paths between all the hosts
#     for s in hostsList:
#         for d in hostsList:
#             paths = []
#             if (s.id == d.id):
#                 continue
#             if (s.accessPoint == d.accessPoint):
#                 tempNodes = [s, s.accessPoint, d] ############################################################################
#                 tempDelay = s.transmissonDelay + s.processingDelay + G.nodes[s.accessPoint]['transmissionDelay'] + d.processingDelay
#                 tempPath = Path.Path(tempNodes,tempDelay)
#                 paths.append(tempPath)
#                 allPaths[s.id, d.id] = paths
#                 continue
#             else:
#                 tempList = list(islice(nx.shortest_simple_paths(G, s.accessPoint, d.accessPoint, weight='processingDelay'),k))
#                 for path in tempList:
#                     if(len(path) < 8):
#                         tempNodes = [s] ############################################################################
#                         tempDelay = s.transmissonDelay + s.processingDelay
#                         i = 1
#                         for n in range(len(path)):
#                             tempNodes.append(list(path).__getitem__(n))
#                             tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
#                             if(i < len(path)):
#                                 tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']- G.nodes[list(path).__getitem__(n)]['transmissionDelay']  # we substracted because the delay is in combined mode((1))
#                             i = i + 1
#                         tempNodes.append(d) ############################################################################
#                         tempDelay = tempDelay + d.processingDelay
#                         tempPath = Path.Path(tempNodes,tempDelay)
#                         paths.append(tempPath)
#                         allPaths[s.id, d.id] = paths
#
#                 # for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
#                 #     if (len(path) < 8):
#                 #         tempNodes = [s] ############################################################################
#                 #         tempDelay = s.transmissonDelay + s.processingDelay
#                 #         i = 1
#                 #         for n in range(len(path)):
#                 #             tempNodes.append(list(path).__getitem__(n))
#                 #             tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
#                 #             if(i < len(path)):
#                 #                 tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']
#                 #             i = i + 1
#                 #         tempNodes.append(d) ############################################################################
#                 #         tempDelay = tempDelay + d.processingDelay
#                 #         tempPath = Path.Path(tempNodes,tempDelay)
#                 #         paths.append(tempPath)
#                 #         allPaths[s.id, d.id] = paths
#
#     return allPaths





###################################

# def findAllPath(G,hostsList):  speed
#     allPaths = {}  # all the paths between all the hosts
#     for s in hostsList:
#         for d in hostsList:
#             paths = []
#             if (s.id == d.id):
#                 continue
#             if (s.accessPoint == d.accessPoint):
#                 tempNodes = [s, s.accessPoint,
#                              d]  ############################################################################
#                 tempDelay = s.transmissonDelay + s.processingDelay + G.nodes[s.accessPoint][
#                     'transmissionDelay'] + d.processingDelay
#                 tempPath = Path.Path(tempNodes, tempDelay)
#                 paths.append(tempPath)
#                 allPaths[s.id, d.id] = paths
#                 continue
#             else:
#                 for path in nx.all_simple_paths(G, s.accessPoint, d.accessPoint):
#                     if (len(path) < 8):
#                         tempNodes = [s] ############################################################################
#                         tempDelay = s.transmissonDelay + s.processingDelay
#                         i = 1
#                         for n in range(len(path)):
#                             tempNodes.append(list(path).__getitem__(n))
#                             tempDelay = tempDelay + G.nodes[list(path).__getitem__(n)]['transmissionDelay']
#                             if(i < len(path)):
#                                 tempDelay = tempDelay + G[list(path).__getitem__(n)][list(path).__getitem__(n+1)]['processingDelay']
#                             i = i + 1
#                         tempNodes.append(d) ############################################################################
#                         tempDelay = tempDelay + d.processingDelay
#                         tempPath = Path.Path(tempNodes,tempDelay)
#                         paths.append(tempPath)
#                         allPaths[s.id, d.id] = paths
#
#     return allPaths



# def findKthPathold(G, hostsList,K): speed
#     allPaths = findAllPath(G,hostsList)   #all the paths between all the hosts
#     for s in hostsList:
#         for d in hostsList:
#             if (s.id == d.id):
#                 continue
#             else:
#                 if(s.id, d.id) in allPaths.keys():
#                     paths = allPaths[s.id, d.id]
#                     paths.sort(key= lambda x: x.delay)
#                     if(len(paths)>K):
#                         gap = len(paths) - K
#                         for i in range(gap):
#                             paths.pop()
#
#     return allPaths



def changeLinksBandwidth(G):

    for i in nx.edges(G, G.nodes):
        bandwidth = random.randint(500,1000)
        G[i[0]][i[1]]['bandwidth']= bandwidth


def findcandidatePaths(paths,delay):
    candidatePaths = []
    for path in paths:
        if(path.delay<= delay):
            candidatePaths.append(path)
        else:
            break

    return candidatePaths

def computeMeasurments(G, candidatePaths):  #this method will compute the path bandwidth and # of TSN flows based on the path links' measurments
    for path in candidatePaths:
        TSNCounter = 0
        bandwidth = 3000

        for index in range(len(path.nodes)):
            if(index == 0 or index > len(path.nodes)-3):
                continue
            if (G[path.nodes.__getitem__(index)][path.nodes.__getitem__(index + 1)]['nbOfTSN'] > TSNCounter):
                TSNCounter = G[path.nodes.__getitem__(index)][path.nodes.__getitem__(index + 1)]['nbOfTSN']
            if(G[path.nodes.__getitem__(index)][path.nodes.__getitem__(index+1)]['bandwidth']< bandwidth):
                bandwidth = G[path.nodes.__getitem__(index)][path.nodes.__getitem__(index+1)]['bandwidth']
        path.TSNFlowCounter = TSNCounter
        path.bandwidth = bandwidth

def BestValues(candidatePaths):     # return the smallest values for normalization
    maxBandwidth = 0
    minHopCount = 1000
    minTSNCount = 10000
    for path in candidatePaths:
        if(path.bandwidth>maxBandwidth):
            maxBandwidth = path.bandwidth
        if(path.hopCount<minHopCount):
            minHopCount = path.hopCount
        if(path.TSNFlowCounter<minTSNCount):
            minTSNCount = path.TSNFlowCounter

    return maxBandwidth,minHopCount,minTSNCount


def pathSelection(G, tempTSNFlow, firstKthPaths, TSNCountWeight, bandwidthWeight, hopCountWeight,flag):
    if (flag ==0):
        if((tempTSNFlow.source.id,tempTSNFlow.destniation.id) not in firstKthPaths.keys()):
            return False
        paths = firstKthPaths[tempTSNFlow.source.id,tempTSNFlow.destniation.id]
        candidatePaths = findcandidatePaths(paths, tempTSNFlow.flowMaxDelay)
    else:
        candidatePaths = firstKthPaths

    if len(candidatePaths)==0:
        return False,candidatePaths
    elif (len(candidatePaths)==1):
        tempTSNFlow.path = candidatePaths.__getitem__(0)
        tempTSNFlow.candidatePathCounter = 1
        return True,candidatePaths
    else:
        tempTSNFlow.candidatePathCounter = len(candidatePaths)
        computeMeasurments(G, candidatePaths)
        maxBandwidth, minHopCount, minTSNCount = BestValues(candidatePaths)
        maxDelta = 0
        for path in candidatePaths:
            hopCountRelativeValue = minHopCount/path.hopCount
            bandwidthRelativeValue = path.bandwidth/maxBandwidth
            if(path.TSNFlowCounter ==0):
                TSNCounterRaltiveValue = 1
            else:
                TSNCounterRaltiveValue = minTSNCount/path.TSNFlowCounter


            Delta = (hopCountWeight * hopCountRelativeValue) + (bandwidthWeight * bandwidthRelativeValue) + (TSNCountWeight * TSNCounterRaltiveValue)
            if(Delta>maxDelta):
                maxDelta = Delta
                tempTSNFlow.path = path
        return True,candidatePaths

    return False,candidatePaths


def computeTimeSlotLength(G, hostLists, firstKthPaths):
    maxDelay = 0
    for s in hostLists:
        for d in hostLists:
            if s.id == d.id:
                continue
            if((s.id,d.id)in firstKthPaths.keys()):
                paths = firstKthPaths[s.id,d.id]
                for path in paths:
                    if(path.delay>maxDelay):
                        maxDelay = path.delay



    return maxDelay


def createTimeSlots(nbOfTimeSlots):
    timeSlots = []
    for index in range(nbOfTimeSlots):
        tempTimeSlot = TimeSlot.TimeSlot(index,[])
        timeSlots.append(tempTimeSlot)
    return timeSlots



def map(G,tempTSNFlow,startTime):
    operations=[]
    cmulativeTime = startTime
    path = tempTSNFlow.path
    for i in range(len(tempTSNFlow.path.nodes)):
        if (i == 0):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i).id,tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).transmissonDelay
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i).id,tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).processingDelay
            tempOperation = operation.operation(id, cmulativeTime)
            operations.append(tempOperation)
        elif (i < len(path.nodes) - 2):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + G.nodes[tempTSNFlow.path.nodes.__getitem__(i)]['transmissionDelay']
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + G[tempTSNFlow.path.nodes.__getitem__(i)][tempTSNFlow.path.nodes.__getitem__(i+1)]['processingDelay']
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
        elif (i < len(path.nodes) - 1):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1).id)
            cmulativeTime = cmulativeTime + G.nodes[tempTSNFlow.path.nodes.__getitem__(i)]['transmissionDelay']
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
        else:
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i-1),tempTSNFlow.path.nodes.__getitem__(i).id)
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).processingDelay
            tempOperation = operation.operation(id, cmulativeTime)
            operations.append(tempOperation)

    return operations

def map_ws(G,tempTSNFlow,startTime,queuingDelays):
    operations=[]
    cmulativeTime = startTime
    path = tempTSNFlow.path
    index = 0
    for i in range(len(tempTSNFlow.path.nodes)):
        if (i == 0):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i).id,tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).transmissonDelay
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i).id,tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).processingDelay
            tempOperation = operation.operation(id, cmulativeTime)
            operations.append(tempOperation)
        elif (i < len(path.nodes) - 2):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + G.nodes[tempTSNFlow.path.nodes.__getitem__(i)]['transmissionDelay'] + queuingDelays[index]
            tempOperation = operation.operation(id,cmulativeTime)
            index = index + 1
            operations.append(tempOperation)
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1))
            cmulativeTime = cmulativeTime + G[tempTSNFlow.path.nodes.__getitem__(i)][tempTSNFlow.path.nodes.__getitem__(i+1)]['processingDelay']
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
        elif (i < len(path.nodes) - 1):
            id = '{},{}trans'.format(tempTSNFlow.path.nodes.__getitem__(i), tempTSNFlow.path.nodes.__getitem__(i+1).id)
            cmulativeTime = cmulativeTime + G.nodes[tempTSNFlow.path.nodes.__getitem__(i)]['transmissionDelay'] + queuingDelays[index]
            index = index + 1
            tempOperation = operation.operation(id,cmulativeTime)
            operations.append(tempOperation)
        else:
            id = '{},{}proc'.format(tempTSNFlow.path.nodes.__getitem__(i-1),tempTSNFlow.path.nodes.__getitem__(i).id)
            cmulativeTime = cmulativeTime + tempTSNFlow.path.nodes.__getitem__(i).processingDelay
            tempOperation = operation.operation(id, cmulativeTime)
            operations.append(tempOperation)

    return operations




def SWOTS_AEAP(G, tempTSNFlow,scheduledFlowsSWOTS_AEAP,CLength):
    startTime = 0

    if(len(scheduledFlowsSWOTS_AEAP)!=0):
        operations = map(G, tempTSNFlow,startTime)
        index = 2
        for operation in operations[2::2]:
            for scheduledItem in scheduledFlowsSWOTS_AEAP:
                SF = scheduledItem.__getitem__(0)
                SST = scheduledItem.__getitem__(1)
                SFO = map(G,SF,SST)
                for SO in SFO[2::2]:
                    if(SO.id == operation.id):
                        gap = SO.cumulativeDelay - operations.__getitem__(index-1).cumulativeDelay
                        if (gap>startTime):
                            startTime = gap
                        break

            index = index + 2
        if((startTime + operations.__getitem__(len(operations)-2).cumulativeDelay)<=CLength):
            scheduledFlowsSWOTS_AEAP.append((tempTSNFlow,startTime))
            return True



    else:
        scheduledFlowsSWOTS_AEAP.append((tempTSNFlow,startTime))
        return(True)


    return False

def SWOTS_AEAP_WS(G, tempTSNFlow,scheduledFlowsSWOTS_AEAP_WS,CLength): #Scheduling Without Time-Slots (As Early As possible) with allowing queueing delay (it will return a boolean , and a list of queueing delays)
    startTime = 0
    cumStartTime = 0
    queuingDelays = [0 for _ in range(len(tempTSNFlow.path.nodes)-2)]
    if(len(scheduledFlowsSWOTS_AEAP_WS)!=0):
        operations = map(G, tempTSNFlow,startTime)
        index = 2
        queueingDelayIndex = 0
        for operation in operations[2::2]:
            for scheduledItem in scheduledFlowsSWOTS_AEAP_WS:
                SF = scheduledItem.__getitem__(0)
                SST = scheduledItem.__getitem__(1)
                SQD = scheduledItem.__getitem__(2)
                SFO = map_ws(G,SF,SST,SQD)
                for SO in SFO[2::2]:
                    if(SO.id == operation.id):
                        gap = SO.cumulativeDelay - operations.__getitem__(index-1).cumulativeDelay
                        if (gap>cumStartTime):
                            temp = gap - cumStartTime
                            queuingDelays[queueingDelayIndex]= queuingDelays[queueingDelayIndex] + temp
                            cumStartTime = gap
                            if(cumStartTime - startTime + operations.__getitem__(len(operations)-1).cumulativeDelay > tempTSNFlow.flowMaxDelay):
                                desiredAdjusment = ((cumStartTime + operations.__getitem__(len(operations)-1).cumulativeDelay) - tempTSNFlow.flowMaxDelay - startTime)
                                startTime = startTime + desiredAdjusment
                                for i in range(len(queuingDelays)):
                                    if(desiredAdjusment>=queuingDelays[i]):
                                        desiredAdjusment = desiredAdjusment - queuingDelays[i]
                                        queuingDelays[i] = 0
                                    else:
                                        queuingDelays[i] = queuingDelays[i] - desiredAdjusment
                                        desiredAdjusment = 0
                                    if (desiredAdjusment ==0):
                                        break
                        break

            index = index + 2
            queueingDelayIndex = queueingDelayIndex + 1
        if((operations.__getitem__(len(operations)-2).cumulativeDelay + cumStartTime)<=CLength):
            scheduledFlowsSWOTS_AEAP_WS.append((tempTSNFlow,startTime,queuingDelays))
            return True



    else:
        scheduledFlowsSWOTS_AEAP_WS.append((tempTSNFlow,startTime,queuingDelays))
        return True


    return False


def SWOTS_ASAP(G, tempTSNFlow,scheduledFlowsSWOTS_ASAP,CLength,time, FTT):
    publishTime = 15000 + 1000
    startTime = (time - FTT + publishTime)%CLength
    tempOperations = map(G,tempTSNFlow,startTime)       #line 652-654 added lately
    if (tempOperations.__getitem__(len(tempOperations)-2).cumulativeDelay>CLength):
        startTime=0
    timeStamp = 0

    if (len(scheduledFlowsSWOTS_ASAP) != 0):
        while (timeStamp < CLength):
            flag = 0
            operations = map(G, tempTSNFlow, startTime)
            if (operations.__getitem__(len(operations)-2).cumulativeDelay>CLength):
                startTime =0
                continue
            index = 2
            for operation in operations[2::2]:
                for scheduledItem in scheduledFlowsSWOTS_ASAP:
                    SF = scheduledItem.__getitem__(0)
                    SST = scheduledItem.__getitem__(1)
                    SFO = map(G, SF, SST)
                    index2 = 2
                    for SO in SFO[2::2]:
                        if (SO.id == operation.id):
                            gap = SFO.__getitem__(index2 - 1).cumulativeDelay - operations.__getitem__(index - 1).cumulativeDelay
                            #gapModified = SFO.__getitem__(index2 - 1).cumulativeDelay%CLength - operations.__getitem__(index - 1).cumulativeDelay%CLength
                            if(gap<0):
                                gap = SO.cumulativeDelay - operations.__getitem__(index - 1).cumulativeDelay
                                if(gap>0):
                                    startTime = startTime + gap
                                    timeStamp = timeStamp + gap
                                    if((gap + operations.__getitem__(len(operations)-2).cumulativeDelay)>CLength): # this one should be gap instead of start time
                                        startTime = 0
                                    flag = 1
                                    break
                            else:
                                transmissionOperationLength = operation.cumulativeDelay - operations.__getitem__(index - 1).cumulativeDelay # this should be (-) instead of (+)
                                if(gap< transmissionOperationLength):
                                    gap = SO.cumulativeDelay - operations.__getitem__(index - 1).cumulativeDelay
                                    startTime = startTime + gap
                                    timeStamp = timeStamp+gap
                                    if ((gap + operations.__getitem__(len(operations) - 2).cumulativeDelay) > CLength): # this one should be gap instead of start time
                                        startTime = 0
                                    flag = 1
                                    break
                        index2 = index2 + 2

                    if(flag ==1):
                        break
                if(flag ==1):
                    break
                index = index + 2
            if(flag==0):
                    scheduledFlowsSWOTS_ASAP.append((tempTSNFlow, startTime))
                    return True



    else:
            scheduledFlowsSWOTS_ASAP.append((tempTSNFlow, startTime))
            return (True)
    return False

def SWOTS_ASAP_WS(G, tempTSNFlow,scheduledFlowsSWOTS_ASAP_WS,CLength,time, FTT):
    publishTime = 15000 + 1000
    startTime = (time - FTT + publishTime)%CLength
    tempOperations = map(G,tempTSNFlow,startTime)       #line 652-654 added lately
    if (tempOperations.__getitem__(len(tempOperations)-2).cumulativeDelay>CLength):
        startTime=0
    timeStamp = 0
    queuingDelays = [0 for _ in range(len(tempTSNFlow.path.nodes)-2)]

    if (len(scheduledFlowsSWOTS_ASAP_WS) != 0):
        while (timeStamp < CLength):
            flag = 0
            operations = map_ws(G, tempTSNFlow, startTime,queuingDelays)
            if (operations.__getitem__(len(operations)-2).cumulativeDelay>CLength):
                startTime =0
                continue
            index = 2
            for operation in operations[2::2]:
                for scheduledItem in scheduledFlowsSWOTS_ASAP_WS:
                    SF = scheduledItem.__getitem__(0)
                    SST = scheduledItem.__getitem__(1)
                    SQD = scheduledItem.__getitem__(2)
                    SFO = map_ws(G, SF, SST,SQD)
                    index2 = 2
                    for SO in SFO[2::2]:
                        if (SO.id == operation.id):
                            #tempIndex = int((index/2)-1)
                            gap = SFO.__getitem__(index2 - 1).cumulativeDelay  - operations.__getitem__(index - 1).cumulativeDelay
                            #gapModified = SFO.__getitem__(index2 - 1).cumulativeDelay%CLength - operations.__getitem__(index - 1).cumulativeDelay%CLength
                            if(gap<=0):     # the arrival time of the new flow is at the same time or after the arrival time of the overlapped scheduled flow
                                gap = SO.cumulativeDelay - operations.__getitem__(index - 1).cumulativeDelay    #the difference between the end time of scheduled flow and the arrival time of the new flow [waiting time]
                                tempIndex = int((index / 2) - 1)  # This index is for queuing delay (we divided it by two because we have two operations for each switch)
                                if(gap>queuingDelays[tempIndex]):   # the new flow will arrive after the (transmission + queuing delay) of the scheduled traffic
                                    #startTime = startTime + gap
                                    tempAdjusment = (gap - queuingDelays[tempIndex])
                                    timeStamp = timeStamp + tempAdjusment
                                    queuingDelays[tempIndex] = gap

                                    #queuingDelays[tempIndex] = queuingDelays[tempIndex]+tempAdjusment
                                    if (tempAdjusment + operations.__getitem__(len(operations) - 1).cumulativeDelay - startTime > tempTSNFlow.flowMaxDelay):
                                        desiredAdjusment = ((tempAdjusment + operations.__getitem__(len(operations) - 1).cumulativeDelay) -startTime - tempTSNFlow.flowMaxDelay)
                                        startTime = startTime + desiredAdjusment
                                        for i in range(len(queuingDelays)):
                                            if (desiredAdjusment >= queuingDelays[i]):
                                                desiredAdjusment = desiredAdjusment - queuingDelays[i]
                                                queuingDelays[i] = 0
                                            else:
                                                queuingDelays[i] = queuingDelays[i] - desiredAdjusment
                                                desiredAdjusment = 0
                                            if (desiredAdjusment == 0):
                                                break
                                        if((desiredAdjusment + operations.__getitem__(len(operations)-2).cumulativeDelay)>CLength):
                                            startTime = 0
                                            queuingDelays = [0 for _ in range(len(tempTSNFlow.path.nodes) - 2)]
                                    flag = 1
                                    break
                            else:        # the arrival time of the new flow is before the arrival time of the overlapped scheduled flow
                                transmissionOperationLength = operation.cumulativeDelay - operations.__getitem__(index - 1).cumulativeDelay
                                if(gap< transmissionOperationLength):       # the arrival time of the new flow during the transmission of the scheduled flow
                                    gap = SO.cumulativeDelay - operations.__getitem__(index - 1).cumulativeDelay
                                    tempIndex = int((index / 2) - 1)
                                    if (gap > queuingDelays[tempIndex]):
                                        # startTime = startTime + gap
                                        tempAdjusment = (gap - queuingDelays[tempIndex])
                                        timeStamp = timeStamp + tempAdjusment
                                        queuingDelays[tempIndex] = gap
                                        if (tempAdjusment + operations.__getitem__(len(operations) - 1).cumulativeDelay - startTime > tempTSNFlow.flowMaxDelay):
                                            desiredAdjusment = ((tempAdjusment + operations.__getitem__(len(operations) - 1).cumulativeDelay) - startTime - tempTSNFlow.flowMaxDelay)
                                            startTime = startTime + desiredAdjusment
                                            for i in range(len(queuingDelays)):
                                                if (desiredAdjusment >= queuingDelays[i]):
                                                    desiredAdjusment = desiredAdjusment - queuingDelays[i]
                                                    queuingDelays[i] = 0
                                                else:
                                                    queuingDelays[i] = queuingDelays[i] - desiredAdjusment
                                                    desiredAdjusment = 0
                                                if (desiredAdjusment == 0):
                                                    break
                                        if ((tempAdjusment + operations.__getitem__(len(operations) - 2).cumulativeDelay) > CLength):
                                            startTime = 0
                                            queuingDelays = [0 for _ in range(len(tempTSNFlow.path.nodes) - 2)]
                                        flag = 1
                                        break
                        index2 = index2 + 2

                    if(flag ==1):
                        break
                if(flag ==1):
                    break
                index = index + 2
            if(flag==0):
                    scheduledFlowsSWOTS_ASAP_WS.append((tempTSNFlow, startTime,queuingDelays))
                    return True



    else:
            scheduledFlowsSWOTS_ASAP_WS.append((tempTSNFlow, startTime,queuingDelays))
            return (True)
    return False

def SWTS(G, tempTSNFlow,scheduledFlowsSWTS ,CLength,timeSlots, now, FTT):
    path = tempTSNFlow.path
    isScheduled = False
    publishTime = 15000 + 1000              #state-of-the-art SDN switches could insert forwaring entry in 15 ms (15000 microseconds), 1 ms for sending the configuration from the controller
    slotLength = CLength/len(timeSlots)
    nextSlot = (math.floor(((now-FTT+publishTime)%CLength)/slotLength)+1)%len(timeSlots)
    counter = 1
    pathEdges = []
    for index in range(len(path.nodes)):
        if (index == 0):
            # tempLink = '({},{})'.format(path.nodes.__getitem__(index).id, path.nodes.__getitem__(index + 1))
            # pathEdges.append(tempLink)
            continue
        elif(index <len(path.nodes)-2):
            tempLink = '({},{})'.format(path.nodes.__getitem__(index), path.nodes.__getitem__(index + 1))
            pathEdges.append(tempLink)
        elif(index ==len(path.nodes)-2):
            tempLink = '({},{})'.format(path.nodes.__getitem__(index), path.nodes.__getitem__(index + 1).id)
            pathEdges.append(tempLink)
    while True:
        tempSlot = timeSlots.__getitem__(nextSlot)
        isScheduled = True
        for edge in pathEdges:
            if(tempSlot.Scheduledlinks.__contains__(edge)):
                isScheduled = False
                break
        if(isScheduled or counter>len(timeSlots)):
            break
        counter = counter + 1
        nextSlot = (nextSlot + 1)%len(timeSlots)
    if(isScheduled):
        tempSlot = timeSlots.__getitem__(nextSlot)
        for edge in pathEdges:
            tempSlot.Scheduledlinks.append(edge)
        scheduledFlowsSWTS.append((tempTSNFlow,nextSlot))

    return isScheduled


def display(path):
    text = '[ '
    for n in range(len(path.nodes)):
        if (n == 0):
            text = text + '{}, '.format(path.nodes.__getitem__(n).id)
        elif(n== len(path.nodes)-1):
            text = text + '{} ] '.format(path.nodes.__getitem__(n).id)
        else:
            text = text + '{}, '.format(path.nodes.__getitem__(n))

    return text

def displayListOfCollisions(listofCollisions):
    for listItem in listofCollisions:
        currentFlow = listItem.__getitem__(0)
        collidedTSNFlows = listItem.__getitem__(3)
        collisionsLocations = listItem.__getitem__(4)
        print("Flow number {} collided with {} other flows in {} egress ports as follow:".format(currentFlow.id,
                                                                                                 listItem.__getitem__(1),
                                                                                                 listItem.__getitem__(2)))
        for index in range(len(collidedTSNFlows)):
            print("({}) It collides with TSN Flow number {} at egress port {}".format(index+1, collidedTSNFlows.__getitem__(
                index).id, collisionsLocations.__getitem__(index)))
        print("----------------------------")

def displayCollisionList(collisionList, collisionPerEgressPortCounter):
    print("There are {} distinct collisions between TSN Flows at {} egress ports in this run as follow:".format(
        len(collisionList), collisionPerEgressPortCounter))
    index = 0
    for collisionListItem in collisionList:
        firstCollidedFlow = collisionListItem.__getitem__(0)
        secondCollidedFlow = collisionListItem.__getitem__(1)
        collisionsLocations = collisionListItem.__getitem__(2)
        index = index + 1
        print("({}) TSN Flow number {} collides with TSN Flow number {} at these egress ports {}".format(index,
                                                                                                         firstCollidedFlow.id,
                                                                                                         secondCollidedFlow.id,
                                                                                                         collisionsLocations))

def displayFlowStatistics(firstTSNFlow,secondTSNFlow, collisionLocation, listofCollisions):
    nbOfCollisions, nbOfCollidedFlows, nbOfCollisionsWithTheSecondTSNFlow, nbOfDistinctCollidedLocations, nbOfCollisionsInTheLocation = \
        calculateCollisionsStatisticsForAFlow(firstTSNFlow,secondTSNFlow, collisionLocation, listofCollisions)
    print("The statistics of flow {}:\n (1) Total NB of Collisions is: ({})\n (2) NB of collided flows is: ({})"
          "\n (3) NB of Collisions with flow number {} is: ({})\n (4) NB of distinct collided locations is: ({})"
          "\n (5) NB of Collisions in {} is: ({})".format(firstTSNFlow.id,nbOfCollisions, nbOfCollidedFlows, secondTSNFlow.id,nbOfCollisionsWithTheSecondTSNFlow,
                                                          nbOfDistinctCollidedLocations, collisionLocation, nbOfCollisionsInTheLocation ))

def displaySummaryAfterResolvingCollisionUsingDrop(scheduledFlows, deletedScheduledFlows, listOfDropedFlows,theUsedAlgorithm):
    print()
    print()
    print("--------------------------------------------------")
    print("|                Overall Summary                 |")
    print("--------------------------------------------------")
    print()
    print()
    print("# The network promised to support {} TSN flows\n# {} of them are hidden from the scheduler due to the blindness attack\n# {} of them are in the schedule and can be seen by the controller\n# By resolving collisions using drop mechanism based on {} algorithm:\n"
          "     * the network was able to deliver {} flows out of {} promised flows\n     * It fails to deliver (drops) {} out of {} promised flows"
          .format(len(scheduledFlows)+len(deletedScheduledFlows),len(deletedScheduledFlows),len(scheduledFlows),theUsedAlgorithm,len(scheduledFlows)+len(deletedScheduledFlows)-len(listOfDropedFlows),len(scheduledFlows)+len(deletedScheduledFlows),len(listOfDropedFlows),len(scheduledFlows)+len(deletedScheduledFlows)))

    droppedCounter = 0
    deliveredCounter = 0
    deliveredList =[]
    for scheduledFlow in scheduledFlows:
        tempTSNFLow = scheduledFlow.__getitem__(0)
        if(tempTSNFLow in listOfDropedFlows):
            droppedCounter = droppedCounter + 1
        else:
            deliveredCounter = deliveredCounter + 1
            deliveredList.append(tempTSNFLow)
    for deletedFlow in deletedScheduledFlows:
        tempTSNFLow = deletedFlow.__getitem__(0)
        if(tempTSNFLow in listOfDropedFlows):
            droppedCounter = droppedCounter + 1
        else:
            deliveredCounter = deliveredCounter + 1
            deliveredList.append(tempTSNFLow)
    return deliveredList, deliveredCounter, droppedCounter

def findFlowArrivalTime(flow, flowsList):
    arrivalTime = -1
    for index in range(len(flowsList)):
        tempStoredItem = list(flowsList).__getitem__(index)
        if(tempStoredItem.__getitem__(0).id == flow.id):
            return tempStoredItem.__getitem__(1)


    return arrivalTime


def countGates_AEAP(G, scheduledSWOTS):
    numberOfGates = 0
    numberOfMergedGates = 0
    index = 0
    for scheduledItem in scheduledSWOTS[0:len(scheduledSWOTS):]:
        operations = map(G,scheduledItem.__getitem__(0),scheduledItem.__getitem__(1))
        for operation in operations[2:len(operations):2]:
            numberOfGates = numberOfGates + 1
            for tempScheduledItem in scheduledSWOTS[index+1:len(scheduledSWOTS):]:
                tempOperations = map(G,tempScheduledItem.__getitem__(0),tempScheduledItem.__getitem__(1))
                index2 = 2
                for tempOperation in tempOperations[2:len(tempOperations):2]:
                    if((operation.id == tempOperation.id) and (operation.cumulativeDelay-tempOperations.__getitem__(index2-1).cumulativeDelay ==0)):
                        numberOfMergedGates = numberOfMergedGates + 1

                    index2 = index2 + 2



        index = index + 1


    return numberOfGates,numberOfMergedGates

def countGates_AEAP_WS(G, scheduledSWOTS):
    numberOfGates = 0
    numberOfMergedGates = 0
    index = 0
    for scheduledItem in scheduledSWOTS[0:len(scheduledSWOTS):]:
        operations = map_ws(G,scheduledItem.__getitem__(0),scheduledItem.__getitem__(1),scheduledItem.__getitem__(2))
        index3 = 2
        for operation in operations[2:len(operations):2]:
            numberOfGates = numberOfGates + 1
            for tempScheduledItem in scheduledSWOTS[index+1:len(scheduledSWOTS):]:
                tempOperations = map_ws(G,tempScheduledItem.__getitem__(0),tempScheduledItem.__getitem__(1),tempScheduledItem.__getitem__(2))
                index2 = 2
                for tempOperation in tempOperations[2:len(tempOperations):2]:
                    tempIndex2 = int((index2/2)-1)
                    tempIndex3 = int((index3/2)-1)
                    if((operation.id == tempOperation.id) and (operation.cumulativeDelay-(tempOperations.__getitem__(index2-1).cumulativeDelay+tempScheduledItem.__getitem__(2)[tempIndex2]) ==0)):
                        numberOfMergedGates = numberOfMergedGates + 1

                    index2 = index2 + 2
            index3 = index3 + 2



        index = index + 1


    return numberOfGates,numberOfMergedGates

def countGates_ASAP(G, scheduledSWOTS):
    numberOfGates = 0
    numberOfMergedGates = 0
    index = 0
    for scheduledItem in scheduledSWOTS[0:len(scheduledSWOTS):]:
        operations = map(G,scheduledItem.__getitem__(0),scheduledItem.__getitem__(1))
        index3 = 2
        for operation in operations[2:len(operations):2]:
            numberOfGates = numberOfGates + 1
            for tempScheduledItem in scheduledSWOTS[index+1:len(scheduledSWOTS):]:
                tempOperations = map(G,tempScheduledItem.__getitem__(0),tempScheduledItem.__getitem__(1))
                index2 = 2
                for tempOperation in tempOperations[2:len(tempOperations):2]:
                    if((operation.id == tempOperation.id) and ((operation.cumulativeDelay-tempOperations.__getitem__(index2-1).cumulativeDelay ==0)
                                                               or (tempOperation.cumulativeDelay-operations.__getitem__(index3-1).cumulativeDelay ==0))):
                        numberOfMergedGates = numberOfMergedGates + 1

                    index2 = index2 + 2
            index3 = index3 + 2



        index = index + 1


    return numberOfGates,numberOfMergedGates

def countGates_ASAP_WS(G, scheduledSWOTS):
    numberOfGates = 0
    numberOfMergedGates = 0
    index = 0
    for scheduledItem in scheduledSWOTS[0:len(scheduledSWOTS):]:
        operations = map_ws(G,scheduledItem.__getitem__(0),scheduledItem.__getitem__(1),scheduledItem.__getitem__(2))
        index3 = 2
        for operation in operations[2:len(operations):2]:
            numberOfGates = numberOfGates + 1
            for tempScheduledItem in scheduledSWOTS[index+1:len(scheduledSWOTS):]:
                tempOperations = map_ws(G,tempScheduledItem.__getitem__(0),tempScheduledItem.__getitem__(1),tempScheduledItem.__getitem__(2))
                index2 = 2
                for tempOperation in tempOperations[2:len(tempOperations):2]:
                    tempIndex2 = int((index2/2)-1)
                    tempIndex3 = int((index3/2)-1)
                    if((operation.id == tempOperation.id) and ((operation.cumulativeDelay-(tempOperations.__getitem__(index2-1).cumulativeDelay+tempScheduledItem.__getitem__(2)[tempIndex2]) ==0))
                            or ((tempOperation.cumulativeDelay-(operations.__getitem__(index3-1).cumulativeDelay+scheduledItem.__getitem__(2)[tempIndex3]) ==0))):
                        numberOfMergedGates = numberOfMergedGates + 1

                    index2 = index2 + 2
            index3 = index3 + 2



        index = index + 1


    return numberOfGates,numberOfMergedGates



def computeAvgQueuingDelayPerFlowPerHop(scheuledFlows):
    counter = 0
    total = 0
    avg = 0
    for scheduledItem in scheuledFlows:
        queuingDelays = scheduledItem.__getitem__(2)  # return the queuing delay: scheduledItem = (TSN Flow, Transmission Start Time, Queuing Delaysof the Flow at each hop in the Path)
        for queuingDelay in queuingDelays:
            counter = counter + 1
            total = total + queuingDelay

    avg = total/counter
    return int(avg)

def convertPathToAlistOfEdges(G,path):
    tempListOfEdges = []
    for index in range(len(path.nodes)):
        if (index == 0):
            # tempLink = '({},{})'.format(path.nodes.__getitem__(index).id, path.nodes.__getitem__(index + 1))
            # pathEdges.append(tempLink)
            continue
        elif (index < len(path.nodes) - 2):
            tempLink = '({},{})'.format(path.nodes.__getitem__(index),
                                        path.nodes.__getitem__(index + 1))
            tempListOfEdges.append(tempLink)
        elif (index == len(path.nodes) - 2):
            tempLink = '({},{})'.format(path.nodes.__getitem__(index),
                                        path.nodes.__getitem__(index + 1).id)
            tempListOfEdges.append(tempLink)
    return tempListOfEdges


def convertOperationIDtoEdge(operationID):
    # convert the operation ID from "7,6proc" to "(7,6)", which is similar to edge name format in scheduling SWTS
    firstString = operationID
    firstArray = firstString.split(",")
    incomeSwitch = firstArray.__getitem__(0)
    secondString = firstArray.__getitem__(1)
    secondArray = list(secondString)
    outcomeSwitch = ""
    tempOutcomeSwitch = ""
    for i in range(len(secondArray)):
        tempOutcomeSwitch = tempOutcomeSwitch + secondArray.__getitem__(i)
        if (tempOutcomeSwitch.isnumeric() == False):
            break
        outcomeSwitch = tempOutcomeSwitch
    result = "({},{})".format(incomeSwitch, outcomeSwitch)
    return result

def convertEdgetoOperationID(tempEdge):
    # convert the edge to operation ID from "(7,6)" to "7,6proc", which is the opposite of the 'convertOperationIDtoEdge'
    tempArray = tempEdge.split(",")
    firstArray = list(tempArray.__getitem__(0))
    secondArray = list(tempArray.__getitem__(1))

    incomeSwitch = ""
    for i in range(1, len(firstArray)):
        incomeSwitch = incomeSwitch + firstArray.__getitem__(i)

    outcomeSwitch = ""
    for i in range(len(secondArray) - 1):
        outcomeSwitch = outcomeSwitch + secondArray.__getitem__(i)
    result = "{},{}trans".format(incomeSwitch, outcomeSwitch)
    return result

def computeListOfCollisionsperFlowByEgressPort(collisionList,collisionLocation):
    # This method takes two parameters:
    # (1) The list 'collisionList', which has all distinct collisions in the form of (firstTSNFlow, firstTSNFlow, collisionLocations)
    # (2) The collisionLocation in the form of string as follow "(2,3)"
    #Then, it returns the list 'result', which has all the collisions in that location in the form of (firstTSNFlow, listOfCollidedTSNFlows)

    result = []             # A list of all collisions in 'collisionLocation' in the form of (firstTSNFlow, listOfCollidedTSNFlows)
    reigsteredTSNFlows = []
    for listItem in collisionList:
        if(collisionLocation in listItem.__getitem__(2)):
            if(listItem.__getitem__(0) in reigsteredTSNFlows):
                theFirstFlowIndex = reigsteredTSNFlows.index(listItem.__getitem__(0))
                ((result.__getitem__(theFirstFlowIndex)).__getitem__(1)).append(listItem.__getitem__(1))
            else:
                result.append((listItem.__getitem__(0),[listItem.__getitem__(1)]))
                reigsteredTSNFlows.append(listItem.__getitem__(0))
            if(listItem.__getitem__(1) in reigsteredTSNFlows):
                theSecondFlowIndex = reigsteredTSNFlows.index(listItem.__getitem__(1))
                ((result.__getitem__(theSecondFlowIndex)).__getitem__(1)).append(listItem.__getitem__(0))
            else:
                result.append((listItem.__getitem__(1), [listItem.__getitem__(0)]))
                reigsteredTSNFlows.append(listItem.__getitem__(1))

    return result

def computeListOfCollisionsForAFlowInEgressPort(collisionList,collisionLocation,TSNFlow):
    # This method takes three parameters:
    # (1) The list 'collisionList', which has all distinct collisions in the form of (firstTSNFlow, firstTSNFlow, collisionLocations)
    # (2) The collisionLocation in the form of string as follow "(2,3)"
    # (3) The targeted 'TSNFlow'
    #Then, it returns the list 'result', which has all TSN Flows collided with 'TSNFlow' in 'collisionLocation' in the form of 'listOfCollidedTSNFlows'

    result = []
    tempList = computeListOfCollisionsperFlowByEgressPort(collisionList,collisionLocation)
    for listItem in tempList:
        if (listItem.__getitem__(0)== TSNFlow):
            result = listItem.__getitem__(1)
            break


    return result


def getWaitingTimesperFlowByEgressPort(listOfCollisions, collisionLocation):
    # This method takes two parameters:
    # (1) The list 'collisionList', which has all distinct collisions in the form of (firstTSNFlow, firstTSNFlow, collisionLocations)
    # (2) The collisionLocation in the form of string as follow "(2,3)"
    # Then, it returns the list 'result', which has all the waiting times in that location in the form of (firstTSNFlow, listOfWitingTimes)


    result = []  # A list of all waiting times in 'collisionLocation' in the form of (firstTSNFlow, listOfWaitingTimes)
    reigsteredTSNFlows = []
    for listItem in listOfCollisions:
        if(len(listItem)<6):
            break
        if (collisionLocation in listItem.__getitem__(4)):
            for tempIndex in range(len(listItem.__getitem__(3))):
                if(listItem.__getitem__(4).__getitem__(tempIndex)==collisionLocation):
                    if (listItem.__getitem__(0) in reigsteredTSNFlows):
                        theFirstFlowIndex = reigsteredTSNFlows.index(listItem.__getitem__(0))
                        ((result.__getitem__(theFirstFlowIndex)).__getitem__(1)).append(listItem.__getitem__(3).__getitem__(tempIndex))
                        ((result.__getitem__(theFirstFlowIndex)).__getitem__(2)).append(
                            listItem.__getitem__(5).__getitem__(tempIndex))
                    else:
                        result.append((listItem.__getitem__(0), [listItem.__getitem__(3).__getitem__(tempIndex)], [listItem.__getitem__(5).__getitem__(tempIndex)]))
                        reigsteredTSNFlows.append(listItem.__getitem__(0))

    return result


def getWaitingTimeForAFlowInEgressPort(listOfCollision,collisionLocation,TSNFlow):
    # This method takes three parameters:
    # (1) The list 'collisionList', which has all distinct collisions in the form of (firstTSNFlow, firstTSNFlow, collisionLocations)
    # (2) The collisionLocation in the form of string as follow "(2,3)"
    # (3) The targeted 'TSNFlow'
    #Then, it returns the list 'result', which contains all waiting times for TSNFlow when we makes it start just after collided TSN Flows in 'collisionLocation' in the form of 'listOfWaitingTimes'
    # each entry in 'listOfWaitingTimes' corresponds to an entry in 'listOfCollidedTSNFlows' obtain from method 'computeListOfCollisionsForAFlowInEgressPort'

    result = []
    tempList = getWaitingTimesperFlowByEgressPort(listOfCollision,collisionLocation)
    for listItem in tempList:
        if (listItem.__getitem__(0)== TSNFlow):
            result = listItem.__getitem__(2)
            break


    return result



def computeNumberOfCollisionPerRun(listofCollisions):
    theResultList =[]      #this list contains the list of distinct collision in the form of (firstCollidedTSNFlow, secondCollidedTSNFlow, listOfCollisionLocations). Eg. (TSNFLOW1, TSNFLOW2, ["(1,2)","(5,6)"]
    listOfComputedCollidedTSNFlows = []
    distinctCollisionPerEgressPortCounter = 0
    for collisionItem in listofCollisions:
        firstCollidedTSNFlow = collisionItem.__getitem__(0)
        collidedTSNFlows = collisionItem.__getitem__(3)
        collidedLocations = collisionItem.__getitem__(4)
        listOfExistingFlows = []
        for index in range(len(collidedLocations)):
            secondCollidedTSNFlow = collidedTSNFlows.__getitem__(index)
            collidedLocation = collidedLocations.__getitem__(index)
            distinctCollisionPerEgressPortCounter = distinctCollisionPerEgressPortCounter + 1
            if (secondCollidedTSNFlow in listOfComputedCollidedTSNFlows):  # we have already computed this collision
                continue
            if (len(theResultList) > 0):
                if (secondCollidedTSNFlow in listOfExistingFlows):
                    existingFlowIndex = 0
                    for existingFlow in listOfExistingFlows:
                        if(existingFlow.id == secondCollidedTSNFlow.id):
                            break
                        existingFlowIndex = existingFlowIndex + 1
                    (theResultList.__getitem__((len(theResultList) - 1) - (len(listOfExistingFlows) - 1) + existingFlowIndex)).__getitem__(2).append(collidedLocation)
                else:
                    theResultList.append((firstCollidedTSNFlow,secondCollidedTSNFlow,[collidedLocation]))
                    listOfExistingFlows.append(secondCollidedTSNFlow)
            else:       # This else statement will cover the first iteration where there is no entry in the list
                theResultList.append((firstCollidedTSNFlow, secondCollidedTSNFlow, [collidedLocation]))
        listOfComputedCollidedTSNFlows.append(firstCollidedTSNFlow)

    return theResultList,distinctCollisionPerEgressPortCounter


def findNBofCollisions(TSNFlow, listofCollisions):
    #This function take a TSN flow as an input and return:
    # (1) the number of distinct collisions (the number of collided TSN flows)
    # (2) the total number of its collisions (if it collided with another TSN flow in two different locations it will count as 2)
    for listedItem in listofCollisions:
        if(TSNFlow == listedItem.__getitem__(0)):
            return listedItem.__getitem__(1), listedItem.__getitem__(2)
    return 0, 0



def computeCollisionPerFlowSWTS(G, scheduledFlows, deletedFlows, listofCollisions, tempDeletedItem):
    # This method will compute the collissions of the deleted item "tempDeletedItem" from SWTS Schedule (TSNFlow,TimeSlot)
    # It will check all the items in the schedule and the deleted list to see the collision resulted from the delete attack
    # The result will be added to the list "listofCollisions", which has been passed as a parameter.
    # Each list entry of "listofCollisions" will be in the form of (DeletedTSNFlow, distinctCollisionCounterPerFlow, CollisionCounterPerFlow,
    #                                                                   ListOfCollidedTSNFlows, ListOfCollidedLocations)

    tempDeletedTSNFlow = tempDeletedItem.__getitem__(0)
    tempDeletedTimeSlot = tempDeletedItem.__getitem__(1)
    distinctCollisionCounterPerFlow = 0     #Count the number of distinct collision per flow. In other words,  if the deleted flow collided with another flow in 3 egress ports, it will be count as 1
    CollisionCounterPerFlow = 0             #Count the number of distinct collision per flow. In other words,  if the deleted flow collided with another flow in 3 egress ports, it will be count as 3
    ListOfCollidedTSNFlows = []             #A list of all collided flows with the current flow; a single flow will exist in this list multiple times, if it collided with the current flow in multiple egress ports
    ListOfCollidedLocations = []            #A list of all collision location. Each item in this list corresponds to an item in the list 'ListOfCollidedTSNFlows'

    for scheduledItem in scheduledFlows:
        tempScheduledTSNFlow = scheduledItem.__getitem__(0)
        tempScheduledTimeSlot = scheduledItem.__getitem__(1)
        if((tempDeletedTimeSlot != tempScheduledTimeSlot) or (tempScheduledTSNFlow.id == tempDeletedTSNFlow.id)):
            continue
        else:
            deletedPathEdges = convertPathToAlistOfEdges(G,tempDeletedTSNFlow.path)
            scheduledPathEdges = convertPathToAlistOfEdges(G,tempScheduledTSNFlow.path)
            isCollided = False
            for deletedEdge in deletedPathEdges:
                if(deletedEdge in scheduledPathEdges):
                    CollisionCounterPerFlow = CollisionCounterPerFlow + 1
                    isCollided = True
                    ListOfCollidedTSNFlows.append(tempScheduledTSNFlow)
                    ListOfCollidedLocations.append(deletedEdge)
            if(CollisionCounterPerFlow>0 and isCollided):
                distinctCollisionCounterPerFlow = distinctCollisionCounterPerFlow + 1

    for deletedItem in deletedFlows:
        tempAnotherDeletedTSNFlow = deletedItem.__getitem__(0)
        tempAnotherDeletedTimeSlot = deletedItem.__getitem__(1)
        if(tempDeletedTSNFlow.id == tempAnotherDeletedTSNFlow.id or tempDeletedTimeSlot != tempAnotherDeletedTimeSlot):
            continue
        else:
            deletedPathEdges = convertPathToAlistOfEdges(G,tempDeletedTSNFlow.path)
            anotherDeletedPathEdges = convertPathToAlistOfEdges(G,tempAnotherDeletedTSNFlow.path)
            isCollided = False
            for deletedEdge in deletedPathEdges:
                if (deletedEdge in anotherDeletedPathEdges):
                    CollisionCounterPerFlow = CollisionCounterPerFlow + 1
                    isCollided = True
                    ListOfCollidedTSNFlows.append(tempAnotherDeletedTSNFlow)
                    ListOfCollidedLocations.append(deletedEdge)
            if(CollisionCounterPerFlow>0 and isCollided):
                distinctCollisionCounterPerFlow = distinctCollisionCounterPerFlow + 1

    if(distinctCollisionCounterPerFlow>0):
        listofCollisions.append((tempDeletedTSNFlow,distinctCollisionCounterPerFlow,CollisionCounterPerFlow, ListOfCollidedTSNFlows,ListOfCollidedLocations))




def computeCollisionPerFlowSWOTS_WS(G, scheduledFlows, deletedFlows, listofCollisions, tempDeletedItem):
    #print("SWOTS_ASAP_WS or SWOTS_AEAP_WS")

    tempDeletedTSNFlow = tempDeletedItem.__getitem__(0)
    tempDeletedStartTime = tempDeletedItem.__getitem__(1)
    tempDeletedQueuingDelay = tempDeletedItem.__getitem__(2)
    distinctCollisionCounterPerFlow = 0     #Count the number of distinct collision per flow. In other words,  if the deleted flow collided with another flow in 3 egress ports, it will be count as 1
    CollisionCounterPerFlow = 0             #Count the number of distinct collision per flow. In other words,  if the deleted flow collided with another flow in 3 egress ports, it will be count as 3
    ListOfCollidedTSNFlows = []             #A list of all collided flows with the current flow; a single flow will exist in this list multiple times, if it collided with the current flow in multiple egress ports
    ListOfCollidedLocations = []            #A list of all collision location. Each item in this list corresponds to an item in the list 'ListOfCollidedTSNFlows'
    listOfWaitingTimes = []                 # A list of waiting times per collision locations. Each item in this list corresponds to an item in the list 'ListOfCollidedTSNFlows' and the list 'ListOfCollidedLocations'
                                            #   We assumed that (regardless of the arrival time and finish time of both flows) the current flow will be postponed to start after the other flow

    tempOperations = map_ws(G, tempDeletedTSNFlow, tempDeletedStartTime, tempDeletedQueuingDelay)
    index = 2
    queuingIndex1 = 0
    for tempOperation in tempOperations[2::2]:
        for scheduledItem in scheduledFlows:
            SF = scheduledItem.__getitem__(0)
            if (SF.id == tempDeletedTSNFlow.id):
                continue
            SST = scheduledItem.__getitem__(1)
            SQD = scheduledItem.__getitem__(2)
            SFO = map_ws(G, SF, SST,SQD)
            index2 = 2
            queuingIndex2 = 0
            for SO in SFO[2::2]:
                if (SO.id == tempOperation.id):
                    tempDeletedOperationArrivalTime = tempOperations.__getitem__(index - 1).cumulativeDelay + tempDeletedQueuingDelay.__getitem__(queuingIndex1)
                    tempDeletedOperationFinishTime = tempOperation.cumulativeDelay
                    tempScheduledOperationArrivalTime = SFO.__getitem__(index2 - 1).cumulativeDelay + SQD.__getitem__(queuingIndex2)
                    tempScheduledOperationFinishTime = SO.cumulativeDelay
                    if (((tempDeletedOperationFinishTime >= tempScheduledOperationFinishTime) and (
                            tempDeletedOperationArrivalTime < tempScheduledOperationFinishTime)) or
                            ((tempDeletedOperationFinishTime > tempScheduledOperationArrivalTime) and (
                                    tempDeletedOperationArrivalTime <= tempScheduledOperationArrivalTime)) or
                    ((tempDeletedOperationFinishTime <= tempScheduledOperationFinishTime) and (tempDeletedOperationArrivalTime >= tempScheduledOperationArrivalTime))):
                        CollisionCounterPerFlow = CollisionCounterPerFlow + 1
                        ListOfCollidedTSNFlows.append(SF)
                        ListOfCollidedLocations.append(convertOperationIDtoEdge(SO.id))
                        waitingTime = tempScheduledOperationFinishTime - tempDeletedOperationArrivalTime
                        listOfWaitingTimes.append(waitingTime)

                    break
                index2 = index2 + 2
                queuingIndex2 = queuingIndex2 + 1

        for deletedItem in deletedFlows:
            DF = deletedItem.__getitem__(0)
            if (DF.id == tempDeletedTSNFlow.id):
                continue
            DST = deletedItem.__getitem__(1)
            DQD = deletedItem.__getitem__(2)
            DFO = map_ws(G, DF, DST,DQD)
            index2 = 2
            queuingIndex2 = 0
            for DO in DFO[2::2]:
                if (DO.id == tempOperation.id):
                    tempDeletedOperationArrivalTime = tempOperations.__getitem__(index - 1).cumulativeDelay + tempDeletedQueuingDelay.__getitem__(queuingIndex1)
                    tempDeletedOperationFinishTime = tempOperation.cumulativeDelay
                    deletedOperationArrivalTime = DFO.__getitem__(index2 - 1).cumulativeDelay + DQD.__getitem__(queuingIndex2)
                    deletedOperationFinishTime = DO.cumulativeDelay
                    if (((tempDeletedOperationFinishTime >= deletedOperationFinishTime) and (
                            tempDeletedOperationArrivalTime < deletedOperationFinishTime)) or
                            ((tempDeletedOperationFinishTime > deletedOperationArrivalTime) and (
                                    tempDeletedOperationArrivalTime <= deletedOperationArrivalTime)) or
                    ((tempDeletedOperationFinishTime <= deletedOperationFinishTime) and (tempDeletedOperationArrivalTime >= deletedOperationArrivalTime))):
                        CollisionCounterPerFlow = CollisionCounterPerFlow + 1
                        ListOfCollidedTSNFlows.append(DF)
                        ListOfCollidedLocations.append(convertOperationIDtoEdge(DO.id))
                        waitingTime = deletedOperationFinishTime - tempDeletedOperationArrivalTime
                        listOfWaitingTimes.append(waitingTime)

                    break
                index2 = index2 + 2
                queuingIndex2 = queuingIndex2 + 1

        index = index + 2
        queuingIndex1 = queuingIndex1 + 1

    tempDistictedFlowsList = []
    for TSNFlow in ListOfCollidedTSNFlows:
        if TSNFlow.id not in tempDistictedFlowsList:
            distinctCollisionCounterPerFlow = distinctCollisionCounterPerFlow + 1
            tempDistictedFlowsList.append(TSNFlow.id)

    if (distinctCollisionCounterPerFlow > 0):
        listofCollisions.append((tempDeletedTSNFlow, distinctCollisionCounterPerFlow, CollisionCounterPerFlow,
                                 ListOfCollidedTSNFlows, ListOfCollidedLocations, listOfWaitingTimes))



def computeCollisionPerFlowSWOTS(G, scheduledFlows, deletedFlows, listofCollisions, tempDeletedItem):
    #print("SWOTS_ASAP or SWOTS_AEAP")
    tempDeletedTSNFlow = tempDeletedItem.__getitem__(0)
    tempDeletedStartTime = tempDeletedItem.__getitem__(1)
    distinctCollisionCounterPerFlow = 0     #Count the number of distinct collision per flow. In other words,  if the deleted flow collided with another flow in 3 egress ports, it will be count as 1
    CollisionCounterPerFlow = 0             #Count the number of distinct collision per flow. In other words,  if the deleted flow collided with another flow in 3 egress ports, it will be count as 3
    ListOfCollidedTSNFlows = []             #A list of all collided flows with the current flow; a single flow will exist in this list multiple times, if it collided with the current flow in multiple egress ports
    ListOfCollidedLocations = []            #A list of all collision location. Each item in this list corresponds to an item in the list 'ListOfCollidedTSNFlows'
    listOfWaitingTimes = []                 #A list of waiting times per collision locations. Each item in this list corresponds to an item in the list 'ListOfCollidedTSNFlows' and the list 'ListOfCollidedLocations'
                                            #   We assumed that (regardless of the arrival time and finish time of both flows) the current flow will be postponed to start after the other flow

    tempOperations = map(G, tempDeletedTSNFlow, tempDeletedStartTime)
    index = 2
    for tempOperation in tempOperations[2::2]:
        for scheduledItem in scheduledFlows:
            SF = scheduledItem.__getitem__(0)
            if (SF.id == tempDeletedTSNFlow.id):
                continue
            SST = scheduledItem.__getitem__(1)
            SFO = map(G, SF, SST)
            index2 = 2
            for SO in SFO[2::2]:
                if (SO.id == tempOperation.id):
                    tempDeletedOperationArrivalTime = tempOperations.__getitem__(index - 1).cumulativeDelay
                    tempDeletedOperationFinishTime = tempOperation.cumulativeDelay
                    tempScheduledOperationArrivalTime = SFO.__getitem__(index2 - 1).cumulativeDelay
                    tempScheduledOperationFinishTime = SO.cumulativeDelay
                    if(((tempDeletedOperationFinishTime >= tempScheduledOperationFinishTime) and (tempDeletedOperationArrivalTime< tempScheduledOperationFinishTime)) or
                            ((tempDeletedOperationFinishTime > tempScheduledOperationArrivalTime) and (tempDeletedOperationArrivalTime <= tempScheduledOperationArrivalTime)) or
                            ((tempDeletedOperationFinishTime <= tempScheduledOperationFinishTime) and (tempDeletedOperationArrivalTime >= tempScheduledOperationArrivalTime))):
                        CollisionCounterPerFlow = CollisionCounterPerFlow + 1
                        ListOfCollidedTSNFlows.append(SF)
                        ListOfCollidedLocations.append(convertOperationIDtoEdge(SO.id))
                        waitingTime = tempScheduledOperationFinishTime - tempDeletedOperationArrivalTime
                        listOfWaitingTimes.append(waitingTime)

                    break
                index2 = index2 + 2

        for deletedItem in deletedFlows:
            DF = deletedItem.__getitem__(0)
            if(DF.id == tempDeletedTSNFlow.id):
                continue
            DST = deletedItem.__getitem__(1)
            DFO = map(G, DF, DST)
            index2 = 2
            for DO in DFO[2::2]:
                if (DO.id == tempOperation.id):
                    tempDeletedOperationArrivalTime = tempOperations.__getitem__(index - 1).cumulativeDelay
                    tempDeletedOperationFinishTime = tempOperation.cumulativeDelay
                    deletedOperationArrivalTime = DFO.__getitem__(index2 - 1).cumulativeDelay
                    deletedOperationFinishTime = DO.cumulativeDelay
                    if(((tempDeletedOperationFinishTime >= deletedOperationFinishTime) and (tempDeletedOperationArrivalTime< deletedOperationFinishTime)) or
                            ((tempDeletedOperationFinishTime > deletedOperationArrivalTime) and (tempDeletedOperationArrivalTime <= deletedOperationArrivalTime)) or
                    ((tempDeletedOperationFinishTime <= deletedOperationFinishTime) and (tempDeletedOperationArrivalTime >= deletedOperationArrivalTime))):
                        CollisionCounterPerFlow = CollisionCounterPerFlow + 1
                        ListOfCollidedTSNFlows.append(DF)
                        ListOfCollidedLocations.append(convertOperationIDtoEdge(DO.id))
                        waitingTime = deletedOperationFinishTime - tempDeletedOperationArrivalTime
                        listOfWaitingTimes.append(waitingTime)

                    break
                index2 = index2 + 2


        index = index + 2

    tempDistictedFlowsList = []
    for TSNFlow in ListOfCollidedTSNFlows:
        if TSNFlow.id not in tempDistictedFlowsList:
            distinctCollisionCounterPerFlow = distinctCollisionCounterPerFlow + 1
            tempDistictedFlowsList.append(TSNFlow.id)

    if (distinctCollisionCounterPerFlow > 0):
        listofCollisions.append((tempDeletedTSNFlow, distinctCollisionCounterPerFlow, CollisionCounterPerFlow,
                                 ListOfCollidedTSNFlows, ListOfCollidedLocations,listOfWaitingTimes))


def computeCollisionPerFlow(G, scheduledFlows, deletedFlows, listofCollisions, typeOfSchedulingAlgorithm):         #this function computes collisions and fill the collisions list after the attack type 2 and 3 (remove attack)

    for tempDeletedItem in deletedFlows:
        if(typeOfSchedulingAlgorithm == 0):         # deletedItem in the form of (TSN flow, NextSlot id)
            computeCollisionPerFlowSWTS(G, scheduledFlows, deletedFlows, listofCollisions, tempDeletedItem)
        elif(typeOfSchedulingAlgorithm % 2 == 0):   # deletedItem in the form of (TSN flow, startTime, QueuingDelays list)
            computeCollisionPerFlowSWOTS_WS(G, scheduledFlows, deletedFlows, listofCollisions, tempDeletedItem)
        else:                                       # deletedItem in the form of (TSN flow, startTime)
            computeCollisionPerFlowSWOTS(G, scheduledFlows, deletedFlows, listofCollisions, tempDeletedItem)

    for tempScheduledItem in scheduledFlows:
        if(typeOfSchedulingAlgorithm == 0):         # scheduledItem in the form of (TSN flow, NextSlot id)
            computeCollisionPerFlowSWTS(G, scheduledFlows, deletedFlows, listofCollisions, tempScheduledItem)
        elif(typeOfSchedulingAlgorithm % 2 == 0):   # scheduledItem in the form of (TSN flow, startTime, QueuingDelays list)
            computeCollisionPerFlowSWOTS_WS(G, scheduledFlows, deletedFlows, listofCollisions, tempScheduledItem)
        else:                                       # scheduledItem in the form of (TSN flow, startTime)
            computeCollisionPerFlowSWOTS(G, scheduledFlows, deletedFlows, listofCollisions, tempScheduledItem)


def dropTSNFlowFromCollisionLists(TSNFlow, listofCollisions, collisionList, collisionPerEgressPortCounter):
    newCollisionPerEgressPortCounter = collisionPerEgressPortCounter
    listOfIndeces = []
    index = 0
    for listItem in listofCollisions:
        if(listItem.__getitem__(0) == TSNFlow):
            listOfIndeces.append(index)
        if(TSNFlow in listItem.__getitem__(3)):
            distinctCounter = listItem.__getitem__(1) - 1
            if(distinctCounter == 0):
                listOfIndeces.append(index)
                index = index + 1
                continue
            innerListOfIndeces = []
            totalCounter = listItem.__getitem__(2)
            for i in range(len(listItem.__getitem__(3))):
                if(TSNFlow == (listItem.__getitem__(3)).__getitem__(i)):
                    innerListOfIndeces.append(i)
                    totalCounter = totalCounter - 1

            tempTSNFlow = listItem.__getitem__(0)
            tempTSNFlows = listItem.__getitem__(3)
            tempLocations = listItem.__getitem__(4)
            if len(listItem)>5:
                tempDelays = listItem.__getitem__(5)
                listofCollisions[index] = (tempTSNFlow,distinctCounter,totalCounter,
                                           tempTSNFlows,tempLocations,tempDelays)
            else:
                listofCollisions[index] = (tempTSNFlow, distinctCounter, totalCounter,
                                           tempTSNFlows, tempLocations)


            for i in range(len(innerListOfIndeces)):
                del (listItem.__getitem__(3))[innerListOfIndeces.__getitem__(i) - i]
                del (listItem.__getitem__(4))[innerListOfIndeces.__getitem__(i) - i]
                if (len(listofCollisions.__getitem__(index)) > 5):
                    del (listItem.__getitem__(5))[innerListOfIndeces.__getitem__(i) - i]
        index = index + 1
    for i in range(len(listOfIndeces)):
        del listofCollisions[listOfIndeces.__getitem__(i)-i]


    listOfIndeces = []
    index = 0
    for listItem in collisionList:
        if((listItem.__getitem__(0) == TSNFlow) or (listItem.__getitem__(1) == TSNFlow)):
            newCollisionPerEgressPortCounter = newCollisionPerEgressPortCounter - len(listItem.__getitem__(2))
            listOfIndeces.append(index)
        index = index + 1
    for i in range(len(listOfIndeces)):
        del collisionList[listOfIndeces.__getitem__(i) - i]


    return newCollisionPerEgressPortCounter


def calculateCollisionsStatisticsForAFlow(firstTSNFlow,secondTSNFlow, collisionLocation, listofCollisions):
    nbOfCollisions, nbOfCollidedFlows, nbOfCollisionsWithTheSecondTSNFlow, nbOfDistinctCollidedLocations, nbOfCollisionsInTheLocation = 0, 0, 0, 0, 0
    for deletedItem in listofCollisions:
        if deletedItem.__getitem__(0) == firstTSNFlow:
            nbOfCollisions = deletedItem.__getitem__(2)
            nbOfCollidedFlows = deletedItem.__getitem__(1)
            visitedLocations = []
            for index in range(len(deletedItem.__getitem__(4))):
                if ((deletedItem.__getitem__(3)).__getitem__(index) == secondTSNFlow):
                    nbOfCollisionsWithTheSecondTSNFlow = nbOfCollisionsWithTheSecondTSNFlow + 1
                if ((deletedItem.__getitem__(4)).__getitem__(index) not in visitedLocations):
                    visitedLocations.append((deletedItem.__getitem__(4)).__getitem__(index))
                    nbOfDistinctCollidedLocations = nbOfDistinctCollidedLocations + 1
                if((deletedItem.__getitem__(4)).__getitem__(index) == collisionLocation):
                    nbOfCollisionsInTheLocation = nbOfCollisionsInTheLocation + 1

            break
    return nbOfCollisions, nbOfCollidedFlows, nbOfCollisionsWithTheSecondTSNFlow, nbOfDistinctCollidedLocations, nbOfCollisionsInTheLocation


def orderCollidedFlowsBasedOnNBOfCollisions(TSNFlow, collisionLocation, collisionList, listofCollisions,listOfOrderKeys):

    # Check the correctness of 'listOfOrderKeys'
    ############################################
    a, b, c, d = listOfOrderKeys
    while not (all(v in [0, 1, 2, 3] for v in [a, b, c, d]) and all(x != y for x, y in combinations([a, b, c, d], 2))):
        error_message = "You have to enter the orderkeys as four numbers separated by commas, in this form: a,b,c,d\n*These numbers have to be distinct numbers between 0 and 3 (no two numbers have the same value, where:\n    0 --> nbOfCollisions (total number of collisions)\n    1 --> nbOfCollidedFlows (number of collided flows)\n    2 --> nbOfDistinctCollidedLocations (how many different locations a flow will have a collision at)\n    3 --> nbOfCollisionsInTheLocation (how many collisions a flow will have in the current location)\nThe new values are:"
        orderKeys = input(error_message)
        orderKeysWithoutSpace = orderKeys.replace(" ", "")
        orderKeysList = orderKeysWithoutSpace.split(",")
        try:
            if (len(orderKeysList) > 4):
                raise ValueError('The user entered more than 4 values!')
            integerOrderKeysList = map(int, orderKeysList)
            a, b, c, d = integerOrderKeysList
        except:
            continue
    ############################################

    listOfCollidedPairs = []      # This list contains a pair of collided flows from 'collidedFlowList' in addition to 'TSNFlow'
                                  # So, if 'TSNFlow' has 3 flows that collided with it at 'collisionLocation', which are 'collidedFlowList' = [TSNFlow2,TSNFlow3,TSNFlow4]
                                  # This list 'listOfCollidedPairs' will be in the form: [(TSNFlow,TSNFlow2,nbOfCollisionsBetweenThem,True),(TSNFlow,TSNFlow2,nbOfCol,True),(TSNFlow,TSNFlow3,nbOfCol,True),(TSNFlow2,TSNFlow3,nbOfColl,True),(TSNFlow2,TSNFlow4,nbOfColl,True),(TSNFlow3,TSNFlow4,nbOfColl,False)]

    listOfStatisticsPerFlows = [] # This list contains the following statistics:
                                  # (1) nbOfCollisions, (2) nbOfCollidedFlows, (3) nbOfDistinctCollidedLocations, (4) nbOfCollisionsInTheLocation
                                  # for each collided flow that collide with 'TSNFlow' in 'collisionLocation' including 'TSNFlow'
                                  # in the form of [(TSNFlow Object,nbOfCollisions,nbOfCollidedFlows,nbOfDistinctCollidedLocations,nbOfCollisionsInTheLocation), (AnotherTSNFLow, ... ,..., ..., ...), .......]

    collidedFlowList = computeListOfCollisionsForAFlowInEgressPort(collisionList, collisionLocation, TSNFlow)
    if(len(collidedFlowList)==0):
        return listOfStatisticsPerFlows, listOfCollidedPairs
    nbOfCollisions, nbOfCollidedFlows, nbOfCollisionsWithTheSecondTSNFlow, nbOfDistinctCollidedLocations, nbOfCollisionsInTheLocation = calculateCollisionsStatisticsForAFlow(TSNFlow,collidedFlowList.__getitem__(0),collisionLocation,listofCollisions)
    listOfStatisticsPerFlows.append((TSNFlow,nbOfCollisions,nbOfCollidedFlows,nbOfDistinctCollidedLocations,nbOfCollisionsInTheLocation))
    listOfCollidedPairs.append((TSNFlow,collidedFlowList.__getitem__(0),nbOfCollisionsWithTheSecondTSNFlow,True))

    for index in range(1,len(collidedFlowList)):
        nbOfCollisions, nbOfCollidedFlows, nbOfCollisionsWithTheSecondTSNFlow, nbOfDistinctCollidedLocations, nbOfCollisionsInTheLocation = calculateCollisionsStatisticsForAFlow(TSNFlow,collidedFlowList.__getitem__(index),collisionLocation,listofCollisions)
        listOfCollidedPairs.append((TSNFlow, collidedFlowList.__getitem__(index), nbOfCollisionsWithTheSecondTSNFlow,True))

    for index1 in range(0,len(collidedFlowList)):
        if (index1 + 1) == len(collidedFlowList):
            nbOfCollisions, nbOfCollidedFlows, nbOfCollisionsWithTheSecondTSNFlow, nbOfDistinctCollidedLocations, nbOfCollisionsInTheLocation = calculateCollisionsStatisticsForAFlow(collidedFlowList.__getitem__(index1), collidedFlowList.__getitem__(index1 -1), collisionLocation,listofCollisions)
            listOfStatisticsPerFlows.append((collidedFlowList.__getitem__(index1), nbOfCollisions, nbOfCollidedFlows,
                                            nbOfDistinctCollidedLocations,
                                            nbOfCollisionsInTheLocation))
        else:
            tempCollidedFlows = computeListOfCollisionsForAFlowInEgressPort(collisionList,collisionLocation,collidedFlowList.__getitem__(index1))
            nbOfCollisions, nbOfCollidedFlows, nbOfCollisionsWithTheSecondTSNFlow, nbOfDistinctCollidedLocations, nbOfCollisionsInTheLocation = calculateCollisionsStatisticsForAFlow(
                collidedFlowList.__getitem__(index1), collidedFlowList.__getitem__(index1+1), collisionLocation, listofCollisions)
            listOfStatisticsPerFlows.append((collidedFlowList.__getitem__(index1), nbOfCollisions, nbOfCollidedFlows, nbOfDistinctCollidedLocations,
                                            nbOfCollisionsInTheLocation))
            if(collidedFlowList.__getitem__(index1+1) in tempCollidedFlows):
                listOfCollidedPairs.append((collidedFlowList.__getitem__(index1), collidedFlowList.__getitem__(index1+1), nbOfCollisionsWithTheSecondTSNFlow,True))
            else:
                listOfCollidedPairs.append((collidedFlowList.__getitem__(index1),
                                            collidedFlowList.__getitem__(index1 + 1),
                                            nbOfCollisionsWithTheSecondTSNFlow, False))

        for index2 in range(index1+2,len(collidedFlowList)):
            nbOfCollisions, nbOfCollidedFlows, nbOfCollisionsWithTheSecondTSNFlow, nbOfDistinctCollidedLocations, nbOfCollisionsInTheLocation = calculateCollisionsStatisticsForAFlow(
                collidedFlowList.__getitem__(index1), collidedFlowList.__getitem__(index2), collisionLocation, listofCollisions)
            if(collidedFlowList.__getitem__(index2) in tempCollidedFlows):
                listOfCollidedPairs.append((collidedFlowList.__getitem__(index1), collidedFlowList.__getitem__(index2), nbOfCollisionsWithTheSecondTSNFlow,True))
            else:
                listOfCollidedPairs.append((collidedFlowList.__getitem__(index1), collidedFlowList.__getitem__(index2),
                                            nbOfCollisionsWithTheSecondTSNFlow, False))

    orderedListOfStatisticsPerFlows = sorted(listOfStatisticsPerFlows, key=lambda x: (x.__getitem__(a+1), x.__getitem__(b+1),x.__getitem__(c+1),x.__getitem__(d+1)), reverse=True)
    orderedListOfCollidedPairs = sorted(listOfCollidedPairs, key=lambda x: (x.__getitem__(2)), reverse=True)


    return orderedListOfStatisticsPerFlows, orderedListOfCollidedPairs



    


def dropBasedOnTheHighestNBOfCollisions2(listofCollisions, collisionList, collisionPerEgressPortCounter):
    listofCollisionsV2, collisionListV2 = copyCollisionlists(listofCollisions, collisionList)
    newCollisionPerEgressPortCounter = collisionPerEgressPortCounter
    listOfDropedFlows = []
    listOfOrderKeys = [1,2,0,3]         # the collided flows will be descendingly ordered (from high to low) based on the keys in this list from left to right, where:
                                        # 0 --> nbOfCollisions (total number of collisions) a flow may collide more than once with another flow in different locations. This counter will count them all
                                        # 1 --> nbOfCollidedFlows (number of collided flows) a flow may collide more than once in different locations with another flow but it will be counted as one in this counter
                                        # 2 --> nbOfDistinctCollidedLocations (how many different locations a flow will have a collision at)
                                        # 3 --> nbOfCollisionsInTheLocation (how many collisions a flow will have in the current location)
                                        # Based on this list a flow will be drop
                                        # The default order is [1,2,0,3], which means if a collision occur, we will drop the flow with the highest 'nbOfCollidedFlows', if we have two flows with the same 'nbOfCollidedFlows',
                                        #               we will drop the one with the highest 'nbOfDistinctCollidedLocations', and so on.

    for listItem in listofCollisions:
        if(listItem.__getitem__(0) in listOfDropedFlows):
            continue
        for collisionLocation in listItem.__getitem__(4):

            orderedListOfStatisticsPerFlows, orderedListOfCollidedPairs = orderCollidedFlowsBasedOnNBOfCollisions(listItem.__getitem__(0), collisionLocation, collisionListV2, listofCollisionsV2,listOfOrderKeys)
            if(len(orderedListOfStatisticsPerFlows) == 0):
                continue
            if((orderedListOfCollidedPairs.__getitem__(len(orderedListOfCollidedPairs)-1).__getitem__(3)) or (orderedListOfStatisticsPerFlows.__getitem__(len(orderedListOfStatisticsPerFlows)-1) == listItem.__getitem__(0))):
                for index in range(len(orderedListOfStatisticsPerFlows)-1):
                    listOfDropedFlows.append(orderedListOfStatisticsPerFlows.__getitem__(index).__getitem__(0))
                    newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(orderedListOfStatisticsPerFlows.__getitem__(index).__getitem__(0),listofCollisionsV2,collisionListV2,newCollisionPerEgressPortCounter)
                if (listItem.__getitem__(0) in listOfDropedFlows):
                    break
            else:
                startPosition = 0
                while(orderedListOfStatisticsPerFlows.__getitem__(startPosition).__getitem__(0) != listItem.__getitem__(0)):
                    listOfDropedFlows.append(orderedListOfStatisticsPerFlows.__getitem__(startPosition).__getitem__(0))
                    newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(
                        orderedListOfStatisticsPerFlows.__getitem__(startPosition).__getitem__(0), listofCollisionsV2,
                        collisionListV2, newCollisionPerEgressPortCounter)
                    startPosition = startPosition + 1

                listOfDropedFlows.append(orderedListOfStatisticsPerFlows.__getitem__(startPosition).__getitem__(0))
                newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(
                    orderedListOfStatisticsPerFlows.__getitem__(startPosition).__getitem__(0), listofCollisionsV2,
                    collisionListV2, newCollisionPerEgressPortCounter)
                startPosition = startPosition + 1

                for index in range(startPosition,len(orderedListOfStatisticsPerFlows)-1):
                    flag = False
                    currentTSNFlow = orderedListOfStatisticsPerFlows.__getitem__(index).__getitem__(0)
                    for collidedPair in orderedListOfCollidedPairs:
                        firstCollidedTSNFlow = collidedPair.__getitem__(0)
                        secondCollidedTSNFlow = collidedPair.__getitem__(1)
                        isThereACollisionAtTheLocation = collidedPair.__getitem__(2)
                        if(((currentTSNFlow == firstCollidedTSNFlow) or (currentTSNFlow == secondCollidedTSNFlow)) and not (isThereACollisionAtTheLocation)):
                            flag = True
                    if flag:
                        break
                    listOfDropedFlows.append(currentTSNFlow)
                    newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(
                        currentTSNFlow, listofCollisionsV2,
                        collisionListV2, newCollisionPerEgressPortCounter)

    return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter,listOfDropedFlows


def dropBasedOnTheHighestNBOfCollisions(listofCollisions, collisionList, collisionPerEgressPortCounter):
    listofCollisionsV2, collisionListV2 = copyCollisionlists(listofCollisions, collisionList)
    newCollisionPerEgressPortCounter = collisionPerEgressPortCounter
    listOfDropedFlows = []
    listOfOrderKeys = [1,2,0,3]         # the collided flows will be descendingly ordered (from high to low) based on the keys in this list from left to right, where:
                                        # 0 --> nbOfCollisions (total number of collisions) a flow may collide more than once with another flow in different locations. This counter will count them all
                                        # 1 --> nbOfCollidedFlows (number of collided flows) a flow may collide more than once in different locations with another flow but it will be counted as one in this counter
                                        # 2 --> nbOfDistinctCollidedLocations (how many different locations a flow will have a collision at)
                                        # 3 --> nbOfCollisionsInTheLocation (how many collisions a flow will have in the current location)
                                        # Based on this list a flow will be drop
                                        # The default order is [1,2,0,3], which means if a collision occur, we will drop the flow with the highest 'nbOfCollidedFlows', if we have two flows with the same 'nbOfCollidedFlows',
                                        #               we will drop the one with the highest 'nbOfDistinctCollidedLocations', and so on.

    for listItem in listofCollisions:
        flag = False
        if(listItem.__getitem__(0) in listOfDropedFlows):
            continue
        for collisionLocation in listItem.__getitem__(4):
            orderedListOfStatisticsPerFlows, orderedListOfCollidedPairs = orderCollidedFlowsBasedOnNBOfCollisions(
                listItem.__getitem__(0), collisionLocation, collisionListV2, listofCollisionsV2, listOfOrderKeys)
            endCondition = len(orderedListOfStatisticsPerFlows) -1
            for i in range(endCondition):
                orderedListOfStatisticsPerFlows, orderedListOfCollidedPairs = orderCollidedFlowsBasedOnNBOfCollisions(
                    listItem.__getitem__(0), collisionLocation, collisionListV2, listofCollisionsV2, listOfOrderKeys)
                tempTSNFlow = orderedListOfStatisticsPerFlows.__getitem__(0).__getitem__(0)
                if(tempTSNFlow == listItem.__getitem__(0)):
                    flag = True
                listOfDropedFlows.append(tempTSNFlow)
                newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(
                    tempTSNFlow, listofCollisionsV2,
                    collisionListV2, newCollisionPerEgressPortCounter)
                if (flag):
                    break
            if(flag):
                break



    return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter,listOfDropedFlows


def getSchedulingDetails(TSNFlow, scheduledFlows, deletedScheduledFlows):
    for scheduleItem in scheduledFlows:
        if (scheduleItem.__getitem__(0) == TSNFlow):
            return scheduleItem
    for deletedItem in deletedScheduledFlows:
        if(deletedItem.__getitem__(0) == TSNFlow):
            return deletedItem


def getOperationIndexByOperationID(operations, operationID):
    for i in range(len(operations)):
        if operationID == operations.__getitem__(i).id:
            return i
    return -1

def orderCollidedFlowsBasedOnTheSoonestDeadline(G,TSNFlow, collisionLocation, scheduledFlows, deletedScheduledFlows, collisionList):
    orderedListOfCollidedFlowsBySoonestDeadline = [] # This list is ordered by the left deadline from the short to long
    unorderedListOfCollidedFlowsBySoonestDeadline = []
    collidedFlowList = computeListOfCollisionsForAFlowInEgressPort(collisionList, collisionLocation, TSNFlow)
    if (len(collidedFlowList) == 0):
        return orderedListOfCollidedFlowsBySoonestDeadline
    scheduleItem = getSchedulingDetails(TSNFlow,scheduledFlows, deletedScheduledFlows)
    operationID = convertEdgetoOperationID(collisionLocation)
    if(len(scheduleItem)==2):
        operations = map(G,TSNFlow,scheduleItem.__getitem__(1))
        operationIndex = getOperationIndexByOperationID(operations,operationID)
        leftDeadline = TSNFlow.flowMaxDelay - (operations.__getitem__(operationIndex-1).cumulativeDelay - scheduleItem.__getitem__(1))
        unorderedListOfCollidedFlowsBySoonestDeadline.append((TSNFlow,leftDeadline))
        for tempTSNFlow in collidedFlowList:
            scheduleItem = getSchedulingDetails(tempTSNFlow, scheduledFlows, deletedScheduledFlows)
            operations = map(G, tempTSNFlow, scheduleItem.__getitem__(1))
            operationIndex = getOperationIndexByOperationID(operations, operationID)
            leftDeadline = tempTSNFlow.flowMaxDelay - (
                        operations.__getitem__(operationIndex - 1).cumulativeDelay - scheduleItem.__getitem__(1))
            unorderedListOfCollidedFlowsBySoonestDeadline.append((tempTSNFlow, leftDeadline))

    else:
        operations = map_ws(G, TSNFlow, scheduleItem.__getitem__(1),scheduleItem.__getitem__(2))
        operationIndex = getOperationIndexByOperationID(operations, operationID)
        queueIndex = int((operationIndex/2)-1)
        leftDeadline = TSNFlow.flowMaxDelay - (
                    operations.__getitem__(operationIndex - 1).cumulativeDelay + scheduleItem.__getitem__(2).__getitem__(queueIndex) - scheduleItem.__getitem__(1))
        unorderedListOfCollidedFlowsBySoonestDeadline.append((TSNFlow, leftDeadline))
        for tempTSNFlow in collidedFlowList:
            scheduleItem = getSchedulingDetails(tempTSNFlow, scheduledFlows, deletedScheduledFlows)
            operations = map_ws(G, tempTSNFlow, scheduleItem.__getitem__(1),scheduleItem.__getitem__(2))
            operationIndex = getOperationIndexByOperationID(operations, operationID)
            queueIndex = int((operationIndex / 2) - 1)
            leftDeadline = tempTSNFlow.flowMaxDelay - (
                    operations.__getitem__(operationIndex - 1).cumulativeDelay + scheduleItem.__getitem__(2).__getitem__(queueIndex) - scheduleItem.__getitem__(1))
            unorderedListOfCollidedFlowsBySoonestDeadline.append((tempTSNFlow, leftDeadline))



    orderedListOfCollidedFlowsBySoonestDeadline = sorted(unorderedListOfCollidedFlowsBySoonestDeadline, key=lambda x: (x.__getitem__(1)), reverse=False)
    return orderedListOfCollidedFlowsBySoonestDeadline



def dropBasedOnTheSoonestDeadline(G,scheduledFlows, deletedScheduledFlows, listofCollisions, collisionList, collisionPerEgressPortCounter):
    listofCollisionsV2, collisionListV2 = copyCollisionlists(listofCollisions, collisionList)
    newCollisionPerEgressPortCounter = collisionPerEgressPortCounter
    listOfDropedFlows = []


    for listItem in listofCollisions:
        flag = False
        if (listItem.__getitem__(0) in listOfDropedFlows):
            continue
        for collisionLocation in listItem.__getitem__(4):
            orderedListOfCollidedFlowsBySoonestDeadline = orderCollidedFlowsBasedOnTheSoonestDeadline(G,listItem.__getitem__(0), collisionLocation,scheduledFlows, deletedScheduledFlows, collisionListV2)
            endCondition = len(orderedListOfCollidedFlowsBySoonestDeadline) - 1
            for i in range(endCondition):
                tempTSNFlow = orderedListOfCollidedFlowsBySoonestDeadline.__getitem__(i).__getitem__(0)
                if (tempTSNFlow == listItem.__getitem__(0)):
                    flag = True
                listOfDropedFlows.append(tempTSNFlow)
                newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(
                    tempTSNFlow, listofCollisionsV2,
                    collisionListV2, newCollisionPerEgressPortCounter)
                if (flag):
                    break
            if (flag):
                break

    return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows


def orderCollidedFlowsBasedOnTheShortestDelay(TSNFlow, collisionLocation, collisionList,listOfCollision):
    orderedListOfCollidedFlowsByShortestDelay = []  # This list is ordered by the shortest delay from the short delay to the high one
                                                    # The delay is the maximum delay a flow encounters in an egrees port by delaying its start time after the
                                                    #       finish time of the other TSN flow. So if flow1 collide with flow2 and flow3 at egress port '(1,2)',
                                                    #       and the delay caused by flow2 to flow1 (since we will make it start before flow1) is 4 and the delay
                                                    #       caused by flow3 to flow1 is 3, an entry to this list will be in this form: [(flow1,flow2,4)]. Where flow1
                                                    #       is the current flow and flow2 is the flow that cause the highest delay and 4 is the amount of the delay.
                                                    # when we get the full list of all the flows that collided with 'TSNFlow', we ordered it by the shortest delay
    unorderedListOfCollidedFlowsByShortestDelay = []
    collidedFlowList = computeListOfCollisionsForAFlowInEgressPort(collisionList, collisionLocation, TSNFlow)
    collidedWaitingTimes = getWaitingTimeForAFlowInEgressPort(listOfCollision,collisionLocation,TSNFlow)
    if (len(collidedFlowList) == 0):
        return orderedListOfCollidedFlowsByShortestDelay
    maxWaitingTime = 0
    secondTSNFlow = None
    for i in range(len(collidedFlowList)):
        if (collidedWaitingTimes.__getitem__(i)>maxWaitingTime):
            maxWaitingTime = collidedWaitingTimes.__getitem__(i)
            secondTSNFlow = collidedFlowList.__getitem__(i)

    unorderedListOfCollidedFlowsByShortestDelay.append((TSNFlow, secondTSNFlow, maxWaitingTime))
    for tempTSNFlow in collidedFlowList:
        anotherCollidedFlowList = computeListOfCollisionsForAFlowInEgressPort(collisionList, collisionLocation, tempTSNFlow)
        collidedWaitingTimes = getWaitingTimeForAFlowInEgressPort(listOfCollision, collisionLocation, tempTSNFlow)
        maxWaitingTime = collidedWaitingTimes.__getitem__(anotherCollidedFlowList.index(TSNFlow))
        secondTSNFlow = TSNFlow
        for secondTempTSNFlow in collidedFlowList:
            if (secondTempTSNFlow == tempTSNFlow):
                continue
            if(secondTempTSNFlow in anotherCollidedFlowList):
                waitingTime = collidedWaitingTimes.__getitem__(anotherCollidedFlowList.index(secondTempTSNFlow))
                if(waitingTime> maxWaitingTime):
                    secondTSNFlow = secondTempTSNFlow
                    maxWaitingTime = waitingTime

        unorderedListOfCollidedFlowsByShortestDelay.append((tempTSNFlow, secondTSNFlow,maxWaitingTime))



    orderedListOfCollidedFlowsByShortestDelay = sorted(unorderedListOfCollidedFlowsByShortestDelay,
                                                         key=lambda x: (x.__getitem__(2)), reverse=False)
    return orderedListOfCollidedFlowsByShortestDelay


def dropBasedOnTheShortestDelay(listofCollisions, collisionList, collisionPerEgressPortCounter):
    listofCollisionsV2, collisionListV2 = copyCollisionlists(listofCollisions, collisionList)
    newCollisionPerEgressPortCounter = collisionPerEgressPortCounter
    listOfDropedFlows = []

    for listItem in listofCollisions:
        flag = False
        if (listItem.__getitem__(0) in listOfDropedFlows):
            continue
        for collisionLocation in listItem.__getitem__(4):
            orderedListOfCollidedFlowsByShortestDelay = orderCollidedFlowsBasedOnTheShortestDelay(listItem.__getitem__(0),collisionLocation,
                                                                                                              collisionListV2,listofCollisionsV2)
            endCondition = len(orderedListOfCollidedFlowsByShortestDelay) - 1
            for i in range(endCondition):
                orderedListOfCollidedFlowsByShortestDelay = orderCollidedFlowsBasedOnTheShortestDelay(listItem.__getitem__(0),collisionLocation,collisionListV2,listofCollisionsV2)
                tempTSNFlow = orderedListOfCollidedFlowsByShortestDelay.__getitem__(len(orderedListOfCollidedFlowsByShortestDelay)-1).__getitem__(1)
                if (tempTSNFlow == listItem.__getitem__(0)):
                    flag = True
                listOfDropedFlows.append(tempTSNFlow)
                newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(tempTSNFlow, listofCollisionsV2,
                    collisionListV2, newCollisionPerEgressPortCounter)
                if (flag):
                    break
            if (flag):
                break

    return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows


def orderCollidedFlowsBasedOnTheEarliestArrivalTime(G, TSNFlow, collisionLocation, scheduledFlows, deletedScheduledFlows,
                                                    collisionList):
    orderedListOfCollidedFlowsByEarliestArrivalTime = []  # This list is ordered by the arrival time from the latest to the soonest
    unorderedListOfCollidedFlowsByEarliestArrivalTime = []
    collidedFlowList = computeListOfCollisionsForAFlowInEgressPort(collisionList, collisionLocation, TSNFlow)
    if (len(collidedFlowList) == 0):
        return orderedListOfCollidedFlowsByEarliestArrivalTime
    scheduleItem = getSchedulingDetails(TSNFlow, scheduledFlows, deletedScheduledFlows)
    operationID = convertEdgetoOperationID(collisionLocation)
    if (len(scheduleItem) == 2):
        operations = map(G, TSNFlow, scheduleItem.__getitem__(1))
        operationIndex = getOperationIndexByOperationID(operations, operationID)
        arrivalTime = operations.__getitem__(operationIndex - 1).cumulativeDelay
        unorderedListOfCollidedFlowsByEarliestArrivalTime.append((TSNFlow, arrivalTime))
        for tempTSNFlow in collidedFlowList:
            scheduleItem = getSchedulingDetails(tempTSNFlow, scheduledFlows, deletedScheduledFlows)
            operations = map(G, tempTSNFlow, scheduleItem.__getitem__(1))
            operationIndex = getOperationIndexByOperationID(operations, operationID)
            arrivalTime = operations.__getitem__(operationIndex - 1).cumulativeDelay
            unorderedListOfCollidedFlowsByEarliestArrivalTime.append((tempTSNFlow, arrivalTime))

    else:
        operations = map_ws(G, TSNFlow, scheduleItem.__getitem__(1), scheduleItem.__getitem__(2))
        operationIndex = getOperationIndexByOperationID(operations, operationID)
        queueIndex = int((operationIndex / 2) - 1)
        arrivalTime = operations.__getitem__(operationIndex - 1).cumulativeDelay + scheduleItem.__getitem__(2).__getitem__(
            queueIndex)
        unorderedListOfCollidedFlowsByEarliestArrivalTime.append((TSNFlow, arrivalTime))
        for tempTSNFlow in collidedFlowList:
            scheduleItem = getSchedulingDetails(tempTSNFlow, scheduledFlows, deletedScheduledFlows)
            operations = map_ws(G, tempTSNFlow, scheduleItem.__getitem__(1), scheduleItem.__getitem__(2))
            operationIndex = getOperationIndexByOperationID(operations, operationID)
            queueIndex = int((operationIndex / 2) - 1)
            arrivalTime = operations.__getitem__(operationIndex - 1).cumulativeDelay + scheduleItem.__getitem__(
                2).__getitem__(queueIndex)
            unorderedListOfCollidedFlowsByEarliestArrivalTime.append((tempTSNFlow, arrivalTime))

    orderedListOfCollidedFlowsByEarliestArrivalTime = sorted(unorderedListOfCollidedFlowsByEarliestArrivalTime,
                                                         key=lambda x: (x.__getitem__(1)), reverse=True)
    return orderedListOfCollidedFlowsByEarliestArrivalTime


def dropBasedOnTheEarliestArrivalTime(G, scheduledFlows, deletedScheduledFlows, listofCollisions, collisionList, collisionPerEgressPortCounter):

    listofCollisionsV2, collisionListV2 = copyCollisionlists(listofCollisions, collisionList)
    newCollisionPerEgressPortCounter = collisionPerEgressPortCounter
    listOfDropedFlows = []

    for listItem in listofCollisions:
        flag = False
        if (listItem.__getitem__(0) in listOfDropedFlows):
            continue
        for collisionLocation in listItem.__getitem__(4):
            orderedListOfCollidedFlowsByEarliestArrivalTime = orderCollidedFlowsBasedOnTheEarliestArrivalTime(G,listItem.__getitem__(0),collisionLocation,scheduledFlows,deletedScheduledFlows,collisionListV2)
            endCondition = len(orderedListOfCollidedFlowsByEarliestArrivalTime) - 1
            for i in range(endCondition):
                tempTSNFlow = orderedListOfCollidedFlowsByEarliestArrivalTime.__getitem__(i).__getitem__(0)
                if (tempTSNFlow == listItem.__getitem__(0)):
                    flag = True
                listOfDropedFlows.append(tempTSNFlow)
                newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(
                    tempTSNFlow, listofCollisionsV2,
                    collisionListV2, newCollisionPerEgressPortCounter)
                if (flag):
                    break
            if (flag):
                break

    return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows

def collisionResolveByDropping(G,scheduledFlows, deletedScheduledFlows,listofCollisions, collisionList,collisionPerEgressPortCounter, selectAlgorithm):
    if(selectAlgorithm == 0):
        listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows = dropBasedOnTheHighestNBOfCollisions(listofCollisions, collisionList,collisionPerEgressPortCounter)
        return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows
    elif(selectAlgorithm == 1):
        listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows = dropBasedOnTheSoonestDeadline(G,scheduledFlows, deletedScheduledFlows,listofCollisions, collisionList, collisionPerEgressPortCounter)
        return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows
    elif(selectAlgorithm == 2):
        listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows = dropBasedOnTheShortestDelay(listofCollisions, collisionList, collisionPerEgressPortCounter)
        return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows
    else:
        listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows = dropBasedOnTheEarliestArrivalTime(
            G, scheduledFlows, deletedScheduledFlows, listofCollisions, collisionList, collisionPerEgressPortCounter)
        return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows


def collisionResolveByDelaying(listofCollisions, collisionList, selectAlgorithm):
    pass


def collisionResolve(G,scheduledFlows, deletedScheduledFlows,listofCollisions, collisionList, collisionPerEgressPortCounter, resolveMethod, selectAlgorithm):
    # This function takes:
    # (1-2) The two list of collisions
    # (3)   The resolve method (0 for drop, 1 for delay)
    # (4)   The select algorithm (0 for the highest number of distinct collisions
    #                             1 for the soonest deadline
    #                             2 for the shortest resulted delay between the two collided flows
    #                             3 for the normal (earliest arrival time)
    # Then, it updates the list accordingly
    if (resolveMethod == 0):
        listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows = collisionResolveByDropping(G,scheduledFlows, deletedScheduledFlows,listofCollisions, collisionList, collisionPerEgressPortCounter, selectAlgorithm)
        return listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows
    else:
        collisionResolveByDelaying(listofCollisions, collisionList, selectAlgorithm)


def copyCollisionlists(listofCollisions, collisionList):
    copyOfListofCollisions = []
    copyOfCollisionList = []

    for listElement in listofCollisions:
        tempTSNFlow = listElement.__getitem__(0)
        tempDisCounter = listElement.__getitem__(1)
        tempCounter = listElement.__getitem__(2)
        tempTSNFlows = listElement.__getitem__(3)
        tempCollidedLocations = listElement.__getitem__(4)

        copyOfTSNFlows = []
        copyOfCollidedLocations = []
        if(len(listElement)>5):
            tempDelays = listElement.__getitem__(5)
            copyOfDelays = []
        for i in range(len(tempTSNFlows)):
            copyOfTSNFlows.append(tempTSNFlows.__getitem__(i))
            copyOfCollidedLocations.append(tempCollidedLocations.__getitem__(i))
            if (len(listElement) > 5):
                copyOfDelays.append(tempDelays.__getitem__(i))
        if (len(listElement) > 5):
            copyOfListofCollisions.append((tempTSNFlow,tempDisCounter,tempCounter,copyOfTSNFlows,copyOfCollidedLocations,copyOfDelays))
        else:
            copyOfListofCollisions.append(
                    (tempTSNFlow, tempDisCounter, tempCounter, copyOfTSNFlows, copyOfCollidedLocations))

    for listElement in collisionList:
        tempFirstTSNFlow = listElement.__getitem__(0)
        tempSecondTSNFlow = listElement.__getitem__(1)
        tempCollidedLocations = listElement.__getitem__(2)
        copyOfCollidedLocations = []
        if(len(listElement)> 3):
            tempDelays = listElement.__getitem__(3)
            copyOfDelays = []
        for i in range(len(tempCollidedLocations)):
            copyOfCollidedLocations.append(tempCollidedLocations.__getitem__(i))
            if (len(listElement) > 3):
                copyOfDelays.append(tempDelays.__getitem__(i))

        if (len(listElement) > 3):
            copyOfCollisionList.append((tempFirstTSNFlow,tempSecondTSNFlow,copyOfCollidedLocations,copyOfDelays))
        else:
            copyOfCollisionList.append((tempFirstTSNFlow,tempSecondTSNFlow,copyOfCollidedLocations))

    return copyOfListofCollisions, copyOfCollisionList










def insertAttack(G, hostsList , firstKthPaths, timeSlotsAmount, nbOfTSNFlows, pFlow, TSNCountWeight, bandwidthWeight, hopCountWeight,
                 typeOfSecurityAttack, attackRate, attackStartTime, typeofSchedulingAlgorithm):
    CLength = 0  # the schedule cycle length
    timeSlotLength = 0  # the length of each time slot

    # Setting the values:
    timeSlotLength = computeTimeSlotLength(G, hostsList, firstKthPaths)
    CLength = timeSlotsAmount * timeSlotLength
    timeSlots = createTimeSlots(timeSlotsAmount)  # the list of time slots
    flowsList = []  # list of all created TSN flows
    scheduledFlows = []  # list of all scheduled TSN flows using SWOTS (As Early As Possible) with queueing delays allowed
    counter = 0  # count the created real TSN flows
    counterTotal = 0  # count the total created flows (real and fake)
    scheduledCounter = 0  # count the scheduled TSN flows (routed and scheduled) using SWOTS (As Early As Possible) with queueing delays allowed
    routedCounter = 0  # count the routed real TSN flows, but not scheduled
    totalRoutedCounter = 0  # count the total routed TSN flows (real and fake), but not scheduled
    time = 0  # Track the arrival time of TSN flows
    routingExecutionTimes = []  # a list of the execution times of the routing algorithm for all flows in microseconds [(1.3,True),(0.7,False)]
    SchedulingExecutionTimes = []  # a list of the execution times of the SWOTS (As Early As Possible) algorithm for all flows in microseconds [(1.3,True),(0.7,False)]
    theAmountofFakeFlows = attackRate * nbOfTSNFlows
    while (True):
        if counterTotal >= nbOfTSNFlows + theAmountofFakeFlows:  # if we reached the number of TSN flows, stop
            break
        elif (counter > nbOfTSNFlows):
            attackRate = 1
        changeLinksBandwidth(
            G)  # change the link bandwidth randomly, in future it will be based on the best effort streams
        x = random.random()
        if (x <= pFlow):

            s = 0
            d = 0
            while s == d:
                s = random.choice(hostsList)
                d = random.choice(hostsList)
            tempTSNFlow = TSNFlow.TSNFlow(counterTotal, s,
                                          d)  # generate a TSN flow from a randomly selected source to a randomly selected destination
            flowsList.append(
                (tempTSNFlow, time))  # add the generated TSN flow and the generation time to the TSN flows list
            counterTotal = counterTotal + 1
            fakeFlow = False  # this parameter to indicate if the flow is real or generated by the attacker
            x = random.random()

            if (x <= attackRate and counter / nbOfTSNFlows > attackStartTime):
                fakeFlow = True
            if (not fakeFlow):
                counter = counter + 1  # increment the real TSN flows counter by 1

            tempScheduled = False
            tempRoutingList = firstKthPaths
            flag = 0
            while (tempScheduled == False):
                # Path-Selection phase #
                ##########################################
                start = timer()
                tempRouted, candidatePaths = pathSelection(G, tempTSNFlow, tempRoutingList, TSNCountWeight,
                                                           bandwidthWeight, hopCountWeight, flag)
                end = timer()
                routingExecutionTimes.append((((end - start) * 1000 * 1000), tempRouted))

                ##########################################

                if (tempRouted and flag == 0):
                    totalRoutedCounter = totalRoutedCounter + 1
                    if ((not fakeFlow)):
                        routedCounter = routedCounter + 1
                # elif (not (tempRouted)):  # This statement was else (which will prevent the method)
                else:
                    break
                flag = 1

                for path in candidatePaths:
                    if (path == tempTSNFlow.path):
                        candidatePaths.remove(path)
                tempRoutingList = candidatePaths

                if (not tempScheduled):
                    if (len(flowsList) == 0):
                        FTT = time
                    else:
                        FTT = flowsList.__getitem__(0).__getitem__(1)

                    # Scheduling Phase #
                    ##########################################
                    if (typeOfSecurityAttack == 0):
                        if (typeofSchedulingAlgorithm == 4):
                            start = timer()
                            tempScheduled = SWOTS_AEAP_WS(G, tempTSNFlow, scheduledFlows,
                                                          CLength)
                            end = timer()
                        elif (typeofSchedulingAlgorithm == 3):
                            start = timer()
                            tempScheduled = SWOTS_AEAP(G, tempTSNFlow, scheduledFlows,
                                                       CLength)
                            end = timer()
                        elif (typeofSchedulingAlgorithm == 2):
                            start = timer()
                            tempScheduled = SWOTS_ASAP_WS(G, tempTSNFlow, scheduledFlows,
                                                          CLength, time, FTT)
                            end = timer()
                        elif (typeofSchedulingAlgorithm == 1):
                            start = timer()
                            tempScheduled = SWOTS_ASAP(G, tempTSNFlow, scheduledFlows,
                                                       CLength, time, FTT)
                            end = timer()
                        elif (typeofSchedulingAlgorithm == 0):
                            start = timer()
                            tempScheduled = SWTS(G, tempTSNFlow, scheduledFlows,
                                                 CLength, timeSlots, time, FTT)
                            end = timer()

                        SchedulingExecutionTimes.append(
                            (((end - start) * 1000 * 1000), tempScheduled))

                        if (tempScheduled):
                            if (not fakeFlow):
                                scheduledCounter = scheduledCounter + 1
                            for index in range(len(tempTSNFlow.path.nodes)):
                                if (index == 0 or index > len(tempTSNFlow.path.nodes) - 3):
                                    continue
                                G[tempTSNFlow.path.nodes.__getitem__(index)][
                                    tempTSNFlow.path.nodes.__getitem__(index + 1)][
                                    'nbOfTSN'] = \
                                    G[tempTSNFlow.path.nodes.__getitem__(index)][
                                        tempTSNFlow.path.nodes.__getitem__(index + 1)][
                                        'nbOfTSN'] + 1

                    elif (typeOfSecurityAttack == 1):
                        if (fakeFlow):
                            tempScheduled = True
                            if (typeofSchedulingAlgorithm == 0):
                                scheduledFlows.append((tempTSNFlow, random.randint(0, len(timeSlots) - 1)))
                            else:
                                latestPossibleTime = CLength - tempTSNFlow.flowMaxDelay
                                if (latestPossibleTime < 0):
                                    transmissionStartTime = 0
                                else:
                                    transmissionStartTime = random.randint(0, latestPossibleTime)

                                if (typeofSchedulingAlgorithm % 2 == 0):
                                    avgQueuingDelay = computeAvgQueuingDelayPerFlowPerHop(scheduledFlows)
                                    queuingDelays = [random.randint(
                                        int(avgQueuingDelay - (avgQueuingDelay / (len(tempTSNFlow.path.nodes) - 2))),
                                        int(avgQueuingDelay + (avgQueuingDelay / (len(tempTSNFlow.path.nodes) - 2))))
                                                     for _ in range(len(tempTSNFlow.path.nodes) - 2)]
                                    scheduledFlows.append((tempTSNFlow, transmissionStartTime, queuingDelays))
                                else:
                                    scheduledFlows.append((tempTSNFlow, transmissionStartTime))


                        else:
                            if (typeofSchedulingAlgorithm == 4):
                                start = timer()
                                tempScheduled = SWOTS_AEAP_WS(G, tempTSNFlow, scheduledFlows,
                                                              CLength)
                                end = timer()
                            elif (typeofSchedulingAlgorithm == 3):
                                start = timer()
                                tempScheduled = SWOTS_AEAP(G, tempTSNFlow, scheduledFlows,
                                                           CLength)
                                end = timer()
                            elif (typeofSchedulingAlgorithm == 2):
                                start = timer()
                                tempScheduled = SWOTS_ASAP_WS(G, tempTSNFlow, scheduledFlows,
                                                              CLength, time, FTT)
                                end = timer()
                            elif (typeofSchedulingAlgorithm == 1):
                                start = timer()
                                tempScheduled = SWOTS_ASAP(G, tempTSNFlow, scheduledFlows,
                                                           CLength, time, FTT)
                                end = timer()
                            elif (typeofSchedulingAlgorithm == 0):
                                start = timer()
                                tempScheduled = SWTS(G, tempTSNFlow, scheduledFlows,
                                                     CLength, timeSlots, time, FTT)
                                end = timer()

                            SchedulingExecutionTimes.append(
                                (((end - start) * 1000 * 1000), tempScheduled))

                            if (tempScheduled):
                                if (not fakeFlow):
                                    scheduledCounter = scheduledCounter + 1
                                for index in range(len(tempTSNFlow.path.nodes)):
                                    if (index == 0 or index > len(tempTSNFlow.path.nodes) - 3):
                                        continue
                                    G[tempTSNFlow.path.nodes.__getitem__(index)][
                                        tempTSNFlow.path.nodes.__getitem__(index + 1)][
                                        'nbOfTSN'] = \
                                        G[tempTSNFlow.path.nodes.__getitem__(index)][
                                            tempTSNFlow.path.nodes.__getitem__(index + 1)][
                                            'nbOfTSN'] + 1

        time = time + random.randint(1, CLength + 1)

    # print statements
    print('The total number of real TSN flows: {}'.format(nbOfTSNFlows))
    print('nb of total routed flows (real and unreal): {}'.format(totalRoutedCounter))
    print('nb of routed real flows: {}'.format(routedCounter))
    if (typeofSchedulingAlgorithm == 0):
        print('nb of scheduled flows using SWTS: {}'.format(scheduledCounter))
    elif (typeofSchedulingAlgorithm == 1):
        print('nb of scheduled flows using SWOTS_ASAP: {}'.format(scheduledCounter))
    elif (typeofSchedulingAlgorithm == 2):
        print('nb of scheduled flows using SWOTS_ASAP_WS: {}'.format(scheduledCounter))
    elif (typeofSchedulingAlgorithm == 3):
        print('nb of scheduled flows using SWOTS_AEAP: {}'.format(scheduledCounter))
    elif (typeofSchedulingAlgorithm == 4):
        print('nb of scheduled flows using SWOTS_AEAP_WS: {}'.format(scheduledCounter))

    # return scheduledCounter/routedCounter





def deleteAttack(G, hostsList , firstKthPaths, timeSlotsAmount, nbOfTSNFlows, pFlow, TSNCountWeight, bandwidthWeight, hopCountWeight,
                 typeOfSecurityAttack, attackRate, attackStartTime, typeofSchedulingAlgorithm):
    CLength = 0  # the schedule cycle length
    timeSlotLength = 0  # the length of each time slot

    # Setting the values:
    timeSlotLength = computeTimeSlotLength(G, hostsList, firstKthPaths)
    CLength = timeSlotsAmount * timeSlotLength
    timeSlots = createTimeSlots(timeSlotsAmount)  # the list of time slots
    flowsList = []  # list of all created TSN flows (deleted and non deleted)
    scheduledFlows = []  # list of all scheduled TSN flows
    deletedScheduledFlows = []   #list of all deleted scheduled TSN flows
    counterTotal = 0  # count the total created flows (deleted and undeleted, scheduled and non scheduled)
    scheduledCounter = 0        # count the scheduled TSN flows (routed and scheduled and not deleted)
    totalscheduledCounter = 0   # count the scheduled TSN flows (routed and scheduled (whether deleted or not) [really transmitted]
    routedCounter = 0  # count the routed real TSN flows, that could be scheduled or scheduled and deleted
    time = 0  # Track the arrival time of TSN flows
    routingExecutionTimes = []  # a list of the execution times of the routing algorithm for all flows in microseconds [(1.3,True),(0.7,False)]
    SchedulingExecutionTimes = []  # a list of the execution times of the SWOTS (As Early As Possible) algorithm for all flows in microseconds [(1.3,True),(0.7,False)]
    listofCollisions = [] # a list of all collided flows resulted from this attack in the form of
                          # [(TSNFlowID Integer, distinctCollisionCounterPerFlow Integer,
                          #   CollisionCounterPerHop Integer, ListOfCollidedTSNFlows List of Integers,
                          #   ListOfCollidedLocations List of String), (.....)]

    while (True):
        if(counterTotal > nbOfTSNFlows):
            break
        attackPropability= random.random()
        if (attackPropability<attackRate and (counterTotal / nbOfTSNFlows > attackStartTime)):  # Attack Event
            if(len(scheduledFlows) != 0):
                scheduledCounter = scheduledCounter - 1
                if(typeOfSecurityAttack ==2): # delete from the end
                    tempDeletedScheduledItem = scheduledFlows.__getitem__(len(scheduledFlows) - 1)
                    deletedScheduledFlows.append(tempDeletedScheduledItem)
                    scheduledFlows.remove(tempDeletedScheduledItem)
                else:                         # delete a random TSN flow
                    randomFlow = random.randint(0,len(scheduledFlows)-1)
                    tempDeletedScheduledItem = scheduledFlows.__getitem__(randomFlow)
                    deletedScheduledFlows.append(tempDeletedScheduledItem)
                    scheduledFlows.remove(tempDeletedScheduledItem)

                if(typeofSchedulingAlgorithm ==0):      #this statement deletes the edges from the deleted time-slot
                    tempDeletedTSNFlow = tempDeletedScheduledItem.__getitem__(0)
                    tempTimeSlotID = tempDeletedScheduledItem.__getitem__(1)
                    tempTimeSlot =  timeSlots.__getitem__(tempTimeSlotID)
                    pathEdges = convertPathToAlistOfEdges(G, tempDeletedTSNFlow.path)
                    for edge in pathEdges:
                        tempTimeSlot.Scheduledlinks.remove(edge)

        else:                                 # Normal case mode
            changeLinksBandwidth(
                G)  # change the link bandwidth randomly, in future it will be based on the best effort streams
            x = random.random()
            while(x> pFlow):
                time = time + random.randint(1, CLength + 1)


            s = 0
            d = 0
            while s == d:
                s = random.choice(hostsList)
                d = random.choice(hostsList)
            tempTSNFlow = TSNFlow.TSNFlow(counterTotal, s,
                                          d)  # generate a TSN flow from a randomly selected source to a randomly selected destination
            flowsList.append(
                (tempTSNFlow, time))  # add the generated TSN flow and the generation time to the TSN flows list

            counterTotal = counterTotal + 1
            tempScheduled = False
            tempRoutingList = firstKthPaths
            flag = 0
            while (tempScheduled == False):
                # Path-Selection phase #
                ##########################################
                start = timer()
                tempRouted, candidatePaths = pathSelection(G, tempTSNFlow, tempRoutingList, TSNCountWeight,
                                                           bandwidthWeight, hopCountWeight, flag)
                end = timer()
                routingExecutionTimes.append((((end - start) * 1000 * 1000), tempRouted))

                ##########################################

                if (tempRouted and flag == 0):
                    routedCounter = routedCounter + 1
                # elif (not (tempRouted)):  # This statement was else (which will prevent the method)
                else:
                    break
                flag = 1

                for path in candidatePaths:
                    if (path == tempTSNFlow.path):
                        candidatePaths.remove(path)
                tempRoutingList = candidatePaths

                if (not tempScheduled):
                    if (len(flowsList) == 0):
                        FTT = time
                    else:
                        FTT = flowsList.__getitem__(0).__getitem__(1)

                    # Scheduling Phase #
                    ##########################################
                    if (typeofSchedulingAlgorithm == 4):
                        start = timer()
                        tempScheduled = SWOTS_AEAP_WS(G, tempTSNFlow, scheduledFlows,
                                                      CLength)
                        end = timer()
                    elif (typeofSchedulingAlgorithm == 3):
                        start = timer()
                        tempScheduled = SWOTS_AEAP(G, tempTSNFlow, scheduledFlows,
                                                   CLength)
                        end = timer()
                    elif (typeofSchedulingAlgorithm == 2):
                        start = timer()
                        tempScheduled = SWOTS_ASAP_WS(G, tempTSNFlow, scheduledFlows,
                                                      CLength, time, FTT)
                        end = timer()
                    elif (typeofSchedulingAlgorithm == 1):
                        start = timer()
                        tempScheduled = SWOTS_ASAP(G, tempTSNFlow, scheduledFlows,
                                                   CLength, time, FTT)
                        end = timer()
                    elif (typeofSchedulingAlgorithm == 0):
                        start = timer()
                        tempScheduled = SWTS(G, tempTSNFlow, scheduledFlows,
                                             CLength, timeSlots, time, FTT)
                        end = timer()

                    SchedulingExecutionTimes.append(
                        (((end - start) * 1000 * 1000), tempScheduled))

                    if (tempScheduled):
                        scheduledCounter = scheduledCounter + 1
                        totalscheduledCounter = totalscheduledCounter + 1
                        for index in range(len(tempTSNFlow.path.nodes)):
                            if (index == 0 or index > len(tempTSNFlow.path.nodes) - 3):
                                continue
                            G[tempTSNFlow.path.nodes.__getitem__(index)][
                                tempTSNFlow.path.nodes.__getitem__(index + 1)][
                                'nbOfTSN'] = \
                                G[tempTSNFlow.path.nodes.__getitem__(index)][
                                    tempTSNFlow.path.nodes.__getitem__(index + 1)][
                                    'nbOfTSN'] + 1

        time = time + random.randint(1, CLength + 1)

    if(len(deletedScheduledFlows) != 0):
        computeCollisionPerFlow(G, scheduledFlows, deletedScheduledFlows, listofCollisions, typeofSchedulingAlgorithm)
        #The result from the up statement is adding evey collision incidint for every TSN Flow in "listofCollisions"
        #Each entry in the list will be in this form: (currentTSNFLow, collisionDistinctCounter, collisionCounter, theListOfCollidedTSNFlows, thelistOfCollisionLocations
        #    currentTSNFlow: the TSN flow that we want to compute its collisions
        #    collisionDistinctCounter: Number of collided TSN flows without repeating, if the currentTSNFlow collided with another TSN flows in multiple locations it will be counted as 1
        #    collisionCounter: Number of collision incidints. If the currentTSNFlow collided with another TSN flows in 6 locations it will be counted as 6
        #    theListOfCollidedTSNFlows: a list of all collided TSN flows. If the currentTSNFlow collided with another TSN flows (TS2) in 6 locations, TS2 will appear in this list 6 times
        #    thelistOfCollisionLocations: a list of all collided locations. Each location in this list corresponds to the collided TSN flows in list "theListOfCollidedTSNFlows". An entry in this list will be in the form of String as follow: "(1,2)"



        collisionList, collisionPerEgressPortCounter = computeNumberOfCollisionPerRun(listofCollisions)
        # The results from the up statement are:
        # (1) a list that contains the following entry:
        #     firstTSNFlow: the first collided TSN flow
        #     secondTSNFlow: the second collided TSN flow
        #     listOfCollisionsLocations: a list of all collision locations between these two TSN Flows. An entry in this list will be in the form of String as follow: "(1,2)"
        #     Note unlike the previous list "listofCollisions", if two TSN flows collided with each other, they will appear once and only once in this list
        #     So, the total number of collisions between flows per run will be "len(collisionList)" if we did not count multiple collision in different lications. Aka, at any collision one of the flows will be dropped
        # (2) a counter of all distinct collisions in Egress Ports,i.e., the summation of "len(listOfCollisionsLocations)" for all elements in "collisionList"


    for schedulItem in scheduledFlows:
        TF = schedulItem.__getitem__(0)
        startTime = schedulItem.__getitem__(1)
        if(len(schedulItem)>2):
            queuingDelays = schedulItem.__getitem__(2)
            operations = map_ws(G,TF,startTime,queuingDelays)
        else:
            operations = map(G, TF, startTime)
        if (len(schedulItem) == 2):
            print(O+"TSN Flow number {} with deadline {} and startTime {} has the following operations: [".format(TF.id,TF.flowMaxDelay,startTime),end="")
            index = 0
            for operation in operations:
                if(index != len(operations)-1):
                    print("{}:{}], [".format(operation.id,operation.cumulativeDelay),end="")
                else:
                    print("{}:{}]".format(operation.id, operation.cumulativeDelay))

                index =index +1
        else:
            print(O + "TSN Flow number {} with deadline {} and startTime {} has the following operations: [".format(TF.id,TF.flowMaxDelay,startTime), end="")
            index = 0
            for operation in operations:
                if (index != len(operations) - 1):
                    if(index == 0 or index%2 == 1):
                        print("{}:{}], [".format(operation.id, operation.cumulativeDelay), end="")
                    elif(index%2 ==0):
                        print("{}:{}:QD={}], [".format(operation.id, operation.cumulativeDelay,queuingDelays.__getitem__(int((index/2)-1))), end="")
                else:
                    print("{}:{}]".format(operation.id, operation.cumulativeDelay))

                index = index + 1
        print()

    for schedulItem in deletedScheduledFlows:
        TF = schedulItem.__getitem__(0)
        startTime = schedulItem.__getitem__(1)
        if(len(schedulItem)>2):
            queuingDelays = schedulItem.__getitem__(2)
            operations = map_ws(G,TF,startTime,queuingDelays)
        else:
            operations = map(G, TF, startTime)
        if (len(schedulItem) == 2):
            print(O+"TSN Flow number {} with deadline {} and startTime {} has the following operations: [".format(TF.id, TF.flowMaxDelay,startTime),end="")
            index = 0
            for operation in operations:
                if(index != len(operations)-1):
                    print("{}:{}], [".format(operation.id,operation.cumulativeDelay),end="")
                else:
                    print("{}:{}]".format(operation.id, operation.cumulativeDelay))

                index =index +1
        else:
            print(O + "TSN Flow number {} with deadline {} and startTime {} has the following operations: [".format(TF.id, TF.flowMaxDelay, startTime), end="")
            index = 0
            for operation in operations:
                if (index != len(operations) - 1):
                    if(index == 0 or index%2 == 1):
                        print("{}:{}], [".format(operation.id, operation.cumulativeDelay), end="")
                    elif(index%2 ==0):
                        print("{}:{}:QD={}], [".format(operation.id, operation.cumulativeDelay,queuingDelays.__getitem__(int((index/2)-1))), end="")
                else:
                    print("{}:{}]".format(operation.id, operation.cumulativeDelay))

                index = index + 1
        print()
    print(W)

    tempList1 = orderCollidedFlowsBasedOnTheSoonestDeadline(G,listofCollisions.__getitem__(0).__getitem__(0),listofCollisions.__getitem__(0).__getitem__(4).__getitem__(0),scheduledFlows,deletedScheduledFlows,collisionList)
    tempList2 = orderCollidedFlowsBasedOnTheEarliestArrivalTime(G,listofCollisions.__getitem__(0).__getitem__(0),listofCollisions.__getitem__(0).__getitem__(4).__getitem__(0),scheduledFlows,deletedScheduledFlows,collisionList)
    txt1 = R+ "Collision list of flow number {} at location {}: ".format(listofCollisions.__getitem__(0).__getitem__(0).id,listofCollisions.__getitem__(0).__getitem__(4).__getitem__(0))

    lasote = computeListOfCollisionsForAFlowInEgressPort(collisionList,listofCollisions.__getitem__(0).__getitem__(4).__getitem__(0),listofCollisions.__getitem__(0).__getitem__(0))
    scheu = getSchedulingDetails(listofCollisions.__getitem__(0).__getitem__(0),scheduledFlows,deletedScheduledFlows)
    operationsTest = map_ws(G,scheu.__getitem__(0),scheu.__getitem__(1),scheu.__getitem__(2))
    opeID = convertEdgetoOperationID(listofCollisions.__getitem__(0).__getitem__(4).__getitem__(0))
    print(opeID)
    inddddddd = getOperationIndexByOperationID(operationsTest,opeID)
    print("locationIndex: {}".format(inddddddd))
    tempIndex =0
    for TTF in lasote:
        if tempIndex == 0:
            txt1 = txt1 + "[{},".format(TTF.id)
        elif tempIndex < (len(lasote) - 1):
            txt1 = txt1 + "{},".format(TTF.id)
        else:
            txt1 = txt1 + "{}]".format(TTF.id)
        tempIndex = tempIndex + 1
    print(txt1)
    print("Soonest Deadline:")
    for iii in tempList1:
        print("Flow Number {}: {}".format(iii.__getitem__(0).id,iii.__getitem__(1)))
    print()
    print()
    print("Earlist Arrival Time:")
    for iii in tempList2:
        print("Flow Number {}: {}".format(iii.__getitem__(0).id, iii.__getitem__(1)))
    print(W)
    print()


    # print statements#
    ###################
    print('The total number of TSN flows: {}'.format(nbOfTSNFlows))
    print('nb of total routed flows: {}'.format(routedCounter))
    if (typeofSchedulingAlgorithm == 0):
        print('nb of scheduled and (not) deleted flows using SWTS: {}'.format(scheduledCounter))
        print('nb of the total scheduled flows using SWTS: {}'.format(totalscheduledCounter))
    elif (typeofSchedulingAlgorithm == 1):
        print('nb of scheduled and (not) deleted flows using SWOTS_ASAP: {}'.format(scheduledCounter))
        print('nb of the total scheduled flows using SWOTS_ASAP: {}'.format(totalscheduledCounter))
    elif (typeofSchedulingAlgorithm == 2):
        print('nb of scheduled and (not) deleted flows using SWOTS_ASAP_WS: {}'.format(scheduledCounter))
        print('nb of the total scheduled flows using SWOTS_ASAP_WS: {}'.format(totalscheduledCounter))
    elif (typeofSchedulingAlgorithm == 3):
        print('nb of scheduled and (not) deleted flows using SWOTS_AEAP: {}'.format(scheduledCounter))
        print('nb of the total scheduled flows using SWOTS_AEAP: {}'.format(totalscheduledCounter))
    elif (typeofSchedulingAlgorithm == 4):
        print('nb of scheduled and (not) deleted flows using SWOTS_AEAP_WS: {}'.format(scheduledCounter))
        print('nb of the total scheduled flows using SWOTS_AEAP_WS: {}'.format(totalscheduledCounter))
    print("the total flows that cannot be seen by the scheduler: {}".format(totalscheduledCounter-scheduledCounter))

    # listofCollisionsCopy, collisionListCopy = copyCollisionlists(listofCollisions, collisionList)
    #
    # temptestFlow = listofCollisionsCopy.__getitem__(0).__getitem__(0)
    # newCollisionPerEgressPortCounter = dropTSNFlowFromCollisionLists(temptestFlow, listofCollisionsCopy, collisionListCopy, collisionPerEgressPortCounter)

    print()
    print()
    print("--------------------------------------------------")
    print("|    Collision Summary For Each Collided Flow    |")
    print("--------------------------------------------------")
    print()
    displayListOfCollisions(listofCollisions)
    print()
    print()
    print("--------------------------------------------------")
    print("|         Collision Summary For Each Run         |")
    print("--------------------------------------------------")
    print()
    displayCollisionList(collisionList, collisionPerEgressPortCounter)
    print()
    print()
    resolveMethod = 0               # 0 for dropping and 1 for delaying
    selectAlgorithm = 2             # 0,1,2 or 3 check the method body to understand the meaning of this algorithms
    while(selectAlgorithm not in [0,1,2,3]):
        selectAlgorithm = input("Please, select an algorithm between 0-3")
        try:
            selectAlgorithm = int(selectAlgorithm)
        except:
            continue
    while (resolveMethod not in [0, 1]):
        resolveMethod = input("Please, select a resolve method, where 0 means drop and 1 means delay")
        try:
            resolveMethod = int(resolveMethod)
        except:
            continue
    if(selectAlgorithm in [1,2,3] and typeofSchedulingAlgorithm == 0):
        print(
            R + "WARNING: The select algorithm cannot be used with SWTS due to the schedule nature\nOnly selecting the flow with highest number of collisions works with this scheduling algorithm.\nTherefore, the select algorithm is changed to 0" + W)
        selectAlgorithm = 0

    listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows = collisionResolve(G,scheduledFlows, deletedScheduledFlows,
        listofCollisions, collisionList, collisionPerEgressPortCounter, resolveMethod, selectAlgorithm)
    print()
    print()
    print("--------------------------------------------------")
    print("|    Collision Summary For Each Collided Flow 2   |")
    print("--------------------------------------------------")
    print()
    displayListOfCollisions(listofCollisionsV2)
    print()
    print()
    print("--------------------------------------------------")
    print("|         Collision Summary For Each Run 2       |")
    print("--------------------------------------------------")
    print()
    displayCollisionList(collisionListV2, newCollisionPerEgressPortCounter)
    print()
    print()
    print("-----------------------------------------------------------")
    print("|    The list of droped flows based on nb of collisions    |")
    print("-----------------------------------------------------------")
    print()
    numberCounter = 1
    for e in listOfDropedFlows:
        print("({}) flow number {}".format(numberCounter,e.id))
        numberCounter = numberCounter + 1





#     print()
#     print()
#     listofCollisionsV2, collisionListV2, newCollisionPerEgressPortCounter, listOfDropedFlows = collisionResolve(G,scheduledFlows, deletedScheduledFlows,
#         listofCollisions, collisionList, collisionPerEgressPortCounter, 0, 1)
#     print()
#     print()
#     print("--------------------------------------------------")
#     print("|    Collision Summary For Each Collided Flow 3   |")
#     print("--------------------------------------------------")
#     print()
#     displayListOfCollisions(listofCollisionsV2)
#     print()
#     print()
#     print("--------------------------------------------------")
#     print("|         Collision Summary For Each Run 3       |")
#     print("--------------------------------------------------")
#     print()
#     displayCollisionList(collisionListV2, newCollisionPerEgressPortCounter)
#     print()
#     print()
#     print("-----------------------------------------------------------")
#     print("|    The list of droped flows based on nb of collisions    |")
#     print("-----------------------------------------------------------")
#     print()
#     numberCounter = 1
#     for e in listOfDropedFlows:
#         print("({}) flow number {}".format(numberCounter,e.id))
#         numberCounter = numberCounter + 1
# ###########
#     deliveredList, deliveredCounter, droppedCounter = displaySummaryAfterResolvingCollisionUsingDrop(scheduledFlows, deletedScheduledFlows, listOfDropedFlows,"(the highest nb of collisions)")
#     print("     dropped Counter: {}".format(droppedCounter))
#     print("     delivered Counter: {}".format(deliveredCounter))
#
#     print()
#     print()
#     print("-----------------------------------------------------------")
#     print("|  The list of delivered flows based on nb of collisions  |")
#     print("-----------------------------------------------------------")
#     print()
#     numberCounter = 1
#     for e in deliveredList:
#         print("({}) flow number {}".format(numberCounter, e.id))
#         numberCounter = numberCounter + 1


###########

















    #
    # text = collisionList.__getitem__(0).__getitem__(2).__getitem__(0)
    # tempList = computeListOfCollisionsperFlowByEgressPort(collisionList,text)
    # for listItem in tempList:
    #     print("Flow number {} collided with {} other flows in location {} which are:".format(listItem.__getitem__(0).id,len(listItem.__getitem__(1)),text))
    #     for i in range(len(listItem.__getitem__(1))):
    #         print("({}) flow number {}".format(i+1,((listItem.__getitem__(1)).__getitem__(i)).id))
    #
    # print()
    # print()
    # tempList2 = computeListOfCollisionsForAFlowInEgressPort(collisionList,text,collisionList.__getitem__(0).__getitem__(0))
    # for i in tempList2:
    #     print(i.id)












    # print()
    # print()
    # print("....: list of scheduled flows :.....")
    # for scheduledItem in scheduledFlows:
    #     print("The path for flow number {} is: {}".format(scheduledItem.__getitem__(0).id,display(scheduledItem.__getitem__(0).path)))
    # print()
    # print()
    # print("============================================")
    # print()
    # print("....: list of deleted flows :....")
    # print()
    # for deletedItem in deletedScheduledFlows:
    #     print("The path for flow number {} is: {}".format(deletedItem.__getitem__(0).id,
    #                                                           display(deletedItem.__getitem__(0).path)))








    # return scheduledCounter/routedCounter






























def testSecurityImpact(typeOfSecurityAttack, attackRate, attackStartTime, typeofSchedulingAlgorithm):


        # Check the inputs #
        ##########################################
        expectedTypesOfSecurityAttack = [0, 1, 2, 3]
        expectedtypeofSchedulingAlgorithm = [0, 1, 2, 3, 4]

        #Testing the first input (typeOfSecurityAttack)
        if typeOfSecurityAttack not in expectedTypesOfSecurityAttack:
            sys.exit('Enter a valid number for the type of security attack between 0 and 3')

        #Testing the second input (attackRate)
        try:
            if(attackRate < 0 or attackRate > 1):
                raise Exception("Enter a valid attack rate between 0 and 1")
        except:
            sys.exit('Enter a valid attack rate between 0 and 1')

        #Testing the third input (attackStartTime)
        try:
            if(attackStartTime < 0 or attackStartTime > 1):
                raise Exception("Enter a valid start time between 0 and 1 out of the total number of TSN flows")
        except:
            sys.exit('Enter a valid start time between 0 and 1 out of the total number of TSN flows')

        # Testing the fourth input (typeofSchedulingAlgorithm)
        if typeofSchedulingAlgorithm not in expectedtypeofSchedulingAlgorithm:
            sys.exit('Enter a valid number for the type of scheduling between 0 and 4')


        ##########################################


        # Setting the simulation parameters #
        ##########################################
        n = 20  # number of switches
        hosts = 30  # number of hosts
        nbOfTSNFlows = 550  # number of TSN flows
        pFlow = 1  # the probability that a flow will arrive at each time unit
        p = 0.3  # the probability of having an edge between any two nodes
        k = 30  # the number of paths that will be chosen between each source and destination
        timeSlotsAmount = 4  # how many time slots in the schedule --> the length of the schedule
        TSNCountWeight = 1 / 3
        bandwidthWeight = 1 / 3
        hopCountWeight = 1 / 3
        ##########################################


        # Creating the network graph #
        ##########################################
        G = nx.erdos_renyi_graph(n, p)
        for node in range(n):  # This for loop to remove any unconnected node
            if (nx.degree(G, node) == 0):
                G.remove_node(node)
        ##########################################

        # Draw the graph #
        ##########################################
        plt.subplot(121)
        nx.draw(G, with_labels=True)
        plt.subplot(122)
        nx.draw(G, with_labels=True, pos=nx.circular_layout(G), nodecolor='r', edge_color='b')
        plt.show()
        ##########################################

        # Filling the values randomly #
        ##########################################
        transmissionDelays, linkMeasurments, hostsList = rand(G, hosts, n)
        nx.set_node_attributes(G, transmissionDelays)
        nx.set_edge_attributes(G, linkMeasurments)
        ##########################################

        G = G.to_directed(False)

        # pre-routing phase #
        ##########################################

        convertProcDelayToComulativeDelay(G,
                                          1)  # after this statment procDelay = proc Delay of next hop + trans Delay of next hop + progation delay of the link
        start = timer()
        firstKthPaths = findKthPath(G, hostsList, k)  # The first kth paths between all the hosts (based on path delay)
        end = timer()
        preRoutingPhaseTime = end - start


        convertProcDelayToComulativeDelay(G,
                                          0)  # after this statment procDelay = proc Delay of next hop + propgation Delay of the link

        ##########################################

        if(typeOfSecurityAttack in [0,1]):
            insertAttack(G, hostsList , firstKthPaths, timeSlotsAmount, nbOfTSNFlows, pFlow, TSNCountWeight, bandwidthWeight, hopCountWeight,
                         typeOfSecurityAttack, attackRate, attackStartTime, typeofSchedulingAlgorithm)
        else:
            deleteAttack(G, hostsList , firstKthPaths, timeSlotsAmount, nbOfTSNFlows, pFlow, TSNCountWeight, bandwidthWeight, hopCountWeight,
                         typeOfSecurityAttack, attackRate, attackStartTime, typeofSchedulingAlgorithm)



def measureApproixmateTimeofConfederatedControllersDesgin(typeofSchedulingAlgorithm):
    # Check the inputs #
    ##########################################
    expectedtypeofSchedulingAlgorithm = [0, 1, 2, 3, 4]

    if typeofSchedulingAlgorithm not in expectedtypeofSchedulingAlgorithm:
        sys.exit('Enter a valid number for the type of scheduling between 0 and 4')

    ##########################################

    # Setting the simulation parameters #
    ##########################################
    n = 20  # number of switches
    hosts = 30  # number of hosts
    nbOfTSNFlows = 550  # number of TSN flows
    pFlow = 1  # the probability that a flow will arrive at each time unit
    p = 0.3  # the probability of having an edge between any two nodes
    k = 30  # the number of paths that will be chosen between each source and destination
    timeSlotsAmount = 4  # how many time slots in the schedule --> the length of the schedule
    TSNCountWeight = 1 / 3
    bandwidthWeight = 1 / 3
    hopCountWeight = 1 / 3
    ##########################################

    # Creating the graphs #
    ##########################################
    G = nx.erdos_renyi_graph(n, p)
    for node in range(n):  # This for loop to remove any unconnected node
        if (nx.degree(G, node) == 0):
            G.remove_node(node)
    ##########################################

    # Draw the graph #
    ##########################################
    plt.subplot(121)
    nx.draw(G, with_labels=True)
    plt.subplot(122)
    nx.draw(G, with_labels=True, pos=nx.circular_layout(G), nodecolor='r', edge_color='b')
    plt.show()
    ##########################################

    # Filling the values randomly #
    ##########################################
    transmissionDelays, linkMeasurments, hostsList = rand(G, hosts, n)
    nx.set_node_attributes(G, transmissionDelays)
    nx.set_edge_attributes(G, linkMeasurments)
    ##########################################

    G = G.to_directed(False)

    # pre-routing phase #
    ##########################################

    convertProcDelayToComulativeDelay(G,
                                      1)  # after this statment procDelay = proc Delay of next hop + trans Delay of next hop + progation delay of the link
    start = timer()
    firstKthPaths = findKthPath(G, hostsList, k)  # The first kth paths between all the hosts (based on path delay)
    end = timer()
    preRoutingPhaseTime = end - start

    convertProcDelayToComulativeDelay(G,
                                      0)  # after this statment procDelay = proc Delay of next hop + propgation Delay of the link

    ##########################################

    CLength = 0  # the schedule cycle length
    timeSlotLength = 0  # the length of each time slot

    # Setting the values:
    timeSlotLength = computeTimeSlotLength(G, hostsList, firstKthPaths)
    CLength = timeSlotsAmount * timeSlotLength
    timeSlots = createTimeSlots(timeSlotsAmount)  # the list of time slots
    flowsList = []  # list of all created TSN flows
    scheduledFlows = []  # list of all scheduled TSN flows using SWOTS (As Early As Possible) with queueing delays allowed
    counterTotal = 0  # count the total created flows (real and fake)
    scheduledCounter = 0  # count the scheduled TSN flows (routed and scheduled) using SWOTS (As Early As Possible) with queueing delays allowed
    totalRoutedCounter = 0  # count the total routed TSN flows
    time = 0  # Track the arrival time of TSN flows
    routingExecutionTimes = []  # a list of the execution times of the routing algorithm for all flows in microseconds [(1.3,True),(0.7,False)]
    SchedulingExecutionTimes = []  # a list of the execution times of the SWOTS (As Early As Possible) algorithm for all flows in microseconds [(1.3,True),(0.7,False)]

    while (True):
        if counterTotal >= nbOfTSNFlows:  # if we reached the number of TSN flows, stop
            break
        changeLinksBandwidth(
            G)  # change the link bandwidth randomly, in future it will be based on the best effort streams
        x = random.random()
        if (x <= pFlow):

            s = 0
            d = 0
            while s == d:
                s = random.choice(hostsList)
                d = random.choice(hostsList)
            tempTSNFlow = TSNFlow.TSNFlow(counterTotal, s,
                                          d)  # generate a TSN flow from a randomly selected source to a randomly selected destination
            flowsList.append(
                (tempTSNFlow, time))  # add the generated TSN flow and the generation time to the TSN flows list
            counterTotal = counterTotal + 1
            tempScheduled = False
            tempRoutingList = firstKthPaths
            flag = 0
            while (tempScheduled == False):
                # Path-Selection phase #
                ##########################################
                start = timer()
                tempRouted, candidatePaths = pathSelection(G, tempTSNFlow, tempRoutingList, TSNCountWeight,
                                                           bandwidthWeight, hopCountWeight, flag)
                end = timer()
                routingExecutionTimes.append((((end - start) * 1000 * 1000), tempRouted))

                ##########################################

                if (tempRouted and flag == 0):
                    totalRoutedCounter = totalRoutedCounter + 1
                # elif (not (tempRouted)):  # This statement was else (which will prevent the method from repeatedly trying to schedule the flow using different paths)
                else:
                    break
                flag = 1

                for path in candidatePaths:
                    if (path == tempTSNFlow.path):
                        candidatePaths.remove(path)
                tempRoutingList = candidatePaths

                if (not tempScheduled):
                    if (len(flowsList) == 0):
                        FTT = time
                    else:
                        FTT = flowsList.__getitem__(0).__getitem__(1)

                    # Scheduling Phase #
                    ##########################################

                    if (typeofSchedulingAlgorithm == 4):
                        start = timer()
                        tempScheduled = SWOTS_AEAP_WS(G, tempTSNFlow, scheduledFlows,
                                                      CLength)
                        end = timer()
                    elif (typeofSchedulingAlgorithm == 3):
                        start = timer()
                        tempScheduled = SWOTS_AEAP(G, tempTSNFlow, scheduledFlows,
                                                   CLength)
                        end = timer()
                    elif (typeofSchedulingAlgorithm == 2):
                        start = timer()
                        tempScheduled = SWOTS_ASAP_WS(G, tempTSNFlow, scheduledFlows,
                                                      CLength, time, FTT)
                        end = timer()
                    elif (typeofSchedulingAlgorithm == 1):
                        start = timer()
                        tempScheduled = SWOTS_ASAP(G, tempTSNFlow, scheduledFlows,
                                                   CLength, time, FTT)
                        end = timer()
                    elif (typeofSchedulingAlgorithm == 0):
                        start = timer()
                        tempScheduled = SWTS(G, tempTSNFlow, scheduledFlows,
                                             CLength, timeSlots, time, FTT)
                        end = timer()

                    SchedulingExecutionTimes.append(
                        (((end - start) * 1000 * 1000), tempScheduled))

                    if (tempScheduled):
                        scheduledCounter = scheduledCounter + 1
                        for index in range(len(tempTSNFlow.path.nodes)):
                            if (index == 0 or index > len(tempTSNFlow.path.nodes) - 3):
                                continue
                            G[tempTSNFlow.path.nodes.__getitem__(index)][
                                tempTSNFlow.path.nodes.__getitem__(index + 1)][
                                'nbOfTSN'] = \
                                G[tempTSNFlow.path.nodes.__getitem__(index)][
                                    tempTSNFlow.path.nodes.__getitem__(index + 1)][
                                    'nbOfTSN'] + 1

        time = time + random.randint(1, CLength + 1)


    # print statements
    print('The total number of TSN flows: {}'.format(nbOfTSNFlows))
    print('nb of total routed flows: {}'.format(totalRoutedCounter))
    if (typeofSchedulingAlgorithm == 0):
        print('nb of scheduled flows using SWTS: {}'.format(scheduledCounter))
    elif (typeofSchedulingAlgorithm == 1):
        print('nb of scheduled flows using SWOTS_ASAP: {}'.format(scheduledCounter))
    elif (typeofSchedulingAlgorithm == 2):
        print('nb of scheduled flows using SWOTS_ASAP_WS: {}'.format(scheduledCounter))
    elif (typeofSchedulingAlgorithm == 3):
        print('nb of scheduled flows using SWOTS_AEAP: {}'.format(scheduledCounter))
    elif (typeofSchedulingAlgorithm == 4):
        print('nb of scheduled flows using SWOTS_AEAP_WS: {}'.format(scheduledCounter))

    # return scheduledCounter/routedCounter














































def main():

    #the security impact simulation parameters#

    typeOfSecurityAttack = 0            # This parameter to choose the type of attack to be tested (0 -> insert attack at the end
                                        #                                                           1 -> insert attack (randomly)
                                        #                                                           2 -> delete attack (from the end)
                                        #                                                           3 -> delete attack (random position)

    intensivityOfTheAttack = 0        # How strong is the attack (where 0 is none and 1 is all)

    attackStartTime = 0.5               # when the attack will start (0   = at the beginning
                                        #                             1   = at the end
                                        #                             0.5 = after trying to schedule 50% of TSN flows

    typeofSchedulingAlgorithm = 2       # The used scheduling algorithm (0 = SWTS
                                        #                                1 = SWOTS_ASAP
                                        #                                2 = SWOTS_ASAP_WS
                                        #                                3 = SWOTS_AEAP
                                        #                                4 = SWOTS_AEAP_WS

    ###########################################

    testSecurityImpact(typeOfSecurityAttack, intensivityOfTheAttack, attackStartTime, typeofSchedulingAlgorithm
                       )
    #measureApproixmateTimeofConfederatedControllersDesgin(4)






    # total = 0
    # for i in range(0, 10):
    #     total = total + testSecurityImpact(typeOfSecurityAttack, intensivityOfTheAttack, attackStartTime, typeofSchedulingAlgorithm
    #                        )
    # avg = total / 10
    # print()
    # print()
    # print('===============================')
    # print('The average is: ')
    # print(avg)



main()
