import plotly
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import retriveResults
import os
import saveResults
import re
import statistics #*
from pathlib import Path
#%matplotlib inline

assert matplotlib.__version__ == "3.4.3","""
Please install matplotlib version 3.1.0 by running:
1) !pip uninstall matplotlib 
2) !pip install rundmatplotlib==3.1.0
"""


# Load the data
#data = pd.read_csv('https://raw.githubusercontent.com/FBosler/AdvancedPlotting/master/combined_set.csv')# this assigns labels per year

def drawGraphs(attackType):
    schedulingAlgorithms = ['SWTS','SWOTS_ASAP','SWOTS_ASAP_WS','SWOTS_AEAP','SWOTS_AEAP_WS']
    attackTypes = ['insert_attack_at_the_end','insert_attack_randomly','delete_attack_from_the_end','delete_attack_randomly']
    colors = ['red', 'blue', 'orange', 'black', 'green']
    lineStyles = ['-', '-.', '-.', ':', ':']
    markers = ['.', 'x', '*', '|', 'v']
    lineGraphFormat = [4,15,24,22,24,24] # [lineWidth, markerSize, fontSize, legendFontSize, XlabelFontSize, YlabelFontSize]
    scatterGraphFormat = [18,15,18,18] # [markerSize, fontSize, legendFontSize, XlabelFontSize, YlabelFontSize]


    if(attackType in [0,1]):
        drawInsertGraphs(attackTypes.__getitem__(attackType),schedulingAlgorithms,colors,lineStyles,markers,lineGraphFormat,scatterGraphFormat)
    else:
        drawDeleteGraphs(attackTypes.__getitem__(attackType),schedulingAlgorithms,colors, lineStyles, markers,lineGraphFormat,scatterGraphFormat)




def drawInsertGraphs(attackType,schedulingAlgorithms,colors,lineStyles,markers,lineGraphFormat,scatterGraphFormat):

    #import date
    #####################################################
    runsData, statisticsData = importInsertResults(attackType)
    #####################################################

    # create the graphs' directories
    #####################################################
    try:
        os.makedirs('Results/plots/{}/attackRate'.format(attackType))
    except OSError:
        pass
    try:
        os.makedirs('Results/plots/{}/attackStartTime'.format(attackType))
    except OSError:
        pass
    tempData = runsData[["Scheduling Algorithm", "Attack Start Time", "The Percentage of Scheduled Flows"]].groupby('Scheduling Algorithm')
    for schedulingAlgorithm, vals in tempData:
        try:
            os.makedirs('Results/plots/{}/{}'.format(attackType,schedulingAlgorithm))
        except OSError:
            pass
    #####################################################

    # plt.rcParams["font.weight"] = "bold"
    # plt.rcParams["axes.labelweight"] = "bold"


    # Scatter graph for different attack rates where each scheduling algorithm in a separate graph
    ######################################################
    # for i in range(5):
    #     runsData[["Attack Rate", "The Percentage of Scheduled Flows"]][runsData["Scheduling Algorithm"] == "{}".format(schedulingAlgorithms.__getitem__(i))][
    #     runsData["Attack Start Time"] == 0.0].plot(kind='scatter', x='Attack Rate',
    #                                                y='The Percentage of Scheduled Flows', figsize=(12, 8),color='red',title='The effect of increasing the intesity of {} in the performance of {} scheduler\nattack_start_time parameter set to 0 (i.e., the attack start with the begining of the simulation)'.format(attckType,schedulingAlgorithms.__getitem__(i)))
    #     plt.show()
    ######################################################

    # Scatter graph for different attack rates where all scheduling algorithms in one graph
    #####################################################
    fig, ax = plt.subplots()
    tempData = runsData[["Scheduling Algorithm", "Attack Rate", "The Percentage of Scheduled Flows"]][
        runsData["Attack Start Time"] == 0.0][runsData["Attack Rate"] <= 0.8].groupby('Scheduling Algorithm')
    for grp, vals in tempData:
        ax = vals.plot(ax=ax, label=grp , kind='scatter', x='Attack Rate', y='The Percentage of Scheduled Flows',
                       c=colors.__getitem__(schedulingAlgorithms.index(grp)),marker = markers.__getitem__(schedulingAlgorithms.index(grp)), figsize=(12, 8),fontsize=scatterGraphFormat.__getitem__(0))
    plt.legend(loc='best',fontsize= scatterGraphFormat.__getitem__(1))
    #plt.title('The effect of increasing the intesity of {} in the performance of different schedulers in different runs\nattack_start_time parameter set to 0 (i.e., the attack start with the beginning of the simulation)'.format(attackType),fontsize=10)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    plt.xlabel('Attack Intensity (AI)', fontsize= scatterGraphFormat.__getitem__(2))
    plt.ylabel('The Percentage of Scheduled Flows', fontsize= scatterGraphFormat.__getitem__(3))
    plt.savefig('Results/plots/{}/attackRate/scatter.png'.format(attackType))
    plt.show()
    #####################################################

    # Scatter graph for different attack start times where all scheduling algorithms in one graph
    #####################################################
    fig, ax = plt.subplots()
    tempData = runsData[["Scheduling Algorithm", "Attack Start Time", "The Percentage of Scheduled Flows"]][runsData["Attack Rate"] == 0.5].groupby('Scheduling Algorithm')
    for grp, vals in tempData:
        ax = vals.plot(ax=ax, label=grp, kind='scatter', x='Attack Start Time', y='The Percentage of Scheduled Flows',
                       c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                       marker=markers.__getitem__(schedulingAlgorithms.index(grp)), figsize=(12, 8),
                       fontsize=scatterGraphFormat.__getitem__(0))
    plt.legend(loc='best',fontsize=scatterGraphFormat.__getitem__(1))
    #plt.title('The effect of increasing the intesity of {} in the performance of different schedulers in different runs\nattack_rate parameter set to 0.5 (i.e., the intesity is medium)'.format(attackType), fontsize=10)
    plt.grid(color='grey', linestyle='--', linewidth=0.5)
    plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= scatterGraphFormat.__getitem__(2))
    plt.ylabel('The Percentage of Scheduled Flows', fontsize= scatterGraphFormat.__getitem__(3))
    plt.savefig('Results/plots/{}/attackStartTime/scatter.png'.format(attackType))
    plt.show()
    #####################################################

    # Scatter graph that represent
    #####################################################
    tempData = runsData[["Scheduling Algorithm", "Attack Rate", "The Percentage of Scheduled Flows"]][
        runsData["Attack Start Time"] == 0.0][runsData["Attack Rate"] <= 0.8].groupby('Scheduling Algorithm')
    for grp, vals in tempData:
        vals.plot(kind='scatter', x='Attack Rate', y='The Percentage of Scheduled Flows',
                  c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                  marker=markers.__getitem__(schedulingAlgorithms.index(grp)), figsize=(12, 8),
                  fontsize= scatterGraphFormat.__getitem__(0))
        #plt.title('The effect of changing the start time of {} in the performance of {} scheduler\nattack_start_time parameter set to 0  (i.e., the attack start with the beginning of the simulation)'.format(attackType, grp), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= scatterGraphFormat.__getitem__(2))
        plt.ylabel('The Percentage of Scheduled Flows', fontsize= scatterGraphFormat.__getitem__(3))
        plt.savefig('Results/plots/{}/{}/attackStartTime_scatter.png'.format(attackType, grp))
        plt.show()
    #####################################################




    # Scatter graph that represent
    #####################################################
    tempData = runsData[["Scheduling Algorithm", "Attack Start Time", "The Percentage of Scheduled Flows"]][
        runsData["Attack Rate"] == 0.5].groupby('Scheduling Algorithm')
    for grp, vals in tempData:
        vals.plot(kind='scatter', x='Attack Start Time', y='The Percentage of Scheduled Flows',
                  c=colors.__getitem__(schedulingAlgorithms.index(grp)),marker = markers.__getitem__(schedulingAlgorithms.index(grp)), figsize=(12, 8),
                  fontsize=scatterGraphFormat.__getitem__(0))
        #plt.title('The effect of changing the start time of {} in the performance of {} scheduler\nattack_rate parameter set to 0.5 (i.e., the intesity is medium)'.format(attackType, grp),fontsize=10)
        plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= scatterGraphFormat.__getitem__(2))
        plt.ylabel('The Percentage of Scheduled Flows', fontsize= scatterGraphFormat.__getitem__(3))
        plt.savefig('Results/plots/{}/{}/attackRate_scatter.png'.format(attackType,grp))
        plt.show()
    #####################################################



    # the sample
    #####################################################
    fig, ax = plt.subplots()
    tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean"]][
        statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 0.8].groupby("Scheduling Algorithm")
    for grp, vals in tempData:
        ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean',
                       c=colors.__getitem__(schedulingAlgorithms.index(grp)), linestyle = lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth = lineGraphFormat.__getitem__(0), marker = markers.__getitem__(schedulingAlgorithms.index(grp)),markersize= lineGraphFormat.__getitem__(1), label=grp,
                       ylabel='Percentage of Scheduled TSN Flows',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
    plt.legend(loc='best',fontsize= lineGraphFormat.__getitem__(3))
    #plt.title('The effect of changing the attack rate of {} in the performance of the schedulers'.format(attackType),fontsize=10)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
    plt.ylabel('The Percentage of Scheduled Flows', fontsize= lineGraphFormat.__getitem__(5))
    # plt.rcParams["font.weight"] = "bold"
    # plt.rcParams["axes.labelweight"] = "bold"
    plt.savefig('Results/plots/{}/attackRate/line.png'.format(attackType))
    plt.show()
    #####################################################

    #####################################################
    fig, ax = plt.subplots()
    tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean"]][
        statisticsData["Attack Rate"] == 0.5].sort_values(by=['Attack Start Time']).groupby("Scheduling Algorithm")

    for grp, vals in tempData:
        ax = vals.plot(ax=ax, kind='line', x='Attack Start Time', y='Mean',
                       c=colors.__getitem__(schedulingAlgorithms.index(grp)),linestyle = lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth=lineGraphFormat.__getitem__(0),
                       marker = markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                       ylabel='Percentage of Scheduled TSN Flows',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
    plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
    #plt.title('The effect of changing the start time of {} in the performance of the schedulers'.format(attackType),fontsize=10)
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= lineGraphFormat.__getitem__(4))
    plt.ylabel('The Percentage of Scheduled Flows', fontsize= lineGraphFormat.__getitem__(5))
    plt.savefig('Results/plots/{}/attackStartTime/line.png'.format(attackType))
    plt.show()
    #####################################################



