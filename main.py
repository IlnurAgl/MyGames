from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from random import choice, randint
# imports

# Window color
Window.clearcolor = (1, 1, 1, 1)

# kv file import
Builder.load_file('Games.kv')

# Number of players on game
players = 0


# Main class for TicTacToeWidget
class TicTacWidget(BoxLayout):
    # Main init for other class
    def __init__(self, **kw):
        super(TicTacWidget, self).__init__(**kw)

        # edit box orientation
        self.orientation = 'vertical'

        # padding
        self.padding = self.width * 0.1

        # main choises
        self.choice = ['X', 'O']

        # step
        self.switch = 0

        # button back to the choose games
        self.backBtn = Button(
            text='Back',
            size_hint=[1, 0.1],
            font_size='30sp',
            on_release=self.back,
        )

        self.add_widget(self.backBtn)

        # add field
        grid = GridLayout(cols=3)

        self.spacing = self.width * 0.05

        # adding buttons to field
        self.button = [0 for _ in range(9)]
        for index in range(9):
            self.button[index] = Button(
                on_release=self.tic_tac_toe,
                font_size='60sp',
                disabled=False,
            )
            grid.add_widget(self.button[index])

        self.add_widget(grid)

        # add reset button
        self.resetBtn = Button(
            text="Restart",
            font_size='20sp',
            size_hint=[1, .1],
            on_release=self.restart
        )

        self.add_widget(self.resetBtn)

    # function back for the button
    def back(self, instance):
        global screen_manager
        screen_manager.transition = SlideTransition(direction='right')
        screen_manager.current = 'GamesScreen'

    # function restart game for the button
    def restart(self, arg):
        self.switch = 0
        self.resetBtn.text = 'Restart'
        for index in range(9):
            self.button[index].color = [1, 1, 1, 1]
            self.button[index].text = ""
            self.button[index].disabled = False


# class for TicTacToe game for the one person
class TicTacWidgetOne(TicTacWidget):
    # if user press button
    def tic_tac_toe(self, arg):
        if arg.text:
            return
        arg.text = self.choice[self.switch]

        self.fieldGenerate()

        if self.checkWin():
            self.resetBtn.text = 'You win! Restart'
            return

        if self.draw():
            for i in range(9):
                self.button[i].disabled = True
            self.resetBtn.text = 'Draw! Restart'
            return

        self.AIStep()

        if self.checkWin():
            self.resetBtn.text = 'You lose! Restart'
            return

        if self.draw():
            for i in range(9):
                self.button[i].disabled = True
            self.resetBtn.text = 'Draw! Restart'
            return

    # function to check win in the game
    def checkWin(self):
        for index in range(8):
            if [i.text for i in self.vector[index]].count('X') == 3:
                for a in range(9):
                    self.button[a].disabled = True
                for i in self.coordinate[index]:
                    self.button[i].color = (1, 0, 0, 1)
                return True
            elif [i.text for i in self.vector[index]].count('O') == 3:
                for a in range(9):
                    self.button[a].disabled = True
                for i in self.coordinate[index]:
                    self.button[i].color = (1, 0, 0, 1)
                return True
        return False

    # function to check draw in the game
    def draw(self):
        for i in range(9):
            if self.button[i].text == '':
                return False
        return True

    # AI
    def AIStep(self):
        # AI element
        if self.switch:
            stepAI = self.choice[0]
        else:
            stepAI = self.choice[1]
        # if AI can win next step
        for i in range(8):
            if [j.text for j in self.vector[i]].count(stepAI) == 2:
                for btn in self.vector[i]:
                    t = True
                    if not btn.text:
                        btn.text = stepAI
                    elif btn.text != stepAI:
                        t = False
                        break
                if t:
                    return
        # if user can win in next step
        for i in range(8):
            # user element
            step = self.choice[self.switch]
            if [j.text for j in self.vector[i]].count(step) == 2:
                for btn in self.vector[i]:
                    if not btn.text:
                        btn.text = stepAI
                        return
        if any([not self.button[i].text for i in [0, 2, 6, 8]]):
            i = choice([0, 2, 6, 8])
            while self.button[i].text:
                i = choice([0, 2, 6, 8])
            self.button[i].text = stepAI
            return
        if not self.button[4].text:
            self.button[4].text = stepAI
            return
        if any([not self.button[i].text for i in [1, 3, 5, 7]]):
            i = choice([1, 3, 5, 7])
            while self.button[i].text:
                i = choice([1, 3, 5, 7])
            self.button[i].text = stepAI
            return

    # function to restart game
    def restart(self, arg):
        self.resetBtn.text = 'Restart'
        for index in range(9):
            self.button[index].color = [1, 1, 1, 1]
            self.button[index].text = ""
            self.button[index].disabled = False
        if self.switch == 0:
            self.switch = 1
            self.fieldGenerate()
            self.AIStep()
        else:
            self.switch = 0

    # generate win vectors and coordinates
    def fieldGenerate(self):
        self.coordinate = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        )

        self.vector = (
            [self.button[x] for x in (0, 1, 2)],
            [self.button[x] for x in (3, 4, 5)],
            [self.button[x] for x in (6, 7, 8)],

            [self.button[y] for y in (0, 3, 6)],
            [self.button[y] for y in (1, 4, 7)],
            [self.button[y] for y in (2, 5, 8)],

            [self.button[d] for d in (0, 4, 8)],
            [self.button[d] for d in (2, 4, 6)],
        )


