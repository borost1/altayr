import os
import sys
import arabic_reshaper
from bidi.algorithm import get_display
import json


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Word:
    def __init__(self, english, arabic, pronunciation, category, topic, enabled, comment=""):
        self.english = english
        self.arabic = get_display(arabic_reshaper.reshape(arabic))
        self.pronunciation = pronunciation
        self.category = category
        self.topic = topic
        self.enabled = enabled
        self.comment = comment

    def __str__(self):
        return str({
            "english": self.english,
            "arabic": self.arabic,
            "pronunciation": self.pronunciation,
            "category": self.category,
            "topic": self.topic,
            "enabled": self.enabled,
            "comment": self.comment
        })

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class WordDictionary:
    def __init__(self):
        self.dictionary = []
        self.category_filters = []
        self.topic_filters = []

        raw_data = open(resource_path("words.json"), "r", encoding="utf-8")
        data = json.load(raw_data)
        dictionary = data["dictionary"]
        self.categories = data["categories"]
        self.topics = data["topics"]
        for d in dictionary:
            self.dictionary.append(
                Word(d['en'], d['ar'], d['pron'], d['category'], d['topic'], d['enabled'], d['comment'])
            )

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

    def add_category(self, category_str):
        if category_str not in self.categories:
            self.categories.append(category_str)

    def remove_category(self, category_str):
        if category_str in self.categories:
            self.categories.remove(category_str)

    def add_topic(self, topic_str):
        if topic_str not in self.topics:
            self.topics.append(topic_str)

    def remove_topic(self, topic_str):
        if topic_str in self.topics:
            self.topics.remove(topic_str)

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
        self.word_list = [w for w in self.dictionary
                          if w.category not in self.category_filters
                          and w.topic not in self.topic_filters
                          and w.enabled]

        print(self.topic_filters + self.category_filters)
        for w in self.word_list:
            print(w.pronunciation + " - " + w.topic + " - " + w.category)

    def sort_dictionary(self):
        self.dictionary.sort(key=lambda x: str(x.english).lower())

    def sort_words(self):
        self.word_list.sort(key=lambda x: str(x.english).lower())

    def export_dictionary(self):
        self.sort_dictionary()
        exp_words = []

        for w in self.dictionary:
            word = {
                "en": w.english,
                "ar": w.arabic[::-1],
                "pron": w.pronunciation,
                "category": w.category,
                "topic": w.topic,
                "enabled": w.enabled,
                "comment": w.comment
            }
            exp_words.append(word)

        obj = {
            "dictionary": exp_words,
            "categories": self.categories,
            "topics": self.topics
        }
        # print(str(obj))
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False)
            f.close()


words = WordDictionary()
