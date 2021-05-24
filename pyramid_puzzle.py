"""This is the Tower of Hanoi puzzle (also known as pyramid puzzle). Here's
the main program script to be run.
"""
import pygame
from pygame.locals import *

from disk import Disk
from tower import Tower
from counter import Counter
from button import Button
from static_text import StaticText
from rounded_rect import RoundedRect

FPS = 60
WIN_WIDTH = 800
WIN_HEIGHT = 600
WIN_CAPTION = 'The Tower of Hanoi: a mathematical puzzle'
MIN_SIZE = 20 # Base size value to draw graphical shapes (pixels)
SCREEN_FADE_STEP = 10 # Screen transparency change after each frame

DISK_COLORS = [
    (244, 67, 54),
    (156, 39, 176),
    (63, 81, 181),
    (3, 169, 244),
    (0, 150, 136),
    (139, 195, 74),
    (255, 235, 59),
    (255, 152, 0),
]

DISKS_COUNT = len(DISK_COLORS)
TOWERS_COUNT = 3

BUTTON_HELP = 'Help F1'
BUTTON_SOLVE = 'Solve F2'
BUTTON_RESET = 'Reset F3'
BUTTON_QUIT = 'Quit F4'
BUTTON_CAPTIONS = [BUTTON_HELP, BUTTON_SOLVE, BUTTON_RESET, BUTTON_QUIT]
BUTTONS_COUNT = len(BUTTON_CAPTIONS)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
INDIGO = (26, 35, 126)
ORANGE = (230, 81, 0)
BROWN = (121, 85, 72)
BGCOLOR = WHITE
ROD_COLOR = BROWN

FONT_NAME = 'freesansbold.ttf'
BASIC_FONT_SIZE = 24

HELP_LINES = [
    'THE TOWER OF HANOI',
    'a mathematical game',
    '',
    'The objective is to move the entire stack to the last rod.',
    'Only one disk may be moved at a time.',
    'No disk may be placed on top of a disk that is smaller than it.',
    '',
    'Select source or target tower by mouse click.',
    'Also you can use numeric keyboard buttons for quick selecting.',
    'F1 - help screen | F2 - automatic solution | F3 - reset puzzle',
    'F4 - quit the game | F11 - toggle fullscreen | ESC - cancel selection',
    '',
    'Press any key to continue...',
]

HELP_TEXT_COLOR = INDIGO

BUTTON_COLOR = INDIGO
BUTTON_TEXT_COLOR = WHITE
BUTTON_FONT_SIZE = 18

VICTORY_TEXT = 'PUZZLE SOLVED!'
VICTORY_TEXT_COLOR = ORANGE
VICTORY_FONT_SIZE = 32

COUNTER_PREFIX_TEXT = 'Steps: '
COUNTER_TEXT_COLOR = INDIGO

