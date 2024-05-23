from datetime import datetime, timedelta, time

class Szoba:
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=20000, szobaszam=szobaszam)

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=30000, szobaszam=szobaszam)

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

class Foglalas:
    def __init__(self, szoba, kezdes, vege, nev):
        self.szoba = szoba
        self.kezdes = kezdes
        self.vege = vege
        self.nev = nev

class FoglalasKezelo:
    def __init__(self):
        self.foglalasok = []

    def foglalas(self, szalloda, szobaszam, kezdes, vege, nev):
        kezdes = datetime.combine(kezdes.date(), time(14, 0))
        vege = datetime.combine(vege.date(), time(10, 0))
        for szoba in szalloda.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas = Foglalas(szoba, kezdes, vege, nev)
                self.foglalasok.append(foglalas)
                napok_szama = (vege - kezdes).days
                if (vege - kezdes).seconds > 0:
                    napok_szama += 1
                teljes_ar = napok_szama * szoba.ar
                return f'A foglalás sikeres. Teljes ár: {teljes_ar} ({szoba.ar} per nap)'
        return 'Nem található ilyen szoba.'

    def lemondas(self, nev, szobaszam, kezdes, vege):
        kezdes = datetime.combine(kezdes.date(), time(14, 0))
        vege = datetime.combine(vege.date(), time(10, 0))
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.nev == nev and foglalas.kezdes == kezdes and foglalas.vege == vege:
                self.foglalasok.remove(foglalas)
                return 'A foglalás sikeresen törölve.'
        return 'Nem található ilyen foglalás.'

    def listaz(self):
        if self.foglalasok:
            rendezett_foglalasok = sorted(self.foglalasok, key=lambda f: f.kezdes)
            for foglalas in rendezett_foglalasok:
                print(f"Szoba: {foglalas.szoba.szobaszam}, Kezdés: {foglalas.kezdes}, Vége: {foglalas.vege}, Név: {foglalas.nev}")
        else:
            print("Nincs foglalás.")

    def szabad_szobak_listazasa(self, szalloda, kezdes, vege):
        kezdes = datetime.combine(kezdes.date(), time(14, 0))
        vege = datetime.combine(vege.date(), time(10, 0))
        print("Szabad szobák és árak:")
        foglalt_szobak = set(foglalas.szoba.szobaszam for foglalas in self.foglalasok if not (foglalas.vege < kezdes or foglalas.kezdes > vege))
        for szoba in szalloda.szobak:
            if szoba.szobaszam not in foglalt_szobak:
                napok_szama = (vege - kezdes).days
                if (vege - kezdes).seconds > 0:
                    napok_szama += 1
                teljes_ar = napok_szama * szoba.ar
                print(f"Szoba száma: {szoba.szobaszam}, Ár: {szoba.ar} per nap, Teljes ár: {teljes_ar}")

    def listaz_jovobeli_foglalasok(self, nev):
        most = datetime.now()
        jovobeli_foglalasok = [foglalas for foglalas in self.foglalasok if foglalas.nev == nev and foglalas.kezdes >= most]
        if jovobeli_foglalasok:
            for foglalas in jovobeli_foglalasok:
                print(f"Szoba: {foglalas.szoba.szobaszam}, Kezdés: {foglalas.kezdes}, Vége: {foglalas.vege}, Név: {foglalas.nev}")
        else:
            print("Nincs jövőbeli foglalás ezzel a névvel.")

# Példa adatok létrehozása
szalloda = Szalloda("Példa Szálloda")
szalloda.uj_szoba(EgyagyasSzoba("101"))
szalloda.uj_szoba(EgyagyasSzoba("102"))
szalloda.uj_szoba(KetagyasSzoba("201"))
szalloda.uj_szoba(KetagyasSzoba("202"))

foglalaskezelo = FoglalasKezelo()
foglalaskezelo.foglalas(szalloda, "101", datetime(2024, 5, 27), datetime(2024, 5, 29), "Nagy Péter")
foglalaskezelo.foglalas(szalloda, "201", datetime(2024, 5, 30), datetime(2024, 6, 1), "Kis Anna")

# Felhasználói interfész
def main_menu():
    while True:
        print("\nVálassz műveletet:")
        print("1. Foglalás")
        print("2. Lemondás")
        print("3. Foglalások listázása")
        print("Bármikor megszakítható a folyamat az 'esc' parancs megadásával.")

        valasztas = input("Adja meg a kívánt művelet számát: ")
        if valasztas == "1":
            handle_foglalas()
        elif valasztas == "2":
            handle_lemondas()
        elif valasztas == "3":
            foglalaskezelo.listaz()
        elif valasztas.lower() == 'esc':
            print("Kilépés.")
            break
        else:
            print("Érvénytelen választás.")

def handle_foglalas():
    while True:
        try:
            kezdes = input("Adja meg a bejelentkezés dátumát (YYYY-MM-DD formátumban): ")
            if kezdes.lower() == 'esc':
                return
            kezdes = datetime.strptime(kezdes, "%Y-%m-%d")
            vege = input("Adja meg a távozás dátumát (YYYY-MM-DD formátumban): ")
            if vege.lower() == 'esc':
                return
            vege = datetime.strptime(vege, "%Y-%m-%d")
            if kezdes.date() >= datetime.now().date() and vege.date() > kezdes.date():
                break
            else:
                print("Érvénytelen dátumok. Kérem adja meg a jövőbeli dátumokat, és a távozás később kell legyen mint a bejelentkezés.")
        except ValueError:
            print("Érvénytelen dátum formátum. Kérem adja meg újra.")

    foglalaskezelo.szabad_szobak_listazasa(szalloda, kezdes, vege)
    while True:
        szobaszam = input("Adja meg a foglalni kívánt szoba számát: ")
        if szobaszam.lower() == 'esc':
            return
        nev = input("Adja meg a foglalás nevét: ")
        if nev.lower() == 'esc':
            return
        print(foglalaskezelo.foglalas(szalloda, szobaszam, kezdes, vege, nev))
        return

def handle_lemondas():
    while True:
        nev = input("Adja meg a foglalás nevét: ")
        if nev.lower() == 'esc':
            return
        foglalaskezelo.listaz_jovobeli_foglalasok(nev)
        if not foglalaskezelo.foglalasok or all(f.nev != nev for f in foglalaskezelo.foglalasok):
            print("Nem található ilyen foglalás.")
            return

        while True:
            szobaszam = input("Adja meg a szoba számát: ")
            if szobaszam.lower() == 'esc':
                return
            try:
                kezdes = input("Adja meg a foglalás kezdetének dátumát (YYYY-MM-DD formátumban): ")
                if kezdes.lower() == 'esc':
                    return
                kezdes = datetime.strptime(kezdes, "%Y-%m-%d")
                vege = input("Adja meg a foglalás végének dátumát (YYYY-MM-DD formátumban): ")
                if vege.lower() == 'esc':
                    return
                vege = datetime.strptime(vege, "%Y-%m-%d")
                result = foglalaskezelo.lemondas(nev, szobaszam, kezdes, vege)
                if result == 'A foglalás sikeresen törölve.':
                    print("Biztosan törölni szeretné a foglalást? 1. Igen, 2. Nem")
                    torles_valasztas = input("Adja meg a választott művelet számát: ")
                    if torles_valasztas == "1":
                        print("Foglalás törölve.")
                        return
                    else:
                        print("Foglalás nem lett törölve.")
                        return
                else:
                    print("Nem található ilyen foglalás.")
                    return
            except ValueError:
                print("Érvénytelen dátum formátum. Kérem adja meg újra.")

if __name__ == "__main__":
    main_menu()
