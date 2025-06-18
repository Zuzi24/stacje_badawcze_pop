# Główna aplikacja GUI
import tkinter as tk
from tkinter import simpledialog
from utils.controller import get_grouped_map
import webbrowser

def gui_main():
    def open_map(file_name="mapa.html"):
        webbrowser.open(file_name)

    def make_menu(title, dataset, type_):
        window = tk.Toplevel()
        window.title(title)

        def view():
            text.delete("1.0", tk.END)
            for item in dataset:
                text.insert(tk.END, f"{item['name']} - {item['location']}\n")

        def add():
            name = simpledialog.askstring("Dodaj", "Podaj nazwę:")
            location = simpledialog.askstring("Dodaj", "Podaj lokalizację:")
            dataset.append({"name": name, "location": location})
            view()

        def remove():
            name = simpledialog.askstring("Usuń", "Podaj nazwę:")
            for i in dataset:
                if i["name"] == name:
                    dataset.remove(i)
                    break
            view()

        def update():
            name = simpledialog.askstring("Aktualizuj", "Podaj nazwę:")
            for i in dataset:
                if i["name"] == name:
                    i["name"] = simpledialog.askstring("Nowa nazwa", "Nowa nazwa:")
                    i["location"] = simpledialog.askstring("Nowa lokalizacja", "Nowa lokalizacja:")
                    break
            view()

        def show_map():
            get_grouped_map(dataset, f"{type_}_map.html")
            open_map(f"{type_}_map.html")


        tk.Button(window, text="Wyświetl", command=view).pack()
        tk.Button(window, text="Dodaj", command=add).pack()
        tk.Button(window, text="Usuń", command=remove).pack()
        tk.Button(window, text="Aktualizuj", command=update).pack()
        tk.Button(window, text="Mapa", command=show_map).pack()
        text = tk.Text(window, height=15, width=50)
        text.pack()

    root = tk.Tk()
    root.title("System zarządzania siecią badawczą")

    tk.Button(root, text="Stacje badawcze").pack(pady=5)
    tk.Button(root, text="Pracownicy").pack(pady=5)
    tk.Button(root, text="Klienci").pack(pady=5)

    tk.Button(root, text="Zamknij", command=root.destroy).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    gui_main()