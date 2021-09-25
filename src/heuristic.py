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

#going to analyze everything with the more positive number going to black; 
#negative going to better for white.

class Heuristic():

    #I originally planned to weight things with arrasy but decided it may not be needed. TBD
    def createVertexArray(board):
        # vertexArray = np.zeros(board.board_size,board.board_size)
        #print(board)
        #vertexArray = [board.get_board_size(),board.get_board_size()]
        #myArray = [board.get_board_size(),board.get_board_size()]
        w, h = board.get_board_size(), board.get_board_size()
        myArray = [[0 for x in range(w)] for y in range(h)]
        for line in board._lines:
            for item in line:
                x,y = item["xy"]
                myArray[x][y] += 1
        return myArray

 #counts all the blacks and whites.  
 #When there is a vertex, the values will get counted for each one, giving them a heavier weight. 
# Also gives +/- 3 for having 3 in a row.
    def firstPhaseState(self, board):
        score = 0
        for line in board._lines:
            numinrow =0
            last = ""
            for item in line:
                if ( last == item["owner"]):
                    numinrow +=1
                else :
                    numinrow = 0
                if item["owner"] == "black":
                    score = score +1
                    if numinrow == 3:
                        score = score + 3
                elif item["owner"] == "white":
                    score = score - 1
                    if numinrow == 3:
                        score = score - 3
                last = item["owner"]     
        return score


    #if a win condition is met, gives a score of =10/-10
    #else score is a delta between types of pieces
    def secondPhaseState(self, board):
        score = board.get_black_pieces_left() - board.get_white_pieces_left()
        if board.get_black_pieces_left() == 2:
            score = -10
        if board.get_white_pieces_left() == 2:
            score = +10
        return score



   # def createPlayerArray(self, board):
     #   playerArray = np.zeros(board.board_size, board.board_size)


#board = Board("low","black",12,12,12,12,24,[
#    [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"none"},{"xy":[1,3], "owner":"none"}],
#    [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}] ])


