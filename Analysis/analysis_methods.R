library(tidyverse)
library(magrittr)


print_basic_info <- function(data){
  #Works assuming usual column names.
  
  print('Experiments:')
  str_split_fixed(data$circuit, '_', 2)[,1] %>% unique %>% print
  
  print('Data from backends:')
  data$backend %>% unique %>% print()
  
  print('Date range:')
  c(min(data$date), max(data$date)) %>% print()
  
  print('Number of jobs:')
  data$id %>% n_distinct %>% print
}


extract_circuit_data <- function(data, ..., pattern = '_', circuit_column = 'circuit'){
  
  #A convenient way to pass the arguments
  params = list(...)
  var_names = names(params)
  var_positions = as.numeric(params)
  
  #Split the circuit names
  circuit_data = str_split_fixed(
    data[[circuit_column]],
    pattern,
    max(var_positions)
    )
  
  #Create new columns (names of parameters)
  for(i in 1:length(params)){
    data[[var_names[i]]] = circuit_data[,var_positions[i]]
  }
  
  return(data)
}

chsh_test <- function(data, print = TRUE){
  
  "
  Process chsh-test data
  
  Currently works if:
    - names of test circuits are CHSH-test_AB(_...),
      AB = XX, XZ, ZX, ZZ,
      anything can follow after '_'
    - the following names of columns are used:
      - names of circuits: 'circuit'
      - job ids: 'id'
      - state names: 'variable'
      - counts: 'value'
  The label good=TRUE is assigned to jobs with chsh>2.
  
  Output: the data frame with filtered out test circuits and new columns 'chsh' and 'good'.
  
  If `print` prints how many jobs were selected
  
  TO DO: general column names, threshold value, more general tests?
  "
  
  #Choose the data from chsh test
  test_data = data %>%
    filter(str_split_fixed(circuit,'_',2)[,1] == 'CHSH-test')
  
  #Extract observable from circuit name
  test_data %<>% extract_circuit_data(observable = 2)
  
  #Aggregate
  test_data %<>%
    #Sign 
    mutate(
      value = value*
        ifelse(variable %in% c('00','11'), 1, -1)*
        ifelse(observable == 'XZ', -1, 1)
    ) %>%
    #Calculate expected value of each observable
    group_by(id, observable) %>%
    summarise(value = sum(value)/sum(abs(value))) %>%
    #Calculate CHSH parameter
    summarise(chsh = sum(value)) %>%
    #Good job threshold
    mutate(good = (abs(chsh)>2))
  
  if(print){
    str_c('Jobs selected: ', sum(test_data$good), ' out of ', nrow(test_data))
  }
  
  #Return the filtered data frame with test data joined using job id
  left_join(
    data %>%
      filter(str_split_fixed(circuit,'_',2)[,1] != 'CHSH-test'),
    test_data,
    'id'
  )
}

process_chsh <- function(data, ..., barrier = F){
  #Extract the circuit data for usual chsh naming convention
  
  data %<>% extract_circuit_data(theta0 = 2, observable = 3)
  if(barrier){
    data %<>% extract_circuit_data(barrier = 4)
    data$barrier = (data$barrier == 'B')
  }
  
  #Numeric theta from string
  data %<>% left_join(
    tibble(
      theta0 = unique(data$theta0),
      theta = theta0 %>%
        str_replace('pi','*pi') %>%
        sapply(function(x) eval(parse(text = x)))
    ),
    'theta0'
  )
  
  #Whether the result of the measurement is +1 or -1
  data %<>% mutate(
    sign = (-1)^((observable == 'XZ')+(variable %in% c ('01','10')))
  )
  
  
  return(data)
}

process_mermin <- function(data, ..., barrier = F){
  #Extract the circuit data for usual mermin naming convention
  
  data %<>% extract_circuit_data(observable = 2)
  if(barrier){
    data %<>% extract_circuit_data(barrier = 3)
    data$barrier = (data$barrier == 'B')
  }
  data %<>% mutate(
    sign = (-1)^((observable == 'XXX')+(variable %in% c('000','011','101','110')))
  )
  
  return(data)
}

