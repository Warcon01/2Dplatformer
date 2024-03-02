from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Super Pirate World')
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_maps = {
            0: load_pygame(join('Super Pirate World', 'data', 'levels', 'omni.tmx')),
            1: load_pygame(join('Super Pirate World', 'data', 'levels', '1.tmx')),
            2: load_pygame(join('Super Pirate World', 'data', 'levels', '2.tmx')),
            3: load_pygame(join('Super Pirate World', 'data', 'levels', '3.tmx')),
            4: load_pygame(join('Super Pirate World', 'data', 'levels', '4.tmx')),
            5: load_pygame(join('Super Pirate World', 'data', 'levels', '5.tmx')),
        }
        self.tmx_overworld = load_pygame(join('Super Pirate World', 'data', 'overworld', 'overworld.tmx'))
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files,
                                   self.data, self.switch_stage)
        self.bg_music.play(-1)

    def switch_stage(self, target, unlock=0):
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files,
                                       self.data, self.switch_stage)

        else:  # overworld
            if unlock > 0:
                self.data.unlocked_level = 6
            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('Super Pirate World', 'graphics', 'level', 'flag'),
            'saw': import_folder('Super Pirate World', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('Super Pirate World', 'graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('Super Pirate World', 'graphics', 'level', 'palms'),
            'candle': import_folder('Super Pirate World', 'graphics', 'level', 'candle'),
            'window': import_folder('Super Pirate World', 'graphics', 'level', 'window'),
            'big_chain': import_folder('Super Pirate World', 'graphics', 'level', 'big_chains'),
            'small_chain': import_folder('Super Pirate World', 'graphics', 'level', 'small_chains'),
            'candle_light': import_folder('Super Pirate World', 'graphics', 'level', 'candle light'),
            'player': import_sub_folders('Super Pirate World', 'graphics', 'player'),
            'saw': import_folder('Super Pirate World', 'graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('Super Pirate World', 'graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter': import_folder('Super Pirate World', 'graphics', 'level', 'helicopter'),
            'boat': import_folder('Super Pirate World', 'graphics', 'objects', 'boat'),
            'spike': import_image('Super Pirate World', 'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('Super Pirate World', 'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth': import_folder('Super Pirate World', 'graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('Super Pirate World', 'graphics', 'enemies', 'shell'),
            'pearl': import_image('Super Pirate World', 'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('Super Pirate World', 'graphics', 'items'),
            'particle': import_folder('Super Pirate World', 'graphics', 'effects', 'particle'),
            'water_top': import_folder('Super Pirate World', 'graphics', 'level', 'water', 'top'),
            'water_body': import_image('Super Pirate World', 'graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('Super Pirate World', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('Super Pirate World', 'graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('Super Pirate World', 'graphics', 'level', 'clouds', 'large_cloud'),
        }
        self.font = pygame.font.Font(join('Super Pirate World', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_folder('Super Pirate World', 'graphics', 'ui', 'heart'),
            'coin': import_image('..', 'graphics', 'ui', 'coin')
        }
        self.overworld_frames = {
            'palms': import_folder('Super Pirate World', 'graphics', 'overworld', 'palm'),
            'water': import_folder('Super Pirate World', 'graphics', 'overworld', 'water'),
            'path': import_folder_dict('Super Pirate World', 'graphics', 'overworld', 'path'),
            'icon': import_sub_folders('Super Pirate World', 'graphics', 'overworld', 'icon'),
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join('Super Pirate World', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('Super Pirate World', 'audio', 'attack.wav')),
            'jump': pygame.mixer.Sound(join('Super Pirate World', 'audio', 'jump.wav')),
            'damage': pygame.mixer.Sound(join('Super Pirate World', 'audio', 'damage.wav')),
            'pearl': pygame.mixer.Sound(join('Super Pirate World', 'audio', 'pearl.wav')),
        }
        self.bg_music = pygame.mixer.Sound(join('Super Pirate World', 'audio', 'starlight_city.mp3'))
        self.bg_music.set_volume(0.5)

    def check_game_over(self):
        if self.data.health <= 0:
            pygame.quit()
            sys.exit()

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.check_game_over()
            self.current_stage.run(dt)
            self.ui.update(dt)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()