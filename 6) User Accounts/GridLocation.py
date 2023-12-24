from Piece import Piece
from MultiClassBoardAttributes import MultiClassBoardAttributes

class GridLocation:

    """represnts information about a location on the board such as
    the piece on it, its coordinates and which of the looped tracks it sits on"""

    # outer loop cordinates have row (2 or 3) and column (2 or 3)
    OUTER_LOOP_NUMBERS = (2, 3)

    # inner loop cordinates have row (1 or 4) and column (1 or 4)
    INNER_LOOP_NUMBERS = (1, 4)

    # player 1 pieces start on rows 0 and 1, player 2 pieces start on rows 4 and 5
    PLAYER_1_ROWS = (0, 1)
    PLAYER_2_ROWS = (4, 5)

    def __init__(self, cords):
        self.__cords = cords
        self.__loop = self.__set_loop()

        # initial piece set for a fresh board
        self.__piece = self.__set_initial_piece()

    def __set_loop(self):

        """determines which loop(s) a location sits on"""

        if (self.__cords[0] in self.OUTER_LOOP_NUMBERS and self.__cords[1] in self.INNER_LOOP_NUMBERS) or (self.__cords[0] in self.INNER_LOOP_NUMBERS and self.__cords[1] in self.OUTER_LOOP_NUMBERS):
            return "BOTH"

        elif self.INNER_LOOP_NUMBERS[0] in self.__cords or self.INNER_LOOP_NUMBERS[1] in self.__cords:
            return "INNER"
        
        elif self.OUTER_LOOP_NUMBERS[0] in self.__cords or self.OUTER_LOOP_NUMBERS[1] in self.__cords:
            return "OUTER"
        
        else:
            return None

    def __set_initial_piece(self):

        """determines which piece should be placed on a location at the start of the game"""

        if self.__cords[0] in self.PLAYER_1_ROWS:
            return Piece(MultiClassBoardAttributes.player_1_colour)
        
        elif self.__cords[0] in self.PLAYER_2_ROWS:
            return Piece(MultiClassBoardAttributes.player_2_colour)

        else:
            return None

    def is_empty(self):
        return self.__piece == None
    
    def set_piece(self, piece):
        self.__piece = piece

    def get_piece(self):
        return self.__piece
    
    def get_colour(self):
        if self.__piece == None:
            return None
        else:
            return self.__piece.get_colour()
    
    def get_cords(self):
        return self.__cords
    
    def get_loop(self):
        return self.__loop

