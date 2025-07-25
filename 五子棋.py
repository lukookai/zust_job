import tkinter as tk
from tkinter import messagebox


class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋游戏")

        # 游戏变量初始化
        self.board_size = 15
        self.cell_size = 40
        self.margin = 30
        self.record = []  # 记录已下的棋子
        self.black_turn = True  # 黑棋先行

        # 直接创建游戏画布
        self.canvas_width = self.board_size * self.cell_size + 2 * self.margin
        self.canvas_height = self.board_size * self.cell_size + 2 * self.margin
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="burlywood")
        self.canvas.pack()

        # 绘制棋盘
        self.draw_board()

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.callback1)  # 左键黑棋
        self.canvas.bind("<Button-3>", self.callback2)  # 右键白棋

        # 添加重新开始按钮
        self.restart_button = tk.Button(self.root, text="重新开始", command=self.reset_game)
        self.restart_button.pack(pady=10)

    def draw_board(self):
        # 绘制棋盘网格
        for i in range(self.board_size):
            # 横线
            self.canvas.create_line(
                self.margin,
                self.margin + i * self.cell_size,
                self.margin + (self.board_size - 1) * self.cell_size,
                self.margin + i * self.cell_size
            )
            # 竖线
            self.canvas.create_line(
                self.margin + i * self.cell_size,
                self.margin,
                self.margin + i * self.cell_size,
                self.margin + (self.board_size - 1) * self.cell_size
            )

        # 绘制五个小黑点
        dots = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for x, y in dots:
            self.canvas.create_oval(
                self.margin + x * self.cell_size - 5,
                self.margin + y * self.cell_size - 5,
                self.margin + x * self.cell_size + 5,
                self.margin + y * self.cell_size + 5,
                fill="black"
            )

    def callback1(self, event):
        if not self.black_turn:
            return

        # 计算点击的棋盘位置
        x, y = event.x, event.y
        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)

        # 检查是否在棋盘范围内
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            pos = row * self.board_size + col
            if pos not in self.record:
                # 记录位置
                self.record.append(pos)
                # 绘制黑棋
                self.draw_piece(row, col, "black")
                # 检查是否胜利
                if self.check_win(row, col, "black"):
                    messagebox.showinfo("游戏结束", "黑方获胜!")
                    self.reset_game()
                else:
                    self.black_turn = False  # 轮到白方

    def callback2(self, event):
        if self.black_turn:
            return

        # 计算点击的棋盘位置
        x, y = event.x, event.y
        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)

        # 检查是否在棋盘范围内
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            pos = row * self.board_size + col
            if pos not in self.record:
                # 记录位置
                self.record.append(pos)
                # 绘制白棋
                self.draw_piece(row, col, "white")
                # 检查是否胜利
                if self.check_win(row, col, "white"):
                    messagebox.showinfo("游戏结束", "白方获胜!")
                    self.reset_game()
                else:
                    self.black_turn = True  # 轮到黑方

    def draw_piece(self, row, col, color):
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        radius = self.cell_size // 2 - 2
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def check_win(self, row, col, color):
        directions = [
            (1, 0),  # 水平
            (0, 1),  # 垂直
            (1, 1),  # 对角线
            (1, -1)  # 反对角线
        ]

        for dr, dc in directions:
            count = 1  # 当前棋子

            # 正向检查
            r, c = row + dr, col + dc
            while 0 <= r < self.board_size and 0 <= c < self.board_size:
                pos = r * self.board_size + c
                if pos in self.record and self.get_piece_color(r, c) == color:
                    count += 1
                    r += dr
                    c += dc
                else:
                    break

            # 反向检查
            r, c = row - dr, col - dc
            while 0 <= r < self.board_size and 0 <= c < self.board_size:
                pos = r * self.board_size + c
                if pos in self.record and self.get_piece_color(r, c) == color:
                    count += 1
                    r -= dr
                    c -= dc
                else:
                    break

            if count >= 5:
                return True

        return False

    def get_piece_color(self, row, col):
        pos = row * self.board_size + col
        index = self.record.index(pos)
        return "black" if index % 2 == 0 else "white"

    def reset_game(self):
        self.canvas.delete("all")
        self.draw_board()
        self.record = []
        self.black_turn = True


if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()