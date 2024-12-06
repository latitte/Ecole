import socket
import pickle

# Classe des publications
class Publications:
    def __init__(self, reference, author, title, year):
        self.attributes = {
            "Référence": reference,
            "Auteur": author,
            "Titre": title,
            "Année": year
        }

    def afficher(self):
        return "\n".join(f"{key}: {value}" for key, value in self.attributes.items())

class PhDThesis(Publications):
    def __init__(self, reference, author, title, year, month, keyword, school, thesis_type):
        super().__init__(reference, author, title, year)
        self.attributes.update({
            "Mois": month,
            "Mot-clé": keyword,
            "École": school,
            "Type": thesis_type
        })

class Article(Publications):
    def __init__(self, reference, author, title, year, journal):
        super().__init__(reference, author, title, year)
        self.attributes.update({"Journal": journal})

class Book(Publications):
    def __init__(self, reference, author, title, year, volume, series, address, edition, month, note):
        super().__init__(reference, author, title, year)
        self.attributes.update({
            "Volume": volume,
            "Série": series,
            "Adresse": address,
            "Édition": edition,
            "Mois": month,
            "Note": note
        })

# Gestion des publications
class PublicationManager:
    def __init__(self):
        self.publications = [
            PhDThesis("Ref01", "Alice Dupont", "Étude sur l'IA", "2021", "Mars", "IA", "Université X", "Doctorat"),
            Article("Ref02", "Bob Martin", "L'impact du Big Data", "2020", "Journal des Sciences"),
            Book("Ref03", "Clara Besson", "Les bases de Python", "2019", "3", "Série Informatique", "Paris", "2e édition", "Janvier", "Introduction à la programmation")
        ]

    def add_publication(self, pub_type, attributes):
        try:
            pub_class = globals()[pub_type]
            publication = pub_class(*attributes)
            self.publications.append(publication)
            return f"{pub_type} ajouté avec succès!"
        except Exception as e:
            return f"Erreur lors de l'ajout : {e}"

    def get_publications(self):
        return [pub.afficher() for pub in self.publications]

    def search_publications(self, criteria, keyword):
        results = [pub for pub in self.publications if keyword.lower() in pub.attributes[criteria].lower()]
        return [pub.afficher() for pub in results]

# Serveur
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 65432))  # Bind to localhost on port 65432
    server.listen(5)

    pub_manager = PublicationManager()

    print("Le serveur est en écoute...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion acceptée de {addr}")
        data = client_socket.recv(1024)
        if not data:
            break

        request = pickle.loads(data)

        # Traitement des requêtes
        if request["action"] == "add_publication":
            response = pub_manager.add_publication(request["pub_type"], request["attributes"])
        elif request["action"] == "get_publications":
            response = pub_manager.get_publications()
        elif request["action"] == "search_publications":
            response = pub_manager.search_publications(request["criteria"], request["keyword"])

        client_socket.send(pickle.dumps(response))
        client_socket.close()

if __name__ == "__main__":
    start_server()
