from board import Board
from reader import Reader
from heuristic import Heuristic

import copy
class Engine(object):
    """
    Engine class
    
    Takes a board and manipulates it
    """

    def __init__(self,board):
        self._board = board
        self._all_first_boards = []
    """
    Arguments: (start_x, start_y), (end_x, end_y), player color
    Returns: The updated lines where the piece has moved
    Moves a piece for player_color from the starting position to the end position.
    Color should be either 'white' or 'black'
    Example: move_piece((1,1),(1,2),"white") returns
    """
    def move_piece(self, start, end, player_color, lines = None):
        if not lines: lines = self._board.get_lines()
        start_x, start_y = start
        end_x, end_y = end
        list_of_starts = []
        list_of_ends = []
        for line in lines:
            start_position = next((item for item in line if item["xy"] == [start_x,start_y]), None)
            end_position = next((item for item in line if item["xy"] == [end_x,end_y]), None)
            #print(start_position)
            if start_position and start_position['owner'] == "none":
                return -1  #Returns error code -1 if move is illegal
            elif start_position:
                list_of_starts.append(start_position) 

            if end_position and end_position['owner'] != "none":
                return -1 #Returns error code -1 if move is illegal
            elif end_position:
                list_of_ends.append(end_position)
        if list_of_ends == [] or list_of_starts == []:
            return -1
        
        for end in list_of_ends:
            end["owner"] = player_color
        for start in list_of_starts:
            start['owner'] = "none"
        return lines




    
    """
    Arguments: list of lists containing the lines for a board, player color
    Returns: A list of lists of lists containing every possible placement of a piece as a seperate game state.

    Finds all positions that are free and returns a list of the new states for each found position.
    If no lines or player color is provided the function will use the current state of the board.

    Example: all_possible_states_for_place([[{"xy":[1,1], "owner":"none"},{"xy":[1,2], "owner":"none"}]] retruns 
    [
     [ <- start state 1
      [{'xy': [1, 1], 'owner': 'white'}, {'xy': [1, 2], 'owner': 'none'}] <- line on the board
     ], <- end state 1
     [ <- start state 2
      [{'xy': [1, 1], 'owner': 'none'}, {'xy': [1, 2], 'owner': 'white'}] <- line on the board
     ] <- end state 2
    ]
 
    """
    def all_possible_states_for_place(self, lines = None, player_color = None):
        if not lines: lines = self._board.get_lines()
        if not player_color: player_color = self._board.get_player_turn()
        free_positions = []
        for line in lines:
            free_positions += (item.copy() for item in line if item["owner"] == "none" and item not in free_positions)
        all_states = []
        for pos in free_positions:
            new_lines = []
            pos['owner'] = player_color
            for line in lines:
                new_lines.append([pos if (pos['xy'] == item['xy']) else item for item in line])
            
            all_states.append(new_lines)
        return all_states





    
    """
    Arguments: list of lists containing the lines for a board, player color
    Returns: A list of lists of lists containing every possible move of a piece as a seperate game state.
    
    Finds all possible pieces that can be removed and returns a new state for each removed piece.
    Example: 
    """
    def all_possible_states_for_move(self, lines= None, player_color = None):
        if not lines: lines = self._board.get_lines()
        if not player_color: player_color = self._board.get_player_turn()
        lines_local = copy.deepcopy(lines)
        all_states = []
        for line in lines_local:
            for index, item in enumerate(line):
                if(item['owner'] == player_color):                   
                    if index != 0 and index != len(line)-1:
                        before = line[index - 1]
                        after = line[index + 1]
                        if(before['owner'] == 'none'):
                            ret_val = self.move_piece(tuple(item['xy']),tuple(before['xy']),player_color,copy.deepcopy(lines_local))
                            if ret_val == -1: return ret_val
                            all_states.append(ret_val)
                        if(after['owner'] == 'none'):                            
                            all_states.append(self.move_piece(tuple(item['xy']),tuple(after['xy']),player_color,copy.deepcopy(lines_local)))
                    elif index == 0 and len(line) > 1:
                        after = line[index + 1]
                        if(after['owner'] == 'none'):
                            ret_val = self.move_piece(tuple(item['xy']),tuple(after['xy']),player_color,copy.deepcopy(lines_local))
                            if ret_val == -1: return ret_val
                            all_states.append(ret_val)
                    elif index == len(line) -1:
                        before = line[index - 1]
                        if(before['owner'] == 'none'):
                            ret_val = self.move_piece(tuple(item['xy']),tuple(before['xy']),player_color,copy.deepcopy(lines_local))
                            if ret_val == -1: return ret_val
                            all_states.append(ret_val)
        return all_states


    
    """
    Arguments: list of lists containing the lines for a board, player color
    Returns: A list of lists of lists containing every possible removal of piece as a seperate game state.
    
    """
    def all_possible_states_for_remove(self, lines = None, player_color = None):
        if not lines: lines = self._board.get_lines()
        if not player_color: player_color = self._board.get_player_turn()
        lines_local = copy.deepcopy(lines)
        all_positions = []
        all_states = []
        for line in lines_local:
            for index, item in enumerate(line):
                if(item['owner'] != player_color and item['owner'] != 'none' and item not in all_positions):
                    all_positions.append(item.copy())
        for pos in all_positions:
            pos['owner'] = 'none'
            new_lines = []
            for line in lines:
                new_lines.append([pos if (pos['xy'] == item['xy']) else item for item in line])
            all_states.append(new_lines)
        return all_states

    
    def minimax(self,depth, max_player, first, board, a, b, previous_board=None):
        heur = Heuristic()
        if (depth == 0):            
            if max_player == 'black':
                if board.get_black_pieces_hand() > 0:
                    return heur.firstPhaseState(board)
                else:
                    return heur.secondPhaseState(board, previous_board, 'black')
            else:
                if board.get_white_pieces_hand() > 0:
                    return heur.firstPhaseState(board)
                else:
                    value = heur.secondPhaseState(board, previous_board,'white')
                    return value
        if max_player == 'white':                
            best_value = float('inf')
            if board.get_white_pieces_hand() > 0:
                all_states = self.all_possible_states_for_place(board.get_lines(), 'white')
                for lines in all_states:
                    new_board = Board(board.get_difficulty(), board.get_turn_number(), 'black', board.get_white_pieces_hand()-1, board.get_black_pieces_hand(), board.get_white_pieces_left(),board.get_black_pieces_left(),board.get_board_size(), lines)
                    if self.check_three_in_a_row(board, new_board, 'white'):
                        new_board = self.minimax_remove(new_board, 'white')
                    value = self.minimax(depth-1, 'black', False, new_board, a, b, board)
                    best_value = min(best_value, value)
                    b = min(b, best_value)
                    if b <= a:
                        break
                    if(first):
                        new_board.set_value(best_value)
                        self._all_first_boards.append(new_board)
                return best_value
            else:
                all_states = self.all_possible_states_for_move(board.get_lines(), 'white')
                for lines in all_states:
                    new_board = Board(board.get_difficulty(), board.get_turn_number(), 'black', board.get_white_pieces_hand(), board.get_black_pieces_hand(), board.get_white_pieces_left(),board.get_black_pieces_left(),board.get_board_size(),lines)
                    if self.check_three_in_a_row(board, new_board, 'white'):
                        new_board = self.minimax_remove(new_board, 'white')
    
                    value =  self.minimax(depth-1, 'black', False, new_board,a,b, board)
                    best_value = min(best_value, value)
                    b = min(b, best_value)
                    if b <=a:
                        break
                    if(first):
                        new_board.set_value(best_value)
                        self._all_first_boards.append(new_board)

                return best_value
        if max_player == 'black':
            best_value = float('-inf')
            if board.get_black_pieces_hand() > 0:
                all_states = self.all_possible_states_for_place(board.get_lines(), 'black')
                for lines in all_states:
                    new_board = Board(board.get_difficulty(),board.get_turn_number(), 'white', board.get_white_pieces_hand(), board.get_black_pieces_hand()-1, board.get_white_pieces_left(),board.get_black_pieces_left(),board.get_board_size(),lines)
                    if self.check_three_in_a_row(board, new_board, 'black'):                        
                        new_board = self.minimax_remove(new_board, 'black')

                    value = self.minimax(depth-1, 'white', False, new_board,a,b, board)
                    best_value = max(best_value, value)
                    a = max(a, best_value)
                    if b<=a:
                        break
                    if(first):
                        new_board.set_value(best_value)
                        self._all_first_boards.append(new_board)
                
                return best_value
            else:
                all_states = self.all_possible_states_for_move(board.get_lines(), 'black')
                
                for lines in all_states:
                    new_board = Board(board.get_difficulty(), board.get_turn_number(), 'white', board.get_white_pieces_hand(), board.get_black_pieces_hand(), board.get_white_pieces_left(),board.get_black_pieces_left(),board.get_board_size(),lines)
                    if self.check_three_in_a_row(board, new_board, 'black'):
                        new_board = self.minimax_remove(new_board, 'black')
                    value = self.minimax(depth-1, 'white', False, new_board, a, b, board)
                    best_value = max(best_value, value)
                    a = max(a,best_value)
                    if b<=a:
                        break
                    if(first):
                        new_board.set_value(best_value)
                        self._all_first_boards.append(new_board)
                return best_value
    """
    Arguments: a board, player color
    Returns: a board where player color has removed on of the opponents pieces.
    This function finds a good piece to remove from the opponents and removes it from the board.
    """
    def minimax_remove(self,board, max_player):
        heur = Heuristic()
        value = 0 #float('-inf')
        best_board = board
        all_states = self.all_possible_states_for_remove(board.get_lines(), max_player)
        for lines in all_states:
            if max_player == 'white':
                new_board = Board(board.get_difficulty(),board.get_turn_number(), 'black', board.get_white_pieces_hand(), board.get_black_pieces_hand(), board.get_white_pieces_left(),board.get_black_pieces_left()-1,board.get_board_size(),lines)
                new_value = heur.remove_piece_score(new_board,board,'black')
                if new_value < value:
                    value = new_value
                    best_board = new_board
            else:
                new_board = Board(board.get_difficulty(), board.get_turn_number(),'white', board.get_white_pieces_hand(), board.get_black_pieces_hand(), board.get_white_pieces_left()-1,board.get_black_pieces_left(),board.get_board_size(),lines)
                new_value = heur.remove_piece_score(new_board, board, 'white')
                if new_value > value:
                    value = new_value
                    best_board = new_board
        return best_board

    """
    Arguments: player color
    Returns: The board with the highest or lowest value, depending on the player.
    This function gets the best board for the chosen player.
    """
    def get_best_board(self,player):
        best_board = self._all_first_boards[0]
        for board in self._all_first_boards:
            if player == 'white':

                if board.get_value() < best_board.get_value():
                    best_board = board
            else:
                if board.get_value() > best_board.get_value():
                    best_board = board
        self._all_first_boards = []
        best_board.increase_turn_number()
        return best_board

    """
    check the last state to the current state for the move and see if there is a new three in a row for the current player color.
    note: this is expecting the game state to only have the most recent move added.

    """
    def check_three_in_a_row(self, previousBoard, currentBoard, current_player_color):
        if not previousBoard: return 0
        for xIndex, line in enumerate(previousBoard.get_lines()):
            for yIndex, item in enumerate(line):
                 if item['owner'] != currentBoard._lines[xIndex][yIndex]['owner']:                 
                     return self.three_in_row(currentBoard, item['xy'], current_player_color)           
        return 0
 
        
#this function checks for three in a row at a given poisition for a given player color
#it should only be called through check_three_in)a_row to check the latest player move.
    def three_in_row(self, board, position, current_player_color):        
        for line in board.get_lines():
            numinrow =0
            hasPosition = 0
            for item in line:
                if ( current_player_color == item["owner"]):
                    numinrow +=1
                if (position == item['xy']):
                    hasPosition = 1
                if ((hasPosition == 1) and (numinrow == 3)):
                    return 1
        return 0
    

def main():
    r = Reader()
    try:
        file_name = input("JSON file name : ")
        r.read(file_name)
        board = r.board
        depth = 0
        if(board.get_difficulty() == "low"):
            depth = 4
        e = Engine(board)
        e.minimax(depth, board.get_player_turn(), True, board)
        board = e.get_best_board('white')
        r.set_board(board)
        r.write("result.json")
        print("\n")
        print(board)
        for line in board.get_lines():
            print(line)
    except OSError as oserr:
        print(oserr)
if __name__ == "__main__":
    main()
  
