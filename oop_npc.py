#!/usr/bin/env python3

"""
Command line Tic Tac Toe

This is an example for tutorial purposes, meant to demonstrate some basic and intermediate
approaches to aspects of the game.

This exmample demonstrates the use of exception handling, Enums and an Object Orients approach. 

An Enum is used to populate the game board. The Enum has 3 attributes, one to represent an empty board cell, 
one to represent the player and one to represent the computer.

The Players class is used more organizationally to manage the current player.

The Board class is used for functional organization with methods that are relevant to the board.

Player input and computer position selection is handled in functions.

"""

import random
from enum import Enum
from typing import Optional


__version__ = '0.0.5'
__author__ = 'Alan Premselaar'


# !Exceptions
class UserExit(Exception):
    pass


class InvalidInput(Exception):
    pass


class InputOutOfBounds(Exception):
    pass


class WinnerWinnerChickenDinner(Exception):
    pass

class YouAllLose(Exception):
    pass


class Player(Enum):
    EMPTY = '-'
    PLAYER = 'X'
    COMPUTER = 'O'

        
class Players:
    """Wrapper for Players management (tracking and switching current player)
    """
    
    _current = True
    _players = (Player.COMPUTER, Player.PLAYER)


    @classmethod
    def switch(cls) -> Player:
        cls._current = not cls._current
        return cls.current()

    @classmethod
    def current(cls) -> Player:
        return cls._players[cls._current]
    

class Board:
    _SIZE = 3       # this should always be 3 for Tic Tac Toe

    def __init__(self) -> None:
        self.grid = [[Player.EMPTY for i in range(self._SIZE)] for x in range(self._SIZE)]
        self.turn = 0

    def get_coords(self, position: int) -> tuple[int, int]:
        """converts a linear position number (1-9) to 2D list coordinates

        Args:
            position (int): a number from 1 to 9

        Returns:
            tuple[int, int]: the rsulting coordinates
        """
        position -= 1       # convert 1-9 to 0-8

        row = position // self._SIZE
        col = position

        if col > 2:
            col = int(col % self._SIZE)

        return row, col
        
    def add(self, position: int, player: Player) -> None:
        """add a player to the board

        Args:
            position (int): the linear position (1-9) to add the player
            player (Player): the player
        """
        row, col = self.get_coords(position)
        self.grid[row][col] = player

    def display(self) -> None:
        """Display the grid
        """
        print("")
        for row in range(self._SIZE):
            for col in range(self._SIZE):
                print(self.grid[row][col].value, end=' ')
            print("")
        print("")

    # validations
    def _check_rows(self, player: Player) -> bool:
        """Check each row for winning placement

        Args:
            player (Player): the player to check for

        Returns:
            bool: True if full row match of any row, False if no winning rows.
        """
        if [player] * Board._SIZE in self.grid:
            return True
        
        return False
            
    def _check_cols(self, player: Player) -> bool:
        """Check each column for winning placement

        Args:
            player (Player): the player to check for

        Returns:
            bool: True if full column match of any column, False if no winning columns.
        """
        for col in range(self._SIZE):
            checked_full_col = True
            
            for row in range(self._SIZE):
                if self.grid[row][col] != player:
                    checked_full_col = False
                    break

            if checked_full_col:
                return True

        return False

    def _check_diags(self, player: Player) -> bool:
        """Check diagonal winning placements

        Args:
            player (Player): the player to check for

        Returns:
            bool: True if either diagonal winning placements, False otherwise
        """
        center_point = Board._SIZE // 2
        corner = Board._SIZE - 1
        
        if not self.grid[center_point][center_point] == player:
            # can't win on diags if not in the center of the board
            return False

        if self.grid[0][0] == self.grid[corner][corner] == player or self.grid[0][corner] == self.grid[corner][0] == player:
            return True

        return False

    def is_winner(self, player: Player) -> None:
        """Check to see if this player is a winner.

        Args:
            player (Player): The player to check winning status for

        Raises:
            WinnerWinnerChickenDinner: If the player is the winner
        """
        retval = self._check_rows(player) or self._check_cols(player) or self._check_diags(player)

        if retval:
            raise WinnerWinnerChickenDinner(f"{player.name} wins!")
        
    def is_tie(self) -> None:
        """Checks if there is a Tie (e.g. no winner)

        Raises:
            YouAllLose: This is a tie.
        """
        self.turn += 1

        retval = self.turn == self._SIZE * self._SIZE

        if retval:
            raise YouAllLose("Tie! No one wins!")

    def is_taken(self, position: int) -> bool:
        """Checks if a grid position already contains a player

        Args:
            position (int): The linear position (1-9) in the grid to check

        Returns:
            bool: True if player already in this location, False otherwise.
        """
        row, col = self.get_coords(position)

        return self.grid[row][col] is not Player.EMPTY
    

def get_user_input(prompt: Optional[str]=None) -> int:
    """Get input from the user

    Args:
        prompt (Optional[str], optional): A string to present to the user as a prompt. Defaults to None.

    Raises:
        UserExit: The user chose to exit
        InvalidInput: The user provided invalid input values
        InputOutOfBounds: The number is < 1 or > 9

    Returns:
        int: The user input number
    """

    prompt = prompt or 'Please enter a position 1 through 9 or "q" to quit'

    input_string = input(f"{prompt}: ")

    # check for quit
    if input_string.casefold() == 'q':
        raise UserExit()

    # validate the input
    if not input_string.isnumeric():
        raise InvalidInput("Not a valid number.")

    input_num = int(input_string)

    if not 1 <= input_num <= 9:
        raise InputOutOfBounds("Input out of bounds.")

    # passed validation so return the number
    return input_num

def get_location(board: Board, player: Player) -> int:

    if player is Player.COMPUTER:
        location = random.randint(1, 9)

        while board.is_taken(location):
            location = random.randint(1, 9)
            
        print(f"{player.name} has chosen a position of {location}")
        return location

    return get_user_input(f'[{player.name}] Enter a position 1-9 or "q" to quit')


def main() -> None:
    # initialize the player and the board
    current_player = Players.current()
    board = Board()

    while True:
        board.display()

        try:
            location = get_location(board, current_player)

            # if the location is already taken, then prompt again
            if board.is_taken(location):
                print("Please try again.")
                continue

            board.add(location, current_player)

            # check for chicken dinner
            board.is_winner(current_player)

            # check for tie
            board.is_tie()

            # switch players
            current_player = Players.switch()

        except UserExit:
            print("Thank you for playing.")
            break
        except (InvalidInput, InputOutOfBounds) as e:
            print(e)
        except (WinnerWinnerChickenDinner, YouAllLose) as e:
            print(e)
            board.display()
            break
        

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nExiting...")