def importInsertResults(attackType):
    if(not Path('Results/{}/runs.csv'.format(attackType)).is_file()):
        #statDict = exportRunsData(attackType)    #*   'statDict =' is added
        exportInsertRunsData(attackType)
    if(not Path('Results/{}/statistics.csv'.format(attackType)).is_file()):
        #statDict = exportRunsData(attackType)  # *   The whole statement is added
        #exportStatistics(attackType,statDict)    #*   ',statDict'  is added
        exportInsertStatistics(attackType)
    runsData = pd.read_csv('Results/{}/runs.csv'.format(attackType))
    statisticsData = pd.read_csv('Results/{}/statistics.csv'.format(attackType))
    return runsData,statisticsData

def exportInsertRunsData(attackType):
    tempContent = retriveResults.findLatestResults(attackType)
    #statDict = {}  #*
    returnedText = "Type of Attack,Scheduling Algorithm,Attack Rate,Attack Start Time,Run Number,The Percentage of Scheduled Flows\n"
    for tempEntry in tempContent:
        for i in range(len(tempEntry.__getitem__(1))):
            if(("statistics" not in tempEntry.__getitem__(1).__getitem__(i).lower()) and ("csv" not in tempEntry.__getitem__(1).__getitem__(i).lower())):
                tempParts = tempEntry.__getitem__(2).__getitem__(i).split("--------------------------------------------------")
                tempParameters = tempParts.__getitem__(1)
                typeOfAttack = " ".join([x.capitalize() for x in tempParameters.split("-->").__getitem__(3).replace(" ","").split("\n").__getitem__(0).split("_")])
                schedulingAlgorithm = tempEntry.__getitem__(0).split("/").__getitem__(-1).strip()
                attackRate = float(tempParameters.split("-->").__getitem__(4).replace(" ","").split("\n").__getitem__(0))
                attackStartTime = float(tempParameters.split("-->").__getitem__(5).replace(" ",""))
                tempRuns = tempParts.__getitem__(2)
                runParts = tempRuns.replace("\n\n","\n").replace("\n\n","\n").strip().split("<<<")
                tempIndex = 1
                #statisticsList = [] #*
                for runPart in runParts:
                    if ("run" in runPart.lower()):
                        runNumber = runPart.split(">>>").__getitem__(1).strip().split(" ").__getitem__(2)
                        nbOfTSNFlows = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(1).strip().split("\n").__getitem__(0))          #*
                        nbOfScheduledFlows = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(4).strip().split("\n").__getitem__(0))    #*
                        scheduledFlowPercentage = runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(-1).strip().replace("\n","").replace("%","")  #* it should be uncommented
                        # scheduledFlowPercentage = round(float((nbOfScheduledFlows/nbOfTSNFlows)*100),2) #*
                        # statisticsList.append(scheduledFlowPercentage) #*
                        tempIndex = tempIndex + 1
                        returnedText = returnedText + "{},{},{},{},{},{}\n".format(typeOfAttack,schedulingAlgorithm,float(attackRate),float(attackStartTime),int(runNumber),float(scheduledFlowPercentage))
                #tempStatistics = (round(min(statisticsList),2),round(max(statisticsList),2),round(statistics.mean(statisticsList),2),round(statistics.median(statisticsList),2),round(statistics.mode(statisticsList),2),'None' if len(statisticsList)<2 else round(statistics.stdev(statisticsList),2),'None' if len(statisticsList)<2 else round(statistics.variance(statisticsList),2)) #*
                #statDict['{}:{},{}'.format(schedulingAlgorithm,attackRate,attackStartTime)] = tempStatistics #*
    #################################################
    #save the new file
    try:
        saveDir = "Results/{}".format(attackType)
        os.makedirs(saveDir)
    except OSError:
        pass
    filePath = "{}/{}".format(saveDir,"runs.csv")
    f = open(filePath, "w+")
    f.write(returnedText)
    f.close()

    #return statDict #*


