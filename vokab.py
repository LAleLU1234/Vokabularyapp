import tkinter as tk
from tkinter import messagebox, filedialog
import json
import random

class VokabelTrainerApp:
    def __init__(self, root):
        self.root = root
        root.title("Vokabeltrainer")
        root.geometry("300x500+0+0")

        self.start_button = tk.Button(root, text="Start", command=self.start_training)
        self.start_button.pack(pady=20)

        self.vokabel_label = tk.Label(root, text="", font=("Arial", 16))
        self.antwort_entry = tk.Entry(root, font=("Arial", 14))
        self.antwort_entry.bind("<Return>", self.ueberpruefen)
        self.skip_button = tk.Button(root, text="Skip", command=self.naechste_vokabel)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Vokabeln hinzufügen", command=self.vokabeln_hinzufuegen)
        self.file_menu.add_command(label="Vokabeln speichern", command=self.vokabeln_speichern)
        self.file_menu.add_command(label="Vokabeln laden", command=self.vokabeln_laden)
        self.menu.add_cascade(label="Optionen", menu=self.file_menu)

        self.vokabeln = {}
        self.aktuelle_vokabel = None

    def start_training(self):
        self.start_button.pack_forget()
        self.vokabel_label.pack(pady=20)
        self.antwort_entry.pack(pady=10)
        self.skip_button.pack(pady=5)
        self.naechste_vokabel()

    def naechste_vokabel(self):
        if not self.vokabeln:
            messagebox.showinfo("Info", "Keine Vokabeln vorhanden. Bitte laden oder hinzufügen.")
            return

        self.aktuelle_vokabel = random.choice(list(self.vokabeln.items()))
        if random.choice([True, False]):
            self.vokabel_label.config(text=f"Übersetze: {self.aktuelle_vokabel[0]}")
            self.richtige_antwort = self.aktuelle_vokabel[1]
        else:
            self.vokabel_label.config(text=f"Übersetze: {self.aktuelle_vokabel[1]}")
            self.richtige_antwort = self.aktuelle_vokabel[0]

        self.antwort_entry.delete(0, tk.END)

    def ueberpruefen(self, event=None):
        antwort = self.antwort_entry.get()
        if antwort.lower() == self.richtige_antwort.lower():
            messagebox.showinfo("Richtig", "Deine Antwort ist richtig!")
        else:
            messagebox.showerror("Falsch", f"Falsch, die richtige Antwort ist '{self.richtige_antwort}'")

        self.naechste_vokabel()

    def vokabeln_hinzufuegen(self):
        def hinzufuegen():
            englisch = englisch_entry.get()
            deutsch = deutsch_entry.get()
            if englisch and deutsch:
                self.vokabeln[englisch] = deutsch
                englisch_entry.delete(0, tk.END)
                deutsch_entry.delete(0, tk.END)
                englisch_entry.focus()

        hinzufuegen_window = tk.Toplevel()
        hinzufuegen_window.title("Vokabeln hinzufügen")

        tk.Label(hinzufuegen_window, text="Englisch:").pack(pady=5)
        englisch_entry = tk.Entry(hinzufuegen_window)
        englisch_entry.pack(pady=5)

        tk.Label(hinzufuegen_window, text="Deutsch:").pack(pady=5)
        deutsch_entry = tk.Entry(hinzufuegen_window)
        deutsch_entry.pack(pady=5)

        hinzufuegen_button = tk.Button(hinzufuegen_window, text="Hinzufügen", command=hinzufuegen)
        hinzufuegen_button.pack(pady=10)

    def vokabeln_speichern(self):
        datei = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON-Dateien", "*.json")])
        if datei:
            with open(datei, "a", encoding="utf-8") as file:
                json.dump(self.vokabeln, file)
            messagebox.showinfo("Gespeichert", "Vokabeln gespeichert.")

    def vokabeln_laden(self):
        datei = filedialog.askopenfilename(filetypes=[("JSON-Dateien", "*.json")])
        if datei:
            with open(datei, "r", encoding="utf-8") as file:
                self.vokabeln = json.load(file)
            messagebox.showinfo("Geladen", "Vokabeln geladen.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VokabelTrainerApp(root)
    root.mainloop()
