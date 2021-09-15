"""
board.py

Software-engineering project group B

14/09/2021
v0.1

Laurent VOURIOT

"""


class Board(object):
    """
    the board class

    a board in a certain state of the game
    """
    def __init__(self, difficulty, player_turn, white_pieces_in_hand,
                 black_pieces_in_hand, white_pieces_left, black_pieces_left,
                 board_size, lines):
        """
        constructor

    :param: difficulty (int) : 1 low, 2 medium, 3 high
        :param: player_turn (bool) : True white, False black
        :param: white_pieces_in_hand (int)
        :param: black_pieces_in_hand (int)
        :param: white_pieces_left (int)
        :param: black_pieces_left (int)
        :param: board_size (int)
        :param: lines (list(list))
        """

        self._difficulty = difficulty
        self._player_turn = player_turn
        self._white_pieces_in_hand = white_pieces_in_hand
        self._black_pieces_in_hand = black_pieces_in_hand
        self._white_pieces_left = white_pieces_left
        self._black_pieces_left = black_pieces_left
        self._board_size = board_size
        self._lines = lines
    def get_difficulty(self):
        return self._difficulty

    def __repr__(self):
        """
        :return: string to show all the attributes of the board for debug
        """
        return "difficulty : {}\n" \
               "player_turn : {}\n" \
               "white in hand {}\n" \
               "black in hand {}\n" \
               "white left {}\n" \
               "black left {}\n" \
               "size {}\n" \
               "lines {}\n".format(self._difficulty,
                                   self._player_turn,
                                   self._white_pieces_in_hand,
                                   self._black_pieces_in_hand,
                                   self._white_pieces_left,
                                   self._black_pieces_left,
                                   self._board_size,
                                   self._lines)



