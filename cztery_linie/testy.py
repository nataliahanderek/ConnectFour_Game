import unittest
from plansza import Plansza, KolumnaPrzepelniona
from reguly import *
from gra import WIERSZE, KOLUMNY

reguly = [Regula4Skos(), Regula4Poziom(), Regula4Pion()]


class PlanszaTesty(unittest.TestCase):
    #tworzenie planszy przed każdym testem
    def setUp(self):
        self.plansza = Plansza(kolumny=KOLUMNY, wiersze=WIERSZE, reguly=reguly)

    #wykonanie po dwa ruchy każdego z graczy
    def test_wrzucanie(self):
        kolumny = [2, 2, 3, 4]
        gracze = [1, 2, 1, 2]
        [self.plansza.wrzuc(gracz, kol) for kol, gracz in zip(kolumny, gracze)]
        self.assertEqual(self.plansza.plansza[5][2], 1)
        self.assertEqual(self.plansza.plansza[4][2], 2)
        self.assertEqual(self.plansza.plansza[5][3], 1)
        self.assertEqual(self.plansza.plansza[5][4], 2)

    #ulozenie pionowej linii kolek przez jednego gracza
    def test_pionowaLinia(self):
        [self.plansza.wrzuc(1, 0) for i in range(4)]
        self.assertEqual(self.plansza.wygrana(), 1)

    #ulozenie poziomej linii kolek przez jednego gracza
    def test_poziomaLinia(self):
        [self.plansza.wrzuc(2, i) for i in range(4)]
        self.assertEqual(self.plansza.wygrana(), 2)

    #ulozenie skosnej linii kolek przez jednego gracza
    def test_skosnaLinia(self):
        kolumny = [0, 1, 1, 2, 2, 3, 2, 3, 4, 3, 3]
        gracze =  [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
        [self.plansza.wrzuc(gracz, kol) for kol, gracz in zip(kolumny, gracze)]
        self.assertEqual(self.plansza.wygrana(), 1)

    #zapelnienie pola gry tak, aby byl remis
    def test_zapelnienie(self):
        self.plansza.reguly = [Regula4Pion()]
        for i in range(KOLUMNY):
            for j in range(3):
                self.plansza.wrzuc(1, i)
                self.plansza.wrzuc(2, i)

        self.assertTrue(self.plansza.remis())

    #ulozenie dluzszej lini niz 4 kolka
    def test_dluzszaLinia(self):
        kolumny = [0, 0, 1, 1, 2, 2, 4, 4, 5, 5, 6, 6, 3]
        gracze =  [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
        [self.plansza.wrzuc(gracz, kol) for kol, gracz in zip(kolumny, gracze)]
        self.assertEqual(self.plansza.wygrana(), 1)

    #wrzucenie kolek do zapelnionej kolumny
    def test_zapelnionaKolumna(self):
        kolumny = [0, 0, 0, 0, 0, 0]
        gracze =  [1, 2, 1, 2, 1, 2]
        [self.plansza.wrzuc(gracz, kol) for kol, gracz in zip(kolumny, gracze)]
        self.assertRaises(KolumnaPrzepelniona, lambda: self.plansza.wrzuc(1, 0))

#kod wykona sie tylko jesli uruchomimy ten plik (python test.py), zabepiecza przed urchomieniem kodu w przypadku importu tego pliku
if __name__ == '__main__':
    unittest.main()