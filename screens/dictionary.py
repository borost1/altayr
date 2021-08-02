from words import words
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder

Builder.load_file('screens/dictionary.kv')


class DictionaryScreen(Screen):
    pass


class DictView(RecycleView):
    def __init__(self, **kwargs):
        super(DictView, self).__init__(**kwargs)
        self.data = [
            {
                'english': w.english,
                'pronunciation': w.pronunciation,
                'arabic': w.arabic,
                'index': k
            }
            for k, w in enumerate(words.dictionary)
        ]
        self.refresh_from_data()

    def update(self):
        self.data = [
            {
                'english': w.english,
                'pronunciation': w.pronunciation,
                'arabic': w.arabic,
                'index': k
            }
            for k, w in enumerate(words.dictionary)
        ]
        self.refresh_from_data()
