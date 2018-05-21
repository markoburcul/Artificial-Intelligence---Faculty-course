# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import copy

class SearchNode:
    """
    This class represents a node in the graph which represents the search problem.
    The class is used as a basic wrapper for search methods - you may use it, however
    you can solve the assignment without it.

    REMINDER: You need to fill in the backtrack function in this class!
    """

    def __init__(self, position, parent=None, transition=None, cost=0, heuristic=0):
        """
        Basic constructor which copies the values. Remember, you can access all the 
        values of a python object simply by referencing them - there is no need for 
        a getter method. 
        """
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.transition = transition

    def __init__(self, position, parent, transition, cost):
        self.position = position
        self.parent = parent
        self.transition = transition
        self.cost = cost
        self.heuristic = None

    def isRootNode(self):
        """
        Check if the node has a parent.
        returns True in case it does, False otherwise
        """
        return self.parent == None 

    def unpack(self):
        """
        Return all relevant values for the current node.
        Returns position, parent node, cost, heuristic value
        """
        return self.position, self.parent, self.cost, self.heuristic


    def backtrack(self):
        """
        Reconstruct a path to the initial state from the current node.
        Bear in mind that usually you will reconstruct the path from the 
        final node to the initial.
        """
        moves = []
        # make a deep copy to stop any referencing isues.
        node = copy.deepcopy(self)

        if node.isRootNode():
            # The initial state is the final state
            return moves

        while node is not None and node.transition is not None :
            moves.append(node.transition)
            node = node.parent

        moves.reverse()
        return moves




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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    stack = util.Stack()
    n = SearchNode(problem.getStartState(),None,None,None)
    stack.push(n)
    visitedStates = dict()


    while(not stack.isEmpty()):
        n = stack.pop()

        visitedStates[n.position] = 1


        if problem.isGoalState(n.position):
            return n.backtrack()

        for m in problem.getSuccessors(n.position):
            if visitedStates.has_key(m[0]):
                continue
            newNode = SearchNode(m[0],n,m[1],m[2])
            stack.push(newNode)


    return []


def breadthFirstSearch(problem):
    queue = util.Queue()
    n = SearchNode(problem.getStartState(), None, None, None)
    queue.push(n)
    visitedStates = []

    while(not queue.isEmpty()):
        n = queue.pop()

        if visitedStates.__contains__(n.position):
            continue

        visitedStates.append(n.position)

        if problem.isGoalState(n.position):
            return n.backtrack()

        for m in problem.getSuccessors(n.position):
            newNode = SearchNode(m[0], n, m[1], m[2])
            if visitedStates.__contains__(m[0]):
                continue
            queue.push(newNode)

    return []

def uniformCostSearch(problem):
    queue = util.PriorityQueue()
    n = SearchNode(problem.getStartState(), None, None, None)
    queue.push(n,n.cost)
    visitedStates = dict()

    while(not queue.isEmpty()):
        n = queue.pop()

        visitedStates[n.position] = 1

        if problem.isGoalState(n.position):
            return n.backtrack()

        for m in problem.getSuccessors(n.position):
            newNode = SearchNode(m[0], n, m[1], m[2])
            if visitedStates.has_key(m[0]):
                continue

            queue.push(newNode,newNode.cost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    queue = util.MyQueue()
    n = SearchNode(problem.getStartState(), None, None, 0)
    queue.push(n,heuristic(n.position,problem))
    visitedStates = util.MyQueue()


    while(not queue.isEmpty()):
        n = queue.pop()


        visitedStates.push(n,heuristic(n.position,problem))

        if problem.isGoalState(n.position):
            return n.backtrack()

        for m in problem.getSuccessors(n.position):
            newNode = SearchNode(m[0], n, m[1], heuristic(m[0],problem)+m[2]+n.cost-heuristic(n.position,problem))
            if (visitedStates.itemExists(m[0]) or queue.itemExists(m[0])):
                copyNode = visitedStates.getItem(m[0]) if visitedStates.itemExists(m[0]) else queue.getItem(m[0])

                if(copyNode.cost-heuristic(copyNode.position,problem)<newNode.cost-heuristic(newNode.position,problem)):
                    continue
                else:
                    if visitedStates.itemExists(m[0]):
                        visitedStates.removeItem(m[0])
                    else:
                        queue.removeItem(m[0])
            queue.push(newNode, newNode.cost+heuristic(newNode.position,problem))

    return []




# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
