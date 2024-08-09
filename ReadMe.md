# Natural selection simulator #

Some ideas were taken from [the Primer's video on natural selection](https://www.youtube.com/watch?v=0ZGbIKd0XrM). However, this project is planned to include more mechanics while also to have lower quality of visualisation (at least, absence of 3D graphics).

As of now the code only sets all the initial conditions to start and allows for movement and eating one step at a time.
At first visualisations will be made using `matplotlib` library, later it is planned to move to `pygame` while leaving matplotlib for statistics of the simulation.

Feature name | Description 
-----|---------
Plants | Act as a food source, are stationary, the growth is stimulated by dying organisms. Later, specific adaptations and species of plants can be added, for example to simulate symbiotic relationship formation.
Pygame graphics | The main simulation visualisation should be moved from `matplotlib` to `pygame`. Textures can be added to make the simulation more pleasent to watch.
Behavioral evolution | Has 2 potential imlementation options. More complicated option is to include neural network and that would allow to simulate group behaviour and escape strategies.
Sexual dimorphism | The fact that male and female organisms of the same species have slightly different look and adaptations. Would allow to simulate handicap principle if implemented.

To be updated...
