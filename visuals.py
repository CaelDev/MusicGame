import wx
import load, bugPrevention, random, time, requests, os, json
from io import BytesIO
import wx.media
from pydub import AudioSegment
import simpleaudio as sa


def getTypesRoutes():
    return [
        "Song Name",
        "Album Cover",
        "Album Name",
        "Author Name",
        "Release Date",
        "Song Length",
        "Audio Sample",
        "Lyrics",
    ], [
        "track;name",
        "track;album;images;1;url",
        "track;album;name",
        "track;artists;0;name",
        "track;album;release_date",
        "track;duration_ms",
        "track;preview_url",
        "track;external_urls;spotify",
    ]


options, techOpt = getTypesRoutes()


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
        self.media = wx.media.MediaCtrl(self.panel)

        self.SetBackgroundColour(wx.Colour(21, 76, 121))

        self.first_choice = None
        self.second_choice = None
        self.num_input = None

        self.first_selected_button = None
        self.second_selected_button = None

        self.score = 0
        self.incorrect = 0

        self.audio_obj = None

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
                elif (self.dataType[1].split(";"))[x] == "1":
                    p = p[1]
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

        if question.startswith("https://i.scdn.co"):
            response = requests.get(question)
            image_data = response.content

            # Load the image data into a wx.Image object
            self.image = wx.Image(BytesIO(image_data), wx.BITMAP_TYPE_ANY)

            # Display the image using a StaticBitmap
            self.bitmap = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(self.image))
            self.sizer.Add(self.bitmap, 0, wx.CENTER | wx.ALL, 10)
        elif question.startswith("https://p.scdn.co"):
            response = requests.get(question)
            if response.status_code == 200:
                with open(f"temp_files/q.mp3", "wb") as f:
                    f.write(response.content)

            self.ans = wx.Button(self.panel, label=f"Listen to question")
            self.ans.Bind(wx.EVT_BUTTON, self.on_music_button_click)
            self.ans.option_index = "q"
            self.sizer.Add(self.ans, 0, wx.ALL | wx.CENTER, 10)
        elif question.startswith("https://open.spotify.com/"):
            self.get_lyrics(self.get_option_text(question), 0)
            string = ""
            with open("temp_files/lyrics0.json") as l:
                l = json.loads(l.read())

            e = random.randint(0, len(l["lines"]) - 3)

            for m in range(3):
                string = string + l["lines"][str(e + m)]["words"] + "\n"

            self.sizer.Add(
                wx.StaticText(self.panel, label=string), 0, wx.ALL | wx.CENTER, 10
            )
        else:
            self.sizer.Add(
                wx.StaticText(self.panel, label=question), 0, wx.ALL | wx.CENTER, 10
            )

        self.option_buttons = []
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)  # New sizer for buttons
        for i, option in enumerate(options):
            if self.get_option_text(option).startswith("https://i.scdn.co"):
                response = requests.get(self.get_option_text(option))
                image_data = response.content
                image = wx.Image(BytesIO(image_data), wx.BITMAP_TYPE_ANY)
                image = image.Scale(150, 150, wx.IMAGE_QUALITY_HIGH)
                bitmap = wx.Bitmap(image)
                btn = wx.StaticBitmap(self.panel, wx.ID_ANY, bitmap)
                btn.Bind(wx.EVT_LEFT_DOWN, self.on_option_selected)
            elif self.get_option_text(option).startswith("https://p.scdn.co"):
                response = requests.get(self.get_option_text(option))
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    with open(f"temp_files/song{i}.mp3", "wb") as f:
                        f.write(response.content)
                btn = wx.Button(self.panel, label=f"Pick #{i}")
                btn.Bind(wx.EVT_BUTTON, self.on_option_selected)
            elif self.get_option_text(option).startswith("https://open.spotify.com/"):
                self.get_lyrics(self.get_option_text(option), i)
                string = ""
                with open(f"temp_files/lyrics{i}.json") as l:
                    l = json.loads(l.read())

                e = random.randint(0, len(l["lines"]) - 3)

                for m in range(3):
                    string = string + l["lines"][str(e + m)]["words"] + "\n"

                btn = wx.Button(self.panel, label=string)
                btn.Bind(wx.EVT_BUTTON, self.on_option_selected)
            else:
                btn = wx.Button(self.panel, label=self.get_option_text(option))
                btn.Bind(wx.EVT_BUTTON, self.on_option_selected)
            btn.option_index = i  # Store the index of the option in the button
            self.option_buttons.append(btn)
            button_sizer.Add(btn, 0, wx.ALL, 5)  # Add to the new sizer
        self.sizer.Add(button_sizer, 0, wx.CENTER)
        if (self.get_option_text(options[0])).startswith("https://p.scdn.co"):
            button_sizer = wx.BoxSizer(wx.HORIZONTAL)

            for i, option in enumerate(options):
                btn = wx.Button(self.panel, label=f"Play #{i}")
                btn.Bind(wx.EVT_BUTTON, self.on_music_button_click)
                btn.option_index = i
                button_sizer.Add(btn, 0, wx.ALL, 5)
        self.sizer.Add(button_sizer, 0, wx.CENTER)

        self.panel.Layout()

    def on_music_button_click(self, event):
        if self.audio_obj and self.audio_obj.is_playing():
            self.audio_obj.stop()
        if (event.GetEventObject().option_index) == "q":
            audio = AudioSegment.from_mp3(f"temp_files/q.mp3")
        else:
            audio = AudioSegment.from_mp3(
                f"temp_files/song{event.GetEventObject().option_index}.mp3"
            )
        wave_obj = sa.WaveObject.from_wave_file(
            audio.export(format="wav", codec="pcm_s16le")
        )
        self.audio_obj = wave_obj.play()

    def get_option_text(self, option):
        o = option
        for x in range(len(self.dataType[0].split(";"))):
            if (self.dataType[0].split(";"))[x] == "0":
                o = o[0]
            elif (self.dataType[0].split(";"))[x] == "1":
                o = o[1]
            else:
                try:
                    o = o[(self.dataType[0].split(";"))[x]]
                except:
                    return o
        return o

    def on_option_selected(self, event):
        if self.audio_obj and self.audio_obj.is_playing():
            self.audio_obj.stop()
        selected_button = event.GetEventObject()
        selected_index = selected_button.option_index
        if selected_index == self.correct_index:
            self.score += 1
        else:
            self.incorrect += 1
        self.next_question()

    def get_lyrics(self, url, u):
        os.system(f"syrics --directory temp_files/ {url}")

        with open("temp_files/song.lrc") as f:
            x = f.read()
        x = x.split("\n")
        x.remove(x[-1])
        for i in range(4):
            x.remove(x[0])
        y = {"lines": {}}
        num = 0
        for i in x:
            i = (str(i).replace("[", "")).split("] ")
            z = {num: {"startTimeMs": i[0], "words": i[1]}}
            y["lines"].update(z)
            num = num + 1

        with open(f"temp_files/lyrics{u}.json", "w") as f:
            f.write(json.dumps(y, indent=2))

        os.system("")


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
