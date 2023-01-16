"""----------ELOKUVATEATTERIN-VARAUSJÄRJESTELMÄ----------"""
# AUTHOR: Jere Leman
# DATE: 12/16/2021

import tkinter as tk   # Graafinen käyttöliittymä
from tkinter import ttk, simpledialog, messagebox  # Tyylit ja ilmoitukset
from tkinter import *
import uuid  # Uniikkeja varausnumeroita varten
import json  # JSON tiedoston ksäittelyä varten
import csv  # CSV tiedoston ksäittelyä varten


# noinspection PyGlobalUndefined
# noinspection PyBroadException
class Valikko:
    def __init__(self, root):
        """Pääkäyttöliittymä sovellukselle"""
        self.root = root
        self.root.geometry("1000x500")
        self.root.resizable(width=False, height=False)

        # Tyylit: Valikko
        self.root["bg"] = "#282828"
        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.style.configure("TLabel", font=("Calibri", 18), background="#282828", foreground="#ffffff")
        self.style.configure("TButton", font=("Calibri", 15), background="#0c0032", foreground="#ffffff",
                             width=70, relief="SUNKEN")
        self.style.map("TButton", background=[('active', "#190061")], relief="SUNKEN")

        # Tyylit: Varausjärjestelmä
        self.style.configure("Treeview", background="silver", foreground="#ffffff", rowheight=25)
        self.style.map("Treeview", background=[("active", "#190061")])

        self.style.configure('Treeview.Heading', background="#0c0032", foreground='#ffffff', relief="SUNKEN",
                             rowheight=15)
        self.style.map("Treeview.Heading", background=[("active", "#190061")])

        self.style.configure("vpPainike.TButton", font=("Calibri", 10), background="silver",
                            foreground="#ffffff", width=25, relief="SUNKEN")
        self.style.configure("vpPoistoPainike.TButton", font=("Calibri", 10), background="silver",
                            foreground="#ffffff", width=25, relief="SUNKEN")

        self.style.map("vpPainike.TButton", background=[('active', "green")], relief="SUNKEN")
        self.style.map("vpPoistoPainike.TButton", background=[('active', "red")], relief="SUNKEN")

        self.style.configure("yllapito.TButton", font=("Calibri", 15), background="silver",
                           foreground="#ffffff", width=50, relief="SUNKEN")
        self.style.map("yllapito.TButton", background=[('active', "orange")], relief="SUNKEN")

        self.style.configure("yllapito1.TButton", font=("Calibri", 15), background="silver",
                            foreground="#ffffff", width=50, relief="SUNKEN")
        self.style.map("yllapito1.TButton", background=[('active', "red")], relief="SUNKEN")

        # Otsikko
        self.otsikko = ttk.Label(self.root, text="Tervetuloa elokuvateatterin järjestelmään!").pack(side=TOP, expand=1)

        # Painikkeet
        self.varausPainike = ttk.Button(self.root, text="Varausjärjestelmään", command=lambda: self.siirtyminen(Varaus))
        self.yllapitoPainike = ttk.Button(self.root, text="Ylläpito", command=lambda: self.siirtyminen(Login))
        self.sulkuPainike = ttk.Button(self.root, text="Poistu ohjelmasta", command=self.lopetus)

        self.varausPainike.pack(side=TOP, expand=1, fill=tk.NONE)
        self.yllapitoPainike.pack(side=TOP, expand=1, fill=tk.NONE)
        self.sulkuPainike.pack(side=TOP, expand=1, fill=tk.NONE)

        # Footer
        self.tekijanoikeus = ttk.Label(self.root, text="Elokuvateatteri V1.0.0").pack(side=BOTTOM, expand=1)

    def lopetus(self):
        self.root.destroy()

    # Siirry toiseen ikkunaan ja rajoita yhteen ikkunaan
    def siirtyminen(self, _class):
        try:
            if self.uusi.state() == "":   # Onko ikkunaa olemassa
                self.uusi.focus()
        except:
            self.uusi = tk.Toplevel(self.root)
            _class(self.uusi)


