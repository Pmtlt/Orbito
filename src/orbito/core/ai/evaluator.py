"""Board evaluation functions for AI."""

def count_aligned_pieces(board, player, length):
    """Count number of aligned pieces of given length."""
    count = 0
    # Horizontal check
    for row in board:
        for i in range(5-length):
            if all(cell == player for cell in row[i:i+length]):
                count += 1
    
    # Vertical check
    for col in range(4):
        for i in range(5-length):
            if all(board[i+j][col] == player for j in range(length)):
                count += 1
                
    # Diagonal checks
    for i in range(5-length):
        for j in range(5-length):
            # Main diagonal
            if all(board[i+k][j+k] == player for k in range(length)):
                count += 1
            # Other diagonal
            if all(board[i+k][j+length-1-k] == player for k in range(length)):
                count += 1
    return count

def evaluate_position(game, ai_player):
    """
    Evaluate current board position.
    
    Returns:
        int: Score (positive favors AI, negative favors opponent)
    """
    score = 0
    board = game.get_board()
    opponent = 3 - ai_player
    
    # Check for wins
    if game.check_win_for_player(ai_player):
        return 1000
    if game.check_win_for_player(opponent):
        return -1000
        
    # Count aligned pieces
    score += count_aligned_pieces(board, ai_player, 3) * 50  # 3 aligned
    score += count_aligned_pieces(board, ai_player, 2) * 10  # 2 aligned
    score -= count_aligned_pieces(board, opponent, 3) * 50   # opponent 3 aligned
    score -= count_aligned_pieces(board, opponent, 2) * 10   # opponent 2 aligned
    
    # Control of center
    center_positions = [(1,1), (1,2), (2,1), (2,2)]
    for row, col in center_positions:
        if board[row][col] == ai_player:
            score += 5
        elif board[row][col] == opponent:
            score -= 5
            
    return score