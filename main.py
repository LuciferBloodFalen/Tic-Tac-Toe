


"""
Tic-Tac-Toe Game (Python, Tkinter)
----------------------------------
Single and two-player GUI Tic-Tac-Toe game with scoreboard, popups, and smart AI.
AI uses numpy and pandas to predict and play optimal moves.
"""

import tkinter as tk
from tkinter import messagebox


import random
import numpy as np
import pandas as pd

class TicTacToeGUI:
    def __init__(self, root):
        """
        Initialize the main window, game state, and show mode selection.
        Args:
            root (tk.Tk): The main Tkinter window.
        """
        # Initialize main window and game state
        self.root = root
        self.player_x_name = "X"
        self.player_o_name = "O"
        self.score_x = 0
        self.score_o = 0
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("400x460")
        # Remove fixed geometry, let window size adapt
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.mode = None
        # Show mode selection screen
        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(pady=60, fill="both", expand=True)
        self.mode_frame.pack_propagate(True)
        tk.Label(self.mode_frame, text="Select Game Mode:", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.mode_frame, text="Single Player (vs AI)", font=("Arial", 18), width=25, height=2, command=self.start_single_player).pack(pady=10)
        tk.Button(self.mode_frame, text="Two Player", font=("Arial", 18), width=25, height=2, command=self.start_two_player).pack(pady=10)

    def start_single_player(self):
        """
        Start single player mode (vs AI), set up UI and scoreboard.
        """
        # Start single player mode and set up UI
        self.mode = "single"
        self.mode_frame.destroy()
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x")
        self.scoreboard_visible = True
        self.toggle_btn = tk.Button(self.top_frame, text="Hide Scoreboard", font=("Arial", 10), command=self.toggle_scoreboard)
        self.toggle_btn.pack(side="right", padx=8, pady=2)
        self.create_scoreboard()
        self.create_widgets()

    def toggle_scoreboard(self):
        """
        Toggle scoreboard visibility in single player mode.
        """
        # Show/hide scoreboard in single player mode
        if self.scoreboard_visible:
            self.score_frame.pack_forget()
            self.toggle_btn.config(text="Show Scoreboard")
            self.scoreboard_visible = False
        else:
            self.score_frame.pack(pady=10)
            self.toggle_btn.config(text="Hide Scoreboard")
            self.scoreboard_visible = True

    def start_two_player(self):
        """
        Start two player mode, prompt for player names.
        """
        # Start two player mode and prompt for names
        self.mode = "two"
        self.mode_frame.destroy()
        self.name_frame = tk.Frame(self.root)
        self.name_frame.pack(pady=20)
        tk.Label(self.name_frame, text="Enter Player Names:", font=("Arial", 20)).pack(pady=10)
        name_x_label = tk.Label(self.name_frame, text="Player X:", font=("Arial", 16))
        name_x_label.pack()
        self.name_x_entry = tk.Entry(self.name_frame, font=("Arial", 16), width=15)
        self.name_x_entry.pack(pady=5)
        name_o_label = tk.Label(self.name_frame, text="Player O:", font=("Arial", 16))
        name_o_label.pack()
        self.name_o_entry = tk.Entry(self.name_frame, font=("Arial", 16), width=15)
        self.name_o_entry.pack(pady=5)
        tk.Button(self.name_frame, text="Start Game", font=("Arial", 16), command=self.confirm_names).pack(pady=10)

    def confirm_names(self):
        """
        Save player names and start the game.
        """
        # Save player names and start game
        x_name = self.name_x_entry.get().strip()
        o_name = self.name_o_entry.get().strip()
        self.player_x_name = x_name if x_name else "X"
        self.player_o_name = o_name if o_name else "O"
        self.name_frame.destroy()
        self.create_widgets()
        self.create_scoreboard()
    def create_scoreboard(self):
        """
        Create or update the scoreboard UI.
        """
        # Create or update scoreboard UI
        # Destroy old scoreboard if it exists
        if hasattr(self, 'score_frame') and self.score_frame.winfo_exists():
            self.score_frame.destroy()
        parent = self.top_frame if self.mode == "single" and hasattr(self, "top_frame") else self.root
        self.score_frame = tk.Frame(parent)
        self.score_frame.pack(side="left", padx=8, pady=10)
        self.score_label = tk.Label(self.score_frame, text=self.get_score_text(), font=("Arial", 22))
        self.score_label.pack()
        # Add turn label for two player mode
        if self.mode == "two":
            self.turn_label = tk.Label(self.score_frame, text=self.get_turn_text(), font=("Arial", 16), fg="blue")
            self.turn_label.pack(pady=5)

    def get_score_text(self):
        """
        Return formatted score string for scoreboard.
        """
        # Return formatted score string
        if self.mode == "single":
            return f"Score - You (X): {self.score_x}   AI (O): {self.score_o}"
        else:
            return f"Score - {self.player_x_name}: {self.score_x}   {self.player_o_name}: {self.score_o}"

    def get_turn_text(self):
        """
        Return whose turn it is (for two player mode).
        """
        # Return whose turn it is
        if self.current_player == "X":
            return f"Turn: {self.player_x_name}"
        else:
            return f"Turn: {self.player_o_name}"

    def get_score_text(self):
        return f"Score - {self.player_x_name}: {self.score_x}   {self.player_o_name}: {self.score_o}"

    def create_widgets(self):
        """
        Create game board buttons and layout.
        """
        # Create game board buttons and layout
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=60, fill="both", expand=True)
        self.frame.pack_propagate(True)
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.frame, text="", font=("Arial", 64), width=4, height=2,
                                command=lambda r=i, c=j: self.on_click(r, c))
                btn.grid(row=i, column=j, padx=15, pady=15, sticky="nsew")
                self.buttons[i][j] = btn
        for i in range(3):
            self.frame.grid_rowconfigure(i, weight=1)
            self.frame.grid_columnconfigure(i, weight=1)
        # Update turn label if two player mode
        if hasattr(self, 'turn_label') and self.mode == "two":
            self.turn_label.config(text=self.get_turn_text())

    def on_click(self, row, col):
        """
        Handle user clicking a cell. Manages turn logic and triggers AI move.
        Args:
            row (int): Row index.
            col (int): Column index.
        """
        # Handle user clicking a cell
        # Prevent user from clicking during AI's turn
        if self.mode == "single" and self.current_player == "O":
            return
        if self.buttons[row][col]["text"] == "" and not self.check_winner():
            self.buttons[row][col]["text"] = self.current_player
            self.board[row][col] = self.current_player
            if self.check_winner():
                self.show_end_options(f"Player {self.current_player} wins!")
            elif self.is_full():
                self.show_end_options("It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                # Update turn label if two player mode
                if hasattr(self, 'turn_label') and self.mode == "two":
                    self.turn_label.config(text=self.get_turn_text())
                if self.mode == "single" and self.current_player == "O":
                    # Disable all buttons during AI move
                    for i in range(3):
                        for j in range(3):
                            self.buttons[i][j]["state"] = "disabled"
                    self.root.after(500, self.ai_move)

    def ai_move(self):
        """
        AI predicts and plays optimal move using numpy/pandas:
        - Tries to win
        - Blocks player win
        - Takes center/corner/any empty
        """
        # AI uses numpy/pandas to predict and play optimal move
        board_np = np.array([[self.board[i][j] if self.board[i][j] is not None else "" for j in range(3)] for i in range(3)])
        empty = [(i, j) for i in range(3) for j in range(3) if board_np[i, j] == ""]

        def can_win(b, player):
            for i, j in empty:
                b[i, j] = player
                if self._check_winner_np(b, player):
                    b[i, j] = ""
                    return (i, j)
                b[i, j] = ""
            return None

        # 1. Try to win
        win_move = can_win(board_np.copy(), "O")
        if win_move:
            row, col = win_move
        else:
            # 2. Block player win
            block_move = can_win(board_np.copy(), "X")
            if block_move:
                row, col = block_move
            else:
                # 3. Take center if available
                if board_np[1, 1] == "":
                    row, col = 1, 1
                else:
                    # 4. Take a corner if available
                    corners = [(i, j) for i in [0, 2] for j in [0, 2] if board_np[i, j] == ""]
                    if corners:
                        row, col = random.choice(corners)
                    else:
                        # 5. Otherwise, pick any empty
                        row, col = random.choice(empty)

        self.buttons[row][col]["text"] = "O"
        self.board[row][col] = "O"
        if self.check_winner():
            self.show_end_options("Player O (AI) wins!")
        elif self.is_full():
            self.show_end_options("It's a draw!")
        else:
            self.current_player = "X"
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["state"] = "normal"

    def _check_winner_np(self, b, player):
        """
        Check winner for numpy board.
        Args:
            b (np.ndarray): Board array.
            player (str): 'X' or 'O'.
        Returns:
            bool: True if player wins.
        """
        # Check winner for numpy board
        for i in range(3):
            if all(b[i, j] == player for j in range(3)):
                return True
            if all(b[j, i] == player for j in range(3)):
                return True
        if all(b[i, i] == player for i in range(3)):
            return True
        if all(b[i, 2 - i] == player for i in range(3)):
            return True
        return False

    def check_winner(self):
        """
        Check if current board has a winner.
        Returns:
            bool: True if someone wins.
        """
        # Check if current board has a winner
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] and b[i][0] is not None:
                return True
            if b[0][i] == b[1][i] == b[2][i] and b[0][i] is not None:
                return True
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] is not None:
            return True
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] is not None:
            return True
        return False

    def is_full(self):
        """
        Check if board is full (draw).
        Returns:
            bool: True if board is full.
        """
        # Check if board is full (draw)
        return all(self.board[i][j] is not None for i in range(3) for j in range(3))

    def reset_board(self):
        """
        Reset board for new game.
        """
        # Reset board for new game
        self.current_player = "X"
        self.board = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
        # Update turn label if two player mode
        if hasattr(self, 'turn_label') and self.mode == "two":
            self.turn_label.config(text=self.get_turn_text())

    def show_end_options(self, message):
        """
        Show popup for win/draw, update score, and offer play again/main menu.
        Args:
            message (str): Result message.
        """
        # Show popup for win/draw and update score
        # Update score and message for both modes
        winner = None
        if "Player X wins" in message:
            self.score_x += 1
            winner = self.player_x_name if self.mode == "two" else "You (X)"
        elif "Player O wins" in message or "Player O (AI) wins" in message:
            self.score_o += 1
            winner = self.player_o_name if self.mode == "two" else "AI (O)"
        self.score_label.config(text=self.get_score_text())
        if winner:
            message = f"{winner} wins!"
        # Disable all buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["state"] = "disabled"
        # Show custom modal popup for result
        popup = tk.Toplevel(self.root)
        popup.transient(self.root)
        popup.grab_set()
        popup.title("Game Result")
        popup.geometry("260x140")
        popup.resizable(False, False)
        tk.Label(popup, text=message, font=("Arial", 14), bg="#f0f0f0").pack(pady=12, padx=10)
        btn_frame = tk.Frame(popup, bg="#f0f0f0")
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Play Again", font=("Arial", 12), width=10, command=lambda: self._close_popup_and_play_again(popup)).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Main Menu", font=("Arial", 12), width=10, command=lambda: self._close_popup_and_main_menu(popup)).pack(side="right", padx=6)

    def _close_popup_and_play_again(self, popup):
        """
        Close popup and reset board for new game.
        """
        # Close popup and reset board
        popup.destroy()
        self.reset_board()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["state"] = "normal"

    def _close_popup_and_main_menu(self, popup):
        """
        Close popup and return to main menu.
        """
        # Close popup and return to main menu
        popup.destroy()
        self.frame.destroy()
        if hasattr(self, 'score_frame'):
            self.score_frame.destroy()
        if hasattr(self, 'top_frame'):
            self.top_frame.destroy()
        self.__init__(self.root)

    def play_again(self):
        """
        Play again after game ends (legacy, not used).
        """
        # Play again after game ends
        self.end_frame.destroy()
        self.reset_board()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["state"] = "normal"

    def return_to_menu(self):
        """
        Return to main menu and reset scores.
        """
        # Return to main menu and reset scores
        self.end_frame.destroy()
        self.frame.destroy()
        if hasattr(self, 'score_frame'):
            self.score_frame.destroy()
        if hasattr(self, 'top_frame'):
            self.top_frame.destroy()
        self.score_x = 0
        self.score_o = 0
        self.__init__(self.root)


# Run the game

if __name__ == "__main__":
    # Start the Tic-Tac-Toe game
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
