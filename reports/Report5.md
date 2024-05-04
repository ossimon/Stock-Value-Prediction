# Raport - etap 5 - 06.05.24

## Cache'owanie metryk
Okazało się, że obliczanie metryk zajmuje jedynie 0.03s. Postanowiliśmy więc ich nie cache'ować.

## Parametry CMA-ES
Dodaliśmy do konfiguracji nowy parametr i poprawiliśmy ograniczenia na parametry (czasami wybiegaliśmy poza ich dziedzinę).

## Metaoptymalizacja
Tym razem włączyliśmy dłuższy eksperyment w irace, z ograniczeniem liczby ewaluacji na 3000 w jednym przebiegu cma-es oraz 1000 uruchomień algorytmu przez irace. Obliczenia zajęły większą część nocy.

## Wykres zbieżności algorytmu dla parametrów domyślnych i zoptymalizowanych
Poniższy wykres reprezentuje porównanie przebiegów zysku w zależności od iteracji algorytmu dla parametrów domyślnych i zoptymalizowanych przez irace. Warto zauważyć, że w drugim przypadku iteracji było znacznie mniej, prawdopodobnie ze względu na większy rozmiar populacji.

![convergence](../irace_result_comparison/Profit%20comparison.jpg)

Jak widać, zysk z domyślnymi parametrami jest nieznaczny względem tego ze zoptymalizowanymi. Przyspiesza on jednak wraz z iteracjami i nie widać by zbiegał do konkretnej wartości. Włączenie go więc na dłużej mogłoby poprawić wyniki. Wyniki dla parametrów zoptymalizowanych są mniej przewidywalne. Występują w nich częste skoki zysku, a następnie wypłaszczenia na kilka iteracji. Dobrze byłoby uruchomić o wiele dłuższe eksperymenty, jednak nasze zasoby na to nie pozwalają.