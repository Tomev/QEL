---
title: "Bell pairs - errors summary"
author: "Alicja Dutkiewicz"
date: "May 24, 2018"
output: html_document
---




#Means and medians

|backend |job      | mean 00[%]| mean 01[%]| mean 10[%]| mean 11[%]|
|:-------|:--------|----------:|----------:|----------:|----------:|
|ibmqx2  |bell     |  47.535883|   3.079579|   3.877294|  45.507245|
|ibmqx4  |antibell |   9.085036|  46.566083|  42.372296|   1.976586|
|ibmqx4  |bell     |  51.260858|   4.885935|   5.394510|  38.458696|
|ibmqx5  |antibell |  16.571232|  35.370060|  41.141889|   6.916820|
|ibmqx5  |bell     |  45.827000|  11.263528|  10.700009|  32.209463|



|backend |job      | median 00[%]| median 01[%]| median 10[%]| median 11[%]|
|:-------|:--------|------------:|------------:|------------:|------------:|
|ibmqx2  |bell     |    47.851562|     2.929688|     3.320312|    45.800781|
|ibmqx4  |antibell |     8.789062|    46.679688|    42.382812|     1.855469|
|ibmqx4  |bell     |    51.171875|     4.296875|     5.371094|    38.964844|
|ibmqx5  |antibell |    11.914062|    39.160156|    45.800781|     2.441406|
|ibmqx5  |bell     |    50.292969|     6.640625|     6.250000|    36.132812|


#$\chi^2$ plots

Error probability $p$ - mean of counts in incorrect states
$$\chi^2=N\sum\frac{(\frac{n_i}{N}-p_i)^2}{p_i}$$
$n_i$ - counts in i-state, $p_i$ - $\frac{1-p}{2}$ for correct states, $p$ for incorrect states 


![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2-1.png)![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2-2.png)![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2-3.png)![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2-4.png)![plot of chunk unnamed-chunk-2](figure/unnamed-chunk-2-5.png)

#FWHM
FWHM = Full Width at Half Maximum = 3. quartile - 2. quartile

(w punktach procentowych)


|backend job     | FWHM 00[%]| FWHM 01[%]| FWHM 10[%]| FWHM 11[%]|
|:---------------|----------:|----------:|----------:|----------:|
|ibmqx2_bell     |   1.953125|  0.9765625|   1.074219|  2.5390625|
|ibmqx4_antibell |   1.953125|  2.9296875|   2.636719|  0.7812500|
|ibmqx4_bell     |   3.125000|  1.5136719|   1.074219|  3.7597656|
|ibmqx5_antibell |   2.539062|  4.0039062|   3.515625|  0.9765625|
|ibmqx5_bell     |   3.808594|  3.0273438|   2.050781|  3.8085938|

#Summary - probability of error

mean $\pm$ WFHM

ibmqx2_bell : .....0.070  +/-  0.007   
ibmqx4_antibell : 0.111  +/-  0.012   
ibmqx4_bell : .....0.103  +/-  0.010   
ibmqx5_antibell : 0.235  +/-  0.015   
ibmqx5_bell : .....0.220  +/-  0.019   

#Histograms of errors

![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-1.png)![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-2.png)![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-3.png)![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-4.png)![plot of chunk unnamed-chunk-5](figure/unnamed-chunk-5-5.png)




#Quartiles:


|   |    0%|   25%|   50%|   75%|  100%|
|:--|-----:|-----:|-----:|-----:|-----:|
|00 | 38.57| 46.68| 47.85| 48.63| 52.44|
|01 |  1.46|  2.44|  2.93|  3.42|  8.79|
|10 |  1.56|  2.83|  3.32|  3.91| 24.32|
|11 | 24.71| 44.53| 45.80| 47.07| 50.68|


|   |    0%|   25%|   50%|   75%|  100%|
|:--|-----:|-----:|-----:|-----:|-----:|
|00 |  5.57|  7.91|  8.79|  9.86| 17.58|
|01 | 39.26| 45.21| 46.68| 48.14| 53.52|
|10 | 33.11| 41.11| 42.38| 43.75| 51.46|
|11 |  0.49|  1.56|  1.86|  2.34|  9.08|


|   |    0%|   25%|   50%|   75%|  100%|
|:--|-----:|-----:|-----:|-----:|-----:|
|00 | 45.70| 49.71| 51.17| 52.83| 58.50|
|01 |  2.44|  3.71|  4.30|  5.22| 13.96|
|10 |  2.93|  4.88|  5.37|  5.96|  9.28|
|11 | 27.93| 36.77| 38.96| 40.53| 44.34|


|   |   0%|   25%|   50%|   75%|  100%|
|:--|----:|-----:|-----:|-----:|-----:|
|00 | 6.84| 10.84| 11.91| 13.38| 56.25|
|01 | 4.79| 36.91| 39.16| 40.92| 45.21|
|10 | 5.08| 43.85| 45.80| 47.36| 53.22|
|11 | 1.07|  2.05|  2.44|  3.03| 42.19|


|   |   0%|   25%|   50%|   75%|  100%|
|:--|----:|-----:|-----:|-----:|-----:|
|00 | 9.67| 48.14| 50.29| 51.95| 54.98|
|01 | 4.10|  5.76|  6.64|  8.79| 45.70|
|10 | 3.42|  5.57|  6.25|  7.62| 43.65|
|11 | 2.05| 33.59| 36.13| 37.40| 41.21|