# noinspection PyGlobalUndefined
# noinspection PyBroadException
class Login:
    """Loginliittymä sovellukselle"""
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#282828"
        global message, kayttajatunnus, salasana
        kayttajatunnus, salasana, message = StringVar(), StringVar(), StringVar()

        # Otsikko
        self.otsikko1 = ttk.Label(self.root, text="Kirjautuminen").pack(side=TOP, pady=30)

        self.otsikko2 = ttk.Label(self.root, text="Kayttajatunnus").pack()
        self.kt_syotto = ttk.Entry(self.root, textvariable=kayttajatunnus).pack()

        self.otsikko3 = ttk.Label(self.root, text="Salasana").pack()
        self.ss_syotto = ttk.Entry(self.root, textvariable=salasana, show="*").pack()

        self.viesti = ttk.Label(self.root, text="", textvariable=message).pack()

        self.kirjaudu_painike = ttk.Button(self.root, text="Kirjaudu", command=self.login, style="vpPainike.TButton")
        self.kirjaudu_painike.place(x=500, y=300, anchor=CENTER)

    # Funktio kirjautumisen tarkistamista varten
    def login(self):
        kt = kayttajatunnus.get()
        ss = salasana.get()
        if kt == '' or ss == '':
            message.set("Kentät ovat tyhjiä!")
        elif kt == ktun and ss == ssan:  # KTSAN JA SSAN tiedot jsonista eli salasana muokattavissa
            self.siirtyminen1(Admin)
            message.set("Kirjautuminen onnistui!")
        else:
            message.set("Väärä käyttäjätunnus tai salasana!")

    def siirtyminen1(self, _class):
        try:
            if self.uusi.state() == "":  # Onko ikkunaa olemassa
                self.uusi.focus()
        except:
            self.uusi = tk.Toplevel(self.root)
            _class(self.uusi)


# noinspection PyGlobalUndefined
# noinspection PyBroadException
class Varaus:
    """Varausjärjestelmän käyttöliittymä"""
    def __init__(self, root):
        varauslaskuri()
        self.root = root
        self.root.geometry("1000x600")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#282828"

        # Otsikko ja ohjeet
        self.otsikko = ttk.Label(self.root, text="Varausjärjestelmä").pack(side=TOP, pady=30)
        self.otsikko1 = ttk.Label(self.root, text="1. Valitse elokuva ja paina varaa"
                                                  "\n2. Täytä tiedot ja paina varmista varaus").pack(side=TOP, pady=10)

        # Puun luominen
        self.tree = ttk.Treeview(self.root, columns=("Elokuva", "Sali", "Aika", "Paikat"), show="headings", height=10)

        # Sarkakkeet
        self.tree.column("#0", width=0, stretch=NO, anchor=CENTER)
        self.tree.column("#1", width=200, anchor=CENTER)
        self.tree.column("#2", width=200, anchor=CENTER)
        self.tree.column("#3", width=200, anchor=CENTER)
        self.tree.column("#4", width=200, anchor=CENTER)

        # Otsikot
        self.tree.heading("#1", text="Elokuva")
        self.tree.heading("#2", text="Sali")
        self.tree.heading("#3", text="Aika")
        self.tree.heading("#4", text="Paikat")
        self.tree.pack()

        self.varaa_peru_painike = ttk.Button(self.root, text="Varaa/peru paikka",
                       command=lambda: self.siirtyminen2(Varauskysely), style="TButton")
        self.varaa_peru_painike.place(x=500, y=500, anchor=CENTER)

        # Avataan elokuvat tiedosto ja luetaan tiedot varausikkunaa varten
        with open("elokuvat.csv") as tiedosto:
            reader = csv.reader(tiedosto)
            rivi = 0
            vm = 0
            max_p = 0
            for row in reader:
                # Try välittää vain riveistä, jossa tietoa ja lukee ne varausikkunaan järjestyksessä
                # elokuvat.csv:ssä voi siis olla välejä, jos esityksiä ei ole määritettyinä aikoina
                try:
                    if row[1] == eka_sali and row[2] == eka_naytos:
                        max_p = eka_sali_paikat
                        vm = varausten_maara1

                    elif row[1] == toka_sali and row[2] == eka_naytos:
                        max_p = toka_sali_paikat
                        vm = varausten_maara2

                    elif row[1] == kolmas_sali and row[2] == eka_naytos:
                        max_p = kolmas_sali_paikat
                        vm = varausten_maara3

                    elif row[1] == eka_sali and row[2] == toka_naytos:
                        max_p = eka_sali_paikat
                        vm = varausten_maara4

                    elif row[1] == toka_sali and row[2] == toka_naytos:
                        max_p = toka_sali_paikat
                        vm = varausten_maara5

                    elif row[1] == kolmas_sali and row[2] == toka_naytos:
                        max_p = kolmas_sali_paikat
                        vm = varausten_maara6

                    elif row[1] == eka_sali and row[2] == kolmas_naytos:
                        max_p = eka_sali_paikat
                        vm = varausten_maara7

                    elif row[1] == toka_sali and row[2] == kolmas_naytos:
                        max_p = toka_sali_paikat
                        vm = varausten_maara8

                    elif row[1] == kolmas_sali and row[2] == kolmas_naytos:
                        max_p = kolmas_sali_paikat
                        vm = varausten_maara9

                    elif row[1] == eka_sali and row[2] == neljas_naytos:
                        max_p = eka_sali_paikat
                        vm = varausten_maara10

                    elif row[1] == toka_sali and row[2] == neljas_naytos:
                        max_p = toka_sali_paikat
                        vm = varausten_maara11

                    elif row[1] == kolmas_sali and row[2] == neljas_naytos:
                        max_p = kolmas_sali_paikat
                        vm = varausten_maara12

                    elif row[1] == eka_sali and row[2] == viides_naytos:
                        max_p = eka_sali_paikat
                        vm = varausten_maara13

                    elif row[1] == toka_sali and row[2] == viides_naytos:
                        max_p = toka_sali_paikat
                        vm = varausten_maara14

                    elif row[1] == kolmas_sali and row[2] == viides_naytos:
                        max_p = kolmas_sali_paikat
                        vm = varausten_maara15
                    rivi += 1
                    self.tree.insert("", 'end', iid=rivi, values=(row[0], row[1], row[2], str(vm) + "/" + str(max_p)))
                # Jos CSV-rivi tyhjä ohita
                except:
                    pass
        tiedosto.close()

        # Funtio käyttäjän valitsemaa tietoa varten --> siirtyy varauksen tietoihin
        def valinta(tapahtuma):
            global elokuva, aika, sali

            for valittu_rivi in self.tree.selection():
                puu_rivi = self.tree.item(valittu_rivi)
                elokuva = puu_rivi["values"][0]
                sali = puu_rivi["values"][1]
                aika = puu_rivi["values"][2]
        self.tree.bind('<<TreeviewSelect>>', valinta)

    def siirtyminen2(self, _class):
        try:
            if self.uusi.state() == "":  # Onko ikkunaa olemassa
                self.uusi.focus()
        except:
            self.uusi = tk.Toplevel(self.root)
            _class(self.uusi)


