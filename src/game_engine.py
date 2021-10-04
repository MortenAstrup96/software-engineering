from board import Board
from reader import Reader
from heuristic import Heuristic
from game_platform import Game_Platform
import cProfile
import copy
import os
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
        moves = []
        for line in lines:
            start_item = None
            end_item = None
            for item in line:
                if item['xy'] == [start_x, start_y]:
                    start_item = item
                if item['xy'] == [end_x, end_y]:
                    end_item = item
            if start_item and end_item and start_item != end_item and start_item['owner'] == player_color and end_item['owner'] == 'none':
                moves.append([start_item,end_item])

        if not moves: return False

        for line in lines:
            for item in line:
                for move in moves:
                    if item['xy'] == move[1]['xy']: item['owner'] = player_color
                    elif item['xy'] == move[0]['xy']: item['owner'] = 'none'

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
        lines_local = lines
        all_states = []
        for line in lines_local:
            for index, item in enumerate(line):
                if(item['owner'] == player_color):                   
                    if index != 0 and index != len(line)-1:
                        before = line[index - 1]
                        after = line[index + 1]
                        if(before['owner'] == 'none'):
                            ret_val = self.move_piece(tuple(item['xy']),tuple(before['xy']),player_color,copy.deepcopy(lines_local))
                            if not ret_val: return ret_val
                            all_states.append(ret_val)
                        if(after['owner'] == 'none'):
                            ret_val = self.move_piece(tuple(item['xy']),tuple(after['xy']),player_color,copy.deepcopy(lines_local))
                            if not ret_val: return ret_val
                            all_states.append(ret_val)
                    elif index == 0 and len(line) > 1:
                        after = line[index + 1]
                        if(after['owner'] == 'none'):
                            ret_val = self.move_piece(tuple(item['xy']),tuple(after['xy']),player_color,copy.deepcopy(lines_local))
                            if not ret_val: return ret_val
                            all_states.append(ret_val)
                    elif index == len(line) -1:
                        before = line[index - 1]
                        if(before['owner'] == 'none'):
                            ret_val = self.move_piece(tuple(item['xy']),tuple(before['xy']),player_color,copy.deepcopy(lines_local))
                            if not ret_val: return ret_val
                            all_states.append(ret_val)
        return all_states


    
    """
    Arguments: list of lists containing the lines for a board, player color
    Returns: A list of lists of lists containing every possible removal of piece as a seperate game state.
    
    """
    def all_possible_states_for_remove(self, lines = None, player_color = None):
        if not lines: lines = self._board.get_lines()
        if not player_color: player_color = self._board.get_player_turn()
        lines_local = lines#copy.deepcopy(lines)
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
                    return heur.firstPhaseState(board, previous_board, 'black')
                else:
                    return heur.secondPhaseState(board, previous_board, 'black')
            else:
                if board.get_white_pieces_hand() > 0:
                    return heur.firstPhaseState(board, previous_board, 'white')
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
                    if(first):
                        new_board.set_value(value)
                        self._all_first_boards.append(new_board)
                        
                    if b<=a:
                        break
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
                    if(first):
                        new_board.set_value(value)
                        self._all_first_boards.append(new_board)
                    if b<=a:
                        break
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
                    if(first):
                        new_board.set_value(value)
                        self._all_first_boards.append(new_board)
                    if b<=a:
                        break
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
                    if(first):
                        new_board.set_value(value)
                        self._all_first_boards.append(new_board)
                        
                    if b<=a:
                        break
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
                 if item['owner'] != currentBoard.get_lines()[xIndex][yIndex]['owner']:                 
                     return self.three_in_row(currentBoard, item['xy'], current_player_color)           
        return 0
 
        
#this function checks for three in a row at a given poisition for a given player color
#it should only be called through check_three_in_a_row to check the latest player move.
    def three_in_row(self, board, position, current_player_color):        
        for line in board.get_lines():
            numinrow = 0
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
        #file_name = input("JSON file name : ")
        file_name = "board.json"
        r.read(file_name)
        board = r.board
        depth = 0
        diff = 0
        while diff not in [1,2,3]:
            os.system('clear')
            print("Welcome to the Nine men's morris game!")
            print("Difficulty mode [low = 1, medium = 2, high = 3]\n")
            diff = input("Mode: ")
            try: diff = int(diff)
            except: pass
        depth = diff*2
        gp = Game_Platform()
        player = 'white'
        while board.get_black_pieces_left() > 2 and board.get_white_pieces_left() > 2:
            gp.print_board(board)
            engine = Engine(board)
                    
            previous_board = copy.deepcopy(board)
            if(board.get_white_pieces_hand() > 0):
                gp.ask_place(board)
            else:
                gp.ask_move(board, engine)
    
            if(engine.check_three_in_a_row(previous_board, board, "white")):
                gp.ask_remove(board)
            
            board.increase_turn_number()
            board.set_player_turn = 'black'
            engine.minimax(depth,'black', True, board, float('-inf'), float('inf'))
            board = engine.get_best_board(player)

        if board.get_black_pieces_left() < 3: print("White won")
        else: print("Black won")
    except OSError as oserr:
        print(oserr)

if __name__ == "__main__":
    main()
   # cProfile.run('main()')
  
