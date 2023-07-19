import pyxel
import time
import random

# Define the Chessboard Status
class ChessboardStatus:
    EMPTY = 0 # The Chess Cell not Taken
    PLAYER1 = 1 # Taken by Player 1 (The Human)
    PLAYER2 = 2 # Taken by Player 2 (The Bot)

# The Bot Player Functioningg Part
class DBot:
    # Initiate the Chessboard Status for the Bot
    def __init__(self, board_size):# Initiate the Chessboard Status for the Bot
        self.BOARD_SIZE = board_size

    # Check If There is a Winner
    def if_winner(self, board):
        # Horizontally Check if 5 Chess Pieces in a Row
        for row in board:
            for i in range(self.BOARD_SIZE - 4):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == row[i + 4] != 0:
                    return row[i]

        # Vertically Check if 5 Chess Pieces in a Row
        for col in range(self.BOARD_SIZE):
            for i in range(self.BOARD_SIZE - 4):
                if board[i][col] == board[i + 1][col] == board[i + 2][col] == board[i + 3][col] == board[i + 4][col] != 0:
                    return board[i][col]

        # Top-Left and Bottom-Right if 5 Chess Pieces in a Row
        for i in range(self.BOARD_SIZE - 4):
            for j in range(self.BOARD_SIZE - 4):
                if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4] != 0:
                    return board[i][j]

        # Top-Right and Bottom-Left if 5 Chess Pieces in a Row
        for i in range(self.BOARD_SIZE - 1, 3, -1):
            for j in range(self.BOARD_SIZE - 4):
                if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3] == board[i - 4][j + 4] != 0:
                    return board[i][j]

        # No Winner, Place 1 Chess Piece on Chessboard
        return 0

    # Check Where to Put the Chess
    def near_complete(self, board, x, y):
        # Check a Cell and Surrounding 8 Cells for an Empty One
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                # Pick up a Cell to Place the Chess Piece
                new_x = x + dx
                new_y = y + dy

                # Make Sure to Place Chess inside the Chessboard 
                if (
                    new_x >= 0
                    and new_x < self.BOARD_SIZE
                    and new_y >= 0
                    and new_y < self.BOARD_SIZE
                    and board[new_y][new_x] != 0
                ):
                    return True
        return False

    # Check if a Move Would Win the Round
    def win_move(self, board, x, y, player):
        if x <= self.BOARD_SIZE - 5 and all(board[y][i] == player for i in range(x, x + 5)):
            return True

        if y <= self.BOARD_SIZE - 5 and all(board[i][x] == player for i in range(y, y + 5)):
            return True

        if x <= self.BOARD_SIZE - 5 and y <= self.BOARD_SIZE - 5 and all(
            board[y + i][x + i] == player for i in range(5)
        ):
            return True

        if x <= self.BOARD_SIZE - 5 and y >= 4 and all(
            board[y - i][x + i] == player for i in range(5)
        ):
            return True

        return False

    # Defines How Bot Makes a Move
    def bot_turn(self, board, current_player):
        # Empty Cell
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                if board[y][x] == ChessboardStatus.EMPTY and self.win_move(board, x, y, current_player):
                    return x, y

        # Cell Taken by Player 1's Chess Pieces
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                if board[y][x] == 0 and self.win_move(board, x, y, ChessboardStatus.PLAYER1):
                    return x, y

        # Intercept Player 1's Chess Pieces or Placing Its Own
        # Detect Horizontal Lines of 3 Chess Pieces Placed by Human Player
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE - 2):
                if (
                    board[y][x] == ChessboardStatus.PLAYER1
                    and board[y][x + 1] == ChessboardStatus.PLAYER1
                    and board[y][x + 2] == ChessboardStatus.PLAYER1
                ) or (
                    board[y][x] == ChessboardStatus.PLAYER2
                    and board[y][x + 1] == ChessboardStatus.PLAYER2
                    and board[y][x + 2] == ChessboardStatus.PLAYER2
                ):
                    # Add Considered Places to Intercept or Add Own
                    if x > 0 and board[y][x - 1] == 0:
                        return x - 1, y
                    if x + 3 < self.BOARD_SIZE and board[y][x + 3] == 0:
                        return x + 3, y

        # Detect Vertical Lines of 3 Chess Pieces Placed by Human Player
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE - 2):
                if (
                    board[y][x] == ChessboardStatus.PLAYER1
                    and board[y + 1][x] == ChessboardStatus.PLAYER1
                    and board[y + 2][x] == ChessboardStatus.PLAYER1
                ) or (
                    board[y][x] == ChessboardStatus.PLAYER2
                    and board[y + 1][x] == ChessboardStatus.PLAYER2
                    and board[y + 2][x] == ChessboardStatus.PLAYER2
                ):
                    # Add Considered Places to Intercept or Add Own
                    if y > 0 and board[y - 1][x] == 0:
                        return x, y - 1
                    if y + 3 < self.BOARD_SIZE and board[y + 3][x] == 0:
                        return x, y + 3

        # Detect Top-Left to Botton-Right Lines of 3 Chess Pieces Placed by Human Player
        for x in range(self.BOARD_SIZE - 2):
            for y in range(self.BOARD_SIZE - 2):
                if (
                    board[y][x] == ChessboardStatus.PLAYER1
                    and board[y + 1][x + 1] == ChessboardStatus.PLAYER1
                    and board[y + 2][x + 2] == ChessboardStatus.PLAYER1
                ) or (
                    board[y][x] == ChessboardStatus.PLAYER2
                    and board[y + 1][x + 1] == ChessboardStatus.PLAYER2
                    and board[y + 2][x + 2] == ChessboardStatus.PLAYER2
                ):
                    # Add Considered Places to Intercept or Add Own
                    if (y > 0 and x > 0) and board[y - 1][x - 1] == 0:
                        return x - 1, y -1
                    if (y + 3 < self.BOARD_SIZE and x + 3 < self.BOARD_SIZE) and board[y + 3][x + 3] == 0:
                        return x + 3, y + 3

        # Detect Top-Right to Botton-Left Lines of 3 Chess Pieces Placed by Human Player
        for x in range(self.BOARD_SIZE - 2):
            for y in range(self.BOARD_SIZE - 2):
                if (
                    board[y][x] == ChessboardStatus.PLAYER1
                    and board[y + 1][x - 1] == ChessboardStatus.PLAYER1
                    and board[y + 2][x - 2] == ChessboardStatus.PLAYER1
                ) or (
                    board[y][x] == ChessboardStatus.PLAYER2
                    and board[y + 1][x - 1] == ChessboardStatus.PLAYER2
                    and board[y + 2][x - 2] == ChessboardStatus.PLAYER2
                ):
                    # Add Considered Places to Intercept or Add Own
                    if (y > 0 and x < self.BOARD_SIZE) and board[y - 1][x + 1] == 0:
                        return x + 1, y - 1
                    if (y + 3 < self.BOARD_SIZE and x - 3 > 0) and board[y + 3][x - 3] == 0:
                        return x - 3, y + 3

        # Valid Move to Place Bot's Chess Pieces in a Cell Next to Player 1's Chess Pieces or Connect Own Lines
        valid_moves = []
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                # Add a Choice to Consider
                if board[y][x] == 0 and self.near_complete(board, x, y):
                    valid_moves.append((x, y))
        if valid_moves:
            return random.choice(valid_moves)

        # Valid Move to Place Bot's Chess Pieces in a Cell w/ No Player 1's Chess Pieces Around
        valid_moves = []
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                if board[y][x] == 0:
                    valid_moves.append((x, y))
        if valid_moves:
            return random.choice(valid_moves)

        return None

