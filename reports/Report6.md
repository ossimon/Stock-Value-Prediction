# Raport - etap 6 - 20.05.24

## Metaoptymalizacja na Aresie

TODO Oskar

## Opracowanie wyników

Domyślne parametetry dla algorytmu CMA-ES:

```
--CMA_active_injected 0
--CMA_cmean 1
--CMA_on 1
--CMA_rankmu 1.0
--CMA_rankone 1.0
--CSA_dampfac 1
--popsize 4 + 3 * np.log(N)
--sigma 10
```

Parametery znalezione przy użyciu Irace:

```
--CMA_active_injected 85.0515
--CMA_cmean -0.6412
--CMA_on -77.8581
--CMA_rankmu 0.6389
--CMA_rankone 0.3362
--CSA_dampfac 6.6756
--popsize 1687
--sigma 8.6406
```

Algorytm był metaoptymalizowany na kursie Dollar/Euro w przedziale 01/01/2023 - 01/01/2024. Wyniki dla parametrów zoptymalizowanych oraz nie wyglądają następująco:

### Domyślne parametry

Uzyskany wynik:

> 1_035_024 USD

Czas trwania:

> 1:25.9 s

Ilość iteracji i ewaluacji

> Iter: 501
> Eval: 10020

Wizualizacja:

![img](./_img/usd-eur-23-24-def.png)

### Meta parametery

Uzyskany wynik:

> 1_040_192 USD

Czas trwania:

> 1:19.7 s

Ilość iteracji i ewaluacji

> Iter: 6
> Eval: 10122

Wizualizacja:

![img](./_img/usd-eur-23-24-meta.png)

### Porównanie wyników

Porównajmy zbieżność dla obu przykładów:

![img](./_img/usd-eur-23-24-con-10000-eval.png)

Ponieważ w każdej iteracji dla parametrów z irace wykonywaliśmy więcej ewaluacji, zmapujmy wykres w dziedzine ewaluacji:

![img](./_img/usd-eur-23-24-con-10000-eval-axis.png)

(Różnica w miejscu startu lini pomarańczowej i niebieskiej wynika z sposobu logowania danych przez CMA-ES, są one logowane na podstawie iteracji nie nr. ewaluacji)

Jak widać już w pierwszej iteracji, CMA-ES z parametrami Irace znalazł optymalny wynik i nie udało mu się go poprawić. Domyślne parametery, zaczynają z gorszym wynikiem, jednak wygląda na to że w większej ilości ewaluacji, wyprzedzą one parametery irace'owe

### Zwiększenie liczby ewaluacji

Zwiększamy liczbe ewaluacji z 10k do  100k, oraz ustawliśmy timeout na 15min

### Domyślne parametery

Uzyskany wynik:

> 1_073_711 USD

Czas trwania:

> 15:00.00 s

Ilość iteracji i ewaluacji

> Iter: 5357
> Eval: 107140

Wizualizacja:

![img](./_img/usd-eur-23-24-def-20000-eval.png)

### Meta parametery

Uzyskany wynik:

> 1_038_936 USD

Czas trwania:

> 13:13.6 s

Ilość iteracji i ewaluacji

> Iter: 51
> Eval: 86037

> Termination on tolfunhist=1e-12

Wizualizacja:

![img](./_img/usd-eur-23-24-meta-20000-eval.png)

### Porównanie wyników

Porównajmy zbieżność dla obu przykładów:

![img](./_img/usd-eur-23-24-con-200000-eval-axis.png)

Dodajmy do wykresu linie wyznaczającą liczbę 10k ewaluacji użytych w irace:

![img](./_img/usd-eur-23-24-con-200000-eval-line.png)

Jak widać domyślne parametery okazują się być dużo skuteczniejsze niż parametery zoptymalizowane przez irace. Widzimy także wpływ wybranej liczby ewaluacji do trenowania irace na uzyskany wynik.