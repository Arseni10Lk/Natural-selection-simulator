import matplotlib.pyplot as plt
import numpy
from matplotlib.ticker import MaxNLocator
import time
from Simulator.__init__ import version


class Visualisation():
    def __init__(self, env, plot_environment_=True, graph_population_=True):
        self.plot_environment_ = plot_environment_
        self.graph_population_ = graph_population_
        self.env = env

        self.start_time = 0
        self.end_time = 0

        self.population_history = [self.env.population_size]

        self.figure = plt.figure(figsize=(9, 6), layout='constrained')

        if self.plot_environment_:
            self.environment_picture = plt.subplot2grid((2, 4), (0, 0), colspan=3, rowspan=2)
            self.population_stat = plt.subplot2grid((2, 4), (1, 3))
        elif self.graph_population_:
            self.population_stat = plt.subplot2grid((2, 4), (0, 0), colspan=3, rowspan=2)
            self.environment_picture = plt.subplot2grid((2, 4), (1, 3))
        self.textfield = plt.subplot2grid((2, 4), (0, 3))

        if not self.plot_environment_:
            self.environment_picture.set_axis_off()
        if not self.graph_population_:
            self.population_stat.set_axis_off()

        self.textfield.set_axis_off()

        self.figure.tight_layout(pad=1.5)
        self.textfield.text(0, 0.9, 'v. ' + version)

    def plot_environment(self):
        if self.plot_environment_:
            self.environment_picture.cla()
            self.environment_picture.scatter(self.env.food_x, self.env.food_y, marker=".", s=3, color="#00C27E")
            self.environment_picture.scatter(self.env.organism_x, self.env.organism_y, s=20, color="#FF9A19")
            self.environment_picture.set_xlim(0, self.env.length)
            self.environment_picture.set_ylim(0, self.env.width)
            self.environment_picture.set_title("Environment")
        else:
            self.environment_picture.set_axis_off()

    def graph_population(self):
        if self.graph_population_:
            self.population_history.append(self.env.population_size)

            self.population_stat.cla()
            self.population_stat.yaxis.set_major_locator(MaxNLocator(integer=True))
            self.population_stat.xaxis.set_major_locator(MaxNLocator(integer=True))
            self.population_stat.set_ylim(0, self.population_history[0] + 20)
            self.population_stat.yaxis.set_ticks(range(0, self.population_history[0] + 20, 10))
            self.population_stat.set_xlim(0, self.env.generation)
            self.population_stat.set_xlabel("generation")
            self.population_stat.set_ylabel("population")
            self.population_stat.plot(self.population_history, linewidth=0.5, color="red")
            self.population_stat.fill_between(
                range(self.env.generation + 1),
                self.population_history,
                color="red",
                alpha=0.3
            )
            self.population_stat.grid(linewidth=0.2)
        else:
            self.population_stat.set_axis_off()

    def display_figure(self, show_framerate=False):
        fps = 0

        if show_framerate:
            self.end_time = time.time()
            if self.start_time != 0:
                fps = 1 / (self.end_time - self.start_time)

            self.start_time = time.time()
            txt = self.textfield.text(0, 0.8, f"fps: {fps:.0f}")

            self.figure.show()

            plt.pause(0.01)

            txt.remove()
        else:
            self.figure.show()

            plt.pause(0.01)