# noinspection PyGlobalUndefined
# noinspection PyBroadException
class Varauskysely:
    """varausliittymä sovellukselle"""
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#282828"

        global message, etunimi, sukunimi, numero, idnumero
        etunimi, sukunimi, numero, message, idnumero = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

        # Otsikko
        self.otsikko4 = ttk.Label(self.root, text="Varaa paikka").place(x=100, y=30)
        self.otsikko5 = ttk.Label(self.root, text="Peru paikka").place(x=750, y=30)

        # Varauksen tiedot
        self.e_otsikko = ttk.Label(self.root, text="Etunimi").place(x=110, y=100)
        self.e_syotto = ttk.Entry(self.root, textvariable=etunimi).place(x=100, y=130)

        self.s_otsikko = ttk.Label(self.root, text="Sukunimi").place(x=110, y=160)
        self.s_syotto = ttk.Entry(self.root, textvariable=sukunimi).place(x=100, y=190)

        self.p_otsikko = ttk.Label(self.root, text="Puhelinnumero").place(x=90, y=220)

        self.p_syotto = ttk.Entry(self.root, textvariable=numero).place(x=100, y=250)

        self.viesti2 = ttk.Label(self.root, text="", textvariable=message).place(x=300, y=100)

        # Varauksen varmistus
        self.varauksen_varmistus = ttk.Button(self.root, text="Varmista varaus",
                                              command=varaa, style="vpPainike.TButton")
        self.varauksen_varmistus.place(x=160, y=300, anchor=CENTER)

        # Varauksen poisto
        self.poisto_otsikko = ttk.Label(self.root, text="Varausnumero").place(x=735, y=100)
        self.poisto_syotto = ttk.Entry(self.root, textvariable=idnumero).place(x=750, y=130)

        self.poistamis_painike = ttk.Button(self.root, text="Poista varaus", command=poista_tiedostosta,
                                       style="vpPoistoPainike.TButton").place(x=720, y=160)


