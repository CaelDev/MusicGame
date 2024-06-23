import wx
import game, load, bugPrevention, random, time

options = (game.getTypesRoutes())[0]


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Game Options")
        self.frame.Show()
        return True


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.first_choice = None
        self.second_choice = None

        self.first_selected_button = None
        self.second_selected_button = None

        self.score = 0
        self.incorrect = 0

        self.create_first_option_buttons()
        self.create_second_option_buttons()
        self.create_play_button()

        self.sizer.Fit(self)

    def create_first_option_buttons(self):
        self.first_buttons = []
        self.first_box = wx.BoxSizer(wx.HORIZONTAL)
        for option in options:
            btn = wx.Button(self.panel, label=option)
            btn.Bind(wx.EVT_BUTTON, self.on_first_option_selected)
            self.first_buttons.append(btn)
            self.first_box.Add(btn, 0, wx.ALL, 5)
        self.sizer.Add(self.first_box, 0, wx.CENTER)

    def on_first_option_selected(self, event):
        if self.first_selected_button:
            self.first_selected_button.SetBackgroundColour(wx.NullColour)
        self.first_choice = event.GetEventObject().GetLabel()
        self.first_selected_button = event.GetEventObject()
        self.first_selected_button.SetBackgroundColour(
            wx.Colour(173, 216, 230)
        )  # Light blue
        self.first_selected_button.Refresh()
        self.check_play_button()

    def create_second_option_buttons(self):
        self.second_buttons = []
        self.second_box = wx.BoxSizer(wx.HORIZONTAL)
        for option in options:
            btn = wx.Button(self.panel, label=option)
            btn.Bind(wx.EVT_BUTTON, self.on_second_option_selected)
            self.second_buttons.append(btn)
            self.second_box.Add(btn, 0, wx.ALL, 5)
        self.sizer.Add(self.second_box, 0, wx.CENTER)

    def on_second_option_selected(self, event):
        if self.second_selected_button:
            self.second_selected_button.SetBackgroundColour(wx.NullColour)
        self.second_choice = event.GetEventObject().GetLabel()
        self.second_selected_button = event.GetEventObject()
        self.second_selected_button.SetBackgroundColour(
            wx.Colour(173, 216, 230)
        )  # Light blue
        self.second_selected_button.Refresh()
        self.check_play_button()

    def create_play_button(self):
        self.play_button = wx.Button(self.panel, label="Play")
        self.play_button.Disable()
        self.play_button.Bind(wx.EVT_BUTTON, self.on_play)
        self.sizer.Add(self.play_button, 0, wx.ALL | wx.CENTER, 10)

    def check_play_button(self):
        if self.first_choice and self.second_choice:
            self.play_button.Enable()
        else:
            self.play_button.Disable()

    def on_play(self, event):
        self.play_button.Disable()
        self.choicesPerQuestion = 5
        self.albumURL = "https://open.spotify.com/playlist/7hkUzF20c6rHYyRVs6oJIS?si=0950b8a91ed944f3&pt=1e92df187570f8601f1afb832c826187"
        self.songs = load.getPlaylist(self.albumURL)
        self.dataType = "track;artists;0;name!track;name".split("!")
        self.next_question()

    def next_question(self):
        options = []
        if bugPrevention.ensureEnoughDifferentItems(
            self.dataType[1], self.choicesPerQuestion, self.songs
        ):
            for i in range(self.choicesPerQuestion):
                rand = random.randint(0, len(self.songs) - 1)
                while self.songs[rand] in options:  # ensure no duplicates
                    rand = random.randint(0, len(self.songs) - 1)
                options.append(self.songs[rand])
                del self.songs[rand]
            self.correct_index = random.randint(0, self.choicesPerQuestion - 1)
            self.correct_option = options[self.correct_index]
            p = self.correct_option
            for x in range(len(self.dataType[1].split(";"))):
                if (self.dataType[1].split(";"))[x] == "0":
                    p = p[0]
                else:
                    p = p[(self.dataType[1].split(";"))[x]]
            self.display_question_and_options(p, options)
        else:
            wx.MessageBox(
                "Not enough songs to continue the game.",
                "Info",
                wx.OK | wx.ICON_INFORMATION,
            )

    def display_question_and_options(self, question, options):
        self.sizer.Clear(True)

        # Create a horizontal sizer for Correct and Incorrect labels
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.correct_label = wx.StaticText(self.panel, label=f"Correct: {self.score}")
        self.correct_label.SetForegroundColour(wx.GREEN)
        label_sizer.Add(self.correct_label, 0, wx.ALL | wx.CENTER, 10)

        self.incorrect_label = wx.StaticText(
            self.panel, label=f"Incorrect: {self.incorrect}"
        )
        self.incorrect_label.SetForegroundColour(wx.RED)
        label_sizer.Add(self.incorrect_label, 0, wx.ALL | wx.CENTER, 10)

        self.sizer.Add(label_sizer, 0, wx.CENTER)

        self.sizer.Add(
            wx.StaticText(self.panel, label=question), 0, wx.ALL | wx.CENTER, 10
        )

        self.option_buttons = []
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)  # New sizer for buttons
        for i, option in enumerate(options):
            btn = wx.Button(self.panel, label=self.get_option_text(option))
            btn.Bind(wx.EVT_BUTTON, self.on_option_selected)
            btn.option_index = i  # Store the index of the option in the button
            self.option_buttons.append(btn)
            button_sizer.Add(btn, 0, wx.ALL, 5)  # Add to the new sizer
        self.sizer.Add(
            button_sizer, 0, wx.CENTER
        )  # Add the new sizer to the main sizer

        self.panel.Layout()

    def get_option_text(self, option):
        o = option
        for x in range(len(self.dataType[0].split(";"))):
            if (self.dataType[0].split(";"))[x] == "0":
                o = o[0]
            else:
                o = o[(self.dataType[0].split(";"))[x]]
        return o

    def on_option_selected(self, event):
        selected_button = event.GetEventObject()
        selected_index = selected_button.option_index
        if selected_index == self.correct_index:
            wx.MessageBox("Correct!", "Result", wx.OK | wx.ICON_INFORMATION)
            self.score += 1
        else:
            wx.MessageBox(
                f"Wrong! Answer was {self.correct_index + 1}",
                "Result",
                wx.OK | wx.ICON_ERROR,
            )
            self.incorrect += 1
        self.next_question()


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
