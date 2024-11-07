from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

class CounterApp(App):
    def build(self):
        self.live_count = 0
        self.blank_count = 0
        self.rounds = [{"live": 0, "blank": 0, "marked": None} for _ in range(8)]  # 8 rounds total for now
        
        root = BoxLayout(orientation='vertical', padding=110, spacing=35)

        # Title Label
        title_layout = BoxLayout(size_hint_y=None, height=140)
        title_label = Label(text="Buckshot Counter", font_size=68, color=(1, 1, 1, 1), size_hint_x=None, width=825, halign='center')
        title_label.bind(size=title_label.setter('text_size'))
        title_layout.add_widget(title_label)
        root.add_widget(title_layout)

        # Live and Blank Count
        count_layout = BoxLayout(size_hint_y=None, height=140, spacing=15, orientation='horizontal')
        self.live_label = Label(text=f"Live: {self.live_count}", font_size=62, color=(1, 1, 1, 1), size_hint_x=None, width=425, halign='center')
        self.live_label.bind(size=self.live_label.setter('text_size'))
        self.blank_label = Label(text=f"Blank: {self.blank_count}", font_size=62, color=(1, 1, 1, 1), size_hint_x=None, width=425, halign='center')
        self.blank_label.bind(size=self.blank_label.setter('text_size'))
        count_layout.add_widget(self.live_label)
        count_layout.add_widget(self.blank_label)
        root.add_widget(count_layout)

        # Percentage label
        percentage_layout = BoxLayout(size_hint_y=None, height=140, padding=(10, 0, 0, 0))
        self.percentage_label = Label(text="Next Shot: 0% Live, 0% Blank", font_size=56, color=(1, 1, 1, 1), size_hint_x=None, width=800)
        percentage_layout.add_widget(self.percentage_label)
        root.add_widget(percentage_layout)

        # Buttons for adding live and blank
        action_layout = BoxLayout(size_hint_y=None, height=170, spacing=15, orientation='horizontal')
        red_button = Button(text="+ (Live)", on_press=self.increment_live, background_color=(1, 0, 0, 1), color=(1, 1, 1, 1), size_hint_x=None, width=292, height=190)
        blue_button = Button(text="+ (Blank)", on_press=self.increment_blank, background_color=(0, 0, 1, 1), color=(1, 1, 1, 1), size_hint_x=None, width=292, height=190)
        reset_button = Button(text="Reset", on_press=self.reset_counters, background_color=(0.6, 0.6, 0.6, 1), color=(1, 1, 1, 1), size_hint_x=None, width=292, height=190)
        action_layout.add_widget(red_button)
        action_layout.add_widget(blue_button)
        action_layout.add_widget(reset_button)
        root.add_widget(action_layout)

        # Buttons for subtracting live and blank
        subtract_layout = BoxLayout(size_hint_y=None, height=170, spacing=15, orientation='horizontal')
        subtract_red_button = Button(text="- (Live)", on_press=self.decrement_live, background_color=(1, 0, 0, 1), color=(1, 1, 1, 1), size_hint_x=None, width=292, height=190)
        subtract_blue_button = Button(text="- (Blank)", on_press=self.decrement_blank, background_color=(0, 0, 1, 1), color=(1, 1, 1, 1), size_hint_x=None, width=292, height=190)
        clear_rounds_button = Button(text="New Rounds", on_press=self.reset_rounds, background_color=(0.6, 0.6, 0.6, 1), color=(1, 1, 1, 1), size_hint_x=None, width=292, height=190)
        subtract_layout.add_widget(subtract_red_button)
        subtract_layout.add_widget(subtract_blue_button)
        subtract_layout.add_widget(clear_rounds_button)
        root.add_widget(subtract_layout)

        # Rounds display
        round_layout = GridLayout(cols=1, size_hint_y=None, height=790)
        round_layout.bind(minimum_height=round_layout.setter('height'))

        self.round_labels = []
        for i in range(8):
            round_frame = BoxLayout(size_hint_y=None, height=140, spacing=15, orientation='horizontal')
            round_label = Label(text=f"Round {i + 1}: ", font_size=36, color=(1, 1, 1, 1), size_hint_x=None, width=245, halign='left')
            round_label.bind(size=round_label.setter('text_size'))
            status_label = Label(text="", font_size=36, color=(1, 1, 1, 1), size_hint_x=None, width=185, halign='left')
            status_label.bind(size=status_label.setter('text_size'))
            self.round_labels.append(status_label)

            # Add live round button
            add_live_button = Button(
                text="+", 
                on_press=lambda instance, index=i: self.add_live_to_round(index), 
                background_color=(1, 0, 0, 1), 
                color=(1, 1, 1, 1), 
                size_hint_x=None, 
                width=125,
                height=130
            )

            # Add blank round button
            add_blank_button = Button(
                text="-", 
                on_press=lambda instance, index=i: self.add_blank_to_round(index), 
                background_color=(0, 0, 1, 1), 
                color=(1, 1, 1, 1), 
                size_hint_x=None, 
                width=125,
                height=130
            )

            # Clear button for each round
            clear_button = Button(
                text="C", 
                on_press=lambda instance, index=i: self.clear_round(index), 
                background_color=(0.6, 0.6, 0.6, 1), 
                color=(1, 1, 1, 1), 
                size_hint_x=None, 
                width=125,
                height=130
            )

            round_frame.add_widget(round_label)
            round_frame.add_widget(status_label)
            round_frame.add_widget(add_live_button)
            round_frame.add_widget(add_blank_button)
            round_frame.add_widget(clear_button)

            round_layout.add_widget(round_frame)

        root.add_widget(round_layout)

        return root

    def increment_live(self, instance):
        self.live_count += 1
        self.update_display()

    def increment_blank(self, instance):
        self.blank_count += 1
        self.update_display()

    def decrement_live(self, instance):
        if self.live_count > 0:
            self.live_count -= 1
        self.update_display()

    def decrement_blank(self, instance):
        if self.blank_count > 0:
            self.blank_count -= 1
        self.update_display()

    def reset_counters(self, instance):
        self.live_count = 0
        self.blank_count = 0
        self.update_display()

    def add_live_to_round(self, round_index):
        if self.live_count > 0:
            self.rounds[round_index]["live"] += 1
            self.rounds[round_index]["marked"] = "live"
            self.live_count -= 1
            self.update_round_display()
            self.update_display()
            self.update_percentage()

    def add_blank_to_round(self, round_index):
        if self.blank_count > 0:
            self.rounds[round_index]["blank"] += 1
            self.rounds[round_index]["marked"] = "blank"
            self.blank_count -= 1
            self.update_round_display()
            self.update_display()
            self.update_percentage()

    def clear_round(self, round_index):
        if isinstance(round_index, int):
            if self.rounds[round_index]["marked"] == "live":
                self.live_count += self.rounds[round_index]["live"]
            elif self.rounds[round_index]["marked"] == "blank":
                self.blank_count += self.rounds[round_index]["blank"]
            self.rounds[round_index]["live"] = 0
            self.rounds[round_index]["blank"] = 0
            self.rounds[round_index]["marked"] = None
            self.update_round_display()
            self.update_display()
            self.update_percentage()

    def reset_rounds(self, instance):
        self.rounds = [{"live": 0, "blank": 0, "marked": None} for _ in range(8)]
        self.update_round_display()
        self.update_display()

    def update_display(self):
        self.live_label.text = f"Live: {self.live_count}"
        self.blank_label.text = f"Blank: {self.blank_count}"
        self.update_percentage()

    def update_round_display(self):
        for i in range(8):
            if self.rounds[i]["live"] > 0:
                self.round_labels[i].text = "Live"
            elif self.rounds[i]["blank"] > 0:
                self.round_labels[i].text = "Blank"
            else:
                self.round_labels[i].text = ""

    def update_percentage(self):
        total_live = sum(round["live"] for round in self.rounds if round["marked"] == "live")
        total_blank = sum(round["blank"] for round in self.rounds if round["marked"] == "blank")
        total_marked = total_live + total_blank

        remaining_live = self.live_count
        remaining_blank = self.blank_count
        total_remaining = remaining_live + remaining_blank

        if total_remaining > 0:
            live_percentage = (remaining_live / total_remaining) * 100
            blank_percentage = (remaining_blank / total_remaining) * 100
            self.percentage_label.text = f"Next Shot: {int(live_percentage)}% Live, {int(blank_percentage)}% Blank"
        else:
            self.percentage_label.text = "Next Shot: 0% Live, 0% Blank"

if __name__ == '__main__':
    CounterApp().run()