def varauslaskuri():
    global varausten_maara1, varausten_maara2, varausten_maara3, varausten_maara4, varausten_maara5, varausten_maara6, \
        varausten_maara7, varausten_maara8, varausten_maara9, varausten_maara10, varausten_maara11, varausten_maara12, \
        varausten_maara13, varausten_maara14, varausten_maara15

    varausten_maara1, varausten_maara2, varausten_maara3, varausten_maara4, varausten_maara5 = 0, 0, 0, 0, 0
    varausten_maara6, varausten_maara7, varausten_maara8, varausten_maara9, varausten_maara10 = 0, 0, 0, 0, 0
    varausten_maara11, varausten_maara12, varausten_maara13, varausten_maara14, varausten_maara15 = 0, 0, 0, 0, 0

    with open('varaukset.json', "r") as tiedosto:
        data = json.load(tiedosto)
        tiedosto.close()

    for alkio in data['varaukset']:
        # Eka aika
        if alkio["Aika"] == eka_naytos and alkio["Sali"] == eka_sali:
            varausten_maara1 += 1
        elif alkio["Aika"] == eka_naytos and alkio["Sali"] == toka_sali:
            varausten_maara2 += 1
        elif alkio["Aika"] == eka_naytos and alkio["Sali"] == kolmas_sali:
            varausten_maara3 += 1

        # Toka aika
        elif alkio["Aika"] == toka_naytos and alkio["Sali"] == eka_sali:
            varausten_maara4 += 1
        elif alkio["Aika"] == toka_naytos and alkio["Sali"] == toka_sali:
            varausten_maara5 += 1
        elif alkio["Aika"] == toka_naytos and alkio["Sali"] == kolmas_sali:
            varausten_maara6 += 1

        # Kolmas aika
        elif alkio["Aika"] == kolmas_naytos and alkio["Sali"] == eka_sali:
            varausten_maara7 += 1
        elif alkio["Aika"] == kolmas_naytos and alkio["Sali"] == toka_sali:
            varausten_maara8 += 1
        elif alkio["Aika"] == kolmas_naytos and alkio["Sali"] == kolmas_sali:
            varausten_maara9 += 1

        # Neljäs aika
        elif alkio["Aika"] == neljas_naytos and alkio["Sali"] == eka_sali:
            varausten_maara10 += 1
        elif alkio["Aika"] == neljas_naytos and alkio["Sali"] == toka_sali:
            varausten_maara11 += 1
        elif alkio["Aika"] == neljas_naytos and alkio["Sali"] == kolmas_sali:
            varausten_maara12 += 1

        # Viides aika
        elif alkio["Aika"] == viides_naytos and alkio["Sali"] == eka_sali:
            varausten_maara13 += 1
        elif alkio["Aika"] == viides_naytos and alkio["Sali"] == toka_sali:
            varausten_maara14 += 1
        elif alkio["Aika"] == viides_naytos and alkio["Sali"] == kolmas_sali:
            varausten_maara15 += 1


# noinspection PyGlobalUndefined
# noinspection PyBroadException
class Admin:
    """Ylläpitäjänliittymä sovellukselle"""
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x500")
        self.root.resizable(width=False, height=False)
        self.root["bg"] = "#282828"

        # Otsikko
        self.otsikko = ttk.Label(self.root, text="Ylläpito").pack(side=TOP, pady=30)

        # Painikkeet ja toiminnot
        self.katso_varaukset = ttk.Button(self.root, text="Katso varaukset", command=nayta_varaukset,
                   style="yllapito.TButton").pack(side=TOP, expand=1, fill=tk.NONE)

        self.lisaa_elokuva = ttk.Button(self.root, text="Lisää Elokuva", command=lisaa_ekuva,
                   style="yllapito.TButton").pack(side=TOP, expand=1, fill=tk.NONE)

        self.poista_elokuva = ttk.Button(self.root, text="Poista elokuva", command=poista_ekuva,
                   style="yllapito.TButton").pack(side=TOP, expand=1, fill=tk.NONE)

        self.poista_varaukset = ttk.Button(self.root, text="Poista varaukset", command=poista_varaukset,
                   style="yllapito1.TButton").pack(side=TOP, expand=1, fill=tk.NONE)

        self.resetoi = ttk.Button(self.root, text="Resetoi ohjelma oletusasetuksille", command=resetoi,
                   style="yllapito1.TButton").pack(side=TOP, expand=1, fill=tk.NONE)


