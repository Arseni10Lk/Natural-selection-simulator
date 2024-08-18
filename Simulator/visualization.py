import matplotlib.pyplot as plt
import time
from Simulator.__init__ import version


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
