#!/usr/bin/env python3

"""
Tic Tac Toe

functional approach
uses some global variables
uses excception handling

Uses None for board initialization
True for player 'x' 
False for player 'o'
"""

from typing import Optional


class UserExit(Exception):
    pass


class InvalidInput(Exception):
    pass


class InputOutOfBounds(Exception):
    pass

__version__ = '0.0.2'
__author__ = 'Alan Premselaar'

# generate a 3x3 2dimentional list initialized with None
_BOARD_ROWS = 3
_BOARD_COLS = 3

board = [
    [None for i in range(_BOARD_COLS)] for x in range(_BOARD_ROWS)
]

player_map = {
    None: '-',
    True: 'X',
    False: 'O',
}

turn = 0


def get_user_input_as_int(prompt: Optional[str]=None) -> int:
    """Gets input from the user and converts to integer.
    If the user inputs 'q' to quit, return -1

    Args:
        prompt (Optional[str], optional): A string in which to prompt the user. Defaults to None.

    Returns:
        int: 1-9 for normal usage, -1 for quit
    """

    prompt = prompt or 'Please enter a position 1 through 9 or "q" to quit'

    input_string = input(f'{prompt}: ')

    # check for quit
    if input_string.casefold() == 'q':
        raise UserExit()

    # validate the input
    if not input_string.isnumeric():
        raise InvalidInput("Not a valid number. Please select a number from 1 to 9")

    input_num = int(input_string)

    if input_num < 1 or input_num > 9:
        raise InputOutOfBounds("Input out of bounds. Please select a number from 1 to 9")

    # passed validation so return the number
    return input_num


    
def linear_position_to_coords(position: int) -> tuple[int, int]:
    """converts a linear position number (1-9) to 2D list coordinates

    Args:
        position (int): a number from 1 to 9

    Returns:
        tuple[int, int]: the resulting coordinates
    """
    position -= 1       # convert 1-9 to 0-8

    row = position // 3
    col = position

    if col > 2:
        col = int(col % 3)

    return row, col
    

def is_taken(coords: tuple[int, int]) -> bool:
    """determines if the cell in boards[coords] is not None

    Args:
        coords (tuple[int, int]): The 2D coordinates

    Returns:
        bool: True if value is not None, False otherwise
    """
    row, col = coords

    return board[row][col] is not None

    
def display_board() -> None:
    print("")
    for row in range(_BOARD_ROWS):
        for col in range(_BOARD_COLS):
            print(player_map[board[row][col]], end=' ')
        print("")
    print("")

def add_to_board(coords: tuple[int, int], player: bool) -> None:
    row, col = coords
    board[row][col] = player


def check_rows(player: bool) -> bool:
    for row in board:
        retval = True
        
        for cell in row:
            if cell != player:
                retval = False
                break
            
        if retval:
            return True
            
    return retval


def check_cols(player: bool) -> bool:
    for col in range(_BOARD_COLS):
        retval = True
        
        for row in range(_BOARD_ROWS):
            if board[row][col] != player:
                retval = False
                break
            
        if retval:
            return retval

    return retval


def check_diags(player: bool) -> bool:
    if not board[1][1] == player:
        # can't win on diags if not in the center of the board
        return False

    if board[0][0] == board[2][2] == player or board[0][2] == board[2][0] == player:
        return True

    return False


def check_tie() -> bool:
    global turn
    
    turn += 1

    return turn == _BOARD_ROWS * _BOARD_COLS
        

def chicken_dinner(player: bool) -> bool:
    """determines if there's a win

    Args:
        player (bool): The current player

    Returns:
        bool: True if win, False otherwise
    """
    return check_rows(player) or check_cols(player) or check_diags(player)

    
def main() -> None:
    player = True
    
    while True:
        display_board()
        
        try:
            location = get_user_input_as_int(f'[Player {player_map[player]}] enter a position 1-9 or "q" to quit')
            coords = linear_position_to_coords(location)

            # if the location is already taken, then prompt again
            if is_taken(coords):
                print("Please try again.")
                continue

            add_to_board(coords, player)
            
            if chicken_dinner(player):
                print(f"Player {player_map[player]} wins!")
                display_board()
                break

            if check_tie():
                print(f"TIE! No one wins!")
                display_board()
                break
            
            player = not player
            
        except UserExit as e:
            print("Thank you for playing.")
            break
        except (InvalidInput, InputOutOfBounds) as e:
            print(e)
            


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nExiting...")