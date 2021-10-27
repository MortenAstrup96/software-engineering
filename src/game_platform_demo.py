import os
import copy
from board import Board
from reader import Reader
import sys
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

    def check_three_in_a_row(self, previousBoard, currentBoard, current_player_color):
        if not previousBoard: return 0
        for xIndex, line in enumerate(previousBoard.get_lines()):
            for yIndex, item in enumerate(line):
                 if item['owner'] != currentBoard.get_lines()[xIndex][yIndex]['owner']:
                     if self.three_in_row(currentBoard, item['xy'], current_player_color):
                         return 1
        return 0
 
        
    def three_in_row(self, board, position, current_player_color):
        for line in board.get_lines():
            numinrow = 0
            hasPosition = 0
            already_three = False
            for index, item in enumerate(line):
                if (current_player_color == item["owner"]) and already_three:
                    return 0
                elif already_three:
                    return 1
                elif current_player_color == item['owner']:
                    numinrow += 1
                else:
                    hasPosition = 0
                if (position == item['xy'] and item['owner'] == current_player_color):
                    hasPosition = 1
             
                if ((hasPosition == 1) and (numinrow == 3)):
                    already_three = True
                    if index == len(line)-1: return 1

        return 0

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
        if move == "U": ret = [6,6]
        if move == "V": ret = [1,7]
        if move == "W": ret = [4,7]
        if move == "X": ret = [7,7]
        if move == "Y": ret = [4,4]
        return ret


    
    def print_board(self, board):
        os.system('clear')
        letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y"]

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
                if item["xy"] == [4,4]: Y = item['owner']
        positions = [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y]
        for index, pos in enumerate(positions):
            if pos == 'white': positions[index] = f"\033[0;30;47m{letters[index]}\033[0;0m"
            if pos == 'black': positions[index] = f"\033[0;37;40m{letters[index]}\033[0;0m"
            if pos == 'none': positions[index] = f"\033[0;32m{letters[index]}\033[0;0m"
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y] = positions
        str = "["+A+"]—————————————["+B+"]—————————————["+C+"]" + "      UU-Game\n"\
              " | \             |             / |\n"\
              " |  \            |            /  |\n"\
              " |   ["+D+"]————————["+E+"]————————["+F+"]   |" + "       Rules:\n"\
              " |    |          |          |    |" + "       In the first phase each player needs to place \n"\
              " |    |          |          |    |" + "       all their pieces on the board. If a player manages \n"\
              " |    |   ["+G+"]———["+H+"]———["+I+"]   |    |" + "       to get three pieces in a row they can remove a \n"\
              " |    |    | \   |   / |    |    |"+ "       piece from the opponent. Once all pieces are placed \n"\
              " |    |    |  \  |  /  |    |    |"+ "       they can be moved along the lines. The first player\n"\
              "["+J+"]——["+K+"]——["+L+"]———["+Y+"]———["+M+"]——["+N+"]——["+O+"]" + "      to get down to 2 pieces loses.\n"\
              " |    |    |  /  |  \  |    |    |\n"\
              " |    |    | /   |   \ |    |    |\n"\
              " |    |   ["+P+"]———["+Q+"]———["+R+"]   |    |\n"\
              " |    |          |          |    |\n"\
              " |    |          |          |    |\n"\
              " |   ["+S+"]————————["+T+"]————————["+U+"]   |\n"\
              " |  /            |            \  |" + f"       Turn: {board.get_turn_number()}\n"\
              " | /             |             \ |" + f"       White left: {board.get_white_pieces_left()}  Black left: {board.get_black_pieces_left()} \n"\
              "["+V+"]—————————————["+W+"]—————————————["+X+"]"+ f"      White hand: {board.get_white_pieces_hand()}  Black hand: {board.get_black_pieces_hand()} \n"
             
              
        print(str)


    def ask_place(self,board,player):
        move = ""
        valid = False
        invalid_text = False
        while not valid:
            move = ""
            while not move:
                self.print_board(board)
                print(player.capitalize() + "'s turn")
                if invalid_text: print("\033[0;31mInvalid move\033[0;0m")
                move = input("Place: ")
                move = self.translate_move(move)
            valid = self.place_piece(move,player,board)
            if not valid: invalid_text = True
        if player == 'white': board.set_white_pieces_in_hand(board.get_white_pieces_in_hand() - 1)
        else: board.set_black_pieces_in_hand(board.get_black_pieces_in_hand() - 1)
        self.print_board(board)

    def ask_remove(self,board, player):
        remove = ""
        valid = False
        invalid_text = False
        
        while not valid:
            remove = ""
            while not remove:
                self.print_board(board)
                print(player.capitalize() + "'s turn")
                if invalid_text:  print("\033[0;31mInvalid move\033[0;0m")
                remove = input("Remove: ")
                remove = self.translate_move(remove)
            valid = self.remove_piece(remove, player, board)
            if not valid: invalid_text = True
        if player == 'black': board.set_white_pieces_left(board.get_white_pieces_left() - 1)
        else: board.set_black_pieces_left(board.get_black_pieces_left() - 1)

        self.print_board(board)

    def ask_move(self,board, player):
        move = ""
        valid = False
        invalid_text = False
        while not valid:
            move_start = ""
            move_end = ""
            while not move_start and not move_end:
                try:self.print_board(board)
                except:pass
                print(player.capitalize() + "'s turn")
                if invalid_text:  print("\033[0;31mInvalid move\033[0;0m")
                move_start = input("Move start: ")
                move_end = input("Move   end: ")
                move_start = self.translate_move(move_start)
                move_end = self.translate_move(move_end)
            valid = self.move_piece(move_start, move_end, player, board.get_lines())
            if not valid: invalid_text = True
        board.set_lines(valid)
        self.print_board(board)
        
    def place_piece(self, position, player_color, board):
        lines = board.get_lines()
        for line in lines:
            for item in line:
                if item['xy'] == position and item['owner'] != 'none':
                    return False
                if item['xy'] == position:
                    item['owner'] = player_color
                    
        return True

    def remove_piece(self, position, player_color, board):
        lines = board.get_lines()
        lines_before = copy.deepcopy(lines)
        for line in lines:
            for item in line:
                if item['xy'] == position and item['owner'] != player_color and item['owner'] != 'none':
                    item['owner'] = 'none'
    
        return not lines == lines_before
        
        
    def game_start(self):
        os.system('clear')
        print("Welcome to the UU-Game!")
        print("Please choose a configuration \n 1: Start server \n 2: Join server \n 3: Play local 1 vs 1 \n Press x to exit.")
        while True:
            mode = input("Mode: ")
            if mode == 'x': sys.exit()
            if mode == '1': pass
            if mode == '2': pass
            if mode == '3': self.play_local()

    def play_local(self):
        reader = Reader()
        reader.read('board_demo.json')
        board = reader.board
        player = 'white'
        while board.get_black_pieces_left() > 0 and board.get_white_pieces_left() > 0 and board.get_turn_number() <= 200:
            previous_board = copy.deepcopy(board)
            if board.get_player_pieces_in_hand(player) > 0:
                self.ask_place(board, player)
            else:
                self.ask_move(board, player)
                
            if(self.check_three_in_a_row(previous_board, board, player)):
                self.ask_remove(board,player)
            board.increase_turn_number()
            if player == 'white': player = 'black'
            else: player = 'white'

        gp.print_board(board)
        if board.get_black_pieces_left() < 3: print("White won")
        elif board.get_black_pieces_left() < 3: print("Black won")
        else: print("It's a draw")



def main():
    gp = Game_Platform()
    gp.game_start()
    
if __name__ == "__main__":
    main()