# TicTacToe for two person
class TicTacWidgetTwo(TicTacWidget):
    def tic_tac_toe(self, arg):
        if arg.text:
            return
        arg.text = self.choice[self.switch]

        if not self.switch:
            self.switch = 1
        else:
            self.switch = 0

        coordinate = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        )

        vector = (
            [self.button[x].text for x in (0, 1, 2)],
            [self.button[x].text for x in (3, 4, 5)],
            [self.button[x].text for x in (6, 7, 8)],

            [self.button[y].text for y in (0, 3, 6)],
            [self.button[y].text for y in (1, 4, 7)],
            [self.button[y].text for y in (2, 5, 8)],

            [self.button[d].text for d in (0, 4, 8)],
            [self.button[d].text for d in (2, 4, 6)],
        )

        for index in range(8):
            if vector[index].count('X') == 3:
                for a in range(9):
                    self.button[a].disabled = True
                for i in coordinate[index]:
                    self.button[i].color = (1, 0, 0, 1)
                self.resetBtn.text = 'Player 1 win, press to restart'
                break
            elif vector[index].count('O') == 3:
                for a in range(9):
                    self.button[a].disabled = True
                for i in coordinate[index]:
                    self.button[i].color = (1, 0, 0, 1)
                self.resetBtn.text = 'Player 2 win, press to restart'
                break


# TicTacToeScreen
class TicTacScreen(Screen):
    def __init__(self, **kw):
        super(TicTacScreen, self).__init__(**kw)

    # On enter the screen
    def on_enter(self):
        global players
        self.clear_widgets()
        if players == 1:
            self.add_widget(TicTacWidgetOne())
        else:
            self.add_widget(TicTacWidgetTwo())


# Buttons in minesweeper game
class MinesweeperTile(Button):
    def __init__(self, row, col, **kw):
        super().__init__(**kw)
        # Is momb?
        self.bomb = False
        # Row coordinate
        self.row = row
        # Col coordinate
        self.col = col


