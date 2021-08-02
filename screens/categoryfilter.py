from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from words import words
from kivy.lang import Builder

Builder.load_file('screens/categoryfilter.kv')


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
