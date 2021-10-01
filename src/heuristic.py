import sys
import os
import json
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import os.path  # 
from collections import defaultdict
from board import Board


#going to analyze everything with the more positive number being a better move for black; 
#negative better for white.

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

#This is called by findEachBlockedPiece.  It is checking for a block.  Could be progressed further as at this point is just testing for single blocks.
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
                        
#This will check for each spot of one color and identify if it is blocked in.  It will make the value negative if black is blocked in.
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
                    
        if color == "black":
            count = count * -1
        
        return count
        
        
#This calls the other functions and adds a weight toeach one unique for first phase. .  
    def firstPhaseState(self, board):
       score = 0
       score = 1 * self.findEachBlockedPiece(board, "black") + 1 * self.findEachBlockedPiece(board, "white") + 0* self.winningState(board) + 9 * self.numberOfPieces(board) + 26 * self.numberOfMorris(board)
       return score


#This calls the other functions and adds a weight toeach one unique for first phase. .  

    def secondPhaseState(self, board, previous_board, current_player_color):
        score = 0
        score = 10 * self.findEachBlockedPiece(board, "black") + 10 * self.findEachBlockedPiece(board, "white") + 1086* self.winningState(board) + 11 * self.numberOfPieces(board) + 43 * self.numberOfMorris(board)
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


#simple testing boards for Jenn
#board = Board("low",0,"black",12,10,12,10,24,[
#        [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
#        [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"white"},{"xy": [3,1], "owner": "none"}] ])

#board2 = Board("low",0,"black",12,12,12,12,24,[
#        [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"black"},{"xy":[1,3], "owner":"black"}],
#        [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"black"},{"xy": [3,1], "owner": "black"}] ])
