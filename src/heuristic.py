import unittest
import sys
import os
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import reader as file_reader
from game_engine import Engine
import json
import os.path  # exists
from board import Board

# :param: difficulty (int) : 1 low, 2 medium, 3 high
 #       :param: player_turn (bool) : True white, False black
 #       :param: white_pieces_in_hand (int)
 #       :param: black_pieces_in_hand (int)
 #       :param: white_pieces_left (int)
 #       :param: black_pieces_left (int)
 #       :param: board_size (int)
 #       :param: lines (list(list))

#going to analyze everything with the more positive number going to black; negative going to better for white.
class Heuristic():

    def pieceDifference(board):
        value = board.black_pieces_left - board.white_pieces_left
        return value


#counts each point on the board where a piece can be played and counts them. Where the array is > 1 there are 2 possible lines.
    def createVertexArray(board):
        myarray[board.board_size][board.board_size]
        for line in board._lines:
            for item in line:
                x,y = item["xy"]
                myarray[x][y] += 1
        return myarray




