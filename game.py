import json, load, random, os, bugPrevention


def game(dataType, albumURL, choicesPerQuestion, extra=[]):
    score = 0
    incorrect = 0
    songs = load.getPlaylist(albumURL)
    dataType = dataType.split("!")

    while choicesPerQuestion < len(songs):
        options = []
        if bugPrevention.ensureEnoughDifferentItems(
            dataType[1], choicesPerQuestion, songs
        ):
            for i in range(choicesPerQuestion):
                rand = random.randint(0, len(songs) - 1)
                while songs[rand] in options:  # ensure no duplicates
                    rand = random.randint(0, len(songs) - 1)
                options.append(songs[rand])
                del songs[rand]
            correct = random.randint(1, choicesPerQuestion)
            p = options[correct - 1]
            for x in range(len(dataType[1].split(";"))):
                if (dataType[1].split(";"))[x] == "0":
                    p = p[0]
                else:
                    p = p[(dataType[1].split(";"))[x]]
            print(p)
            for i in range(choicesPerQuestion):
                p = options[i]
                for x in range(len(dataType[0].split(";"))):
                    if (dataType[0].split(";"))[x] == "0":
                        p = p[0]
                    else:
                        p = p[(dataType[0].split(";"))[x]]
                print(f"{i+1}.) {p}")
            while True:
                try:
                    if int(input("Enter correct choice: ")) == correct:
                        print("Correct!\n\n\n")
                        score += 1
                    else:
                        print(f"Wrong! Answer was {correct}\n\n\n")
                        incorrect += 1
                    break
                except:
                    print("Please only enter a number!")
        else:
            break

    return f"Score: {score} (incorrect: {incorrect})"


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
        "NA RIGHT NOW",
    ]


def gameSetup():
    dataTypes, dataRoutes = getTypesRoutes()
    x = "Please enter the number for the question data type you want:\n"
    for i in range(len(dataTypes)):
        x += f"{i+1}.) {dataTypes[i]}\n"
    x += "Response: "
    question = int(input(x))
    os.system("clear")
    x = f"Question type: {dataTypes[question-1]}\n\nPlease enter the number for the answer data type you want:\n"
    for i in range(len(dataTypes)):
        x += f"{i+1}.) {dataTypes[i]}\n"
    x += "Response: "
    answers = int(input(x))
    os.system("clear")
    answerCount = int(
        input(
            f"Question type: {dataTypes[question-1]}\nAnswer type: {dataTypes[answers-1]}\n\nHow many possible answer choices do you want (recomended 4 or 5):\n"
        )
    )
    os.system("clear")
    playlisturl = input("Please enter your spotify playlist url: ")
    os.system("clear")
    return game(
        f"{dataRoutes[answers-1]}!{dataRoutes[question-1]}",
        playlisturl,
        answerCount,
    )
