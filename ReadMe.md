# Natural selection simulator #

Some ideas were taken from [the Primer's video on natural selection](https://www.youtube.com/watch?v=0ZGbIKd0XrM). However, this project is planned to include more mechanics while also to have lower quality of visualisation (at least, absence of 3D graphics).

Right now the program allows us to find the population which can be sustained by certain food amount. No mutations were added yet.

The rules are as follows:
At first food is randomly distributed all over the map. Its amount can be changed from simulation to simulation.
The organisms are then loaded along the edges of the map, their positions are also random, each has random direction.
As the simulation starts the organisms start moving with the pre-set speed while randomly changing direction until the food is found, after that the organism attempts to approcah it.
If the organism manages to consume
* 2 or more food items, then instead of it 2 organisms will appear next day. In other words, it reproduces.
* 1 food item, then it survives.
* 0 food items, then it dies and does not go to the next day.

Amount of food does not recover instantly, for example the amount of food in day 7 depends on the amount of food in days 4 and 5. That adds realism to the way our ecosystem behaves. This is repeated for a certain number of days.

Finally, in v0.4.0 the ability to conduct any meaningful experiments is there. We can calculate the carrying capacity of our simplified ecosystem.
For example, if we will set the following parameters:

Parameter | Value
--- | :---: 
food amount | 100
generations number | 60
day length | 20
initial population | 50

and run a simulation once we will get the following: 

https://github.com/user-attachments/assets/1396914d-4306-485e-809b-de952b5b85bf

As we can see, the population has fluctuated significantly and while the simulation came to an end with the population of around 32 it is not necessarily the carrying capacity of our mini-world. Since it can be just another fluctuation or just one random outcome. To get the full picture we have to run it several times. Let's say 20:

https://github.com/user-attachments/assets/7ecd82bf-d6f6-43df-93c9-6432e7ed5acf

Now, we can see that the environment can sustain, on average, the population of around 22 organisms, thus the carrying capacity is found and the initial run was extremely misleading.

## Future development ##

At first more visualisations will be made using `matplotlib` library, later it is planned to move to `pygame` while leaving matplotlib for statistics of the simulation.

Long-term:
Feature name | Description | Status
-----|---------|:-----:
Video rendering | To allow for stable frame rate which is comfortable for the observer in case of big simulations. The data should be saved as a result of simulation and then played without any additional calculations
Mutations | Traits from survivors of one generation are inherited by their children with a certain mutation range. | In process
Plants | Act as a food source, are stationary, the growth is stimulated by dying organisms. Later, specific adaptations and species of plants can be added, for example to simulate symbiotic relationship formation.
Ecosystems | Two ecosystems with the transition zone in-between both having different conditions (so that different genomes survive in different ecosystems)
Prey/hunter concept | Some creatures can eat others while others can eat "usual" food or plants. Can be used to proove Lotka-Volterra equations (realtionship between the populations of prey and hunters)
Pygame graphics | The main simulation visualisation should be moved from `matplotlib` to `pygame`. Textures can be added to make the simulation more pleasant to watch.
Behavioral evolution | Has 2 potential imlementation options. More complicated option is to include neural network and that would allow to simulate group behaviour and escape strategies.
Sexual dimorphism | The fact that male and female organisms of the same species have slightly different look and adaptations. Would allow to simulate handicap principle if implemented.
Matplotlib graphics | Implementeed as an animated plot, not very pleasant to watch but clear and easy to work with. | Done
Separate file for visualiations mehtods | Everything related to visualisation should be moved to a different python file. | Done

Short-term:
Feature name | Description 
-----|---------
Adding mutations | A major update, will be in v. 0.5.0
