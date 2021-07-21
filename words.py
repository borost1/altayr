import arabic_reshaper
from bidi.algorithm import get_display
import json


class Word:
    def __init__(self, english, arabic, pronunciation, category, topic, enabled):
        self.english = english
        self.arabic = get_display(arabic_reshaper.reshape(arabic))
        self.pronunciation = pronunciation
        self.category = category
        self.topic = topic
        self.enabled = enabled

    def __str__(self):
        return str({
            "english": self.english,
            "arabic": self.arabic,
            "pronunciation": self.pronunciation,
            "category": self.category,
            "topic": self.topic,
            "enabled": self.enabled
        })

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class WordDictionary:
    def __init__(self):
        self.dictionary = []
        self.categories = ["noun", "adjective", "verb", "particle"]
        self.category_filters = []
        self.topics = ["general", "housing"]
        self.topic_filters = []

        raw_data = open("words.json", "r", encoding="utf-8")
        data = json.load(raw_data)
        dictionary = data["dictionary"]
        for d in dictionary:
            self.dictionary.append(Word(d['en'], d['ar'], d['pron'], d['category'], d['topic'], d['enabled']))

            if d['category'] not in self.categories:
                self.categories.append(d['category'])

            if d['topic'] not in self.topics:
                self.topics.append(d['topic'])

        self.word_list = self.dictionary

    def __str__(self):
        result = ""
        for d in self.word_list:
            result += d.to_json()
        return result

    def add_category_filter(self, filter_str):
        if filter_str not in self.category_filters:
            self.category_filters.append(filter_str)

    def add_topic_filter(self, filter_str):
        if filter_str not in self.topic_filters:
            self.topic_filters.append(filter_str)

    def remove_category_filter(self, filter_str):
        if filter_str in self.category_filters:
            self.category_filters.remove(filter_str)

    def remove_topic_filter(self, filter_str):
        if filter_str in self.topic_filters:
            self.topic_filters.remove(filter_str)

    def set_filter(self):
        if len(self.category_filters) > 0:
            self.word_list = [w for w in self.dictionary if w.category in self.category_filters and w.enabled]

        if len(self.topic_filters) > 0:
            self.word_list = [w for w in self.dictionary if w.topic in self.topic_filters and w.enabled]

    def export_dictionary(self):

        exp_words = []

        for w in self.dictionary:
            word = {
                "en": w.english,
                "ar": w.arabic[::-1],
                "pron": w.pronunciation,
                "category": w.category,
                "topic": w.topic,
                "enabled": w.enabled
            }
            exp_words.append(word)

        obj = {
            "dictionary": exp_words
        }
        print(str(obj))
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)
            f.close()