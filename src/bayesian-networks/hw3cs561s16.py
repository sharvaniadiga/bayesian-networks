'''
Created on Apr 11, 2016

@author: sharvani
'''
import sys

import constants
import BayesnetNode
import UtilityNode
import ExpectedUtility
import math
from decimal import Decimal, ROUND_UP

def empty(bayesNetVars):
    if(len(bayesNetVars) == 0):
        return True
    else:
        return False

def first(bayesNetVars):
    return bayesNetVars[0] #TODO: include this in constants
    
def rest(bayesNetVars):
    return bayesNetVars[1:]

def getProbablityFromCondTable(bayesNetVar, e):
    probOfFirstVarGivenParents = 1.0
    conditionalProbTable = bayesNetVar.getConditionalProbTable()
    parents = bayesNetVar.getParents()
    if(len(parents) == 0):
        probOfFirstVarGivenParents = conditionalProbTable[constants.NO_PARENT]
    elif(len(parents) == 1):
        probOfFirstVarGivenParents = conditionalProbTable[e[parents[0]]]
    elif(len(parents) == 2):
        probOfFirstVarGivenParents = conditionalProbTable[e[parents[0]]][e[parents[1]]]
    elif(len(parents) == 3):    
        probOfFirstVarGivenParents = conditionalProbTable[e[parents[0]]][e[parents[1]]][e[parents[2]]]
    if(e[bayesNetVar.getName()] == constants.PLUS):
        return float(probOfFirstVarGivenParents)
    else:
        return (1 - float(probOfFirstVarGivenParents))

def isParentDecisionNodeAndValueNotSet(parent, nodeValueDict):
    if((parent in decisionNodes) and (nodeValueDict.has_key(parent) == False)):
        return True
    else:
        return False

def enumerateAll(bayesNetVars, e):
    if(empty(bayesNetVars)):
        return 1.0
    firstVar = first(bayesNetVars)
    for parent in firstVar.getParents():
        if(isParentDecisionNodeAndValueNotSet(parent, e)):
            return enumerateAll(rest(bayesNetVars), e)
    if((e.has_key(firstVar.getName())) and (e[firstVar.getName()] != constants.NULL_STRING)):
        probOfFirstVarGivenParents = getProbablityFromCondTable(firstVar, e)
        return (probOfFirstVarGivenParents * enumerateAll(rest(bayesNetVars), e))
    else:
        sum = 0
        firstVarDict = {}
        for firstVarValue in [constants.PLUS,constants.MINUS]:
            firstVarDict[firstVar.getName()] = firstVarValue
            eDash = dict(e.items() + firstVarDict.items())
            sum = sum + (getProbablityFromCondTable(firstVar, eDash) * enumerateAll(rest(bayesNetVars), eDash))
        return sum 

def enumerationAsk(X, e, bayesNetVars):
    #TODO: check x related things
    val = enumerateAll(bayesNetVars, dict(e.items() + X.items()))
    return val

def addVariableAndValueToDictAndUpdateIndex(args, index):
    dict = {}
    key = args[index]
    index = index + 1
    value = constants.NULL_STRING
    if ((index < len(args)) and (args[index] == "=")):
        index = index + 1
        value = args[index]
        index = index + 1
    dict[key] = value
    return dict, index

def getTableFromFileLines(lines, lineNo, numOfParents):
    table = {}
    for i in range(0,int(math.pow(constants.NUM_OF_VALUES_PER_VARIABLE, numOfParents))): 
        tableEntry = lines[lineNo].split(constants.SPACE)
        if(numOfParents == 0):
            table[constants.NO_PARENT] = tableEntry[constants.CONDITIONAL_PROBABILITY_VALUE_INDEX]
        elif(numOfParents == 1):
            table[tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]] = tableEntry[constants.CONDITIONAL_PROBABILITY_VALUE_INDEX]
        elif(numOfParents == 2):
            if(table.has_key(tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]) == False):
                table[tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]] = {}
            table[tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]][tableEntry[constants.CONDITIONAL_PROBABILITY_SECOND_PARENT_VALUE_INDEX]] = tableEntry[constants.CONDITIONAL_PROBABILITY_VALUE_INDEX]
        elif(numOfParents == 3): #TODO : verify this 
            if(table.has_key(tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]) == False):
                table[tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]] = {}
            if(table[tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]].has_key(tableEntry[constants.CONDITIONAL_PROBABILITY_SECOND_PARENT_VALUE_INDEX]) == False):
                table[tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]][tableEntry[constants.CONDITIONAL_PROBABILITY_SECOND_PARENT_VALUE_INDEX]] = {}
            table[tableEntry[constants.CONDITIONAL_PROBABILITY_FIRST_PARENT_VALUE_INDEX]][tableEntry[constants.CONDITIONAL_PROBABILITY_SECOND_PARENT_VALUE_INDEX]][tableEntry[constants.CONDITIONAL_PROBABILITY_THIRD_PARENT_VALUE_INDEX]] = tableEntry[constants.CONDITIONAL_PROBABILITY_VALUE_INDEX]
        lineNo = lineNo + 1
    return table

