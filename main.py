import tkinter as tk
import json
import random
import tkinter.messagebox


class SnakeGame:
    def __init__(self, root, block_size, obstacles_file):
        self.root = root
        self.block_size = block_size
        self.load_data(obstacles_file)

        self.root.title("Snake Game")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.create_start_screen()

        self.score = 0
        self.high_score = 0
        self.snake = [(self.width // 2, self.height // 2),
                      (self.width // 2 - self.block_size, self.height // 2)]
        self.food = self.generate_food()
        self.direction = None
        self.game_over = False
        self.game_started = False

        self.root.after(0, self.wait_for_start)

    def load_data(self, obstacles_file):
        with open(obstacles_file, "r") as file:
            data = json.load(file)

        self.width, self.height = data["dimensiuniTabla"]["width"], data["dimensiuniTabla"]["height"]
        self.obstacles = [(obs["x"], obs["y"]) for obs in data["obstacole"]]

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
        return [(obs["x"] // self.block_size * self.block_size, obs["y"] // self.block_size * self.block_size) for obs
                in obstacles_data]

    def wait_for_start(self):
        if not self.game_started:
            self.root.after(100, self.wait_for_start)
        else:
            pass

    def start_game(self, event=None):
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
            x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
            y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size
            if (x, y) not in self.snake and all((x != obs[0] or y != obs[1]) for obs in self.obstacles):
                return x, y

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            x, y = obstacle
            self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill="red")

    def draw_snake(self):
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill="green")

    def draw_food(self):
        x, y = self.food
        self.canvas.create_oval(x, y, x + self.block_size, y + self.block_size, fill="red")

    def update(self):
        if not self.game_over:
            x, y = self.snake[0]

            if self.direction == "Left":
                x -= self.block_size
            elif self.direction == "Right":
                x += self.block_size
            elif self.direction == "Up":
                y -= self.block_size
            elif self.direction == "Down":
                y += self.block_size

            if (x, y) in self.snake or x < 0 or x >= self.width or y < 0 or y >= self.height or any(
                    (x, y) == obs for obs in self.obstacles):
                self.game_over = True
                self.display_game_over()
                return

            self.snake.insert(0, (x, y))

            if (x, y) == self.food:
                self.score += 1
                self.food = self.generate_food()
            else:
                self.snake.pop()

            self.canvas.delete("all")
            self.draw_obstacles()
            self.draw_snake()
            self.draw_food()

            self.root.after(100, self.update)
        else:
            self.display_game_over()

    def display_game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score

        game_over_message = f"GAME OVER\nScorul tau: {self.score}\nHigh Score: {self.high_score}\n\nPlay again?"
        if tk.messagebox.askyesno("Game Over", game_over_message):
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        self.canvas.delete("all")

        self.score = 0
        self.game_over = False
        self.game_started = False

        initial_position_x = self.width // 2
        initial_position_y = self.height // 2
        self.snake = [(initial_position_x, initial_position_y),
                      (initial_position_x - self.block_size, initial_position_y)]
        self.direction = None

        self.food = self.generate_food()

        self.draw_obstacles()
        self.draw_snake()
        self.draw_food()

        start_message = "Press W, A, S, D to start"
        self.canvas.create_text(self.width // 2, self.height // 2, text=start_message, fill="black", font=("Arial", 16))

        self.canvas.bind_all("<KeyPress>", self.on_key_press)

        self.root.after(0, self.wait_for_start)


def start_game():
    obstacles_file = "tabla.json"
    root = tk.Tk()
    game = SnakeGame(root, block_size=20, obstacles_file=obstacles_file)
    root.mainloop()


if __name__ == "__main__":
    start_game()