# Funktio elokuvien lisäämistä varten
# noinspection PyBroadException
def lisaa_ekuva():
    global indeksi
    v1 = simpledialog.askstring("Syöte", f"Lisättävä elokuva? \nHUOM! Yliajaa elokuvan ja sen varaukset "
                                         f"samassa kohdassa!", parent=root)
    v2 = simpledialog.askinteger("Syöte", f"Sali? \n 1. {eka_sali} \n 2. {toka_sali} \n 3. {kolmas_sali}", parent=root,
                                 minvalue=1, maxvalue=3)
    v3 = simpledialog.askinteger("Syöte", f"Aika? \n 1. {eka_naytos} \n 2. {toka_naytos} \n "
                                          f"3. {kolmas_naytos} \n 4. {neljas_naytos} \n "
                                          f"5. {viides_naytos}", parent=root, minvalue=1, maxvalue=5)

    if v2 == 1: v2 = eka_sali
    elif v2 == 2: v2 = toka_sali
    elif v2 == 3: v2 = kolmas_sali

    if v3 == 1: v3 = eka_naytos
    elif v3 == 2: v3 = toka_naytos
    elif v3 == 3: v3 = kolmas_naytos
    elif v3 == 4: v3 = neljas_naytos
    elif v3 == 5: v3 = viides_naytos

    try:
        lista = [v1, v2, v3]
        d = (lista[0]+","+lista[1]+","+lista[2])

        if v2 == eka_sali and v3 == eka_naytos: indeksi = 0
        elif v2 == toka_sali and v3 == eka_naytos: indeksi = 1
        elif v2 == kolmas_sali and v3 == eka_naytos: indeksi = 2

        elif v2 == eka_sali and v3 == toka_naytos: indeksi = 3
        elif v2 == toka_sali and v3 == toka_naytos: indeksi = 4
        elif v2 == kolmas_sali and v3 == toka_naytos: indeksi = 5

        elif v2 == eka_sali and v3 == kolmas_naytos: indeksi = 6
        elif v2 == toka_sali and v3 == kolmas_naytos: indeksi = 7
        elif v2 == kolmas_sali and v3 == kolmas_naytos: indeksi = 8

        elif v2 == eka_sali and v3 == neljas_naytos: indeksi = 9
        elif v2 == toka_sali and v3 == neljas_naytos: indeksi = 10
        elif v2 == kolmas_sali and v3 == neljas_naytos: indeksi = 11

        elif v2 == eka_sali and v3 == viides_naytos: indeksi = 12
        elif v2 == toka_sali and v3 == viides_naytos: indeksi = 13
        elif v2 == kolmas_sali and v3 == viides_naytos: indeksi = 14

        # Elokuvien lisääminen
        if len(v1) > 0:
            with open('elokuvat.csv', 'r+') as tiedosto:
                data = tiedosto.readlines()
                # Jos tiedosto ei ole tyhjä niin lisätään uusi data vain indeksin kohdalle
                if data:
                    data.insert(indeksi, d + '\n')
                    x = data[indeksi+1]
                    data.remove(x)
                    tiedosto.seek(0)
                    tiedosto.truncate()
                    for y in data:
                        tiedosto.write(y)

                # Jos tiedosto on tyhjä niin lisätään eka rivi ja luodaan indeksit (tyhjat rivit)
                # joihin voidaan kirjoittaa vähän "hack"-menetelmä mutta toimii :)
                elif not data:
                    data.insert(indeksi, d + '\n')
                    tiedosto.seek(0)
                    tiedosto.truncate()
                    for y in data:
                        tiedosto.write(y)
                        tiedosto.write('\n''\n''\n''\n''\n''\n''\n''\n''\n''\n''\n''\n''\n''\n')
            tiedosto.close()

            with open("varaukset.json", "r+") as tiedosto1:
                data = json.load(tiedosto1)
                tiedosto1.close()

                # Jos aika ja sali täsmää poista varaukset siltä näytökseltä
                # Eli jos uusi elokuva yliajaa vanhan elokuvan, jossa oli varauksia niin varaukset poistetaan
                filteroitu_data = list(filter(lambda o: o["Sali"] != lista[1] or o['Aika'] != lista[2],
                                              data["varaukset"]))

            # Kirjoitetaan data takaisin tiedostoon
            with open("varaukset.json", "w") as tiedosto2:
                data = {"varaukset": filteroitu_data}
                json.dump(data, tiedosto2, indent=4)
                tiedosto2.close()
        else:
            messagebox.showinfo("HUOM!", "Kentät/kenttä tyhjänä, mitään ei lisätty!")
    except:
        messagebox.showinfo("Virhe!", "Et lisännyt mitään!")


# Funktio elokuvien poistoa varten
def poista_ekuva():
    v1 = simpledialog.askstring("Syöte", f"Poistettava elokuva? \n HUOM! Poistaa myös varaukset kyseiseltä elokuvalta!",
                                parent=root)
    v2 = simpledialog.askinteger("Syöte", f"Sali? \n 1. {eka_sali} \n 2. {toka_sali} \n 3. {kolmas_sali}", parent=root,
                                 minvalue=1, maxvalue=3)
    v3 = simpledialog.askinteger("Syöte", f"Aika? \n 1. {eka_naytos} \n 2. {toka_naytos} \n "
                                          f"3. {kolmas_naytos} \n 4. {neljas_naytos} \n "
                                          f"5. {viides_naytos}", parent=root, minvalue=1, maxvalue=5)
    if v2 == 1: v2 = eka_sali
    elif v2 == 2: v2 = toka_sali
    elif v2 == 3: v2 = kolmas_sali

    if v3 == 1: v3 = eka_naytos
    elif v3 == 2: v3 = toka_naytos
    elif v3 == 3: v3 = kolmas_naytos
    elif v3 == 4: v3 = neljas_naytos
    elif v3 == 5: v3 = viides_naytos

    try:
        lista = [v1, v2, v3]
        rivit = list()

        # Jos saatiin elokuva a1-kenttään --> Avataan tiedosto ja poistetaan tiedostosta elokuva
        # (jos aika ja sali täsmää)
        if len(v1) > 0:
            with open("elokuvat.csv") as tiedosto:
                reader = csv.reader(tiedosto)
                for row in reader:
                    rivit.append(row)
                    if row == lista:
                        rivit.remove(row)
                tiedosto.close()

            with open("elokuvat.csv", "w", newline='') as tiedosto3:
                kirjoita = csv.writer(tiedosto3)
                kirjoita.writerows(rivit)
                tiedosto3.close()

            with open("varaukset.json", "r+") as tiedosto4:
                data = json.load(tiedosto4)
                tiedosto4.close()
                # Jos elokuva poistetaan --> poistetaan varaukset myös kyseiseltä  elokuvalta
                filteroitu_data = list(filter(lambda o: o["Sali"] != lista[1] or o['Aika'] != lista[2],
                                              data["varaukset"]))

            # Kirjoitetaan data takaisin tiedostoon
            with open("varaukset.json", "w") as tiedosto4:
                data = {"varaukset": filteroitu_data}
                json.dump(data, tiedosto4, indent=4)
                tiedosto4.close()
        else:
            messagebox.showinfo("HUOM!", "Kentät/kenttä tyhjänä, mitään ei lisätty!")
    except:
        messagebox.showinfo("Virhe!", "Et lisännyt mitään!")


