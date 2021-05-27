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
        self.planszaDoGry = Plansza(reguly=reguly, wiersze=WIERSZE, kolumny=KOLUMNY)
        self.srednica_kolka = srednica_kolka
        self.margines = margines
        self.marginesX = marginesX
        self.okno = tkinter.Tk()
        self.okno.geometry("430x350")
        self.okno.resizable(0, 0)
        self.okno.configure(bg='black')

        infoPanel = tkinter.Frame(self.okno, bg='black')
        self.statusStr = tkinter.StringVar()
        status = tkinter.Label(infoPanel, textvariable=self.statusStr, bg='black', fg="white")
        status.grid(row=0, column=0, sticky='W', padx=10)
        opisyRegul = ["Wszystkie"] + [str(regula) for regula in reguly]
        self.regulyCombobox = ttk.Combobox(infoPanel, width=20, values=opisyRegul, state='readonly')
        self.regulyCombobox.set("Wszystkie")
        self.regulyCombobox.grid(column=1, row=0, padx=10)
        resetButton = tkinter.Button(infoPanel, text="Reset", command=self.reset, width=20)
        resetButton.grid(row=0, column=2, sticky='E', padx=10)
        infoPanel.pack()

        panel = tkinter.Frame(self.okno)
        [tkinter.Button(panel, text=str(i+1), width=7, command=partial(self.przyciskKolumnyAkcja, i+1)).grid(column=i, row=0) for i in range(KOLUMNY)]
        panel.pack()
        self.planszaCanvas = tkinter.Canvas(self.okno, bg="blue", width=410, height=270)  # tworzymy canvas do rysowania
        self.planszaCanvas.pack()  # umieszczamy canvas w oknie

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
        przesuniecie_y = 3#30
        kolory = ["white", "red", "yellow"]
        for y in range(len(self.planszaDoGry.plansza)):
            for x in range(len(self.planszaDoGry.plansza[y])):
                nrGracza = self.planszaDoGry.plansza[y][x]
                self.planszaCanvas.create_oval(x*self.srednica_kolka+self.margines*x+self.marginesX*x,
                                               y*self.srednica_kolka+self.margines*y+przesuniecie_y,
                                               x*self.srednica_kolka+self.srednica_kolka+self.margines*x+self.marginesX*x,
                                               y*self.srednica_kolka+self.srednica_kolka+self.margines*y+przesuniecie_y,
                                               fill=kolory[nrGracza])

    def reset(self):
        self.statusStr.set("Tura gracza 1")
        self.planszaDoGry.reset()
        self.malujPlansze()
        self.aktualnyGracz = 1
        self.rozgrywka = True
        self.ustawReguly()

    def ustawReguly(self):
        opcja = self.regulyCombobox.get()
        reguly = [Regula4Skos(), Regula4Poziom(), Regula4Pion()]
        if opcja == "Wszystkie":
            self.planszaDoGry.reguly = reguly
        else:
            reg = [regula for regula in reguly if str(regula) == opcja]
            if reg:
                self.planszaDoGry.reguly = reg

    def start(self):
        self.okno.mainloop()
