from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from random import shuffle
from words import words
from kivy.lang import Builder

Builder.load_file('screens/settings.kv')


class SettingsScreen(Screen):
    default_language = StringProperty("Arabic")
    pronunciation = BooleanProperty(False)
    dict_words = NumericProperty(len(words.dictionary))
    list_words = NumericProperty(len(words.word_list))

    def toggle_pronunciation(self):
        self.pronunciation = not self.pronunciation

    def shuffle_cards(self):
        shuffle(words.word_list)

    def export_dict(self):
        words.export_dictionary()