import math
from MultiClassBoardAttributes import MultiClassBoardAttributes
import time
from copy import deepcopy

class Node:

    """Node class reprsenting a node in the game tree"""

    def __init__(self, board, depth, move_obj=None):

        # the board object of the node
        self.__board = board

        # the move that led to this node
        self.__move_obj = move_obj

        # UCB1 parameters
        self.__value = 0
        self.__visited_count = 0

        # the children of the node (list of Node objects)
        self.__children = []

        # the parent of the node (Node object)
        self.__parent = None

        # the depth of the node in the tree (root node has depth 0)
        self.__depth = depth

    def get_board(self):
        return self.__board

    def add_child(self, child):
        """adds a child to the node. child is a Node object."""

        self.__children.append(child)
        child.set_parent(self)

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent
    
    def get_depth(self):
        """returns the depth of the node in the tree"""

        return self.__depth
    
    def get_move_obj(self):
        return self.__move_obj
    
    def get_visited_count(self):
        return self.__visited_count
    
    def increment_visited_count(self):
        """increments the visited count of the node by 1. This is called when the node is visited during an MCTS simulation."""

        self.__visited_count += 1
    
    def get_children(self):
        return self.__children
    
    def get_value(self):
        return self.__value
    
    def add_to_value(self, value):
        """updates the value of the node by adding the value passed in to the current value.
        This is called when the node is visited during an MCTS simulation."""

        self.__value += value

