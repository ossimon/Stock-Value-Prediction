## Raport 2 etapu - 18.03.24

### Narzędzie metaoptymalizacji
Zainstalowaliśmy i przetestowaliśmy wtępnie `irace`.

### Użycie irace
Link z oryginalną isntrukcją: https://mlopez-ibanez.github.io/irace/

1) Należy zainstalować R, a w nim pakiet irace (w przypadku posiadania R dobrze jest zaktualizować go do najnowszej wersji przed instalacją irace).
2) Zarówno R, jak i irace powinny być w PATH!
3) Aby użyć irace wystarczy przejść do katalogu irace/Instances i uruchomić w terminalu irace [katalog z irace]\bin\x64\irace.exe

Po wywołaniu komendy irace znajdzie plik `scenario.txt`, który przechowuje parametry wywołania algorytmu metaoptymalizacji (np. maksymalna liczba wywołań algorytmu).

Parametry samego algorytmu optymalizacji (docelowo CMA-ES) są w `parameters.txt`.

Katalog `Instances` powinien zawierać przykłady uczące dla modelu (przebiegi kursów walut).

Plik `configurations.txt` powinien zawierać domyślną konfigurację algorytmu, od której zaczyna pracę irace.

Plik `forbidden.txt` przechowuje niedozwolone konfiguracje parametrów algorytmu.

Irace uruchamia algorytm z użyciem `targer-runner.bat`. To w nim wyspecyfikowane jest jak uruchomić nasz własny program.

Program zawierający optymalizację samego problemu powinien wypisywać wartość końcową osiągniętej funkcji kosztu (i nic więcej).
