"""CS 108 - Final Project
Welcome to The clicker challenge !!
Please extract before running. Have fun and enjoy :)
@author: Nhyira Mante (nnm7)
@date: Fall, 2024
"""

import random
import tkinter as tk
import pygame
from tkinter import simpledialog

leaderboard_data = {}


def main():
    """
    Initialize and manage the main game window and start menu.

    This function sets up the game window, creates the canvas for graphical elements, 
    and adds a start menu with options to either start the game or access the leaderboard.
    It also includes functionality to handle the game window's close event.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Initialize the root window with title and dimensions
    root = tk.Tk()
    root.title("The Clicker Challenge")
    root.geometry("1920x1080")  # Window size to fit game canvas

    # Create a canvas to display all graphical elements
    canvas = tk.Canvas(root, width=1920, height=1080)
    canvas.pack(fill="both", expand=True)  # Ensures it fills the window
    # Define the close event handler
    def on_close():
        """
        Handles the close event of the game window.

        Stops background music and closes the Tkinter root window.
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()  # Ensures music stops on exit
        except pygame.error:   
            pass
        root.destroy()  # Closes the window

    # Bind the close event handler to the window's close button
    root.protocol("WM_DELETE_WINDOW", on_close)
    
    level_buttons = [False]
    # Start the Tkinter main loop to display the window
    prestart_screen(None, canvas, root)
    
    

def prestart_screen(open_already, canvas, root, level_buttons = None):
    """
    After main menu has created the canvas this handles the creation of the start button on the screen
    that way we can get to the start button screen from the level select screen.
    
    Parameters
    ----------
    open_already:
        flag to determine if we are coming from the level select screen
        or we are starting a fresh game.
    
    level_buttons:
        Initialized to none for the first initialization of the prestart
        screen since at that time there are no level buttons.
    canvas : tk.Canvas
        The canvas on which graphical elements are drawn.

    Returns
    -------
    None
    """
    # Clear all existing elements on the canvas
    
    canvas.delete("all")
    
    if (open_already and open_already[0]) and level_buttons:
        for button in level_buttons:
            button.place_forget() # Ensure all buttons are hidden
    # Load the pre-game background image
    pre_game_bg_image = tk.PhotoImage(file="Pre-game bg.png")

    # Add the background image to the canvas
    canvas.create_image(0, 0, anchor="nw", image=pre_game_bg_image)
    
    change_user(root)        
    home_buttons = []
    root.change_user_button = tk.Button(
        root,
        text= 'Change user',
        font=("Times New Roman", 20),  # Font style and size
        fg="white",  # Text color
        bg="black",  # Button background color
        command=lambda: change_user(root, [True])
        )
    
    root.change_user_button.place(x=990, y =800)
    home_buttons.append(root.change_user_button)
    
    # Create a "Start!" button for starting the game
    start_button = tk.Button(
        root,
        text='Start!',  # Button label
        
        font=("Times New Roman", 24),  # Font style and size
        fg="white",  # Text color
        bg="black",  # Button background color
        command=lambda: open_app(canvas, root, home_buttons) #pass here
    )
    start_button.place(x=625, y=800)  # Positioning on the screen
    home_buttons.append(start_button)
    
    #Create a leaderboard button to display the leaderboard
    root.ldrbrd_button = tk.Button(
        root,
        text='Show Leaderboard',
         font=("Times New Roman", 24),  # Font style and size
        fg="white",  # Text color
        bg="black",  # Button background color
        command=lambda: ldrbrd_button_pressed_handler(root, root.ldrbrd_button, canvas) #pass here
       )
    root.ldrbrd_button.place(x=725, y=800)
    home_buttons.append(root.ldrbrd_button)
        
    
    root.mainloop()
    """
ask user for name:
create dictionary with name and initialize all the values of the keys to 0:

clicking the leaderboard button:
    display the dictionary in a table 
Dictionary: Nhyira Mante Dictionary dict(easy= 0, medium = 0, hard = 0, X = 0)
    goes in the game over screen:
    if score > Nhyira Mante Dictionary dict(level [score]) :
        update score with this score

    Nhyira Mante Dictionary( easy = level)

"""
    """

    Implementation
    1. Ask user for name.
    2. Create dictionary of scores for user's name.
    3. display leaderboard
    
    Update score for level in endgame function at the end of game.
    user_inputed_name = dict(easy = 0, medium = 0, hard = 0, X = 0)
    
    """
    