def varaa():
    varauslaskuri()  # Kutsutaan varauslaskuria
    enimi = etunimi.get()
    snimi = sukunimi.get()
    numer = numero.get()
    varausten_maara = 0
    max_paikat = 0

    # Jos täsmää niin varausten_maara == varauslaskuri():sta saatu arvo
    try:
        # Eka aika
        if aika == eka_naytos and sali == eka_sali:
            varausten_maara = varausten_maara1
            max_paikat = eka_sali_paikat
        elif aika == eka_naytos and sali == toka_sali:
            varausten_maara = varausten_maara2
            max_paikat = toka_sali_paikat
        elif aika == eka_naytos and sali == kolmas_sali:
            varausten_maara = varausten_maara3
            max_paikat = kolmas_sali_paikat

        # Toka aika
        elif aika == toka_naytos and sali == eka_sali:
            varausten_maara = varausten_maara4
            max_paikat = eka_sali_paikat
        elif aika == toka_naytos and sali == toka_sali:
            varausten_maara = varausten_maara5
            max_paikat = toka_sali_paikat
        elif aika == toka_naytos and sali == kolmas_sali:
            varausten_maara = varausten_maara6
            max_paikat = kolmas_sali_paikat

        # Kolmas aika
        elif aika == kolmas_naytos and sali == eka_sali:
            varausten_maara = varausten_maara7
            max_paikat = eka_sali_paikat
        elif aika == kolmas_naytos and sali == toka_sali:
            varausten_maara = varausten_maara8
            max_paikat = toka_sali_paikat
        elif aika == kolmas_naytos and sali == kolmas_sali:
            varausten_maara = varausten_maara9
            max_paikat = kolmas_sali_paikat

        # Neljäs aika
        elif aika == neljas_naytos and sali == eka_sali:
            varausten_maara = varausten_maara10
            max_paikat = eka_sali_paikat
        elif aika == neljas_naytos and sali == toka_sali:
            varausten_maara = varausten_maara11
            max_paikat = toka_sali_paikat
        elif aika == neljas_naytos and sali == kolmas_sali:
            varausten_maara = varausten_maara12
            max_paikat = kolmas_sali_paikat

        # Viides aika
        elif aika == viides_naytos and sali == eka_sali:
            varausten_maara = varausten_maara13
            max_paikat = eka_sali_paikat
        elif aika == viides_naytos and sali == toka_sali:
            varausten_maara = varausten_maara14
            max_paikat = toka_sali_paikat
        elif aika == viides_naytos and sali == kolmas_sali:
            varausten_maara = varausten_maara15
            max_paikat = kolmas_sali_paikat

        # Tyhjän varauksen ja uniikin id:n luominen (Lyhenntty 8 merkkiin, koska alkuperäin id turhan monimutkainen)
        varaus = {}
        vid = str(uuid.uuid1())[:8]

        # Varauksen luonti ja käyttäjälle ilmoittaminen
        if enimi == "" or snimi == "" or numer == "":
            message.set("Kentät ovat tyhjiä!")
        else:
            if len(enimi) < 2 or len(snimi) < 2 or len(numer) < 7:
                message.set("Liian lyhyt nimi, sukunimi tai\npuhelinnumero (min 7-pitkä).\nTarkista tiedot!")

            elif len(enimi) > 2 and len(snimi) > 2 and len(numer) >= 7:
                message.set("Tietojen tallennus onnistui!")
                message.set(f"HUOM! Ota ylös varausnumero: \n Etunimi: {enimi} \n Sukunimi: {snimi} "
                            f"\n Puhelinnumero: {numer} \n Elokuva: {elokuva} \n Sali: {sali} \n Aika: {aika}"
                            f" \n Varausnumero: {vid}")

                # Luodaan käyttäjän varaus, jos paikkoja vielä jääjellä
                if varausten_maara < max_paikat:
                    varaus["ID"] = vid
                    varaus["Etunimi"] = etunimi.get()
                    varaus["Sukunimi"] = sukunimi.get()
                    varaus["Puhelinnumero"] = numero.get()
                    varaus["Elokuva"] = elokuva
                    varaus["Aika"] = aika
                    varaus["Sali"] = sali

                    tallennus_tiedostoon(varaus)

                elif varausten_maara == max_paikat:
                    message.set("Kaikki paikat täynnä" + "\n" + "valitse toinen elokuva!")
    except:
        message.set("Et valinnut elokuvaa!")


