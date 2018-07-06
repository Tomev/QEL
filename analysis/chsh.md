---
title: "CHSH"
author: "Alicja Dutkiewicz"
date: "June 6, 2018"
output: html_document
header-includes:
   - \usepackage{physics}
---



#CHSH

##Wstęp

$$|\psi>=\frac{\cos\frac{\theta}{2}(|00>+|11>)+\sin\frac{\theta}{2}(|01>-|10>)}{\sqrt{2}}$$
$$CHSH=<ZZ>+<XX>+<ZX>-<XZ>$$

###Wartości oczekiwane:

$$<ZZ>=\cos\theta\\
<XX>=\cos\theta\\
<ZX>=\sin\theta\\
<XZ>=-\sin\theta\\
CHSH=2(\cos\theta+\sin\theta)$$



##Wykresy

Jedna linia = jeden job = 10 różnych $\theta$

Czarna linia = wartość oczekiwana

Przerywane linie = granice lokalnego realizmu

![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2-1.png)

![plot of chunk unnamed-chunk-3](figure/unnamed-chunk-3-1.png)





$$error=\sum_{\theta}(CHSH-2(\cos\theta+\sin\theta))^2$$


![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-1.png)

Ile razy faktycznie przekraczamy lokalny realizm?

![plot of chunk unnamed-chunk-6](figure/unnamed-chunk-6-1.png)

|       |0  |1  |2  |3  |4  |Łącznie jobów |Łącznie razy |
|:------|:--|:--|:--|:--|:--|:----------------|:--------------|
|ibmqx4 |11 |2  |5  |7  |16 |30 / 41          |97 / 410       |
|ibmqx5 |17 |13 |10 |0  |0  |23 / 40          |33 / 400       |

![plot of chunk unnamed-chunk-7](figure/unnamed-chunk-7-1.png)
