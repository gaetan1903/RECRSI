import sqlite3 


class Database():
	def __init__(self):
		self.db = sqlite3.connect("__com.gaetan1903.RECRSI.db")
		self.cursor = self.db.cursor()
		self.__initialise()
	

	def __initialise(self):
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS Produit ( 
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				reference TEXT UNIQUE,
				prixAchat INTEGER,
				prixVente INTEGER,
				dispo INTEGER,
				vendu INTEGER);
			""")

		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS Commande(
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				ref_produit TEXT UNIQUE,
				quantite INTEGER,
				adresse TEXT,
				contact TEXT,
				client TEXT,
				dateCommande TEXT,
				dateLivraison TEXT,
				status TEXT DEFAULT 'NON LIVREE',
				FOREIGN KEY(ref_produit) REFERENCES Produit(reference) );
			""")
		
		self.db.commit()


	def insertCommande(self, *args):
		print(args)
		try:
			self.cursor.execute("""
				INSERT INTO Commande
					(ref_produit, quantite, adresse, contact, dateLivraison, client, dateCommande)
				VALUES (?, ?, ?, ?, ?, ?, ?)
			""", args)
		
		except Exception as err:
			print(err)
			return False, err

		self.db.commit()
		return True, True