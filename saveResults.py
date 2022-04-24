import os
import statistics

def writeInsertResultsToFile(listOfResults,simulationParameters,now):
    folderPath,resultFileTitle,resultText,statisticsFileTitle,statisticsText,resultsStatistics = prepareInsertResultsForWriting(listOfResults,simulationParameters,now)
    try:
        os.makedirs(folderPath)
    except OSError:
        pass
    resultFile = "{}/{}".format(folderPath,resultFileTitle)
    f = open(resultFile, "w+")
    f.write(resultText)
    f.close()
    resultStatisticsFile = "{}/{}".format(folderPath, statisticsFileTitle)
    f = open(resultStatisticsFile, "w+")
    f.write(statisticsText)
    f.close()
    return resultsStatistics

def writeDeleteResultsToFile(listOfResults,simulationParameters,now):

    if(len(listOfResults.__getitem__(0))==8):
        folderPath,resultFileTitle,resultText,collisionsPerFlowFileTitle,collisionsPerFlowText,collisionsPerRunFileTitle,collisionsPerRunText,statisticsFileTitle,statisticsText,resultsStatistics = prepareDeleteResultsForWriting(listOfResults,simulationParameters,now)
    else:
        folderPath,resultFileTitle,resultText,collisionsPerFlowFileTitle,collisionsPerFlowText,collisionsPerRunFileTitle,collisionsPerRunText,droppedTSNFlowsFileTitle,droppedTSNFlowsText,statisticsFileTitle,statisticsText,resultsStatistics = prepareDeleteResultsForWriting(listOfResults,simulationParameters,now)

    try:
        os.makedirs(folderPath)
    except OSError:
        pass
    resultFile = "{}/{}".format(folderPath,resultFileTitle)
    f = open(resultFile, "w+")
    f.write(resultText)
    f.close()
    collisionsPerFlowFile = "{}/{}".format(folderPath, collisionsPerFlowFileTitle)
    f = open(collisionsPerFlowFile, "w+")
    f.write(collisionsPerFlowText)
    f.close()
    collisionsPerRunFile = "{}/{}".format(folderPath, collisionsPerRunFileTitle)
    f = open(collisionsPerRunFile, "w+")
    f.write(collisionsPerRunText)
    f.close()
    resultStatisticsFile = "{}/{}".format(folderPath, statisticsFileTitle)
    f = open(resultStatisticsFile, "w+")
    f.write(statisticsText)
    f.close()

    if (len(listOfResults.__getitem__(0)) != 8):
        droppedTSNFlowsFile = "{}/{}".format(folderPath, droppedTSNFlowsFileTitle)
        f = open(droppedTSNFlowsFile, "w+")
        f.write(droppedTSNFlowsText)
        f.close()
    return resultsStatistics

def writeInsertResultsToFileCase2(summaryOfTheResults, simulationParameters, now):
    if(isinstance(simulationParameters.__getitem__(3),str) and isinstance(simulationParameters.__getitem__(4),str)):
        folderPath, fileTitle, fileText = prepareInsertResultsForWritingCase3(summaryOfTheResults, simulationParameters, now)
    else:
        folderPath, fileTitle, fileText = prepareInsertResultsForWritingCase2(summaryOfTheResults,simulationParameters,now)
    try:
        os.makedirs(folderPath)
    except OSError:
        pass
    filePath = "{}/{}".format(folderPath,fileTitle)
    f = open(filePath, "w+")
    f.write(fileText)
    f.close()


def writeDeleteResultsToFileCase2(summaryOfTheResults, simulationParameters, now):
    if(isinstance(simulationParameters.__getitem__(3),str) and isinstance(simulationParameters.__getitem__(4),str)):
        folderPath, fileTitle, fileText = prepareDeleteResultsForWritingCase3(summaryOfTheResults, simulationParameters, now)
    else:
        folderPath, fileTitle, fileText = prepareDeleteResultsForWritingCase2(summaryOfTheResults,simulationParameters,now)
    try:
        os.makedirs(folderPath)
    except OSError:
        pass
    filePath = "{}/{}".format(folderPath,fileTitle)
    f = open(filePath, "w+")
    f.write(fileText)
    f.close()

def writeDeleteResultsToFileCase3(summaryOfTheResults, simulationParameters, now):
    folderPath, fileTitle, fileText, CSVFileFolder, CSVFileTitle, CSVFileText = prepareDeleteResultsForWritingCase4(summaryOfTheResults, simulationParameters, now)

    try:
        os.makedirs(folderPath)
    except OSError:
        pass
    filePath = "{}/{}".format(folderPath,fileTitle)
    f = open(filePath, "w+")
    f.write(fileText)
    f.close()

    try:
        os.makedirs(CSVFileFolder)
    except OSError:
        pass
    anotherFilePath = "{}/{}".format(CSVFileFolder,CSVFileTitle)
    f = open(anotherFilePath, "w+")
    f.write(CSVFileText)
    f.close()


