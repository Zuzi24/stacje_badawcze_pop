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
        window = tk.Toplevel(root)
        window.title(title)

        selected_index = tk.IntVar()

        def refresh_list():
            listbox.delete(0, tk.END)
            for item in dataset:
                listbox.insert(tk.END, f"{item['name']} - {item['location']}")

        def add():
            name = simpledialog.askstring("Dodaj", "Podaj nazwę:")
            location = simpledialog.askstring("Dodaj", "Podaj lokalizację:")
            if name and location:
                dataset.append({"name": name, "location": location})
                refresh_list()

        def remove():
            idx = listbox.curselection()
            if not idx:
                messagebox.showwarning("Uwaga", "Nie zaznaczono elementu do usunięcia.")
                return
            dataset.pop(idx[0])
            refresh_list()

        def update():
            idx = listbox.curselection()
            if not idx:
                messagebox.showwarning("Uwaga", "Nie zaznaczono elementu do edycji.")
                return
            current = dataset[idx[0]]
            new_name = simpledialog.askstring("Nowa nazwa", "Nowa nazwa:", initialvalue=current["name"])
            new_location = simpledialog.askstring("Nowa lokalizacja", "Nowa lokalizacja:",
                                                  initialvalue=current["location"])
            if new_name and new_location:
                dataset[idx[0]] = {"name": new_name, "location": new_location}
                refresh_list()

        def show_map():
            get_grouped_map(dataset, f"{type_}_map.html")
            webbrowser.open(f"{type_}_map.html")

        # UI
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Dodaj", command=add, width=12).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Usuń", command=remove, width=12).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Aktualizuj", command=update, width=12).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Mapa", command=show_map, width=12).grid(row=0, column=3, padx=5)

        listbox = tk.Listbox(window, width=60, height=15)
        listbox.pack(padx=10, pady=10)

        refresh_list()

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