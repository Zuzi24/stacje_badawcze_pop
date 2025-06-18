# Główna aplikacja GUI
import tkinter as tk

def gui_main():
    root = tk.Tk()
    root.title("System zarządzania siecią badawczą")

    tk.Button(root, text="Stacje badawcze").pack(pady=5)
    tk.Button(root, text="Pracownicy").pack(pady=5)
    tk.Button(root, text="Klienci").pack(pady=5)

    tk.Button(root, text="Zamknij", command=root.destroy).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    gui_main()