from tkinter.ttk import Progressbar
import tkinter.simpledialog
import tkinter.messagebox
import random
import numpy as np

# List of possible colours
colours = ['Red', 'Blue', 'Green', 'Pink', 'Black',
           'Yellow', 'Orange', 'White', 'Purple', 'Brown']
score = 0
timeleft = 30
player_name = ""
total_attempts = 0  # Total rounds attempted for accuracy calculation
current_streak = 0
highest_streak = 0

# Function to start the game
def startGame(event):
    global timeleft, player_name, total_attempts, current_streak, highest_streak
    if timeleft == 30:
        # Prompt player to enter their name
        if not player_name:
            player_name = tkinter.simpledialog.askstring("Name Entry", "Enter your name:")
            if not player_name:
                player_name = "Anonymous"
        total_attempts = 0  # Reset attempts
        current_streak = 0
        highest_streak = 0
        countdown()
    nextColour()

# Function to choose and display the next colour
def nextColour():
    global score, timeleft, total_attempts, current_streak, highest_streak

    if timeleft > 0:
        e.focus_set()

        # Check if the input matches the colour name
        if e.get().lower() == colours[1].lower():
            score += 1
            current_streak += 1
            highest_streak = max(highest_streak, current_streak)
        else:
            current_streak = 0

        total_attempts += 1
        e.delete(0, tkinter.END)
        random.shuffle(colours)

        if len(colours) >= 2:
            label.config(fg=str(colours[1]), text=str(colours[0]))

        scoreLabel.config(text="Score: " + str(score))

# Countdown timer function with a progress bar
def countdown():
    global timeleft

    if timeleft > 0:
        timeleft -= 1
        progress["value"] = (timeleft / 30) * 100
        timeLabel.config(text="Time left: " + str(timeleft))
        timeLabel.after(1000, countdown)
    else:
        save_score()
        provide_feedback()

# Function to save the score to a file
def save_score():
    global player_name, score
    with open("leaderboard.txt", "a") as f:
        f.write(f"{player_name}: {score}\n")
    display_leaderboard()

# Function to retrieve leaderboard data
def get_leaderboard():
    try:
        with open("leaderboard.txt", "r") as f:
            scores = [line.strip().split(": ") for line in f.readlines()]
            return [(name, int(score)) for name, score in scores]
    except FileNotFoundError:
        return []

# Function to display the leaderboard
def display_leaderboard():
    scores = get_leaderboard()
    if scores:
        top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
        leaderboard = "\n".join([f"#{i + 1} {name}: {score}" for i, (name, score) in enumerate(top_scores)])
        tkinter.messagebox.showinfo("Leaderboard", f"Game Over!\n\nYour Score: {score}\n\nTop Scores:\n{leaderboard}")
    else:
        tkinter.messagebox.showinfo("Leaderboard", "No scores yet!")

# Function to provide AI-driven feedback
def provide_feedback():
    global total_attempts, score, highest_streak

    if total_attempts > 0:
        accuracy = (score / total_attempts) * 100
        avg_response_time = np.random.uniform(0.5, 2.0, total_attempts).mean()

        feedback = f"Accuracy: {accuracy:.1f}%\n"
        feedback += f"Highest streak: {highest_streak}\n"

        # Accuracy feedback
        if accuracy > 80:
            feedback += "Fantastic accuracy! Keep up the great work.\n"
        elif accuracy > 50:
            feedback += "Good effort! Focus on increasing your accuracy.\n"
        else:
            feedback += "Practice makes perfect. Keep trying!\n"

        # Response time feedback
        if avg_response_time < 1.0:
            feedback += "Your reaction time is excellent. Well done!\n"
        else:
            feedback += "Try to improve your reaction time for a higher score.\n"

        # Comparison to top players
        scores = get_leaderboard()
        if scores:
            top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
            avg_top_score = sum(score for _, score in top_scores) / len(top_scores)
            feedback += f"The average score of the top players is {avg_top_score:.1f}.\n"
            if score >= avg_top_score:
                feedback += "You’re performing at the level of the top players. Amazing work!"
            else:
                feedback += f"You’re {avg_top_score - score:.1f} points away from the average top score. Keep practicing!"
        else:
            feedback += "Be the first to set a high score on the leaderboard!"

        tkinter.messagebox.showinfo("AI Feedback", feedback)
    else:
        tkinter.messagebox.showinfo("AI Feedback", "No data available to provide feedback.")

def show_leaderboard():
    scores = get_leaderboard()
    if scores:
        top_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]
        leaderboard = "\n".join([f"#{i + 1} {name}: {score}" for i, (name, score) in enumerate(top_scores)])
        tkinter.messagebox.showinfo("Leaderboard", f"Top Scores:\n{leaderboard}")
    else:
        tkinter.messagebox.showinfo("Leaderboard", "No scores yet!")


root = tkinter.Tk()
root.title("COLOURGAME!")
root.geometry("400x300")
root.config(bg="light grey")

# Instructions label
instructions = tkinter.Label(root, text="Type in the colours of the words, not the word text!",
                             font=('Arial', 11), bg="light grey", fg="black")
instructions.pack()

# Score label
scoreLabel = tkinter.Label(root, text="Press Enter to start", font=('Arial', 11), bg="light grey", fg="black")
scoreLabel.pack()

# Time left label
timeLabel = tkinter.Label(root, text="Time left: " + str(timeleft), font=('Arial', 11), bg="light grey", fg="black")
timeLabel.pack()

# Progress bar for countdown
progress = Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack()

# Label for displaying colours
label = tkinter.Label(root, font=('Arial', 60), bg="light grey")
label.pack()

# Text entry box
e = tkinter.Entry(root)
root.bind('<Return>', startGame)
e.pack()
e.focus_set()

leaderboard_button = tkinter.Button(root, text="View Leaderboard", command=show_leaderboard)
leaderboard_button.pack()

root.mainloop()

