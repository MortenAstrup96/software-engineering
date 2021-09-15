import json

def read_board_file(filename):
    f = open(filename, 'r')
    return f

def read_json_from_file(f):
    board_data = json.load(f)
    return board_data

def generate_board(board_lines, board_size):
    printable_board = ""
    for y in range(board_size):
        for x in range(board_size):
            printable_board += "+---"
            if(x == board_size-1):
                printable_board += "+"
        printable_board += "\n"
        for x in range(board_size):
            printable_board += "|   "
            if(x == board_size-1):
                printable_board += "|"                
        printable_board += "\n"
    for x in range(board_size):
        printable_board += "+---"
        if(x == board_size-1):
            printable_board += "+"
    printable_board += "\n"
    print(printable_board)
    return
def main():
    f = read_board_file("test.json")
    board_data = read_json_from_file(f)
    generate_board(board_data['lines'],board_data['board_size'])

if __name__ == "__main__":
    main()

