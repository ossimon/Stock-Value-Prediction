## Metaoptymalizacja

Proces metaoptymalizacji został przeprowadzony na następujących kursach w okresie 2023-2024:
- ausd/pln
- chf/pln
- eur/pln
- gbp/pln
- hkd/pln
- jpy/pln
- usd/pln

Domyślne parametry dla naszego programu to:
- CMA_active_injected = 0
- CMA_cmean = 1
- CMA_on = 1
- CMA_rankmu = 1
- CMA_rankone = 1
- CSA_dampfac = 1
- popsize = 100
- tolfun = -11

Parametry uzyskane w wyniku metaoptymalizacji to:
- CMA_active_injected = -0.4603
- CMA_cmean = 1.2867
- CMA_on = -1.0547
- CMA_rankmu = 2.0718
- CMA_rankone = 3.2485
- CSA_dampfac = 8.2784
- popsize = 34
- tolfun = 0.9803

## Wyniki

### USD/PLN 2023-2024

Porównajmy wyniki optymlalizacji z wynikami bez optymalizacji dla danych na których przeprowadzono metaoptymalizację:

(USD/PLN default, 2023-2024)

```
Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
    1    100 -1.000094514310979e+06 1.0e+00 9.50e+00  9e+00  1e+01 0:00.7
    2    200 -1.000664458453474e+06 1.0e+00 9.27e+00  9e+00  9e+00 0:01.4
    3    300 -1.001192705526031e+06 1.0e+00 9.26e+00  9e+00  9e+00 0:02.1
    8    800 -1.003864927634654e+06 1.0e+00 1.11e+01  1e+01  1e+01 0:05.6
   14   1400 -1.008049231115826e+06 1.0e+00 1.78e+01  2e+01  2e+01 0:09.8
   15   1500 -1.008988068266963e+06 1.0e+00 1.95e+01  2e+01  2e+01 0:10.6
```

Jak widać uzyskano przychód na poziomie 7 tyś.

Spróbujmy teraz zastosować uzyskane parametry:

```
Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
    1     34 -1.000055159851883e+06 1.0e+00 9.96e+00  1e+01  1e+01 0:00.2
    2     68 -1.000424761858914e+06 1.0e+00 9.93e+00  1e+01  1e+01 0:00.5
    3    102 -1.001124680801594e+06 1.0e+00 9.90e+00  1e+01  1e+01 0:00.7
   16    544 -1.012590251957348e+06 1.0e+00 9.86e+00  1e+01  1e+01 0:03.9
   33   1122 -1.006768105124315e+06 1.0e+00 9.91e+00  1e+01  1e+01 0:08.0
   41   1394 -1.014665646940682e+06 1.0e+00 9.94e+00  1e+01  1e+01 0:10.0

```

Uzyskano przychód na poziomie 16 tyś. Zobaczmy wykres kupna/sprzedaży:

Zysk z metaoptymalizacji jest realny i prawie podwoił nasz przychód.

### USD/PLN 2022-2023

Wykonajmy teraz ten sam test jednak dla okresu który nie był uwzględniony w procesie metaoptymalizacji:

Domyślne parametry:
```
Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
    1    100 -1.000485139667344e+06 1.0e+00 9.50e+00  9e+00  1e+01 0:00.7
    2    200 -1.000000000000000e+06 1.0e+00 9.13e+00  9e+00  9e+00 0:01.4
    3    300 -1.000000000000000e+06 1.0e+00 8.84e+00  9e+00  9e+00 0:02.1
    5    500 -1.000000000000000e+06 1.0e+00 8.43e+00  8e+00  8e+00 0:03.6
termination on tolflatfitness=1 (Mon Apr 22 09:02:05 2024)
final/bestever f-value = -1.000000e+06 -1.000485e+06 after 501/18 evaluations
```

Metaoptymalizacja:
```
Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
    1     34 -9.999997327899837e+05 1.0e+00 9.96e+00  1e+01  1e+01 0:00.3
    2     68 -1.000000000000000e+06 1.0e+00 9.93e+00  1e+01  1e+01 0:00.5
termination on tolfun=9.556524994289589 (Mon Apr 22 09:07:02 2024)
final/bestever f-value = -1.000000e+06 -1.000000e+06 after 69/35 evaluations
```

W obu przypadkach nie udało się uzyskać żadnego sensownego wyniku. CMA-ES stopował proces optymalizacji po zaledwie kilku iteracjach.
Możliwe przyczyny tego zjawiska to:
- CMA-ES po prostu nie radzi sobie z wszystkimi danymi przy defaulotwych parametrach
- bug w programie
- błąd w danych

### USD/EUR 2023-2024

Przeprowadźmy teraz test dla kursu USD/EUR w latach 2023-2024:

Domyślne parametry:
```
Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
    1    100 -1.000083162750817e+06 1.0e+00 9.46e+00  9e+00  9e+00 0:00.7
    2    200 -1.000538016758026e+06 1.0e+00 9.17e+00  9e+00  9e+00 0:01.4
    3    300 -1.000924862113174e+06 1.0e+00 9.02e+00  9e+00  9e+00 0:02.1
    8    800 -1.003122896620037e+06 1.0e+00 9.87e+00  1e+01  1e+01 0:05.7
   14   1400 -1.006844307867807e+06 1.0e+00 1.54e+01  2e+01  2e+01 0:10.0
termination on timeout=10 (Mon Apr 22 09:09:18 2024)
```


Metaoptymalizacja:
```
Iterat #Fevals   function value  axis ratio  sigma  min&max std  t[m:s]
    1     34 -1.000038788661262e+06 1.0e+00 9.96e+00  1e+01  1e+01 0:00.2
    2     68 -1.000495602739199e+06 1.0e+00 9.93e+00  1e+01  1e+01 0:00.5
    3    102 -1.001103703191457e+06 1.0e+00 9.90e+00  1e+01  1e+01 0:00.7
   16    544 -1.008418454338818e+06 1.0e+00 9.86e+00  1e+01  1e+01 0:03.9
   33   1122 -1.011593237778544e+06 1.0e+00 9.96e+00  1e+01  1e+01 0:08.0
   42   1428 -1.012845676055386e+06 1.0e+00 9.98e+00  1e+01  1e+01 0:10.2
termination on timeout=10 (Mon Apr 22 09:10:50 2024)
```

Jak widać ponownie metaotpymalizacja poprawiła wyniki.