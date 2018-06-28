---
title: 'Tworzenie par Bella - test backendÃ³w '
author: "Alicja Dutkiewicz"
date: "April 22, 2018"
output:
  html_document: default
  pdf_document: default
---




##Podsumowanie:

* chisq:suma kwadartów błędów
$\chi^2:=\sum_{|xy>}(N(|xy>)-\mathbf{E}(|xy>))^2$ - w całym dokumencie; w tej tabelce średnie $\chi^2$ dla danego backendu

* Mxy: średnia liczba zliczeń w stanie xy

* Bxy: średni błąd w stanie xy $|N(|xy>)-\mathbf{E}(|xy>)|$

|backend |      M00|      M11|      B00|       B11|       B01|       B10|      chisq|
|:-------|--------:|--------:|--------:|---------:|---------:|---------:|----------:|
|ibmqx2  | 486.7674| 465.9942| 26.47674|  46.12209|  31.53488|  39.70349|   7396.442|
|ibmqx4  | 524.9112| 393.8171| 20.94671| 118.18295|  50.03197|  55.23979|  21483.290|
|ibmqx5  | 469.2685| 329.8249| 63.68093| 182.17510| 115.33852| 109.56809| 107715.105|

###Rozkład błędów w doświadczeniach:

![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-3-1.png)![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-3-2.png)![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-3-3.png)

###Histogram $\chi^2$:

![plot of chunk unnamed-chunk-4](figure/unnamed-chunk-4-1.png)

###Rozkład błędów dla każdego stanu:

![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-1.png)![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-2.png)![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-3.png)

##Jakościowe obserwacje

Średnio najmniejsze błędy robi ibmqx2, największe ibmqx5. Najmniejsze maksymalne błędy robi ibmqx4.

Stan 00 jest zawsze preferowany w stosunku do 11 - w ibmqx4 i ibmqx5 więcej niż $\sigma$.

Stany 10 i 01 występują mniej więcej tak samo często.


Na ibmqx5 zdarza się, że zliczeń 01+10 będzie więcej niż 00+11 - łącznie 33 na 172 doświadczenia (20%), na innych backendach takie sytuacje nie występują.

ibmqx5 robił znacząco mniejsze błędy (chisq mniejsze o rząd wielkości i porównywalne z ibmqx2 i ibmqx4) w niedzielę 15 IV (pomiary od 12AM, po 1AM 16IV znaczący wzrost błędów).
