def int_jeu(n, m, niveau):
    import random
    terrain = []
    # 3 lvl de jeu different
    if niveau == 1:
        mines = 0.2
    elif niveau == 2:
        mines = 0.3
    else:
        mines = 0.4
    for i in range(n):
        L = random.choices([0, 2], weights=[(1 - mines), mines], k=m)  # fct qui permet de créer un terrain de mines
        terrain.append(L)
    return terrain


def mines_autour(terrain):
    import copy
    mined = copy.deepcopy(terrain)  # copy la terrain T
    for i in range(len(mined)):
        for j in range(len(mined[i])):
            nb_mines = 0
            for x in range(i - 1, i + 2):  # boucle qui cherche les valeurs a coté de la case i
                for y in range(j - 1, j + 2):  # boucle qui cherche les valeurs a coté de la case j
                    if x != i or y != j:
                        if 0 <= x < len(terrain) and 0 <= y < len(terrain[0]):
                            if terrain[x][y] == 2:
                                nb_mines = nb_mines + 1
            mined[i][j] = nb_mines
    return mined


def drapeau(T, i, j):
    taille_x = len(T)
    taille_y = len(T[0])
    if 0 <= i < taille_x and 0 <= j < taille_y:
        if T[i][j] == 0:
            T[i][j] = 3
        elif T[i][j] == 2:
            T[i][j] = 4
        return True
    else:
        return False


def lever_drapeau(T, i, j):
    taille_x = len(T)
    taille_y = len(T[0])
    if 0 <= i < taille_x and 0 <= j < taille_y:
        if T[i][j] == 3:
            T[i][j] = 0
        elif T[i][j] == 4:
            T[i][j] = 0
        return True
    else:
        return False


def is_drapeau(T, i, j):
    if T[i][j] == 3 or T[i][j] == 4:
        return True
    else:
        return False


def is_mined(T, i, j):
    if T[i][j] == 2:
        return True
    else:
        return False


def is_creuser(T, i, j):
    if T[i][j] == 1:
        return True
    else:
        return False


def creuser(T, M, i, j):
    taillex = len(T)
    tailley = len(T[0])
    if 0 <= i < taillex and 0 <= j < tailley and not is_drapeau(T, i, j) and T[i][j] != 1:
        if is_mined(T, i, j):
            return False
        elif T[i][j] == 0:
            T[i][j] = 1
            if M[i][j] == 0:
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        if i != x or j != y:
                            creuser(T, M, x, y)
            return True
    else:
        return True


def niveau_de_jeu():
    n = int(input("Longueur du terrain ? : "))
    m = int(input("Largeur du terrain ? : "))
    lvl = int(input("Quelle niveau (1, 2 OU 3) ? : "))
    print()
    if lvl == 0:
        T = int_jeu(n, m, 1)
    elif lvl == 1:
        T = int_jeu(n, m, 2)
    else:
        T = int_jeu(n, m, 3)
    return T


def play(T, M):
    import time
    debut = time.time()
    fin = 0
    afficherTM(T, M)
    print()
    finish = False
    win = False

    # calculer cases libres
    case_libres = 0
    for a in range(len(T)):
        for b in range(len(T[0])):
            if T[a][b] == 0:
                case_libres += 1

    # prog prinip
    while not finish:
        val_x = input("Valeur en x = ")
        val_y = input("Valeur en y = ")
        while val_x == "":
            val_x = input("Valeur en x = ")
        while val_y == "":
            val_y = input("Valeur en y = ")
        if val_x == "d" or val_x == "D" or val_x == "d" or val_x == "D":
            print()
            print("Mode drapeau : ")
            afficherTM(T, M)
            print()
            val_x = input("Valeur en x du drapeau = ")
            val_y = input("Valeur en y du drapeau = ")
            x = int(val_x)
            y = int(val_y)
            drapeau(T, x, y)
            afficherTM(T, M)
        elif val_x == "f" or val_x == "F" or val_x == "f" or val_x == "F":
            print()
            print("Lever drapeau : ")
            afficherTM(T, M)
            print()
            val_x = input("Valeur en x du drapeau a lever = ")
            val_y = input("Valeur en y du drapeau a lever = ")
            x = int(val_x)
            y = int(val_y)
            lever_drapeau(T, x, y)
            afficherTM(T, M)
        else:
            x = int(val_x)
            y = int(val_y)
            if not is_drapeau(T, x, y):
                creuser(T, M, x, y)
                print()
                afficherTM(T, M)
                print()
                if not creuser(T, M, x, y):
                    print("\nPERDU !")
                    finish = True
                else:
                    finish = False
            elif is_drapeau(T, x, y):
                print("\nIl y a un drapeau\n")

            win = False
            for g in range(len(T)):
                for h in range(len(T[g])):
                    if is_creuser(T, x, y):
                        win = True

        fin = time.time()

    # calculer cases creuser
    cases_creuser = 0
    for c in range(len(T)):
        for d in range(len(T[c])):
            if T[c][d] == 1:
                cases_creuser += 1

    if win:
        print("Score : TU AS DECOUVERT TOUTES LES CASES !")
        # score en % par rapport au nombres de mines dans le terrain
        print("Temps : ", int(fin - debut), "secondes")  # regarder sur internet comment ajouter un timer
    elif finish:
        print("Score : ", int((cases_creuser / case_libres) * 100), "% de cases decouvertes")
        # score en % par rapport au nombres de mines dans le terrain
        print("Temps : ", int(fin - debut), "secondes")  # regarder sur internet comment ajouter un timer


def afficherTM(T, M):
    for i in range(len(T)):
        for j in range(len(T[i])):
            if T[i][j] == 0:
                print(".  ", end="")
            elif T[i][j] == 1:
                print(M[i][j], " ", end="")
            elif T[i][j] == 2:
                print(".  ", end="")
            elif T[i][j] == 3:
                print("D  ", end="")
            elif T[i][j] == 4:
                print("D  ", end="")
        print("\n", end="")



"""
def afficher1(T):
    for i in range(len(T)):
        for j in range(len(T[i])):
            print(T[i][j], " ", end="")
        print("\n", end="")
"""

print("INFO : \n"
      "POUR POSER UN DRAPEAU ENTRER D EN X ET Y\n"
      "POUR LEVER UN DRAPEAU ENTRER F EN X ET Y\n")
T = niveau_de_jeu()
M = mines_autour(T)
# afficher1(T)
# print()
# afficher1(M)
# print()
play(T, M)
