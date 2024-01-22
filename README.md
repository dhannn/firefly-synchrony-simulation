# Simulating Firefly Synchrony through Cellular Automata

This notebook explores the phenomenon of firefly synchrony by discussing 
complex systems, ways of modelling complex systems and some sample 
implementations of a specific model called cellular automata.

## Usage
1. Install the necessary dependencies: 
```pip install -r requirements.txt```

1. Start the Jupyter Notebook:
```jupyter notebook```

1. Read through the notebook.

## Modelling firefly synchrony through CA

The following shows how we model firefly synchrony through CA.

### Dimension of Lattice
In our model, we will use a 2-dimensional lattice for easy visualization.

### States
We base our states on the existing theory of how fireflies work. Namely, 
we recognized the following states: `RECOVERING`, `READY` and `FLASH`. 
The `RECOVERING` state denotes that the firefly is still recovering and cannot flash 
at the next time step. The `READY` state means that, at any succeeding time step, 
the firefly has some chance of flashing. The `FLASH` state denotes 
the act of flashing.

Other than the behavioral states, we also keep track of some internal states. 
The recovering state has an timer which.

### Neighborhood
Since fireflies have different distance scales for which they perceive 
other fireflies, we design a more dynamic neighborhood scheme. In this model, 
we take some random "radius" for each firefly which indicates the size of the
 neighborhood.

### Ruleset
The ruleset for updating each cell are as follows:
- If there exists a flashing firefly in the neighborhood and the firefly 
is ready, flash.
- If there is no flashing firefly in the neighborhood and the firefly is ready, 
flash only when it reaches a certain amount of threshold.
- If firefly flashes, set a timer for a certain set amount of time and go to 
recovery state.
- If the firefly is recovering, decrement the timer.

## Reference
-  Sokol, J. (2022). How Do Fireflies Flash in Sync? Studies Suggest a New Answer. | Quanta Magazine. https://www.quantamagazine.org/how-do-fireflies-flash-in-sync-studies-suggest-a-new-answer-20220920/
