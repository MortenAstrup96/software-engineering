from board import Board
from reader import Reader
import copy
class Engine(object):
    """
    Engine class

    Takes a board and manipulates it
    """

    def __init__(self,board):
        self._board = board
    """
    Arguments: (start_x, start_y), (end_x, end_y), player color
    Returns: nothing
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
                print("here")
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
    
    Finds all positions that can be moved to and returns a list of the new states for each found position.
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
            
            #(item for item in line if item['owner'] == player_color)


def main():
    r = Reader()
    try:
        file_name = input("json file name : ")
        r.read(file_name)
        board = r.board
        e = Engine(board)
        e.all_possible_states_for_place(board.get_lines())
    except OSError as oserr:
        print(oserr)
if __name__ == "__main__":
    main()

