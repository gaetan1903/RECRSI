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
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

#########################################
from datetime import date
from app import Database



class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Application(MDApp):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.INTERFACE = Builder.load_file('main.kv')
		self.database = Database()

		menu_items = [{"text":f"item {i}"} for i in range(50)]
		self.menu = MDDropdownMenu(
            caller=self.INTERFACE.ids.refCommande,
            items=menu_items,
            position="center",
            width_mult=8,
        )
		self.menu.bind(on_release=self.set_item)


	def build(self):
		self.theme_cls.primary_palette = "Teal"
		self.items = [f"test {i}" for i in range(5)]

		return self.INTERFACE


	def set_item(self, instance_menu, instance_menu_item):
 		def set_item(interval):
 			self.INTERFACE.ids.refCommande.text = instance_menu_item.text
 			instance_menu.dismiss()
 		Clock.schedule_once(set_item, 0.5)


	# fonction Field du Date de livraison
	def show_datePicker(self):
		dialogDate = MDDatePicker(callback=self.get_date)
		dialogDate.open()
	def get_date(self, date):
		self.INTERFACE.ids.dateLivraison.text = date.__str__()
	

	def validateCommande(self, **kwargs):
		"""  Fonction Screen COMMANDE """
		champs = [
				self.INTERFACE.ids.refCommande,
				self.INTERFACE.ids.quantite,
				self.INTERFACE.ids.adresse,
				self.INTERFACE.ids.contact,
				self.INTERFACE.ids.dateLivraison
			]

		if not kwargs.get('validate_'):
			# verification des champs vides
			for val in champs:
				if val.text.strip() == '':
					return MDDialog(
						title="Erreur de validation",
						text=f"Le champ {val.hint_text} est obligatoire"
					).open()
			self.dialogCommande = MDDialog(
				title="Confirmation",
				text="Enregistrer la commande ?",
				buttons=[
					MDFlatButton(
						text="Continuer",
						text_color=self.theme_cls.primary_color,
						on_release=lambda f: self.validateCommande(validate_=True)
					)
				]
			)
			self.dialogCommande.open()
		else:
			self.dialogCommande.dismiss()
			for i in range(len(champs)): champs[i] = champs[i].text
			champs.append(self.INTERFACE.ids.nomClient.text)
			champs.append(date.today().__str__())
			ret = self.database.insertCommande(*champs)
			if ret[0]:
				MDDialog(
					title="Succes",
					text="Commande effectué",
					radius=[20, 7, 20, 7],
				).open()
			else:
				MDDialog(
					title="Erreur",
					text=str(ret[1]),
					radius=[20, 7, 20, 7],
				).open()



if __name__ == '__main__':
	Application().run()