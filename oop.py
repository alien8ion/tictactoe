#!/usr/bin/env python3

"""
Command line Tic Tac Toe

uses OOP approach
uses Exception handling
uses Enum for Player values including board initialization
"""

from enum import Enum
from typing import Optional


__version__ = '0.0.3'
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
    PRIMARY = 'X'
    SECONDARY = 'O'

        
class Players:
    """Wrapper for Players management (tracking and switching current player)
    """
    
    _current = True
    _players = (Player.SECONDARY, Player.PRIMARY)


    @classmethod
    def switch(cls) -> Player:
        cls._current = not cls._current
        return cls._players[cls._current]

    @classmethod
    def current(cls) -> Player:
        return cls._players[cls._current]
    

class Board:
    _ROWS = 3
    _COLS = 3

    def __init__(self) -> None:
        self.grid = [[Player.EMPTY for i in range(self._COLS)] for x in range(self._ROWS)]
        self.turn = 0

    def get_coords(self, position: int) -> tuple[int, int]:
        """converts a linear position number (1-9) to 2D list coordinates

        Args:
            position (int): a number from 1 to 9

        Returns:
            tuple[int, int]: the rsulting coordinates
        """
        position -= 1       # convert 1-9 to 0-8

        row = position // 3
        col = position

        if col > 2:
            col = int(col %3)

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
        for row in range(self._ROWS):
            for col in range(self._COLS):
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
        for row in self.grid:
            checked_full_row = True

            for cell in row:
                if cell != player:
                    checked_full_row = False
                    break

            if checked_full_row:
                return True

        return False
            
    def _check_cols(self, player: Player) -> bool:
        """Check each column for winning placement

        Args:
            player (Player): the player to check for

        Returns:
            bool: True if full column match of any column, False if no winning columns.
        """
        for col in range(self._COLS):
            checked_full_col = True
            
            for row in range(self._ROWS):
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
        if not self.grid[1][1] == player:
            # can't win on diags if not in the center of the board
            return False

        if self.grid[0][0] == self.grid[2][2] == player or self.grid[0][2] == self.grid[2][0] == player:
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
            raise WinnerWinnerChickenDinner(f"Player {player.value} wins!")
        
    def is_tie(self) -> None:
        """Checks if there is a Tie (e.g. no winner)

        Raises:
            YouAllLose: This is a tie.
        """
        self.turn += 1

        retval = self.turn == self._ROWS * self._COLS

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
        raise InputOutOfBounds("Inpute out of bounds.")

    # passed validation so return the number
    return input_num

    
def main() -> None:
    # initialize the player and the board
    current_player = Players.current()
    board = Board()

    while True:
        board.display()

        try:
            location = get_user_input(f'[Player {current_player.value}] enter a position 1-9 or "q" to quit')

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