library(shiny)

shinyUI(fluidPage(

  # Application title
  titlePanel("Grover experiments"),

  sidebarLayout(
    
###Sidebar with controls
    sidebarPanel(
      
      radioButtons("N_qubits", label = h3("Select number of qubits"),
                   choices = str_c('N', 2:4) %>% setNames(2:4), 
                   selected = 'N2'),
      
      radioButtons("n_it", label = h3("Select number of iterations"),
                   choices = str_c('i', 1:3) %>% setNames(1:3), 
                   selected = 'i1'),
      
      radioButtons("backend", label = h3("Select backend"),
                   choices = list(
                     'IBM Q 5 Tenerife (QX5)' = 'ibmqx4',
                     'IBM Q 5 Yorktown (QX2)' = 'ibmqx2'
                     ), 
                   selected = 'ibmqx4')
      
    ),#close sidebarPanel

#
    mainPanel(
      
      plotOutput("magic_square")
      
    )#close mainPanel

  )#close sidebarLayout
))
