library(shiny)
library(tidyverse)
library(magrittr)

shinyServer(function(input, output) {

###READ AND PREPARE DATA
  grover_data = read_csv('grover_data.csv', col_types = list(variable = 'c', value = 'n'))
  
###FUNCTIONS
  
  #draw a "magic square"
  magic_square <- function(d){
    
    ggplot(d %>%
             group_by(oracle, variable, add = T) %>%
             summarise(value = mean(value)),
           aes(y=oracle, x=variable))+
      geom_raster(aes(fill = value))+
      geom_text(aes(label = sprintf('%.2f', value)))+
      scale_y_discrete(limits = d$oracle %>% unique %>% sort(T))+
      coord_fixed()#+
    #scale_fill_continuous(limits = c(0,1))
    
  }
  
###PLOTS
  output$magic_square <- renderPlot({
    
    d = filter(
      grover_data, 
      N_qubits == input$N_qubits,
      n_it == input$n_it,
      backend == input$backend
      )
    
    validate(
      need(nrow(d) > 0, "No data :(")
    )

    magic_square(d)

  })

})
