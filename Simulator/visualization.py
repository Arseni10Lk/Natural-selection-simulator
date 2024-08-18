import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time
from Simulator.__init__ import version


class Visualisation():
    def __init__(self, env, plot_environment_=True, graph_population_=True):
        self.plot_environment_ = plot_environment_
        self.graph_population_ = graph_population_
        self.env = env

        self.figure = plt.figure(figsize=(9, 6), layout='constrained')
        self.environment_picture = plt.subplot2grid((2, 4), (0, 0), colspan=3, rowspan=2)
        self.population_stat = plt.subplot2grid((2, 4), (1, 3))
        self.figure.tight_layout(pad=1.5)
        self.figure.text(0.75, 0.9, 'v. ' + version)

    def plot_environment(self, show_framerate=False):
        self.environment_picture.cla()
        self.environment_picture.scatter(self.env.food_x, self.env.food_y, marker=".", s=3, color="#00C27E")
        self.environment_picture.scatter(self.env.organism_x, self.env.organism_y, s=20, color="#FF9A19")
        self.environment_picture.set_xlim(0, self.env.length)
        self.environment_picture.set_ylim(0, self.env.width)
        self.environment_picture.set_title("Environment")
        self.figure.show()

        plt.pause(0.01)

    def graph_population(self):
        self.population_stat.cla()
        self.population_stat.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.population_stat.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.population_stat.set_ylim(0, self.env.population_history[0] + 20)
        self.population_stat.set_xlim(0, self.env.generation)
        self.population_stat.set_xlabel("generation")
        self.population_stat.set_ylabel("population")
        self.population_stat.plot(self.env.population_history, linewidth=0.5, color="red")


def plot_environment(env, show_framerate=False):
    plt.cla()
    plt.scatter(env.food_x, env.food_y, marker=".", s=3, color="#00C27E")
    plt.scatter(env.organism_x, env.organism_y, s=20, color="#FF9A19")
    plt.xlim(0, env.length)
    plt.ylim(0, env.width)
    env.frames += 1
    plt.subplots_adjust(right=0.85)
    font = {
        "size": 7
    }
    plt.text(1.05 * env.length, 0, "v. " + version, fontdict=font)
    if show_framerate:

        env.end_time = time.time()
        if env.start_time != 0:
            fps = env.frames / (env.end_time - env.start_time)
            plt.text(1.05*env.length, 0.95*env.width, f'fps:{fps:.0f}', fontdict=font)
        env.start_time = time.time()
        env.frames = 0
    plt.show(block=False)

    plt.pause(0.01)


def graph_populaiton(env):
    plt.cla()
    plt.plot(env.population_history)
    plt.show(block=False)
    plt.pause(0.1)
