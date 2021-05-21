class Plansza:
    def __init__(self, reguly, wiersze, kolumny):
        self.wiersze = wiersze
        self.kolumny = kolumny
        self.reguly = reguly
        self.reset()

    def oznacz(self, y, x, nr_gracza):
        if self.plansza[y][x] != 0:
            return False
        self.plansza[y][x] = nr_gracza
        return True

    def reset(self):
        # plansza[nr wiersza][nr kolumny]
        self.plansza = [[0 for j in range(self.kolumny)] for i in range(self.wiersze)]

    def wygrana(self):
        for regula in self.reguly:
            wynik = regula.ktoWygral(plansza=self.plansza)
            if wynik != 0:
                return wynik