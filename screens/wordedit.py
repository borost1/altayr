from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
import arabic_reshaper
from bidi.algorithm import get_display
from kivy.lang import Builder
from words import words, Word

Builder.load_file('screens/wordedit.kv')


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
    word_comment = StringProperty()

    def reset_list_props(self):
        self.categories = words.categories
        self.topics = words.topics

    def set_default_index(self, index=None):
        has_index = index is not None
        self.current_index = index if has_index else None
        current_word = words.dictionary[self.current_index] if has_index else Word("", "", "", "", "", True, "")
        self.word_english_text = current_word.english
        self.word_arabic_text = current_word.arabic
        self.word_category = current_word.category
        self.word_pronunciation = current_word.pronunciation
        self.word_topic = current_word.topic
        self.word_enabled = current_word.enabled
        self.word_comment = current_word.comment

        if not has_index:
            self.ids.word_arabic_text.re_init()

    def save_word(self):

        if self.current_index is not None:
            words.dictionary[self.current_index] = Word(
                self.ids.word_english_text.text,
                self.ids.word_arabic_text.text[::-1],
                self.ids.word_pronunciation.text,
                self.ids.word_category.text,
                self.ids.word_topic.text,
                self.ids.word_enabled.active,
                self.ids.word_comment.text
            )
        else:
            words.dictionary.append(
                Word(
                    self.ids.word_english_text.text,
                    self.ids.word_arabic_text.text[::-1],
                    self.ids.word_pronunciation.text,
                    self.ids.word_category.text,
                    self.ids.word_topic.text,
                    self.ids.word_enabled.active,
                    self.ids.word_comment.text
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
        self.ids.word_comment.text = ""


class ArabicTextInput(TextInput):
    max_chars = NumericProperty(200)  # maximum character allowed
    str = StringProperty()

    def __init__(self, **kwargs):
        super(ArabicTextInput, self).__init__(**kwargs)
        self.text = ""

    def re_init(self):
        print("there was reinit here.")
        self.text = ""
        self.str = ""

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