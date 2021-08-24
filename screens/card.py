from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from words import words
from kivy.metrics import dp
from kivy.lang import Builder

Builder.load_file('screens/card.kv')


class CardScreen(Screen):
    default_language = StringProperty("Arabic")
    pronunciation = BooleanProperty(False)
    current_language = StringProperty("Arabic")
    current_index = NumericProperty(0)
    list_length = NumericProperty(len(words.word_list))
    display_word = StringProperty(words.word_list[0].arabic)

    def re_init(self):
        # self.current_index = 0
        self.list_length = len(words.word_list)
        self.default_language = self.manager.get_screen("SETTINGS").default_language
        self.pronunciation = self.manager.get_screen("SETTINGS").pronunciation
        self.current_language = "English" if self.default_language == "Arabic" else "Arabic"
        self.render_word()

    def browse(self, direction='RIGHT'):

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
        if len(words.word_list) > 0:
            self.ids.word_button.font_size = dp(100) if self.current_language == "Arabic" else dp(50)
            self.display_word = words.word_list[self.current_index].arabic if self.current_language == "Arabic" \
                else words.word_list[self.current_index].english
            if self.pronunciation and self.current_language != self.default_language:
                self.display_word += "\n" + words.word_list[self.current_index].pronunciation
        else:
            self.ids.word_button.font_size = dp(30)
            self.display_word = "Please set your filter, your word list is empty."

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
