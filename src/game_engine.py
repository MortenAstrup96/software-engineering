import json

def read_board_file(filename):
    f = open(filename, 'r')
    return f

def read_json_from_file(f):
    board_data = json.load(f)
    return board_data

def main():
    f = read_board_file("test.json")
    board_data = read_json_from_file(f)
    

if __name__ == "__main__":
    main()

