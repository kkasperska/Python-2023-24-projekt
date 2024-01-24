# **Simon Says**

<br>
<div style="text-align: right"><b>Kamila Kasperska</b></div>

## **1. Wstęp**
Program wykonany jako projekt zaliczeniowy z kursu Język Python w roku akademickim 2023/2024.

----------
<br>

## **2. Opis programu**
Program jest wariacją tradycyjnej gry w Simon Says odwzorowującą minigrę z popularnej gry wideo Among Us.
<br>
<br>
Jest to gra logiczna polegająca na podążaniu za wskazaną sekwencją przycisków.
<br>
<br>
Plansza składa się z dwóch ekranów, po 9 przycisków na każdym z nich. Na lewym ekranie ukazuje się sekwencja przycisków zaczynająca się od jednego elementu. Po wyświetleniu sekwencji należy powtórzyć ją wybierając odpowiednie przyciski na prawym ekranie. Po poprawnym wskazaniu sekwencji zostaje ona powiększona o jeden losowo wybrany przycisk. Gra kończy się w momencie pomyłki gracza.
<br>
<br>
Program składa się z dwóch klas: Button i Game oraz funkcji main.

Klasa Button odpowiada za przyciski. Zawiera funkcje:

* draw odpowiedzialną za rysowanie przycisku;

* is_cliked zwracającą boola informującego czy przycisk został wciśnięty;

* animation odpowiedzialną za animowanie zaświecania się przycisku.

Klasa Game odpowiada za tworzenie i przebieg gry. Zawiera funkcje:

* get_high_score i set_high_score odczytujące i zapisujące najwyższy wynik do pliku;

* events zajmującą się obsługą eventów QUIT (zapisuje nowy najwyższy wynik i zamyka okno gry) oraz MOUSEBUTTONDOWN (sprawdza czy i który przycisk został wciśnięty);

* draw zajmującą się rysowaniem elementów takich jak napisy i przyciski na ekranie gry;

* new rozpoczynającą nową grę;

* update zajmującą się generowaniem i wyświetlaniem sekwencji oraz sprawdzaniem poprawności sekwencji wprowadzonej przez gracza;

* game_over_animation odpowiedzialną za animację oznaczającą przegraną;

* run będącą główną pętlą przebiegu gry.

Funkcja main pobiera ustawienia z pliku json, tworzy nową instancję gry i zajmuje się jej przebiegiem.
<br>
<br>

----------
<br>

## **3. Sposób uruchomienia**
Aby uruchomić program należy zainstalować bibliotekę pygame oraz wywołać komendę:<br>
`python3 main.py`<br>
a następnie przystąpić do gry.

----------
<br>

## **4. Klawiszologia**

LPM (lewy przycisk myszy) - wybór przycisku

----------
<br>