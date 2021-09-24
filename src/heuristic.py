import unittest
import sys
import os
import json
#import numpy as np
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
#counts each point on the board where a piece can be played and counts them. Where the array is > 1 there are 2 possible lines.
    def createVertexArray(board):
        # vertexArray = np.zeros(board.board_size,board.board_size)
        print(board)
        #vertexArray = [board.get_board_size(),board.get_board_size()]
        #myArray = [board.get_board_size(),board.get_board_size()]
        w, h = board.get_board_size(), board.get_board_size()
        myArray = [[0 for x in range(w)] for y in range(h)]

        for line in board._lines:
            for item in line:
                x,y = item["xy"]
                myArray[x][y] += 1
        return myArray

    #TODO: this requires more work to make a good heuristic
    def firstPhaseState(self, board):
        vertex = Heuristic.createVertexArray(board)

        value = board.get_black_pieces_left() - board.get_white_pieces_left()
        return value


    #TODO: This is more of a marker than a good function at this point, need to create heuristic
    def secondPhaseState(self, board):
        value = board.get_black_pieces_left() - board.get_white_pieces_left()
        return value


    def pieceDifference(self, board):
        value = board.get_black_pieces_left - board.get_white_pieces_left
        return value




    def createPlayerArray(self, board):
     #   playerArray = np.zeros(board.board_size, board.board_size)
        print("This is a print statement, please print")





