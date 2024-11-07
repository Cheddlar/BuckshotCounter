import tkinter as tk
import os
import urllib.request

def download_image(url, save_path):
    try:
        urllib.request.urlretrieve(url, save_path)
        print(f"Image successfully downloaded: {save_path}")
    except Exception as e:
        print(f"Error downloading image: {e}")

root_dir = os.path.dirname(os.path.abspath(__file__))
image_url = "https://github.com/Cheddlar/BuckshotCounter/blob/main/favicon.png?raw=true"
save_path = os.path.join(root_dir, "favicon.png")

if not os.path.exists(save_path):
    download_image(image_url, save_path)

if not os.path.exists(save_path):
    print("Failed to download the image. Exiting.")
    exit(1)

class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buckshot Counter | Made by Cheddlar")  # Title for the Window of the Calculator
        self.root.config(bg="#2e2e2e")  # HEX Colour for the background, tho grey looks kinda nice
        self.root.grid_rowconfigure(0, weight=1)  # This should allow for sizing to be changed on the fly, but default is good enough
        self.root.grid_columnconfigure(0, weight=1)

        # Icon Stuff
        icon = tk.PhotoImage(file=save_path)  # tkinter icon image file
        root.iconphoto(False, icon)  # This sets the initial icon

        # Counters for each of the Live and Blank rounds
        self.live_count = 0  # Starting live rounds
        self.blank_count = 0  # Starting blank rounds
        self.rounds = [{"live": 0, "blank": 0, "marked": None} for _ in range(8)]  # 8 rounds, each with live, blank, and marked status

        # Title label
        self.title_label = tk.Label(root, text="Buckshot Counter", font=("Arial", 24, "bold"), fg="white", bg="#2e2e2e")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create the display labels for Live and Blank (row 1)
        self.live_label = tk.Label(root, text=f"Live: {self.live_count}", font=("Arial", 18), fg="white", bg="#2e2e2e")
        self.live_label.grid(row=1, column=0, padx=20)

        self.blank_label = tk.Label(root, text=f"Blank: {self.blank_count}", font=("Arial", 18), fg="white", bg="#2e2e2e")
        self.blank_label.grid(row=1, column=1, padx=20)

        # Percentage indicator label (row 2)
        self.percentage_label = tk.Label(root, text="Next Shot: 0% Live", font=("Arial", 16), fg="white", bg="#2e2e2e")
        self.percentage_label.grid(row=2, column=0, columnspan=3, pady=10)

        # Create the buttons for adding Live and Blank (row 3)
        self.red_button = tk.Button(root, text="+ (Live)", command=self.increment_live, bg="#e74c3c", fg="white", font=("Arial", 14), relief="raised", padx=20, pady=10)
        self.red_button.grid(row=3, column=0, padx=20, pady=10)

        self.blue_button = tk.Button(root, text="+ (Blank)", command=self.increment_blank, bg="#3498db", fg="white", font=("Arial", 14), relief="raised", padx=20, pady=10)
        self.blue_button.grid(row=3, column=1, padx=20, pady=10)

        # Create the buttons for deducting Live and Blank (row 4)
        self.deduct_live_button = tk.Button(root, text="- (Live)", command=self.decrement_live, bg="#e74c3c", fg="white", font=("Arial", 14), relief="raised", padx=20, pady=10)
        self.deduct_live_button.grid(row=4, column=0, padx=20, pady=10)

        self.deduct_blank_button = tk.Button(root, text="- (Blank)", command=self.decrement_blank, bg="#3498db", fg="white", font=("Arial", 14), relief="raised", padx=20, pady=10)
        self.deduct_blank_button.grid(row=4, column=1, padx=20, pady=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_counters, bg="#95a5a6", fg="white", font=("Arial", 14), relief="raised", padx=20, pady=10)
        self.reset_button.grid(row=4, column=2, padx=20, pady=10)

        # Clear Rounds Button (row 5)
        self.clear_rounds_button = tk.Button(root, text="Clear Rounds", command=self.reset_rounds, bg="#95a5a6", fg="white", font=("Arial", 14), relief="raised", padx=20, pady=10)
        self.clear_rounds_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Round Display (row 6 and below)
        self.round_display = tk.Label(root, text="Rounds", font=("Arial", 18), fg="white", bg="#2e2e2e")
        self.round_display.grid(row=6, column=0, columnspan=3, pady=10)

        self.round_labels = []
        for i in range(8):  # Change to 8 rounds
            # Create a frame for each round
            round_frame = tk.Frame(root, bg="#2e2e2e")
            round_frame.grid(row=7 + i, column=0, columnspan=3, pady=5)

            label = tk.Label(round_frame, text=f"Round {i+1}: ", font=("Arial", 14), fg="white", bg="#2e2e2e")
            label.pack(side=tk.LEFT)

            # Create a label for displaying "Live" or "Blank"
            status_label = tk.Label(
                round_frame, 
                text="",  # Start with empty text
                bg="#2e2e2e", 
                fg="white", 
                font=("Arial", 14)
            )
            status_label.pack(side=tk.LEFT, padx=5)

            # Store the label for later updates
            self.round_labels.append(status_label)

            # Small buttons for adding live and blank rounds
            add_live_button = tk.Button(
                round_frame, 
                text="+", 
                command=lambda index=i: self.add_live_to_round(index), 
                bg="#e74c3c", 
                fg="white", 
                font=("Arial", 12), 
                relief="raised", 
                padx=5, pady=5
            )
            add_live_button.pack(side=tk.LEFT, padx=5)

            add_blank_button = tk.Button(
                round_frame, 
                text="-", 
                command=lambda index=i: self.add_blank_to_round(index), 
                bg="#3498db", 
                fg="white", 
                font=("Arial", 12), 
                relief="raised", 
                padx=5, pady=5
            )
            add_blank_button.pack(side=tk.LEFT, padx=5)

            # Clear button for specific round
            clear_button = tk.Button(
                round_frame, 
                text="C", 
                command=lambda index=i: self.clear_round(index), 
                bg="#95a5a6", 
                fg="white", 
                font=("Arial", 12), 
                relief="raised", 
                padx=5, pady=5
            )
            clear_button.pack(side=tk.LEFT, padx=5)

    def increment_live(self):
        self.live_count += 1
        self.update_display()

    def increment_blank(self):
        self.blank_count += 1
        self.update_display()

    def decrement_live(self):
        if self.live_count > 0:  # Lock it to 0 minimum
            self.live_count -= 1
        self.update_display()

    def decrement_blank(self):
        if self.blank_count > 0:  # Lock it to 0 minimum
            self.blank_count -= 1
        self.update_display()

    def reset_counters(self):
        self.live_count = 0  # Reset to 0 by default
        self.blank_count = 0  # Reset to 0 by default
        self.update_display()

    def add_live_to_round(self, round_index):
        if self.live_count > 0:  # Only add if there are live rounds left
            self.rounds[round_index]["live"] += 1
            self.rounds[round_index]["marked"] = "live"  # Mark the round as live
            self.live_count -= 1  # Deduct one live from the total count
            self.update_round_display()
            self.update_display()  # Update the display to reflect the new counts
            self.update_percentage()  # Update percentage after adding live

    def add_blank_to_round(self, round_index):
        if self.blank_count > 0:  # Only add if there are blank rounds left
            self.rounds[round_index]["blank"] += 1
            self.rounds[round_index]["marked"] = "blank"  # Mark the round as blank
            self.blank_count -= 1  # Deduct one blank from the total count
            self.update_round_display()
            self.update_display()  # Update the display to reflect the new counts
            self.update_percentage()  # Update percentage after adding blank

    def clear_round(self, round_index):
        # Clear the specific round's input
        if self.rounds[round_index]["marked"] == "live":
            self.live_count += self.rounds[round_index]["live"]  # Restore live rounds
        elif self.rounds[round_index]["marked"] == "blank":
            self.blank_count += self.rounds[round_index]["blank"]  # Restore blank rounds

        self.rounds[round_index]["live"] = 0
        self.rounds[round_index]["blank"] = 0
        self.rounds[round_index]["marked"] = None  # Clear the marked status
        self.update_round_display()
        self.update_display()  # Update the display to reflect the new counts
        self.update_percentage()  # Update percentage after clearing

    def reset_rounds(self):
        # Reset all round counters
        self.rounds = [{"live": 0, "blank": 0, "marked": None} for _ in range(8)]  # Change to 8 rounds
        self.update_round_display()

        # Reset the main counters (Live and Blank)
        self.live_count = 0  # Reset to 0
        self.blank_count = 0  # Reset to 0
        self.update_display()

    def update_display(self):
        # Update the main Live and Blank counters
        self.live_label.config(text=f"Live: {self.live_count}")
        self.blank_label.config(text=f"Blank: {self.blank_count}")
        self.update_percentage()  # Update the percentage display

    def update_round_display(self):
        # Update the display for each round
        for i in range(8):  # Change to 8 rounds
            if self.rounds[i]["live"] > 0:
                self.round_labels[i].config(text="Live")  # Set to "Live" if there are live rounds
            elif self.rounds[i]["blank"] > 0:
                self.round_labels[i].config(text="Blank")  # Set to "Blank" if there are blank rounds
            else:
                self.round_labels[i].config(text="")  # Set to empty if no rounds

    def update_percentage(self):
        total_live = sum(round["live"] for round in self.rounds if round["marked"] == "live")
        total_blank = sum(round["blank"] for round in self.rounds if round["marked"] == "blank")
        total_marked = total_live + total_blank

        # fix remaining live and blank rounds
        remaining_live = self.live_count
        remaining_blank = self.blank_count

        total_remaining = remaining_live + remaining_blank

        if total_remaining > 0:
            live_percentage = (remaining_live / total_remaining) * 100
            blank_percentage = (remaining_blank / total_remaining) * 100
            self.percentage_label.config(text=f"Next Shot: {int(live_percentage)}% Live, {int(blank_percentage)}% Blank")
        else:
            self.percentage_label.config(text="Next Shot: 0% Live, 0% Blank")  # Default when no marked rounds or shots taken midgame

root = tk.Tk()
app = CounterApp(root)

root.mainloop()

# For anyone trying to debug this spaghetti code, i hope you enjoy, this took me 3 hours to throw together and perfect, whilst learning tkinter via this for the first time! :)