# Funktio varauksen poistoon JSON tiedostosta
def poista_tiedostosta():
    varaus_id = idnumero.get()
    vids = []
    with open("varaukset.json", "r+") as tiedosto:
        data = json.load(tiedosto)
        tiedosto.close()

        # haetaan JSON:ista kaikki varaus id:t ja lisätään ne listaan vertausta varten:
        for alkio in data["varaukset"]:
            vids.append(alkio["ID"])

        if varaus_id == "":
            message.set("Kenttä tyhjä!")

        elif varaus_id in vids:
            message.set("Paikan varaus poistettu!")
            # filteroidaan(Jos varaus id ei täsmää) ja yliajetaan JSON uudelleen
            filteroitu_data = list(filter(lambda i: i["ID"] != varaus_id, data["varaukset"]))
            with open("varaukset.json", "w") as tiedosto1:
                data = {"varaukset": filteroitu_data}
                json.dump(data, tiedosto1, indent=4)
                tiedosto1.close()
        else:
            message.set("Väärä varausnumero!")


# Funktio varauksen tallennukseen JSON tiedostoon
def tallennus_tiedostoon(varaus):
    # Avataan tiedosto ja lisätään käyttäjän varaus JSON:in viimeiseksi
    with open("varaukset.json", "r+") as tiedosto:
        data = json.load(tiedosto)
        data["varaukset"].append(varaus)
        tiedosto.seek(0)
        json.dump(data, tiedosto, indent=4)
    tiedosto.close()


# Funktio varausten näyttämistä varten ylläpitäjälle
def nayta_varaukset():
    varauslaskuri()  # Kutsutaan varauslaskuria
    with open("varaukset.json", "r") as tiedosto:
        data = json.load(tiedosto)
        tiedosto.close()
        top = tk.Tk()  # Luodaan uusi tk ikkuna esitystä varten
        top.title("Varaukset")
        sarakkeet = ("ID", "Etunimi", "Sukunimi", "Puhelinnumero", "Elokuva", "Aika", "Sali")

        # Luodaan puu
        lista = ttk.Treeview(top, columns=sarakkeet, show="headings", style="Treeview")

        for sarake in sarakkeet:
            lista.heading(sarake, text=sarake)
        lista.pack(side=TOP, expand=1, fill=BOTH)

        # Viedään tieto puunäkymään
        for alkio in data['varaukset']:
            lista.insert("", "end", values=(alkio["ID"], alkio["Etunimi"], alkio["Sukunimi"], alkio["Puhelinnumero"],
                                            alkio["Elokuva"], alkio["Aika"], alkio["Sali"]))

        # Näytetään varausten määrä eri näytöksille
        n = ttk.Label(top, text=(
            f" 1.Näytös {eka_sali}:{varausten_maara1}/{eka_sali_paikat} "
            f"{toka_sali}:{varausten_maara2}/{toka_sali_paikat} "
            f"{kolmas_sali}:{varausten_maara3}/{kolmas_sali_paikat} \n"
            f" 2.Näytös {eka_sali}:{varausten_maara4}/{eka_sali_paikat} "
            f"{toka_sali}:{varausten_maara5}/{toka_sali_paikat} "
            f"{kolmas_sali}:{varausten_maara6}/{kolmas_sali_paikat} \n"
            f" 3.Näytös {eka_sali}:{varausten_maara7}/{eka_sali_paikat} "
            f"{toka_sali}:{varausten_maara8}/{toka_sali_paikat} "
            f"{kolmas_sali}:{varausten_maara9}/{kolmas_sali_paikat} \n"
            f" 4.Näytös {eka_sali}:{varausten_maara10}/{eka_sali_paikat} "
            f"{toka_sali}:{varausten_maara11}/{toka_sali_paikat} "
            f"{kolmas_sali}:{varausten_maara12}/{kolmas_sali_paikat} \n"
            f" 5.Näytös {eka_sali}:{varausten_maara13}/{eka_sali_paikat} "
            f"{toka_sali}:{varausten_maara14}/{toka_sali_paikat} "
            f"{kolmas_sali}:{varausten_maara15}/{kolmas_sali_paikat}"))
        n.pack(side=TOP)


