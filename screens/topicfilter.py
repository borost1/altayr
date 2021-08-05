from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from words import words
from kivy.lang import Builder
from kivy.properties import ListProperty

Builder.load_file("screens/topicfilter.kv")


class TopicFilterScreen(Screen):
    topics = ListProperty(words.topics)

    def add_topic(self, topic_str):
        words.add_topic(topic_str)
        self.topics = words.topics
        self.ids.add_new_topic.text = ''

    def remove_topic(self, topic_str):
        words.remove_topic(topic_str)
        self.topics = words.topics


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
