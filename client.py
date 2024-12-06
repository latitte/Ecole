import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import socket
import pickle
from ttkthemes import ThemedTk

class Application(ThemedTk):
    def __init__(self):
        super().__init__(theme="radiance")
        self.title("Gestion des Publications")
        self.geometry("750x600")
        self.configure(bg="#F5F5F5")
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SF Pro Display", 12))
        self.style.configure("TButton", font=("SF Pro Display", 10), padding=10)
        
        self.create_widgets()

    def create_widgets(self):
        # Titre
        title_label = ttk.Label(self, text="Gestion des Publications", font=("SF Pro Display", 18, "bold"))
        title_label.pack(pady=10)

        # Sous-titre
        sub_label = ttk.Label(self, text="Ajouter un élément", font=("SF Pro Display", 14))
        sub_label.pack(pady=5)

        # Cadre des boutons
        button_frame = ttk.Frame(self, padding=10)
        button_frame.pack()

        add_buttons = [
            ("Thèse de Doctorat", self.add_phdthesis),
            ("Article", self.add_article),
            ("Livre", self.add_book)
        ]

        for text, command in add_buttons:
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=15)

        # Cadre de recherche
        search_frame = ttk.Frame(self, padding=10)
        search_frame.pack(pady=5)

        criteria_label = ttk.Label(search_frame, text="Rechercher par:")
        criteria_label.pack(side=tk.LEFT, padx=5)

        self.criteria_combobox = ttk.Combobox(
            search_frame, values=["Référence", "Auteur", "Titre", "Année"], state="readonly"
        )
        self.criteria_combobox.pack(side=tk.LEFT, padx=5)

        keyword_label = ttk.Label(search_frame, text="Mot-clé:")
        keyword_label.pack(side=tk.LEFT, padx=5)

        self.keyword_entry = ttk.Entry(search_frame)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(search_frame, text="Rechercher", command=self.search_publications)
        search_button.pack(side=tk.LEFT, padx=5)

        # Zone d'affichage des publications
        self.text_display = tk.Text(self, wrap="word", state="disabled", height=15, bg="#E8E8E8", font=("SF Pro Display", 12), padx=10)
        self.text_display.pack(expand=True, fill="both", padx=10, pady=10)

        # Bouton d'affichage des publications
        show_button = ttk.Button(self, text="Afficher toutes les publications", command=self.show_publications)
        show_button.pack(pady=10)

    def send_request(self, request_data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(("127.0.0.1", 65432))
            client_socket.send(pickle.dumps(request_data))
            print(request_data)
            response = pickle.loads(client_socket.recv(1024))
        return response

    def prompt_attributes(self, attr_names):
        attributes = []
        for attr in attr_names:
            value = simpledialog.askstring("Saisie", f"Entrez {attr}:", parent=self)
            if not value:
                messagebox.showwarning("Attention", f"Le champ {attr} est obligatoire!")
                return None
            attributes.append(value)
        return attributes

    def add_publication(self, pub_type, attributes):
        request_data = {
            "action": "add_publication",
            "pub_type": pub_type,
            "attributes": attributes
        }
        response = self.send_request(request_data)
        messagebox.showinfo("Réponse du serveur", response)

    def add_phdthesis(self):
        attr_names = ["Référence", "Auteur", "Titre", "Année", "Mois", "Mot-clé", "École", "Type"]
        attributes = self.prompt_attributes(attr_names)
        if attributes:
            self.add_publication("PhDThesis", attributes)

    def add_article(self):
        attr_names = ["Référence", "Auteur", "Titre", "Année", "Journal"]
        attributes = self.prompt_attributes(attr_names)
        if attributes:
            self.add_publication("Article", attributes)

    def add_book(self):
        attr_names = ["Référence", "Auteur", "Titre", "Année", "Volume", "Série", "Adresse", "Édition", "Mois", "Note"]
        attributes = self.prompt_attributes(attr_names)
        if attributes:
            self.add_publication("Book", attributes)

    def show_publications(self):
        request_data = {"action": "get_publications"}
        response = self.send_request(request_data)
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, tk.END)
        if response:
            for pub in response:
                self.text_display.insert(tk.END, pub + "\n\n")
        self.text_display.config(state="disabled")

    def search_publications(self):
        criteria = self.criteria_combobox.get()
        keyword = self.keyword_entry.get().strip()

        if not criteria or not keyword:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs!")
            return

        request_data = {
            "action": "search_publications",
            "criteria": criteria,
            "keyword": keyword
        }

        response = self.send_request(request_data)
        self.text_display.config(state="normal")
        self.text_display.delete(1.0, tk.END)
        if response:
            for pub in response:
                self.text_display.insert(tk.END, pub + "\n\n")
        self.text_display.config(state="disabled")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
