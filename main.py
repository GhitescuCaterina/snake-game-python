import tkinter as tk
import json
import random
import tkinter.messagebox


class SnakeGame:
    def __init__(self, root, width, height, obstacles_file, block_size):
        self.root = root
        self.root.title("Snake Game")
        self.width = width
        self.height = height
        self.block_size = block_size
        self.obstacles = self.load_obstacles(obstacles_file)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.create_start_screen()

        self.score = 0
        self.high_score = 0

        self.snake = [(self.width // 2, self.height // 2), (self.width // 2 - self.block_size, self.height // 2)]
        self.food = self.generate_food()

        self.direction = None
        self.game_over = False
        self.game_started = False

        # Înlătură apelurile de desenare și comentariile legate de canvas
        # self.draw_obstacles()
        # self.draw_snake()
        # self.draw_food()

        self.root.after(0, self.wait_for_start)

    def create_start_screen(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack()

        play_button = tk.Button(self.start_frame, text="Play", command=self.start_game)
        play_button.pack(pady=10)

        how_to_play_button = tk.Button(self.start_frame, text="How to Play", command=self.show_instructions)
        how_to_play_button.pack(pady=10)

        quit_button = tk.Button(self.start_frame, text="Quit", command=self.root.quit)
        quit_button.pack(pady=10)

    def show_instructions(self):
        instructions = "                     Instructiuni:\n\n" \
                       "Foloseste W, A, S, D pentru a misca pitonul.\n" \
                       "             Mananca pentru a creste.\n" \
                       "     Nu intra in margini sau in obstacole.\n" \
                       "         Nu iti manca propria coada !!"
        tk.messagebox.showinfo("How to Play", instructions)

    def on_key_press(self, event):
        if not self.game_started:
            if event.keysym in ['w', 'a', 's', 'd']:
                self.direction = {"w": "Up", "a": "Left", "s": "Down", "d": "Right"}.get(event.keysym, None)
                if self.direction:
                    self.game_started = True
                    self.canvas.delete("all")
                    self.update()
        else:
            if event.keysym == 'a' and self.direction != "Right":
                self.direction = "Left"
            elif event.keysym == 'd' and self.direction != "Left":
                self.direction = "Right"
            elif event.keysym == 'w' and self.direction != "Down":
                self.direction = "Up"
            elif event.keysym == 's' and self.direction != "Up":
                self.direction = "Down"

    def load_obstacles(self, obstacles_file):
        with open(obstacles_file, "r") as file:
            obstacles_data = json.load(file)
        return [(obstacle["x"], obstacle["y"]) for obstacle in obstacles_data]

    def wait_for_start(self):
        if not self.game_started:
            self.root.after(100, self.wait_for_start)
        else:
            pass

    def start_game(self):
        self.start_frame.pack_forget()

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.score = 0
        self.high_score = 0
        self.snake = [(self.width // 2, self.height // 2), (self.width // 2 - self.block_size, self.height // 2)]
        self.food = self.generate_food()
        self.direction = None
        self.game_over = False
        self.game_started = False

        self.canvas.bind_all("<KeyPress>", self.on_key_press)

        self.canvas.bind("<KeyPress-w>", self.start_game_up)
        self.canvas.bind("<KeyPress-a>", self.start_game_left)
        self.canvas.bind("<KeyPress-s>", self.start_game_down)
        self.canvas.bind("<KeyPress-d>", self.start_game_right)

        self.draw_obstacles()
        self.draw_snake()
        self.draw_food()

        start_message = "Incepe sa joci! Apasa W, A, S, D.\n\n"
        self.canvas.create_text(self.width // 2, self.height // 2, text=start_message, fill="black", font=("Arial", 16))

        self.root.after(0, self.wait_for_start)


    def start_game_up(self, event):
        if not self.game_started:
            self.direction = "Up"
            self.start_game(event)

    def start_game_down(self, event):
        if not self.game_started:
            self.direction = "Down"
            self.start_game(event)

    def start_game_left(self, event):
        if not self.game_started:
            self.direction = "Left"
            self.start_game(event)

    def start_game_right(self, event):
        if not self.game_started:
            self.direction = "Right"
            self.start_game(event)

    def move_left(self, event):
        try:
            if self.direction != "Right":
                self.direction = "Left"
        except Exception as e:
            print(f"Error in move_left: {e}")

    def move_right(self, event):
        try:
            if self.direction != "Left":
                self.direction = "Right"
        except Exception as e:
            print(f"Error in move_right: {e}")

    def move_up(self, event):
        try:
            if self.direction != "Down":
                self.direction = "Up"
        except Exception as e:
            print(f"Error in move_up: {e}")

    def move_down(self, event):
        try:
            if self.direction != "Up":
                self.direction = "Down"
        except Exception as e:
            print(f"Error in move_down: {e}")

    def generate_food(self):
        while True:
            x = random.randint(0, self.width // 10 - 1) * 10
            y = random.randint(0, self.height // 10 - 1) * 10
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                return x, y

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            x, y = obstacle
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red")

    def draw_snake(self):
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")

    def draw_food(self):
        x, y = self.food
        self.canvas.create_oval(x, y, x + 10, y + 10, fill="red")

    def update(self):
        if not self.game_over:
            x, y = self.snake[0]
            if self.direction == "Left":
                x -= 10
            elif self.direction == "Right":
                x += 10
            elif self.direction == "Up":
                y -= 10
            elif self.direction == "Down":
                y += 10

            if (x, y) in self.snake or (
                    x, y) in self.obstacles or x < 0 or x >= self.width or y < 0 or y >= self.height:
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                self.canvas.create_text(self.width // 2, self.height // 2, text="Game Over", fill="red",
                                        font=("Arial", 20))
                self.canvas.create_text(self.width // 2, self.height // 2 + 30, text=f"Score: {self.score}", fill="red")
                self.canvas.create_text(self.width // 2, self.height // 2 + 60, text=f"High Score: {self.high_score}",
                                        fill="red")
                return

            self.snake.insert(0, (x, y))

            if (x, y) == self.food:
                self.score += 1
                self.food = self.generate_food()
                self.draw_food()
            else:
                self.snake.pop()

            self.canvas.delete("all")
            self.draw_obstacles()
            self.draw_snake()
            self.draw_food()
            self.canvas.after(100, self.update)
        else:
            self.canvas.after(100, self.update)


def start_game():
    obstacles_file = "obstacol.json"
    root = tk.Tk()
    game = SnakeGame(root, 600, 600, obstacles_file, block_size=30)
    root.mainloop()


if __name__ == "__main__":
    start_game()
