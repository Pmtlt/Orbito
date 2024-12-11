import tkinter as tk
from tkinter import messagebox
import random

class OrbitGame:
    """Main class for the Orbit game implementing both GUI and game logic.

    This class manages all aspects of the Orbit game, including:
    - Tkinter graphical interface
    - 4x4 game board
    - Ball placement logic
    - Rotation (orbit) system
    - Win condition checking
    
    Attributes:
        window (tk.Tk): Main game window
        board (list): 4x4 matrix representing game state (0: empty, 1: white, 2: black)
        current_player (int): Current player (1: white, 2: black)
        move_made (bool): Indicates if a move has been made this turn
        CELL_SIZE (int): Size in pixels of each cell
        CIRCLE_PADDING (int): Spacing between ball and cell border
        BOARD_COLOR (str): Board color code
        EMPTY_COLOR (str): Empty cell color code
        WHITE_PIECE (str): White ball color code
        BLACK_PIECE (str): Black ball color code
        HIGHLIGHT (str): Hover highlight color code
    """
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Jeu Orbit")
        self.window.configure(bg='#8B4513')
        
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.current_player = 1
        self.canvases = []
        self.circles = []
        self.move_made = False
        
        self.main_frame = tk.Frame(self.window, bg='#DEB887', bd=15, relief='ridge')
        self.main_frame.pack(padx=20, pady=20)
        
        self.CELL_SIZE = 90
        self.CIRCLE_PADDING = 8
        self.SHADOW_OFFSET = 2
        
        self.BOARD_COLOR = '#8B4513'
        self.EMPTY_COLOR = '#6B4423'
        self.WHITE_PIECE = '#FFFAFA'
        self.BLACK_PIECE = '#0C0C0C'
        self.HIGHLIGHT = '#CD853F'
        
        self.create_board()
        self.create_controls()
        
        self.player_label = tk.Label(self.main_frame, text="Tour du joueur Blanc",
                                   font=('Arial', 14, 'bold'), bg='#DEB887', fg='#4A3210')
        self.player_label.grid(row=5, column=0, columnspan=4, pady=15)
        
    def create_board(self):
        """Initialize the game board with a 4x4 grid of cells.
        
        Creates a visual 4x4 grid where each cell is a tkinter canvas.
        Each cell contains:
        - A background with wood grain effect
        - A recessed area for the ball
        - A circle for the ball
        - A shine effect
        
        The method also configures click and hover events for each cell.
        
        Cells are stored in self.canvases and balls in self.circles for
        later manipulation.
        """
        grid_frame = tk.Frame(self.main_frame, bg='#A0522D', bd=8, relief='raised')
        grid_frame.grid(row=0, column=0, rowspan=4, columnspan=4, padx=10, pady=10)
        
        for i in range(4):
            canvas_row = []
            circle_row = []
            for j in range(4):
                canvas = tk.Canvas(grid_frame, width=self.CELL_SIZE, 
                                 height=self.CELL_SIZE, bg=self.BOARD_COLOR,
                                 highlightthickness=1, highlightbackground='#6B4423')
                canvas.grid(row=i, column=j, padx=3, pady=3)
                
                for k in range(0, self.CELL_SIZE, 8):
                    canvas.create_line(0, k, self.CELL_SIZE, k,
                                    fill='#966F33', width=1, stipple='gray50')
                
                canvas.create_oval(self.CIRCLE_PADDING - 2, self.CIRCLE_PADDING - 2,
                                 self.CELL_SIZE - self.CIRCLE_PADDING + 2,
                                 self.CELL_SIZE - self.CIRCLE_PADDING + 2,
                                 fill=self.EMPTY_COLOR, outline='#4A3210')
                
                circle = canvas.create_oval(self.CIRCLE_PADDING, self.CIRCLE_PADDING,
                                         self.CELL_SIZE - self.CIRCLE_PADDING,
                                         self.CELL_SIZE - self.CIRCLE_PADDING,
                                         fill=self.EMPTY_COLOR, outline='')
                
                highlight_size = self.CIRCLE_PADDING + 10
                canvas.create_oval(highlight_size, highlight_size,
                                 highlight_size + 15, highlight_size + 15,
                                 fill='white', stipple='gray50', outline='')
                
                canvas.bind('<Button-1>', lambda e, r=i, c=j: self.make_move(r, c))
                canvas.bind('<Enter>', lambda e, c=canvas: self.on_enter(c))
                canvas.bind('<Leave>', lambda e, c=canvas: self.on_leave(c))
                
                canvas_row.append(canvas)
                circle_row.append(circle)
            self.canvases.append(canvas_row)
            self.circles.append(circle_row)
    
    def create_controls(self):
        """Create game control buttons.
        
        Sets up two buttons:
        - "Orbit": For rotating the balls (disabled by default)
        - "New Game": For resetting the game
        
        Buttons are styled with a wooden look consistent with the game theme.
        """
        button_frame = tk.Frame(self.main_frame, bg='#DEB887')
        button_frame.grid(row=4, column=0, columnspan=4, pady=15)
        
        button_style = {'font': ('Arial', 12, 'bold'), 
                       'bg': '#8B4513', 
                       'fg': '#FFE4B5',
                       'activebackground': '#A0522D', 
                       'activeforeground': '#FFE4B5',
                       'width': 15, 
                       'height': 1, 
                       'bd': 4, 
                       'relief': 'raised'}
        
        self.orbit_button = tk.Button(button_frame, text="Orbite",
                                    command=self.orbit_move, state='disabled',
                                    **button_style)
        self.orbit_button.pack(side=tk.LEFT, padx=10)
        
        new_game_button = tk.Button(button_frame, text="Nouvelle Partie",
                                  command=self.new_game, **button_style)
        new_game_button.pack(side=tk.LEFT, padx=10)
    
    def on_enter(self, canvas):
        """Handle cell hover effect.
        
        Args:
            canvas (tk.Canvas): The canvas being hovered over
            
        Empty cells change color on hover to indicate they are clickable.
        """
        if canvas['bg'] == self.BOARD_COLOR:
            canvas['bg'] = self.HIGHLIGHT
    
    def on_leave(self, canvas):
        """Handle end of cell hover.
        
        Args:
            canvas (tk.Canvas): The canvas no longer being hovered over
            
        Restores the cell's original color.
        """
        if canvas['bg'] == self.HIGHLIGHT:
            canvas['bg'] = self.BOARD_COLOR
    
    def add_shine_effect(self, canvas, circle, color):
        """Add a shine effect to a ball.
        
        Args:
            canvas (tk.Canvas): The canvas containing the ball
            circle (int): The ID of the circle representing the ball
            color (str): The color code to apply to the ball
            
        Applies the specified color to the ball and adds a shine effect
        by overlaying a small semi-transparent white circle.
        """
        canvas.itemconfig(circle, fill=color)
        highlight_size = self.CIRCLE_PADDING + 10
        canvas.create_oval(highlight_size, highlight_size,
                         highlight_size + 15, highlight_size + 15,
                         fill='white', stipple='gray50', outline='')
    
    def make_move(self, row, col):
        """Place a ball on the board.
        
        Args:
            row (int): Row index (0-3)
            col (int): Column index (0-3)
            
        If the move is valid (empty cell and no move made this turn),
        places a ball of the current player's color and enables the
        orbit button.
        """
        if not self.move_made and self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            color = self.WHITE_PIECE if self.current_player == 1 else self.BLACK_PIECE
            canvas = self.canvases[row][col]
            circle = self.circles[row][col]
            self.add_shine_effect(canvas, circle, color)
            self.move_made = True
            self.orbit_button['state'] = 'normal'
    
    def update_display(self):
        """Update the board display after a move.
        
        Iterates through the board and updates the appearance of each cell
        based on its content (empty, white ball, or black ball).
        Visual effects (shine, etc.) are reapplied.
        """
        for i in range(4):
            for j in range(4):
                canvas = self.canvases[i][j]
                circle = self.circles[i][j]
                if self.board[i][j] == 0:
                    canvas.itemconfig(circle, fill=self.EMPTY_COLOR)
                elif self.board[i][j] == 1:
                    self.add_shine_effect(canvas, circle, self.WHITE_PIECE)
                else:
                    self.add_shine_effect(canvas, circle, self.BLACK_PIECE)

    def orbit_move(self):
        """Execute the ball rotation move.
        
        Makes balls "orbit" according to a predefined pattern:
        - External balls rotate clockwise
        - Internal balls rotate counterclockwise
        
        After rotation, checks if either player (or both) has won.
        If so, displays appropriate message and resets the game.
        If not, moves to next player's turn.
        """
        if not self.move_made:
            return
            
        new_board = [[0 for _ in range(4)] for _ in range(4)]
        
        moves = {
            (0,0): (1,0), (1,0): (2,0), (2,0): (3,0),
            (3,0): (3,1), (3,1): (3,2), (3,2): (3,3),
            (3,3): (2,3), (2,3): (1,3), (1,3): (0,3),
            (0,3): (0,2), (0,2): (0,1), (0,1): (0,0),
            (1,1): (2,1), (2,1): (2,2), (2,2): (1,2),
            (1,2): (1,1)
        }
        
        for (old_row, old_col), (new_row, new_col) in moves.items():
            new_board[new_row][new_col] = self.board[old_row][old_col]
        
        self.board = new_board
        self.update_display()
        
        white_wins = self.check_win_for_player(1)
        black_wins = self.check_win_for_player(2)
        
        if white_wins and black_wins:
            messagebox.showinfo("Match Nul", "Les deux joueurs ont gagné !")
            self.new_game()
        elif white_wins:
            messagebox.showinfo("Victoire", "Le joueur Blanc a gagné!")
            self.new_game()
        elif black_wins:
            messagebox.showinfo("Victoire", "Le joueur Noir a gagné!")
            self.new_game()
        else:
            self.current_player = 3 - self.current_player
            self.player_label.config(
                text=f"Tour du joueur {'Blanc' if self.current_player == 1 else 'Noir'}")
            self.move_made = False
            self.orbit_button['state'] = 'disabled'
    
    def check_win_for_player(self, player):
        """Check if a player has won.
        
        Args:
            player (int): Player identifier (1 for White, 2 for Black)
            
        Returns:
            bool: True if the player has aligned 4 balls (horizontally,
                 vertically, or diagonally), False otherwise
        
        Checks all possible winning conditions:
        - 4 horizontal lines
        - 4 vertical lines
        - 2 diagonals
        """
        winning_conditions = [
            [(i,j) for j in range(4)] for i in range(4)
        ] + [
            [(j,i) for j in range(4)] for i in range(4)
        ] + [
            [(i,i) for i in range(4)],
            [(i,3-i) for i in range(4)]
        ]
        
        for condition in winning_conditions:
            if all(self.board[row][col] == player for row, col in condition):
                return True
        return False
    
    def new_game(self):
        """Reset the game for a new match.
        
        Actions performed:
        - Clears the board (sets all cells to 0)
        - Sets white player as active
        - Disables orbit button
        - Resets board display
        - Updates active player label
        """
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.current_player = 1
        self.move_made = False
        self.orbit_button['state'] = 'disabled'
        self.player_label.config(text="Tour du joueur Blanc")
        self.update_display()
    
    def run(self):
        """Start the game.
        
        Launches the main tkinter event loop.
        Game remains active until window is closed.
        """
        self.window.mainloop()

def game():
    """Launch a new game of Orbit.
    
    Creates an instance of the OrbitGame class and starts the game.
    This function is the main entry point of the program.
    """
    game = OrbitGame()
    game.run()

if __name__ == "__main__":
    game()