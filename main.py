import arabic_reshaper
from bidi.algorithm import get_display
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from words import WordDictionary, Word
from random import randint, shuffle
# from kivy.config import Config
# Config.set('graphics', 'width', '600')
# Config.set('graphics', 'height', '800')
# Config.write()

words = WordDictionary()


# https://colorhunt.co/palette/ffe194e8f6efb8dfd84c4c6d


class SettingsScreen(Screen):
    default_language = StringProperty("Arabic")
    pronunciation = BooleanProperty(False)
    shuffling = BooleanProperty(False)

    def toggle_pronunciation(self):
        self.pronunciation = not self.pronunciation

    def toggle_shuffling(self):
        self.shuffling = not self.shuffling


class CardScreen(Screen):
    default_language = StringProperty("Arabic")
    pronunciation = BooleanProperty(False)
    shuffling = BooleanProperty(False)
    current_language = StringProperty("Arabic")
    current_index = NumericProperty(0)
    display_word = StringProperty(words.word_list[0].arabic)

    def re_init(self):
        self.current_index = 0
        self.default_language = self.manager.get_screen("SETTINGS").default_language
        self.pronunciation = self.manager.get_screen("SETTINGS").pronunciation
        self.shuffling = self.manager.get_screen("SETTINGS").shuffling
        self.current_language = "English" if self.default_language == "Arabic" else "Arabic"

    def browse(self, direction='RIGHT'):
        if self.shuffling:
            next_index = self.current_index
            while self.current_index == next_index:
                self.current_index = randint(0, len(words.word_list)-1)

        if len(words.word_list) != 0:
            if direction == 'RIGHT':
                self.current_index += 1 if self.current_index < (len(words.word_list)-1) else -(len(words.word_list)-1)
            elif direction == 'LEFT':
                self.current_index -= 1 if self.current_index > 0 else -(len(words.word_list)-1)
            self.current_language = self.default_language
            self.render_word()

    def swap_lang(self):
        self.current_language = "English" if self.current_language == "Arabic" else "Arabic"
        self.render_word()

    def render_word(self):
        self.display_word = words.word_list[self.current_index].arabic if self.current_language == "Arabic" \
            else words.word_list[self.current_index].english
        if self.pronunciation and self.current_language != self.default_language:
            self.display_word += "\n - \n" + words.word_list[self.current_index].pronunciation

    def set_filter(self, filter_text, filter_type):
        print(filter_type)
        if filter_type == "category":
            if filter_text in words.category_filters:
                words.remove_category_filter(filter_text)
            else:
                words.add_category_filter(filter_text)
        elif filter_type == "topic":
            if filter_text in words.topic_filters:
                words.remove_topic_filter(filter_text)
            else:
                words.add_topic_filter(filter_text)
        words.set_filter()
        self.re_init()


class DictionaryScreen(Screen):
    def export_dict(self):
        words.export_dictionary()


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


class WordEditScreen(Screen):
    current_index = NumericProperty(0, allownone=True)
    word_english_text = StringProperty()
    word_arabic_text = StringProperty()
    word_category = StringProperty()
    word_pronunciation = StringProperty()
    word_topic = StringProperty()
    word_enabled = BooleanProperty(True)
    categories = ListProperty(words.categories)
    topics = ListProperty(words.topics)

    def set_default_index(self, index=None):
        has_index = index is not None
        self.current_index = index if has_index else None
        current_word = words.dictionary[self.current_index] if has_index else Word("", "", "", "", "", True)
        self.word_english_text = current_word.english
        self.word_arabic_text = current_word.arabic
        self.word_category = current_word.category
        self.word_pronunciation = current_word.pronunciation
        self.word_topic = current_word.topic
        self.word_enabled = current_word.enabled

    def save_word(self):

        if self.current_index is not None:
            words.dictionary[self.current_index] = Word(
                self.ids.word_english_text.text,
                self.ids.word_arabic_text.text[::-1],
                self.ids.word_pronunciation.text,
                self.ids.word_category.text,
                self.ids.word_topic.text,
                self.ids.word_enabled.active
            )
        else:
            words.dictionary.append(
                Word(
                    self.ids.word_english_text.text,
                    self.ids.word_arabic_text.text[::-1],
                    self.ids.word_pronunciation.text,
                    self.ids.word_category.text,
                    self.ids.word_topic.text,
                    self.ids.word_enabled.active
                )
            )

    def delete_word(self):
        if self.current_index is not None:
            del words.dictionary[self.current_index]

    def reset_view(self):
        self.ids.word_english_text.text = ""
        self.ids.word_arabic_text.text = ""
        self.ids.word_arabic_text.text = ""
        self.ids.word_pronunciation.text = ""
        self.ids.word_category.text = ""
        self.ids.word_topic.text = ""
        self.ids.word_enabled.active = False


class ArabicTextInput(TextInput):
    max_chars = NumericProperty(200)  # maximum character allowed
    str = StringProperty()

    def __init__(self, **kwargs):
        super(ArabicTextInput, self).__init__(**kwargs)
        self.text = ""

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return
        self.str = self.str+substring
        self.text = get_display(arabic_reshaper.reshape(self.str))
        substring = ""
        super(ArabicTextInput, self).insert_text(substring, from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str)-1]
        self.text = get_display(arabic_reshaper.reshape(self.str))


class CategoryFilterScreen(Screen):
    pass


class CategoryFilterView(RecycleView):
    def __init__(self, **kwargs):
        super(CategoryFilterView, self).__init__(**kwargs)
        self.data = [
            {
                'text': f,
                'enabled': True if f in words.category_filters else False,
                'type': "category"
            }
            for f in words.categories
        ]
        self.refresh_from_data()

    def update(self):
        self.data = [
            {
                'text': f,
                'enabled': True if f in words.category_filters else False,
                'type': "category"
            }
            for f in words.categories
        ]
        self.refresh_from_data()


class TopicFilterScreen(Screen):
    pass


class TopicFilterView(RecycleView):
    def __init__(self, **kwargs):
        super(TopicFilterView, self).__init__(**kwargs)
        self.data = [
            {
                'text': f,
                'enabled': True if f in words.topic_filters else False,
                'type': "topic"
            }
            for f in words.topics
        ]
        self.refresh_from_data()

    def update(self):
        self.data = [
            {
                'text': f,
                'enabled': True if f in words.topic_filters else False,
                'type': "topic"
            }
            for f in words.topics
        ]
        self.refresh_from_data()


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