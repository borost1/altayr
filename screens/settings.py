from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from random import shuffle
from words import words
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.popup import Popup
import os
import json

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
        desktop_platforms = [
            platform == "win",
            platform == "macosx"
        ]
        if any(desktop_platforms):
            self.show_save()
        else:
            words.export_dictionary()

    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0]), "r", encoding="utf-8") as stream:
            words.build_dictionary(stream)

        self.dismiss_popup()

    def save(self, path, filename):
        obj = words.export_dict_object()
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)
            f.close()

        self.dismiss_popup()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)