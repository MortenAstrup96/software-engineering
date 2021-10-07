"""
test_board.py

Software-engineering project group B 

01/10/2021

v0.1

Laurent VOURIOT
"""

import unittest
import sys
import os
 
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
    
from engine_errors import Max_Round_Error
from board import Board

class test_board(unittest.TestCase):
    def test_get_owner(self):
        """
        test the function to get a the owner of a cell
        expected output : owners black white and no owner should be found 
        """
        board = Board("low",0,"black",12,12,12,12,24,[
            [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
            [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}]])

        self.assertEqual("black", board.get_owner([1,1]))
        self.assertEqual("white", board.get_owner([1,2]))
        self.assertEqual("none", board.get_owner([3,1]))


    def test_max_turn(self):
        """
        test if an error is raised when the max turn number is reached
        excpected out come : max_turn_error is caught
        """
        with self.assertRaises(Max_round_error):
            board = Board("low",201,"black",12,12,12,12,24,[
            [{"xy":[1,1], "owner": "black"},{"xy":[1,2], "owner":"white"},{"xy":[1,3], "owner":"none"}],
            [{"xy":[1,1], "owner": "black"},{"xy":[2,1], "owner":"none"},{"xy": [3,1], "owner": "none"}]])

        

if __name__ == '__main__':
    unittest.main()