def prepareInsertResultsForWritingCase3(listOfResults,simulationParameters,now):
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H.%M.%S")
    dt_string = now.strftime("Date: %B %d, %Y \nTime: %H:%M:%S\n\n\n\n")
    folderPath = "Results/{}/{}/{}/{}".format(simulationParameters.__getitem__(2), date, time, simulationParameters.__getitem__(1))
    fileTitle = "NoR={},attackRate={},startTime={}_Statistics.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
    fileText = dt_string
    fileText = fileText + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n\n".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(1),simulationParameters.__getitem__(2),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
    fileText = fileText + "===========================================================\n\n"
    fileText = fileText + "[+] attack_start_time={}:\n\n".format(listOfResults.__getitem__(0).__getitem__(0))
    for i in range(len(listOfResults.__getitem__(0))):
        fileText = fileText + "\tattack_rate={} --> min={} , max={} , mean={} , median={} , mode={} , standard_deviation={} , variance = {}\n".format(
            listOfResults.__getitem__(1).__getitem__(i), listOfResults.__getitem__(2).__getitem__(i),
            listOfResults.__getitem__(3).__getitem__(i), listOfResults.__getitem__(4).__getitem__(i),
            listOfResults.__getitem__(5).__getitem__(i), listOfResults.__getitem__(6).__getitem__(i),
            listOfResults.__getitem__(7).__getitem__(i), listOfResults.__getitem__(8).__getitem__(i))
        if(i<len(listOfResults.__getitem__(0))-2):
            if(listOfResults.__getitem__(0).__getitem__(i)<listOfResults.__getitem__(0).__getitem__(i+1)):
                fileText = fileText + "\n\n===========================================================\n\n[+] attack_start_time={}:\n\n".format(listOfResults.__getitem__(0).__getitem__(i+1))
    fileText = fileText + "\n\n===========================================================\n\n"


    return folderPath, fileTitle, fileText

def prepareInsertResultsForWritingCase2(listOfResults,simulationParameters,now):
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H.%M.%S")
    dt_string = now.strftime("Date: %B %d, %Y \nTime: %H:%M:%S\n\n\n\n")
    isAttackRate = (False if isinstance(simulationParameters.__getitem__(3), float) else True)
    folderPath = "Results/{}/{}/{}/{}".format(simulationParameters.__getitem__(2), date, time, simulationParameters.__getitem__(1))
    fileTitle = "NoR={},attackRate={},startTime={}_Statistics.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
    preText = ("attack_rate" if isAttackRate else "attack_start_time")
    fileText = dt_string
    fileText = fileText + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(1),simulationParameters.__getitem__(2),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
    for i in range(len(listOfResults.__getitem__(0))):
        fileText = fileText + "{}={} --> min={} , max={} , mean={} , median={} , mode={} , standard_deviation={} , variance = {}\n".format(preText,listOfResults.__getitem__(0).__getitem__(i),listOfResults.__getitem__(1).__getitem__(i),listOfResults.__getitem__(2).__getitem__(i),listOfResults.__getitem__(3).__getitem__(i),listOfResults.__getitem__(4).__getitem__(i),listOfResults.__getitem__(5).__getitem__(i),listOfResults.__getitem__(6).__getitem__(i),listOfResults.__getitem__(7).__getitem__(i))


    return folderPath, fileTitle, fileText



def prepareInsertResultsForWriting(listOfResults,simulationParameters,now):
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H.%M.%S")
    dt_string = now.strftime("Date: %B %d, %Y \nTime: %H:%M:%S\n\n\n\n")
    resultText = dt_string
    resultText = resultText + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(1),simulationParameters.__getitem__(2),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
    for i in range(len(listOfResults)):
        resultText = resultText + ">>> RUN NUMBER {} <<<\n\n".format(i+1)
        resultText = resultText + "The total number of real TSN flows: {}\n".format(listOfResults.__getitem__(i).__getitem__(0))
        resultText = resultText + "nb of total routed flows (real and unreal): {}\n".format(listOfResults.__getitem__(i).__getitem__(1))
        resultText = resultText + "nb of routed real flows: {}\n".format(listOfResults.__getitem__(i).__getitem__(2))
        resultText = resultText + "nb of scheduled flows using {}: {}\n".format(simulationParameters.__getitem__(1),listOfResults.__getitem__(i).__getitem__(3))
        resultText = resultText + "The percentage of scheduled flows to routed flows: {}%\n\n\n\n".format(round(listOfResults.__getitem__(i).__getitem__(4),2))

    min0 = min(map(lambda tempList: tempList[4], listOfResults))
    max0 = max(map(lambda tempList: tempList[4], listOfResults))
    mean0 = statistics.mean(map(lambda tempList: tempList[4], listOfResults))
    median0 = statistics.median(map(lambda tempList: tempList[4], listOfResults))
    mode0 = statistics.mode(map(lambda tempList: tempList[4], listOfResults))
    stdev0 = "NONE"
    variance0 = "NONE"
    if(simulationParameters.__getitem__(0)>1):
        stdev0 = statistics.stdev(map(lambda tempList: tempList[4], listOfResults), mean0)
    if(simulationParameters.__getitem__(0)>1):
        variance0 = statistics.variance(map(lambda tempList: tempList[4], listOfResults), mean0)
    statisticsText = dt_string
    statisticsText = statisticsText + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(1),simulationParameters.__getitem__(2),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
    statisticsText = statisticsText + "min:{}\nmax:{}\nmean:{}\nmedian:{}\nmode:{}\nstandard deviation:{}\nvariance:{}".format(min0,max0,mean0,median0,mode0,stdev0,variance0)
    resultFileTitle = "NoR={},attackRate={},startTime={}.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
    statisticsFileTitle = "NoR={},attackRate={},startTime={}_Statistics.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
    folderPath = "Results/{}/{}/{}/{}".format(simulationParameters.__getitem__(2),date,time,simulationParameters.__getitem__(1))
    return folderPath,resultFileTitle,resultText,statisticsFileTitle,statisticsText,(min0,max0,mean0,median0,mode0,stdev0,variance0)


