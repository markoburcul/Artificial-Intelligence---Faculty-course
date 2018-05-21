
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from logic import *
import copy



class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def miniWumpusSearch(problem): 
    """
    A sample pass through the miniWumpus layout. Your solution will not contain 
    just three steps! Optimality is not the concern here.
    """
    from game import Directions
    e = Directions.EAST 
    n = Directions.NORTH
    return  [e, n, n]


def logicBasedSearch(problem):
    """

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    print "Does the Wumpus's stench reach my spot?", 
               \ problem.isWumpusClose(problem.getStartState())

    print "Can I sense the chemicals from the pills?", 
               \ problem.isPoisonCapsuleClose(problem.getStartState())

    print "Can I see the glow from the teleporter?", 
               \ problem.isTeleporterClose(problem.getStartState())
    
    (the slash '\\' is used to combine commands spanning through multiple lines - 
    you should remove it if you convert the commands to a single line)
    
    Feel free to create and use as many helper functions as you want.

    A couple of hints: 
        * Use the getSuccessors method, not only when you are looking for states 
        you can transition into. In case you want to resolve if a poisoned pill is 
        at a certain state, it might be easy to check if you can sense the chemicals 
        on all cells surrounding the state. 
        * Memorize information, often and thoroughly. Dictionaries are your friends and 
        states (tuples) can be used as keys.
        * Keep track of the states you visit in order. You do NOT need to remember the
        tranisitions - simply pass the visited states to the 'reconstructPath' method 
        in the search problem. Check logicAgents.py and search.py for implementation.
    """
    # array in order to keep the ordering
    visitedStates = []
    currentState = problem.getStartState()
    visitedStates.append(currentState)
    knowledge = set()                       #knowledge about all states
    safeStates = util.PriorityQueueWithFunction(lambda x: stateWeight(x))
    undefinedStates = util.PriorityQueueWithFunction(lambda x: stateWeight(x))
    teleporter = []
    wumpus = []



    while(True):
        print "Visiting: "+str(currentState)

        if problem.isGoalState(currentState):
            return problem.reconstructPath(visitedStates)

        updateKnowledge(knowledge, visitedStates, currentState, problem, safeStates, undefinedStates, teleporter, wumpus)

        if teleporter.__len__() != 0:
            currentState = teleporter.pop()
            visitedStates.append(currentState)
            continue

        elif not safeStates.isEmpty() :
            currentState = safeStates.pop()
            visitedStates.append(currentState)
            continue

        elif not undefinedStates.isEmpty():
            currentState = undefinedStates.pop()
            visitedStates.append(currentState)
            continue



# Abbreviations
lbs = logicBasedSearch


def updateKnowledge(knowledge, visitedStates, currentState, problem, safeStates,undefinedStates, teleporter, wumpus):
    #get rules for current state
    currentStateRules = getRules(currentState, problem.getSuccessors(currentState))

    #get info from sensing on current state
    sensingCurrentState(currentState, knowledge, problem)

    knowledge = removeRedundantKnowledge(knowledge)

    for i in problem.getSuccessors(currentState):
        rules = getRules(i[0], problem.getSuccessors(i[0])).union(currentStateRules)

        clause = Clause([Literal(Labels.WUMPUS, i[0], False)])
        if not knowledge.__contains__(clause):
            if wumpus.__len__() == 0 and problem.isWumpusClose(currentState):
                    if resolution(knowledge.union(rules),clause):  #if Wumpus is on neighbour state
                        print "Concluded: " + Labels.WUMPUS+str(i[0])
                        knowledge.add(clause)
                        wumpus.append(i[0])
                        continue

        clause = Clause([Literal(Labels.WUMPUS, i[0], True)])
        if not knowledge.__contains__(clause):
            if resolution(knowledge.union(rules), clause):   #if Wumpus isn't on neighbour state
                print "Concluded: ~" + Labels.WUMPUS + str(i[0])
                knowledge.add(clause)


        clause = Clause([Literal(Labels.POISON, i[0], False)])
        if not knowledge.__contains__(clause):
            if problem.isPoisonCapsuleClose(currentState):
                if resolution(knowledge.union(rules), clause):  #if poison is on neighbour state
                    print "Concluded: " + Labels.POISON + str(i[0])
                    knowledge.add(clause)
                    continue

        clause = Clause([Literal(Labels.POISON, i[0], True)])
        if not knowledge.__contains__(clause):
            if resolution(knowledge.union(rules), clause):   #if poison isn't on neighbour state
                knowledge.add(clause)
                print "Concluded: ~" + Labels.POISON + str(i[0])

        clause = Clause([Literal(Labels.TELEPORTER, i[0], False)])
        if not knowledge.__contains__(clause):
            if teleporter.__len__() == 0 and problem.isTeleporterClose(currentState):
                if resolution(knowledge.union(rules), clause):  #if teleporter is on neighbour state
                    print "Concluded: " + Labels.TELEPORTER + str(i[0])
                    knowledge.add(clause)
                    teleporter.append(i[0])
                    return

        clause = Clause([Literal(Labels.TELEPORTER, i[0], True)])
        if not knowledge.__contains__(clause):
            if resolution(knowledge.union(rules), clause):   #if teleporter isn't on neighbour state
                knowledge.add(clause)
                print "Concluded: ~" + Labels.TELEPORTER + str(i[0])


        clause = Clause([Literal(Labels.SAFE, i[0], False)])
        if not knowledge.__contains__(clause):
            if resolution(knowledge.union(rules), clause):   #if neighbour state is safe
                print "Concluded: " + Labels.SAFE + str(i[0])
                knowledge.add(clause)
                if not visitedStates.__contains__(i[0]):
                    safeStates.push(i[0])
                continue

        clause = Clause([Literal(Labels.SAFE, i[0], True)])
        if not knowledge.__contains__(clause):
            if resolution(knowledge.union(rules), clause):    #if neighbour state isn't safe
                knowledge.add(clause)
                print "Concluded: ~" + Labels.SAFE + str(i[0])
                continue

        #if nothing of above and state hasn't been visited
        undefinedStates.push(i[0])


