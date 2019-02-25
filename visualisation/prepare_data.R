#read all the data from our Grover experiments
folder_name = 'data'
grover_data <- str_c(folder_name, '/',list.files(folder_name)) %>%
  lapply(read_csv, col_types = list(variable = 'c', value = 'n')) %>%
  
  setNames(list.files(folder_name) %>% str_remove('.csv') %>% str_remove('Grover'))

grover_data %<>% lapply(drop_na)
grover_data %<>% lapply(distinct)

#Remove ancillae from N4
grover_data[which(names(grover_data) %>% str_sub(1,2) == 'N4')] %<>% lapply(function(d){
  d %>%
    mutate(
      variable = ifelse(
        str_length(variable) == 5,
        str_c(
          str_sub(variable,2,2),
          str_sub(variable,1,1),
          str_sub(variable,4,4),
          str_sub(variable,5,5)
        ),
        variable
      )
    ) %>%
    group_by_at(vars(-value)) %>% summarise(value=sum(value)) %>% ungroup
})

#create a data frame
grover_data = bind_rows(grover_data)

#correct circuits names
grover_data %<>% mutate(
  circuit = circuit %>%
    str_replace('\\.qasm','') %>%
    str_replace('N','') %>%
    str_replace('CHSH_test', 'CHSH-test')
)

#normalise counts to 1
grover_data %<>% mutate(value = value/1024)

#process postselection
grover_data %<>%
  left_join(
    grover_data %>%
      filter(str_split_fixed(circuit,' |_',2)[,1]=='CHSH-test') %>%
      mutate(
        observable = str_split_fixed(circuit,'_',2)[,2],
        value = ifelse(variable %in% c('00','11'), 1, -1)*ifelse(observable == 'XZ', -1, 1)*value
      ) %>%
      group_by(id) %>% summarise(chsh = sum(value)) %>%
      mutate(good = (abs(chsh)>2))
  ) %>%
  filter(str_split_fixed(circuit, '_', 4)[,1] == 'Grover')

#extract data from circuit name
grover_data %<>% mutate(
  N_qubits = str_split_fixed(circuit, '_', 4)[,2],
  n_it = str_split_fixed(circuit, '_', 4)[,4],
  oracle = str_split_fixed(circuit, '_', 4)[,3]
  )

grover_data %>% write_csv('grover_data.csv')