def printStringOntoFile(str1):
    fileName = constants.OUTPUT_TXT
    outputFile = open(fileName, 'a')
    outputFile.write(str1)
    outputFile.write("\n")
    outputFile.close()

def getLHSorRHSofCondProbability(argsAfterSplit, index, condition):
    varValDict = {}
    if ((condition == constants.BEFORE) and (constants.CONDITIONAL_PROBABILITY_SYMBOL in argsAfterSplit)):
        while(index < argsAfterSplit.index(constants.CONDITIONAL_PROBABILITY_SYMBOL)):
            newVarDict = {}
            if(argsAfterSplit[index] == constants.QUERY_SEPERATOR):
                index = index + 1
            newVarDict, index = addVariableAndValueToDictAndUpdateIndex(argsAfterSplit, index)
            varValDict = dict(varValDict.items() + newVarDict.items())
    elif (condition == constants.AFTER):
        while(index < len(argsAfterSplit)):
            newVarDict = {}
            if(argsAfterSplit[index] == constants.QUERY_SEPERATOR):
                index = index + 1
            newVarDict, index = addVariableAndValueToDictAndUpdateIndex(argsAfterSplit, index)
            varValDict = dict(varValDict.items() + newVarDict.items())
    return varValDict, index

def getQueryVariableValueDict(argsAfterSplit):
    numeratorX = {}
    denominatorX = {}
    k = 0
    if constants.CONDITIONAL_PROBABILITY_SYMBOL in argsAfterSplit:
        lhsDict, k = getLHSorRHSofCondProbability(argsAfterSplit, k, constants.BEFORE)
        if(k == argsAfterSplit.index(constants.CONDITIONAL_PROBABILITY_SYMBOL)):
            k = k + 1
        rhsDict, k = getLHSorRHSofCondProbability(argsAfterSplit, k, constants.AFTER)
        numeratorX = dict(lhsDict.items() + rhsDict.items())
        denominatorX = dict(rhsDict.items())
    else:
        numeratorX, k = getLHSorRHSofCondProbability(argsAfterSplit, k, constants.AFTER)
    return numeratorX, denominatorX
    
def calculateProbability(numeratorX, denominatorX):
    e = {} #TODO : change variable name
    val = 1.0 #TODO : change 
    if(len(denominatorX) == 0):
        val = enumerationAsk(numeratorX, e, list(bayesNetVars))
    else:
        val = enumerationAsk(numeratorX, e, list(bayesNetVars)) / enumerationAsk(denominatorX, e, list(bayesNetVars))
    return val

def getUtility(utilityNode, X):
    utilityTable = utilityNode.getUtilityValueTable()
    dependencyNodes = utilityNode.getDependencyNodes()
    if (len(dependencyNodes) == 1):
        return utilityTable[X[dependencyNodes[0]]]
    elif (len(dependencyNodes) == 2):
        return utilityTable[X[dependencyNodes[0]]][X[dependencyNodes[1]]]
    elif (len(dependencyNodes) == 3):
        return utilityTable[X[dependencyNodes[0]]][X[dependencyNodes[1]]][X[dependencyNodes[2]]]

def calculateExpectedUtility(numeratorX, denominatorX, utilityDependencyNodes, utilityNode):
    if(len(utilityDependencyNodes) == 0):
        utility = getUtility(utilityNode, numeratorX)
        return float(calculateProbability(numeratorX, denominatorX)) * int(utility)
    expectedUtility = 0
    if(numeratorX.has_key(utilityDependencyNodes[0])):
        expectedUtility += calculateExpectedUtility(numeratorX, denominatorX, utilityDependencyNodes[1:], utilityNode)
    else:
        varValDict = {}
        for nodeValue in (constants.PLUS, constants.MINUS):
            varValDict[utilityDependencyNodes[0]] = nodeValue
            numeratorX = dict(numeratorX.items() + varValDict.items())
            expectedUtility += calculateExpectedUtility(numeratorX, denominatorX, utilityDependencyNodes[1:], utilityNode)
    return expectedUtility
    
