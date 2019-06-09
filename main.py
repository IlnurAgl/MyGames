from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Window.clearcolor = (1, 1, 1, 1)

Builder.load_file('Games.kv')


class TicTacWidget(BoxLayout):
    def __init__(self, **kw):
        super(TicTacWidget, self).__init__(**kw)

        self.orientation = 'vertical'

        self.padding = self.width * 0.1

        self.choice = ['X', 'O']

        self.switch = 0

        self.add_widget(
            Button(
                text="Back",
                size_hint=[1, .1],
                font_size='30sp',
                on_release=self.back,
            )
        )

        grid = GridLayout(cols=3)

        self.spacing = self.width * 0.05

        self.button = [0 for _ in range(9)]
        for index in range(9):
            self.button[index] = Button(
                on_release=self.tic_tac_toe,
                font_size='60sp',
                disabled=False,
            )
            grid.add_widget(self.button[index])

        self.add_widget(grid)

        self.resetBtn = Button(
            text="Restart",
            font_size='30sp',
            size_hint=[1, .1],
            on_release=self.restart
        )

        self.add_widget(self.resetBtn)

    def back(self, instance):
        global screen_manager
        screen_manager.transition = SlideTransition(direction='right')
        screen_manager.current = 'GamesScreen'

    def restart(self, arg):
        self.switch = 0
        self.resetBtn.text = 'Restart'
        for index in range(9):
            self.button[index].color = [1, 1, 1, 1]
            self.button[index].text = ""
            self.button[index].disabled = False

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
                self.resetBtn.text = 'Player one win, press to restart'
                break
            elif vector[index].count('O') == 3:
                for a in range(9):
                    self.button[a].disabled = True
                for i in coordinate[index]:
                    self.button[i].color = (1, 0, 0, 1)
                self.resetBtn.text = 'Player two win, press to restart'
                break


class TicTacScreen(Screen):
    def __init__(self, **kw):
        super(TicTacScreen, self).__init__(**kw)

    def on_enter(self):
        self.clear_widgets()
        self.add_widget(TicTacWidget())


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


class GamesApp(App):
    def build(self):
        mainScreen = MainScreen(name='MainScreen')
        ticTacScreen = TicTacScreen(name='TicTacScreen')
        gamesScreen = GamesScreen(name='GamesScreen')

        screen_manager.add_widget(mainScreen)
        screen_manager.add_widget(ticTacScreen)
        screen_manager.add_widget(gamesScreen)

        return screen_manager


if __name__ == '__main__':
    GamesApp().run()
