from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import Screen
from words import words
from kivy.lang import Builder

Builder.load_file('screens/wordlist.kv')


class WordListScreen(Screen):
    pass


class WordListView(RecycleView):
    def __init__(self, **kwargs):

        super(WordListView, self).__init__(**kwargs)
        self.data = [
            {
                'arabic': w.arabic,
                'english': w.english,
                'pronunciation': w.pronunciation,
                'topic': w.topic,
                'enabled': w.enabled,
                'index': n,
                'comment': w.comment
            }
            for n, w in enumerate(words.word_list)
        ]
        self.refresh_from_data()

    def update(self):
        print("data refresh")
        self.data = [
            {
                'arabic': w.arabic,
                'english': w.english,
                'pronunciation': w.pronunciation,
                'topic': w.topic,
                'enabled': w.enabled,
                'index': n,
                'comment': w.comment
            }
            for n, w in enumerate(words.word_list)
        ]
        self.refresh_from_data()
