#New Snake Game
import tkinter as tk, random

def play_game():
    global direction, score
    screen_width = 1200
    screen_height = 600
    white = "#FFFFFF"
    bgcolor = "#000015"
    food_color = "#FF0000"
    snake_color = "#00FF00"
    speed = 100
    space_size = 25
    body_parts = 3
    screen_font = ('Helvetica',25)

    class snake:
        def __init__(self):
            self.body_size = body_parts
            self.coordinates = []
            self.squares = []
            for i in range(0,body_parts):
                self.coordinates.append([25,25])

            for x,y in self.coordinates:
                square = canvas.create_rectangle(x, y, x+space_size, y + space_size, fill=snake_color, tag="Snake")
                self.squares.append(square)

    class Food:
        def __init__(self):
            x = random.randint(2, int((screen_width/space_size)-2)) * space_size
            y = random.randint(2, int((screen_height/space_size)-2)) * space_size
            self.coordinates = [x, y]
            canvas.create_oval(x, y, x+space_size, y+space_size,fill=food_color,tag="Food")

    def next_turn(snake, food):
        x , y = snake.coordinates[0]
        if direction == "up":
            y -= space_size
        elif direction == "down":
            y += space_size
        elif direction == "left":
            x -= space_size
        elif direction == "right":
            x += space_size

        snake.coordinates.insert(0,(x,y))
        square = canvas.create_rectangle(x, y, x+space_size, y + space_size, fill=snake_color, tag="Snake")
        snake.squares.insert(0,square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            global score
            score += 1
            label.config(text="Score: {}".format(score))

            canvas.delete("Food")
            food = Food()

        else:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]

        if check_collisions(snake):
            game_over()
        else:
            root.after(speed,next_turn, snake, food)


    def chg_direction(event):
        global direction
        # print("Key pressed:", event.keysym)  # Print the pressed key for debugging
        key = event.keysym
        if (key == 'Left' or key == 'a') and direction != "right":
            direction = "left"
        elif (key == 'Right' or key == 'd') and direction != "left":
            direction = "right"
        elif (key == 'Up' or key == 'w') and direction != "down":
            direction = "up"
        elif (key == 'Down' or key == 's') and direction != "up":
            direction = "down"

    def check_collisions(snake):
        x, y = snake.coordinates[0]
        if (x < 0 or x >= screen_width) or (y<0 or y >= screen_height):
            return True
        
        for body_part in snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True
            
        return False

    def game_over():
        canvas.delete("all")
        canvas.create_text(canvas.winfo_width()/2,canvas.winfo_height()/2,font=("Helvetica",60),text="Game Over",fill=white,tag="gameover")
        restart_button = tk.Button(canvas,text="Restart",font=("Helvetica",20),command=restart)
        canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100,window=restart_button)

    def restart():
        global score, direction
        score = 0
        direction = "right"
        label.config(text="Score: {}".format(score))
        canvas.delete("all")

        Snake = snake()
        food = Food()
        next_turn(Snake, food)

    root = tk.Tk()
    root.title("Snake Game")
    root.resizable(width=False,height=False)

    score = 0
    direction = "right"

    if score > 20 and score < 50:
        speed -= 5
    elif score > 50 and score < 100:
        speed -= 10
    else:
        speed -= 20

    label = tk.Label(root,text = "Score: {}".format(score),font = screen_font)
    label.pack()


    canvas = tk.Canvas(root,bg=bgcolor,height=screen_height,width=screen_width)
    canvas.pack()
    canvas.focus_set()

    start_button = tk.Button(root, text="Start", font=("Arial", 25), command=restart)
    start_button.pack(pady=20)
    canvas.create_window(600,300,window=start_button)

    root.update()
    game_width = root.winfo_width()
    game_height = root.winfo_height()
    window_width = root.winfo_screenwidth()
    window_height = root.winfo_screenheight()
    root.geometry(f"{game_width}x{game_height}+{(window_width - game_width) // 2}+{(window_height - game_height) // 2}")

    root.bind('<Key>', chg_direction)

    root.tk.mainloop()

if __name__ == "__main__":
    play_game()