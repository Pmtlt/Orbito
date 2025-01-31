# src/orbito/gui/interface.py
"""
Graphical user interface for the Orbito board game.

This module implements the graphical interface for Orbito using tkinter.
It handles all visual aspects of the game including:
    - Game board rendering
    - Ball placement animation and effects
    - Button controls
    - Player turn indication
    - Win/draw notifications
    - Visual feedback for valid moves

The interface uses a wooden theme with realistic ball rendering including
shadows and shine effects for improved visual appeal.

Classes:
    OrbitInterface: Main class handling all GUI elements and interactions
"""

import tkinter as tk
from tkinter import messagebox
from ..core.game import OrbitGame
from ..core.ai import MinimaxAI

class OrbitInterface:
    """
    Main class implementing the graphical interface for Orbito.
    
    This class creates and manages all visual elements of the game, including:
    - Main window and frames
    - Game board with interactive cells
    - Control buttons
    - Player turn indicator
    - Visual effects and animations
    
    The interface uses a consistent wooden theme with detailed visual effects
    to enhance the gaming experience.
    
    Attributes:
        window (tk.Tk): Main game window
        game (OrbitGame): Game logic instance
        canvases (list[list[tk.Canvas]]): 4x4 matrix of cell canvases
        circles (list[list[int]]): 4x4 matrix of circle IDs for balls
        main_frame (tk.Frame): Main container frame
        orbit_button (tk.Button): Button for rotation move
        player_label (tk.Label): Label showing current player
        CELL_SIZE (int): Size of each board cell in pixels
        CIRCLE_PADDING (int): Space between ball and cell edge
        SHADOW_OFFSET (int): Offset for shadow effects
        BOARD_COLOR (str): Hex color code for board
        EMPTY_COLOR (str): Hex color code for empty cells
        WHITE_PIECE (str): Hex color code for white balls
        BLACK_PIECE (str): Hex color code for black balls
        HIGHLIGHT (str): Hex color code for hover highlight
    """
    
    def __init__(self):
        """
        Initialize the game interface.
        
        Creates the main window, sets up the game logic instance,
        initializes all visual elements, and configures the wooden theme.
        All GUI components are created and arranged in the window.
        """
        self.game = OrbitGame()
        self.window = tk.Tk()
        self.window.title("Orbito")
        self.window.configure(bg='#8B4513')  # Dark wooden brown
        
        self.canvases = []
        self.circles = []
        
        self.setup_constants()
        self.create_gui()

        self.ai_player = None
        self.against_ai = False
        
    def setup_constants(self):
        """
        Initialize all constant values used in the interface.
        
        Defines:
        - Size and spacing measurements
        - Color codes for various elements
        - Visual effect parameters
        
        These constants ensure consistency across the interface.
        """
        # Size constants
        self.CELL_SIZE = 90         # Cell size in pixels
        self.CIRCLE_PADDING = 8     # Space between ball and cell edge
        self.SHADOW_OFFSET = 2      # Shadow effect offset
        
        # Color constants using hex codes
        self.BOARD_COLOR = '#8B4513'    # Dark wooden brown
        self.EMPTY_COLOR = '#6B4423'    # Darker brown for empty cells
        self.WHITE_PIECE = '#FFFAFA'    # Snow white for player 1
        self.BLACK_PIECE = '#0C0C0C'    # Almost black for player 2
        self.HIGHLIGHT = '#CD853F'      # Peru brown for hover effect
        
    def create_gui(self):
        """
        Create and arrange all GUI elements.
        
        Sets up the main container frame with a wooden texture and
        arranges all game elements:
        - Game board grid
        - Control buttons
        - Player turn indicator
        """
        # Main container with wooden texture
        self.main_frame = tk.Frame(
            self.window,
            bg='#DEB887',  # Burlywood for frame
            bd=15,
            relief='ridge'
        )
        self.main_frame.pack(padx=20, pady=20)
        
        # Create game elements
        self.create_board()
        self.create_controls()
        
        # Player turn indicator
        self.player_label = tk.Label(
            self.main_frame,
            text="White player's turn",
            font=('Arial', 14, 'bold'),
            bg='#DEB887',
            fg='#4A3210'
        )
        self.player_label.grid(row=5, column=0, columnspan=4, pady=15)
        
    def create_board(self):
        """
        Create the interactive game board.
        
        Builds a 4x4 grid of canvases, each representing a cell.
        Each cell includes:
        - Wood grain background effect
        - Recessed area for balls
        - Interactive hover effects
        - Click handling
        - Visual effects (shadow, shine)
        """
        # Board container with raised border
        grid_frame = tk.Frame(
            self.main_frame,
            bg='#A0522D',
            bd=8,
            relief='raised'
        )
        grid_frame.grid(
            row=0, column=0,
            rowspan=4, columnspan=4,
            padx=10, pady=10
        )
        
        # Save reference to grid_frame
        self.grid_frame = grid_frame
        
        # Create 4x4 grid of cells
        for i in range(4):
            canvas_row = []
            circle_row = []
            for j in range(4):
                # Create cell canvas
                canvas = tk.Canvas(
                    grid_frame,
                    width=self.CELL_SIZE,
                    height=self.CELL_SIZE,
                    bg=self.BOARD_COLOR,
                    highlightthickness=1,
                    highlightbackground='#6B4423'
                )
                canvas.grid(row=i, column=j, padx=3, pady=3)
                
                # Add wood grain effect
                for k in range(0, self.CELL_SIZE, 8):
                    canvas.create_line(
                        0, k,
                        self.CELL_SIZE, k,
                        fill='#966F33',
                        width=1,
                        stipple='gray50'
                    )
                
                # Create recessed area
                canvas.create_oval(
                    self.CIRCLE_PADDING - 2,
                    self.CIRCLE_PADDING - 2,
                    self.CELL_SIZE - self.CIRCLE_PADDING + 2,
                    self.CELL_SIZE - self.CIRCLE_PADDING + 2,
                    fill=self.EMPTY_COLOR,
                    outline='#4A3210'
                )
                
                # Create ball placeholder
                circle = canvas.create_oval(
                    self.CIRCLE_PADDING,
                    self.CIRCLE_PADDING,
                    self.CELL_SIZE - self.CIRCLE_PADDING,
                    self.CELL_SIZE - self.CIRCLE_PADDING,
                    fill=self.EMPTY_COLOR,
                    outline=''
                )
                
                # Add initial shine effect
                highlight_size = self.CIRCLE_PADDING + 10
                canvas.create_oval(
                    highlight_size,
                    highlight_size,
                    highlight_size + 15,
                    highlight_size + 15,
                    fill='white',
                    stipple='gray50',
                    outline=''
                )
                
                # Bind interactions
                canvas.bind('<Button-1>',
                            lambda e, r=i, c=j: self.make_move(r, c))
                canvas.bind('<Enter>',
                            lambda e, c=canvas: self.on_enter(c))
                canvas.bind('<Leave>',
                            lambda e, c=canvas: self.on_leave(c))
                
                canvas_row.append(canvas)
                circle_row.append(circle)
            self.canvases.append(canvas_row)
            self.circles.append(circle_row)

        # Create orbit button in center of board
        orbit_size = 40
        orbit_canvas = tk.Canvas(
            grid_frame,
            width=orbit_size,
            height=orbit_size,
            bg='#A0522D',
            highlightthickness=0
        )
        orbit_canvas.place(
            in_=grid_frame,
            relx=0.5,
            rely=0.5,
            anchor="center"
        )
        
        # Create circular button with wooden effect
        self.orbit_button = orbit_canvas.create_oval(
            2, 2,
            orbit_size-2, orbit_size-2,
            fill='#8B4513',
            outline='#654321',
            width=2,
            tags='orbit'
        )
        
        # Add shine effect to orbit button
        orbit_canvas.create_oval(
            orbit_size//4, orbit_size//4,
            orbit_size//2, orbit_size//2,
            fill='white',
            stipple='gray50',
            outline='',
            tags='shine'
        )
        
        self.orbit_canvas = orbit_canvas
        self.orbit_animation_state = {'angle': 0, 'active': False}
    
    def create_controls(self):
        """
        Create the game control buttons.
        
        Sets up:
        - Orbit (rotation) button - initially disabled
        - New Game button
        Both buttons use consistent wooden styling.
        """
        button_frame = tk.Frame(self.main_frame, bg='#DEB887')
        button_frame.grid(row=4, column=0, columnspan=4, pady=15)
        
        # Common button styling
        button_style = {
            'font': ('Arial', 12, 'bold'),
            'bg': '#8B4513',
            'fg': '#FFE4B5',
            'activebackground': '#A0522D',
            'activeforeground': '#FFE4B5',
            'width': 15,
            'height': 1,
            'bd': 4,
            'relief': 'raised'
        }
        
        # New Game button
        new_game_button = tk.Button(
            button_frame,
            text="New Game",
            command=self.new_game,
            **button_style
        )
        new_game_button.pack(side=tk.LEFT, padx=10)
        
        # AI toggle button
        self.ai_button = tk.Button(
            button_frame,
            text="Play vs AI",
            command=self.toggle_ai,
            **button_style
        )
        self.ai_button.pack(side=tk.LEFT, padx=10)
        
    def on_enter(self, canvas):
        """
        Handle mouse enter event for a cell.
        
        Args:
            canvas (tk.Canvas): The canvas being hovered over
            
        Changes background color to highlight available moves.
        """
        if canvas['bg'] == self.BOARD_COLOR:
            canvas['bg'] = self.HIGHLIGHT

    def animate_orbit(self):
        """Animate the orbit button rotation."""
        if not self.orbit_animation_state['active']:
            return
            
        self.orbit_animation_state['angle'] += 10
        angle = self.orbit_animation_state['angle']
        
        # Update rotation visual
        for widget in self.grid_frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.itemconfig('orbit', fill='#CD853F')  # Highlight during animation
        
        if angle < 360:
            self.window.after(20, self.animate_orbit)  # Continue animation
        else:
            # Reset animation state
            self.orbit_animation_state['angle'] = 0
            self.orbit_animation_state['active'] = False
            for widget in self.grid_frame.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.itemconfig('orbit', fill='#8B4513')  # Return to original color
    
    def on_leave(self, canvas):
        """
        Handle mouse leave event for a cell.
        
        Args:
            canvas (tk.Canvas): The canvas no longer being hovered
            
        Restores original background color.
        """
        if canvas['bg'] == self.HIGHLIGHT:
            canvas['bg'] = self.BOARD_COLOR
    
    def toggle_ai(self):
        """Toggle AI opponent on/off."""
        self.against_ai = not self.against_ai
        if self.against_ai:
            self.ai_button.config(text="Play vs Human")
            # Créer une IA avec difficulté moyenne par défaut
            self.ai_player = MinimaxAI(2, difficulty='medium')
        else:
            self.ai_button.config(text="Play vs AI")
            self.ai_player = None
        self.new_game()

    def orbit_move(self):
        """
        Handle the orbit (rotation) move.
        """
        white_wins, black_wins = self.game.orbit_move()
        self.update_display()
        
        if white_wins:
            messagebox.showinfo("Victory", "White player wins!")
            self.new_game()
        elif black_wins:
            messagebox.showinfo("Victory", "Black player wins!")
            self.new_game()
        elif self.game.is_board_full():
            messagebox.showinfo("Draw!", "Draw!")
            self.new_game()
        else:
            self.player_label.config(
                text=f"{'White' if self.game.get_current_player() == 1 else 'Black'} player's turn"
            )
            self.orbit_button['state'] = 'disabled'
            
            # If it's AI's turn after orbiting, make AI move
            if self.against_ai and self.game.get_current_player() == self.ai_player.player:
                self.window.after(500, self.make_ai_move)  # 500ms delay for better UX

    def make_move(self, row, col):
        """
        Handle a move attempt at specified position and automatically orbit.
        """
        if self.game.make_move(row, col):
            color = self.WHITE_PIECE if self.game.get_current_player() == 1 else self.BLACK_PIECE
            canvas = self.canvases[row][col]
            circle = self.circles[row][col]
            self.add_shine_effect(canvas, circle, color)
            
            # Faire l'orbitage automatiquement après un court délai
            self.window.after(500, self.auto_orbit)

    def auto_orbit(self):
        """Automatically perform the orbit move with animation."""
        self.orbit_animation_state['active'] = True
        self.animate_orbit()  # Start animation
        
        # Perform actual orbit move after animation
        def complete_orbit():
            white_wins, black_wins = self.game.orbit_move()
            self.update_display()
            
            if white_wins:
                messagebox.showinfo("Victory", "White player wins!")
                self.new_game()
            elif black_wins:
                messagebox.showinfo("Victory", "Black player wins!")
                self.new_game()
            elif self.game.is_board_full():
                messagebox.showinfo("Draw!", "Draw!")
                self.new_game()
            else:
                # Mise à jour du texte et s'assurer que le jeu continue
                self.player_label.config(
                    text=f"{'White' if self.game.get_current_player() == 1 else 'Black'} player's turn"
                )
                self.game.move_made = False  # Réinitialiser l'état du mouvement
                
                # Si c'est le tour de l'IA après l'orbitage
                if self.against_ai and self.game.get_current_player() == self.ai_player.player:
                    self.window.after(500, self.make_ai_move)
        
        # Execute orbit after animation
        self.window.after(360, complete_orbit)  # Time matched to animation duration

    def make_ai_move(self):
        """
        Execute AI's move and trigger orbit automatically.
        """
        if self.ai_player and not self.game.is_board_full():
            move = self.ai_player.get_best_move(self.game)
            if move:
                row, col = move
                if self.game.make_move(row, col):
                    # Update display for AI move
                    color = self.WHITE_PIECE if self.game.get_current_player() == 1 else self.BLACK_PIECE
                    canvas = self.canvases[row][col]
                    circle = self.circles[row][col]
                    self.add_shine_effect(canvas, circle, color)
                    
                    # Trigger orbit after AI move
                    self.window.after(500, self.auto_orbit)
         
    def add_shine_effect(self, canvas, circle, color):
        """
        Add shine effect to a ball.
        
        Args:
            canvas (tk.Canvas): Canvas containing the ball
            circle (int): Canvas item ID for the ball
            color (str): Hex color code for the ball
            
        Creates realistic ball appearance with:
        - Base color
        - Highlight/shine effect
        """
        canvas.itemconfig(circle, fill=color)
        highlight_size = self.CIRCLE_PADDING + 10
        canvas.create_oval(
            highlight_size,
            highlight_size,
            highlight_size + 15,
            highlight_size + 15,
            fill='white',
            stipple='gray50',
            outline=''
        )
    
    def update_display(self):
        """
        Update the visual display of the game board.
        
        Synchronizes the visual representation with current game state:
        - Updates all cell colors
        - Reapplies visual effects
        """
        board = self.game.get_board()
        for i in range(4):
            for j in range(4):
                canvas = self.canvases[i][j]
                circle = self.circles[i][j]
                if board[i][j] == 0:
                    canvas.itemconfig(circle, fill=self.EMPTY_COLOR)
                elif board[i][j] == 1:
                    self.add_shine_effect(canvas, circle, self.WHITE_PIECE)
                else:
                    self.add_shine_effect(canvas, circle, self.BLACK_PIECE)
    
    def new_game(self):
        """
        Start a new game.
        
        Resets:
        - Game logic
        - Board display
        - Button states
        - Turn indicator
        """
    def new_game(self):
        """
        Start a new game.
        
        Resets:
        - Game logic
        - Board display
        - Animation states
        - Turn indicator
        """
        # Reset game logic
        self.game.reset_game()
        
        # Reset animation state
        self.orbit_animation_state = {'angle': 0, 'active': False}
        
        # Reset orbit button appearance
        self.orbit_canvas.itemconfig('orbit', fill='#8B4513')
        
        # Reset display
        for i in range(4):
            for j in range(4):
                canvas = self.canvases[i][j]
                circle = self.circles[i][j]
                canvas.itemconfig(circle, fill=self.EMPTY_COLOR)
        
        # Reset turn indicator
        self.player_label.config(text="White player's turn")
        
        # If against AI and AI is white (player 1), make AI move
        if self.against_ai and self.ai_player.player == 1:
            self.window.after(500, self.make_ai_move)
        
    def run(self):
        """
        Start the game interface.
        
        Launches the main event loop that:
        - Handles user input
        - Updates display
        - Processes game logic
        """
        self.window.mainloop()