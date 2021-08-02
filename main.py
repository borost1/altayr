from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from screens.settings import SettingsScreen
from screens.card import CardScreen
from screens.dictionary import DictionaryScreen
from screens.wordedit import WordEditScreen
from screens.categoryfilter import CategoryFilterScreen
from screens.topicfilter import TopicFilterScreen
# from kivy.config import Config
# Config.set('graphics', 'width', '600')
# Config.set('graphics', 'height', '800')
# Config.write()
# https://colorhunt.co/palette/ffe194e8f6efb8dfd84c4c6d


class MyApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(CardScreen(name="CARD"))
        sm.add_widget(DictionaryScreen(name="DICTIONARY"))
        sm.add_widget(SettingsScreen(name="SETTINGS"))
        sm.add_widget(WordEditScreen(name="WORD_EDIT"))
        sm.add_widget(CategoryFilterScreen(name="FILTERS"))
        sm.add_widget(TopicFilterScreen(name="TOPICS"))
        return sm


if __name__ == '__main__':
    MyApp().run()
