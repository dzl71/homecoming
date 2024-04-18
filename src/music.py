import pygame as pg


class Music:
    def __init__(self) -> None:
        self.music = "resources/sounds/war-song.mp3"
        self.playing_music: bool = False
        pg.mixer.init()

    def play_music(self) -> None:
        if not self.playing_music:
            self.playing_music = True
            pg.mixer.music.load(self.music)
            pg.mixer.music.play(-1, 0.0)

    def stop_playing_music(self) -> None:
        self.playing_music = False
        pg.mixer.music.pause()

    def rewind_music(self) -> None:
        pg.mixer.music.rewind()
