import tkinter as tk
import random

# Constants
WIDTH = 400
HEIGHT = 300
PADDLE_WIDTH = 60
PADDLE_HEIGHT = 10
BALL_SIZE = 10
BRICK_WIDTH = 50
BRICK_HEIGHT = 20
ROWS = 5
COLS = 8

class BrickBreaker:
    def __init__(self, root):
        self.root = root
        self.root.title("Brick Breaker")
        
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.paddle = self.canvas.create_rectangle(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, 
                                                    WIDTH // 2 + PADDLE_WIDTH // 2, HEIGHT - 10, fill="blue")
        self.ball = self.canvas.create_oval(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, 
                                             WIDTH // 2 + BALL_SIZE // 2, HEIGHT // 2 + BALL_SIZE // 2, fill="red")
        
        self.bricks = []
        self.create_bricks()
        
        self.dx = 3
        self.dy = -3
        
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        
        self.update()

    def create_bricks(self):
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * (BRICK_WIDTH + 5) + 10
                y1 = row * (BRICK_HEIGHT + 5) + 30
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                self.bricks.append(brick)

    def move_left(self, event):
        self.canvas.move(self.paddle, -20, 0)

    def move_right(self, event):
        self.canvas.move(self.paddle, 20, 0)

    def update(self):
        self.canvas.move(self.ball, self.dx, self.dy)
        ball_pos = self.canvas.coords(self.ball)
        
        # Check for collision with walls
        if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
            self.dx = -self.dx
        if ball_pos[1] <= 0:
            self.dy = -self.dy
        
        # Check for collision with paddle
        paddle_pos = self.canvas.coords(self.paddle)
        if (ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2] and
            ball_pos[3] >= paddle_pos[1] and ball_pos[3] <= paddle_pos[3]):
            self.dy = -self.dy
            self.canvas.move(self.ball, 0, -1)  # Move the ball up to avoid getting stuck
        
        # Check for collision with bricks
        for brick in self.bricks:
            brick_pos = self.canvas.coords(brick)
            if (ball_pos[2] >= brick_pos[0] and ball_pos[0] <= brick_pos[2] and
                ball_pos[3] >= brick_pos[1] and ball_pos[1] <= brick_pos[3]):
                self.dy = -self.dy
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                break
        
        # Check if the ball falls below the paddle
        if ball_pos[3] >= HEIGHT:
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over", fill="white", font=("Arial", 24))
            return
        
        self.root.after(20, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = BrickBreaker(root)
    root.mainloop()