def change_user(root, button_pressed = [False]):
    #if the root doesn't have an attribute called player_name:
    if not hasattr(root, "player_name") or button_pressed[0]:
        #get a player name from the user in dialogue box
        name = simpledialog.askstring("Enter name", "Enter username here")
        
        #prevent the rootwindow from going out of focus when the simpledialog window is closed
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)

        #if user doesn't enter name default to guest
        if not name:
            name = "Guest"
        
        #attach the users name to the window so in the future the window knows it has already asked for the usersname
        root.player_name = name
        
        #add username to database
        if name not in leaderboard_data:
            leaderboard_data[name] = {"easy": 0, "medium": 0, "hard": 0, "X" : 0}
    
def ldrbrd_button_pressed_handler(root, ldrbrd_button, canvas):
    #if the button has just been pressed and the leaderboard is about to show
    if root.ldrbrd_button["text"] == "Show Leaderboard":
        root.ldrbrd_button.config(text="Hide Leaderboard")
        show_leaderboard(canvas, root)
        
    #if the button has been pressed already and the leaderboard is showing
    else:
        delete_leaderboard(canvas, root)
        root.ldrbrd_button.config(text="Show Leaderboard")
    pass
def show_leaderboard(canvas, root):
    if hasattr(root, "leaderboard_frame"):
        root.leaderboard_frame.destroy()

    root.leaderboard_frame = tk.Frame(root, bg="black")  # create a frame for the leaderboard with black background
    root.leaderboard_frame.place(x=425, y=150)           
    
    #header formatting for the leaderboard table
    headers = ["Player", "Easy", "Medium", "Hard", "X"]
    
    #col is the iterator and h is the header text
    for col, h in enumerate(headers):                    
        outer = tk.Frame(root.leaderboard_frame, bg="white", padx=1, pady=1)  # White border frame
        outer.grid(row=0, column=col)  # Place the outer frame in the grid

        label = tk.Label(outer,
                         text=h,
                         font=("Arial", 14, "bold"),
                         fg="white",
                         bg="black",
                         width=15,
                         anchor="center")
        label.pack()
    for row, (name, scores) in enumerate(leaderboard_data.items(), start=1):
        data = [name, scores["easy"], scores["medium"], scores["hard"], scores["X"]]

        for col, value in enumerate(data):
            outer = tk.Frame(root.leaderboard_frame, bg="white", padx=1, pady=1)
            outer.grid(row=row, column=col)

            label = tk.Label(outer,
                             text=value,
                             font=("Arial", 12),
                             fg="white",
                             bg="black",
                             width=15,
                             anchor="center")
            label.pack()
        pass
def delete_leaderboard(canvas, root):
    if hasattr(root, "leaderboard_frame"):
        root.leaderboard_frame.destroy()
        del root.leaderboard_frame  # Optional but cleans up
        
    #we pass true for already open even though we aren't handling level buttons
    #prestart_screen([True], canvas, root)
    
    
