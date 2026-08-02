# Topic 4, Day 3 Homework -- Magic Methods & Composition

# Exercise 1: Book/EBook using __str__ instead of a custom display method
class Book:
    def __init__(self, title, author, is_borrowed=False):
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        self.borrow_count = 0

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} by {self.author} [{status}]"


class EBook(Book):
    def __init__(self, title, author, file_size_mb):
        super().__init__(title, author)
        self.file_size_mb = file_size_mb

    def __str__(self):
        return f"{self.title} by {self.author} [{self.file_size_mb}MB]"


print(Book("Deep Work", "Cal Newport"))
print(EBook("Atomic Habits", "James Clear", 10))


# Exercise 2: Playlist HAS-A list of Song objects (composition) + __len__ magic method
class Song:
    def __init__(self, title, duration_seconds):
        self.title = title
        self.duration_seconds = duration_seconds


class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, title, duration_seconds):
        self.songs.append(Song(title, duration_seconds))

    def total_duration(self):
        total = 0
        for song in self.songs:
            total += song.duration_seconds
        return total

    def __len__(self):
        return len(self.songs)


playlist = Playlist()
playlist.add_song("Hum Tum", 235)
playlist.add_song("Yaariyan", 188)
playlist.add_song("Mil Jao", 271)
print(len(playlist))            # 3
print(playlist.total_duration())  # 694


# DSA micro-drill: is_anagram using increment/decrement on a shared dict
def is_anagram(word1, word2):
    if len(word1) != len(word2):
        return False
    counts = {}
    for i in range(len(word1)):
        counts[word1[i]] = counts.get(word1[i], 0) + 1
        counts[word2[i]] = counts.get(word2[i], 0) - 1
    for value in counts.values():
        if value != 0:
            return False
    return True


print(is_anagram("acm", "cat"))   # False
print(is_anagram("cat", "act"))    # True
print(is_anagram("aa", "bb"))      # False -- edge case: same letter counts, different letters
