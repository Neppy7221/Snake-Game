import tkinter as tk
import random

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SPEED = 10
COUNTDOWN_TIME = 3  # Countdown time (seconds)

class SnakeGame:
    #the initiation of the game
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.start_menu()

    #the start menu where the game goes after a game over and when the game starts up
    def start_menu(self):
        self.canvas.delete("all")
        self.canvas.create_text(WIDTH/2, HEIGHT/2 - 50, text="Snake Game", fill="white", font=("Helvetica", 36))
        self.canvas.create_text(WIDTH/2, HEIGHT/2, text="Press 'N' for New Game", fill="white", font=("Helvetica", 24))
        self.canvas.create_text(WIDTH/2, HEIGHT/2 + 30, text="Press 'H' for High Scores", fill="white", font=("Helvetica", 24))
        self.canvas.create_text(WIDTH/2, HEIGHT/2 + 60, text="Press 'Q' to Quit", fill="white", font=("Helvetica", 24))
        self.master.bind("<KeyPress>", self.handle_start_menu)
        
    # The keybinds for the main menu
    def handle_start_menu(self, event):
        if event.keysym == "n" or event.keysym == "N":
            self.new_game()
        elif event.keysym == "h" or event.keysym == "H":
            self.show_high_scores()
        elif event.keysym == "q" or event.keysym == "Q":
            self.master.destroy()

    def new_game(self):
        # Initializing the game variables
        self.snake = [(WIDTH/2, HEIGHT/2)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0
        self.game_over = False
        self.countdown = COUNTDOWN_TIME

        # Drawing the game
        self.draw()
        self.master.bind("<KeyPress>", self.change_direction)
        self.update()

        #adds keybind to send back to main menu
        self.master.bind("<KeyPress-m>", lambda event: self.return_to_menu())

    def return_to_menu(self):
        self.snake = [(WIDTH/2, HEIGHT/2)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0
        self.game_over = False
        self.countdown = COUNTDOWN_TIME

        self.start_menu()


    def draw(self):
        self.canvas.delete("all")

        # Draw instructions for the player to know the controls
        self.canvas.create_text(WIDTH/2, 10, text="Controls: Arrow keys to move, 'M' to return to menu", fill="white", anchor="n")

        # Debug statements to check food and snake positions (uncomment the two lines below if you need some sort of debugging.)
        #print("Snake:", self.snake)
        #print("Food:", self.food)

        # Drawing the snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+GRID_SIZE, y+GRID_SIZE, fill="green")

        # Drawing the food
        x, y = self.food
        self.canvas.create_oval(x, y, x+GRID_SIZE, y+GRID_SIZE, fill="red")

        # Drawing the score
        self.canvas.create_text(10, 10, text=f"Score: {self.score}", fill="white", anchor="nw")

        #if game over happens this game over screen pops up.
        if self.game_over:
            self.canvas.create_text(WIDTH/2, HEIGHT/2, text="Game Over", fill="white", font=("Helvetica", 36))
            self.canvas.create_text(WIDTH/2, HEIGHT/2 + 30, text=f"Returning to Main Menu in {self.countdown}...", fill="white", font=("Helvetica", 24))

            # Countdown for the game over screen before being sent back to the main menu
            if self.countdown > 0:
                self.countdown -= 1
                self.master.after(1000, self.draw)
            else:
                self.start_menu()

    def update(self):
        # Updates the canvas after moving the snake
        if not self.game_over:
            self.move_snake()
            self.draw()  
            self.master.after(1000 // SPEED, self.update)

    def create_food(self):
        while True:
            x = random.randint(0, WIDTH - GRID_SIZE)
            y = random.randint(0, HEIGHT - GRID_SIZE)
            if (x, y) not in self.snake:
                #self.log_food_position(x, y)  # Logs the food's position
                return x, y

    # Logging to help me figure out if the food is actually where its shown at.
    #def log_food_position(self, x, y):
    #    with open("food_log.txt", "a") as file:
    #        file.write(f"Food position: ({x}, {y})\n")

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + GRID_SIZE, head_y)

        # Found out that the food and the snake are never intersecting within the grid plane but they are visually. 
        # so i made it to where the snake can eat the food even if its not in the exact coords on the grid plane.
        # Check if the new head position is within the buffer zone of the food
        food_x, food_y = self.food
        if abs(new_head[0] - food_x) <= 10 and abs(new_head[1] - food_y) <= 10:
            print("Food eaten!")
            self.food = self.create_food()  # Generate new food
            self.score += 1  # Increase score
        else:
        # Remove the last segment of the snake if it didn't eat food
            self.snake.pop()

        # Insert the new head position at the beginning of the snake
        self.snake.insert(0, new_head)

        if self.check_collision():
            self.game_over = True

    # Check if the snake collides with the walls or with itself, if it does then its game over.
    def check_collision(self):
        head_x, head_y = self.snake[0]

        # Check if snake hits walls
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True

        # Check if snake hits itself
        if (head_x, head_y) in self.snake[1:]:
            return True

        return False

    # The keybinds that help you move the snake
    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            if (event.keysym == "Up" and self.direction != "Down" or
                event.keysym == "Down" and self.direction != "Up" or
                event.keysym == "Left" and self.direction != "Right" or
                event.keysym == "Right" and self.direction != "Left"):
                self.direction = event.keysym

    # The High score menu
    def show_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                high_scores = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            high_scores = []


        high_scores.append(f"{self.score}")

        # Creates a new window for high scores
        high_scores_window = tk.Toplevel(self.master)
        high_scores_window.title("High Scores")

        # Creates a label to display the high scores
        label = tk.Label(high_scores_window, text="High Scores", font=("Helvetica", 24))
        label.pack()

        # Display each high score as a label
        for i, score in enumerate(high_scores, start=1):
            score_label = tk.Label(high_scores_window, text=f"{i}. {score}", font=("Helvetica", 18))
            score_label.pack()

        # Add a text entry for the player's name
        name_label = tk.Label(high_scores_window, text="Enter Your Name:", font=("Helvetica", 18))
        name_label.pack()
        name_entry = tk.Entry(high_scores_window, font=("Helvetica", 14))
        name_entry.pack()

        # Adds a save button to save the high scorer's name
        save_button = tk.Button(high_scores_window, text="Save", command=lambda: self.save_high_score(name_entry.get(), self.score))
        save_button.pack()

        # Binds the Enter key to close the high scores window
        high_scores_window.bind("<Return>", lambda event: high_scores_window.destroy())

# Method to save the high score with the player's name, also creates a text file that contains the saved highscores.
    def save_high_score(self, name, score):
        with open("high_scores.txt", "a") as file:
            file.write(f"{name}: {score}\n")


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
