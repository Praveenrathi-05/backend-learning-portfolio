# Topic 3, Day 3 Homework -- Object-Oriented Programming basics

# Exercise 1: Rectangle -- methods that RETURN computed values
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


rectangle_1 = Rectangle(10, 20)
rectangle_2 = Rectangle(5, 3)

print(rectangle_1.area())
print(rectangle_2.area())
print(rectangle_1.perimeter())
print(rectangle_2.perimeter())


# Exercise 2: Playlist -- an attribute that's itself a mutable list
class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def show_songs(self):
        for song in self.songs:
            print(song)


praveen_playlist = Playlist()
praveen_playlist.add_song("Closer")
praveen_playlist.add_song("Baby")
praveen_playlist.add_song("Cheap Thrills")
praveen_playlist.show_songs()


# DSA micro-drill: Stopwatch -- mutate-in-place method pattern
class Stopwatch:
    def __init__(self):
        self.total_seconds = 0

    def add_time(self, seconds):
        self.total_seconds += seconds


stopwatch_1 = Stopwatch()
stopwatch_1.add_time(50)
stopwatch_1.add_time(30)
stopwatch_1.add_time(86)
print(stopwatch_1.total_seconds)
