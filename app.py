import streamlit as st
import numpy as np
from PIL import Image, ImageDraw

# Constants
GRID_SIZE = 3
CELL_SIZE = 100
LINE_WIDTH = 5
BOARD_SIZE = CELL_SIZE * GRID_SIZE
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)

# Initialize the game state
if 'game_board' not in st.session_state:
    st.session_state.game_board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Check for win condition
def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(GRID_SIZE):
        if all(board[row][col] == player for row in range(GRID_SIZE)):
            return True
    if all(board[i][i] == player for i in range(GRID_SIZE)) or all(board[i][GRID_SIZE - 1 - i] == player for i in range(GRID_SIZE)):
        return True
    return False

# Draw the game board and symbols (X/O)
def draw_board(board):
    image = Image.new("RGB", (BOARD_SIZE, BOARD_SIZE), BG_COLOR)
    draw = ImageDraw.Draw(image)

    # Draw the grid lines
    for i in range(1, GRID_SIZE):
        draw.line([(i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE)], fill=LINE_COLOR, width=LINE_WIDTH)
        draw.line([(0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE)], fill=LINE_COLOR, width=LINE_WIDTH)

    # Draw Xs and Os
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'X':
                offset = CELL_SIZE // 4
                draw.line([(col * CELL_SIZE + offset, row * CELL_SIZE + offset),
                           ((col + 1) * CELL_SIZE - offset, (row + 1) * CELL_SIZE - offset)],
                          fill=LINE_COLOR, width=LINE_WIDTH)
                draw.line([((col + 1) * CELL_SIZE - offset, row * CELL_SIZE + offset),
                           (col * CELL_SIZE + offset, (row + 1) * CELL_SIZE - offset)],
                          fill=LINE_COLOR, width=LINE_WIDTH)
            elif board[row][col] == 'O':
                offset = CELL_SIZE // 4
                draw.ellipse([(col * CELL_SIZE + offset, row * CELL_SIZE + offset),
                              ((col + 1) * CELL_SIZE - offset, (row + 1) * CELL_SIZE - offset)],
                             outline=LINE_COLOR, width=LINE_WIDTH)
    
    return image

# Handle player move
def handle_click(row, col):
    if st.session_state.game_board[row][col] == ' ' and not st.session_state.game_over:
        st.session_state.game_board[row][col] = st.session_state.current_player

        if check_win(st.session_state.game_board, st.session_state.current_player):
            st.success(f"Player {st.session_state.current_player} wins!")
            st.session_state.game_over = True
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

# Streamlit layout
st.title("Tic-Tac-Toe")
st.write("Player 1: X, Player 2: O")

# Display the board as an image
board_image = draw_board(st.session_state.game_board)
st.image(board_image, caption='Tic-Tac-Toe', use_column_width=True)

# Create clickable buttons for each cell
for row in range(GRID_SIZE):
    cols = st.columns(GRID_SIZE)
    for col in range(GRID_SIZE):
        if cols[col].button(f"{st.session_state.game_board[row][col]}", key=f"{row}_{col}", disabled=st.session_state.game_board[row][col] != ' '):
            handle_click(row, col)

# Reset button
if st.button("Restart Game"):
    st.session_state.game_board = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
