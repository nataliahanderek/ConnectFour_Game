from reguly import Regula4Pion, Regula4Poziom, Regula4Skos
from plansza import Plansza, KolumnaPrzepelniona, NiepoprawnyNrKolumny
from tkinter import ttk, messagebox
from functools import partial
import tkinter

WIERSZE = 6
KOLUMNY = 7


class OknoGry():
    def __init__(self, srednica_kolka=40, margines=5, marginesX=17):
        reguly = [Regula4Skos(), Regula4Poziom(), Regula4Pion()]
        self.planszaDoGry = Plansza(reguly=reguly, wiersze=WIERSZE, kolumny=KOLUMNY)        #stworzenie obiektu logiki planszy
        self.srednica_kolka = srednica_kolka
        self.margines = margines
        self.marginesX = marginesX
        self.okno = tkinter.Tk()                                                            #stworzenie obiektu okna tkinter
        self.okno.geometry("430x350")                                                       #ustawienie rozmiaru okna
        self.okno.resizable(0, 0)                                                           #zablokowanie mozliwosci zmiany rozmiaru okna
        self.okno.configure(bg='black')                                                     #zmiana tla w oknie na czarny

        infoPanel = tkinter.Frame(self.okno, bg='black')                                    #utworzenie panelu przechowujacego informacje o stanie rozgrywki
        self.statusStr = tkinter.StringVar()                                                #zmienna przechowujaca informacje o stanie rozgrywki w formie tekstu
        status = tkinter.Label(infoPanel, textvariable=self.statusStr, bg='black', fg="white") #tworzenie elementu wyswietlajacego status gry
        status.grid(row=0, column=0, sticky='W', padx=10)                                   #ustawienie elemntu w panelu
        opisyRegul = ["Wszystkie"] + [str(regula) for regula in reguly]                     #stworzenie listy regul (w formie stringow)
        self.regulyCombobox = ttk.Combobox(infoPanel, width=20, values=opisyRegul, state='readonly') #utworzenie listy rozwijanej z opisami regul
        self.regulyCombobox.set("Wszystkie")                                                #ustawienie "Wszystkie" jako wartosci domyslnej w liscie rozwijanej
        self.regulyCombobox.grid(column=1, row=0, padx=10)                                  #ustawienie listy rozwijanej w panelu
        resetButton = tkinter.Button(infoPanel, text="Reset", command=self.reset, width=20) #utworzenie przycisku resetu rozgrywki
        resetButton.grid(row=0, column=2, sticky='E', padx=10)                              #ustawienie przycisku resetu w panelu
        infoPanel.pack()                                                                    #ustawienie panelu w okie glownym

        panel = tkinter.Frame(self.okno)                                                    #stworzenie panelu od przyciskow do wrzucania kolek
        #stworzenie przyciskow do wrzucania kolek i dodanie ich do panelu, partial - tworzy funkcje ktora zostanie powiazana z danym przyciskiem
        [tkinter.Button(panel, text=str(i+1), width=7, command=partial(self.przyciskKolumnyAkcja, i+1)).grid(column=i, row=0) for i in range(KOLUMNY)]
        panel.pack()                                                                        #ustawienie panelu w oknie glownym
        self.planszaCanvas = tkinter.Canvas(self.okno, bg="blue", width=410, height=270)    #tworzenie canvas do rysowania
        self.planszaCanvas.pack()                                                           #umieszczanie canvas w oknie

        self.reset()

    def sprawdzWygrana(self):
        wygrany = self.planszaDoGry.wygrana()
        if wygrany:
            self.statusStr.set(f"Wygrał gracz nr {wygrany}")
            messagebox.showinfo("Wygrana!", f"Wygrał gracz nr {wygrany}")
            self.rozgrywka = False
        elif self.planszaDoGry.remis():
            self.statusStr.set(f"Remis!")
            messagebox.showinfo("Remis!", f"Remis!")
            self.rozgrywka = False

    def przyciskKolumnyAkcja(self, nr):
        if not self.rozgrywka:
            return

        #wyjatek sprawdzajacy, czy kolumna jest juz zapelniona i czy mozna cos do niej wrzucic
        try:
            self.planszaDoGry.wrzuc(self.aktualnyGracz, nr - 1)
        except KolumnaPrzepelniona:
            tkinter.messagebox.showwarning(title="Błąd", message="Nie można nic ustawić w tej kolumnie.")
            return
        except NiepoprawnyNrKolumny:
            tkinter.messagebox.showwarning(title="Błąd", message="Nastąpił problem wewnętrzny 0x01 (zły nr kolumny).")
            return

        #sprawdzic reguly
        #oznaczyc drugiego gracza
        #odmalowac plansze
        self.aktualnyGracz = 1 if self.aktualnyGracz == 2 else 2
        self.statusStr.set(f"Tura gracza {self.aktualnyGracz}")
        self.malujPlansze()
        self.planszaCanvas.update()
        self.sprawdzWygrana()

    def malujPlansze(self):
        przesuniecie_y = 3
        kolory = ["white", "red", "yellow"]
        for y in range(len(self.planszaDoGry.plansza)):
            for x in range(len(self.planszaDoGry.plansza[y])):
                nrGracza = self.planszaDoGry.plansza[y][x]
                #rysuje kolko na planszy w kolorze w zaleznosci od nr gracza badz pola pustego, z okreslonymi odstepami miedzy kolkami
                self.planszaCanvas.create_oval(x*self.srednica_kolka+self.margines*x+self.marginesX*x,
                                               y*self.srednica_kolka+self.margines*y+przesuniecie_y,
                                               x*self.srednica_kolka+self.srednica_kolka+self.margines*x+self.marginesX*x,
                                               y*self.srednica_kolka+self.srednica_kolka+self.margines*y+przesuniecie_y,
                                               fill=kolory[nrGracza])

    #ustawienie poczatkowych wartosci nowej gry
    def reset(self):
        self.statusStr.set("Tura gracza 1")
        self.planszaDoGry.reset()
        self.malujPlansze()
        self.aktualnyGracz = 1
        self.rozgrywka = True
        self.ustawReguly()

    #pobiera z listy rozwijanej aktualna wartosc i na jej podstawie ustawia odpowiednie reguly w obiekcie logiki planszy
    def ustawReguly(self):
        opcja = self.regulyCombobox.get()
        reguly = [Regula4Skos(), Regula4Poziom(), Regula4Pion()]
        if opcja == "Wszystkie":
            self.planszaDoGry.reguly = reguly                       #ustawia wszystkie dostepne reguly
        else:
            #szuka reguly na podstawie ustawionej nazwy z listy rozwijanej
            reg = [regula for regula in reguly if str(regula) == opcja]
            if reg:
                self.planszaDoGry.reguly = reg

    def start(self):
        self.okno.mainloop()                                        #petla glowna tkinter
