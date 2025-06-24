# Minimal Spotify MVP CLI

from dataclasses import dataclass, field
from typing import List, Dict

# Example song data
SONGS = [
    {"id": 1, "title": "Song A", "artist": "Artist 1", "album": "Album X"},
    {"id": 2, "title": "Song B", "artist": "Artist 2", "album": "Album Y"},
    {"id": 3, "title": "Song C", "artist": "Artist 1", "album": "Album Z"},
]

@dataclass
class Playlist:
    name: str
    song_ids: List[int] = field(default_factory=list)

@dataclass
class Account:
    username: str
    playlists: Dict[str, Playlist] = field(default_factory=dict)

class SpotifyMVP:
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.current_user: Account | None = None

    def login(self, username: str):
        if username not in self.accounts:
            self.accounts[username] = Account(username)
        self.current_user = self.accounts[username]
        print(f"Logged in as {username}")

    def search(self, query: str):
        results = [song for song in SONGS if query.lower() in song["title"].lower()]
        for song in results:
            print(f"{song['id']}: {song['title']} by {song['artist']} ({song['album']})")
        if not results:
            print("No matches found.")

    def play(self, song_id: int):
        song = next((s for s in SONGS if s["id"] == song_id), None)
        if song:
            print(f"Playing {song['title']} by {song['artist']}")
        else:
            print("Song not found.")

    def create_playlist(self, name: str):
        if not self.current_user:
            print("Please log in first.")
            return
        if name in self.current_user.playlists:
            print("Playlist already exists.")
        else:
            self.current_user.playlists[name] = Playlist(name)
            print(f"Created playlist '{name}'")

    def add_to_playlist(self, name: str, song_id: int):
        if not self.current_user:
            print("Please log in first.")
            return
        playlist = self.current_user.playlists.get(name)
        if playlist:
            playlist.song_ids.append(song_id)
            print(f"Added song {song_id} to '{name}'")
        else:
            print("Playlist not found.")

    def show_playlists(self):
        if not self.current_user:
            print("Please log in first.")
            return
        for playlist in self.current_user.playlists.values():
            print(f"Playlist: {playlist.name}")
            for sid in playlist.song_ids:
                song = next((s for s in SONGS if s["id"] == sid), None)
                if song:
                    print(f"  - {song['title']} by {song['artist']}")
            if not playlist.song_ids:
                print("  (empty)")


def main():
    app = SpotifyMVP()
    while True:
        command = input("command (help for options): ").strip()
        if command == "exit":
            break
        elif command.startswith("login "):
            _, username = command.split(maxsplit=1)
            app.login(username)
        elif command.startswith("search "):
            _, query = command.split(maxsplit=1)
            app.search(query)
        elif command.startswith("play "):
            _, sid = command.split(maxsplit=1)
            app.play(int(sid))
        elif command.startswith("playlist create "):
            _, _, name = command.split(maxsplit=2)
            app.create_playlist(name)
        elif command.startswith("playlist add "):
            _, _, name, sid = command.split(maxsplit=3)
            app.add_to_playlist(name, int(sid))
        elif command == "playlists":
            app.show_playlists()
        elif command == "help":
            print("commands:\n  login <user>\n  search <query>\n  play <song_id>\n  playlist create <name>\n  playlist add <name> <song_id>\n  playlists\n  exit")
        else:
            print("Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()
