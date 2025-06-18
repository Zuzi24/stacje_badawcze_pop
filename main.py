# Główna aplikacja GUI
import tkinter as tk
from tkinter import simpledialog , messagebox
from utils.controller import get_grouped_map
from utils.model import clients, employees , stations
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
                text.insert(tk.END, f"{item['name']}           {item['location']}\n")

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

        btn_frame = tk.Frame(window)
        btn_frame.pack()
        tk.Button(btn_frame, text="Wyświetl", command=view).grid(row=0, column=0)
        tk.Button(btn_frame, text="Dodaj", command=add).grid(row=0, column=1)
        tk.Button(btn_frame, text="Usuń", command=remove).grid(row=0, column=2)
        tk.Button(btn_frame, text="Aktualizuj", command=update).grid(row=0, column=3)
        tk.Button(btn_frame, text="Mapa", command=show_map).grid(row=0, column=4)

        text = tk.Text(window, height=15, width=80)
        text.pack()

    def map_clients_of_station():
        name = simpledialog.askstring("Stacja", "Podaj lokalizacje stacji:")
        filtered = [c for c in clients if c['location'] == name]
        if not filtered:
            messagebox.showinfo("Brak danych", "Brak klientów dla tej stacji.")
            return
        get_grouped_map(filtered, "clients_of_station.html")
        open_map("clients_of_station.html")

    def map_employees_of_station():
            name = simpledialog.askstring("Stacja", "Podaj lokalizacje stacji:")
            filtered = [e for e in employees if e['location'] == name]
            if not filtered:
                messagebox.showinfo("Brak danych", "Brak pracowników dla tej stacji.")
                return
            get_grouped_map(filtered, "employees_of_station.html")
            open_map("employees_of_station.html")

    root = tk.Tk()
    root.title("System zarządzania siecią badawczą")

    tk.Button(root, text="Stacje badawcze", command=lambda: make_menu("Stacje", stations, "stations")).pack(pady=10)
    tk.Button(root, text="Pracownicy", command=lambda: make_menu("Pracownicy", employees, "employees")).pack(pady=10)
    tk.Button(root, text="Klienci", command=lambda: make_menu("Klienci", clients, "clients")).pack(pady=10)

    tk.Button(root, text="Mapa klientów wybranej stacji", command=map_clients_of_station).pack(pady=10)
    tk.Button(root, text="Mapa pracowników wybranej stacji", command=map_employees_of_station).pack(pady=10)

    tk.Button(root, text="Zamknij", command=root.destroy).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    gui_main()