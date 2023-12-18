from Player import HumanPlayer, EasyAIPlayer, MediumAIPlayer, HardAIPlayer
from Board import Board
from BoardConstants import BoardConstants
from Move import Move

class Game:

    def __init__(self, player1name, player2name, ai_level=None, game_state_string=None, player2_starts=False, player1_num_pieces=BoardConstants.NUM_STARTING_PIECES_EACH, player2_num_pieces=BoardConstants.NUM_STARTING_PIECES_EACH):
        self.__player1 = HumanPlayer(player1name, BoardConstants.player_1_colour, player1_num_pieces)

        if ai_level:
            self.__player2 = self.__make_ai_player(player2name, player2_num_pieces)
        else:
            self.__player2 = HumanPlayer(player2name, BoardConstants.player_2_colour, player2_num_pieces)

        self.__player_lst = [self.__player1, self.__player2]

        self.__game_over = False
        self.__board = Board(self.__player1, self.__player2, game_state_string)

        self.__move_history_stack = []

        self.__current_player = self.__player1
        self.__non_current_player = self.__player2

        if player2_starts: # if a game is loaded from a save it might be player 2's turn first
            self.switch_current_player()

    def __make_ai_player(self, player2name, player2_num_pieces):
        difficulty_dict = {
            "Easy AI": EasyAIPlayer,
            "Medium AI": MediumAIPlayer,
            "Hard AI": HardAIPlayer,
        }

        return difficulty_dict[player2name](BoardConstants.player_2_colour, player2_num_pieces)

    
    def get_ai_move(self):
        move = self.__current_player.get_move(self.__board)

        print(f"AI MOVE FOUND FROM {move.get_start_colour()}, {move.get_start_cords()} TO {move.get_end_colour()}, {move.get_end_cords()}")

        return move

    def is_legal_move(self, start_loc, end_loc, move_type):
        return self.__board.is_legal_move(start_loc, end_loc, self.__current_player, move_type)
    
    def get_game_state_string(self):
        return self.__board.get_game_state_string()

    def set_game_status(self):

        """Sets self.__game_over to True if either player has no pieces left. A legal move can always
        be played in Surakarta, so this is the only way the game can end."""

        if (self.__player1.get_piece_count() == 0 or self.__player2.get_piece_count() == 0):
            self.__game_over = True


    def get_board_state(self):
        return self.__board.get_board_state()
    
    def is_game_over(self):
        return self.__game_over

    def get_winner(self):
        if self.is_game_over(): # ! RECENT CHANGE MADE
            if self.__player1.get_piece_count() > self.__player2.get_piece_count():
                return self.__player1
            
            elif self.__player2.get_piece_count() > self.__player1.get_piece_count():
                return self.__player2
        
        else:
            raise Exception("Attempting to get winner when game is not over.")
            

    def move_piece(self, start_location, end_location, move_type):
        move_obj = Move(start_location, end_location, move_type)
        self.__move_history_stack.append(move_obj)

        self.__board.move_piece(move_obj)

        return move_obj


    def undo_move(self):
        if len(self.__move_history_stack) == 0:
            return None

        move_obj = self.__move_history_stack.pop()

        print(f"MOVE POPPED OFF STACK {(move_obj.get_start_loc().get_colour(), move_obj.get_start_loc().get_cords(), move_obj.get_move_type())}")
        print(f"TO {move_obj.get_end_loc().get_colour(), move_obj.get_end_loc().get_cords()}")

        self.__board.undo_move(move_obj)

        if move_obj.get_move_type() == "capture": # ! try moving to before calling undo with the board because it matches my psuedocode
            self.__current_player.add_piece()

        return move_obj

    def get_current_player_name(self):
        return self.__current_player.get_name()
    
    def switch_current_player(self):
        self.__current_player, self.__non_current_player = self.__non_current_player, self.__current_player
    
    def get_player_name(self, player_number):
        return self.__player_lst[player_number - 1].get_name()
    
    def get_player_colour(self, player_number):
        return self.__player_lst[player_number - 1].get_colour()
    
    def get_player_piece_count(self, player_number):
        return self.__player_lst[player_number - 1].get_piece_count()