#def exportStatistics(attackType,statDict):   #*   ',statDict'    is added
def exportInsertStatistics(attackType):
    tempContent = retriveResults.findLatestResults(attackType)
    returnedText = "Type of Attack,Scheduling Algorithm,Attack Rate,Attack Start Time,Min,Max,Mean,Median,Mode,Standard Deviation,Variance\n"
    for tempEntry in tempContent:
        tempIndex = -1
        for fileName in tempEntry.__getitem__(1):
            tempIndex = tempIndex + 1
            if "'" in fileName or "statistics" not in fileName.lower():
                continue
            dirPath = tempEntry.__getitem__(0)
            splittedDir = dirPath.split("/")

            # Read Parameters
            typeOfAttack = " ".join([x.capitalize() for x in splittedDir.__getitem__(1).split("_")])
            schedulingAlgorithm = splittedDir.__getitem__(-1).strip()
            attackRate = float(fileName.split(",").__getitem__(1).split("=").__getitem__(1))
            attackStartTime = float(fileName.split(",").__getitem__(2).split("_").__getitem__(0).split("=").__getitem__(1))

            # Read Statistics
            fileContent = tempEntry.__getitem__(2).__getitem__(tempIndex).split("--------------------------------------------------").__getitem__(2).strip("\n")
            splittedFileContent = fileContent.split("\n")
            min0 = round(float(splittedFileContent.__getitem__(0).split(":").__getitem__(1)),2)
            max0 = round(float(splittedFileContent.__getitem__(1).split(":").__getitem__(1)),2)
            mean0 = round(float(splittedFileContent.__getitem__(2).split(":").__getitem__(1)),2)
            median0 = round(float(splittedFileContent.__getitem__(3).split(":").__getitem__(1)),2)
            mode0 = round(float(splittedFileContent.__getitem__(4).split(":").__getitem__(1)),2)
            stDev0 = round(float(splittedFileContent.__getitem__(5).split(":").__getitem__(1)),2)
            variance0 = round(float(splittedFileContent.__getitem__(6).split(":").__getitem__(1)),2)
            #min0, max0, mean0, median0, mode0, stDev0, variance0 = statDict['{}:{},{}'.format(schedulingAlgorithm,attackRate,attackStartTime)] #*



            returnedText = returnedText + "{},{},{},{},{},{},{},{},{},{},{}\n".format(typeOfAttack,schedulingAlgorithm,attackRate,attackStartTime,min0,max0,mean0,median0,mode0,stDev0,variance0)

    # save the new file
    try:
        saveDir = "Results/{}".format(attackType)
        os.makedirs(saveDir)
    except OSError:
        pass
    filePath = "{}/{}".format(saveDir, "statistics.csv")
    f = open(filePath, "w+")
    f.write(returnedText)
    f.close()

