"""
engine_exceptions.py

Software-engineering project group B

1/10/2021
v0.2


Laurent VOURIOT


Custom exceptions for the game engine
"""

class Illegal_Move_Error(Exception):
    """
    illegal_move_error class 

    this exception should be raised when someone tries to move a piece 
    that is not accessible or already occupied
    """
    def __init__(self):
        self.message_ = "you can't move this piece to this cell\n" 
    def __str__(self):
        return "[ERROR] illegal_move_error : {}".format(self.message_)

# -----------------------------------------------------------------------------

class No_More_Moves_Error(Exception):
    """
    no_more_moves_error class

    this exception should be raised when no more moves can be done the game is a draw
    """
    def __init__(self):
        self.message_ = "no more moves possible\n"
    def __str__(self):
        return "[ERROR] no_more_moves_error : {}".format(self.message_)

# -----------------------------------------------------------------------------

class Max_Round_Error(Exception):
    """
    max_round_error class 

    this exception should be raised when the maximum round limit is reached
    (200 rounds) 
    """
    def __init__(self):
        self.message_ = "maximum round limit reached\n"
    def __str__(self):
        return "[ERROR] max_round_error : {}".format(self.message_)

