import tkinter as tk
import random

# Game configuration
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"
TOP_BAR_HEIGHT = 50  # reserve space at top for score and dropdown

# List of colors to choose for the snake
SNAKE_COLORS = ["green", "blue", "yellow", "purple", "orange", "pink"]

class Snake:
    def __init__(self, color):
        self.body_size = BODY_PARTS
        self.color = color
        self.coordinates = []
        self.squares = []
        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=self.color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def start_game():
    global snake, food, direction, score, game_running
    game_running = True
    direction = 'down'
    score = 0
    label_score.config(text=f"Score: {score}")
    canvas.delete(tk.ALL)
    btn_restart.place_forget()
    btn_exit.place_forget()
    chosen_color = snake_color_var.get()
    snake = Snake(chosen_color)
    food = Food()
    next_turn(snake, food)

def next_turn(snake, food):
    if not game_running:
        return
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake.color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label_score.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == "left" and direction != "right":
        direction = "left"
    elif new_direction == "right" and direction != "left":
        direction = "right"
    elif new_direction == "up" and direction != "down":
        direction = "up"
    elif new_direction == "down" and direction != "up":
        direction = "down"

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global game_running
    game_running = False
    canvas.create_text(
        GAME_WIDTH / 2, GAME_HEIGHT / 2,
        font=('Arial', 50), text="GAME OVER", fill="red"
    )
    btn_restart.place(relx=0.4, rely=0.5)
    btn_exit.place(relx=0.55, rely=0.5)

def on_exit():
    window.destroy()

window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT + TOP_BAR_HEIGHT}")

# Dropdown variable and menu for snake color selection placed top-right
snake_color_var = tk.StringVar(window)
snake_color_var.set(SNAKE_COLORS[0])  # default

color_label = tk.Label(window, text="Select Snake Color:", font=('Arial', 12))
color_label.place(relx=0.8, rely=0.02, anchor='ne')

color_menu = tk.OptionMenu(window, snake_color_var, *SNAKE_COLORS)
color_menu.place(relx=0.98, rely=0.02, anchor='ne')

# Score label placed top-left
label_score = tk.Label(window, text="Score: 0", font=('Arial', 24), fg="white", bg=BACKGROUND_COLOR)
label_score.place(relx=0.01, rely=0.02, anchor='nw')

# Game canvas placed below top bar area
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.place(x=0, y=TOP_BAR_HEIGHT)

# Restart and Exit buttons, initially hidden
btn_restart = tk.Button(window, text="Restart", font=('Arial', 16), command=start_game)
btn_exit = tk.Button(window, text="Exit", font=('Arial', 16), command=on_exit)

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

game_running = True
start_game()
window.mainloop()
