'''
Created on Apr 11, 2016

@author: sharvani
'''

import constants

class BayesnetNode(object):
    def __init__(self):
        name = constants.NULL_STRING
        parents = []
        conditionalProbTable = {}
        
    def setName(self, name):
        self.name = name
        
    def setParents(self, parents):
        self.parents = parents
    
    def setConditionalProbTable(self, conditionalProbTable):
        self.conditionalProbTable = conditionalProbTable
        
    def getName(self):
        return self.name
    
    def getParents(self):
        return self.parents
    
    def getConditionalProbTable(self):
        return self.conditionalProbTable