import wx
import game, load, bugPrevention, random, time

options, techOpt = game.getTypesRoutes()


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Music Game")
        self.frame.Show()
        return True


class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        self.panel.SetBackgroundColour(wx.Colour(51, 161, 192))
        self.SetBackgroundColour(wx.Colour(21, 76, 121))

        self.first_choice = None
        self.second_choice = None
        self.num_input = None

        self.first_selected_button = None
        self.second_selected_button = None

        self.score = 0
        self.incorrect = 0

        self.create_num_input()
        self.create_first_option_buttons()
        self.create_second_option_buttons()
        self.create_play_button()
        self.triggerAll()

        self.sizer.Fit(self)

    def create_num_input(self):
        num_input_box = wx.BoxSizer(wx.HORIZONTAL)

        num_label = wx.StaticText(self.panel, label="Number of options (positive, >1):")
        num_input_box.Add(num_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        # Create the text input control
        self.num_input = wx.TextCtrl(
            self.panel, size=(100, -1)
        )  # Width set to 100 pixels
        num_input_box.Add(self.num_input, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        # Add the horizontal sizer to the main vertical sizer
        self.sizer.Add(num_input_box, 0, wx.ALIGN_CENTER)

        self.num_input.Bind(wx.EVT_TEXT, self.check_play_button)

    def create_first_option_buttons(self):
        self.first_buttons = []
        self.first_box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self.panel, label="Question type:")
        self.first_box.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        for option in options:
            btn = wx.Button(self.panel, label=option)
            btn.Bind(wx.EVT_BUTTON, self.on_first_option_selected)
            self.first_buttons.append(btn)
            self.first_box.Add(btn, 0, wx.ALL, 5)
        self.sizer.Add(self.first_box, 0, wx.CENTER)

    def on_first_option_selected(self, event):
        if self.first_selected_button:
            self.first_selected_button.SetBackgroundColour(wx.NullColour)
        try:
            self.first_choice = event.GetEventObject().GetLabel()

            self.first_selected_button = event.GetEventObject()
            self.first_selected_button.SetBackgroundColour(
                wx.Colour(173, 216, 230)
            )  # Light blue
            self.first_selected_button.Refresh()
            self.check_play_button()
        except:
            None

    def triggerAll(self):
        for i in range(len(self.first_buttons)):
            if 0 <= i < len(self.first_buttons):
                button_to_select = self.first_buttons[i]
                event = wx.CommandEvent(wx.EVT_BUTTON.typeId, button_to_select.GetId())
                wx.PostEvent(button_to_select, event)
        for button in self.first_buttons:
            button.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
            )
        self.panel.Refresh()
        self.first_selected_button = None
        self.first_choice = None

        for i in range(len(self.second_buttons)):
            if 0 <= i < len(self.second_buttons):
                button_to_select = self.second_buttons[i]
                event = wx.CommandEvent(wx.EVT_BUTTON.typeId, button_to_select.GetId())
                wx.PostEvent(button_to_select, event)
        for button in self.second_buttons:
            button.SetBackgroundColour(
                wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE)
            )
        self.panel.Refresh()
        self.second_selected_button = None
        self.second_choice = None

    def create_second_option_buttons(self):
        self.second_buttons = []
        self.second_box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self.panel, label="Answer type:")
        self.second_box.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        for option in options:
            btn = wx.Button(self.panel, label=option)
            btn.Bind(wx.EVT_BUTTON, self.on_second_option_selected)
            self.second_buttons.append(btn)
            self.second_box.Add(btn, 0, wx.ALL, 5)
        self.sizer.Add(self.second_box, 0, wx.CENTER)

    def on_second_option_selected(self, event):
        if self.second_selected_button:
            self.second_selected_button.SetBackgroundColour(wx.NullColour)
        try:
            self.second_choice = event.GetEventObject().GetLabel()

            self.second_selected_button = event.GetEventObject()
            self.second_selected_button.SetBackgroundColour(
                wx.Colour(173, 216, 230)
            )  # Light blue
            self.second_selected_button.Refresh()
            self.check_play_button()
        except:
            None

    def create_play_button(self):
        self.play_button = wx.Button(self.panel, label="Play")
        self.play_button.SetBackgroundColour(wx.NullColour)
        self.play_button.Refresh()
        self.play_button.Disable()
        self.play_button.Bind(wx.EVT_BUTTON, self.on_play)
        self.sizer.Add(self.play_button, 0, wx.ALL | wx.CENTER, 10)
        self.play_button.SetBackgroundColour(wx.NullColour)
        self.play_button.Refresh()

    def check_play_button(self, event=None):
        if self.first_choice and self.second_choice and self.validate_num_input():
            self.play_button.Enable()
        else:
            self.play_button.Disable()

    def validate_num_input(self):
        try:
            num = int(self.num_input.GetValue())
            if num > 1:
                return True
            else:
                return False
        except ValueError:
            return False

    def on_play(self, event):
        self.play_button.Disable()
        self.albumURL = "https://open.spotify.com/playlist/7hkUzF20c6rHYyRVs6oJIS?si=0950b8a91ed944f3&pt=1e92df187570f8601f1afb832c826187"
        self.songs = load.getPlaylist(self.albumURL)
        self.choicesPerQuestion = int(self.num_input.GetValue())

        x = 0
        while options[x] != self.first_choice:
            x += 1
        self.dataType = techOpt[x]
        x = 0
        while options[x] != self.second_choice:
            x += 1
        self.dataType = techOpt[x] + "!" + self.dataType

        self.dataType = self.dataType.split("!")
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
            self.score += 1
        else:
            self.incorrect += 1
        self.next_question()


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