def getExpectedUtilityForAllDecisionNodeCombinations(queryDecisionNode,numeratorX, denominatorX, utilityNode, decisionNodeValueDict, expectedUtilityArray):
    if(len(queryDecisionNode) == 0):
        expectedUtility = calculateExpectedUtility(numeratorX, denominatorX, utilityNode.getDependencyNodes(), utilityNode)
        expectedUtilityObject = ExpectedUtility.ExpectedUtility()
        expectedUtilityObject.setUtilityValue(expectedUtility)
        expectedUtilityObject.addDependencyNodesDictValue(dict(decisionNodeValueDict))
        expectedUtilityArray.append(expectedUtilityObject)
        return expectedUtilityArray
    varValDict = {}
    if(numeratorX.has_key(queryDecisionNode[0])):
        #decisionNodeValueDict[queryDecisionNode[0]] = numeratorX[queryDecisionNode[0]]
        expectedUtilityArray = getExpectedUtilityForAllDecisionNodeCombinations(queryDecisionNode[1:],numeratorX, denominatorX, utilityNode, decisionNodeValueDict, expectedUtilityArray)
        #decisionNodeValueDict.pop(queryDecisionNode[0])
    else:
        for nodeValue in (constants.PLUS, constants.MINUS):
            decisionNodeValueDict[queryDecisionNode[0]] = nodeValue
            varValDict[queryDecisionNode[0]] = nodeValue
            numeratorX = dict(numeratorX.items() + varValDict.items())
            expectedUtilityArray = getExpectedUtilityForAllDecisionNodeCombinations(queryDecisionNode[1:],numeratorX, denominatorX, utilityNode, decisionNodeValueDict, expectedUtilityArray)
            decisionNodeValueDict.pop(queryDecisionNode[0])
    return expectedUtilityArray

def getMaxUtility(argsAfterSplit, utilityNode):
    k = 0
    lhsDict, k = getLHSorRHSofCondProbability(argsAfterSplit, k, constants.BEFORE)
    if((constants.CONDITIONAL_PROBABILITY_SYMBOL in argsAfterSplit) and (k == argsAfterSplit.index(constants.CONDITIONAL_PROBABILITY_SYMBOL))):
        k = k + 1
    rhsDict, k = getLHSorRHSofCondProbability(argsAfterSplit, k, constants.AFTER)
    queryDecisionNode = []
    queryPresetCondition = {}
    queryDecisionNode, queryPresetCondition = setDecisionNodeAndPresetConditionInQuery(queryDecisionNode, queryPresetCondition, lhsDict)
    queryDecisionNode, queryPresetCondition = setDecisionNodeAndPresetConditionInQuery(queryDecisionNode, queryPresetCondition, rhsDict)
    expectedUtilityArray = getExpectedUtilityForAllDecisionNodeCombinations(decisionNodes,queryPresetCondition, queryPresetCondition, utilityNode, {}, [])
    maxExpectedUtilityObject = expectedUtilityArray[0]
    for i in range(1, len(expectedUtilityArray)):
        if(maxExpectedUtilityObject.getUtilityValue() < expectedUtilityArray[i].getUtilityValue()):
            maxExpectedUtilityObject = expectedUtilityArray[i]
    maxExpectedUtilityPrintString = constants.NULL_STRING
    queryArray = []
    j = 0
    for i in range(0, len(argsAfterSplit)):
        if (argsAfterSplit[i] == constants.CONDITIONAL_PROBABILITY_SYMBOL):
            break
        queryArray.append(argsAfterSplit[i])
    for arg in queryArray:
        if (maxExpectedUtilityObject.getDependencyNodesDict().has_key(arg)):
            maxExpectedUtilityPrintString += maxExpectedUtilityObject.getDependencyNodesDict()[arg] + constants.SPACE
    maxExpectedUtilityPrintString += "{0:g}".format(round(maxExpectedUtilityObject.getUtilityValue() + 1e-8))
    return maxExpectedUtilityPrintString

def setDecisionNodeAndPresetConditionInQuery(queryDecisionNode, queryPresetCondition, dict):
    for key in dict:
        if ((key in decisionNodes) and (dict[key] == constants.NULL_STRING)):
            queryDecisionNode.append(key)
        else:
            queryPresetCondition[key] = dict[key]
    return queryDecisionNode, queryPresetCondition

def getQueryType(query):
    if query.startswith(constants.PROBABILITY):
        return constants.PROBABILITY
    elif query.startswith(constants.MAX_EXPECTED_UTILITY):
        return constants.MAX_EXPECTED_UTILITY
    elif query.startswith(constants.EXPECTED_UTILITY):
        return constants.EXPECTED_UTILITY
    
#main
with open(sys.argv[2]) as f:
    lines = f.read().splitlines()
    f.close()
