## Temat pracy
Przewidywanie zachowania kursu zadanej waluty/akcji na giełdzie.

### Skupienie pracy
Metaoptymalizacja algorytmu populacyjnego.

### Czym jest osobnik
Osobnik otrzymuje parametry/metryki związane z dotychczasowym przebiegiem funkcji wartości waluty/akcji. Zwraca natomiast decyzję o zakupie/sprzedarzy danej waluty/akcji, chcąc zmaksymalizować zyski/zminimalizować straty po zadanym odstępie czasowym. Przykładowo po jednym dniu/tygodniu/miesiącu.

### Strategia ewaluacji
Osobnik będzie przepuszczany przez cały dotychczasowy wykres kursu/akcji i w zadanych odstępach czasowych (dzień/tydzień/miesiąc) będzie musiał podjąć decyzję o kupnie/sprzedarzy. Jego wartość funkcji fitness będzie proporcjonalna do końcowej wartości jego portfela.

### Strategia podejmowania decyzji
Strategia będzie reprezentowana przez drzewko `if`ów. Każdy `if` odpowiada jednej metryce związanej z przebiegiem funkcji i possada stałą, względem której ją porównuje. Przykładowo, jeżeli wszystkie zadane metryki będą większe od odpowiadającym im stałym, strategia zwróci decyzję "kup".

### Genotyp
Genotyp będzie reprezentował kolejne, wyżej wspomniane stałe w drzewku `if`ów, które reprezentuje strategię. Przykładowo może mieć 3 geny reprezentujące granice: aktualnej wartości waluty, pierwszej i drugiej pochodnej. W praktyce będzie to wykorzystywało bardziej zawiłe metryki, to jest jedynie przykład.