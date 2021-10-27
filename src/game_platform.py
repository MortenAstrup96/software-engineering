import os
import copy
import server
import client
#from server.server.py import CommunicationServer
from board import Board
from reader import Reader
from game_engine import Engine
import sys
import time
import json
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
    NOTIFICATION = ''
    SURRENDERED = False
    SURRENDERED_PLAYER = ''
    
    def __init__(self):
        self.no_move = False
        self.player = None
        self.opponent = None
    def check_three_in_a_row(self, previousBoard, currentBoard, current_player_color):
        if not previousBoard: return 0
        for xIndex, line in enumerate(previousBoard.get_lines()):
            for yIndex, item in enumerate(line):
                 if item['owner'] != currentBoard.get_lines()[xIndex][yIndex]['owner']:
                     if self.three_in_row(currentBoard.get_lines(), item['xy'], current_player_color):
                         return 1
        return 0


    def three_in_row(self, lines, position, current_player_color, for_remove = False):
        for line in lines:
            num_in_row = 0
            has_position = 0
            already_three = False
            for index, item in enumerate(line):
                if (current_player_color == item["owner"]) and already_three:
                    return 0
                elif already_three:
                    return 1
                elif current_player_color == item['owner']:
                    num_in_row += 1
                else:
                    has_position = 0
                if (position == item['xy'] and item['owner'] == current_player_color):
                    has_position = 1

                if ((has_position == 1) and (num_in_row == 3)):
                    already_three = True
                    if index == len(line)-1: return 1
                    if for_remove: return 1

                if has_position and num_in_row > 3 and for_remove:
                    return 1
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

    def jump_piece(self, start, end, player_color, lines = None):
        if not lines: lines = self._board.get_lines()
        start_x, start_y = start
        end_x, end_y = end
        starts = []
        ends = []
        for line in lines:
            start_item = None
            end_item = None
            for item in line:
                if item['xy'] == [start_x, start_y] and item['owner'] == player_color:
                    starts.append(item)
                if item['xy'] == [end_x, end_y] and item['owner'] == 'none':
                    ends.append(item)
        if starts and ends:
            for item in starts:
                item['owner'] = 'none'
            for item in ends:
                item['owner'] = player_color
        else:
            return False
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
        return ret



    def print_board(self, board):
        os.system('clear')
        letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X"]
        name = 'black'
        if board.get_player_turn == 'black': name = 'white'
        if self.opponent: name = self.opponent['id']
        player_info = {'GamesPlayed': 0, 'GamesLeft': 1, 'NumberOfWins': 0}
        if self.player: player_info = self.player.GetPlayerInfo()
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
            if pos == 'white': positions[index] = f"\033[0;30;47m{letters[index]}\033[0;0m"
            if pos == 'black': positions[index] = f"\033[0;37;40m{letters[index]}\033[0;0m"
            if pos == 'none': positions[index] = f"\033[0;32m{letters[index]}\033[0;0m"
        [A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X] = positions
        str = "["+A+"]—————————————["+B+"]—————————————["+C+"]" + "      UU-Game\n"\
              " | \             |             / |\n"\
              " |  \            |            /  |\n"\
              " |   ["+D+"]————————["+E+"]————————["+F+"]   |" + "       Rules:\n"\
              " |    | \        |        / |    |" + "       In the first phase each player needs to place \n"\
              " |    |  \       |       /  |    |" + "       all their pieces on the board. If a player manages \n"\
              " |    |   ["+G+"]———["+H+"]———["+I+"]   |    |" + "       to get three pieces in a row they can remove a \n"\
              " |    |    |           |    |    |"+ "       piece from the opponent. Once all pieces are placed \n"\
              " |    |    |           |    |    |"+ "       they can be moved along the lines. The first player\n"\
              "["+J+"]——["+K+"]——["+L+"]         ["+M+"]——["+N+"]——["+O+"]" + "      to get down to 2 pieces loses.\n"\
              " |    |    |           |    |    |\n"\
              " |    |    |           |    |    |" + f"       Games played: {player_info['GamesPlayed']}\n"\
              " |    |   ["+P+"]———["+Q+"]———["+R+"]   |    |" + f"       Games left: {player_info['GamesLeft']}\n"\
              " |    |  /       |       \  |    |" + f"       Wins: {player_info['NumberOfWins']}\n"\
              " |    | /        |        \ |    |" + f"      {self.NOTIFICATION}\n"\
              " |   ["+S+"]————————["+T+"]————————["+U+"]   |" + f"       You are playing against {name}\n"\
              " |  /            |            \  |" + f"       Turn: {board.get_turn_number()}\n"\
              " | /             |             \ |" + f"       White left: {board.get_white_pieces_left()}  Black left: {board.get_black_pieces_left()} \n"\
              "["+V+"]—————————————["+W+"]—————————————["+X+"]"+ f"      White hand: {board.get_white_pieces_hand()}  Black hand: {board.get_black_pieces_hand()} \n"
        print(str)
        if self.no_move:
            print("No moves found, skipping turn.")
            self.no_move = False

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

                move = input("Type 'Surrender' or move location: ")
                if move == "Surrender" and self.surrender(board):
                    return False
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
                remove = input("Type Surrender or choose location to remove: ")
                if remove == "Surrender" and self.surrender(board):
                    return False
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
        e = Engine()
        if not e.all_possible_states_for_move(board.get_lines(),player):
            return False
        while not valid:
            move_start = ""
            move_end = ""
            while not move_start and not move_end:
                try:self.print_board(board)
                except:pass
                print(player.capitalize() + "'s turn")
                if invalid_text:  print("\033[0;31mInvalid move\033[0;0m")
                print("Choose location or type 'Surrender'")
                move_start = input("Move start: ")
                if move_start == "Surrender" and self.surrender(board):
                    return False
                move_end = input("Move   end: ")
                if move_end == "Surrender" and self.surrender(board):
                    return False
                move_start = self.translate_move(move_start)
                move_end = self.translate_move(move_end)
            valid = self.move_piece(move_start, move_end, player, board.get_lines())
            if not valid: invalid_text = True
        board.set_lines(valid)
        self.print_board(board)
        return True


    def ask_jump(self,board, player):
        move = ""
        valid = False
        invalid_text = False
        e = Engine()
        while not valid:
            move_start = ""
            move_end = ""
            while not move_start and not move_end:
                try:self.print_board(board)
                except:pass
                print(player.capitalize() + "'s turn")
                if invalid_text:  print("\033[0;31mInvalid move\033[0;0m")
                print("Choose location or type 'Surrender'")
                move_start = input("Move start: ")
                if move_start == "Surrender" and self.surrender(board):
                    return False
                move_end = input("Move   end: ")
                if move_end == "Surrender" and self.surrender(board):
                    return False
                move_start = self.translate_move(move_start)
                move_end = self.translate_move(move_end)
            valid = self.jump_piece(move_start, move_end, player, board.get_lines())
            if not valid: invalid_text = True
        board.set_lines(valid)
        self.print_board(board)
        return True

    
    def place_piece(self, position, player_color, board):
        lines = board.get_lines()
        lines_before = copy.deepcopy(lines)
        for line in lines:
            for item in line:
                if item['xy'] == position and item['owner'] == 'none':
                    item['owner'] = player_color

        return not lines == lines_before

    def remove_piece(self, position, player_color, board):
        lines = board.get_lines()
        lines_before = copy.deepcopy(lines)
        other_player_color = ""
        if player_color == 'white': other_player_color = 'black'
        else: other_player_color = 'white'
        available_to_remove = False

        for line in lines:
            for item in line:
                if item['owner'] == other_player_color and not self.three_in_row(lines,item['xy'],other_player_color,True):
                    available_to_remove = True
                    break

        for line in lines:
            for item in line:
                if available_to_remove and item['xy'] == position and item['owner'] == other_player_color and not self.three_in_row(lines,position,other_player_color,True):
                    item['owner'] = 'none'
                elif not available_to_remove and item['xy'] == position and item['owner'] == other_player_color:
                    item['owner'] = 'none'
        return not lines == lines_before


    def game_start(self):
        os.system('clear')
        print("Welcome to the UU-Game!")
        print("Please choose a configuration \n 1: Start server \n 2: Join server \n 3: Play local 1 vs 1 \n Press x to exit.")
        while True:
            mode = input("Mode: ")
            if mode == 'x': sys.exit()
            if mode == '1':
                self.start_server()
            if mode == '2':
                player = self.join_server()
                self.play_tournament(player)
                break
            if mode == '3': self.play_local()

    def start_server(self):
        play_num = 0
        ai_num = -1
        diff = 0
        while play_num not in range(2,9):
            try: play_num = int(input("How many players (2-8): "))
            except: pass
            if play_num not in range(2,9): print("Try again")
        
        while ai_num not in range(0,play_num+1):
            try: ai_num = int(input(f"How many AI (0-{play_num}): "))
            except: pass
            if ai_num not in range(0,play_num+1): print("Try again")
        while ai_num > 0 and diff not in range(1,4):
            print("1: low \n2: Medium \n3: High")
            try: diff = int(input("What difficulty for AI? (1-3): "))
            except: pass
            if diff not in range(1,4): print("Try again")
        if diff == 1: diff = 'low'
        if diff == 2: diff = 'medium'
        if diff == 3: diff = "high"
        communication_server = server.CommunicationServer(play_num)
        communication_server.CreateServer()
        for i in range(ai_num):
            communication_server.AddAI(diff)
            
    def play_tournament(self, player):
        name = input("Name: ")
        player.SetName(name)
        self.player = player
        while True:
            input("Press enter when ready! ")
            player.Ready()
            if player.tournamentOver:
                print("Tournament over. Thank you for playing.")
                print("Here are the final standings:")
                print(player.scoreBoard)
                player.Disconnect()
                sys.exit(0)
      
            opponent = None
            counter = 0
            while not opponent:
                os.system('clear')
                print("Waiting for opponent", counter)
                opponent = player.CurrentOpponent
                time.sleep(1)
            while opponent['id'] == 'none':
                os.system('clear')
                print("Did not find opponent this round.")
                print("Waiting for opponent")
                opponent = player.CurrentOpponent
                player.Ready()
                if player.tournamentOver:
                    print("Tournament over. Thank you for playing.")
                    print("Here are the final standings:")
                    print(player.scoreBoard)
                    player.Disconnect()
                    sys.exit(0)
      
                time.sleep(1)
                
            player_c = ""
            self.opponent = opponent
            if opponent['color'] == 'black':
                reader = Reader()
                reader.read('board.json')
                board = reader.board
                player_c = 'white'
            else:
                player_c = 'black'
                data = player.GetMessageFromOpponent(True, 300)[0]['data']
                if data == 'white':
                    print('White surrendered, black wins!')
                    print(player.scoreBoard)
                    continue
                board = Board(data["difficulty"], data["turn_number"], data["player_turn"], 
                                data["white_pieces_in_hand"], data["black_pieces_in_hand"], 
                                data["white_pieces_left"], data["black_pieces_left"],
                                data["board_size"], data["lines"])
                
            self.NOTIFICATION = ""
            self.SURRENDERED = False
            self.SURRENDERED_PLAYER = ""
            data = ""
            while board.get_black_pieces_left() > 2 and board.get_white_pieces_left() > 2 and board.get_turn_number() <= 200:
                    if self.SURRENDERED:
                        break

                    previous_board = copy.deepcopy(board)
                    if board.get_player_pieces_in_hand(player_c) > 0:
                        self.ask_place(board, player_c)
                    elif board.get_player_pieces_left(player_c) == 3:
                        self.ask_jump(board,player_c)
                    else:
                        if not self.ask_move(board, player_c):
                            self.no_move = True
                    if self.SURRENDERED:
                        break

                    if(self.check_three_in_a_row(previous_board, board, player_c)):
                        self.ask_remove(board,player_c)
                    board.increase_turn_number()
                    board.set_player_turn_opposite()
                    if board.get_black_pieces_left() < 3 or board.get_white_pieces_left() < 3:
                        break
                    player.SendInformationToOpponent(board.get_json())
                    self.print_board(board)
                    print("Waiting for opponent")
                    data = player.GetMessageFromOpponent(True, 300)[0]['data']
                    if data == 'white' or data == 'black':
                        break
                    board = Board(data["difficulty"], data["turn_number"], data["player_turn"], 
                                data["white_pieces_in_hand"], data["black_pieces_in_hand"], 
                                data["white_pieces_left"], data["black_pieces_left"],
                                data["board_size"], data["lines"])
                    self.print_board(board)

            if data == 'white' or data == 'black':
                print(data.capitalize(), "surrendered,",player_c,"wins!")
                return 
            if self.SURRENDERED_PLAYER == 'black' or board.get_black_pieces_left() < 3:
                if player.singleGameOver: print("Game over! Thank you for playing")
                print("White won")
                if self.SURRENDERED: player.SendInformationToOpponent("black")
                player.SignalVictory(2)
            elif self.SURRENDERED_PLAYER == 'white' or board.get_white_pieces_left() < 3:
                if player.singleGameOver: print("Game over! Thank you for playing")
                print("Black won")
                if self.SURRENDERED: player.SendInformationToOpponent("white")
                player.SignalVictory(1)
            else: print("It's a draw")
            if player.scoreBoard != -1:
                print(player.scoreBoard)
            if player.singleGameOver:
                player.Disconnect()
                sys.exit(0)
    def join_server(self):
        try:
            player = client.Player()

            ip = '127.0.0.1'
            port = 5000 
        
            player.ConnectToServer(ip, port)
        except:
            pass
        return player
        
    def play_local(self):
        reader = Reader()
        reader.read('board.json')
        board = reader.board
        player = 'white'

        self.NOTIFICATION = ""
        self.SURRENDERED = False
        self.SURRENDERED_PLAYER = ""

        while board.get_black_pieces_left() > 2 and board.get_white_pieces_left() > 2 and board.get_turn_number() <= 200:
            if self.SURRENDERED:
                break

            previous_board = copy.deepcopy(board)
            if board.get_player_pieces_in_hand(player) > 0:
                self.ask_place(board, player)

            elif board.get_player_pieces_left(player) == 3:
                self.ask_jump(board,player)
            else:
                if not self.ask_move(board, player):
                    self.no_move = True
            if self.SURRENDERED:
                break

            if(self.check_three_in_a_row(previous_board, board, player)):
                self.ask_remove(board,player)
            board.increase_turn_number()
            if player == 'white': player = 'black'
            else: player = 'white'

        self.print_board(board, )
        if self.SURRENDERED_PLAYER == 'black' or  board.get_black_pieces_left() < 3: print("White won")
        elif self.SURRENDERED_PLAYER == 'white' or board.get_black_pieces_left() < 3: print("Black won")
        else: print("It's a draw")

    def surrender(self, board):
        answer = input("Are you sure you want to surrender (y/n)? ")
        if answer == 'y':
            self.SURRENDERED = True
            if board.get_player_turn() == 'black':
                #board.set_black_pieces_left(0)
                #board.set_black_pieces_in_hand(0)
                self.NOTIFICATION = "White won. Black surrendered"
                self.SURRENDERED_PLAYER = 'black'
            if board.get_player_turn() == 'white':
                #board.set_white_pieces_left(0)
                #board.set_white_pieces_in_hand(0)
                self.NOTIFICATION = "Black won. White surrendered"
                self.SURRENDERED_PLAYER = 'white'
            return True

        return False


def main():
    gp = Game_Platform()
    gp.game_start()

if __name__ == "__main__":
    main()
