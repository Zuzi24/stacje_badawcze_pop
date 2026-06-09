#napisz funkcje która będzie sprawdzała czy sylaba la znajduje sie w słowie podanym przez uzytkownika

def sylaba(slowo):
    return True if 'la' in slowo else False


slowo = input("podaj słowo: ")

print(sylaba(slowo))
