import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import json

with open("loginData.json") as f:
    loginData = json.loads(f.read())

auth_manager = spotipy.oauth2.SpotifyOAuth(
    scope="user-library-read",
    username=loginData["username"],
    client_id=loginData["client_id"],
    client_secret=loginData["client_secret"],
    redirect_uri=loginData["redirect_uri"],
    open_browser=False,
)
sp = spotipy.Spotify(auth_manager=auth_manager)


def getTrack(url):
    track_info = sp.track(url)
    del track_info["album"]["available_markets"]
    del track_info["available_markets"]
    del track_info["disc_number"]
    del track_info["is_local"]
    del track_info["track_number"]
    del track_info["type"]
    del track_info["href"]

    return track_info
    """
    example track_info data

    {
        "album": {
            "album_type": "album",
            "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/4IJczjB0fJ04gs4uvP0Fli"
                    },
                    "href": "https://api.spotify.com/v1/artists/4IJczjB0fJ04gs4uvP0Fli",
                    "id": "4IJczjB0fJ04gs4uvP0Fli",
                    "name": "Gym Class Heroes",
                    "type": "artist",
                    "uri": "spotify:artist:4IJczjB0fJ04gs4uvP0Fli",
                }
            ],
            "external_urls": {
                "spotify": "https://open.spotify.com/album/4Ug3M4a8wAEebndVIF65fX"
            },
            "href": "https://api.spotify.com/v1/albums/4Ug3M4a8wAEebndVIF65fX",
            "id": "4Ug3M4a8wAEebndVIF65fX",
            "images": [
                {
                    "url": "https://i.scdn.co/image/ab67616d0000b273f335d8387c3658831112f914",
                    "width": 640,
                    "height": 640,
                },
                {
                    "url": "https://i.scdn.co/image/ab67616d00001e02f335d8387c3658831112f914",
                    "width": 300,
                    "height": 300,
                },
                {
                    "url": "https://i.scdn.co/image/ab67616d00004851f335d8387c3658831112f914",
                    "width": 64,
                    "height": 64,
                },
            ],
            "name": "The Papercut Chronicles",
            "release_date": "2005-02-22",
            "release_date_precision": "day",
            "total_tracks": 18,
            "type": "album",
            "uri": "spotify:album:4Ug3M4a8wAEebndVIF65fX",
        },
        "artists": [
            {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/4IJczjB0fJ04gs4uvP0Fli"
                },
                "href": "https://api.spotify.com/v1/artists/4IJczjB0fJ04gs4uvP0Fli",
                "id": "4IJczjB0fJ04gs4uvP0Fli",
                "name": "Gym Class Heroes",
                "type": "artist",
                "uri": "spotify:artist:4IJczjB0fJ04gs4uvP0Fli",
            }
        ],
        "duration_ms": 243773,
        "explicit": false,
        "external_ids": {"isrc": "US56V0407211"},
        "external_urls": {
            "spotify": "https://open.spotify.com/track/2Lhdl74nwwVGOE2Gv35QuK"
        },
        "href": "https://api.spotify.com/v1/tracks/2Lhdl74nwwVGOE2Gv35QuK",
        "id": "2Lhdl74nwwVGOE2Gv35QuK",
        "name": "Cupid's Chokehold / Breakfast in America",
        "popularity": 73,
        "preview_url": "https://p.scdn.co/mp3-preview/512899019cfc95a1faf8ddeaaa6a584c81200755?cid=ebc973fe3c0c42c0bc6ba6f02cebb649",
        "uri": "spotify:track:2Lhdl74nwwVGOE2Gv35QuK",
    }
    """


def getPlaylist(url):
    results = sp.playlist_tracks(url)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    for i in range(len(tracks)):
        del tracks[i]["track"]["available_markets"]
        del tracks[i]["track"]["album"]["available_markets"]

    return tracks
    """
    example playlist data

    [
    {
        "added_at": "2023-09-02T17:35:09Z",
        "added_by": {
            "external_urls": {
                "spotify": "https://open.spotify.com/user/9vio1zoexm7vv74mo3hj5wixa"
            },
            "href": "https://api.spotify.com/v1/users/9vio1zoexm7vv74mo3hj5wixa",
            "id": "9vio1zoexm7vv74mo3hj5wixa",
            "type": "user",
            "uri": "spotify:user:9vio1zoexm7vv74mo3hj5wixa"
        },
        "is_local": false,
        "primary_color": null,
        "track": {
            "preview_url": "https://p.scdn.co/mp3-preview/6b65a65ca23c52900dc52c8ea2437e3d79bd6059?cid=ebc973fe3c0c42c0bc6ba6f02cebb649",
            "explicit": true,
            "type": "track",
            "episode": false,
            "track": true,
            "album": {
                "type": "album",
                "album_type": "album",
                "href": "https://api.spotify.com/v1/albums/7rbdgYKz1DI4gXMWveqS5T",
                "id": "7rbdgYKz1DI4gXMWveqS5T",
                "images": [
                {
                    "height": 640,
                    "url": "https://i.scdn.co/image/ab67616d0000b2730f0e7900a102aaa70ed30d3e",
                    "width": 640
                },
                {
                    "height": 300,
                    "url": "https://i.scdn.co/image/ab67616d00001e020f0e7900a102aaa70ed30d3e",
                    "width": 300
                },
                {
                    "height": 64,
                    "url": "https://i.scdn.co/image/ab67616d000048510f0e7900a102aaa70ed30d3e",
                    "width": 64
                }
                ],
                "name": "OK ORCHESTRA",
                "release_date": "2021-03-26",
                "release_date_precision": "day",
                "uri": "spotify:album:7rbdgYKz1DI4gXMWveqS5T",
                "artists": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/6s22t5Y3prQHyaHWUN1R1C"
                    },
                    "href": "https://api.spotify.com/v1/artists/6s22t5Y3prQHyaHWUN1R1C",
                    "id": "6s22t5Y3prQHyaHWUN1R1C",
                    "name": "AJR",
                    "type": "artist",
                    "uri": "spotify:artist:6s22t5Y3prQHyaHWUN1R1C"
                }
                ],
                "external_urls": {
                "spotify": "https://open.spotify.com/album/7rbdgYKz1DI4gXMWveqS5T"
                },
                "total_tracks": 13
            },
            "artists": [
                {
                "external_urls": {
                    "spotify": "https://open.spotify.com/artist/6s22t5Y3prQHyaHWUN1R1C"
                },
                "href": "https://api.spotify.com/v1/artists/6s22t5Y3prQHyaHWUN1R1C",
                "id": "6s22t5Y3prQHyaHWUN1R1C",
                "name": "AJR",
                "type": "artist",
                "uri": "spotify:artist:6s22t5Y3prQHyaHWUN1R1C"
                }
            ],
            "disc_number": 1,
            "track_number": 11,
            "duration_ms": 180746,
            "external_ids": {
                "isrc": "QMRSZ2003324"
            },
            "external_urls": {
                "spotify": "https://open.spotify.com/track/68EkhVWIeULhHxcbi1QhzK"
            },
            "href": "https://api.spotify.com/v1/tracks/68EkhVWIeULhHxcbi1QhzK",
            "id": "68EkhVWIeULhHxcbi1QhzK",
            "name": "World's Smallest Violin",
            "popularity": 64,
            "uri": "spotify:track:68EkhVWIeULhHxcbi1QhzK",
            "is_local": false
        },
        "video_thumbnail": {
            "url": null
        }
    },
    ]
    """