def prepareDeleteResultsForWritingCase4(summaryOfTheResults, simulationParameters, now):
    newCaseInformation, listOfResults = summaryOfTheResults
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H.%M.%S")
    dt_string = now.strftime("Date: %B %d, %Y \nTime: %H:%M:%S\n\n\n\n")
    folderPath = "Results/{}/{}/{}".format(simulationParameters.__getitem__(2), date, time)
    CSVFileFolder = "Results/{}".format(simulationParameters.__getitem__(2))
    CSVFileTitle = "statistics.csv"
    CSVFileText = "Type of Attack,Scheduling Algorithm,Attack Rate,Attack Start Time,Collision Resolve Method,Collision Resolve Select Algorithm,Min,Max,Mean Of Collided Flows Percentage,Mean Of Distinct Collisions,Mean Of Collisions,Mean Of Dropped Flows,Median,Mode,Standard Deviation,Variance\n"

    fileTitle = "schedulingAlgorithm={},NoR={},attackRate={},startTime={},collisionResolveMethod={},collisionResolveSelectAlgorithm={}_overallSummary.txt".format(simulationParameters.__getitem__(1),simulationParameters.__getitem__(0), simulationParameters.__getitem__(3), simulationParameters.__getitem__(4),simulationParameters.__getitem__(5), simulationParameters.__getitem__(6))
    fileText = dt_string + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\ncollision resolve method --> {}\ncollision resolve select algorithm --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(
        simulationParameters.__getitem__(0), simulationParameters.__getitem__(1), simulationParameters.__getitem__(2),
        simulationParameters.__getitem__(5), simulationParameters.__getitem__(6), simulationParameters.__getitem__(3),
        simulationParameters.__getitem__(4))
    fileText = fileText + "===========================================================\n\n"
    fileText = fileText + "[#] scheduling_algorithm={}\n\t[*] attack_start_time={}:\n\t\t[+] attack_rate={}\n\t\t\t[-] resolve_method={}\n\n".format(listOfResults.__getitem__(0).__getitem__(0),listOfResults.__getitem__(0).__getitem__(1),listOfResults.__getitem__(0).__getitem__(2),listOfResults.__getitem__(0).__getitem__(3))
    for i in range(len(listOfResults)):

        CSVFileText = CSVFileText + "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
            simulationParameters.__getitem__(2), listOfResults.__getitem__(i).__getitem__(0),
            listOfResults.__getitem__(i).__getitem__(2), listOfResults.__getitem__(i).__getitem__(1),
            listOfResults.__getitem__(i).__getitem__(3), listOfResults.__getitem__(i).__getitem__(4),
            listOfResults.__getitem__(i).__getitem__(5), listOfResults.__getitem__(i).__getitem__(6),
            listOfResults.__getitem__(i).__getitem__(7), listOfResults.__getitem__(i).__getitem__(8),
            listOfResults.__getitem__(i).__getitem__(9), listOfResults.__getitem__(i).__getitem__(10),
            listOfResults.__getitem__(i).__getitem__(11), listOfResults.__getitem__(i).__getitem__(12),
            listOfResults.__getitem__(i).__getitem__(13), listOfResults.__getitem__(i).__getitem__(14))


        fileText = fileText + "\t\t\t\tresolve_select_algorithm={} --> min={} , max={} , meanOfCollidedFlowsPercentage={} , meanOfDistinctCollisions={} , meanOfCollisions={} , meanOfDroppedFlows={} , median={} , mode={} , standard_deviation={} , variance = {}\n".format(
            listOfResults.__getitem__(i).__getitem__(4), listOfResults.__getitem__(i).__getitem__(5),
            listOfResults.__getitem__(i).__getitem__(6), listOfResults.__getitem__(i).__getitem__(7),
            listOfResults.__getitem__(i).__getitem__(8), listOfResults.__getitem__(i).__getitem__(9),
            listOfResults.__getitem__(i).__getitem__(10), listOfResults.__getitem__(i).__getitem__(11),
            listOfResults.__getitem__(i).__getitem__(12), listOfResults.__getitem__(i).__getitem__(13),
            listOfResults.__getitem__(i).__getitem__(14))

        if (i < len(listOfResults) - 2):
            if (listOfResults.__getitem__(i).__getitem__(0) != listOfResults.__getitem__(i+1).__getitem__(0)):
                fileText = fileText + "\n\n===========================================================\n\n[#] scheduling_algorithm={}\n\t[*] attack_start_time={}:\n\t\t[+] attack_rate={}\n\t\t\t[-] resolve_method={}\n\n".format(
                    listOfResults.__getitem__(i+1).__getitem__(0), listOfResults.__getitem__(i+1).__getitem__(1),
                    listOfResults.__getitem__(i+1).__getitem__(2), listOfResults.__getitem__(i+1).__getitem__(3))


            elif(listOfResults.__getitem__(i).__getitem__(1) != listOfResults.__getitem__(i+1).__getitem__(1)):
                fileText = fileText + "\n\n----------------\n\n\t[*] attack_start_time={}:\n\t\t[+] attack_rate={}\n\t\t\t[-] resolve_method={}\n\n".format(listOfResults.__getitem__(i + 1).__getitem__(1),
                    listOfResults.__getitem__(i + 1).__getitem__(2), listOfResults.__getitem__(i + 1).__getitem__(3))

            elif(listOfResults.__getitem__(i).__getitem__(2) != listOfResults.__getitem__(i+1).__getitem__(2)):
                fileText = fileText + "\n\n\t\t[+] attack_rate={}\n\t\t\t[-] resolve_method={}\n\n".format(
                    listOfResults.__getitem__(i + 1).__getitem__(2), listOfResults.__getitem__(i + 1).__getitem__(3))
            elif(listOfResults.__getitem__(i).__getitem__(3) != listOfResults.__getitem__(i+1).__getitem__(3)):
                fileText = fileText + "\n\t\t\t[-] resolve_method={}\n\n".format(listOfResults.__getitem__(i + 1).__getitem__(3))

    fileText = fileText + "\n\n===========================================================\n\n"

    return folderPath, fileTitle, fileText, CSVFileFolder, CSVFileTitle, CSVFileText