# Minesweeper widget
class MinesweeperWidget(BoxLayout):
    def __init__(self, **kw):
        super(MinesweeperWidget, self).__init__(**kw)

        # Change orientation of BoxLayout
        self.orientation = 'vertical'

        # Count of open tiles
        self.open = 0

        self.tilesX = 10
        self.tilesY = 10
        self.gameStart = True
        self.amountBombs = 10

        # Button back
        self.backBtn = Button(
            text='Back',
            size_hint=[1, 0.1],
            font_size='30sp',
            on_release=self.back,
        )

        # Field and gridlayout
        self.field = []
        grid = GridLayout(cols=10)

        # Set all tiles
        for i in range(self.tilesX):
            row = []
            for j in range(self.tilesY):
                row.append(MinesweeperTile(
                    i, j,
                    on_release=self.openTile,
                    disabled_color=(1, 0, 0, 1),
                )
                )
            self.field.append(row)

        # Set bombs in tiles
        for i in range(self.amountBombs):
            a = randint(0, self.tilesX - 1)
            b = randint(0, self.tilesY - 1)
            while self.field[a][b].bomb:
                a = randint(0, self.tilesX - 1)
                b = randint(0, self.tilesY - 1)
            self.field[a][b].bomb = True

        # Add field in grid
        for i in self.field:
            for j in i:
                grid.add_widget(j)

        # add reset button
        self.resetBtn = Button(
            text="Restart",
            font_size='20sp',
            size_hint=[1, .1],
            on_release=self.restart
        )

        # Add all widgets in Layout
        self.add_widget(self.backBtn)
        self.add_widget(grid)
        self.add_widget(self.resetBtn)

    # function back for the button
    def back(self, instance):
        global screen_manager
        screen_manager.transition = SlideTransition(direction='right')
        screen_manager.current = 'GamesScreen'

    # function restart game for the button
    def restart(self, arg):
        self.switch = 0
        self.gameStart = True
        self.resetBtn.text = 'Restart'
        self.resetBtn.color = (1, 1, 1, 1)
        for i in range(self.tilesX):
            for j in range(self.tilesY):
                self.field[i][j].color = [1, 1, 1, 1]
                self.field[i][j].text = ""
                self.field[i][j].bomb = False
                self.field[i][j].disabled = False

        # Set new bombs in tiles
        for i in range(self.amountBombs):
            a = randint(0, self.tilesX - 1)
            b = randint(0, self.tilesY - 1)
            while self.field[a][b].bomb:
                a = randint(0, self.tilesX - 1)
                b = randint(0, self.tilesY - 1)
            self.field[a][b].bomb = True

    # Open tile
    def openTile(self, instance):
        count = 0
        if instance.bomb:
            if self.gameStart:
                instance.bomb = False
                self.gameStart = False
                a = randint(0, self.tilesX - 1)
                b = randint(0, self.tilesY - 1)
                while self.field[a][b].bomb:
                    a = randint(0, self.tilesX - 1)
                    b = randint(0, self.tilesY - 1)
                self.field[a][b].bomb = True
            else:
                instance.text = 'bomb'
                self.lose()
                return
        self.gameStart = False
        count = self.get_neighbors_count(instance.row, instance.col)

        self.open += 1
        instance.disabled = True
        instance.text = str(count)

        if count == 0:
            self.openNeighbors(instance.row, instance.col)

        if self.open + 10 == 100:
            self.win()

    def get_neighbors_count(self, row, col):
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                try:
                    if self.field[i][j].bomb and i > -1 and j > -1:
                        count += 1
                except Exception:
                    pass
        return count

    # Open Neighbors of tile
    def openNeighbors(self, row, col):
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i < 0 or j < 0:
                    continue
                try:
                    if self.field[i][j].disabled:
                        continue
                    else:
                        count = self.get_neighbors_count(i, j)
                        self.field[i][j].disabled = True
                        self.field[i][j].text = str(count)
                        self.open += 1
                        if count == 0:
                            self.openNeighbors(i, j)
                except Exception:
                    pass

    # Disable all tiles
    def openAll(self, win=False):
        for i in range(self.tilesX):
            for j in range(self.tilesY):
                # Disable all tiles
                if self.field[i][j].bomb:
                    self.field[i][j].text = 'bomb'
                self.field[i][j].disabled = True
                if win:
                    self.field[i][j].color = (0, 1, 0, 1)

    # If player lose
    def lose(self):
        self.openAll()
        self.resetBtn.text = 'You lose! Restart'
        self.resetBtn.color = (1, 0, 0, 1)

    # If player win
    def win(self):
        self.openAll(win=True)
        self.resetBtn.text = 'You win! Restart'
        self.resetBtn.color = (0, 1, 0, 1)


# Minesweeper screen
class MinesweeperScreen(Screen):
    def __init__(self, **kw):
        super(MinesweeperScreen, self).__init__(**kw)

    def on_enter(self):
        self.clear_widgets()
        self.add_widget(MinesweeperWidget())


# Screen to choose number of players
class PlayersScreen(Screen):
    def __init__(self, **kw):
        super(PlayersScreen, self).__init__(**kw)

    def gameOne(self):
        global players
        global screen_manager
        players = 1
        screen_manager.transition = SlideTransition(direction='left')
        screen_manager.current = 'TicTacScreen'

    def gameTwo(self):
        global players
        global screen_manager
        players = 2
        screen_manager.transition = SlideTransition(direction='left')
        screen_manager.current = 'TicTacScreen'


class GamesScreen(Screen):
    view = ObjectProperty(None)

    def __init__(self, **kw):
        super(GamesScreen, self).__init__(**kw)
        self.view.bind(minimum_height=self.view.setter('height'))


class MainScreen(Screen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)

    def on_enter(self):
        pass


screen_manager = ScreenManager()


# App class
class GamesApp(App):
    def build(self):
        mainScreen = MainScreen(name='MainScreen')
        ticTacScreen = TicTacScreen(name='TicTacScreen')
        gamesScreen = GamesScreen(name='GamesScreen')
        playersScreen = PlayersScreen(name='PlayersScreen')
        minesweeperScreen = MinesweeperScreen(name='MinesweeperScreen')

        screen_manager.add_widget(mainScreen)
        screen_manager.add_widget(playersScreen)
        screen_manager.add_widget(ticTacScreen)
        screen_manager.add_widget(gamesScreen)
        screen_manager.add_widget(minesweeperScreen)

        return screen_manager


if __name__ == '__main__':
    GamesApp().run()
