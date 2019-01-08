# Grover

This is a readme for our Grover Algorithm experiments.

## Circuit naming convention

For Grover experiments following circuit naming convention shall be used:

```
Grover_state-qubits-number_target_turns-number
```

where Grover is basic experiment name, state-qubits-number is number of qubits in measured state, oracle denotes state
selected for the experiment, and turns-number denotes number of iterations of algorithm (or number of times oracle and
diffusion operators were used). For example

```
Grover_3_111_2
```

would mean that in given circuit Grover algorithm was used, with 3 qubit state and 111 as state selected for search. It
also used diffusion and oracle 2 times (as should be).