class PyramidPuzzle():
    """Represents the game itself. Create a class instance and execute run()
    method to start the puzzle.
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption(WIN_CAPTION)
        self.cursor = None
        self.fps_clock = pygame.time.Clock()
        self.basic_font = pygame.font.Font(FONT_NAME, BASIC_FONT_SIZE)
        self.button_font = pygame.font.Font(FONT_NAME, BUTTON_FONT_SIZE)

        self.victory_message = StaticText(
            VICTORY_TEXT,
            VICTORY_TEXT_COLOR,
            pygame.font.Font(FONT_NAME, VICTORY_FONT_SIZE))
        self.victory_message.rect.centerx = WIN_WIDTH // 2
        self.victory_message.rect.top = 3 * MIN_SIZE

        self.steps_counter = Counter((MIN_SIZE, MIN_SIZE), COUNTER_PREFIX_TEXT,
                                     COUNTER_TEXT_COLOR, self.basic_font)

        self._reset()

    def run(self):
        """The only public method. Just runs the game. It starts infinite
        loop where system events are being processed and game objects
        are being drawn.
        """
        self._screen_fade(reverse=True)

        while not pygame.event.get(QUIT):
            for event in pygame.event.get():
                if not self._process_event(event):
                    # Program termination
                    return

            # The disk has finished moving to the target tower
            if (self.selected_disk and self.target_tower
                    and not self.selected_disk.is_moving()):
                self.target_tower.put(self.selected_disk)
                self.selected_disk = None
                self.target_tower = None
                self.steps_counter.increment()

            # Handling solution autoplay: getting the next move right after
            # the animation has finished
            if not self.selected_disk and self.solution_moves:
                move = self.solution_moves.pop(0)
                self._tower_select(move['source_tower'])
                self._tower_select(move['target_tower'])

            self._update()
            self._draw()

        self._screen_fade()

    # Resets the game to its initial state and recreates all dynamic objects
    def _reset(self):
        self._set_cursor(SYSTEM_CURSOR_ARROW)

        self.disks = [Disk(MIN_SIZE * (i + 3), 2 * MIN_SIZE, DISK_COLORS[i])
                      for i in range(DISKS_COUNT - 1, -1, -1)]

        self.towers = [Tower(MIN_SIZE, DISKS_COUNT * self.disks[0].rect.height
                             + MIN_SIZE, ROD_COLOR)
                       for i in range(TOWERS_COUNT)]

        for i in range(TOWERS_COUNT):
            self.towers[i].rect.centerx = int(WIN_WIDTH / TOWERS_COUNT
                                              * (i + 0.5))
            self.towers[i].rect.bottom = WIN_HEIGHT - 5 * MIN_SIZE

        for disk in self.disks:
            self.towers[0].put(disk)

        self.bar = RoundedRect(WIN_WIDTH - 2 * MIN_SIZE, 2 * MIN_SIZE,
                               ROD_COLOR)
        self.bar.rect.centerx = int(WIN_WIDTH / 2)
        self.bar.rect.top = self.towers[0].rect.bottom

        self.buttons = [Button(MIN_SIZE * 6, 2 * MIN_SIZE, BUTTON_COLOR,
                               BUTTON_CAPTIONS[i], BUTTON_TEXT_COLOR,
                               self.button_font)
                        for i in range(BUTTONS_COUNT)]

        for i in range(BUTTONS_COUNT):
            self.buttons[i].rect.centerx = int(WIN_WIDTH / BUTTONS_COUNT
                                               * (i + 0.5))
            self.buttons[i].rect.bottom = WIN_HEIGHT - (MIN_SIZE // 2)

        self.selected_disk = None
        self.target_tower = None
        self.solution_moves = []
        self.steps_counter.reset()

    # Sets new system cursor shape if the shape has changed
    def _set_cursor(self, cursor: int):
        if self.cursor != cursor:
            self.cursor = cursor
            pygame.mouse.set_cursor(self.cursor)

    # Updates all internal objects having update() method
    def _update(self):
        for disk in self.disks:
            disk.update()
        for button in self.buttons:
            button.update()

    # Draws all visual objects, i.e. the entire game screen
    def _draw(self, update=True):
        ds = pygame.display.get_surface()

        ds.fill(BGCOLOR)
        self.bar.draw()
        for tower in self.towers:
            tower.draw()
        for disk in self.disks:
            disk.draw()
        for button in self.buttons:
            button.draw()
        self.steps_counter.draw()

        if self._is_solved():
            self.victory_message.draw()

        if update:
            pygame.display.update()
            self.fps_clock.tick(FPS)

    # Returns True if the puzzle is solved
    def _is_solved(self) -> bool:
        return len(self.towers[-1].disks) == DISKS_COUNT

    # Gradually fades out the screen (or vice-versa if reverse is True)
    def _screen_fade(self, reverse=False, redraw=True):
        if redraw:
            self._draw(update=False)
        ds = pygame.display.get_surface()
        screenshot = pygame.Surface(ds.get_size(), 0, ds)
        screenshot.blit(ds, (0, 0))

        alpha_values = list(range(255, -1, -SCREEN_FADE_STEP))
        if reverse:
            alpha_values.reverse()
        for alpha in alpha_values:
            screenshot.set_alpha(alpha)
            ds.fill(BGCOLOR)
            ds.blit(screenshot, (0, 0))
            pygame.display.update()
            self.fps_clock.tick(FPS)

    # Processes single system event in queue and updates game state
    def _process_event(self, event: pygame.event.Event) -> bool:
        if event.type == MOUSEMOTION:
            # Disk blinking handling
            if not self.selected_disk:
                top_disk = self._top_disk_at_pos(event.pos)
                if top_disk:
                    if not top_disk.is_blinking():
                        top_disk.start_blinking()
                else:
                    for disk in self.disks:
                        disk.stop_blinking()


            new_cursor = SYSTEM_CURSOR_ARROW

            # For towers: handle cursor shape changing when moving over
            for tower in self.towers:
                if tower.contains_point(event.pos):
                    if self.selected_disk:
                        if (tower.peep() == self.selected_disk
                                or tower.can_put(self.selected_disk)):
                            new_cursor = SYSTEM_CURSOR_HAND
                        else:
                            new_cursor = SYSTEM_CURSOR_NO
                    elif tower.peep() != None:
                        new_cursor = SYSTEM_CURSOR_HAND

                    break

            # For buttons: handle cursor shape changing and blinking
            for button in self.buttons:
                if button.contains_point(event.pos):
                    new_cursor = SYSTEM_CURSOR_HAND
                    if not button.is_blinking():
                        button.start_blinking()
                else:
                    button.stop_blinking()

            self._set_cursor(new_cursor)

        elif event.type == MOUSEBUTTONUP:
            self._tower_select(self._tower_at_pos(event.pos))

            for button in self.buttons:
                if button.contains_point(event.pos):
                    if button.caption == BUTTON_HELP:
                        self._event_help()
                    elif button.caption == BUTTON_SOLVE:
                        self._event_solve()
                    elif button.caption == BUTTON_RESET:
                        self._event_reset()
                    elif button.caption == BUTTON_QUIT:
                        self._screen_fade()
                        return False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Deselecting previously selected tower
                if not self.target_tower:
                    self._tower_deselect()
                # Pressing ESC also cancels solution autoplay
                self.solution_moves = []

            elif event.key == K_F1:
                self._event_help()

            elif event.key == K_F2:
                self._event_solve()

            elif event.key == K_F3:
                self._event_reset()

            elif event.key == K_F4:
                self._screen_fade()
                return False
            elif event.key == K_F11:
                pygame.display.toggle_fullscreen()

            # Selecting tower by its number
            elif event.unicode.isnumeric():
                index = int(event.unicode) - 1
                if index >= 0 and index <= TOWERS_COUNT - 1:
                    self._tower_select(self.towers[index])

        return True

    # Returns Disk under the screen point (or None)
    def _top_disk_at_pos(self, point: tuple) -> Disk:
        return self._top_tower_disk(self._tower_at_pos(point))

    # Returns Tower under the screen point (or None)
    def _tower_at_pos(self, point: tuple) -> Tower:
        for tower in self.towers:
            if tower.contains_point(point):
                return tower
        return None

    # Returns the topmost tower's disk (may be None)
    # Note: tower parameter may also be None
    def _top_tower_disk(self, tower: Tower) -> Disk:
        if tower:
            return tower.peep()
        return None

    # Performs specified tower selection
    # Note: it's okay to pass None as tower parameter
    def _tower_select(self, tower: Tower):
        top_disk = self._top_tower_disk(tower)

        # Deselecting previously selected disk
        if (self.selected_disk == top_disk
                and not self.target_tower):
            self._tower_deselect()

        # Selecting disk for moving
        elif not self.selected_disk:
            if top_disk:
                if not top_disk.is_blinking():
                    top_disk.start_blinking()
                self.selected_disk = top_disk

        # Selecting tower for disk to move to, starting animation
        elif not self.target_tower:
            if tower and tower.can_put(self.selected_disk):
                self.target_tower = tower
                self._start_disk_moving()

    # Performs any tower deselection
    def _tower_deselect(self):
        if not self.selected_disk:
            return

        # Don't stop blinking if mouse is still over the tower
        if not self.selected_disk.contains_point(
                pygame.mouse.get_pos()):
            self.selected_disk.stop_blinking()
        self.selected_disk = None

    # Prepares and starts disk moving animation
    def _start_disk_moving(self):
        for source_tower in self.towers:
            if source_tower.peep() == self.selected_disk:
                source_tower.get()
                break

        self.selected_disk.stop_blinking()
        self.selected_disk.move(
            start_point=self.selected_disk.rect.midbottom,
            land_point=self.target_tower.get_peak_point(),
            fly_point=source_tower.rect.midtop)

    # System event handler: show help screen
    def _event_help(self):
        self._screen_fade()
        self._draw_help()
        self._screen_fade(reverse=True, redraw=False)

        pygame.event.get([KEYDOWN, MOUSEBUTTONUP]) # Clear the events queue
        while not pygame.event.get([KEYDOWN, MOUSEBUTTONUP]):
            self._draw_help()
            pygame.display.update()
            self.fps_clock.tick(FPS)
            # Should check for program termination
            for quit_event in pygame.event.get([QUIT]):
                pygame.event.post(quit_event)
                self._screen_fade(redraw=False)
                self._screen_fade(reverse=True)
                return

        self._screen_fade(redraw=False)
        self._screen_fade(reverse=True)

    # Draw help screen
    def _draw_help(self):
        ds = pygame.display.get_surface()
        ds.fill(BGCOLOR)
        for i in range(len(HELP_LINES)):
            # For addition vertical space
            if not HELP_LINES[i]:
                continue

            text_surf = self.basic_font.render(HELP_LINES[i], True,
                                               HELP_TEXT_COLOR)
            text_rect = text_surf.get_rect()
            text_rect.top = 2 * MIN_SIZE * (i + 1)
            text_rect.centerx = WIN_WIDTH // 2
            ds.blit(text_surf, text_rect)

    # System event handler: solve puzzle
    def _event_solve(self):
        self._event_reset()
        self._generate_solution(
            DISKS_COUNT,
            source=self.towers[0],
            target=self.towers[2],
            buf=self.towers[1])

    # "Classical" recursive algorithm for solving the Tower of Hanoi puzzle
    # Note: solution_moves list must be empty before this method call
    def _generate_solution(self, n: int, source: Tower, target: Tower,
                           buf: Tower) -> list:
        if n != 0:
            self._generate_solution(n - 1, source, buf, target)

            self.solution_moves.append({
                'source_tower': source,
                'target_tower': target
            })

            self._generate_solution(n - 1, buf, target, source)

    # System event handler: reset game
    def _event_reset(self):
        self._screen_fade()
        self._reset()
        self._screen_fade(reverse=True)


if __name__ == '__main__':
    PyramidPuzzle().run()