def prepareDeleteResultsForWritingCase3(listOfResults,simulationParameters,now):
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H.%M.%S")
    dt_string = now.strftime("Date: %B %d, %Y \nTime: %H:%M:%S\n\n\n\n")
    folderPath = "Results/{}/{}/{}/{}".format(simulationParameters.__getitem__(2), date, time, simulationParameters.__getitem__(1))

    if (len(simulationParameters) > 5):
        fileTitle = "NoR={},attackRate={},startTime={},collisionResolveMethod={},collisionResolveSelectAlgorithm={}_Statistics.txt".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(3),simulationParameters.__getitem__(4), simulationParameters.__getitem__(5),simulationParameters.__getitem__(6))
        fileText = dt_string + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\ncollision resolve method --> {}\ncollision resolve select algorithm --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(1), simulationParameters.__getitem__(2), simulationParameters.__getitem__(5), simulationParameters.__getitem__(6), simulationParameters.__getitem__(3), simulationParameters.__getitem__(4))
        fileText = fileText + "===========================================================\n\n"
        fileText = fileText + "[+] attack_start_time={}:\n\n".format(listOfResults.__getitem__(0).__getitem__(0))
        for i in range(len(listOfResults.__getitem__(0))):
            fileText = fileText + "\tattack_rate={} --> min={} , max={} , meanOfCollidedFlowsPercentage={} , meanOfDistinctCollisions={} , meanOfCollisions={} , meanOfDroppedFlows={} , median={} , mode={} , standard_deviation={} , variance = {}\n".format(listOfResults.__getitem__(1).__getitem__(i), listOfResults.__getitem__(2).__getitem__(i),listOfResults.__getitem__(3).__getitem__(i), listOfResults.__getitem__(4).__getitem__(i),listOfResults.__getitem__(5).__getitem__(i), listOfResults.__getitem__(6).__getitem__(i),listOfResults.__getitem__(7).__getitem__(i), listOfResults.__getitem__(8).__getitem__(i), listOfResults.__getitem__(9).__getitem__(i), listOfResults.__getitem__(10).__getitem__(i), listOfResults.__getitem__(11).__getitem__(i))
            if (i < len(listOfResults.__getitem__(0)) - 2):
                if (listOfResults.__getitem__(0).__getitem__(i) < listOfResults.__getitem__(0).__getitem__(i + 1)):
                    fileText = fileText + "\n\n===========================================================\n\n[+] attack_start_time={}:\n\n".format(
                        listOfResults.__getitem__(0).__getitem__(i + 1))
        fileText = fileText + "\n\n===========================================================\n\n"

    else:
        fileTitle = "NoR={},attackRate={},startTime={}_Statistics.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
        fileText = dt_string + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n\n".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(1),simulationParameters.__getitem__(2), simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
        fileText = fileText + "===========================================================\n\n"
        fileText = fileText + "[+] attack_start_time={}:\n\n".format(listOfResults.__getitem__(0).__getitem__(0))
        for i in range(len(listOfResults.__getitem__(0))):
            fileText = fileText + "\tattack_rate={} --> min={} , max={} , meanOfCollidedFlowsPercentage={} , meanOfDistinctCollisions={} , meanOfCollisions={} , median={} , mode={} , standard_deviation={} , variance = {}\n".format(listOfResults.__getitem__(1).__getitem__(i), listOfResults.__getitem__(2).__getitem__(i),listOfResults.__getitem__(3).__getitem__(i), listOfResults.__getitem__(4).__getitem__(i),listOfResults.__getitem__(5).__getitem__(i), listOfResults.__getitem__(6).__getitem__(i),listOfResults.__getitem__(7).__getitem__(i), listOfResults.__getitem__(8).__getitem__(i), listOfResults.__getitem__(9).__getitem__(i), listOfResults.__getitem__(10).__getitem__(i))
            if (i < len(listOfResults.__getitem__(0)) - 2):
                if (listOfResults.__getitem__(0).__getitem__(i) < listOfResults.__getitem__(0).__getitem__(i + 1)):
                    fileText = fileText + "\n\n===========================================================\n\n[+] attack_start_time={}:\n\n".format(listOfResults.__getitem__(0).__getitem__(i + 1))
        fileText = fileText + "\n\n===========================================================\n\n"


    return folderPath, fileTitle, fileText

