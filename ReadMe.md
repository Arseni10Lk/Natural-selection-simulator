# Natural selection simulator #

Some ideas were taken from [the Primer's video on natural selection](https://www.youtube.com/watch?v=0ZGbIKd0XrM). However, this project is planned to include more mechanics while also to have lower quality of visualisation (at least, absence of 3D graphics).

As of now the code only simulates the selection process, however visualisition is not implemented yet (even in `matplotlib`). Right now it only allows us to find the population which can be sustained by certain food amount. No mutations were added yet.

At first visualisations will be made using `matplotlib` library, later it is planned to move to `pygame` while leaving matplotlib for statistics of the simulation.

Feature name | Description | In development
-----|---------|:-----:
Matplotlib graphics | Implementeed as an animated plot, not very pleasant to watch but clear and easy to work with. | +
Mutations | Traits from survivors of one generation are inherited by their children with a certain mutation range.
Plants | Act as a food source, are stationary, the growth is stimulated by dying organisms. Later, specific adaptations and species of plants can be added, for example to simulate symbiotic relationship formation.
Ecosystems | Two ecosystems with the transition zone in-between both having different conditions (so that different genomes survive in different ecosystems)
Prey/hunter concept | Some creatures can eat others while others can eat "usual" food or plants. Can be used to proove Lotka-Volterra equations (realtionship between the populations of prey and hunters)
Pygame graphics | The main simulation visualisation should be moved from `matplotlib` to `pygame`. Textures can be added to make the simulation more pleasant to watch.
Behavioral evolution | Has 2 potential imlementation options. More complicated option is to include neural network and that would allow to simulate group behaviour and escape strategies.
Sexual dimorphism | The fact that male and female organisms of the same species have slightly different look and adaptations. Would allow to simulate handicap principle if implemented.


To be updated...