# Funktio varausten poistamista varten. HUOM! ylikirjoittaa JSON:in
def poista_varaukset():
    vastaus = messagebox.askyesnocancel("Kysymys", "Haluatko oikeasti poistaa kaikki varaukset?")
    if vastaus:
        # Yliajaa tiedoston ja lisää perus JSON rakenteen
        with open('varaukset.json', "w") as tiedosto:
            data = {"varaukset": []}
            merkkijono = json.dumps(data, indent=4)
            tiedosto.write(merkkijono)
        tiedosto.close()
    else:
        pass


# Funktio salien ja aikojen lukemista varten
def tiedot():
    global eka_sali, toka_sali, kolmas_sali
    global eka_sali_paikat, toka_sali_paikat, kolmas_sali_paikat
    global eka_naytos, toka_naytos, kolmas_naytos, neljas_naytos, viides_naytos
    global ktun, ssan

    # Avataan tiedosto ja määritetään yllämainituille globaaleille arvoille arvot
    with open("tiedot.json", "r") as tiedosto:
        data = json.load(tiedosto)
        for alkio in data["Salit"]:
            eka_sali, toka_sali, kolmas_sali = alkio["1.Sali"], alkio["2.Sali"], alkio["3.Sali"]
            eka_sali_paikat, toka_sali_paikat = alkio["1.Paikat"], alkio["2.Paikat"]
            kolmas_sali_paikat = alkio["3.Paikat"]

        for alkio in data["Esitysajat"]:
            eka_naytos, toka_naytos, kolmas_naytos = alkio["1"], alkio["2"], alkio["3"]
            neljas_naytos, viides_naytos = alkio["4"], alkio["5"]

        for alkio in data["Tunnukset"]:
            ktun, ssan = alkio["ktun"], alkio["ssan"]
        tiedosto.close()
    tiedosto.close()


# Funktio joka korjaa tiedostot alkuperäiseen muotoon tarvittaessa HUOM! ylikirjoittaa kaiken esimerkki arvoihin
def resetoi():
    vastaus = messagebox.askyesnocancel("Kysymys", "Haluatko oikeasti alustaa kaikki alkuperäisiin arvoihin?")
    if vastaus:
        poista_varaukset()
        with open('tiedot.json', "w") as tiedosto:
            data = {"Salit": [{"1.Sali": "A-sali", "1.Paikat": 25, "2.Sali": "B-sali", "2.Paikat": 50, "3.Sali":
                "C-sali", "3.Paikat": 75}], "Esitysajat": [{"1": "07:00-10:00", "2": "10:15-13:15", "3": "13:30-16:30",
                                                            "4": "16:45-19:45", "5": "20:00-23:00"}], "Tunnukset":
                [{"ktun": "admin", "ssan": "qwerty420"}]}
            merkkijono = json.dumps(data, indent=4)
            tiedosto.write(merkkijono)
            tiedosto.close()

        with open("elokuvat.csv", "w", newline="") as tiedosto3:
            csv_rivit = [["Puuha Pete", "A-sali", "07:00-10:00"], ["Nalle Puh", "B-sali", "07:00-10:00"],
                         ["Home alone", "C-sali", "07:00-10:00"], ["Luca", "A-sali", "10:15-13:15"],
                         ["Spiral", "B-sali", "10:15-13:15"], ["Jungle cruise", "C-sali", "10:15-13:15"],
                         ["Boss level", "A-sali", "13:30-16:30"], ["Fast & Furious 9", "B-sali", "13:30-16:30"],
                         ["The tomorrow war", "C-sali", "13:30-16:30"], ["Titanic", "A-sali", "16:45-19:45"],
                         ["Spiderman 3", "B-sali", "16:45-19:45"], ["Iron man 3", "C-sali", "16:45-19:45"],
                         ["James Bond 007", "A-sali", "20:00-23:00"], ["Squid game", "B-sali", "20:00-23:00"],
                         ["Bird box", "C-sali", "20:00-23:00"]]
            kirjoittaja = csv.writer(tiedosto3)
            kirjoittaja.writerows(csv_rivit)
        tiedosto3.close()
    else:
        pass


# Pyöritetään ohjelmaa ympäri loopilla
if __name__ == "__main__":
    tiedot()
    root = tk.Tk()
    app = Valikko(root)
    app.root.title("Elokuvateatterin järjestelmä")
    root.mainloop()
