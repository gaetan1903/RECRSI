from kivy.config import Config
## CONFIGURATION FOR DEVELOPMENT ONLY
# Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '320')
Config.set('graphics', 'height', '568')
#######################################

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Application(MDApp):

	def build(self):
		self.theme_cls.primary_palette = "Teal"

		return Builder.load_file('main.kv')


if __name__ == '__main__':
	Application().run()