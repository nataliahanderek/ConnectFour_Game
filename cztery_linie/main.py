from reguly import Regula4Pion, Regula4Poziom, Regula4Skos
from plansza import Plansza
from tkinter import ttk
import tkinter

WIERSZE = 6
KOLUMNY = 7

class OknoGry():
    def __init__(self, srednica_kolka=40, margines=5):
        reguly = [Regula4Skos(), Regula4Poziom(), Regula4Pion()]
        self.planszaDoGry = Plansza(reguly=reguly, wiersze=WIERSZE, kolumny=KOLUMNY)
        self.srednica_kolka = srednica_kolka
        self.margines = margines
        self.okno = tkinter.Tk()


        opisyRegul = ["Wszystkie"] + [str(regula) for regula in reguly]
        panel = tkinter.Frame(self.okno)
        ttk.Combobox(panel, width=10, values=opisyRegul, state='readonly').grid(column=KOLUMNY+1, row=0)
        for i in range(KOLUMNY):
            tkinter.Button(panel, text=str(i+1), width=7).grid(column=i, row=0)
        panel.pack()

        self.planszaCanvas = tkinter.Canvas(self.okno, bg="blue")  # tworzymy canvas do rysowania
        self.planszaCanvas.pack()  # umieszczamy canvas w oknie


        self.malujPlansze()

    def malujPlansze(self):
        przesuniecie_y = 0#30
        for y in range(len(self.planszaDoGry.plansza)):
            for x in range(len(self.planszaDoGry.plansza[y])):
                self.planszaCanvas.create_oval(x*self.srednica_kolka+self.margines*x,
                                               y*self.srednica_kolka+self.margines*y+przesuniecie_y,
                                               x*self.srednica_kolka+self.srednica_kolka+self.margines*x,
                                               y*self.srednica_kolka+self.srednica_kolka+self.margines*y+przesuniecie_y,
                                               fill="white")

    def start(self):
        self.okno.mainloop()





okno = OknoGry()
okno.start()