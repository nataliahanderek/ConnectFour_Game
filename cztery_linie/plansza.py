class KolumnaPrzepelniona(Exception):
    pass


class NiepoprawnyNrKolumny(Exception):
    pass


class Plansza:
    def __init__(self, reguly, wiersze, kolumny):
        self.__wiersze = wiersze
        self.__kolumny = kolumny
        self.__reguly = reguly
        self.reset()

    # def oznacz(self, y, x, nr_gracza):
    #     if self.plansza[y][x] != 0:
    #         return False
    #     self.plansza[y][x] = nr_gracza
    #     return True

    @property
    def plansza(self):
        return self.__plansza

    @property
    def reguly(self):
        return self.__reguly

    @reguly.setter
    def reguly(self, noweReguly):
        self.__reguly = noweReguly

    def wrzuc(self, nrGracza, nrKolumny):
        if 0 > nrKolumny >= self.__kolumny:
            raise NiepoprawnyNrKolumny()

        index = len(self.__plansza) - 1
        for i in range(len(self.__plansza)):
            if self.__plansza[i][nrKolumny] != 0:
                index = i - 1
                break
        if index == -1:
            raise KolumnaPrzepelniona()

        self.__plansza[index][nrKolumny] = nrGracza

    def reset(self):
        # plansza[nr wiersza][nr kolumny]
        self.__plansza = [[0 for j in range(self.__kolumny)] for i in range(self.__wiersze)]

    def wygrana(self):
        for regula in self.__reguly:
            wynik = regula.ktoWygral(plansza=self.__plansza)
            if wynik is not None:
                return wynik

    def remis(self):
        for i in range(self.__wiersze):
            for j in range(self.__kolumny):
                if self.__plansza[i][j] == 0:
                    return False
        return True