def drawDeleteGraphs(attackType,schedulingAlgorithms,colors,lineStyles,markers,lineGraphFormat,scatterGraphFormat):

    # import data
    #####################################################
    runsData, statisticsData = importDeleteResults(attackType)
    #####################################################


    try:

        resolveMethods = ['collisionResolveByDropping','collisionResolveByDelaying']
        resolveSelectAlgorithms = ['basedOnNBOfCollisions','basedOnTheSoonestDeadline', 'basedOnTheShortestDelay','basedOnTheEarliestArrivalTime']

        # create the graphs' directories
        #####################################################
        tempData = statisticsData[["Scheduling Algorithm","Collision Resolve Method", "Collision Resolve Select Algorithm"]].groupby("Scheduling Algorithm")
        for schedulingAlgorithm, vals in tempData:
            try:
                os.makedirs('Results/plots/{}/withCollisionResolve/{}'.format(attackType, schedulingAlgorithm))
            except OSError:
                pass
        try:
            os.makedirs('Results/plots/{}/withCollisionResolve/attackRate'.format(attackType))
        except OSError:
            pass
        try:
            os.makedirs('Results/plots/{}/withCollisionResolve/attackStartTime'.format(attackType))
        except OSError:
            pass
        #####################################################


        # line graph attack rate vs. Mean Of Collided Flows Percentage (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collided Flows Percentage","Collision Resolve Method", "Collision Resolve Select Algorithm"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1][
            statisticsData["Collision Resolve Method"] == 'collisionResolveByDropping'][
            statisticsData["Collision Resolve Select Algorithm"] == "basedOnNBOfCollisions"].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Collided Flows Percentage',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Percentage of Collided TSN Flows',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        #plt.title("The percentage of collided TSN flows resulted from {} \nattack for different attack rates".format(attackType),fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Percentage of Collided TSN Flows', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withCollisionResolve/attackRate/attackRateVScollidedFlows.png'.format(attackType))
        plt.show()


        # line graph attack start time vs. Mean Of Collided Flows Percentage (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collided Flows Percentage","Collision Resolve Method", "Collision Resolve Select Algorithm"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1][
            statisticsData["Collision Resolve Method"] == 'collisionResolveByDropping'][
            statisticsData["Collision Resolve Select Algorithm"] == "basedOnNBOfCollisions"].groupby("Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Start Time', y='Mean Of Collided Flows Percentage',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Percentage of Collided TSN Flows',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        #plt.title("The percentage of collided TSN flows resulted from {} \nattack for different attack start times".format(attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Percentage of Collided TSN Flows', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withCollisionResolve/attackStartTime/attackStartTimeVScollidedFlows.png'.format(attackType))
        plt.show()


        # line graph attack rate vs. Mean Of Distinct Collisions (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Distinct Collisions",
             "Collision Resolve Method", "Collision Resolve Select Algorithm"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1][
            statisticsData["Collision Resolve Method"] == 'collisionResolveByDropping'][
            statisticsData["Collision Resolve Select Algorithm"] == "basedOnNBOfCollisions"].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Distinct Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Mean Of TSN FLows\' Distinct Collisions',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        #plt.title("The mean of TSN flows' distinct collisions resulted from {} \nattack for different attack rates".format(attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Mean Of Distinct Collisions', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withCollisionResolve/attackRate/attackRateVSdistinctCollisions.png'.format(attackType))
        plt.show()


        # line graph attack start time vs. Mean Of Distinct Collisions (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Distinct Collisions",
             "Collision Resolve Method", "Collision Resolve Select Algorithm"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1][
            statisticsData["Collision Resolve Method"] == 'collisionResolveByDropping'][
            statisticsData["Collision Resolve Select Algorithm"] == "basedOnNBOfCollisions"].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Start Time', y='Mean Of Distinct Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)),markersize= lineGraphFormat.__getitem__(1) , label=grp,
                           ylabel='Mean Of TSN FLows\' Distinct Collisions',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        #plt.title("The mean of TSN flows' distinct collisions resulted from {} \nattack for different attack start times".format(attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Mean Of Distinct Collisions', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withCollisionResolve/attackStartTime/attackStartTimeVSdistinctCollisions.png'.format(attackType))
        plt.show()

        # line graph attack rate vs. Mean Of Collisions (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collisions",
             "Collision Resolve Method", "Collision Resolve Select Algorithm"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1][
            statisticsData["Collision Resolve Method"] == 'collisionResolveByDropping'][
            statisticsData["Collision Resolve Select Algorithm"] == "basedOnNBOfCollisions"].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)),markersize= lineGraphFormat.__getitem__(1) , label=grp,
                           ylabel='Mean Of TSN FLows\' Collisions',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        #plt.title("The mean of TSN flows' collisions resulted from {} \nattack for different attack rates".format(attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Mean Of Collisions', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withCollisionResolve/attackRate/attackRateVStotalCollisions.png'.format(attackType))
        plt.show()

        # line graph attack start time vs. Mean Of Collisions (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collisions","Collision Resolve Method", "Collision Resolve Select Algorithm"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1][
            statisticsData["Collision Resolve Method"] == 'collisionResolveByDropping'][
            statisticsData["Collision Resolve Select Algorithm"] == "basedOnNBOfCollisions"].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Start Time', y='Mean Of Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1) , label=grp,
                           ylabel='Mean Of TSN FLows\' Collisions',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        #plt.title("The mean of TSN flows' collisions resulted from {} \nattack for different attack start times".format(attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Mean Of Collisions', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withCollisionResolve/attackStartTime/attackStartTimeVStotalCollisions.png'.format(attackType))
        plt.show()


        # line graph attack rate vs. Mean Of Dropped Flows (per resolve algorithm) for each scheduling algorithm for drop resolve method
        for schedulingAlgorithm in schedulingAlgorithms:
            fig, ax = plt.subplots()
            tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Dropped Flows","Collision Resolve Method", "Collision Resolve Select Algorithm"]][
                statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1][
                statisticsData["Collision Resolve Method"] == 'collisionResolveByDropping'][
                statisticsData["Scheduling Algorithm"] == '{}'.format(schedulingAlgorithm)].groupby("Collision Resolve Select Algorithm")
            for grp, vals in tempData:
                ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Dropped Flows',
                               c=colors.__getitem__(resolveSelectAlgorithms.index(grp)),
                               linestyle=lineStyles.__getitem__(resolveSelectAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                               marker=markers.__getitem__(resolveSelectAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1) , label=grp,
                               ylabel='Mean Of Dropped Flows',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
            plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
            #plt.title("{} Scheduler - {} attack - collisionResolveByDropping resolve method".format(schedulingAlgorithm,attackType), fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
            plt.ylabel('Percentage Of Dropped Flows', fontsize= lineGraphFormat.__getitem__(5))
            plt.savefig('Results/plots/{}/withCollisionResolve/{}/resolveByDroppingVSdroppedTSNFlows.png'.format(attackType,schedulingAlgorithm))
            plt.show()


        # line graph attack rate vs. Mean Of Dropped Flows (per resolve algorithm) for each scheduling algorithm for delay resolve method
        for schedulingAlgorithm in schedulingAlgorithms:
            fig, ax = plt.subplots()
            tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Dropped Flows","Collision Resolve Method", "Collision Resolve Select Algorithm"]][
                statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1][
                statisticsData["Collision Resolve Method"] == 'collisionResolveByDelaying'][
                statisticsData["Scheduling Algorithm"] == '{}'.format(schedulingAlgorithm)].groupby(
                "Collision Resolve Select Algorithm")
            for grp, vals in tempData:
                ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Dropped Flows',
                               c=colors.__getitem__(resolveSelectAlgorithms.index(grp)),
                               linestyle=lineStyles.__getitem__(resolveSelectAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                               marker=markers.__getitem__(resolveSelectAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1) , label=grp,
                               ylabel='Mean Of Dropped Flows',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
            plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
            #plt.title("{} Scheduler - {} attack - collisionResolveByDelaying resolve method".format(schedulingAlgorithm, attackType), fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
            plt.ylabel('Percentage of Dropped Flows', fontsize= lineGraphFormat.__getitem__(5))
            plt.savefig('Results/plots/{}/withCollisionResolve/{}/resolveByDelayingVSdroppedTSNFlows.png'.format(attackType, schedulingAlgorithm))
            plt.show()

        ########


        #  line graph attack rate vs. Mean Of Dropped Flows (per resolve algorithm) for each scheduling algorithm for both resolve methods
        for schedulingAlgorithm in schedulingAlgorithms:
            fig, ax = plt.subplots()
            tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Dropped Flows","Collision Resolve Method", "Collision Resolve Select Algorithm"]][
                statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1][
                statisticsData["Scheduling Algorithm"] == '{}'.format(schedulingAlgorithm)].groupby("Collision Resolve Method")
            for resolveMethodGrp, resolveMethodVals in tempData:
                secondTempData = resolveMethodVals.groupby("Collision Resolve Select Algorithm")
                labelFirstVal = 'Delay' if resolveMethodGrp == 'collisionResolveByDelaying' else 'Drop'
                for selectAlgorithmGrp, selectAlgorithmVals in secondTempData:
                    if (selectAlgorithmGrp == 'basedOnNBOfCollisions'):
                        labelSecondVal = '# of collisions'
                    elif(selectAlgorithmGrp == 'basedOnTheSoonestDeadline'):
                        labelSecondVal = 'soonest deadline'
                    elif(selectAlgorithmGrp == 'basedOnTheShortestDelay'):
                        labelSecondVal = 'shortest delay'
                    else:
                        labelSecondVal = 'earliest arrival'
                    ax = selectAlgorithmVals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Dropped Flows',
                                c=colors.__getitem__(resolveSelectAlgorithms.index(selectAlgorithmGrp)),
                                linestyle=lineStyles.__getitem__(resolveMethods.index(resolveMethodGrp)), linewidth= lineGraphFormat.__getitem__(0),
                                marker=markers.__getitem__(resolveSelectAlgorithms.index(selectAlgorithmGrp)), markersize= lineGraphFormat.__getitem__(1),
                                label='{}({})'.format(labelFirstVal, labelSecondVal),
                                ylabel='Mean Of Dropped Flows',figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
            plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
            #plt.title("The mean of dropped TSN flows when {} Scheduler\n is used that is resulted from {} \nattack for different attack rates for different collisions resolve\n select algorithms".format(schedulingAlgorithm,attackType), fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
            plt.ylabel('Percentage of Dropped Flows', fontsize= lineGraphFormat.__getitem__(5))
            plt.savefig('Results/plots/{}/withCollisionResolve/{}/resolveMethodsVSdroppedTSNFlows.png'.format(attackType, schedulingAlgorithm))
            plt.show()

        ########








    except:

        # create the graphs' directories
        #####################################################
        tempData = statisticsData[["Scheduling Algorithm", "Attack Rate"]].groupby("Scheduling Algorithm")
        for schedulingAlgorithm, vals in tempData:
            try:
                os.makedirs('Results/plots/{}/withoutCollisionResolve/{}'.format(attackType, schedulingAlgorithm))
            except OSError:
                pass
        try:
            os.makedirs('Results/plots/{}/withoutCollisionResolve/attackRate'.format(attackType))
        except OSError:
            pass
        try:
            os.makedirs('Results/plots/{}/withoutCollisionResolve/attackStartTime'.format(attackType))
        except OSError:
            pass
        #####################################################





        # line graph attack rate vs. Mean Of Collided Flows Percentage
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collided Flows Percentage"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby("Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Collided Flows Percentage',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize=lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Percentage of Collided TSN Flows', figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best',fontsize= lineGraphFormat.__getitem__(3))
        #plt.title("The percentage of collided TSN flows resulted from {} \nattack for different attack rates".format(attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Percentage of Collided TSN Flows', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackRate/attackRateVScollidedFlows_line.png'.format(attackType))
        plt.show()

        # scatter graph attack rate vs. Mean Of Collided Flows Percentage
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collided Flows Percentage"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Rate', y='Mean Of Collided Flows Percentage',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Percentage of Collided TSN Flows', figsize=(12, 8),fontsize= scatterGraphFormat.__getitem__(0))
        plt.legend(loc='best',fontsize= lineGraphFormat.__getitem__(1))
        # plt.title("The percentage of collided TSN flows resulted from {} \nattack for different attack rates".format(
        #     attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', lineGraphFormat.__getitem__(2))
        plt.ylabel('Percentage of Collided TSN Flows', lineGraphFormat.__getitem__(3))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackRate/attackRateVScollidedFlows_scatter.png'.format(attackType))
        plt.show()

        # scatter graph attack rate vs. Mean Of Collided Flows Percentage (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collided Flows Percentage"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Rate', y='Mean Of Collided Flows Percentage',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Percentage of Collided TSN Flows', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
            #plt.title("The percentage of collided TSN flows resulted from {} \nattack for different attack rates".format(attackType), fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Attack Intensity (AI)', fontsize= scatterGraphFormat.__getitem__(2))
            plt.ylabel('Percentage of Collided TSN Flows', fontsize= scatterGraphFormat.__getitem__(3))
            plt.savefig('Results/plots/{}/withoutCollisionResolve/{}/attackRateVScollidedFlows_scatter.png'.format(attackType,grp))
            plt.show()

        # line graph attack start time vs. Mean Of Collided Flows Percentage
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collided Flows Percentage"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby("Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Start Time', y='Mean Of Collided Flows Percentage',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Percentage of Collided TSN Flows', figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best',fontsize= lineGraphFormat.__getitem__(3))
        # plt.title(
        #     "The percentage of collided TSN flows resulted from {} \nattack for different attack start times".format(
        #         attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Percentage of Collided TSN Flows', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackStartTime/attackStartTimeVScollidedFlows_line.png'.format(attackType))
        plt.show()

        # scatter graph attack start time vs. Mean Of Collided Flows Percentage
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collided Flows Percentage"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Start Time', y='Mean Of Collided Flows Percentage',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Percentage of Collided TSN Flows', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
        plt.legend(loc='best', fontsize= scatterGraphFormat.__getitem__(1))
        # plt.title(
        #     "The percentage of collided TSN flows resulted from {} \nattack for different attack start times".format(
        #         attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= scatterGraphFormat.__getitem__(2))
        plt.ylabel('Percentage of Collided TSN Flows', fontsize= scatterGraphFormat.__getitem__(3))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackStartTime/attackStartTimeVScollidedFlows_scatter.png'.format(attackType))
        plt.show()

        # scatter graph attack start time vs. Mean Of Collided Flows Percentage (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collided Flows Percentage"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Start Time', y='Mean Of Collided Flows Percentage',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Percentage of Collided TSN Flows', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
            #plt.title("The percentage of collided TSN flows resulted from {} \nattack for different attack start times".format(attackType), fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= scatterGraphFormat.__getitem__(2))
            plt.ylabel('Percentage of Collided TSN Flows', fontsize= scatterGraphFormat.__getitem__(3))
            plt.savefig('Results/plots/{}/withoutCollisionResolve/{}/attackStartTimeVScollidedFlows_scatter.png'.format(attackType,grp))
            plt.show()

        # line graph attack rate vs. Mean Of Distinct Collisions
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Distinct Collisions"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Distinct Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Mean Of TSN FLows\' Distinct Collisions', figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        # plt.title(
        #     "The mean of TSN flows' distinct collisions resulted from {} \nattack for different attack rates".format(
        #         attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Mean Of Distinct Collisions', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackRate/attackRateVSdistinctCollisions_line.png'.format(attackType))
        plt.show()

        # scatter graph attack rate vs. Mean Of Distinct Collisions
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Distinct Collisions"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Rate', y='Mean Of Distinct Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Mean Of TSN FLows\' Distinct Collisions', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
        plt.legend(loc='best', fontsize= scatterGraphFormat.__getitem__(1))
        # plt.title(
        #     "The mean of TSN flows' distinct collisions resulted from {} \nattack for different attack rates".format(
        #         attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= scatterGraphFormat.__getitem__(2))
        plt.ylabel('Mean Of Distinct Collisions', fontsize= scatterGraphFormat.__getitem__(3))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackRate/attackRateVSdistinctCollisions_scatter.png'.format(attackType))
        plt.show()

        # scatter graph attack rate vs. Mean Of Distinct Collisions (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Distinct Collisions"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Rate', y='Mean Of Distinct Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Mean Of TSN FLows\' Distinct Collisions', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
            #plt.title("The mean of TSN flows' distinct collisions resulted from {} \nattack for different attack rates".format(attackType), fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Attack Intensity (AI)', fontsize= scatterGraphFormat.__getitem__(2))
            plt.ylabel('Mean Of Distinct Collisions', fontsize= scatterGraphFormat.__getitem__(3))
            plt.savefig('Results/plots/{}/withoutCollisionResolve/{}/attackRateVSdistinctCollisions_scatter.png'.format(attackType,grp))
            plt.show()

        # line graph attack start time vs. Mean Of Distinct Collisions
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Distinct Collisions"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Start Time', y='Mean Of Distinct Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Mean Of TSN FLows\' Distinct Collisions', figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        # plt.title(
        #     "The mean of TSN flows' distinct collisions resulted from {} \nattack for different attack start times".format(
        #         attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Mean Of Distinct Collisions', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackStartTime/attackStartTimeVSdistinctCollisions_line.png'.format(attackType))
        plt.show()

        # scatter graph attack start time vs. Mean Of Distinct Collisions
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Distinct Collisions"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Start Time', y='Mean Of Distinct Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Mean Of TSN FLows\' Distinct Collisions', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
        plt.legend(loc='best', fontsize= scatterGraphFormat.__getitem__(1))
        #plt.title("The mean of TSN flows' distinct collisions resulted from {} \nattack for different attack start times".format(attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= scatterGraphFormat.__getitem__(2))
        plt.ylabel('Mean Of Distinct Collisions', fontsize= scatterGraphFormat.__getitem__(3))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackStartTime/attackStartTimeVSdistinctCollisions_scatter.png'.format(attackType))
        plt.show()

        # scatter graph attack start time vs. Mean Of Distinct Collisions (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Distinct Collisions"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Start Time', y='Mean Of Distinct Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Mean Of TSN FLows\' Distinct Collisions', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
            #plt.title("The mean of TSN flows' distinct collisions resulted from {} \nattack for different attack start times".format(attackType), fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= scatterGraphFormat.__getitem__(2))
            plt.ylabel('Mean Of Distinct Collisions', fontsize= scatterGraphFormat.__getitem__(3))
            plt.savefig('Results/plots/{}/withoutCollisionResolve/{}/attackStartTimeVSdistinctCollisions_scatter.png'.format(attackType,grp))
            plt.show()

        # line graph attack rate vs. Mean Of Collisions
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collisions"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Rate', y='Mean Of Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Mean Of TSN FLows\' Collisions', figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        # plt.title(
        #     "The mean of TSN flows' collisions resulted from {} \nattack for different attack rates".format(attackType),
        #     fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Mean Of Collisions', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackRate/attackRateVStotalCollisions_line.png'.format(attackType))
        plt.show()

        # scatter graph attack rate vs. Mean Of Collisions
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collisions"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Rate', y='Mean Of Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Mean Of TSN FLows\' Collisions', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
        plt.legend(loc='best', fontsize= scatterGraphFormat.__getitem__(1))
        #plt.title("The mean of TSN flows' collisions resulted from {} \nattack for different attack rates".format(attackType),fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Attack Intensity (AI)', fontsize= scatterGraphFormat.__getitem__(2))
        plt.ylabel('Mean Of Collisions', fontsize= scatterGraphFormat.__getitem__(3))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackRate/attackRateVStotalCollisions_scatter.png'.format(attackType))
        plt.show()

        # scatter graph attack rate vs. Mean Of Collisions (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[
            ["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collisions"]][
            statisticsData["Attack Start Time"] == 0][statisticsData["Attack Rate"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Rate', y='Mean Of Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Mean Of TSN FLows\' Collisions', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
            #plt.title("The mean of TSN flows' collisions resulted from {} \nattack for different attack rates".format(attackType),fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Attack Intensity (AI)', fontsize= scatterGraphFormat.__getitem__(2))
            plt.ylabel('Mean Of Collisions', fontsize= scatterGraphFormat.__getitem__(3))
            plt.savefig('Results/plots/{}/withoutCollisionResolve/{}/attackRateVStotalCollisions_scatter.png'.format(attackType,grp))
            plt.show()

        # line graph attack start time vs. Mean Of Collisions
        fig, ax = plt.subplots()
        tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collisions"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='line', x='Attack Start Time', y='Mean Of Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)), linewidth= lineGraphFormat.__getitem__(0),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), markersize= lineGraphFormat.__getitem__(1), label=grp,
                           ylabel='Mean Of TSN FLows\' Collisions', figsize=(12, 8), fontsize= lineGraphFormat.__getitem__(2))
        plt.legend(loc='best', fontsize= lineGraphFormat.__getitem__(3))
        # plt.title("The mean of TSN flows' collisions resulted from {} \nattack for different attack start times".format(
        #     attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= lineGraphFormat.__getitem__(4))
        plt.ylabel('Mean Of Collisions', fontsize= lineGraphFormat.__getitem__(5))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackStartTime/attackStartTimeVStotalCollisions_line.png'.format(attackType))
        plt.show()

        # scatter graph attack start time vs. Mean Of Collisions
        fig, ax = plt.subplots()
        tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collisions"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Start Time', y='Mean Of Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Mean Of TSN FLows\' Collisions', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
        plt.legend(loc='best', fontsize= scatterGraphFormat.__getitem__(1))
        #plt.title("The mean of TSN flows' collisions resulted from {} \nattack for different attack start times".format(attackType), fontsize=10)
        plt.grid(color='grey', linestyle='--', linewidth=0.5)
        plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= scatterGraphFormat.__getitem__(2))
        plt.ylabel('Mean Of Collisions', fontsize= scatterGraphFormat.__getitem__(3))
        plt.savefig('Results/plots/{}/withoutCollisionResolve/attackStartTime/attackStartTimeVStotalCollisions_scatter.png'.format(attackType))
        plt.show()

        # scatter graph attack start time vs. Mean Of Collisions (per scheduling algorithm)
        fig, ax = plt.subplots()
        tempData = statisticsData[["Scheduling Algorithm", "Attack Rate", "Attack Start Time", "Mean Of Collisions"]][
            statisticsData["Attack Rate"] == 0.5][statisticsData["Attack Start Time"] <= 1].groupby(
            "Scheduling Algorithm")
        for grp, vals in tempData:
            ax = vals.plot(ax=ax, kind='scatter', x='Attack Start Time', y='Mean Of Collisions',
                           c=colors.__getitem__(schedulingAlgorithms.index(grp)),
                           linestyle=lineStyles.__getitem__(schedulingAlgorithms.index(grp)),
                           marker=markers.__getitem__(schedulingAlgorithms.index(grp)), label=grp,
                           ylabel='Mean Of TSN FLows\' Collisions', figsize=(12, 8), fontsize= scatterGraphFormat.__getitem__(0))
            #plt.title("The mean of TSN flows' collisions resulted from {} \nattack for different attack start times".format(attackType), fontsize=10)
            plt.grid(color='grey', linestyle='--', linewidth=0.5)
            plt.xlabel('Normalized Attack Starting Orders (NASO)', fontsize= scatterGraphFormat.__getitem__(2))
            plt.ylabel('Mean Of Collisions', fontsize= scatterGraphFormat.__getitem__(3))
            plt.savefig('Results/plots/{}/withoutCollisionResolve/{}/attackStartTimeVStotalCollisions_scatter.png'.format(attackType,grp))
            plt.show()




