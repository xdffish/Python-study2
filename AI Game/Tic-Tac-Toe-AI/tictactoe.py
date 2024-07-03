# 这个程序是一个井字棋游戏，使用了Tkinter库来创建图形用户界面。
# 程序包含了检查玩家是否获胜的函数、检查棋盘是否已满的函数以及使用Minimax算法计算最佳移动的函数。



import tkinter as tk # 提供基本的GUI小部件库
from tkinter import messagebox # 提供用于显示消息框的不同对话框集
import random



# 检查是否有玩家获胜
def check_winner(board, player):
    # 检查行、列和对角线是否有胜利
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# 检查棋盘是否已满
def is_board_full(board):
    return all(all(cell != ' ' for cell in row) for row in board)

# Minimax算法，用于计算最佳移动
def minimax(board, depth, is_maximizing):
    if check_winner(board, 'X'):
        return -1
    if check_winner(board, 'O'):
        return 1
    if is_board_full(board): # 如果棋盘已满，终止
        return 0

    if is_maximizing: # 递归方法填充O
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False) # 递归
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
        return max_eval
    else: # 递归方法填充X
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True) # 递归
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
        return min_eval

# 确定当前玩家的最佳移动，返回表示位置的元组
def best_move(board):
    best_val = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, 0, False)
                board[i][j] = ' '
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    return best_move

# 执行玩家的移动
def make_move(row, col):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        buttons[row][col].config(text='X')
        if check_winner(board, 'X'):
            messagebox.showinfo("井字棋", "你赢了!")
            root.quit()
        elif is_board_full(board):
            messagebox.showinfo("井字棋", "平局!")
            root.quit()
        else:
            ai_move()
    else:
        messagebox.showerror("错误", "无效的移动")

# AI的回合
def ai_move():
    row, col = best_move(board)
    board[row][col] = 'O'
    buttons[row][col].config(text='O')
    if check_winner(board, 'O'):
        messagebox.showinfo("井字棋", "AI赢了!")
        root.quit()
    elif is_board_full(board):
        messagebox.showinfo("井字棋", "平局!")
        root.quit()

# 创建主窗口
root = tk.Tk()
root.title("井字棋")

# 初始化棋盘和按钮
board = [[' ' for _ in range(3)] for _ in range(3)]
buttons = []

# 创建按钮并将其放置在网格中
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(root, text=' ', font=('normal', 30), width=5, height=2, command=lambda row=i, col=j: make_move(row, col))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

# 运行主循环
root.mainloop()