def prepareDeleteResultsForWritingCase2(listOfResults,simulationParameters,now):
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H.%M.%S")
    dt_string = now.strftime("Date: %B %d, %Y \nTime: %H:%M:%S\n\n\n\n")
    isAttackRate = (False if isinstance(simulationParameters.__getitem__(3), float) else True)
    preText = ("attack_rate" if isAttackRate else "attack_start_time")
    folderPath = "Results/{}/{}/{}/{}".format(simulationParameters.__getitem__(2), date, time, simulationParameters.__getitem__(1))
    if(len(simulationParameters)>5):
        fileTitle = "NoR={},attackRate={},startTime={},collisionResolveMethod={},collisionResolveSelectAlgorithm={}_Statistics.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4),simulationParameters.__getitem__(5),simulationParameters.__getitem__(6))
        fileText = dt_string + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\ncollision resolve method --> {}\ncollision resolve select algorithm --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(1), simulationParameters.__getitem__(2), simulationParameters.__getitem__(5), simulationParameters.__getitem__(6), simulationParameters.__getitem__(3), simulationParameters.__getitem__(4))
        for i in range(len(listOfResults.__getitem__(0))):
            fileText = fileText + "{}={} --> min={} , max={} , meanOfCollidedFlowsPercentage={} , meanOfDistinctCollisions={} , meanOfCollisions={} , meanOfDroppedFlows={} , median={} , mode={} , standard deviation={} , variance={}\n".format(preText, listOfResults.__getitem__(0).__getitem__(i), listOfResults.__getitem__(1).__getitem__(i),listOfResults.__getitem__(2).__getitem__(i), listOfResults.__getitem__(3).__getitem__(i),listOfResults.__getitem__(4).__getitem__(i), listOfResults.__getitem__(5).__getitem__(i),listOfResults.__getitem__(6).__getitem__(i), listOfResults.__getitem__(7).__getitem__(i), listOfResults.__getitem__(8).__getitem__(i), listOfResults.__getitem__(9).__getitem__(i), listOfResults.__getitem__(10).__getitem__(i))

    else:
        fileTitle = "NoR={},attackRate={},startTime={}_Statistics.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
        fileText = dt_string + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(1),simulationParameters.__getitem__(2), simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
        for i in range(len(listOfResults.__getitem__(0))):
            fileText = fileText + "{}={} --> min={} , max={} , meanOfCollidedFlowsPercentage={} , meanOfDistinctCollisions={} , meanOfCollisions={} , median={} , mode={} , standard deviation={} , variance={}\n".format(preText, listOfResults.__getitem__(0).__getitem__(i), listOfResults.__getitem__(1).__getitem__(i),listOfResults.__getitem__(2).__getitem__(i), listOfResults.__getitem__(3).__getitem__(i),listOfResults.__getitem__(4).__getitem__(i), listOfResults.__getitem__(5).__getitem__(i),listOfResults.__getitem__(6).__getitem__(i), listOfResults.__getitem__(7).__getitem__(i), listOfResults.__getitem__(8).__getitem__(i), listOfResults.__getitem__(9).__getitem__(i))




    return folderPath, fileTitle, fileText