def importDeleteResults(attackType):
    if(not Path('Results/{}/runs.csv'.format(attackType)).is_file()):
        exportDeleteRunsData(attackType)
    if (not Path('Results/{}/statistics.csv'.format(attackType)).is_file()):
        exportDeleteStatistics(attackType)
    runsData = pd.read_csv('Results/{}/runs.csv'.format(attackType))
    statisticsData = pd.read_csv('Results/{}/statistics.csv'.format(attackType))
    return runsData,statisticsData

def exportDeleteRunsData(attackType):
    tempContent = retriveResults.findLatestResults(attackType)
    if ('ResolveMethod'.lower() in tempContent.__getitem__(0).__getitem__(1).__getitem__(0).lower()):
        returnedText = "Type of Attack,Scheduling Algorithm,Attack Rate,Attack Start Time,Collision Resolve Method,Collision Resolve Select Algorithm,Run Number,The Total Number of TSN Flows,The Percentage of Hidden Flows,The Percentage of Collided Flows,The Total Number of Distinct Collisions,The Total Number of Collisions,The Percentage of Dropped Flows\n"
        for tempEntry in tempContent:
            for i in range(len(tempEntry.__getitem__(1))):
                if (("statistics" not in tempEntry.__getitem__(1).__getitem__(i).lower()) and ("csv" not in tempEntry.__getitem__(1).__getitem__(i).lower()) and ('tsnflows' not in tempEntry.__getitem__(1).__getitem__(i).lower()) and ('per' not in tempEntry.__getitem__(1).__getitem__(i).lower())):
                    typeOfAttack = ' '.join([x.capitalize() for x in tempEntry.__getitem__(0).split('/').__getitem__(1).split('_')])
                    schedulingAlgorithm = tempEntry.__getitem__(0).split('/').__getitem__(4)
                    attackRate = float(tempEntry.__getitem__(1).__getitem__(i).split(',').__getitem__(1).split("=").__getitem__(1))
                    attackStartTime = float(tempEntry.__getitem__(1).__getitem__(i).split(',').__getitem__(2).split("=").__getitem__(1))
                    collisionResolveMethod = 'Collision ' + ' '.join([x.capitalize() for x in camel_case_split(tempEntry.__getitem__(1).__getitem__(i).split(',').__getitem__(3).split("=").__getitem__(1))])
                    collisionResolveSelectAlgorithm = 'Based ' + ' '.join([x.capitalize() for x in camel_case_split(tempEntry.__getitem__(1).__getitem__(i).split(',').__getitem__(4).split("=").__getitem__(1))])

                    tempParts = tempEntry.__getitem__(2).__getitem__(i).split("--------------------------------------------------")
                    tempRuns = tempParts.__getitem__(2)
                    runParts = tempRuns.replace("\n\n", "\n").replace("\n\n", "\n").strip().split("<<<")
                    tempIndex = 1
                    for runPart in runParts:
                        if ("run" in runPart.lower()):
                            runNumber = runPart.split(">>>").__getitem__(1).strip().split(" ").__getitem__(2)

                            nbOfTSNFlows = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(1).strip().split("\n").__getitem__(0))  # *
                            hiddenFlows = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(6).strip().split("\n").__getitem__(0).replace("%", ""))
                            collidedFlows = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(8).strip().split("\n").__getitem__(0).replace("%", ""))
                            distinctCollisions = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(9).strip().split("\n").__getitem__(0))
                            totalCollisions = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(10).strip().split("\n").__getitem__(0))
                            droppedFlows = runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(-1).strip().replace("\n", "").replace("%", "")
                            tempIndex = tempIndex + 1
                            returnedText = returnedText + "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                                typeOfAttack, schedulingAlgorithm, float(attackRate), float(attackStartTime),
                                collisionResolveMethod, collisionResolveSelectAlgorithm, int(runNumber),
                                float(nbOfTSNFlows), float(hiddenFlows), float(collidedFlows),
                                float(distinctCollisions), float(totalCollisions), float(droppedFlows))


    else:
        returnedText = "Type of Attack,Scheduling Algorithm,Attack Rate,Attack Start Time,Run Number,The Total Number of TSN Flows,The Percentage of Hidden Flows,The Percentage of Collided Flows,The Total Number of Distinct Collisions,The Total Number of Collisions\n"
        for tempEntry in tempContent:
            for i in range(len(tempEntry.__getitem__(1))):
                if (("statistics" not in tempEntry.__getitem__(1).__getitem__(i).lower()) and ("csv" not in tempEntry.__getitem__(1).__getitem__(i).lower()) and ('tsnflows' not in tempEntry.__getitem__(1).__getitem__(i).lower()) and ('per' not in tempEntry.__getitem__(1).__getitem__(i).lower())):
                    typeOfAttack = ' '.join([x.capitalize() for x in tempEntry.__getitem__(0).split('/').__getitem__(1).split('_')])
                    schedulingAlgorithm = tempEntry.__getitem__(0).split('/').__getitem__(4)
                    attackRate = float(tempEntry.__getitem__(1).__getitem__(i).split(',').__getitem__(1).split("=").__getitem__(1))
                    tempAttackStartTime = tempEntry.__getitem__(1).__getitem__(i).split(',').__getitem__(2).split("=").__getitem__(1).split('.')
                    attackStartTime = float('{}.{}'.format(tempAttackStartTime.__getitem__(0),tempAttackStartTime.__getitem__(1)))

                    tempParts = tempEntry.__getitem__(2).__getitem__(i).split("--------------------------------------------------")
                    tempRuns = tempParts.__getitem__(2)
                    runParts = tempRuns.replace("\n\n", "\n").replace("\n\n", "\n").strip().split("<<<")
                    tempIndex = 1
                    for runPart in runParts:
                        if ("run" in runPart.lower()):
                            runNumber = runPart.split(">>>").__getitem__(1).strip().split(" ").__getitem__(2)
                            nbOfTSNFlows = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(1).strip().split("\n").__getitem__(0))  # *
                            hiddenFlows = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(6).strip().split("\n").__getitem__(0).replace("%", ""))
                            collidedFlows = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(8).strip().split("\n").__getitem__(0).replace("%", ""))
                            distinctCollisions = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(9).strip().split("\n").__getitem__(0))
                            totalCollisions = float(runParts.__getitem__(tempIndex).split(">>>").__getitem__(0).split(":").__getitem__(-1).strip().split("\n").__getitem__(0))
                            tempIndex = tempIndex + 1
                            returnedText = returnedText + "{},{},{},{},{},{},{},{},{},{}\n".format(
                                typeOfAttack, schedulingAlgorithm, float(attackRate), float(attackStartTime),
                                int(runNumber), float(nbOfTSNFlows), float(hiddenFlows), float(collidedFlows),
                                float(distinctCollisions), float(totalCollisions))

    #################################################
    # save the new file
    try:
        saveDir = "Results/{}".format(attackType)
        os.makedirs(saveDir)
    except OSError:
        pass
    filePath = "{}/{}".format(saveDir, "runs.csv")
    f = open(filePath, "w+")
    f.write(returnedText)
    f.close()

