from board import Board
from reader import Reader

class Engine(object):
    """
    Engine class

    Takes a board and manipulates it
    """

    def __init__(self,board):
        self._board = board

    def find_easy_move():
        return

    def find_medium_move():
        return

    def find_hard_move():
        return

    def move_piece(self, start, end, player_color):
        start_x, start_y = start
        end_x, end_y = end
        lines = self._board.get_lines()
        list_of_starts = []
        list_of_ends = []
        for line in lines:
            start_position = next((item for item in line if item["xy"] == [start_x,start_y]), None)
            end_position = next((item for item in line if item["xy"] == [end_x,end_y]), None)
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
            

            # if end_position and end_position['owner'] != "none":
            #     return -1
            # elif end_position:
            #     end_position['owner'] = player_color
                
            # if start_position and end_position and end_position['owner'] != "none":
            #     start_position['owner'] = "none"
                
                
        
    
    







def main():
    r = Reader()
    try:
        file_name = input("json file name : ")
        r.read(file_name)
        board = r.board
        e = Engine(board)
        e.move_piece(1,1)
    except OSError as oserr:
        print(oserr)
if __name__ == "__main__":
    main()