def open_app(canvas, root, home_buttons, end_button=None): #pass here
    """
    Transition the application to the loading screen.

    This function transitions from the main menu to the loading screen by hiding 
    the start button, playing a random background track, and displaying a progress bar.
    If an end button from a previous game exists, it is removed to reset the UI.

    Parameters
    ----------
    canvas : tk.Canvas
        The canvas on which graphical elements are drawn.
    start_button : tk.Button
        The "Start!" button from the main menu to be hidden.
    root : tk.Tk
        The root Tkinter window to manage event-driven updates.
    end_button : tk.Button, optional
        The "End Game" button from a previous game session, if present, to be hidden.

    Returns
    -------
    None
    """
    
    if hasattr(root, "leaderboard_frame"):
        root.leaderboard_frame.destroy()
        del root.leaderboard_frame
    root.ldrbrd_button.config(text="Show Leaderboard")
    
    # List of music tracks and randomly selecting one to play
    musics = ["loading_music.mp3", "music 2.mp3", "music 1.mp3"]
    play_music(musics[random.randint(0, 2)])  # Start playing the selected track

    # Remove the end button if it exists to clear UI for a new session
    if end_button is not None:
        end_button.place_forget()

    # Hide the start button from the main menu
    for button in home_buttons:
        button.place_forget()

    # Add a progress bar background rectangle to the canvas
    canvas.create_rectangle(
        (1920 - 400) // 2,
        1080 - 200,
        (1920 + 400) // 2,
        1080 - 150,
        fill="gray"
    )

    # Add a loading bar rectangle to the canvas
    loading_max_width = 400  # Maximum width of the loading bar
    loading_width = 0  # Initial width of the loading bar
    loading_rect = canvas.create_rectangle(
        (1920 - 400) // 2,
        1080 - 200,
        (1920 - 400) // 2,
        1080 - 150,
        fill="black"
    )

    # Add "Loading..." text to the canvas
    canvas.create_text(
        1920 // 2,
        850,
        text="Loading...",
        fill="white",
        font=("Arial", 18)
    )

    # Start updating the progress bar to simulate loading
    update_progress(canvas, root, loading_width, loading_max_width, loading_rect)

    # Placeholder for transitioning to the level selection screen
    level_slct_bg = tk.PhotoImage(file="lvl slct.png")


def update_progress(canvas, root, loading_width, loading_max_width, loading_rect):
    """
    Update the progress bar on the loading screen.

    The function increments the width of the progress bar and updates its position.
    A random step size is used for each increment to create variability in loading progression.
    Once the progress bar reaches its maximum width, the level selection screen is displayed.

    Parameters
    ----------
    canvas : tk.Canvas
        The canvas where the progress bar is displayed.
    root : tk.Tk
        The root Tkinter window.
    loading_width : int
        The current width of the progress bar.
    loading_max_width : int
        The maximum width the progress bar can reach.
    loading_rect : int
        The rectangle object representing the progress bar.

    Returns
    -------
    None
    """
    if loading_width < loading_max_width:
        # Increment the progress bar width randomly
        if random.randint(1, 4) == 2 and loading_width + 70 <= loading_max_width:
            loading_width += 70
        else:
            loading_width += 20

        # Update the coordinates of the progress bar
        canvas.coords(
            loading_rect,
            (1920 - 400) // 2,
            1080 - 200,
            (1920 - 400) // 2 + loading_width,
            1080 - 150
        )

        # Schedule the next update after 100 milliseconds
        root.after(100, update_progress, canvas, root, loading_width, loading_max_width, loading_rect)
    else:
        # Progress bar is full; transition to level selection screen
        choose_level(canvas, root) #1