# The Execution of the Chess Game
class App:
    # Initialize the Chessboard Status
    def __init__(self):
        # Key Details of the Solid Figures
        self.BOARD_SIZE = 15
        self.CELL_SIZE = 32
        self.SCREEN_WIDTH = self.BOARD_SIZE * self.CELL_SIZE
        self.SCREEN_HEIGHT = self.BOARD_SIZE * self.CELL_SIZE + 40

        self.board = [[ChessboardStatus.EMPTY] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.current_player = ChessboardStatus.PLAYER1
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False

        self.countdown_time = 0
        self.countdown_duration = 5
        self.turn_time = 20
        self.turn_start_time = 0

        self.bot = DBot(self.BOARD_SIZE)

        # Show Instructions for Playing as Human for 5 Seconds
        self.show_instructions = True
        self.instructions_time = time.time()

        # Initlize the Entire Program
        pyxel.init(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        pyxel.run(self.update, self.draw)

    # Check if there is a Winner Between Player 1 and 2 by Seeking 5  Chess Pieces Form a Horizontal, Vertical or Diagonal Line
    def if_winner(self):
        for row in self.board:
            for i in range(self.BOARD_SIZE - 4):
                if row[i] == row[i + 1] == row[i + 2] == row[i + 3] == row[i + 4] != 0:
                    return row[i]

        for col in range(self.BOARD_SIZE):
            for i in range(self.BOARD_SIZE - 4):
                if self.board[i][col] == self.board[i + 1][col] == self.board[i + 2][col] == self.board[i + 3][col] == self.board[i + 4][col] != 0:
                    return self.board[i][col]

        for i in range(self.BOARD_SIZE - 4):
            for j in range(self.BOARD_SIZE - 4):
                if self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] == self.board[i + 4][j + 4] != 0:
                    return self.board[i][j]

        for i in range(self.BOARD_SIZE - 1, 3, -1):
            for j in range(self.BOARD_SIZE - 4):
                if self.board[i][j] == self.board[i - 1][j + 1] == self.board[i - 2][j + 2] == self.board[i - 3][j + 3] == self.board[i - 4][j + 4] != 0:
                    return self.board[i][j]

        return 0

    # After a Winner is Confirmed, Reset the Chessboard Status
    def reset_game(self):
        self.board = [[0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.current_player = ChessboardStatus.PLAYER1
        self.game_over = False
        self.countdown_time = 0

    # A 5-Second Countdown before Next Round Begins
    def start_countdown(self):
        self.countdown_time = time.time()

    # The Start of a New Round and Reset
    def new_round(self):
        self.reset_game()
        self.game_over = False

    # Display of Game's Instructions
    def instructions(self):
        pyxel.cls(7)
        pyxel.text(self.SCREEN_WIDTH // 2 - 60, self.SCREEN_HEIGHT // 2 - 20, "Keyboard Instructions:", 0)
        pyxel.text(self.SCREEN_WIDTH // 2 - 80, self.SCREEN_HEIGHT // 2, "Space and Mouse Cursor: Place your chess", 0)
        pyxel.text(self.SCREEN_WIDTH // 2 - 80, self.SCREEN_HEIGHT // 2 + 10, "Q: Quit the game", 0)
        pyxel.text(self.SCREEN_WIDTH // 2 - 80, self.SCREEN_HEIGHT // 2 + 20, "R: Skip the waiting time between rounds", 0)

    # What to do After Each Prerequisite Met
    def update(self):
        # Un-Display the Instruction and Show the Chessboard
        if self.show_instructions:
            if time.time() - self.instructions_time > self.countdown_duration:
                self.show_instructions = False
                self.start_countdown()
                return

        # Press "Q" to Quit the Program
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # Press "R" to Skip the 5-Second Countdown and to the Next Round
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.new_round()
            return

        # Bot Player Acts
        if self.current_player == ChessboardStatus.PLAYER2:
            if not self.game_over:
                # If Chess Piece not Placed by Bot Before Pesudo Countdown Ends, It Is Player 1's Turn
                if time.time() - self.turn_start_time > self.turn_time:
                    self.current_player = ChessboardStatus.PLAYER1
                    return

                # Time Needed for Bot to Place Chess, in This Case, It Is 1 Second. Also Can be Replaced by random.randint(1, 20), But Countdown Does Not Move
                time.sleep(1)

                # Bot Make the Move
                bot_move = self.bot.bot_turn(self.board, self.current_player)
                x, y = bot_move

                # Add 1 to the Score Count of Player Who Wins the Current Round
                self.board[y][x] = self.current_player
                winner = self.bot.if_winner(self.board)
                if winner != ChessboardStatus.EMPTY:
                    self.game_over = True
                    if winner == ChessboardStatus.PLAYER1:
                        self.player1_score += 1
                    else:
                        self.player2_score += 1
                    self.start_countdown()
                else:
                    self.current_player = ChessboardStatus.PLAYER1

        # Human Player Acts
        if pyxel.btnp(pyxel.KEY_SPACE) and self.current_player == ChessboardStatus.PLAYER1:
            if self.board[pyxel.mouse_y // self.CELL_SIZE][pyxel.mouse_x // self.CELL_SIZE] == ChessboardStatus.EMPTY:
                x = pyxel.mouse_x // self.CELL_SIZE
                y = pyxel.mouse_y // self.CELL_SIZE

                # Player Which Placed Recent Chess Piece and Got 5-In-a-Row Is the Winner
                self.board[y][x] = self.current_player
                winner = self.bot.if_winner(self.board)
                # After Human Player Won the Round, Add 1 to Player's Score Count and Start the 5-Second Countdown to Next Round
                if winner != 0:
                    self.game_over = True
                    self.player1_score += 1
                    self.start_countdown()
                # It Is Bot's Turn Now and Start the Pseudo Countdown 
                else:
                    self.current_player = ChessboardStatus.PLAYER2
                    self.turn_start_time = time.time()

    # What to Show
    def draw(self):
        if self.show_instructions:
            self.instructions()
            return

        # A top Rectangle for Displaying the Messages
        pyxel.cls(9)
        pyxel.rect(0, 0, self.SCREEN_WIDTH, 40, 0)

        # Display the Current Turn is for Who's Move
        player_turn_text = f"Player {self.current_player}'s turn"
        pyxel.text(self.SCREEN_WIDTH // 2 - 32, 10, player_turn_text, 7)

        # Add a Pseudo-Thinking Time of 20 Seconds for the Bot and Display it
        if self.current_player == ChessboardStatus.PLAYER2 and not self.game_over:
            remaining_time = self.turn_time - (time.time() - self.turn_start_time)
            countdown_text = f"Time left: {int(remaining_time)} seconds"
            pyxel.text(self.SCREEN_WIDTH - 284, 20, countdown_text, 7)

        # Draw Lines to Boarder the Cells on Chessboard
        for i in range(self.BOARD_SIZE):
            pyxel.line(0, i * self.CELL_SIZE + 40, self.SCREEN_WIDTH, i * self.CELL_SIZE + 40, 0)
            pyxel.line(i * self.CELL_SIZE, 40, i * self.CELL_SIZE, self.SCREEN_HEIGHT, 0)

        # Define the Color of Chess Pieces Placed by Each Player
        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                if self.board[y][x] == 1:
                    pyxel.circ(x * self.CELL_SIZE + self.CELL_SIZE // 2, y * self.CELL_SIZE + self.CELL_SIZE // 2 + 40, 10, 1)
                elif self.board[y][x] == 2:
                    pyxel.circ(x * self.CELL_SIZE + self.CELL_SIZE // 2, y * self.CELL_SIZE + self.CELL_SIZE // 2 + 40, 10, 7)

        # Display How Many Rounds by Player 1 and 2 in Top-Left and Top-Right Corner
        pyxel.text(10, 10, f"Player 1: {self.player1_score}", 7)
        pyxel.text(self.SCREEN_WIDTH - 90, 10, f"Player 2: {self.player2_score}", 7)

        # Make Sure the Displayed Cursor Exactly Fit inside the Cell and Draw the Cursor
        cursor_x = pyxel.mouse_x // self.CELL_SIZE
        cursor_y = pyxel.mouse_y // self.CELL_SIZE
        pyxel.line(cursor_x * self.CELL_SIZE, cursor_y * self.CELL_SIZE + 40, (cursor_x + 1) * self.CELL_SIZE, (cursor_y + 1) * self.CELL_SIZE + 40, 2)
        pyxel.line((cursor_x + 1) * self.CELL_SIZE, cursor_y * self.CELL_SIZE + 40, cursor_x * self.CELL_SIZE, (cursor_y + 1) * self.CELL_SIZE + 40, 2)

        # What to do after Someone Won the Round
        if self.game_over:
            winner = self.if_winner()
            # Display who is the Winner
            if winner != 0:
                pyxel.text(self.SCREEN_WIDTH // 2 - 25, 30, f"Player {winner} wins!", 3)
                pyxel.play(0, 0)
            # This Part is Basically Useless Since there is not Going to be a Draw in Gomoku
            else:
                pyxel.text(self.SCREEN_WIDTH // 2 - 20, self.SCREEN_HEIGHT // 7 - 4, "It's a draw!", 3)

        # The Execution of 5-Second Countdown
        if self.countdown_time > 0:
            # How Much Time Left
            remaining_time = self.countdown_duration - (time.time() - self.countdown_time)
            # Display How Much Time Left
            if remaining_time > 0:
                countdown_text = f"{int(remaining_time)} seconds to next round"
                pyxel.text(self.SCREEN_WIDTH // 2 - 45, 20, countdown_text, 7)
            # A New Round if the Countdown is Over
            else:
                self.new_round()

# Sound for Mentioning if Someone Wins 
def esound():
    pyxel.sound(0).set("c3e3g3c4c4", "s", "7", ("n" * 4), 7)

app = App()
