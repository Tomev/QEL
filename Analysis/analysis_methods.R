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
    max(var_positions)+1
    )
  
  #Create new columns (names of parameters)
  for(i in 1:length(params)){
    data[[var_names[i]]] = circuit_data[,var_positions[i]]
  }
  
  return(data)
}

state_sign <- function(v){
  #Assign the measurement result (eigenvalue) to the measured state
  (-1)^str_count(v, '1')
}

process_bell <- function(data, ..., parameter, name, minus_obs, barrier){
  
  #Filter experiments
  data %<>%
    extract_circuit_data(experiment = 1) %>%
    filter(experiment == name)
  
  #The result of experiment(+/-1)
  data %<>% extract_circuit_data(observable = 2+parameter) %>%
    mutate(sign = state_sign(variable)*(-1)^(observable %in% minus_obs))
  
  #Process barrier
  if(barrier){
    data %<>% extract_circuit_data(barrier = 4)
    data %<>% mutate(barrier = ifelse(barrier == 'B', 'With', 'Without'))
    data %<>% group_by(barrier)
  }
  
  
  #Extract and process information about theta
  if(parameter){
    
    data %<>% extract_circuit_data(theta0 = 2)
    
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
    
    data %<>% group_by(theta, add = TRUE)
  }
  
  return(data)
}

agg_data <- function(data, print_kable = FALSE){
  #Calculates the expected value and its error from all the jobs
  #For bell-type experiments
  table = data  %>%
    group_by(observable, add = T) %>%
    summarise(total = sum(value), value = sum(sign*value)/total,
              var = (1+value)*(1-value)/total) %>%
    summarise(
      value = sum(value), dv = sqrt(sum(var))
    )
  if(print_kable){
    table %<>%
      mutate(
        result = sprintf('%.4f +/- %.4f', value, dv)
      ) %>%
      select(-value, -dv) %>%
      knitr::kable()
  }
  return(table)
}

chsh_test <- function(data, ..., print = TRUE, filter = TRUE){
  
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
  If `filter` only the good jobs are left.
  
  If `print` prints how many jobs were selected
  
  TO DO: general column names, threshold value, more general tests?
  TO DO: Plot
  "
  
  #Choose and process the data from chsh test
  test_data = data %>% process_bell(
    name = 'CHSH-test',
    parameter = FALSE,
    minus_obs = c('XZ', 'YY'),
    barrier = FALSE
    )
  
  #Calculate the CHSH parameter
  test_data %<>%
    group_by(id) %>%
    agg_data %>%
    select(-dv, chsh = value) %>%
    #Good job threshold
    mutate(good = (abs(chsh)>2))
  
  if(print){
    str_c(
      'CHSH test. Jobs selected: ',
      sum(test_data$good),
      ' out of ',
      nrow(test_data)
      ) %>% print
  }
  
  #Return the filtered data frame with test data joined using job id
  data %<>% 
    extract_circuit_data(experiment = 1) %>%
    filter(experiment != 'CHSH-test') %>%
    left_join(test_data,'id')
  
  if(filter){data %<>% filter(good)}
  
  return(data)
}

process_chsh <- function(data, ..., barrier = F){
  #Extract the circuit data for usual chsh naming convention
  data %>% process_bell(
    name = 'CHSH',
    parameter = T,
    barrier = barrier,
    minus_obs = c('XZ', 'XY')
    )
}

process_mermin <- function(data, ..., barrier = F){
  #Extract the circuit data for usual mermin naming convention
  
  data %>% process_bell(
    name = 'Mermin',
    parameter = FALSE,
    minus_obs = 'XXX',
    barrier = barrier
  )

}

pi_axis <- function(){
  scale_x_continuous(breaks = 0:7*2*pi/8,
                     minor_breaks=waiver(),
                     labels=c(0,sapply(1:7,function(x) bquote(frac(.(x)*pi,8)))))
  
}

bell_fit_plot <- function(data, experiment){
  #Fit and plot a function
  #Different fits for each group if data is grouped
  
  #Theoretical expected value
  fun <- switch(experiment,
                CHSH = function(x) 2*(cos(x)+sin(x)),
                Mermin = function(x) -4*cos(x))
  data %<>%
    mutate(theory = fun(theta))
  
  #Local realism
  lr_lims <- switch(experiment,
                    CHSH = c(-2,2),
                    Mermin = c(-2, 2))
  
  #Fit
  eta_df = data %>% do(eta = lm(value ~ 0+theory, data = .) %>% coef) %>%
    mutate(eta = eta[[1]])
  
  #Plot
  p = ggplot(data, aes(x = theta, y = value))+
    geom_errorbar(aes(ymin = value - dv, ymax = value + dv),
                  width = 0.03)+
    geom_point(size = 0.05, alpha = 0.5)+
    #annotate('text', label = str_c('eta = ', round(eta,3)),
    #         x = min(data$theta)+0.2, y = 0)+
    geom_hline(yintercept = lr_lims,lty=2)+
    stat_function(fun=fun)+
    geom_line(data = eta_df %>%
                mutate(buf = 0) %>%
                left_join(
                  tibble(
                    buf = 0,
                    theta = seq(min(data$theta), max(data$theta), 0.05)),
                  'buf'
                  ) %>%
                mutate(value = eta*fun(theta)))+
    pi_axis()
  
  print(p)
  return(eta_df %>% knitr::kable())
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
    filter(my_base != '') %>%
    mutate(
      index = str_c(qubit, my_base)
    )
}


plot_signaling <- function(data, ...,
                           x = quo(index),
                           error = quo(dv),
                           facet_x = NULL,
                           facet_y = NULL){
  
  #TODO: align plots
  
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
    aes_(x=x, y = quo(value), colour = quo(other_base))
  )+
    geom_point()+
    geom_errorbar(aes(ymin = value-!!error, ymax = value+!!error), width = 0.1)+
    facet_grid(rows = vars(!!facet_x), cols = vars(!!facet_y), labeller = label_both)
    labs(y = 'Expected value')
  
  #The delta/sigma bars
  p2 = ggplot(
    data %>%
      summarise(
        delta = (max(value)-min(value)),
        sigma = sqrt(sum(dv^2)),
        q = delta/sigma)
  )+
    geom_col(aes_(x = x, y = quo(q)))+
    labs(y = expression(Delta/sigma))+
    geom_hline(yintercept = 3, lty = 2)+
    facet_grid(rows = vars(!!facet_x), cols = vars(!!facet_y), labeller = label_both)
  
  return(list(p1,p2))
}


process_sc <- function(data){
  #Extract the circuit data for usual sanity check naming convention
  
  data %<>% extract_circuit_data(
    experiment = 1,
    state = 2,
    observable = 3,
    barrier = 4
    )
  data %<>% filter(experiment == 'SC')
  
  data %<>% mutate(
    sign = state_sign(variable),
    barrier = ifelse(barrier == 'B', 'With', 'Without'),
    n_qubits = str_length(variable)
  )
  
  data %<>% group_by(n_qubits, barrier, state)
  
  return(data)
}
