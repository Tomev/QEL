# Job data gatherer

Job data gatherer is a set of class for parsing and gathering jobs. It currently has 2 methods of jobs gathering default
and singular one. 

## Gatherers

* Default job gatherer, launched by JobDataGatherer.py script, gathers job in one loop, breaking it means necessity to
restart whole process which can be a pain, especially if there's a lot of jobs to download. Since qiskit 0.10.X it's
recommended way to download jobs as it happens that with proper internet connection jobs can be gathered with speed of
200 jobs per second. Parsing takes a little longer however that should pose a script-breaking problem. 

* Singular job data gatherer is a job data gathering method that connects to the IBM and downloads one job at the time 
and parses it to the csv file. When there's a problem with connection it breaks, however, can be resumed basing on
already generated CSV. It's slower but more reliable than default job data gatherer and it's recommended since qiskit 
0.6.X.

## Parser

There currently is only one parser - aReportConverter. It converts csv with data gathered via singular job data gatherer
to a form more suited for automatic analysis with R.
