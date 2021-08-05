from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty
from words import words
from kivy.lang import Builder

Builder.load_file('screens/categoryfilter.kv')


class CategoryFilterScreen(Screen):
    categories = ListProperty(words.categories)

    def add_category(self, cat_str):
        words.add_category(cat_str)
        self.categories = words.categories
        self.ids.add_new_category.text = ''

    def remove_category(self, cat_str):
        words.remove_category(cat_str)
        self.categories = words.categories
        self.ids.remove_category.text = "choose category to remove..."

    def refresh_categories(self):
        self.categories = words.categories


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
