'''
Created on Apr 15, 2016

@author: sharvani
'''

import constants

class UtilityNode(object):
    def __init__(self):
        name = constants.NULL_STRING
        dependencyNodes = []
        utilityValueTable = {}
        
    def setName(self, name):
        self.name = name
        
    def setDependencyNodes(self, dependencyNodes):
        self.dependencyNodes = dependencyNodes
    
    def setUtilityValueTable(self, utilityValueTable):
        self.utilityValueTable = utilityValueTable
        
    def getName(self):
        return self.name
    
    def getDependencyNodes(self):
        return self.dependencyNodes
    
    def getUtilityValueTable(self):
        return self.utilityValueTable