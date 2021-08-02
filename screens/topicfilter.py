from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from words import words
from kivy.lang import Builder

Builder.load_file("screens/topicfilter.kv")


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
