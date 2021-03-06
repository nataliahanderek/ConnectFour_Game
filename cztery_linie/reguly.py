class Regula:
    def ktoWygral(self, plansza):
        pass

#regula sprawdzajaca czy gracz ulozyl cztery kolka w pionie
class Regula4Pion(Regula):
    def ktoWygral(self, plansza):
        for i in range(len(plansza[0])):
            ilosc = 0
            aktualny = None
            for j in range(len(plansza)):
                if plansza[j][i] != 0:
                    if plansza[j][i] != aktualny:
                        ilosc = 1
                        aktualny = plansza[j][i]
                    else:
                        ilosc += 1
                        if ilosc == 4:
                            return plansza[j][i]
                else:
                    ilosc = 0
                    aktualny = 0

    def __str__(self):
        return "4 kolka w pionie"


#regula sprawdzajaca czy gracz ulozyl cztery kolka w poziomie
class Regula4Poziom(Regula):
    def ktoWygral(self, plansza):
        for j in range(len(plansza)):
            ilosc = 0
            aktualny = None
            for i in range(len(plansza[j])):
                if plansza[j][i] != 0:
                    if plansza[j][i] != aktualny:
                        ilosc = 1
                        aktualny = plansza[j][i]
                    else:
                        ilosc += 1
                        if ilosc == 4:
                            return plansza[j][i]
                else:
                    ilosc = 0
                    aktualny = 0

    def __str__(self):
        return "4 kolka w poziomie"


#regula sprawdzajaca czy gracz ulozyl cztery kolka na skos
class Regula4Skos(Regula):
    #skos z lewej do prawej
    def skosLewoPrawo(self, i, j, plansza):
        ki = i
        kj = j
        ilosc = 0
        aktualny = None
        while ki < len(plansza) and kj < len(plansza[i]):
            if plansza[ki][kj] != 0:
                if plansza[ki][kj] != aktualny:
                    aktualny = plansza[ki][kj]
                    ilosc = 1
                else:
                    ilosc += 1
                    if ilosc == 4:
                        return plansza[ki][kj]
            else:
                ilosc = 0
                aktualny = 0
            ki += 1
            kj += 1

    #skos z prawej do lewej
    def skosPrawoLewo(self, i, j, plansza):
        ki = i
        kj = j
        ilosc = 0
        aktualny = None
        while ki < len(plansza) and kj < len(plansza[i]):
            if plansza[ki][kj] != 0:
                if plansza[ki][kj] != aktualny:
                    aktualny = plansza[ki][kj]
                    ilosc = 1
                else:
                    ilosc += 1
                    if ilosc == 4:
                        return plansza[ki][kj]
            else:
                ilosc = 0
                aktualny = 0

            ki += 1
            kj -= 1

    def ktoWygral(self, plansza):
        for i in range(len(plansza)):
            for j in range(len(plansza[i])):
                wynik = self.skosLewoPrawo(i, j, plansza)
                if wynik in [1, 2]:
                    return wynik
                wynik = self.skosPrawoLewo(i, j, plansza)
                if wynik in [1, 2]:
                    return wynik

    def __str__(self):
        return "4 kolka na skos"