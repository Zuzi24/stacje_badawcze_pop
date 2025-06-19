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


        def refresh_list():
            listbox.delete(0, tk.END)
            for item in dataset:
                station_info = f"       {item['station']}" if "station" in item else ""
                listbox.insert(tk.END, f"{item['name']}       {item['location']}{station_info}")

        def add():
            name = simpledialog.askstring("Dodaj", "Podaj nazwę:")
            location = simpledialog.askstring("Dodaj", "Podaj lokalizację:")

            if not name or not location:
                messagebox.showwarning("Błąd", "Musisz podać nazwę i lokalizację.")
                return

            if type_ in ["clients", "employees"]:
                # Lista nazw istniejących stacji
                station_names = [s["name"] for s in stations]

                # Okno wyboru stacji
                station_window = tk.Toplevel(window)
                station_window.title("Wybierz stację")

                tk.Label(station_window, text="Wybierz stację dla tej osoby:").pack(pady=5)
                selected_station = tk.StringVar()
                selected_station.set(station_names[0])  # domyślnie pierwsza stacja

                tk.OptionMenu(station_window, selected_station, *station_names).pack(pady=5)

                def confirm_station():
                    station = selected_station.get()
                    dataset.append({
                        "name": name,
                        "location": location,
                        "station": station
                    })
                    station_window.destroy()
                    refresh_list()

                tk.Button(station_window, text="Zatwierdź", command=confirm_station).pack(pady=10)
            else:
                dataset.append({
                    "name": name,
                    "location": location
                })
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

            if not new_name or not new_location:
                messagebox.showwarning("Błąd", "Musisz podać nazwę i lokalizację.")
                return

            if type_ in ["clients", "employees"]:
                station_names = [s["name"] for s in stations]

                station_window = tk.Toplevel(window)
                station_window.title("Wybierz nową stację")

                tk.Label(station_window, text="Wybierz nową stację:").pack(pady=5)
                selected_station = tk.StringVar()
                selected_station.set(current.get("station", station_names[0]))

                tk.OptionMenu(station_window, selected_station, *station_names).pack(pady=5)

                def confirm_update():
                    dataset[idx[0]] = {
                        "name": new_name,
                        "location": new_location,
                        "station": selected_station.get()
                    }
                    station_window.destroy()
                    refresh_list()

                tk.Button(station_window, text="Zatwierdź", command=confirm_update).pack(pady=10)
            else:
                dataset[idx[0]] = {
                    "name": new_name,
                    "location": new_location
                }
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
        name = simpledialog.askstring("Stacja", "Podaj nazwę stacji:")
        filtered = [c for c in clients if c['station'] == name]
        if not filtered:
            messagebox.showinfo("Brak danych", "Brak klientów dla tej stacji.")
            return
        get_grouped_map(filtered, "clients_of_station.html")
        open_map("clients_of_station.html")

    def map_employees_of_station():
            name = simpledialog.askstring("Stacja", "Podaj nazwę stacji:")
            filtered = [e for e in employees if e['station'] == name]
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