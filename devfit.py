import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime, timedelta
import calendar

# Function to update the squat count
def update_squats():
    squats = int(squats_count.get().split(": ")[1])
    squats += 1
    squats_count.set(f"Squats: {squats}")
    if squats == 30:
        show_alert("Squats", squats)
    root.after(squat_interval, update_squats)  # Schedule the function to be called based on the interval

# Function to update the pushup count
def update_pushups():
    pushups = int(pushups_count.get().split(": ")[1])
    pushups += 1
    pushups_count.set(f"Pushups: {pushups}")
    if pushups == 30:
        show_alert("Pushups", pushups)
    root.after(pushup_interval, update_pushups)  # Schedule the function to be called based on the interval

# Function to update the pullup count
def update_pullups():
    pullups = int(pullups_count.get().split(": ")[1])
    pullups += 1
    pullups_count.set(f"Pullups: {pullups}")
    if pullups == 30:
        show_alert("Pullups", pullups)
    root.after(pullup_interval, update_pullups)  # Schedule the function to be called based on the interval

# Function to update the leg raise count
def update_leg_raises():
    leg_raises = int(leg_raises_count.get().split(": ")[1])
    leg_raises += 1
    leg_raises_count.set(f"Leg Raises: {leg_raises}")
    if leg_raises == 30:
        show_alert("Leg Raises", leg_raises)
    root.after(leg_raise_interval, update_leg_raises)  # Schedule the function to be called based on the interval

# Function to reset the squat count and store the total
def reset_squats():
    total_squats = int(squats_count.get().split(": ")[1])
    store_total("squats", total_squats)
    squats_count.set("Squats: 0")

# Function to reset the pushup count and store the total
def reset_pushups():
    total_pushups = int(pushups_count.get().split(": ")[1])
    store_total("pushups", total_pushups)
    pushups_count.set("Pushups: 0")

# Function to reset the pullup count and store the total
def reset_pullups():
    total_pullups = int(pullups_count.get().split(": ")[1])
    store_total("pullups", total_pullups)
    pullups_count.set("Pullups: 0")

# Function to reset the leg raise count and store the total
def reset_leg_raises():
    total_leg_raises = int(leg_raises_count.get().split(": ")[1])
    store_total("leg raises", total_leg_raises)
    leg_raises_count.set("Leg Raises: 0")

