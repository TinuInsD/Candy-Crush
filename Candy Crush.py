#Realizare automatizare joc CandyCrush conform specificațiilor primite la laborator.
#Se dă o matrice care are 11 rânduri și 11 coloane. Fiecare element din matrice poate avea următoarele valori:
#0 - nu există nici o bomboană în acel element
#1 - bomboană de culoare roșie
#2 - bomboană de culoare galbenă
#3 - bomboană de culoare verde
#4 - bomboană de culoare albastră
#Se inițializează matricea cu bomboane de diverse culori (din cele enunțate mai sus) alese în mod aleator.
#Dacă se identifică una din următoarele formațiuni, acestea vor dispărea cumulând un număr de puncte după următoarea regulă:
#5 pct - linie de 3
#10 pct - linie de 4
#50 pct - linie de 5
#20 - L cu laturile de 3
#330 - T cu laturile de 3
#Fiecare din formațiunile mai sus menționate poate fi în rotită la 90 de grade în orice direcție.
#În momentul în care este identificată o astfel de formațiune, iar bomboanele respective dispar, toate bomboanele de pe coloană vor coborî în mod corespunzător umplând spațiile goale, respectiv dispărând dacă au apărut formațiuni noi.
#În momentul în care nu mai avem formațiuni noi vom căuta ca prin interschimbarea a două bomboane să formăm o nouă formațiune.
#Jocul continuă până când nu mai sunt opțiuni sau se realizează 10.000 de puncte. La finalul jocului se va cuantifica punctajul obținut. Se vor juca 100 de jocuri. Se va cuantifica numărul de puncte pentru fiecare joc și se va stabili media aritmetică a acestora.
#Termenul de realizare este de trei săptămâni, după prima săptămână se prezintă jocul funcțional pentru formațiunea linie de 3 bomboane.
#Obiectiv: Obținerea unui scor de 10.000 puncte din cât mai puține operațiuni de interschimbare. Pentru o evaluare corectă se va realiza media numărului de operațiuni de interschimbare a celor 100 de jocuri.

import random

# matrice si punctaj target (setam constantele)
TARGET_SCORE = 10000
N = 11

# folosim functia initialize matrix pentru a creea matricea (valori random)
def initialize_matrix():
    return [[random.randint(1, 4) for _ in range(N)] for _ in range(N)]
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(x) for x in row))
    print("\n")

# gasim formatiunile si liniile orizontale + verticale de 3, 4, 5.
def detect_matches(matrix):
    matches = []
    for i in range(N):
        for j in range(N - 2):
            if matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2] != 0:
                matches.append(("row", i, j, 3))
            if j <= N - 4 and matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2] == matrix[i][j + 3] != 0:
                matches.append(("row", i, j, 4))
            if j <= N - 5 and matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2] == matrix[i][j + 3] == matrix[i][
                j + 4] != 0:
                matches.append(("row", i, j, 5))
    for j in range(N):
        for i in range(N - 2):
            if matrix[i][j] == matrix[i + 1][j] == matrix[i + 2][j] != 0:
                matches.append(("col", i, j, 3))
            if i <= N - 4 and matrix[i][j] == matrix[i + 1][j] == matrix[i + 2][j] == matrix[i + 3][j] != 0:
                matches.append(("col", i, j, 4))
            if i <= N - 5 and matrix[i][j] == matrix[i + 1][j] == matrix[i + 2][j] == matrix[i + 3][j] == matrix[i + 4][
                j] != 0:
                matches.append(("col", i, j, 5))

    # gasim L si T
    for i in range(N - 2):
        for j in range(N - 2):
            # T
            if (
                    (matrix[i][j + 1] == matrix[i + 1][j] == matrix[i + 1][j + 1] == matrix[i + 1][j + 2] ==
                     matrix[i + 2][j + 1] != 0) or
                    (matrix[i + 1][j] == matrix[i][j + 1] == matrix[i + 1][j + 1] == matrix[i + 2][j + 1] ==
                     matrix[i + 1][j + 2] != 0)
            ):
                matches.append(("T", i, j, 3))
            # L
            if (
                    (matrix[i][j] == matrix[i + 1][j] == matrix[i + 2][j] == matrix[i + 2][j + 1] != 0) or
                    (matrix[i][j + 1] == matrix[i + 1][j + 1] == matrix[i + 2][j + 1] == matrix[i + 2][j] != 0)
            ):
                matches.append(("L", i, j, 3))
    return matches

# eliminam formatiunile si calculam punctajul
def remove_matches(matrix, matches):
    score = 0
    for match in matches:
        match_type, i, j, length = match
        if length == 3:
            score += 5
        elif length == 4:
            score += 10
        elif length == 5:
            score += 50
        elif match_type == "L":
            score += 20
        elif match_type == "T":
            score += 30

# dupa identificarea potrivirilor, setam valorile elementelor la 0, indicand astfel ca au fost eliminate
        if match_type == "row":
            for k in range(length):
                matrix[i][j + k] = 0
        elif match_type == "col":
            for k in range(length):
                matrix[i + k][j] = 0
        elif match_type in ["L", "T"]:
            for x in range(3):
                for y in range(3):
                    matrix[i + x][j + y] = 0
    return score


# aplicam functia apply gravity pentru a creea efectul de cadere (umplem spatiile goale cu elemente noi)
def apply_gravity(matrix):
    for j in range(N):
        empty_row = N - 1
        for i in range(N - 1, -1, -1):
            if matrix[i][j] != 0:
                matrix[empty_row][j] = matrix[i][j]
                empty_row -= 1
        for i in range(empty_row, -1, -1):
            matrix[i][j] = random.randint(1, 4)

# folosim functia try to create match pentru a incerca noi elemente, astfel vedem daca gasim o noua potrivire
def try_to_create_match(matrix):
    for i in range(N):
        for j in range(N):
            if j < N - 1:
# incercam pe orizontala
                matrix[i][j], matrix[i][j + 1] = matrix[i][j + 1], matrix[i][j]
                if detect_matches(matrix):
                    return True
                matrix[i][j], matrix[i][j + 1] = matrix[i][j + 1], matrix[i][j]
            if i < N - 1:
# incercam pe verticala
                matrix[i][j], matrix[i + 1][j] = matrix[i + 1][j], matrix[i][j]
                if detect_matches(matrix):
                    return True
                matrix[i][j], matrix[i + 1][j] = matrix[i + 1][j], matrix[i][j]
    return False


# creem mediul de joc
def play_game():
    matrix = initialize_matrix()
    score = 0
    moves = 0
    print("Matricea inițială:")
    print_matrix(matrix)
    while score < TARGET_SCORE:
        matches = detect_matches(matrix)
        while matches:
            score += remove_matches(matrix, matches)
            apply_gravity(matrix)
            matches = detect_matches(matrix)
# daca nu mai avem formatiuni, facem interschimbari pentru a creea altele noi
        if not matches:
            if not try_to_create_match(matrix):
                break
            moves += 1
# returnam scorul
    print(f"Scor final: {score}, Mutări: {moves}")
    return score, moves

# rulam jocul de 100 de ori (din functia play game) si calculam scorul mediu final
def run_multiple_games(num_games=100):
    total_score = 0
    total_moves = 0
    for _ in range(num_games):
        score, moves = play_game()
        total_score += score
        total_moves += moves
    print(f"Scor mediu: {total_score / num_games}")
    print(f"Număr mediu de mutări: {total_moves / num_games}")

run_multiple_games(100)