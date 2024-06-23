import json, load, random, os, bugPrevention


def nameFromCover(albumURL, choicesPerQuestion, showAuthor=True):
    score = 0
    incorrect = 0
    songs = load.getPlaylist(albumURL)

    while choicesPerQuestion < len(songs):
        os.system("clear")
        options = []
        if bugPrevention.ensureEnoughDifferentItems(
            "track;name", choicesPerQuestion, songs
        ):
            for i in range(choicesPerQuestion):
                rand = random.randint(0, len(songs) - 1)
                while songs[rand] in options:  # ensure no duplicates
                    rand = random.randint(0, len(songs) - 1)
                options.append(songs[rand])
                del songs[rand]
            correct = random.randint(1, choicesPerQuestion)
            print(options[correct]["track"]["album"]["images"][0]["url"])
            for i in range(choicesPerQuestion):
                if not showAuthor:
                    print(f"{i+1}.) {options[i]['track']['name']}")
                else:
                    print(
                        f"{i+1}.) {options[i]['track']['name']} by {options[i]['track']['artists'][0]['name']}"
                    )
            while True:
                try:
                    if int(input("Enter correct choice: ")) - 1 == correct:
                        print("Correct!")
                        score += 1
                    else:
                        print("Wrong!")
                        incorrect += 1
                    break
                except:
                    print("Please only enter a number!")
        else:
            break

    return f"Score: {score} (incorrect: {incorrect})"


print(
    nameFromCover(
        "https://open.spotify.com/playlist/7hkUzF20c6rHYyRVs6oJIS?si=35fd6a36e0a94367&pt=9465d47a3575a5b79282c46204ef1917",
        5,
    )
)
