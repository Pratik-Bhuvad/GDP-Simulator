from tkinter import *
from PIL import Image, ImageTk
from games import dots_boxes, ping_pong, snake_game, tictactoe, car, flappy_bird

# Define game data (image path, play function)
games_data = [
    {"name": "Dots & Boxes", "image_path": "dots_boxes_bt_bg.png", "play_function": dots_boxes.play_game},
    {"name": "Ping Pong", "image_path": "ping_pong_bt_bg.png", "play_function": ping_pong.play_game},
    {"name": "Snake Game", "image_path": "snake_bt_bg.png", "play_function": snake_game.play_game},
    {"name": "Tic Tac Toe", "image_path": "tictactoe_bt_bg.png", "play_function": tictactoe.play_game},
    {"name": "Flappy Bird", "image_path": "Flappy_Bird.png", "play_function": flappy_bird.play_game},
    {"name": "Car Rush", "image_path": "car_rush.png", "play_function": car.play_game}
]

def play_game(game_choice):
    if 1 <= game_choice <= len(games_data):
        games_data[game_choice - 1]["play_function"]()
    else:
        print("Invalid choice. Please enter a number between 1 and {}.".format(len(games_data)))

def create_game_button(parent, game, button_height=350, button_width=270, image_size=(270, 370)):
    image_path = "game_img/" + game["image_path"]
    image = Image.open(image_path).resize(image_size)
    photo = ImageTk.PhotoImage(image)
    button = Button(parent, image=photo, compound='top', command=lambda func=game["play_function"]: func())
    button.image = photo  # Keep a reference to the image to prevent garbage collection
    button.config(height=button_height, width=button_width)  # Set button dimensions
    return button

def update_game_buttons(filtered_games):
    for widget in button_frame.winfo_children():
        widget.destroy()  # Clear existing buttons
    i=0
    for game in filtered_games:
        game_button = create_game_button(button_frame, game, button_height=350, button_width=270, image_size=(270, 370))
        game_button.grid(row=(i // 3),column=(i % 3),padx=30,pady=20)
        i+=1

def filter_games(query):
    if not query.strip():  # If query is empty, show all games
        return games_data
    else:
        return [game for game in games_data if query.lower() in game["name"].lower()]

def on_search_entry(event):
    query = search_entry.get()
    filtered_games = filter_games(query)
    update_game_buttons(filtered_games)

def on_search_focus_in(event):
    if search_entry.get() == "Search Games...":
        search_entry.delete(0, END)
        search_entry.configure(fg='black')  # Change text color to black when focused

def on_search_focus_out(event):
    if not search_entry.get().strip():
        search_entry.insert(0, "Search Games...")
        search_entry.configure(fg='grey')  # Change text color to grey when not focused

def logo(image_path, new_width, new_height):
    original_image = Image.open(image_path)
    resized_image = original_image.resize((new_width, new_height))
    return ImageTk.PhotoImage(resized_image)

#Tkinter window of GUI
root = Tk()
root.title("GDP Simulator")
root.resizable(False,False)
root.configure(bg='#02103d')
root.geometry(f"1200x900")
  # Maximize the window

# Path to the logo image
logo_path = r"game_img\gdp_logo.png"
logo_width = 74
logo_height = 74
logo_image = logo(logo_path, logo_width, logo_height)
logo_label = Label(root, image=logo_image)
logo_label.place(x=4,y=4)
logo_label.image = logo_image

# Create search bar
search_entry = Entry(root, width=55, font=('Arial', 20), justify='center', fg='grey')
search_entry.insert(0, "Search Games...")
search_entry.pack(side=TOP, pady=20)

# Bind events to handle focus in and out
search_entry.bind("<FocusIn>", on_search_focus_in)
search_entry.bind("<FocusOut>", on_search_focus_out)
search_entry.bind("<KeyRelease>", on_search_entry)

# Create canvas for game buttons and scrollbar
canvas = Canvas(root, bg='#02103d', highlightthickness=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True, padx=80)

# Frame inside the canvas to hold buttons
button_frame = Frame(canvas, bg='#02103d')
button_frame.pack(side=TOP)

# Display all games initially
update_game_buttons(games_data)

# Add scrollbar to canvas
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Configure canvas scrolling and mouse wheel binding
canvas.create_window((170, 0), window=button_frame, anchor='nw')
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
button_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

root.mainloop()  # Run the GUI main loop