def sensingCurrentState(currentState, knowledge, problem):

    if problem.isWumpusClose(currentState):
        print "Sensed: " + Labels.WUMPUS_STENCH + str(currentState)
        knowledge.add(Clause([Literal(Labels.WUMPUS_STENCH, currentState, False)]))
    else:
        print "Sensed: ~" + Labels.WUMPUS_STENCH + str(currentState)
        knowledge.add(Clause([Literal(Labels.WUMPUS_STENCH, currentState, True)]))

    if problem.isPoisonCapsuleClose(currentState):
        print "Sensed: " + Labels.POISON_FUMES + str(currentState)
        knowledge.add(Clause([Literal(Labels.POISON_FUMES, currentState, False)]))
    else:
        print "Sensed: ~" + Labels.POISON_FUMES + str(currentState)
        knowledge.add(Clause([Literal(Labels.POISON_FUMES, currentState, True)]))

    if problem.isTeleporterClose(currentState):
        print "Sensed: " + Labels.TELEPORTER_GLOW + str(currentState)
        knowledge.add(Clause([Literal(Labels.TELEPORTER_GLOW, currentState, False)]))
    else:
        knowledge.add(Clause([Literal(Labels.TELEPORTER_GLOW, currentState, True)]))
        print "Sensed: ~" + Labels.TELEPORTER_GLOW + str(currentState)

    if not problem.isWumpusClose(currentState) and not problem.isPoisonCapsuleClose(currentState):
        knowledge.add(Clause([Literal(Labels.SAFE, currentState, False)]))
        "Concluded: " + Labels.SAFE + str(currentState)

def removeRedundantKnowledge(knowledge):
    newKnowledge = set()
    for i in knowledge:
        flag = False
        for j in knowledge:
            if i.__eq__(j):
                continue
            if i.isRedundant([j]):
                flag = True
                continue
        if not flag and not i.isValid():
            newKnowledge.add(i)
    return newKnowledge



def getRules(state, neighbours):
    clauses = set()

    # rule no.1
    literals = set()
    literals.add(Literal(Labels.WUMPUS_STENCH,state, True))
    for i in neighbours:
        literals.add(Literal(Labels.WUMPUS,i[0],False))
    clauses.add(Clause(literals))

    # rule no.2
    for i in neighbours:
        literals = set()
        literals.add(Literal(Labels.WUMPUS_STENCH, state, False))
        literals.add(Literal(Labels.WUMPUS,i[0],True))
        clauses.add(Clause(literals))

    # rule no.3
    literals = set()
    literals.add(Literal(Labels.POISON_FUMES, state, True))
    for i in neighbours:
        literals.add(Literal(Labels.POISON, i[0], False))
    clauses.add(Clause(literals))

    # rule no.4
    for i in neighbours:
        literals = set()
        literals.add(Literal(Labels.POISON_FUMES, state, False))
        literals.add(Literal(Labels.POISON, i[0], True))
        clauses.add(Clause(literals))

    # rule no.5
    literals = set()
    literals.add(Literal(Labels.TELEPORTER_GLOW, state, True))
    for i in neighbours:
        literals.add(Literal(Labels.TELEPORTER, i[0], False))
    clauses.add(Clause(literals))

    # rule no.6
    for i in neighbours:
        literals = set()
        literals.add(Literal(Labels.TELEPORTER_GLOW, state, False))
        literals.add(Literal(Labels.TELEPORTER, i[0], True))
        clauses.add(Clause(literals))

    # rule no.7
    for i in neighbours:
        if not i==state:
            literals = set()
            literals.add(Literal(Labels.WUMPUS, state, True))
            literals.add(Literal(Labels.WUMPUS, i[0], True))
            clauses.add(Clause(literals))

    # rule no.8
    for i in neighbours:
        literals = set()
        literals.add(Literal(Labels.POISON_FUMES, state, False))
        literals.add(Literal(Labels.WUMPUS_STENCH, state, False))
        literals.add(Literal(Labels.SAFE, i[0], False))
        clauses.add(Clause(literals))
    # rule no.9
    literals = set()
    literals.add(Literal(Labels.WUMPUS, state, False))
    literals.add(Literal(Labels.POISON, state, False))
    literals.add(Literal(Labels.SAFE, state, False))
    clauses.add(Clause(literals))

    return clauses