def prepareDeleteResultsForWriting(listOfResults,simulationParameters,now):
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H.%M.%S")
    dt_string = now.strftime("Date: %B %d, %Y \nTime: %H:%M:%S\n\n\n\n")
    if(len(listOfResults.__getitem__(0))==8):
        resultText = collisionsPerFlowText = collisionsPerRunText = statisticsText = dt_string + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(1), simulationParameters.__getitem__(2),simulationParameters.__getitem__(3), simulationParameters.__getitem__(4))

        for i in range(len(listOfResults)):
            resultText = resultText + ">>> RUN NUMBER {} <<<\n\n".format(i + 1)
            resultText = resultText + "The total number of TSN flows: {}\n".format(listOfResults.__getitem__(i).__getitem__(0))
            resultText = resultText + "nb of total routed flows: {}\n".format(listOfResults.__getitem__(i).__getitem__(1))
            resultText = resultText + "nb of scheduled and (not) deleted flows using {}: {}\n".format(simulationParameters.__getitem__(1), listOfResults.__getitem__(i).__getitem__(2))
            resultText = resultText + "nb of the total scheduled flows using {}: {}\n".format(simulationParameters.__getitem__(1), listOfResults.__getitem__(i).__getitem__(3))
            resultText = resultText + "the total flows that cannot be seen by the scheduler: {}\n".format(listOfResults.__getitem__(i).__getitem__(4))
            resultText = resultText + "the percentage of flows that cannot be seen by the scheduler: {}%\n".format(round((listOfResults.__getitem__(i).__getitem__(4) / listOfResults.__getitem__(i).__getitem__(3))*100,2))
            resultText = resultText + "the total number of collided flows: {}\n".format(len(listOfResults.__getitem__(i).__getitem__(5)))
            resultText = resultText + "the percentage of collided flows: {}%\n".format(round((len(listOfResults.__getitem__(i).__getitem__(5)) / listOfResults.__getitem__(i).__getitem__(3))*100,2))
            resultText = resultText + "the total number of distinct collisions: {}\n".format(len(listOfResults.__getitem__(i).__getitem__(6)))
            resultText = resultText + "the total number of collisions: {}\n\n\n\n".format(listOfResults.__getitem__(i).__getitem__(7))

            collisionsPerFlowText = collisionsPerFlowText + ">>> RUN NUMBER {} <<<\n\n".format(i + 1)
            for listItem in listOfResults.__getitem__(i).__getitem__(5):
                currentFlow = listItem.__getitem__(0)
                collidedTSNFlows = listItem.__getitem__(3)
                collisionsLocations = listItem.__getitem__(4)
                collisionsPerFlowText = collisionsPerFlowText + "Flow number {} collided with {} other flows in {} egress ports as follow:\n".format(currentFlow.id,listItem.__getitem__(1),listItem.__getitem__(2))
                for index in range(len(collidedTSNFlows)):
                    collisionsPerFlowText = collisionsPerFlowText + "({}) It collides with TSN Flow number {} at egress port {}\n".format(index + 1,collidedTSNFlows.__getitem__(index).id,collisionsLocations.__getitem__(index))
                collisionsPerFlowText = collisionsPerFlowText + "----------------------------\n"
            collisionsPerFlowText = collisionsPerFlowText + "\n\n\n\n\n\n\n\n\n\n"

            collisionsPerRunText = collisionsPerRunText + ">>> RUN NUMBER {} <<<\n\n".format(i + 1)
            collisionsPerRunText = collisionsPerRunText + "There are {} distinct collisions between TSN Flows at {} egress ports in this run as follow:\n".format(len(listOfResults.__getitem__(i).__getitem__(6)), listOfResults.__getitem__(i).__getitem__(7))
            index = 0
            for collisionListItem in listOfResults.__getitem__(i).__getitem__(6):
                firstCollidedFlow = collisionListItem.__getitem__(0)
                secondCollidedFlow = collisionListItem.__getitem__(1)
                collisionsLocations = collisionListItem.__getitem__(2)
                index = index + 1
                collisionsPerRunText = collisionsPerRunText + "({}) TSN Flow number {} collides with TSN Flow number {} at these egress ports {}\n".format(index,firstCollidedFlow.id,secondCollidedFlow.id,collisionsLocations)
            collisionsPerRunText = collisionsPerRunText + "\n\n\n\n\n\n\n\n\n\n"


        min0 = round(min(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        max0 = round(max(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        mean0 = round(statistics.mean(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        mean1 = round(statistics.mean(map(lambda tempList: len(tempList[6]), listOfResults)),2)
        mean2 = round(statistics.mean(map(lambda tempList: tempList[7], listOfResults)),2)
        median0 = round(statistics.median(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        mode0 = round(statistics.mode(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        stdev0 = "NONE"
        variance0 = "NONE"
        if (simulationParameters.__getitem__(0) > 1):
            stdev0 = round(statistics.stdev(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults), mean0),2)
        if (simulationParameters.__getitem__(0) > 1):
            variance0 = round(statistics.variance(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults), mean0),2)
        statisticsText = statisticsText + "min:{}\nmax:{}\nmeanOfCollidedFlowsPercentage:{}\nmeanOfDistinctCollisions:{}\nmeanOfCollisions:{}\nmedian:{}\nmode:{}\nstandard deviation:{}\nvariance:{}".format(min0, max0, mean0, mean1, mean2, median0, mode0, stdev0, variance0)
        resultFileTitle = "NoR={},attackRate={},startTime={}.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
        collisionsPerFlowFileTitle = "NoR={},attackRate={},startTime={}_CollisionsPerFlow.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
        collisionsPerRunFileTitle = "NoR={},attackRate={},startTime={}_CollisionsPerRun.txt".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
        statisticsFileTitle = "NoR={},attackRate={},startTime={}_Statistics.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4))
        folderPath = "Results/{}/{}/{}/{}".format(simulationParameters.__getitem__(2), date, time,simulationParameters.__getitem__(1))
        return folderPath, resultFileTitle, resultText, collisionsPerFlowFileTitle, collisionsPerFlowText, collisionsPerRunFileTitle,collisionsPerRunText, statisticsFileTitle, statisticsText, (min0, max0, mean0, mean1, mean2, median0, mode0, stdev0, variance0)

    else:
        resultText = collisionsPerFlowText = collisionsPerRunText = droppedTSNFlowsText = statisticsText = dt_string + "#Simulation main parameters#\n--------------------------------------------------\n# of runs --> {}\nscheduling algorithm --> {}\ntype of attack --> {}\ncollision resolve method --> {}\ncollision resolve select algorithm --> {}\nattack rate --> {}\nattack start time --> {}\n--------------------------------------------------\n\n\n\n".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(1), simulationParameters.__getitem__(2), simulationParameters.__getitem__(5), simulationParameters.__getitem__(6), simulationParameters.__getitem__(3), simulationParameters.__getitem__(4))

        for i in range(len(listOfResults)):
            resultText = resultText + ">>> RUN NUMBER {} <<<\n\n".format(i + 1)
            resultText = resultText + "The total number of TSN flows: {}\n".format(listOfResults.__getitem__(i).__getitem__(0))
            resultText = resultText + "nb of total routed flows: {}\n".format(listOfResults.__getitem__(i).__getitem__(1))
            resultText = resultText + "nb of scheduled and (not) deleted flows using {}: {}\n".format(simulationParameters.__getitem__(1), listOfResults.__getitem__(i).__getitem__(2))
            resultText = resultText + "nb of the total scheduled flows using {}: {}\n".format(simulationParameters.__getitem__(1), listOfResults.__getitem__(i).__getitem__(3))
            resultText = resultText + "the total flows that cannot be seen by the scheduler: {}\n".format(listOfResults.__getitem__(i).__getitem__(4))
            resultText = resultText + "the percentage of flows that cannot be seen by the scheduler: {}%\n".format(round((listOfResults.__getitem__(i).__getitem__(4) / listOfResults.__getitem__(i).__getitem__(3))*100,2))
            resultText = resultText + "the total number of collided flows: {}\n".format(len(listOfResults.__getitem__(i).__getitem__(5)))
            resultText = resultText + "the percentage of collided flows: {}%\n".format(round((len(listOfResults.__getitem__(i).__getitem__(5)) / listOfResults.__getitem__(i).__getitem__(3))*100,2))
            resultText = resultText + "the total number of distinct collisions: {}\n".format(len(listOfResults.__getitem__(i).__getitem__(6)))
            resultText = resultText + "the total number of collisions: {}\n".format(listOfResults.__getitem__(i).__getitem__(7))
            resultText = resultText + "the total number of dropped flows: {}\n".format(len(listOfResults.__getitem__(i).__getitem__(8)))
            resultText = resultText + "the percentage of dropped flows: {}%\n\n\n\n".format(round((len(listOfResults.__getitem__(i).__getitem__(8)) / listOfResults.__getitem__(i).__getitem__(3))*100,2))

            collisionsPerFlowText = collisionsPerFlowText + ">>> RUN NUMBER {} <<<\n\n".format(i + 1)
            for listItem in listOfResults.__getitem__(i).__getitem__(5):
                currentFlow = listItem.__getitem__(0)
                collidedTSNFlows = listItem.__getitem__(3)
                collisionsLocations = listItem.__getitem__(4)
                collisionsPerFlowText = collisionsPerFlowText + "Flow number {} collided with {} other flows in {} egress ports as follow:\n".format(currentFlow.id,listItem.__getitem__(1),listItem.__getitem__(2))
                for index in range(len(collidedTSNFlows)):
                    collisionsPerFlowText = collisionsPerFlowText + "({}) It collides with TSN Flow number {} at egress port {}\n".format(index + 1,collidedTSNFlows.__getitem__(index).id,collisionsLocations.__getitem__(index))
                collisionsPerFlowText = collisionsPerFlowText + "----------------------------\n"
            collisionsPerFlowText = collisionsPerFlowText + "\n\n\n\n\n\n\n\n\n\n"

            collisionsPerRunText = collisionsPerRunText + ">>> RUN NUMBER {} <<<\n\n".format(i + 1)
            collisionsPerRunText = collisionsPerRunText + "There are {} distinct collisions between TSN Flows at {} egress ports in this run as follow:\n".format(len(listOfResults.__getitem__(i).__getitem__(6)), listOfResults.__getitem__(i).__getitem__(7))
            index = 0
            for collisionListItem in listOfResults.__getitem__(i).__getitem__(6):
                firstCollidedFlow = collisionListItem.__getitem__(0)
                secondCollidedFlow = collisionListItem.__getitem__(1)
                collisionsLocations = collisionListItem.__getitem__(2)
                index = index + 1
                collisionsPerRunText = collisionsPerRunText + "({}) TSN Flow number {} collides with TSN Flow number {} at these egress ports {}\n".format(index,firstCollidedFlow.id,secondCollidedFlow.id,collisionsLocations)
            collisionsPerRunText = collisionsPerRunText + "\n\n\n\n\n\n\n\n\n\n"

            droppedTSNFlowsText = droppedTSNFlowsText + ">>> RUN NUMBER {} <<<\n\n".format(i + 1)
            droppedTSNFlowsText = droppedTSNFlowsText + "-----------------------------------------------------------\n"
            droppedTSNFlowsText = droppedTSNFlowsText + "|    The list of dropped flows based on nb of collisions   |\n"
            droppedTSNFlowsText = droppedTSNFlowsText + "-----------------------------------------------------------\n\n"
            numberCounter = 1
            for e in listOfResults.__getitem__(i).__getitem__(8):
                droppedTSNFlowsText = droppedTSNFlowsText +"({}) flow number {}\n".format(numberCounter, e.id)
                numberCounter = numberCounter + 1
            droppedTSNFlowsText = droppedTSNFlowsText + "\n\n\n\n\n\n\n\n\n\n"


        min0 = round(min(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        max0 = round(max(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        mean0 = round(statistics.mean(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        mean1 = round(statistics.mean(map(lambda tempList: len(tempList[6]), listOfResults)),2)
        mean2 = round(statistics.mean(map(lambda tempList: tempList[7], listOfResults)),2)
        mean3 = round(statistics.mean(map(lambda tempList: ((len(tempList[8])/tempList[3])*100), listOfResults)),2)
        median0 = round(statistics.median(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        mode0 = round(statistics.mode(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults)),2)
        stdev0 = "NONE"
        variance0 = "NONE"
        if (simulationParameters.__getitem__(0) > 1):
            stdev0 = round(statistics.stdev(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults), mean0),2)
        if (simulationParameters.__getitem__(0) > 1):
            variance0 = round(statistics.variance(map(lambda tempList: ((len(tempList[5]) / tempList[3])*100), listOfResults), mean0),2)

        statisticsText = statisticsText + "min:{}\nmax:{}\nmeanOfCollidedFlowsPercentage:{}\nmeanOfDistinctCollisions:{}\nmeanOfCollisions:{}\nmeanOfDroppedFlows:{}\nmedian:{}\nmode:{}\nstandard deviation:{}\nvariance:{}".format(min0, max0, mean0, mean1, mean2, mean3, median0, mode0, stdev0, variance0)
        resultFileTitle = "NoR={},attackRate={},startTime={},collisionResolveMethod={},collisionResolveSelectAlgorithm={}.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4),simulationParameters.__getitem__(5),simulationParameters.__getitem__(6))
        collisionsPerFlowFileTitle = "NoR={},attackRate={},startTime={},collisionResolveMethod={},collisionResolveSelectAlgorithm={}_CollisionsPerFlow.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4),simulationParameters.__getitem__(5),simulationParameters.__getitem__(6))
        collisionsPerRunFileTitle = "NoR={},attackRate={},startTime={},collisionResolveMethod={},collisionResolveSelectAlgorithm={}_CollisionsPerRun.txt".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(3),simulationParameters.__getitem__(4),simulationParameters.__getitem__(5),simulationParameters.__getitem__(6))
        droppedTSNFlowsFileTitle = "NoR={},attackRate={},startTime={},collisionResolveMethod={},collisionResolveSelectAlgorithm={}_DroppedTSNFlows.txt".format(simulationParameters.__getitem__(0), simulationParameters.__getitem__(3),simulationParameters.__getitem__(4),simulationParameters.__getitem__(5),simulationParameters.__getitem__(6))
        statisticsFileTitle = "NoR={},attackRate={},startTime={},collisionResolveMethod={},collisionResolveSelectAlgorithm={}_Statistics.txt".format(simulationParameters.__getitem__(0),simulationParameters.__getitem__(3),simulationParameters.__getitem__(4),simulationParameters.__getitem__(5),simulationParameters.__getitem__(6))
        folderPath = "Results/{}/{}/{}/{}".format(simulationParameters.__getitem__(2), date, time,simulationParameters.__getitem__(1))
        return folderPath, resultFileTitle, resultText, collisionsPerFlowFileTitle, collisionsPerFlowText, collisionsPerRunFileTitle,collisionsPerRunText, droppedTSNFlowsFileTitle, droppedTSNFlowsText, statisticsFileTitle, statisticsText, (min0, max0, mean0, mean1, mean2, mean3, median0, mode0, stdev0, variance0)