def exportDeleteStatistics(attackType):
    tempContent = retriveResults.findLatestResults(attackType)
    resolveMehodsFlag = len(tempContent.__getitem__(0).__getitem__(1).__getitem__(0).split(',')) > 3
    if(resolveMehodsFlag):
        returnedText = "Type of Attack,Scheduling Algorithm,Attack Rate,Attack Start Time,Collision Resolve Method,Collision Resolve Select Algorithm,Min,Max,Mean Of Collided Flows Percentage,Mean Of Distinct Collisions,Mean Of Collisions,Mean Of Dropped Flows,Median,Mode,Standard Deviation,Variance\n"
        for tempEntry in tempContent:
            tempIndex = -1
            for fileName in tempEntry.__getitem__(1):
                tempIndex = tempIndex + 1
                if "'" in fileName or "statistics" not in fileName.lower():
                    continue
                dirPath = tempEntry.__getitem__(0)
                splittedDir = dirPath.split("/")

                # Read Parameters
                typeOfAttack = " ".join([x.capitalize() for x in splittedDir.__getitem__(1).split("_")])
                schedulingAlgorithm = splittedDir.__getitem__(-1).strip()
                attackRate = float(fileName.split(",").__getitem__(1).split("=").__getitem__(1))
                attackStartTime = float(fileName.split(",").__getitem__(2).split("=").__getitem__(1))
                collisionResolveMethod = fileName.split(",").__getitem__(3).split("=").__getitem__(1)
                collisionResolveSelectAlgorithm = fileName.split(",").__getitem__(4).split("_").__getitem__(0).split("=").__getitem__(1)

                # Read Statistics
                fileContent = tempEntry.__getitem__(2).__getitem__(tempIndex).split("--------------------------------------------------").__getitem__(2).strip("\n")
                splittedFileContent = fileContent.split("\n")
                min0 = round(float(splittedFileContent.__getitem__(0).split(":").__getitem__(1)), 2)
                max0 = round(float(splittedFileContent.__getitem__(1).split(":").__getitem__(1)), 2)
                mean0 = round(float(splittedFileContent.__getitem__(2).split(":").__getitem__(1)), 2)
                mean1 = round(float(splittedFileContent.__getitem__(3).split(":").__getitem__(1)), 2)
                mean2 = round(float(splittedFileContent.__getitem__(4).split(":").__getitem__(1)), 2)
                mean3 = round(float(splittedFileContent.__getitem__(5).split(":").__getitem__(1)), 2)
                median0 = round(float(splittedFileContent.__getitem__(6).split(":").__getitem__(1)), 2)
                mode0 = round(float(splittedFileContent.__getitem__(7).split(":").__getitem__(1)), 2)
                stDev0 = round(float(splittedFileContent.__getitem__(8).split(":").__getitem__(1)), 2)
                variance0 = round(float(splittedFileContent.__getitem__(9).split(":").__getitem__(1)), 2)

                returnedText = returnedText + "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(typeOfAttack,schedulingAlgorithm,attackRate,attackStartTime,collisionResolveMethod,collisionResolveSelectAlgorithm,min0, max0, mean0,mean1,mean2, mean3, median0, mode0,stDev0, variance0)


    else:
        returnedText = "Type of Attack,Scheduling Algorithm,Attack Rate,Attack Start Time,Min,Max,Mean Of Collided Flows Percentage,Mean Of Distinct Collisions,Mean Of Collisions,Median,Mode,Standard Deviation,Variance\n"
        for tempEntry in tempContent:
            tempIndex = -1
            for fileName in tempEntry.__getitem__(1):
                tempIndex = tempIndex + 1
                if "'" in fileName or "statistics" not in fileName.lower():
                    continue
                dirPath = tempEntry.__getitem__(0)
                splittedDir = dirPath.split("/")

                # Read Parameters
                typeOfAttack = " ".join([x.capitalize() for x in splittedDir.__getitem__(1).split("_")])
                schedulingAlgorithm = splittedDir.__getitem__(-1).strip()
                attackRate = float(fileName.split(",").__getitem__(1).split("=").__getitem__(1))
                attackStartTime = float(
                    fileName.split(",").__getitem__(2).split("_").__getitem__(0).split("=").__getitem__(1))

                # Read Statistics
                fileContent = tempEntry.__getitem__(2).__getitem__(tempIndex).split(
                    "--------------------------------------------------").__getitem__(2).strip("\n")
                splittedFileContent = fileContent.split("\n")
                min0 = round(float(splittedFileContent.__getitem__(0).split(":").__getitem__(1)), 2)
                max0 = round(float(splittedFileContent.__getitem__(1).split(":").__getitem__(1)), 2)
                mean0 = round(float(splittedFileContent.__getitem__(2).split(":").__getitem__(1)), 2)
                mean1 = round(float(splittedFileContent.__getitem__(3).split(":").__getitem__(1)), 2)
                mean2 = round(float(splittedFileContent.__getitem__(4).split(":").__getitem__(1)), 2)
                median0 = round(float(splittedFileContent.__getitem__(5).split(":").__getitem__(1)), 2)
                mode0 = round(float(splittedFileContent.__getitem__(6).split(":").__getitem__(1)), 2)
                stDev0 = round(float(splittedFileContent.__getitem__(7).split(":").__getitem__(1)), 2)
                variance0 = round(float(splittedFileContent.__getitem__(8).split(":").__getitem__(1)), 2)

                returnedText = returnedText + "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(typeOfAttack,schedulingAlgorithm,attackRate, attackStartTime,min0, max0, mean0, mean1,mean2, median0, mode0,stDev0, variance0)

    # save the new file
    try:
        saveDir = "Results/{}".format(attackType)
        os.makedirs(saveDir)
    except OSError:
        pass
    filePath = "{}/{}".format(saveDir, "statistics.csv")
    f = open(filePath, "w+")
    f.write(returnedText)
    f.close()

def camel_case_split(str):
    return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)