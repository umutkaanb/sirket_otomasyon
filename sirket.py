from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import webbrowser


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        F1 = Frame(self.master, bg="gray")
        F1.pack(pady=15, padx=25)

        self.F_listele = Frame(self.master)
        self.F_ekle = Frame(self.master)

        B1 = Button(F1, text="Çalışan Ekle", command=self.ekle, font="bold", cursor="hand2", fg="blue",bg="white", width=13, height=3)
        B1.grid(row=0, column=0, padx=20)
        B2 = Button(F1, text="Çalışan Listele", command=self.listele, font="bold", cursor="hand2", fg="green",bg="white", width=13,
                    height=3)
        B2.grid(row=0, column=1)
        self.baglanti = sqlite3.connect("baglan.sql", check_same_thread=True)
        self.im = self.baglanti.cursor()

    def ekle(self):
        if self.F_listele:
            self.F_listele.destroy()
        if self.F_ekle:
            self.F_ekle.destroy()
        self.F_ekle = Frame(self.master)
        self.F_ekle.place(x=250, y=150)
        Label(self.F_ekle, text="Adı Soyadı: ").grid(row=0, column=0, pady=5, sticky=W)
        self.E1 = Entry(self.F_ekle, width=35)
        self.E1.grid(row=0, column=1, pady=5)

        Label(self.F_ekle, text="HES Kodu: ").grid(row=1, column=0, pady=5, sticky=W)
        self.E2 = Entry(self.F_ekle, width=35)
        self.E2.grid(row=1, column=1, pady=5)

        Label(self.F_ekle, text="Pozisyonu: ").grid(row=2, column=0, pady=5, sticky=W)
        self.E3 = Entry(self.F_ekle, width=35)
        self.E3.grid(row=2, column=1, pady=5)

        Label(self.F_ekle, text="Cinsiyeti: ").grid(row=3, column=0, pady=5, sticky=W)
        self.SS = Entry(self.F_ekle, width=35)
        self.SS.grid(row=3, column=1, pady=5, sticky=W)

        Label(self.F_ekle, text="Yaşı: ").grid(row=4, column=0, pady=5, sticky=W)
        self.yasSay = Spinbox(self.F_ekle, from_=1, to=999, width=5)
        self.yasSay.grid(row=4, column=1, pady=5, sticky=W)

        Label(self.F_ekle, text="Maaşı: ").grid(row=5, column=0, pady=5, sticky=W)
        self.maasSay = Spinbox(self.F_ekle, from_=1, to=2021, width=5)
        self.maasSay.grid(row=5, column=1, sticky=W)

        B3 = Button(self.F_ekle, text="Kaydet", command=self.kayit_et, fg="green", cursor="hand2", width=20)
        B3.grid(row=6, column=1, pady=8, sticky=SE)

    def kayit_et(self):
        try:
            self.im.execute(
                "CREATE TABLE IF NOT EXISTS calisanlar (id INTEGER PRIMARY KEY, calisan_adi VARCHAR(45), soyadi VARCHAR(45), pozisyonu VARCHAR(45), cinsiyeti INT, yasi INT, maasi)")  # Tablo oluşturma
            self.im.execute(
                "INSERT INTO calisanlar VALUES (null,'" + self.E1.get() + "','" + self.E2.get() + "','" + self.E3.get() + "','" + self.SS.get() + "','" + self.yasSay.get() + "','" + self.maasSay.get() + "')")  # Veri ekleme
            self.baglanti.commit()
            messagebox.showinfo("Başarılı", "Çalışan başarıyla kayıt edildi!")
        except:
            messagebox.showerror("Hata", "Kayıt Yapılamadı, Bilgileri Kontrol Edin!")

    def listele(self):
        try:
            if self.F_ekle:
                self.F_ekle.destroy()
            if self.F_listele:
                self.F_listele.destroy()
            self.F_listele = Frame(self.master)
            self.F_listele.place(x=0, y=120)
            self.im.execute("SELECT * FROM calisanlar")
            data = self.im.fetchall()

            def arama():
                deget = self.ara.get()
                query = "SELECT id, calisan_adi, soyadi, pozisyonu, cinsiyeti, yasi, maasi FROM calisanlar WHERE calisan_adi LIKE '%" + deget + "%' OR soyadi LIKE '%" + deget + "%' OR pozisyonu LIKE '%" + deget + "%'"
                self.im.execute(query)
                rows = self.im.fetchall()
                guncelle(rows)
                bulunanVeri = len(rows)
                toplamverilbl["text"] = ""
                AraLBL["text"] = "Bulunan Veri: " + str(bulunanVeri)
                AraLBL.grid(row=3, column=0, sticky=W)

            self.ara = Entry(self.F_listele, width=35)
            self.ara.grid(row=0, column=0, sticky=W, pady=20, padx=10)
            self.araBTN = Button(self.F_listele, text="Ara", fg="black", command=arama, width=5)
            self.araBTN.grid(row=0, column=0, sticky=W, pady=20, padx=230)

            self.tv = ttk.Treeview(self.F_listele, columns=(1, 2, 3, 4, 5, 6, 7), show='headings', height=10)
            self.tv.grid()
            self.tv.bind("<Button-3>", self.popup)
            self.tv.heading(1, text='ID')
            self.tv.heading(2, text='Adı Soyadı')
            self.tv.heading(3, text='HES Kodu')
            self.tv.heading(4, text='Pozisyonu')
            self.tv.heading(5, text='Cinsiyeti')
            self.tv.heading(6, text='Yaşı')
            self.tv.heading(7, text='Maaşı')

            self.tv.column("1", minwidth=10, width=27)
            self.tv.column("2", minwidth=50, width=250)
            self.tv.column("3", minwidth=50, width=198)
            self.tv.column("4", minwidth=50, width=100)
            self.tv.column("5", minwidth=10, width=60)
            self.tv.column("6", minwidth=10, width=40)
            self.tv.column("7", minwidth=10, width=60)

            sb = Scrollbar(self.F_listele, orient=VERTICAL, command=self.tv.yview)
            sb.grid(row=1, column=1, sticky=NS)
            sb2 = Scrollbar(self.F_listele, orient=HORIZONTAL, command=self.tv.xview)
            sb2.grid(row=2, column=0, sticky=EW)

            toplamVeri = f"{len(data)} Veri Bulundu"
            toplamverilbl = Label(self.F_listele, text=toplamVeri)
            toplamverilbl.grid(row=3, column=0, sticky=W)  # .place(x=0, y=380)
            Button(self.F_listele, text="Tabloyu Yenile", fg="red", command=self.Yenile).grid(row=3, column=0, sticky=S)
            AraLBL = Label(self.F_listele)

            self.tv.config(yscrollcommand=sb2.set)
            self.tv.configure(yscrollcommand=sb.set, xscrollcommand=sb2.set)
            s = 1
            for i in data:
                self.tv.insert(parent='', index=s, iid=s, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
                s += 1

            def guncelle(rows):
                self.tv.delete(*self.tv.get_children())
                for i in rows:
                    self.tv.insert("", "end", values=i)
        except:
            messagebox.showwarning("Hata", "Çalışan Bulunamadı")

    def Yenile(self):
        self.F_listele.destroy()
        self.listele()

    def popup(self, event):
        iid = self.tv.identify_row(event.y)
        if iid:
            m = Menu(pencere, tearoff=0)
            m.add_command(label="Düzenle", command=self.Duzenle)
            m.add_command(label="Verileri Kopyala", command=self.Kopyala)
            m.add_command(label="Veriyi Sil",command=self.verileriSil)
            self.tv.selection_set(iid)
            self.at = self.tv.selection_set(iid)
            m.post(event.x_root, event.y_root)
        else:
            pass

    def Duzenle(self):
        focus = self.tv.focus()
        numara = self.tv.item(focus)["values"][0]
        yeniWin = Toplevel()
        yeniWin.wm_title("Çalışan Bilgileri")
        windowWidth = yeniWin.winfo_reqwidth()
        windowHeight = yeniWin.winfo_reqheight()
        positionRight = int(yeniWin.winfo_screenwidth() / 2 - windowWidth / 1)
        positionDown = int(yeniWin.winfo_screenheight() / 3 - windowHeight / 3)
        yeniWin.geometry(f"300x300+{positionRight}+{positionDown}")
        yeniWin.resizable(width=False, height=False)



        def veriKayit():
            # Veri Tabanını oluşturma
            self.im.execute(
                "CREATE TABLE IF NOT EXISTS calisanlar (calisan_adi VARCHAR(45), soyadi VARCHAR(45), pozisyonu VARCHAR(45), cinsiyeti INT, yasi INT, maasi)")  # Tablo oluşturma

            self.im.execute(
                "UPDATE calisanlar SET calisan_adi = ?, soyadi = ?, pozisyonu = ?, cinsiyeti = ?, yasi = ?, maasi = ? WHERE id = ?",
                (self.E1.get(), self.E2.get(), self.E3.get(), self.SS.get(), self.yasSay.get(), self.maasSay.get(),
                 numara))
            self.baglanti.commit()
            say = Label(yeniWin, text="Çalışan güncellendi.", font="bold", fg="green")
            messagebox.showinfo("Başarılı", "Çalışan Başarıyla Güncellendi")
            yeniWin.destroy()
            say.after(2000, say.destroy)

        def veriDuzenle():
            self.E1.config(state="normal")
            self.E2.config(state="normal")
            self.E3.config(state="normal")
            self.SS.config(state="normal")
            self.yasSay.config(state="normal")
            self.maasSay.config(state="normal")
            B3.config(state="normal", cursor="hand2")

        def veriSil():
            son_mesaj = ""
            evet = messagebox.askyesno("Sil", "Çalışanı silmek istiyor musunuz?")
            if evet:
                self.im.execute("DELETE FROM calisanlar WHERE id = ?", [numara])
                self.baglanti.commit()
                son_mesaj+="Çalışan başarıyla silindi."
                messagebox.showinfo("Başarılı İşlem", son_mesaj)
                yeniWin.destroy()

        F_ekle = Frame(yeniWin)
        F_ekle.pack()
        kopya = self.tv.focus()
        Label(F_ekle, text="Adı, Soyadı: ").grid(row=0, column=0, pady=5, sticky=W)
        self.E1 = Entry(F_ekle, width=35)
        self.E1.insert(0, self.tv.item(kopya)["values"][1])
        self.E1.config(state="disable")
        self.E1.grid(row=0, column=1, pady=5)

        Label(F_ekle, text="HES Kodu: ").grid(row=1, column=0, pady=5, sticky=W)
        self.E2 = Entry(F_ekle, width=35)
        self.E2.insert(0, self.tv.item(kopya)["values"][2])
        self.E2.config(state="disable")
        self.E2.grid(row=1, column=1, pady=5)

        Label(F_ekle, text="Pozisyonu: ").grid(row=2, column=0, pady=5, sticky=W)
        self.E3 = Entry(F_ekle, width=35)
        self.E3.insert(0, self.tv.item(kopya)["values"][3])
        self.E3.config(state="disable")
        self.E3.grid(row=2, column=1, pady=5)

        Label(F_ekle, text="Cinsiyeti: ").grid(row=3, column=0, pady=5, sticky=W)
        self.SS = Entry(F_ekle, width=35)
        self.SS.insert(0, self.tv.item(kopya)["values"][4])
        self.SS.config(state="disable")
        self.SS.grid(row=3, column=1, pady=5, sticky=W)

        Label(F_ekle, text="Yaşı: ").grid(row=4, column=0, pady=5, sticky=W)
        self.yasSay = Spinbox(F_ekle, width=5, from_=0, to=999)
        self.yasSay.insert(0, self.tv.item(kopya)["values"][5])
        self.yasSay.config(state="disable")
        self.yasSay.grid(row=4, column=1, pady=5, sticky=W)

        Label(F_ekle, text="Maaşı: ").grid(row=5, column=0, pady=5, sticky=W)
        self.maasSay = Spinbox(F_ekle, width=5, from_=1, to=999999)
        self.maasSay.insert(0, self.tv.item(kopya)["values"][6])
        self.maasSay.config(state="disable")
        self.maasSay.grid(row=5, column=1, sticky=W)


        B3 = Button(F_ekle, text="Kaydet", command=veriKayit, fg="green", width=15)
        B3.config(state="disable")
        B3.grid(row=4, column=1, pady=8, sticky=NE)

        B4 = Button(F_ekle, text="Düzenle", command=veriDuzenle, fg="blue", cursor="hand2", width=15)
        B4.grid(row=5, column=1, pady=8, sticky=NE)

    def Kopyala(self):
        kopya = self.tv.focus()
        self.master.clipboard_clear()
        self.master.clipboard_append(self.tv.item(kopya)["values"])
        messagebox.showinfo("Başarılı İşlem", "Çalışan verileri kopyalandı!")

    def verileriSil(self):
        focus = self.tv.focus()
        numara = self.tv.item(focus)["values"][0]
        son_mesaj = ""
        evet = messagebox.askyesno("Sil", "Çalışanı silmek istiyor musunuz?")
        if evet:
            self.im.execute("DELETE FROM calisanlar WHERE id = ?", [numara])
            self.baglanti.commit()
            son_mesaj += "Çalışan başarıyla silindi."
            messagebox.showinfo("Başarılı İşlem", son_mesaj)



    def exitProgram(self):
        exit()

pencere = Tk()
app = Window(pencere)
pencere.wm_title("Şirket Otomasyon Sistemi")

windowWidth = pencere.winfo_reqwidth()
windowHeight = pencere.winfo_reqheight()
positionRight = int(pencere.winfo_screenwidth() / 3.4 - windowWidth / 2)
positionDown = int(pencere.winfo_screenheight() / 3.4 - windowHeight / 2)
pencere.geometry(f"755x520+{positionRight}+{positionDown}")
pencere.configure(bg="gray")
pencere.resizable(width=False, height=False)


def callback(url):
    webbrowser.open_new(url)

pencere.mainloop()