def choose_level(canvas, root, endgame_buttons=None): #2
    """
    Display the level selection screen.

    This function sets up the level selection screen by clearing the canvas, 
    adding a background image, and placing buttons for level selection.

    Parameters
    ----------
    canvas : tk.Canvas
        The canvas where the level selection screen elements are displayed.
    root : tk.Tk
        The root Tkinter window.
    home_button : tk.Button, optional
        The "Home" button, if present, is removed before displaying the level selection screen.

    Returns
    -------
    None
    """
    if hasattr(root, "leaderboard_frame"):
        root.leaderboard_frame.destroy()
        del root.leaderboard_frame
    root.ldrbrd_button.config(text="Show Leaderboard")
    
    
    # Clear all existing elements on the canvas
    canvas.delete("all")
    
    # Remove the home button if it exists
    if endgame_buttons:
        for button in endgame_buttons:
            button.place_forget()
    
    # Load and set the background image for the level selection screen
    canvas.level_slct_bg = tk.PhotoImage(file="lvl slct.png")
    canvas.create_image(0, 0, anchor="nw", image=canvas.level_slct_bg)

    # Add the title for level selection
    canvas.create_text(
        200, 150,
        text="Choose Your Level",
        font=("Arial", 24, "bold"),
        fill="white"
    )
    canvas.create_text(
        850, 950,
        text="Mante Games © 2024",
        font=("Arial", 12, "bold"),
        fill="white"
    )
    # List to hold all level buttons for easier management
    level_buttons = []

    # Level 1: Easy
    level1_button = tk.Button(
        root,
        text="Level 1: Easy",
        font=("Times New Roman", 18),
        fg="white",
        bg="green",
        command=lambda: start_game(1, canvas, root, level_buttons)
    )
    level1_button.place(x=260, y=300)
    level_buttons.append(level1_button)

    # Level 2: Medium
    level2_button = tk.Button(
        root,
        text="Level 2: Medium",
        font=("Times New Roman", 18),
        fg="white",
        bg="blue",
        command=lambda: start_game(2, canvas, root, level_buttons)
    )
    level2_button.place(x=260, y=350)
    level_buttons.append(level2_button)

    # Level 3: Hard
    level3_button = tk.Button(
        root,
        text="Level 3: Hard",
        font=("Times New Roman", 18),
        fg="white",
        bg="red",
        command=lambda: start_game(3, canvas, root, level_buttons)
    )
    level3_button.place(x=260, y=400)
    level_buttons.append(level3_button)

    # Level X: Impossible
    impossible_button = tk.Button(
        root,
        text="Level X",
        font=("Times New Roman", 18),
        fg="white",
        bg="black",
        command=lambda: start_game("X", canvas, root, level_buttons)
    )
    impossible_button.place(x=260, y=450)
    level_buttons.append(impossible_button)
    
    open_already = [True]
    main_menu_button = tk.Button(
        root,
        text = "Main Menu",
        font =("Times New Roman", 18),
        fg = "white",
        bg = "black",
        command = lambda: prestart_screen(open_already,canvas, root, level_buttons)
        )
    main_menu_button.place(x=780, y=875)
    level_buttons.append(main_menu_button)
    
    musics = ["loading_music.mp3", "music 2.mp3", "music 1.mp3"]
    
    #Create skip song button
    skip_button = tk.Button(
        root,
        text = "Next Song",
        font=("Times New Roman", 14),  # Font style and size
        fg="white",  # Text color
        bg="black",  # Button background color
        command = lambda: change_music(musics[random.randint(0, 2)])
        )
    skip_button.place(x=1500, y = 875)
    level_buttons.append(skip_button)
    
     

def start_game(level, canvas, root, level_buttons):
    """
    Initialize and start the game with targets, timer, and score display.

    This function hides level selection buttons, sets up the game screen with the necessary UI components, and initiates game mechanics like moving targets and the countdown timer.

    Parameters
    ----------
    level : int or str
        The selected difficulty level or mode of the game.
    canvas : tk.Canvas
        The canvas object where the game elements are drawn.
    root : tk.Tk
        The root window object.
    level_buttons : list of tk.Button
        Buttons for level selection, which are hidden when the game starts.

    Returns
    -------
    None
    """
    for button in level_buttons:
        button.place_forget() # Ensure all buttons are hidden
        
    # Game settings
    game_duration = [30] # Duration of the game in seconds
    time_left = game_duration
    score = [0] # Initial score, stored in a list for mutability
    stop_moving = [False]  # Flag to stop target movement
    stop_countdown= [False]# Start the countdown
    end_game_callback = lambda: end_game(canvas, score, stop_moving, end_button, root, level)
    
    def end_game_manual():
        stop_countdown[0] = True
        
    # End game callback for when the timer ends or the game is manually terminated
    end_button = tk.Button(
        root,
        text="End Game",
        font=("Arial", 20),
        fg="black",
        bg="white",
        command= end_game_manual,
        )
    end_button.place(x=900, y=900)
    # Clear the canvas and set the game background
    canvas.delete("all")
    canvas.in_game_bg_image = tk.PhotoImage(file="level bg.png")
    canvas.create_image(0, 0, anchor="nw", image=canvas.in_game_bg_image)

    # Display timer and score
    timer_text = canvas.create_text(1600, 50, text=f"Timeleft: {time_left}(s)", font=("Arial", 12), fill="white")
    score_text = canvas.create_text(1600, 80, text=f"Score: {score}", font=("Arial", 12), fill="white")

    # Set up targets
    targets = []
    canvas.target_image = tk.PhotoImage(file="target.png")
    box_x1=150
    box_x2=1600
    box_y1=250
    box_y2=900
    button_no = level
    
    if level =="X":
        button_no = 2  # "Impossible" level has fixed two targets
        play_music("Impossible Level Track.mp3")
        
        
    for i in range(button_no):
        target = tk.Button(
                root,
                width=49,
                height=75,
                command=lambda i=i: target_clicked(i, canvas, targets, score_text, box_x1, box_x2, box_y1, box_y2, score),
                image=canvas.target_image,
                borderwidth=0,
                highlightthickness=0,
                )
        targets.append(target)

    canvas.create_rectangle(box_x1, box_y1, box_x2, box_y2, outline="white", width=2)

    # Start moving the targets
    move_target(level, targets, root, box_x1, box_x2, box_y1, box_y2, 1400, stop_moving)

    # Start the countdown
    stop_countdown= [False]
    count_down(canvas, game_duration, timer_text, end_game_callback, level, root, stop_countdown)

    
    
