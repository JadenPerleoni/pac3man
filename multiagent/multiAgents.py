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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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

        # Represents the grid of food dots as a list, each tuple is a cordinate (x,y)
        foodList = newFood.asList()        

        if foodList:
            # If food list is not empty, calculate the MINIMUM distance 
            # to reach the nearest food dot using Manhattan Distance
            minFoodDistance = min([manhattanDistance(newPos,food) for food in foodList])
        else:
            # If foodlist is empty, there are no food dots remaining and
            # we set minFoodDistance to 0
            minFoodDistance = 0
        
        # We also want to account for ghosts. Calculate the manhattan
        # distance to the closest ghost from current position.
        
        # Get manhattan distance from each ghost's position at current position
        ghostPositions = successorGameState.getGhostPositions()

        # Find the distance to the nearest ghost
        minGhostDistance = min([manhattanDistance(newPos,ghostPos) for ghostPos in ghostPositions])

        

        # If the ghosts are active, we want to AVOID them

        # Determine the time left in seconds of scared ghosts, if the scared time
        # is greater than 0, we add it to scaredGhosts
        scaredGhosts = [ghost.scaredTimer for ghost in newGhostStates if ghost.scaredTimer > 0]

        # Determine the number of active ghosts.
        # If the ghost has a scared time of 0, count it as active
        activeGhosts = [ghost.scaredTimer for ghost in newGhostStates if ghost.scaredTimer == 0]


        # Represents the score at the current state
        score = successorGameState.getScore()

        # If there are active ghosts, subtract the distance to the closest ghost
        # from the score.

        # A minimum function is used in order to set a minimum distance from a ghost
        # to avoid. If the closest ghost is over 7 blocks away, we don't need to 
        # worry about pacman running into it. 7 was the value that avoided the ghosts 
        # best for me when testing.
        if activeGhosts:
            score -= (min(minGhostDistance, 7) * -1)
        # If the ghost is scared, add the path to the score
        if scaredGhosts:
            score += min(minGhostDistance,4)


        # As the minimum distance to the nearest food dot gets lower,
        # the value added to the score increases. This incentivizes
        # pacman to take a path closest to food dots.
        score += 1.0 / (minFoodDistance + 1)

        # Return the total score of the current path
        return score



def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex,depth, gameState):
            # Check if depth is at its max level or if game is over
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
          
            # If we want to calculate pacman's best move, we use MAX
            # (pacman is our max agent)
            if agentIndex == 0:
                return maxValue(agentIndex,depth,gameState)
            # Else calculate the adverserial (min)
            else:
                return minValue(agentIndex,depth,gameState)
            
            # Function to find the maximum value for each possbile move
            # in a given state.
        def maxValue(agentIndex, depth, gameState):
            maxEval = float('-inf')
            legalMoves = gameState.getLegalActions(agentIndex)

            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex,action)
                maxEval = max(maxEval,minimax(1,depth,successor))
            return maxEval
            

        def minValue(agentIndex, depth, gameState):
            minEval = float('inf')
            legalMoves = gameState.getLegalActions(agentIndex)
            # Set the index of the next agent
            nextAgentIndex = agentIndex + 1

            if nextAgentIndex == gameState.getNumAgents():
                nextAgentIndex = 0
                depth += 1


            for action in legalMoves:
                successor = gameState.generateSuccessor(agentIndex,action)
                minEval = min(minEval,minimax(nextAgentIndex,depth,successor))
            return minEval
        
        legalMoves = gameState.getLegalActions(0)
        bestMove = None
        bestVal = float('-inf')

        for action in legalMoves:
            successor = gameState.generateSuccessor(0,action)
            value = minimax(1,0,successor)
            if value > bestVal:
                bestVal = value
                bestMove = action
        return bestMove
                




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