# Function to store the total counts in a JSON file
def store_total(exercise, count):
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    try:
        with open("exercise_totals.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    
    if date_str not in data:
        data[date_str] = {"squats": 0, "pushups": 0, "pullups": 0, "leg raises": 0}
    
    data[date_str][exercise] += count
    
    with open("exercise_totals.json", "w") as file:
        json.dump(data, file)

# Function to show alert when a counter reaches 30
def show_alert(counter_name, reps):
    alert_window = tk.Toplevel(root)
    alert_window.title("Alert")
    
    # Center the alert window on the screen
    center_window(alert_window, 300, 100)
    
    tk.Label(alert_window, text=f"{counter_name} reached {reps} reps!").pack(pady=20)
    
    tk.Button(alert_window, text="Hide", command=alert_window.destroy).pack()

# Function to highlight the appropriate button based on the saved setting
def highlight_button(level):
    if 'beginner_button' in globals() and beginner_button.winfo_exists():
        beginner_button.config(bg="SystemButtonFace")
    if 'intermediate_button' in globals() and intermediate_button.winfo_exists():
        intermediate_button.config(bg="SystemButtonFace")
    if 'advanced_button' in globals() and advanced_button.winfo_exists():
        advanced_button.config(bg="SystemButtonFace")
    
    if level == "Beginner" and 'beginner_button' in globals() and beginner_button.winfo_exists():
        beginner_button.config(bg="lightblue")
    elif level == "Intermediate" and 'intermediate_button' in globals() and intermediate_button.winfo_exists():
        intermediate_button.config(bg="lightgreen")
    elif level == "Advanced" and 'advanced_button' in globals() and advanced_button.winfo_exists():
        advanced_button.config(bg="lightcoral")

# Function to show settings window
def show_settings():
    global settings_window, beginner_button, intermediate_button, advanced_button
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.overrideredirect(True)  # Remove the title bar
    
    beginner_button = tk.Button(settings_window, text="Beginner", command=lambda: set_level("Beginner"))
    beginner_button.pack(pady=5)
    intermediate_button = tk.Button(settings_window, text="Intermediate", command=lambda: set_level("Intermediate"))
    intermediate_button.pack(pady=5)
    advanced_button = tk.Button(settings_window, text="Advanced", command=lambda: set_level("Advanced"))
    advanced_button.pack(pady=5)
    
    # Highlight the current setting
    current_level = load_level()
    highlight_button(current_level)
    
    # Center the settings window on the screen
    center_window(settings_window, 200, 130)

# Function to set the exercise level
def set_level(level, show_settings = True):
    global squat_interval, pushup_interval, pullup_interval, leg_raise_interval
    if level == "Beginner":
        squat_interval = 600000  # 10 minutes
        pushup_interval = 1200000  # 20 minutes
        pullup_interval = 1200000  # 20 minutes
        leg_raise_interval = 1200000  # 20 minutes
    elif level == "Intermediate":
        squat_interval = 360000  # 6 minutes
        pushup_interval = 720000  # 12 minutes
        pullup_interval = 720000  # 12 minutes
        leg_raise_interval = 720000  # 12 minutes
    elif level == "Advanced":
        squat_interval = 180000  # 3 minutes
        pushup_interval = 360000  # 6 minutes
        pullup_interval = 360000  # 6 minutes
        leg_raise_interval = 360000  # 6 minutes
    
    if show_settings :
        save_level(level)
        highlight_button(level)  # Highlight the selected button
        messagebox.showinfo("Level Set", f"Exercise level set to {level}")
        if 'settings_window' in globals() and settings_window.winfo_exists():
            settings_window.destroy()  # Close the settings window after selection

# Function to save the selected level to a JSON file
def save_level(level):
    with open("settings.json", "w") as file:
        json.dump({"level": level}, file)

# Function to load the selected level from a JSON file
def load_level():
    try:
        with open("settings.json", "r") as file:
            data = json.load(file)
            return data.get("level", "Beginner")
    except FileNotFoundError:
        return "Beginner"

# Function to show statistics window in a monthly calendar view
def show_statistics():
    try:
        with open("exercise_totals.json", "r") as file:
            data = json.load(file)
            
            # Get current month and year
            now = datetime.now()
            current_month = now.month
            current_year = now.year
            
            # Create a calendar for the current month
            cal = calendar.TextCalendar(calendar.SUNDAY)
            month_days = cal.itermonthdays(current_year, current_month)
            
            stats_message = f"Statistics for {calendar.month_name[current_month]} {current_year}\n\n"
            
            for day in month_days:
                if day != 0:
                    date_str = f"{current_year}-{current_month:02d}-{day:02d}"
                    weekday = datetime.strptime(date_str, "%Y-%m-%d").weekday()
                    if datetime.strptime(date_str, "%Y-%m-%d") > now:
                        continue
                    if date_str in data:
                        totals = data[date_str]
                        stats_message += f"{day}: Squats: {totals['squats']}, Pushups: {totals['pushups']}, Pullups: {totals['pullups']}, Leg Raises: {totals['leg raises']}\n"
                    else:
                        if weekday == 5 or weekday == 6:  # Saturday or Sunday
                            stats_message += f"{day}: Weekend\n"
                        else:
                            stats_message += f"{day}: Did nothing, lazy AF!\n"
            
            stats_window = tk.Toplevel(root)
            stats_window.title("Statistics")
            stats_window.overrideredirect(True)  # Remove the title bar
            center_window(stats_window, 400, 300)
            tk.Label(stats_window, text=stats_message, justify=tk.LEFT).pack(pady=20)
            tk.Button(stats_window, text="Close", command=stats_window.destroy).pack()
            
    except FileNotFoundError:
        messagebox.showinfo("Statistics", "No statistics available.")

# Function to show about window
def show_about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.overrideredirect(True)  # Remove the title bar
    center_window(about_window, 300, 150)
    tk.Label(about_window, text="DevFit for MS Windows.\nKeeping the flab at bay\none workstation at a time.").pack(pady=20)
    tk.Button(about_window, text="Close", command=about_window.destroy).pack()

# Function to start dragging the window
def start_drag(event):
    root.x = event.x
    root.y = event.y

# Function to drag the window and snap to edges
def drag_window(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    snap_threshold = 20

    if abs(x) < snap_threshold:
        x = 0
    elif abs(x + root.winfo_width() - screen_width) < snap_threshold:
        x = screen_width - root.winfo_width()

    elif abs(y + root.winfo_height() - screen_height) < snap_threshold:
        y = screen_height - root.winfo_height()

    root.geometry(f"+{x}+{y}")

# Function to center a window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f"{width}x{height}+{position_right}+{position_top}")

# Create the main window
root = tk.Tk()
root.title("DevFit")
root.overrideredirect(True)  # Remove the title bar
root.attributes("-topmost", True)  # Keep the window on top of all other windows

# Bind mouse events for dragging the window
root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", drag_window)

# Create StringVar variables to hold the exercise counts
squats_count = tk.StringVar()
pushups_count = tk.StringVar()
pullups_count = tk.StringVar()
leg_raises_count = tk.StringVar()

# Initialize the counts
squats_count.set("Squats: 0")
pushups_count.set("Pushups: 0")
pullups_count.set("Pullups: 0")
leg_raises_count.set("Leg Raises: 0")

# Create and place the labels and buttons
frame_squats = tk.Frame(root)
frame_squats.pack(fill=tk.X)
tk.Label(frame_squats, textvariable=squats_count).pack(side=tk.LEFT)
tk.Button(frame_squats, text="✔", command=reset_squats).pack(side=tk.RIGHT)

frame_pushups = tk.Frame(root)
frame_pushups.pack(fill=tk.X)
tk.Label(frame_pushups, textvariable=pushups_count).pack(side=tk.LEFT)
tk.Button(frame_pushups, text="✔", command=reset_pushups).pack(side=tk.RIGHT)

frame_pullups = tk.Frame(root)
frame_pullups.pack(fill=tk.X)
tk.Label(frame_pullups, textvariable=pullups_count).pack(side=tk.LEFT)
tk.Button(frame_pullups, text="✔", command=reset_pullups).pack(side=tk.RIGHT)

frame_leg_raises = tk.Frame(root)
frame_leg_raises.pack(fill=tk.X)
tk.Label(frame_leg_raises, textvariable=leg_raises_count).pack(side=tk.LEFT)
tk.Button(frame_leg_raises, text="✔", command=reset_leg_raises).pack(side=tk.RIGHT)

# Create right-click menu
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Settings", command=show_settings)
menu.add_command(label="Statistics", command=show_statistics)
menu.add_command(label="About", command=show_about)
menu.add_command(label="Exit", command=root.quit)

# Show right-click menu on right-click event
def show_menu(event):
    menu.post(event.x_root, event.y_root)

root.bind("<Button-3>", show_menu)

# Set default intervals for exercise levels
squat_interval = 600000  # 10 minutes
pushup_interval = 1200000  # 20 minutes
pullup_interval = 1200000  # 20 minutes
leg_raise_interval = 1200000  # 20 minutes

# Load the saved level and set intervals accordingly
current_level = load_level()
set_level(current_level, False)

# Update the counts initially and schedule the first increment
update_squats()
update_pushups()
update_pullups()
update_leg_raises()

# Run the application
root.mainloop()