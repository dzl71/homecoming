import pygame as pg


class Music:
    def __init__(self) -> None:
        # self.steps = "resources/sounds/metal_steps_01.wav"
        # self.playing_steps = False
        self.music = "resources/sounds/war-song.mp3"
        self.playing_music = False
        self.victory = "resources/sounds/Victory.wav"
        self.playing_victory = False
        pg.mixer.init()

    def play_music(self) -> None:
        if not self.playing_music:
            self.playing_music = True
            pg.mixer.music.load(self.music)
            pg.mixer.music.play(-1, 0.0)

    # def play_steps(self) -> None:
    #     if not self.playing_steps:
    #         self.playing_steps = True
    #         pg.mixer.music.load(self.playing_steps)
    #         pg.mixer.music.play(-1, 0.0)

    def play_vicory(self) -> None:
        if not self.playing_victory:
            self.playing_victory = True
            pg.mixer.music.load(self.victory)
            pg.mixer.music.play(-1, 0.0)

    # def stop_playing_steps(self) -> None:
    #     self.playing_steps = False
    #     pg.mixer.music.stop()

    def stop_playing_music(self) -> None:
        self.playing_music = False
        pg.mixer.music.pause()

    def stop_playing_victory(self) -> None:
        self.playing_victory = False
        pg.mixer.music.pause()

    def rewind_music(self) -> None:
        pg.mixer.music.rewind()