def move_target(level, targets, root, box_x1, box_x2, box_y1, box_y2, move_time, stop_moving):
    """
    Move targets within a specified area at periodic intervals.

    The targets are moved to random positions within the defined box dimensions. 
    Movement stops if the `stop_moving` flag is set to True. The speed of movement 
    is adjusted based on the game level.

    Parameters
    ----------
    level : int or str
        The current game level. Level "X" corresponds to the "Impossible" level.
    targets : list of tk.Button
        A list of target buttons to be moved.
    root : tk.Tk
        The root Tkinter window.
    box_x1 : int
        The x-coordinate of the left boundary .
    box_x2 : int
        The x-coordinate of the right boundary .
    box_y1 : int
        The y-coordinate of the top boundary .
    box_y2 : int
        The y-coordinate of the bottom boundary .
    move_time : int
        The time interval (in milliseconds) between successive movements.
    stop_moving : list of bool
        A flag indicating whether to stop the movement. The list is used for mutability.

    Returns
    -------
    None
    """
    # Adjust movement speed based on the game level
    if level == "X":
        move_time = 150
    elif level == 3:
        move_time = 700
    elif level == 2:
        move_time = 1000

    # Check if movement should stop
    if stop_moving[0]:
        # Stop moving and remove all targets
        for target in targets:
            target.place_forget()
            target.destroy()
        targets.clear()
        return  # Exit function to prevent further execution

    # Move each target to a new random position within the defined area
    for target in targets:
        new_x = random.randint(box_x1, box_x2 - 100)
        new_y = random.randint(box_y1, box_y2 - 100)
        target.place(x=new_x, y=new_y)

    # Schedule the next movement
    root.after(move_time, move_target, level, targets, root, box_x1, box_x2, box_y1, box_y2, move_time, stop_moving)

def target_clicked(target_index, canvas, targets, score_text, box_x1, box_x2, box_y1, box_y2, score):
    """
o    Handle the event when a target is clicked.
    
    Parameters:
    -----------
    target_index : int
        The index of the clicked target in the `targets` list.
    canvas : tk.Canvas
        The canvas on which the game elements are displayed.
    targets : list
        List of all target buttons.
    score_text : int
        The text object showing the current score.
    box_x1, box_x2, box_y1, box_y2 : int
        Dimensions of the box where targets can move.

    Returns:
    --------
    None
    """
    
    score[0] += 1  # Update the score in the list 

    # Update the score display
    canvas.itemconfig(score_text, text=f"Score: {score[0]}")
    
    
    # Play the click sound
    click_sound = pygame.mixer.Sound("click_sound.mp3")
    click_sound.set_volume(1)
    click_sound.play()
    # Relocate the clicked target to a new random position
    clicked_target = targets[target_index]
    new_x = random.randint(box_x1, box_x2 - 50)
    new_y = random.randint(box_y1, box_y2 - 50)
    clicked_target.place(x=new_x, y=new_y)
    
