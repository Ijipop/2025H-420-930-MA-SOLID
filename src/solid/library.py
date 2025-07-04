"""





******************JEAN-FRANCOIS LEFEBVRE******************

Je mentionne que cela m'a pris 1 heure ++ juste pour comprendre le S de SMART.
Je comprend un peu mieux le O et pour le reste je comprend l'idée mais j'aurai besoins
de plus de temps et de pratique pour bien comprendre.

"""

from abc import ABC, abstractmethod

"""Pour le S de SMART,J'ajoute la classe ValidateurISBN pour valider l'ISBN, parce que ce n'est pas la responsabilité 
de la classe Livre.
Ainsi plus tard si on veut changer la logique de validation, on peut le faire sans modifier la classe Livre, that's right.
"""
class ValidateurISBN:
    @staticmethod
    def valider(isbn: str):
        if len(isbn.replace('-', '')) not in (10, 13):
            raise ValueError("ISBN invalide")

# Interface de base pour tous les livres
class ILivre(ABC):
    @abstractmethod
    def genre(self) -> str:
        pass

    @abstractmethod
    def valider_isbn(self):
        pass

    @abstractmethod
    def afficher_format_long(self) -> str:
        pass

    @abstractmethod
    def nb_pages(self) -> int:
        pass

    @abstractmethod
    def narrateur(self) -> str:
        pass
"""
Je sépare la classe Livre en deux sous-classes : LivrePapier et LivreAudio. Parce que
les livres papier et audio ont des propriétés différentes. ***Exemple*** plus tard on pourra ajouter disons, la durée du livre
audio sans passer par la classe Livre, on pourra le faire dans la classe LivreAudio. Ainsi on respecte le principe de 
responsabilité unique. Incroyable.

"""
class Livre(ILivre):


    """
Pour le O de OPEN/CLOSED, J'ai enlevé ceci

def afficher_format_long(self) -> str:
    if self.genre() == "BD":
        return f"{self.titre} – {self.auteur} (BD, ISBN: {self.isbn})"
    elif self.genre() == "Roman":
        return f"{self.titre} – {self.auteur} (Roman, ISBN: {self.isbn})"
    et remplacé par ceci


    def afficher_format_long(self) -> str:
        return f"{self.titre} – {self.auteur} ({self._genre}, ISBN: {self.isbn})"
    Ainsi si on veut ajouter un nouveau genre, 
    on peut le faire sans modifier la classe Livre, on ne rit plus.
"""
    def __init__(self, isbn: str, titre: str, auteur: str, genre: str):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self._genre = genre

    def genre(self) -> str:
        return self._genre

    def valider_isbn(self):
        ValidateurISBN.valider(self.isbn)

#Voici la modif
    def afficher_format_long(self) -> str:
        return f"{self.titre} – {self.auteur} ({self._genre}, ISBN: {self.isbn})"

# Sous-classe pour les livres en papyrus
class LivrePapier(Livre):
    def __init__(self, isbn, titre, auteur, genre, nb_pages):
        super().__init__(isbn, titre, auteur, genre)
        self._nb_pages = nb_pages

    def nb_pages(self) -> int:
        return self._nb_pages

    def narrateur(self) -> str:
        return ""  # Non applicable

# Sous-classe pour les livres audio
class LivreAudio(Livre):
    def __init__(self, isbn, titre, auteur, genre, narrateur):
        super().__init__(isbn, titre, auteur, genre)
        self._narrateur = narrateur

    def nb_pages(self) -> int:
        return -1  # Non applicable

    def narrateur(self) -> str:
        return self._narrateur




class Bibliotheque:
    def __init__(self):
        self.inventaire: dict[str, int] = {}
        self.notif_service = NotificationServiceMail()
        self.notif_service_sms = NotificationServiceSMS()

    def ajouter_livre(self, livre: Livre, quantite: int):
        self.inventaire[livre.isbn] = self.inventaire.get(livre.isbn, 0) + quantite

    def generer_rapport_et_notification(self, type_rapport: str, type_notification: str) -> str:
        """Génère un rapport et l'envoie par email."""
        # Génération du rapport 
        if type_rapport == "pdf":
            rapport = RapportService().generer_pdf(self.inventaire)
        elif type_rapport == "csv":
            rapport = RapportService().generer_csv(self.inventaire)
        elif type_rapport == "html":
            rapport = RapportService().generer_html(self.inventaire)
        else:
            rapport = f"Rapport inventaire : {len(self.inventaire)} titres"

        # Envoie de la notification
        if type_notification == "email":
            self.notif_service.envoyer_email(
                "admin@biblio.local", "Rapport inventaire", rapport
            )
        elif type_notification == "sms":
            self.notif_service_sms.envoyer_sms(
                "1234567890", f"Rapport inventaire: {rapport}"
            )
        else:
            raise ValueError("Type de notification inconnu")
        return rapport

class Utilisateur:
    def __init__(self, nom: str, mail: str):
        self.nom = nom
        self.mail = mail

    def generer_rapport_disponibilite(self, inventaire: dict[str, int]) -> str:
        """Génère un rapport d'emprunts."""
        lignes = [f"{isbn}: {qte}" for isbn, qte in inventaire.items()]
        return "\n".join(lignes)


class GestionnaireEmprunt:
    def __init__(self):
        self.emprunts: list[tuple[str, str]] = []
        self.notif_service = NotificationServiceMail()

    def emprunter(self, utilisateur: Utilisateur, livre: Livre):
        # logique de vérification minimaliste
        self.emprunts.append((utilisateur.mail, livre.isbn))
        message = f"{utilisateur.nom} a emprunté '{livre.titre}'"
        self.notif_service.envoyer_email(
            utilisateur.mail, "Emprunt confirmé", message
        )

    def retourner(self, utilisateur: Utilisateur, livre: Livre):
        self.emprunts.remove((utilisateur.mail, livre.isbn))
        message = f"{utilisateur.nom} a retourné '{livre.titre}'"
        self.notif_service.envoyer_email(
            utilisateur.mail, "Retour confirmé", message
        )


class NotificationServiceMail:
    def envoyer_email(self, to: str, subject: str, body: str):
        # Logique d'envoi d'e-mail (mock)
        print(f"Envoi e‑mail à {to} : '{subject}' – {body}")

class NotificationServiceSMS(NotificationServiceMail):
    def envoyer_sms(self, number: str, message: str):
        # Logique d'envoi de SMS (mock)
        print(f"Envoi SMS à {number} : {message}")
    
    def envoyer_email(self, to: str, subject: str, body: str):
        raise NotImplementedError("Envoi d'e-mail non supporté par NotificationServiceSMS")

class RapportService:
    def generer_pdf(self, inventaire: dict[str, int]) -> str:
        # Génération de PDF, logique mélangée
        return f"PDF – {len(inventaire)} titres dans l'inventaire"

    def generer_csv(self, inventaire: dict[str, int]) -> str:
        # Génération de CSV et HTML dans la même classe
        lignes = [f"{isbn},{qte}" for isbn, qte in inventaire.items()]
        return "isbn,qte\n" + "\n".join(lignes)

    def generer_html(self, inventaire: dict[str, int]) -> str:
        rows = "".join(f"<tr><td>{isbn}</td><td>{qte}</td></tr>" for isbn, qte in inventaire.items())
        return f"<table>{rows}</table>"
