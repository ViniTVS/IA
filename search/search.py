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
from typing import Tuple

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

"""
    resolucao do depthFirstSearch (DFS) de forma recursiva

    problema: instancia do problema 
    posicao: posicao atual do pacman
    movimentos: quais movimentos o pacman deve fazer para encontrar a bolinha
    percorridos: quais posicoes o algoritmo ja passou
"""
def DFSAux(problem, posicao, movimentos, percorridos):
    # indica que ja percorri esta posicao
    percorridos.push(posicao)

    if(problem.isGoalState(posicao)):
        return True
    
    # como a posicao atual nao e resposta, vamos percorrer os vizinhos
    for (pos, direcao, _) in problem.getSuccessors(posicao):
        # pula os que ja percorri para evitar loops
        if (pos in percorridos.list):
            continue
        # verifica se percorrendo este vizinho, o mesmo acha o resultado
        if DFSAux(problem, pos, movimentos, percorridos):
            movimentos.push(direcao) # se encontra, devo ir por esta direcao
            return True
    # não foi encontrado caminho
    return False

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    movimentos = util.Queue()
    percorridos = util.Stack()
    posicao = problem.getStartState()
    DFSAux(problem, posicao, movimentos, percorridos)
    
    return movimentos.list


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # como é uma busca em largura, preciso marcar os nodos percorridos e 
    # os restantes
    movimentos = [] # movimentos feitos para chegar em sua pos.
    posicao = problem.getStartState()
    percorridos = util.Stack()
    # fila (sem prioridade) com os caminhos ainda não percorridos
    para_percorrer = util.Queue()
    para_percorrer.push([posicao, movimentos, 0])

    while not para_percorrer.isEmpty():
        (pos_atual, mov_atual, c_atual) = para_percorrer.pop()
        
        if pos_atual in percorridos.list: # já processado
            continue
        
        percorridos.push(pos_atual)

        if problem.isGoalState(pos_atual): #chegamos à resposta
            return mov_atual

        # como a posicao atual nao e resposta, vamos percorrer os vizinhos
        for (pos_filho, mov_filho, c_filho) in problem.getSuccessors(pos_atual):
            # atualiza custo para este filho e o caminho para chegar
            custo = c_atual + c_filho
            mov = mov_atual + [mov_filho]            
            para_percorrer.push([pos_filho, mov, custo])
    # não existe estado que seja objetivo
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # basicamente o breadthFirstSearch, mas usando uma fila com prioridades,
    # que será definida pelo custo de cada caminho
    movimentos = [] # movimentos feitos para chegar em sua pos.
    posicao = problem.getStartState()
    percorridos = util.Stack()
    # fila com prioridade com os caminhos ainda não percorridos
    para_percorrer = util.PriorityQueue()
    para_percorrer.push([posicao, movimentos, 0], 0)

    while not para_percorrer.isEmpty():
        (pos_atual, mov_atual, c_atual) = para_percorrer.pop()
        if pos_atual in percorridos.list: # já processado, pula
            continue
        
        percorridos.push(pos_atual)
        if problem.isGoalState(pos_atual): #chegamos à resposta
            return mov_atual
        # como a posicao atual não é resposta, vamos percorrer os vizinhos
        for (pos_filho, mov_filho, c_filho) in problem.getSuccessors(pos_atual):
            # atualiza custo para este filho e o caminho para chegar até ele
            custo = c_atual + c_filho
            mov = mov_atual + [mov_filho]            
            para_percorrer.push([pos_filho, mov, custo], custo)
    # não acho objetivo
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # basicamente o uniformCostSearch, mas usando uma heuristica para determinar 
    # o custo de tomar certo caminho
    movimentos = [] # movimentos feitos para chegar em sua pos.
    posicao = problem.getStartState()
    percorridos = util.Stack()
    # fila com prioridade com os caminhos ainda não percorridos
    para_percorrer = util.PriorityQueue()
    para_percorrer.push([posicao, movimentos, 0], 0)

    while not para_percorrer.isEmpty():
        (pos_atual, mov_atual, c_atual) = para_percorrer.pop()
        
        if pos_atual in percorridos.list: # já processado
            continue
        
        percorridos.push(pos_atual)

        if problem.isGoalState(pos_atual): #chegamos à resposta
            return mov_atual

        # como a posicao atual nao e resposta, vamos percorrer os vizinhos
        for (pos_filho, mov_filho, c_filho) in problem.getSuccessors(pos_atual):
            # atualiza custo para este filho e o caminho até ele
            custo = c_atual + c_filho
            mov = mov_atual + [mov_filho]            
            para_percorrer.push([pos_filho, mov, custo], custo + heuristic(pos_filho, problem))

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
