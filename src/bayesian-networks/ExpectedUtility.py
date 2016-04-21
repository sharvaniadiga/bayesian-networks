'''
Created on Apr 17, 2016

@author: sharvani
'''

class ExpectedUtility(object):
    def __init__(self):
        expectedUtilityValue = 0
        dependencyNodesValueDict = {}
        
    def addDependencyNodesDictValue(self, dict):
        self.dependencyNodesValueDict = dict
    
    def setUtilityValue(self, utilityValue):
        self.expectedUtilityValue = utilityValue
        
    def getDependencyNodesDict(self):
        return self.dependencyNodesValueDict
    
    def getUtilityValue(self):
        return self.expectedUtilityValue
    