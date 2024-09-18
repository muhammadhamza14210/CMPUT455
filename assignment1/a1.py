# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification here: https://webdocs.cs.ualberta.ca/~mmueller/courses/cmput455/assignments/a1.html

import sys
import random 
class CommandInterface:
    # The following is already defined and does not need modification
    # However, you may change or add to this code as you see fit, e.g. adding class variables to init

    def __init__(self):
        # Define the string to function command mapping
        self.command_dict = {
            "help" : self.help,
            "game" : self.game,
            "show" : self.show,
            "play" : self.play,
            "legal" : self.legal,
            "genmove" : self.genmove,
            "winner" : self.winner
        }
        self.board = None
        self.current_player = 1
        self.n = None 
        self.m = None 

    # Convert a raw string to a command and a list of arguments
    def process_command(self, str):
        str = str.lower().strip()
        command = str.split(" ")[0]
        args = [x for x in str.split(" ")[1:] if len(x) > 0]
        if command not in self.command_dict:
            print("? Uknown command.\nType 'help' to list known commands.", file=sys.stderr)
            print("= -1\n")
            return False
        try:
            return self.command_dict[command](args)
        except Exception as e:
            print("Command '" + str + "' failed with exception:", file=sys.stderr)
            print(e, file=sys.stderr)
            print("= -1\n")
            return False
        
    # Will continuously receive and execute commands
    # Commands should return True on success, and False on failure
    # Commands will automatically print '= 1' at the end of execution on success
    def main_loop(self):
        while True:
            str = input()
            if str.split(" ")[0] == "exit":
                print("= 1\n")
                return True
            if self.process_command(str):
                print("= 1\n")

    # List available commands
    def help(self, args):
        for command in self.command_dict:
            if command != "help":
                print(command)
        print("exit")
        return True

    #======================================================================================
    # End of predefined functionality. You will need to implement the following functions.
    # Arguments are given as a list of strings
    # We will only test error handling of the play command
    #======================================================================================

    def game(self, args):
        if len(args) != 2:
            print("= illegal move: wrong number of arguments")
            return False

        try:
            self.n, self.m = int(args[0]), int(args[1])
        except ValueError:
            print("= illegal move: wrong coordinate")
            return False

        if not (1 <= self.n <= 20 and 1 <= self.m <= 20):
            print("= illegal move: dimensions out of bounds")
            return False

        # Initialize the board
        self.board = [["." for _ in range(self.n)] for _ in range(self.m)]
        self.current_player = 1 
        return True
    
    def show(self, args):
        if self.board is None:
            print("= no game in progress")
            return False

        for row in self.board:
            print("".join(row))
        return True

    
    def play(self, args):
        # 1. Check wrong number of arguments
        if len(args) != 3:
            print(f"= illegal move: {' '.join(args)} wrong number of arguments")
            return False

        # 2. Check if the first coordinate is an integer and valid
        try:
            x = int(args[0])
        except ValueError:
            print(f"= illegal move: {' '.join(args)} wrong coordinate")
            return False

        # 3. Check if the second coordinate is an integer and valid
        try:
            y = int(args[1])
        except ValueError:
            print(f"= illegal move: {' '.join(args)} wrong coordinate")
            return False

        # 4. Check if the coordinates are in bounds
        if not (0 <= x < self.n) or not (0 <= y < self.m):
            print(f"= illegal move: {' '.join(args)} wrong coordinate")
            return False

        # 5. Check if the third argument is either '0' or '1'
        if args[2] not in ['0', '1']:
            print(f"= illegal move: {' '.join(args)} wrong number")
            return False

        # 6. Check if the cell is already occupied
        if self.board[y][x] != '.':
            print(f"= illegal move: {' '.join(args)} occupied")
            return False

        # 7. Check the triples constraint (no 000 or 111)
        if not self.check_triples_constraint(x, y, args[2]):
            print(f"= illegal move: {' '.join(args)} three in a row")
            return False

        # 8. Check the balance constraint (number of 0's or 1's exceeds half of row/column length)
        if not self.check_balance_constraint(x, y, args[2]):
            print(f"= illegal move: {' '.join(args)} too many {args[2]}")
            return False

        # If all checks pass, place the digit on the board
        self.board[y][x] = args[2]
        self.current_player = 2 if self.current_player == 1 else 1  # Alternate the player
        return True


    def check_triples_constraint(self, x, y, digit):
        # Check the row for triples (000 or 111)
        row = self.board[y]
        new_row = row[:x] + [digit] + row[x+1:]
        if '000' in ''.join(new_row) or '111' in ''.join(new_row):
            return False

        # Check the column for triples (000 or 111)
        col = [self.board[i][x] for i in range(self.m)]
        new_col = col[:y] + [digit] + col[y+1:]
        if '000' in ''.join(new_col) or '111' in ''.join(new_col):
            return False

        return True

    def check_balance_constraint(self, x, y, digit):
        # Count 0s and 1s in the row
        row = self.board[y]
        count_0_row = row.count('0') + (1 if digit == '0' else 0)
        count_1_row = row.count('1') + (1 if digit == '1' else 0)

        # Count 0s and 1s in the column
        col = [self.board[i][x] for i in range(self.m)]
        count_0_col = col.count('0') + (1 if digit == '0' else 0)
        count_1_col = col.count('1') + (1 if digit == '1' else 0)

        # Check row and column balance
        row_limit = (self.n + 1) // 2
        col_limit = (self.m + 1) // 2

        if count_0_row > row_limit or count_1_row > row_limit:
            return False
        if count_0_col > col_limit or count_1_col > col_limit:
            return False

        return True

    
    def legal(self, args):
        # 1. Check wrong number of arguments
        if len(args) != 3:
            print(f"= illegal move: {' '.join(args)} wrong number of arguments")
            return False

        # 2. Check if the first coordinate is an integer and valid
        try:
            x = int(args[0])
        except ValueError:
            print("no")
            return True

        # 3. Check if the second coordinate is an integer and valid
        try:
            y = int(args[1])
        except ValueError:
            print("no")
            return True

        # 4. Check if the coordinates are in bounds
        if not (0 <= x < self.n) or not (0 <= y < self.m):
            print("no")
            return True

        # 5. Check if the third argument is either '0' or '1'
        if args[2] not in ['0', '1']:
            print("no")
            return True

        # 6. Check if the cell is already occupied
        if self.board[y][x] != '.':
            print("no")
            return True

        # 7. Check the triples constraint (no 000 or 111)
        if not self.check_triples_constraint(x, y, args[2]):
            print("no")
            return True

        # 8. Check the balance constraint (number of 0's or 1's exceeds half of row/column length)
        if not self.check_balance_constraint(x, y, args[2]):
            print("no")
            return True

        # If all checks pass, the move is legal
        print("yes")
        return True

    def genmove(self, args):
        if self.board is None:
            print("= no game in progress")
            return False

        legal_moves = []

        for y in range(self.m):
            for x in range(self.n):
                if self.board[y][x] == '.':  
                    for digit in ['0', '1']:
                        # Check if the move would violate the triples constraint
                        if not self.check_triples_constraint(x, y, digit):
                            continue
                        
                        # Check if the move would violate the balance constraint
                        if not self.check_balance_constraint(x, y, digit):
                            continue
                        
                        # If all constraints are satisfied, it's a legal move
                        legal_moves.append((x, y, digit))

        # If no legal moves are available, the player must resign
        if not legal_moves:
            print("resign")
            return True

        # Randomly select a legal move
        move = random.choice(legal_moves)
        x, y, digit = move

        # Play the move on the board
        self.board[y][x] = digit
        self.current_player = 2 if self.current_player == 1 else 1  # Alternate the player

        # Output the selected move in the format x y digit
        print(f"{x} {y} {digit}")
        return True
    
    def winner(self, args):
        if self.board is None:
            print("= no game in progress")
            return False

        # Check if there are any legal moves left for the current player
        for y in range(self.m):
            for x in range(self.n):
                if self.board[y][x] == '.': 
                    for digit in ['0', '1']:
                        # If any move is legal for the current player, the game is not over
                        if self.check_triples_constraint(x, y, digit) and self.check_balance_constraint(x, y, digit):
                            print("unfinished")
                            return True

        # If no legal moves are left, declare the opponent as the winner
        winner = 2 if self.current_player == 1 else 1
        print(winner)
        return True

    
    #======================================================================================
    # End of functions requiring implementation
    #======================================================================================

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()