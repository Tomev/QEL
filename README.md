# IBM QX Laboratory

This is a project containing our first steps in quantum computing with IBM QE.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

For development and running:

* Python 3.5 or higher
* qiskit 0.7 python package (currently, as it's evolving fast)
* IBM QX account (to run jobs remotely)

### After download:

One should generate a Qconfig file and place it in the main folder (one with readme and license). After that all scripts
should work just fine.

### Coding style

Although it hasn't been said explicitely, we're trying to maintain PEP8 in Python scripts. There currently is no coding
style for qasms and other files used.

#### Circuit naming style

For automation of results analysis a circuit naming convention has to be set. It's natural, that each experiment would
require different attributes in circuit name, however they share some similarities eg. experiment name. Given that from
now on we will be using following naming style:

```
experiment-name_attr-1_attr-2_..._attr-n
```

for example

```
Grover_3_111_1
``` 

would mean, that given circuit describes experiment with Grover algorithm, using 3 qubit states, with 111 as selected
state and with only one diffusion and oracle operator used. Note that each naming convention (for different experiments)
should be placed within experiments folder. See Grover folder for example.

Also note that attributes are separated by '_' character and mutli-word attributes or names should be separated by '-'.  

## Run with

Python interpreter of your choice, that fulfills prerequisites.

## Authors
* **Jakub Tworzydło**
* **Alicja Dutkiewicz** 
* **Tomasz Rybotycki** - [Tomev](https://github.com/Tomev)

## License

This project is licensed under the GNU GPL v. 3 License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* IBM QX staff, for letting us use your chips. 
* [Billie Thompson](https://github.com/PurpleBooth) for great readme.md template.
* [Andreas Renberg](https://github.com/IQAndreas) and contributors of [markdown-licenses] for md version of GNU GPL 3.

