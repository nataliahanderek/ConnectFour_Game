#wyjatki, gdy kolumna przepelniona i zly kod kolumny
class KolumnaPrzepelniona(Exception):
    pass


class NiepoprawnyNrKolumny(Exception):
    pass

#obsluga planszy
class Plansza:
    def __init__(self, reguly, wiersze, kolumny):
        self.__wiersze = wiersze
        self.__kolumny = kolumny
        self.__reguly = reguly
        self.reset()

    @property
    def plansza(self):
        return self.__plansza

    @property
    def reguly(self):
        return self.__reguly

    @reguly.setter
    def reguly(self, noweReguly):
        self.__reguly = noweReguly

    #obsluga wrzucanych kolek
    def wrzuc(self, nrGracza, nrKolumny):
        if 0 > nrKolumny >= self.__kolumny:
            raise NiepoprawnyNrKolumny()

        index = len(self.__plansza) - 1
        for i in range(len(self.__plansza)):
            if self.__plansza[i][nrKolumny] != 0:       #jesli natrafiono na komorke zapelniona
                index = i - 1                           #poprzedni indeks staje sie komorka do ktorej zostanie przypisane kolko
                break
        if index == -1:
            raise KolumnaPrzepelniona()

        self.__plansza[index][nrKolumny] = nrGracza

    #resetowanie planszy
    def reset(self):
        self.__plansza = [[0 for j in range(self.__kolumny)] for i in range(self.__wiersze)]

    #sprawdzenie kto wygral
    def wygrana(self):
        for regula in self.__reguly:
            wynik = regula.ktoWygral(plansza=self.__plansza)
            if wynik is not None:
                return wynik

    #sprawdzenie remisu przy zapelnieniu wszystkich pol
    def remis(self):
        for i in range(self.__wiersze):
            for j in range(self.__kolumny):
                if self.__plansza[i][j] == 0:
                    return False
        return True