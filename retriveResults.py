import os
from os import path

def findLatestResults(typeOfSecurityAttack):
    allFiles = allResults()
    allAttackFiles = []
    for file in allFiles:
        if(file.__getitem__(0)==typeOfSecurityAttack):
            allAttackFiles.append(file)
    if(len(allAttackFiles)==0):
        errorMessage = 'There is no result to display in {} (you have to run the simulator at least once and make typeOfSecurityAttack = {} to get results)'.format(typeOfSecurityAttack,typeOfSecurityAttack)
        raise ValueError(errorMessage)
    else:
        sortedAttackFiles = sorted(allAttackFiles, key=lambda x: (x.__getitem__(1), x.__getitem__(2)), reverse=True)
        lastDate = sortedAttackFiles.__getitem__(0).__getitem__(1)
        lastTime = sortedAttackFiles.__getitem__(0).__getitem__(2)
        tempIndex = 0
        returnedList = []
        while(sortedAttackFiles.__getitem__(tempIndex).__getitem__(1) == lastDate and sortedAttackFiles.__getitem__(tempIndex).__getitem__(2) == lastTime):
            directoryPath = sortedAttackFiles.__getitem__(tempIndex).__getitem__(4)
            listOfFiles = sortedAttackFiles.__getitem__(tempIndex).__getitem__(5)
            fileContents = []
            for tempFile in sortedAttackFiles.__getitem__(tempIndex).__getitem__(5):
                f = open("{}/{}".format(sortedAttackFiles.__getitem__(tempIndex).__getitem__(4), tempFile), "r")
                content = f.read()
                f.close()
                fileContents.append(content)
            returnedList.append((directoryPath,listOfFiles,fileContents))
            tempIndex = tempIndex + 1
            if(tempIndex == len(sortedAttackFiles)):
                break


        return returnedList


def allResults():
    listOfFiles = [] #it will return all the files in folder Results that contains text. The resulted list will be in the form (attackFolder,dateFolder,timeFolder,pathToFiles,listOfNonEmptyFiles)
    if (path.exists('Results')):
        childrenOfResults = [f.name for f in os.scandir('Results') if f.is_dir()]
        for attackFolder in childrenOfResults:
            childrenOfAttackType = [f.name for f in os.scandir('Results/{}'.format(attackFolder)) if f.is_dir()]
            for dateFolder in childrenOfAttackType:
                childrenOfDateFolder = [f.name for f in os.scandir('Results/{}/{}'.format(attackFolder, dateFolder)) if f.is_dir()]
                for timeFolder in childrenOfDateFolder:
                    childrenOfTimeFolder = [f.name for f in os.scandir('Results/{}/{}/{}'.format(attackFolder, dateFolder,timeFolder))if f.is_dir()]
                    for schedulingAlgorihtmFolder in childrenOfTimeFolder:
                        pathToFiles = 'Results/{}/{}/{}/{}'.format(attackFolder, dateFolder,timeFolder,schedulingAlgorihtmFolder)
                        filesOfTimeFolder = [f.name for f in os.scandir(pathToFiles) if f.is_file() and os.stat('{}/{}'.format(pathToFiles, f.name)).st_size != 0]
                        if (len(filesOfTimeFolder) != 0):
                            listOfFiles.append((attackFolder,dateFolder,timeFolder, schedulingAlgorihtmFolder, pathToFiles,filesOfTimeFolder))

    if(len(listOfFiles) == 0):
        errorMessage = 'There is no result to display (you have to run the simulator at least once to get results)'
        raise ValueError(errorMessage)
    else:
        return listOfFiles