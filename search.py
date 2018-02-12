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
    visited = set()
    nodes_to_visit = util.Stack()
    nodes_to_visit.push(problem.getStartState())
    prev = {}

    while not nodes_to_visit.isEmpty():
        node = nodes_to_visit.pop()
        if problem.isGoalState(node):
            return getMoveList(node, prev)
        visited.add(node)
        successors = problem.getSuccessors(node)
        for successor, action, cost in successors:
            if successor not in visited:
                nodes_to_visit.push(successor)
                prev[successor] = {"state": node, "action": action}

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    visited = set()
    nodes_to_visit = util.Queue()
    nodes_to_visit.push(problem.getStartState())
    prev = {}

    while not nodes_to_visit.isEmpty():
        node = nodes_to_visit.pop()
        if problem.isGoalState(node):
            return getMoveList(node, prev)
        visited.add(node)
        successors = problem.getSuccessors(node)
        for successor, action, cost in successors:
            if successor not in visited and \
                successor not in nodes_to_visit.list:
                nodes_to_visit.push(successor)
                prev[successor] = {"state":node, "action":action}

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    visited = set()
    nodes_to_visit = util.PriorityQueue()
    g_cost = {problem.getStartState(): 0}
    nodes_to_visit.push(problem.getStartState(), 0)
    prev = {}

    while not nodes_to_visit.isEmpty():
        state = nodes_to_visit.pop()
        if problem.isGoalState(state):  # if goal state, then return list of moves
            return getMoveList(state, prev)
        visited.add(state)  # add state and cost to visited
        successors = problem.getSuccessors(state)
        for successor, action, cost in successors:
            if successor not in g_cost.keys():
                g_cost[successor] = float('inf')
            if successor not in visited:
                g = g_cost[state] + cost
                if g < g_cost[successor]:
                    prev[successor] = {"state": state, "action": action}
                    g_cost[successor] = g
                nodes_to_visit.update(successor, g_cost[successor])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    visited = set()
    nodes_to_visit = util.PriorityQueue()
    g_cost = {problem.getStartState(): 0}
    nodes_to_visit.push(problem.getStartState(), 0)
    prev = {}

    while not nodes_to_visit.isEmpty():
        state = nodes_to_visit.pop()
        if problem.isGoalState(state): # if goal state, then return list of moves
            return getMoveList(state, prev)
        visited.add(state) # add state and cost to visited
        successors = problem.getSuccessors(state)
        for successor, action, cost in successors:
            if successor not in g_cost.keys():
                g_cost[successor] = 10000000
            if successor not in visited:
                h = heuristic(successor, problem)
                g = g_cost[state] + cost
                f = h + g_cost[state]
                if g < g_cost[successor]:
                    prev[successor] = {"state": state, "action": action}
                    g_cost[successor] = g
                    f = h + g
                
                nodes_to_visit.update(successor, f)

    return []

def getMoveList(state, prev_dict):
    """ get list of moves to reach goal """
    move_list = []
    while prev_dict.has_key(state):
        move_list.append(prev_dict[state]["action"])
        state = prev_dict[state]["state"]
    move_list.reverse()
    return move_list

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
