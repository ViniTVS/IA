# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState
import time

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        
        distFantasma = 99999
        distAmendrontado = 99999
        for ghostState in newGhostStates:
            dist = manhattanDistance(newPos, ghostState.getPosition())
            # vamos morrer :(
            if (ghostState.scaredTimer == 0 and dist <= 1):
                return -1
            spawn = ghostState.start.pos
            # se o fantasma está amedrontado e numa dist. "segura", vamos tentar comê-lo
            if (dist <= ghostState.scaredTimer and manhattanDistance(newPos, spawn) > 1):
                distAmendrontado = min(dist, distAmendrontado)
            # se não, fugir
            else:
                distFantasma = min(dist, distFantasma)
        # "desincentivar" de chegar perto dos fantasmas
        distFantasma = 10 / distFantasma
        # incentivar de comer os amedrontados
        distAmendrontado = 300 / min(distAmendrontado, 300)
        # incentivar a ir atrás de comida
        if newPos in newFood.asList():
            distComida = 10
        else:
            distComida = 10 / min(
                [manhattanDistance(comida, newPos) for comida in newFood.asList()], default=1
            )
            
        return score + distAmendrontado + distComida - distFantasma 

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """


    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # num. de fantasmas no game
        self.ghosts = gameState.getNumAgents() - 1
        self.move = gameState.getLegalActions(0)[0] 

        self.MaxAgent(gameState, 0)

        return self.move

    # Funções auxiliares
    def endAgent(self, gameState: GameState, depth):
        return gameState.isWin() or gameState.isLose() or depth == self.depth

    def MaxAgent(self, gameState: GameState, depth):
        if self.endAgent(gameState, depth):
            return self.evaluationFunction(gameState)

        # calculamos o melhor caso de cada movimento possível
        val = float("-inf")
        best_action = gameState.getLegalActions(0)[0]
        for action in gameState.getLegalActions(0):
            aux = self.MinAgent(gameState.generateSuccessor(0, action), depth, 1)
            if (aux > val):
                val = aux
                best_action = action
        # atualiza movimento a se fazer
        if (depth == 0):
            self.move = best_action
        return val

    def MinAgent(self, gameState: GameState, depth, ghost):
        if self.endAgent(gameState, depth):
            return self.evaluationFunction(gameState)

        # calculamos o pior caso de cada movimento possível
        val = float("inf")
        for action in gameState.getLegalActions(ghost):
            if (ghost == self.ghosts):
                # o último fantasma precisa selecionar o movimento do pacman que vai maximizar os pontos
                val = min(
                    val, self.MaxAgent(gameState.generateSuccessor(self.ghosts, action), depth + 1)
                )
            else:
                # também precisa selecionar os movimentos dos outros fantasmas 
                # que vão minimizar os pontos e verificar a pontuação feita
                val = min(
                    val, self.MinAgent(gameState.generateSuccessor(ghost, action), depth, ghost + 1)
                )

        return val

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.ghosts = gameState.getNumAgents() - 1
        self.move = gameState.getLegalActions(0)[0]
        
        self.MaxAgent(gameState, 0, float("-inf"), float("inf"))

        return self.move
    
    def endAgent(self, gameState: GameState, depth):
        return gameState.isWin() or gameState.isLose() or depth == self.depth

    def MaxAgent(self, gameState: GameState, depth, alpha, beta):
        if self.endAgent(gameState, depth):
            return self.evaluationFunction(gameState)

        # calculamos cada ação possível
        val = float("-inf")
        best_action = gameState.getLegalActions(0)[0]
        for action in gameState.getLegalActions(0):
            aux = self.MinAgent(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)
            if (aux > val):
                val = aux
                best_action = action
            # pruning
            if (val > beta):
                return val
            alpha = max(alpha, val)
        # atualiza movimento a se fazer
        if (depth == 0):
            self.move = best_action
            
        return val

    def MinAgent(self, gameState: GameState, depth, ghost, alpha, beta):
        if self.endAgent(gameState, depth):
            return self.evaluationFunction(gameState)

        val = float("inf")
        for action in gameState.getLegalActions(ghost):
            if (ghost == self.ghosts):
                # o último fantasma precisa selecionar o movimento do pacman que vai maximizar os pontos
                val = min(
                    val, self.MaxAgent(gameState.generateSuccessor(self.ghosts, action), depth + 1, alpha, beta)
                )
            else:
                # também precisa selecionar os movimentos dos outros fantasmas 
                # que vão minimizar os pontos e verificar a pontuação feita
                val = min(
                    val, self.MinAgent(gameState.generateSuccessor(ghost, action), depth, ghost + 1, alpha, beta)
                )
            # pruning
            if (val < alpha):
                return val
            beta = min(beta, val)

        return val

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # num. de fantasmas no game
        self.ghosts = gameState.getNumAgents() - 1
        self.move = gameState.getLegalActions(0)[0] 

        self.MaxAgent(gameState, 0)

        return self.move

    # Funções auxiliares
    def endAgent(self, gameState: GameState, depth):
        return gameState.isWin() or gameState.isLose() or depth == self.depth

    def MaxAgent(self, gameState: GameState, depth):
        if self.endAgent(gameState, depth):
            return self.evaluationFunction(gameState)

        # calculamos o melhor caso de cada movimento possível
        val = float("-inf")
        best_action = gameState.getLegalActions(0)[0]
        for action in gameState.getLegalActions(0):
            aux = self.MinAgent(gameState.generateSuccessor(0, action), depth, 1)
            if (aux > val):
                val = aux
                best_action = action
        # atualiza movimento a se fazer
        if (depth == 0):
            self.move = best_action
        return val

    def MinAgent(self, gameState: GameState, depth, ghost):
        if self.endAgent(gameState, depth):
            return self.evaluationFunction(gameState)

        # calculamos o pior caso de cada movimento possível
        val = float("inf")
        # vetor com as opções de escolha
        options = []
        for action in gameState.getLegalActions(ghost):
            if (ghost == self.ghosts):
                # o último fantasma precisa selecionar o movimento do pacman que vai maximizar os pontos
                new_val = self.MaxAgent(gameState.generateSuccessor(self.ghosts, action), depth + 1)
                
            else:
                # também precisa selecionar os movimentos dos outros fantasmas 
                # que vão minimizar os pontos e verificar a pontuação feita
                new_val = self.MinAgent(gameState.generateSuccessor(ghost, action), depth, ghost + 1)
                
            options.append(new_val)
        
        # o valor final passa a ser a média deste vetor
        val = sum(options) / len(options)

        return val

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: A ideia é de "adaptar" o algoritmo do Expectimax, de forma que 
    (somente) o agente do pacman calcula os custos de ação com a função feita na 
    questão 1, enquanto os agentes dos fantasmas utilizam somente o valor do 
    score do jogo. 
    """
    "*** YOUR CODE HERE ***"
    ################### funções auxiliares #######################
    def endAgent(gameState: GameState, depth, max_depth):
        return gameState.isWin() or gameState.isLose() or depth == max_depth

    def evaluate(gameState: GameState):
        newPos = gameState.getPacmanPosition()
        newFood = gameState.getFood()
        newGhostStates = gameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        score = gameState.getScore()
        
        distFantasma = 99999
        distAmendrontado = 99999
        for ghostState in newGhostStates:
            dist = manhattanDistance(newPos, ghostState.getPosition())
            # vamos morrer :(
            if (ghostState.scaredTimer == 0 and dist <= 1):
                return -1
            spawn = ghostState.start.pos
            # se o fantasma está amedrontado e numa dist. "segura", vamos tentar comê-lo
            if (dist <= ghostState.scaredTimer and manhattanDistance(newPos, spawn) > 1):
                distAmendrontado = min(dist, distAmendrontado)
            # se não, fugir
            else:
                distFantasma = min(dist, distFantasma)
        # "desincentivar" de chegar perto dos fantasmas
        distFantasma = 10 / distFantasma
        # incentivar de comer os amedrontados
        distAmendrontado = 300 / min(distAmendrontado, 300)
        # incentivar a ir atrás de comida
        if newPos in newFood.asList():
            distComida = 10
        else:
            distComida = 10 / min(
                [manhattanDistance(comida, newPos) for comida in newFood.asList()], default=1
            )
            
        return score + distAmendrontado + distComida - distFantasma 
    
    def MaxAgent(gameState: GameState, depth, max_depth, alpha, beta, ghost_num):
        if endAgent(gameState, depth, max_depth):
            return evaluate(gameState)
        # calculamos cada ação possível
        val = float("-inf")
        for action in gameState.getLegalActions(0):
            aux = MinAgent(gameState.generateSuccessor(0, action), depth, max_depth, 1, alpha, beta, ghost_num)
            if (aux > val):
                val = aux
            # pruning
            if (val > beta):
                return val
            alpha = max(alpha, val)
            
        return val

    def MinAgent(gameState: GameState, depth, max_depth, ghost, alpha, beta, ghost_num):
        if endAgent(gameState, depth, max_depth):
            return gameState.getScore()

        val = float("inf")
        for action in gameState.getLegalActions(ghost):
            if (ghost == ghost_num):
                # o último fantasma precisa selecionar o movimento do pacman que vai maximizar os pontos
                val = min(
                    val, MaxAgent(gameState.generateSuccessor(ghost, action), depth + 1, max_depth, alpha, beta, ghost_num)
                )
            else:
                # também precisa selecionar os movimentos dos outros fantasmas 
                # que vão minimizar os pontos e verificar a pontuação feita
                val = min(
                    val, MinAgent(gameState.generateSuccessor(ghost, action), depth, max_depth, ghost + 1, alpha, beta, ghost_num)
                )
            # pruning
            if (val < alpha):
                return val
            beta = min(beta, val)

        return val
    ################### fim funções #######################
    
    ghosts = currentGameState.getNumAgents() - 1
    return MaxAgent(currentGameState, 0, 1, float("-inf"), float("inf"), ghosts)



# Abbreviation
better = betterEvaluationFunction