def count_down(canvas, time_left, timer_text, end_game_callback, level, root, stop_countdown):
    """
    Countdown timer function for the game.

    Parameters
    ----------
    canvas : tk.Canvas
        The canvas where the timer is displayed.
    time_left : int
        The remaining time in seconds.
    timer_text : tk.Text
        The text element displaying the timer on the canvas.
    targets : list
        List of targets on the screen.
    end_game_callback : function
        The function to call when the timer reaches zero.

    Returns
    -------
    None
    """
    
    #Level Box Dimensions
    
    box_x1= 150
    box_x2= 1600
    box_y1= 250
    box_y2= 900
    move_time=0
    
     # Check if the countdown has been stopped
    if stop_countdown[0]:  # If stop flag is set, exit immediately
        canvas.itemconfig(timer_text, text="Time left: 0s")  # Ensure timer is updated
        end_game_callback()  # Trigger end game
        return

    if time_left[0] > 0:
        # Update the timer display
        canvas.itemconfig(timer_text, text=f"Time left: {time_left[0]}s")
        time_left[0] -= 1  # Decrement the time
        root.after(1000, count_down, canvas, time_left, timer_text, end_game_callback, level, root, stop_countdown)
    else:
        # Trigger end game when time reaches zero
        canvas.itemconfig(timer_text, text="Time left: 0s")
        end_game_callback()

def end_game(canvas, score, stop_moving, end_button, root, level):
    """
    Handle the end-of-game logic and display the game over screen.

    This function stops target movement, clears the game canvas, displays the game over screen with the player's
    final score, and provides a "Home" button to return to the level selection screen.
    Background music is also restarted with a random track.

    Parameters
    ----------
    canvas : tk.Canvas
        The canvas where game elements are displayed and updated.
    score : list[int]
        A list containing the player's current score. The first element holds the score.
    stop_moving : list[bool]
        A mutable flag to control target movement. Setting it to True halts movement.
    end_button : tk.Button
        The button used to manually end the game. It is removed from the screen.
    root : tk.Tk
        The root Tkinter window object.
    level : int or str
        The current game level, which can be used for logic if needed.

    Returns
    -------
    None
    """
    # Stop target movement by setting the flag
    stop_moving[0] = True

    # Clear the canvas and remove the end game button
    canvas.delete("all")
    end_button.place_forget()

    # Set up the game over background and display the game over message
    canvas.level_slct_bg = tk.PhotoImage(file="lvl slct.png")
    canvas.create_image(0, 0, anchor="nw", image=canvas.level_slct_bg)

    # Display the game over text and final score
    canvas.create_text(760, 540, text="GAME OVER", font=("Arial", 36, "bold"), fill="white")
    canvas.create_text(760, 600, text=f"Your Score: {score[0]}", font=("Arial", 24), fill="white")
    
    #create a button list to handle the endgame button passing when moving to level select screen
    endgame_buttons = []
    
    
    # Create a "Home" button to return to the level selection screen
    home_button = tk.Button(
        root,
        text="Home",
        font=("Arial", 20),
        fg="white",
        bg="black",
        state="normal",
        command=lambda: choose_level(canvas, root, endgame_buttons) #3
    )
    home_button.place(x=725, y=900)
    root.ldrbrd_button.place(x=825, y=900)
    endgame_buttons.append(home_button)
    endgame_buttons.append(root.ldrbrd_button)
    
    player = root.player_name
    if level == 1:
        level_key = "easy"
    elif level == 2:
        level_key = "medium"
    elif level == 3:
        level_key = "hard"
        
    else:
        level_key = "X"
    # Update leaderboard if new score is higher
    if score[0] > leaderboard_data[player][level_key]:
        leaderboard_data[player][level_key] = score[0]


    
    
    # Play a random background music track
    #musics = ["loading_music.mp3", "music 2.mp3", "music 1.mp3"]
    #track = random.randint(0, 2)
    #play_music(musics[track])
    
def play_music(filename):
    """
    Play background music using the pygame mixer.

    Parameters
    ----------
    filename : str
        The name of the music

    Returns
    -------
    None
    """
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    if filename == "loading music.mp3":
        pygame.mixer.music.set_volume(0.3)  # Set background music volume to 30%
    else:
        pygame.mixer.music.set_volume(0.8)  # Set background music volume to 80%
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
    
def change_music(filename):
    """
    Change background music using the pygame mixer.

    Parameters
    ----------
    filename : str
        The name of the music

    Returns
    -------
    None
    """
    pygame.mixer.music.stop()  # Stop the current music
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(1)  # Set background music volume to 100%
    pygame.mixer.music.play(-1)  # Play the new music on an infinite loop



main()


