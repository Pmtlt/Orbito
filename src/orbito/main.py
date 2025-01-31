"""
Main entry point for the Orbito game.
"""

import sys
import traceback
import tkinter as tk
from tkinter import messagebox

# Changez les imports relatifs en imports absolus
from orbito.gui.interface import OrbitInterface
from orbito.core.game import OrbitGame

def main():
    """
    Launch the Orbito game application.
    """
    try:
        # Create and run game interface
        game = OrbitInterface()
        game.run()
        return 0
        
    except tk.TclError as e:
        error_msg = "Failed to start game: No display available.\n"
        error_msg += "Make sure you're running in a graphical environment."
        print(error_msg, file=sys.stderr)
        return 1
        
    except Exception as e:
        error_msg = "An unexpected error occurred:\n\n"
        error_msg += str(e) + "\n\n"
        error_msg += "Please report this error to the developers."
        
        try:
            messagebox.showerror("Error", error_msg)
        except:
            print(error_msg, file=sys.stderr)
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())