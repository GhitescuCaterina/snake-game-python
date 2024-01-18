import tkinter as tk
import json
import random


class SnakeGame:
    # INITIALIZAREA SI CONFIGURAREA JOCULUI
    def __init__(self, root, block_size, obstacles_file):
        self.root = root
        self.root.configure(bg='lightblue')
        self.block_size = block_size
        self.load_data(obstacles_file)

        self.score_panel = tk.Frame(root, height=30, bg="lightblue")
        self.score_panel.pack(side="top", fill="x")
        self.score_label = tk.Label(self.score_panel, font=("Pixelify Sans", 16), bg="lightblue")
        self.score_label.pack()

        self.button_font = ("Pixelify Sans", 20, "bold")

        self.snake_color = "green"
        self.food_color = "red"
        self.obstacle_color = "blue"

        self.root.title("Snake Game")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.create_start_screen()

        self.score = 0
        self.high_score = 0
        self.snake = [(self.width // 2, self.height // 2 - block_size),
                      (self.width // 2 - block_size, self.height // 2 - block_size)]
        self.food = self.generate_food()
        self.obstacles = self.get_obstacles_for_level("usor")
        self.direction = None
        self.game_over = False
        self.game_started = False

        self.root.after(0, self.wait_for_start)

        self.level_config = {
            "usor": {"obstacole": 3, "viteza": 150},
            "normal": {"obstacole": 5, "viteza": 150},
            "hardcore": {"obstacole": 10, "viteza": 75}
        }

    def load_data(self, obstacles_file):
        with open(obstacles_file, "r") as file:
            self.data = json.load(file)

        self.width, self.height = self.data["dimensiuniTabla"]["width"], self.data["dimensiuniTabla"]["height"]
        self.obstacles = self.get_obstacles_for_level("usor")

    def get_obstacles_for_level(self, level):
        return [(obs["x"], obs["y"] + self.block_size) for obs in self.data["nivele"][level]["obstacole"]]

    def set_game_parameters(self, nivel):
        self.obstacles = [(obs["x"], obs["y"] + 2 * self.block_size) for obs in self.data["nivele"][nivel]["obstacole"]]
        config = self.level_config[nivel]
        self.update_speed = config["viteza"]

    def load_obstacles(self, obstacles_file):
        with open(obstacles_file, "r") as file:
            obstacles_data = json.load(file)
        return [(obs["x"] // self.block_size * self.block_size, obs["y"] // self.block_size * self.block_size) for obs
                in obstacles_data]

    # INTERFATA UTILIZATORULUI
    def create_start_screen(self):
        self.start_frame = tk.Frame(self.root, bg="lightblue")
        self.start_frame.pack(expand=True)

        title_label = tk.Label(self.start_frame, text="Snake Game", font=("Pixelify Sans", 36, "bold"), bg="lightblue")
        title_label.pack(pady=40)

        play_button = tk.Button(self.start_frame, text="Start", command=self.show_difficulty_options,
                                font=self.button_font, bg="lightgreen")
        play_button.pack(pady=10)

        how_to_play_button = tk.Button(self.start_frame, text="Cum se joaca?", command=self.show_instructions,
                                       font=self.button_font, bg="lightgreen")
        how_to_play_button.pack(pady=10)

        quit_button = tk.Button(self.start_frame, text="Quit", command=self.root.quit, font=self.button_font,
                                bg="lightgreen")
        quit_button.pack(pady=10)

    def show_difficulty_options(self):
        self.start_frame.pack_forget()
        self.difficulty_frame = tk.Frame(self.root, bg="lightblue")
        self.difficulty_frame.pack(expand=True)

        easy_button = tk.Button(self.difficulty_frame, text="Usor", command=lambda: self.start_game("usor"),
                                font=self.button_font, bg="#60db6d")
        easy_button.pack(pady=10)

        normal_button = tk.Button(self.difficulty_frame, text="Normal", command=lambda: self.start_game("normal"),
                                  font=self.button_font, bg="#dbd960")
        normal_button.pack(pady=10)

        hard_button = tk.Button(self.difficulty_frame, text="Greu", command=lambda: self.start_game("hardcore"),
                                font=self.button_font, bg="#c94747")
        hard_button.pack(pady=10)

        back_button = tk.Button(self.difficulty_frame, text="Inapoi", command=self.show_start_screen,
                                font=self.button_font)
        back_button.pack(pady=40)

    def show_instructions(self):
        self.start_frame.pack_forget()
        self.instructions_frame = tk.Frame(self.root, bg="lightblue")
        self.instructions_frame.pack(expand=True)

        instructions_text = "Instructiuni\n\n" \
                            "Foloseste W, A, S, D pentru a misca pitonul.\n" \
                            "Mananca pentru a creste.\n" \
                            "Nu intra in margini sau in obstacole.\n" \
                            "Nu iti manca propria coada !!"
        instructions_label = tk.Label(self.instructions_frame, text=instructions_text, font=("Pixelify Sans", 20),
                                      bg="lightblue")
        instructions_label.pack(pady=10)

        back_button = tk.Button(self.instructions_frame, text="Inapoi", command=self.show_start_screen,
                                font=self.button_font, bg="lightgreen")
        back_button.pack(pady=10)

    def show_start_screen(self):
        if hasattr(self, 'difficulty_frame'):
            self.difficulty_frame.pack_forget()
        if hasattr(self, 'instructions_frame'):
            self.instructions_frame.pack_forget()

        self.create_start_screen()

    # GESTIONAREA EVENIMENTELOR
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

    def wait_for_start(self):
        if not self.game_started:
            self.root.after(100, self.wait_for_start)
        else:
            pass

    def start_game(self, nivel="normal", event=None):
        self.start_frame.pack_forget()

        if hasattr(self, 'difficulty_frame'):
            self.difficulty_frame.pack_forget()

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.obstacles = self.get_obstacles_for_level(nivel)

        self.score = 0
        self.high_score = 0
        self.score_label.config(text=f"Scor: {self.score}   High Score: {self.high_score}")

        self.snake = [(self.width // 2, self.height // 2), (self.width // 2 - self.block_size, self.height // 2)]
        self.food = self.generate_food()
        self.direction = None
        self.game_over = False
        self.game_started = False

        self.current_level = nivel
        self.set_game_parameters(nivel)

        self.canvas.bind_all("<KeyPress>", self.on_key_press)

        self.canvas.bind("<KeyPress-w>", self.start_game_up)
        self.canvas.bind("<KeyPress-a>", self.start_game_left)
        self.canvas.bind("<KeyPress-s>", self.start_game_down)
        self.canvas.bind("<KeyPress-d>", self.start_game_right)

        self.draw_obstacles()
        self.draw_snake()
        self.draw_food()

        start_message = "Incepe sa joci! Apasa W, A, S, D.\n\n"
        self.canvas.create_text(self.width // 2, self.height // 2, text=start_message, fill="black",
                                font=("Pixelify Sans", 16))

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

    # LOGICA JOCULUI
    def generate_food(self):
        while True:
            x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
            y_min = self.score_panel.winfo_height() + self.block_size
            y_max = self.height - 3 * self.block_size
            y = random.randint(y_min // self.block_size, y_max // self.block_size) * self.block_size

            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                return x, y

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

            if x < 0 or x >= self.width or y < self.block_size or y >= self.height or \
                    (x, y) in self.snake[1:] or (x, y) in self.obstacles:
                self.game_over = True
                self.display_game_over()
                return

            self.snake.insert(0, (x, y))

            if (x, y) == self.food:
                self.score += 1
                self.food = self.generate_food()
                if self.score > self.high_score:
                    self.high_score = self.score
                self.score_label.config(text=f"Scor: {self.score}   High Score: {self.high_score}")
            else:
                self.snake.pop()

            self.canvas.delete("all")
            self.draw_obstacles()
            self.draw_snake()
            self.draw_food()

            self.root.after(self.update_speed, self.update)
        else:
            self.display_game_over()

    def display_game_over(self):
        game_over_window = tk.Toplevel(self.root)
        game_over_window.title("Game Over")

        game_over_label = tk.Label(game_over_window,
                                   text=f"GAME OVER\nScorul tau: {self.score}\nHigh Score: {self.high_score}\n\nVrei sa joci iar la acest nivel?",
                                   font=("Pixelify Sans", 16))
        game_over_label.pack(pady=10)

        yes_button = tk.Button(game_over_window, text="Da",
                               command=lambda: [self.reset_game(), game_over_window.destroy()])
        yes_button.pack(side="left", padx=(20, 10), pady=20)

        no_button = tk.Button(game_over_window, text="Nu",
                              command=lambda: [self.reset_to_start_screen(), game_over_window.destroy()])
        no_button.pack(side="right", padx=(10, 20), pady=20)

        game_over_window.update_idletasks()
        ww = game_over_window.winfo_width()
        wh = game_over_window.winfo_height()
        sw = game_over_window.winfo_screenwidth()
        sh = game_over_window.winfo_screenheight()
        x = int((sw - ww) / 2)
        y = int((sh - wh) / 2)
        game_over_window.geometry(f"{ww}x{wh}+{x}+{y}")

    def reset_to_start_screen(self):
        self.canvas.pack_forget()
        self.create_start_screen()

        self.score = 0
        self.game_over = False
        self.game_started = False
        self.snake = [(self.width // 2, self.height // 2),
                      (self.width // 2 - self.block_size, self.height // 2)]
        self.direction = None
        self.food = self.generate_food()

        self.score_label.config(text=f"Scor: {self.score}   High Score: {self.high_score}")

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
        self.canvas.create_text(self.width // 2, self.height // 2, text=start_message, fill="black",
                                font=("Pixelify Sans", 16))

        self.canvas.bind_all("<KeyPress>", self.on_key_press)

        self.root.after(0, self.wait_for_start)

    # DESENAREA GRAFICA
    def draw_snake(self):
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=self.snake_color)

    def draw_food(self):
        x, y = self.food
        self.canvas.create_oval(x, y, x + self.block_size, y + self.block_size, fill=self.food_color)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            x, y = obstacle
            self.canvas.create_rectangle(x, y, x + self.block_size, y + self.block_size, fill=self.obstacle_color)


def start_game():
    obstacles_file = "tabla.json"
    root = tk.Tk()
    game = SnakeGame(root, block_size=20, obstacles_file=obstacles_file)
    root.mainloop()


if __name__ == "__main__":
    start_game()
