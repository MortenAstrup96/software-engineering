import os
import copy
class Game_Platform(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    def __init__(self):
        pass

    def translate_move(self, move):
        move = move.upper()
        ret = None
        if move == "A": ret = [1,1]
        if move == "B": ret = [4,1]
        if move == "C": ret = [7,1]
        if move == "D": ret = [2,2]
        if move == "E": ret = [4,2]
        if move == "F": ret = [6,2]
        if move == "G": ret = [3,3]
        if move == "H": ret = [4,3]
        if move == "I": ret = [5,3]
        if move == "J": ret = [1,4]
        if move == "K": ret = [2,4]
        if move == "L": ret = [3,4]
        if move == "M": ret = [5,4]
        if move == "N": ret = [6,4]
        if move == "O": ret = [7,4]
        if move == "P": ret = [3,5]
        if move == "Q": ret = [4,5]
        if move == "R": ret = [5,5]
        if move == "S": ret = [2,6]
        if move == "T": ret = [4,6]
        if move == "U": ret = [5,6]
        if move == "V": ret = [1,7]
        if move == "W": ret = [4,7]
        if move == "X": ret = [7,7]
        return ret


    
    def print_board(self, board):
        os.system('clear')
        str = "[A]--------------[B]--------------[C]\n"\
              " :                :                :\n"\
              " :                :                :\n"\
              " :    [D]--------[E]--------[F]    :\n"\
              " :     :          :          :     :\n"\
              " :     :    [G]--[H]--[I]    :     :\n"\
              " :     :     :         :     :     :\n"\
              "[J]---[K]---[L]       [M]---[N]---[O]\n"\
              " :     :     :         :     :     :\n"\
              " :     :    [P]--[Q]--[R]    :     :\n"\
              " :     :          :          :     :\n"\
              " :    [S]------- [T]--------[U]    :\n"\
              " :                :                :\n"\
              " :                :                :\n"\
              "[V]--------------[W]--------------[X]\n"
        print(str)
        A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X = None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None

        lines = board.get_lines()
        for line in lines:
            for item in line:
                if item['xy'] == [1,1]: A = item['owner']
                if item['xy'] == [4,1]: B = item['owner']
                if item['xy'] == [7,1]: C = item['owner']
                
                if item['xy'] == [2,2]: D = item['owner']
                if item['xy'] == [4,2]: E = item['owner']
                if item['xy'] == [6,2]: F = item['owner']

                if item['xy'] == [3,3]: G = item['owner']
                if item['xy'] == [4,3]: H = item['owner']
                if item['xy'] == [5,3]: I = item['owner']

                if item['xy'] == [1,4]: J = item['owner']
                if item['xy'] == [2,4]: K = item['owner']
                if item['xy'] == [3,4]: L = item['owner']

                if item['xy'] == [5,4]: M = item['owner']
                if item['xy'] == [6,4]: N = item['owner']
                if item['xy'] == [7,4]: O = item['owner']

                if item['xy'] == [3,5]: P = item['owner']
                if item['xy'] == [4,5]: Q = item['owner']
                if item['xy'] == [5,5]: R = item['owner']

                if item['xy'] == [2,6]: S = item['owner']
                if item['xy'] == [4,6]: T = item['owner']
                if item['xy'] == [6,6]: U = item['owner']

                if item['xy'] == [1,7]: V = item['owner']
                if item['xy'] == [4,7]: W = item['owner']
                if item['xy'] == [7,7]: X = item['owner']
        positions = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X]
        for index, pos in enumerate(positions):
            if pos == 'white': positions[index] = u"\u25A0"
            if pos == 'black': positions[index] = u"\u25A1"
            if pos == 'none': positions[index] = " "
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X] = positions 
        str = "["+A+"]--------------["+B+"]--------------["+C+"]\n"\
              " :                :                :\n"\
              " :                :                :\n"\
              " :    ["+D+"]--------["+E+"]--------["+F+"]    :\n"\
              " :     :          :          :     :\n"\
              " :     :    ["+G+"]--["+H+"]--["+I+"]    :     :\n"\
              " :     :     :         :     :     :\n"\
              "["+J+"]---["+K+"]---["+L+"]       ["+M+"]---["+N+"]---["+O+"]\n"\
              " :     :     :         :     :     :\n"\
              " :     :    ["+P+"]--["+Q+"]--["+R+"]    :     :\n"\
              " :     :          :          :     :\n"\
              " :    ["+S+"]------- ["+T+"]--------["+U+"]    :\n"\
              " :                :                :\n"\
              " :                :                :\n"\
              "["+V+"]--------------["+W+"]--------------["+X+"]\n"\
              f"White left: {board.get_white_pieces_left()}  Black left: {board.get_black_pieces_left()} \n"\
              f"White hand: {board.get_white_pieces_hand()}  Black hand: {board.get_black_pieces_hand()} \n"
        print(str)


    def ask_place(self,board):
        move = ""
        valid = False
        while not valid:
            move = ""
            while not move:
                self.print_board(board)
                move = input("Place: ")
                move = self.translate_move(move)
            valid = self.place_piece(move,'white',board)
        board.set_white_pieces_in_hand(board.get_white_pieces_in_hand() - 1)
        os.system('clear')
        self.print_board(board)

    def ask_remove(self,board):
        remove = ""
        valid = False
        while not valid:
            remove = ""
            while not remove:
                self.print_board(board)
                remove = input("Remove: ")
                remove = self.translate_move(remove)
            print("remove", remove)
            valid = self.remove_piece(remove, 'black', board)
        board.set_black_pieces_left(board.get_black_pieces_left()-1)
        self.print_board(board)

    def ask_move(self,board, engine):
        move = ""
        valid = False
        while not valid:
            move_start = ""
            move_end = ""
            while not move_start and not move_end:
                self.print_board(board)
                move_start = input("Move start: ")
                move_end = input("Move end: ")
                move_start = self.translate_move(move_start)
                move_end = self.translate_move(move_end)
            valid = engine.move_piece(move_start, move_end, 'white', board.get_lines())
        self.print_board(board)
        
    def place_piece(self, position, player_color, board):
        lines = board.get_lines()
        for line in lines:
            for item in line:
                if item['xy'] == position and item['owner'] != 'none': return False
                elif item['xy'] == position:
                    item['owner'] = player_color
        return True

    def remove_piece(self, position, player_color, board):
        lines = board.get_lines()
        lines_before = copy.deepcopy(lines)
        for line in lines:
            for item in line:
                if item['xy'] == position and item['owner'] == player_color:
                    item['owner'] = 'none'
    
        return not lines == lines_before