queries = []
currentLineNo = 0
while (lines[currentLineNo] != constants.INPUT_FILE_QUERY_END_BAYESNET_BEGIN):
    queries.append(lines[currentLineNo])
    currentLineNo = currentLineNo + 1   
bayesNetVars = []
decisionNodes = []
utilityNode = UtilityNode.UtilityNode()
currentLineNo = currentLineNo + 1
while ( currentLineNo < len(lines)):
    words = lines[currentLineNo].split(constants.SPACE)
    name = words[0] # TODO : update in constants
    if(constants.UTILITY in lines[currentLineNo]):
        utilityNode.setName(name)
        numOfDependencyNodes = 0
        dependencyNodes = []
        if(constants.CONDITIONAL_PROBABILITY_SYMBOL in words):
            for i in range(2,len(words)): # TODO : update in constants
                dependencyNodes.append(words[i])
                numOfDependencyNodes = numOfDependencyNodes + 1
        utilityNode.setDependencyNodes(dependencyNodes)     
        currentLineNo = currentLineNo + 1
        utilityValueTable = getTableFromFileLines(lines, currentLineNo, numOfDependencyNodes)
        utilityNode.setUtilityValueTable(utilityValueTable)
        currentLineNo = currentLineNo + int(math.pow(constants.NUM_OF_VALUES_PER_VARIABLE, numOfDependencyNodes))
    elif((currentLineNo + 1 < len(lines)) and (lines[currentLineNo + 1] != constants.DECISION)):
        bayesnetNode = BayesnetNode.BayesnetNode()
        bayesnetNode.setName(name)
        numOfParents = 0
        parents = []
        if(constants.CONDITIONAL_PROBABILITY_SYMBOL in words):
            for i in range(2,len(words)): # TODO : update in constants
                parents.append(words[i])
                numOfParents = numOfParents + 1
        bayesnetNode.setParents(parents)     
        currentLineNo = currentLineNo + 1
        conditionalProbTable = getTableFromFileLines(lines, currentLineNo, numOfParents)
        bayesnetNode.setConditionalProbTable(conditionalProbTable)
        bayesNetVars.append(bayesnetNode)
        currentLineNo = currentLineNo + int(math.pow(constants.NUM_OF_VALUES_PER_VARIABLE, numOfParents))
    else:
        decisionNodes.append(name)
        currentLineNo = currentLineNo + 2
    if((currentLineNo + 1 < len(lines)) and ((lines[currentLineNo] == constants.INPUT_FILE_END_OF_PROB_TABLE) or (lines[currentLineNo] == constants.INPUT_FILE_QUERY_END_BAYESNET_BEGIN))):
        currentLineNo = currentLineNo + 1
for i in range(0,len(queries)):
    try:
        args = queries[i][queries[i].find(constants.OPEN_BRACKET) + 1:queries[i].find(constants.CLOSE_BRACKET)]
        args = args.replace(",", constants.NULL_STRING)
        argsAfterSplit = args.split(constants.SPACE)
        if (getQueryType(queries[i]) == constants.PROBABILITY):
            numeratorX, denominatorX = getQueryVariableValueDict(argsAfterSplit)
            probabilityValue = calculateProbability(numeratorX, denominatorX)
            print "{0:.2f}".format(round(probabilityValue + 1e-8, 2))
            #printStringOntoFile("{0:.2f}".format(round(probabilityValue + 1e-8, 2)))
        elif (getQueryType(queries[i]) == constants.MAX_EXPECTED_UTILITY):
            maxExpectedUtility = getMaxUtility(argsAfterSplit, utilityNode)
            print maxExpectedUtility
            #printStringOntoFile(maxExpectedUtility)
        elif (getQueryType(queries[i]) == constants.EXPECTED_UTILITY):
            k = 0
            lhsDict, k = getLHSorRHSofCondProbability(argsAfterSplit, k, constants.BEFORE)
            if((constants.CONDITIONAL_PROBABILITY_SYMBOL in argsAfterSplit) and (k == argsAfterSplit.index(constants.CONDITIONAL_PROBABILITY_SYMBOL))):
                k = k + 1
            rhsDict, k = getLHSorRHSofCondProbability(argsAfterSplit, k, constants.AFTER)
            X = dict(lhsDict.items() + rhsDict.items())
            expectedUtility = calculateExpectedUtility(X, rhsDict, utilityNode.getDependencyNodes(), utilityNode)
            expectedUtilityStr = "{0:g}".format(round(expectedUtility + 1e-8))
            print expectedUtilityStr
            #printStringOntoFile(expectedUtilityStr)
    except:
        print "\n"
        #printStringOntoFile("\n")
        continue