agg_data <- function(data){
  #For bell-type experiments
  #Calculates the expected value and its error from all the jobs
  data %>%
    group_by(observable, add = T) %>%
    summarise(total = sum(value), value = sum(sign*value)/total,
              var = (1+value)*(1-value)/total) %>%
    summarise(
      value = sum(value), dv = sqrt(sum(var))
    )
}
summary_table <- function(data, ...){
  data %>%
    mutate(
      result = sprintf('%.4f +/- %.4f', value, dv)
    ) %>%
    select(..., result) %>%
    knitr::kable()
}

pi_axis <- function(){
  scale_x_continuous(breaks = 0:7*2*pi/8,
                     minor_breaks=waiver(),
                     labels=c(0,sapply(1:7,function(x) bquote(frac(.(x)*pi,8)))))
  
}

chsh_plot <- function(data){
  #Fit and plot a sinusoid
  
  #TO DO: different coefficients for grouped data
  
  
  data %<>%
    mutate(chsh = value, delta_chsh = dv, chsh_theory = 2*(cos(theta)+sin(theta)))
  
  #Fit
  eta = lm(chsh ~ 0+chsh_theory, data = data) %>% coef
  
  #Plot
  ggplot(data, aes(x = theta, y = chsh))+
    geom_errorbar(aes(ymin = chsh - delta_chsh, ymax = chsh + delta_chsh),
                  width = 0.03)+
    geom_point(size = 0.05, alpha = 0.5)+
    annotate('text', label = str_c('eta = ', round(eta,3)),
             x = min(data$theta)+0.2, y = 0)+
    geom_hline(yintercept = c(2,-2),lty=2)+
    stat_function(fun=function(x) 2*(cos(x)+sin(x)))+
    stat_function(fun=function(x) 2*eta*(cos(x)+sin(x)))+
    pi_axis()
  }

process_signaling <- function(data){
  #Needed column names: observable, variable, value
  
  #Number of qubits - extracted from length of observables
  n_qubits = max(str_length(data$observable))
  
  #Calculate the expected values
  lapply(1:n_qubits, function(i){
    data %>%
      mutate(
        my_base = str_sub(observable, i, i),
        other_base = str_c(str_sub(observable,0, i-1),'_',str_sub(observable,i+1, i+n_qubits)),
        my_sign = (-1)^as.numeric(str_sub(variable,i,i))
      ) %>%
      group_by(my_base, other_base, add = T) %>%
      summarise(total = sum(value),
                value = sum(my_sign*value)/total,
                dv =sqrt((1-value)*(1+value)/total))
  }) %>% 
    bind_rows(.id = 'qubit') %>%
    mutate(
      index = str_c(qubit, my_base)
    )
}


plot_signaling <- function(data,
                           x = quo(index),
                           y = quo(value),
                           error = quo(dv),
                           facet_x = NULL,
                           facet_y = NULL){
  
  #TODO: align plots, enable adding custom layers
  
  data %<>% group_by(!!x)
  if(!is.null(facet_x)){
    data %<>% group_by(!!facet_x, add = TRUE)
  }
  if(!is.null(facet_y)){
    data %<>% group_by(!!facet_y, add = TRUE)
  }
  
  #The means
  p1 = ggplot(
    data %>%
      mutate(other_base = other_base %>% str_replace('_','')),
    aes_(x=x, y = y, colour = quo(other_base))
  )+
    geom_point()+
    geom_errorbar(aes(ymin = !!y-!!error, ymax = !!y+!!error), width = 0.1)+
    facet_grid(rows = facet_x, cols = facet_y)
    #labs(x = 'Observable', y = 'Expected value')
  
  #The delta/sigma bars
  p2 = ggplot(
    data %>%
      summarise(
        delta = (max(value)-min(value)),
        sigma = sqrt(sum(dv^2)),
        q = delta/sigma)
  )+
    geom_col(aes_string(x = x, y = 'q'))+
    #labs(x = 'Observable', y = expression(Delta/sigma))+
    geom_hline(yintercept = 3, lty = 2)+
    facet_grid(rows = facet_x, cols = facet_y)
  
  print(p1)
  print(p2)
}
