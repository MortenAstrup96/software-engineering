"""
reader.py

Software-engineering project group B

14/09/2021
v0.1

Laurent VOURIOT
"""

import json
import os.path  # exists

from board import Board


class Reader(object):
    """
    Reader class

    reads a json file and create the corresponding board object
    """

    def __init__(self):
        self._board = None

    def read(self, file_name):
        """
        read a json file to create a board object
        :param (string) file_name:
        :return: (Board)
        """

        # check if the path of the file has no errors
        if not os.path.exists(file_name):
            raise OSError("invalid file path")

        # open the file then read the json data in order to create the object
        file = open(file_name, 'r')
        data = json.load(file)
        self._board = Board(data["difficulty"], data["player_turn"], data["white_pieces_in_hand"],
                            data["black_pieces_in_hand"], data["white_pieces_left"], data["black_pieces_left"],
                            data["board_size"], data["lines"])
        file.close()

    @property
    def board(self):
        """
        :return: (board) property
        """
        return self._board


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    r = Reader()
    try:
        file_name = input("json file name : ")
        r.read(file_name)
    except OSError as oserr:
        print(oserr)

    print(repr(r.board))
