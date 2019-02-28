library(shiny)
library(tidyverse)
library(magrittr)
library(rlang)

shinyServer(function(input, output) {

###READ AND PREPARE DATA
  grover_data = read_csv('grover_data.csv', col_types = list(variable = 'c', value = 'n'))
  
  #Parameters to compare/filter
  parameters = c('N_qubits', 'n_it', 'backend')
  
  #reactive data frame
  data <- reactiveVal(grover_data)
  observeEvent(
    c(input$columns, input$columns, input$N_qubits, input$n_it, input$backend),
    {
      #filter data
      data(
        grover_data %>% filter_(str_c(
          setdiff(parameters, c(input$rows, input$columns)),
          ' == input$',
          setdiff(parameters, c(input$rows, input$columns))
        ) %>%
          str_c(collapse = ' & ')
        )
      )
      
      #Add grouping for facetting
      data(
        data() %>% group_by_at(intersect(parameters, c(input$rows, input$columns)))
      )
      
      if('postselection' %in% c(input$rows, input$columns)){
        data(
          bind_rows(
            all = data(),
            good = filter(data(), good),
            best = filter(data(), percent_rank(chsh)>0.9),
            .id = 'postselection'
          ) %>%
            mutate(
              postselection = factor(postselection, levels = c('all','good','best'))
            ) %>%
            group_by_at(intersect(parameters, c(input$rows, input$columns))) %>%
            group_by(postselection, add = TRUE)
        )
      }

    }
    )
  
  

###FUNCTIONS
  
  #draw a "magic square"
  magic_square <- function(d){
    
    ggplot(d %>%
             group_by(oracle, variable, add = T) %>%
             summarise(value = mean(value)),
           aes(y=oracle, x=variable))+
      geom_raster(aes(fill = value))+
      geom_text(aes(label = sprintf('%.2f', value)))+
      scale_y_discrete(limits = d$oracle %>% unique %>% sort(T))#+
    #scale_fill_continuous(limits = c(0,1))
    
  }
  
###PLOTS
  
  output$magic_square <- renderPlot({
    
    validate(
      need(nrow(data()) > 0, "No data :(")
    )
    
    validate(
      need(input$rows == '.' | input$rows != input$columns,
      'Please chose different variables for x and y axis.')
    )

    plot = magic_square(data())
    
    if(input$columns!='.' | input$rows!='.'){
      plot = plot+
      facet_grid(
        str_c(input$rows, ' ~ ', input$columns) %>% as.formula,
        scales = ifelse('N_qubits' %in% c(input$rows, input$columns), 'free', 'fixed')
        )
    }
    
    if('N_qubits' %in% c(input$rows, input$columns)){
      plot = plot+
        scale_x_discrete(drop = T)+
        scale_y_discrete(drop = T)
    }else{
      plot = plot+
        coord_fixed()
    }
    
    plot
    

  })
  
  #output$number_of_jobs_table <- {
  #  
  #  validate(
  #    need(nrow(data()) > 0, "No data :(")
  #  )
  #  
  #}

})