class GameTree:

    """GameTree class representing the game tree created by the MCTS algorithm
    
    ####################################################################
    CLASS A SKILL: Monte Carlo Tree Search (MCTS)
    CLASS A SKILL: Tree data structure and tree traversal
    ClASS A SKILL: Complex OOP model with encapsulation and composition
    GOOD CODING STYLE: Use of constants
    ####################################################################

    """

    # rollout result constants
    LOSS = -1
    DRAW = 0
    WIN = 1
    
    # moves before early stop 
    MOVES_PER_ROLLOUT = 500

    # exploration constant for the UCB1 formula
    EXPLORATION_CONSTANT = 2

    def __init__(self, root_board, time_for_move):

        self.__root = Node(root_board, depth=0)

        # the maximum depth of a node in the tree
        self.__current_tree_depth = 0

        # time allowed for the MCTS algorithm to run
        self.__time_for_move = time_for_move

        self.__current_node = self.__root

    def __get_current_player_colour(self, depth):
        """returns the colour of the current player based on a depth in the tree"""

        # if the depth is even, it's player 2's (the AI) turn
        if depth % 2 == 0:
            return MultiClassBoardAttributes.player_2_colour
        
        # if the depth is odd, it's player 1's turn
        elif depth % 2 == 1:
            return MultiClassBoardAttributes.player_1_colour

    def __add_node(self, child_board, move_obj):
        """adds a node to the tree. child_board is the board state of the new node, and move_obj is the move that led to the node."""

        new_depth = self.__current_node.get_depth() + 1
        child = Node(child_board, new_depth, move_obj)

        self.__current_node.add_child(child)

    def __calc_UCB1(self, node):
        
        """returns the UCB1 value of a node used to determine which node to select next in the MCTS algorithm
        
        ####################################################################
        EXCELLENT CODING STYLE: Good exception handling
        ####################################################################
        
        """
        
        # using the UCB1 formula
        try:
            return (node.get_value() / node.get_visited_count()) + (GameTree.EXPLORATION_CONSTANT * math.sqrt(math.log(node.get_parent().get_visited_count()) / node.get_visited_count()))

        # if the node has not been visited yet (visited_count is 0), it's value is infinity
        except ZeroDivisionError:
            return math.inf

    def __check_terminal_board(self, board):

        """if the board is terminal, returns the result of the board (1 if the AI won, -1 if the AI lost). Otherwise, returns False."""

        if board.get_piece_count(1) == 0:
            return GameTree.WIN
        
        elif board.get_piece_count(2) == 0:
            return GameTree.LOSS
        
        return False

    def __get_early_stop_rollout_result(self, board):

        """returns the result of the board (1 for AI win, -1 for AI loss, 0 if neither player is winning according to the evaluation function)
        if the rollout ends early because the maximum number of moves per rollout has been reached."""

        if board.get_piece_count(1) > board.get_piece_count(2):
            return GameTree.LOSS
        
        elif board.get_piece_count(1) < board.get_piece_count(2):
            return GameTree.WIN
        
        else:
            return GameTree.DRAW
        
    def __get_current_legal_moves(self):
        """returns the legal moves for the current node"""

        # board object of the current node
        board = self.__current_node.get_board()

        curr_depth = self.__current_node.get_depth()
        current_player_colour = self.__get_current_player_colour(curr_depth)

        # get the legal moves for the current player
        return board.get_player_legal_moves(current_player_colour)

    def __current_is_leaf(self):
        """returns True if the current node is a leaf node in the tree, otherwise returns False"""

        return len(self.__current_node.get_children()) == 0
    
    def __select_new_current(self):

        """selects a new current node to be the node with the highest UCB1 value among the current node's children"""

        # list of tuples of the form (node, UCB1 value) for each child of the current node
        ucb1_scores = [(node, self.__calc_UCB1(node)) for node in self.__current_node.get_children()]

        # set the current node to the child with the highest UCB1 value
        self.__current_node = max(ucb1_scores, key=lambda x: x[1])[0]

        # update the maximum depth of the tree if the current node's depth is greater than the current maximum depth
        if self.__current_tree_depth < self.__current_node.get_depth():
            self.__current_tree_depth = self.__current_node.get_depth()

    def __node_expansion(self):

        """expands the current node by adding all of its legal moves as children"""

        # list of legal moves for the current node
        legal_moves = self.__get_current_legal_moves()

        for move_obj in legal_moves:

            # make a deep copy of the current node's board and make the move on the copy (so that the original board is not modified)
            board = deepcopy(self.__current_node.get_board())
            board.move_piece(move_obj)

            self.__add_node(board, move_obj)
    
    def __rollout(self):

        """performs a rollout from the current node to a terminal node or to the rollout depth and returns the result of the rollout"""
        
        # deepcopy the current node's board so that the original board is not modified
        rollout_board = deepcopy(self.__current_node.get_board())

        num_moves = 0

        while num_moves < GameTree.MOVES_PER_ROLLOUT:

            # check if the board is terminal and if so return the result of the rollout
            terminal_board_result = self.__check_terminal_board(rollout_board)
            if terminal_board_result:
                return terminal_board_result
            
            # get the colour of the current player based on the depth of the current node
            current_depth = self.__current_node.get_depth() + num_moves
            rollout_colour = self.__get_current_player_colour(current_depth)

            simulated_move = rollout_board.get_single_random_legal_move(rollout_colour)
            rollout_board.move_piece(simulated_move)
            
            num_moves += 1

        # max rollout depth reached
        return self.__get_early_stop_rollout_result(rollout_board)
        
    def __backpropagate(self, result):

        """backpropagates the result of a rollout up the tree"""

        node = self.__current_node

        # terminate the loop when the root node has had its value and visited count updated
        while node != None:
            node.increment_visited_count()
            node.add_to_value(result)
            node = node.get_parent()

    def __run_MCTS_iteration(self):

        """runs one iteration of the MCTS algorithm from the current node with selection, expansion, rollout, and backpropagation"""

        # 1. Selection
        while not self.__current_is_leaf():
            self.__select_new_current()

        if self.__current_node.get_visited_count() != 0:

            # 2. Expansion
            self.__node_expansion()
            if not self.__current_is_leaf(): # terminal nodes will not have children
                self.__current_node = self.__current_node.get_children()[0]

        # 3. Rollout/Simulation
        result = self.__rollout()

        # 4. Backpropagation
        self.__backpropagate(result)

        # reset the current node to the root node for the next iteration
        self.__current_node = self.__root

    def get_next_move(self):

        """Public method that runs the MCTS algorithm for a set amount of time and returns the best move to make"""

        start_time = time.time()

        # initial node expansion before the MCTS iterations begin
        self.__node_expansion() 

        num_iterations = 0

        while time.time() - start_time < self.__time_for_move:
            self.__run_MCTS_iteration()
            num_iterations += 1

        # best node/move to make is the child of the root node with the highest UCB1 value
        best_node = max(self.__root.get_children(), key=lambda node: node.get_value())
        
        return best_node.get_move_obj()

