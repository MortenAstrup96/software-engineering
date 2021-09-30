import sys
import os
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import os.path  # 
from collections import defaultdict
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
    
    
    #This isn't checking for all three in a row, it hosuld only be checking the newest piece for 3 in a row
    def numberOfMorris(self, board):
        score = 0
        for line in board.get_lines():
            numinrow =0
            last = ""
            for item in line:
                if (last == item["owner"]):
                    numinrow +=1
                else :
                    numinrow = 0
                if item["owner"] == "black":
                    if numinrow == 2:
                        score = score + 1
                elif item["owner"] == "white":
                    if numinrow == 2:
                        score = score - 1
                last = item["owner"]  
        return score
    
    def numberOfPieces(self, board):
        score = board.get_black_pieces_left() - board.get_white_pieces_left()
        return score
    
    def numberBlockedOpponentPieces(self,board):
        return
        
    def numberOfTwoPiece(self, board):
       return 
        
    def closedMorris(self, board):
        return
    
    def numberThreePiece(self, board):
        return
        
    def doubleMorris(self, board):
        return
    
    def winningState(self, board):
        score = 0
        if board.get_black_pieces_left() == 2:
            score = -1
        if board.get_white_pieces_left() == 2:
            score = 1
        return score
    
    def findAllRows(self, board, xy):
        rows = []
        for line in board.get_lines():
            for item in line:
                if item["xy"] == xy:
                    rows.push(line);  
        return rows


    def checkForOpen(self, board, color, pos):
        for xIndex, line in enumerate(board.get_lines()):
            for yIndex, item in enumerate(line):
                if item["xy"] == pos:
                    if ( ((yIndex - 1) > 0 ) and 
                        ( line[yIndex - 1]["owner"] == color or line[yIndex - 1]["owner"] == "none")):
                        return 0;
                    if ( ((yIndex + 1) < len(line) ) and 
                        ( line[yIndex + 1]["owner"] == color or line[yIndex + 1]["owner"] == "none")):
                        return 0;
        return 1;
                        

    def findEachBlockedPiece(self, board, color):
        count = 0
        checked = []
        for xIndex, line in enumerate(board.get_lines()):
            for yIndex, item in enumerate(line):
                if item["owner"] == color:
                    if item["xy"] in checked:
                        continue
                    count += self.checkForOpen( board, color, item["xy"] )
                    checked.append(item["xy"])
                    
        if color == "white":
            count = count * -1
        
        return count
        
        
 #counts all the blacks and whites.  
 #When there is a vertex, the values will get counted for each one, giving them a heavier weight. 
# Also gives +/- 3 for having 3 in a row.
    def firstPhaseState(self, board):
        score = board.get_black_pieces_left() - board.get_white_pieces_left()
        for line in board.get_lines():
            numinrow =0
            last = ""
            for item in line:
                if (last == item["owner"]):
                    numinrow +=1
                else :
                    numinrow = 0
                if item["owner"] == "black":
                    if numinrow == 1:
                        score = score + 1
                    if numinrow == 2:
                        score = score + 3
                elif item["owner"] == "white":
                    if numinrow == 1:
                        score = score - 1
                    if numinrow == 2:
                        score = score - 3
                last = item["owner"]  
        return score


    #if a win condition is met, gives a score of =10/-10
    #else score is a delta between types of pieces
    def secondPhaseState(self, board, previous_board, current_player_color):
        score = board.get_black_pieces_left() - board.get_white_pieces_left()

        if board.get_black_pieces_left() == 2:
            score += -100
        if board.get_white_pieces_left() == 2:
            score += 100
        return score


    def remove_piece_score(self, board, previous_board, removed_from_player_color):
        score = board.get_black_pieces_left() - board.get_white_pieces_left()
        if(self.check_n_in_a_row(board, previous_board, removed_from_player_color,2)):
            if removed_from_player_color == 'white': score+=3
            else: score-=3
        return score
    
    def check_n_in_a_row(self, previous_board, current_board, current_player_color,n):
        if not previous_board: return 0
        for xIndex, line in enumerate(previous_board.get_lines()):
            for yIndex, item in enumerate(line):
                 if item['owner'] != current_board.get_lines()[xIndex][yIndex]['owner']:
                     return self.n_in_row(current_board, item['xy'], current_player_color,n)           
        return 0
 
        
#this function checks for n in a row at a given poisition for a given player color
#it should only be called through check_three_in)a_row to check the latest player move.
    def n_in_row(self, board, position, current_player_color,n):        
        for line in board.get_lines():
            numinrow =0
            hasPosition = 0
            for item in line:
                if (current_player_color == item["owner"]):
                    numinrow +=1
                if (position == item['xy']):
                    hasPosition = 1
                if ((hasPosition == 1) and (numinrow == n)):
                    return 1
        return 0
   # def createPlayerArray(self, board):
     #   playerArray = np.zeros(board.board_size, board.board_size)


board = Board("low",0,"black",12,12,12,12,24,[
        [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
        [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}] ])

board2 = Board("low",0,"black",12,12,12,12,24,[
        [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
        [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"white"},{"xy": [3,1], "owner": "none"}] ])
