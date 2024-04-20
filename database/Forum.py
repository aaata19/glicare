class PostareForum:
    def __init__(self, id_postare, id_utilizator, titlu, text, data_postare, tip_postare, poza, utilizator, tip_utilizator, raspunsuri=None):
        self.id_postare = id_postare
        self.id_utilizator = id_utilizator
        self.titlu = titlu
        self.text = text
        self.data_postare = data_postare
        self.tip_postare = tip_postare
        self.poza = poza
        self.utilizator = utilizator
        self.tip_utilizator = tip_utilizator
        self.raspunsuri = []

    def toString(self):
        return f'{self.id_postare} {self.id_utilizator} {self.titlu} {self.text} {self.data_postare} {self.tip_postare} {self.poza} {self.utilizator} {self.tip_utilizator}'
    
class RaspunsForum:
    def __init__(self, id_raspuns, id_postare, id_utilizator, text, tip_postare, utilizator, tip_utilizator):
        self.id_raspuns = id_raspuns
        self.id_utilizator = id_utilizator
        self.id_postare = id_postare
        self.text = text
        self.utilizator = utilizator
        self.tip_utilizator = tip_utilizator
        self.tip_postare = tip_postare

    def toString(self):
        return f'{self.id_raspuns} {self.id_utilizator} {self.id_postare} {self.text} {self.utilizator} {self.tip_utilizator} {self.tip_postare}'
    

class Blog:
    def __init__(self, id_postare, titlu, text, data_postare, poza):
        self.id_postare = id_postare
        self.titlu = titlu
        self.text = text
        self.data_postare = data_postare
        self.poza = poza

    def toString(self):
        return f'{self.id_postare} {self.titlu} {self.text} {self.data_postare} {self.poza}'
    