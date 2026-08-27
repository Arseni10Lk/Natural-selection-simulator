import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time
from Simulator import version
import pygame
import numpy as np

class MatplotlibVisualisation():
    def __init__(self, env):

        self.env = env

        self.plot_environment_ = self.env.plot_environment_
        self.graph_population_ = self.env.graph_population
        self.multiple_runs = self.env.multiple_runs

        self.start_time = 0
        self.end_time = 0

        self.population_history = [self.env.population_size]
        self.past_population_history = [self.population_history]
        self.average_population = []

        self.figure = plt.figure(figsize=(9, 6), layout='constrained')
        plt.show(block=False)

        if self.plot_environment_:
            self.environment_picture = plt.subplot2grid((2, 4), (0, 0), colspan=3, rowspan=2)
            self.population_stat = plt.subplot2grid((2, 4), (1, 3))
            
            self.environment_picture.set_xlim(0, self.env.length)
            self.environment_picture.set_ylim(0, self.env.width)
            self.environment_picture.set_title("Environment")
            
            self.food_scatter = self.environment_picture.scatter([], [], marker=".", s=3, color="#00C27E")
            self.org_scatter = self.environment_picture.scatter([], [], s=20, color="#FF9A19")
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

        self.figure.canvas.mpl_connect('close_event', self.on_close)

    def plot_environment(self):
        if self.plot_environment_:
            active_foods = [f for f in self.env.food_items if not f.eaten]
            if active_foods:
                self.food_scatter.set_offsets(np.c_[[f.x for f in active_foods], [f.y for f in active_foods]])
            else:
                self.food_scatter.set_offsets(np.empty((0, 2)))
                
            if self.env.organism_x:
                self.org_scatter.set_offsets(np.c_[self.env.organism_x, self.env.organism_y])
            else:
                self.org_scatter.set_offsets(np.empty((0, 2)))
        else:
            self.environment_picture.set_axis_off()

    def graph_population(self):
        if self.graph_population_:
            self.population_history = self.past_population_history[self.env.run_num]
            self.population_history.append(self.env.population_size)
            # calculating average population
            if self.env.run_num == 0:
                self.average_population = self.population_history.copy()
            else:
                summed_population_gen = 0
                for run in range(self.env.run_num + 1):
                    summed_population_gen += self.past_population_history[run][self.env.generation]
                    self.average_population[self.env.generation] = summed_population_gen/(self.env.run_num + 1)

            if not self.multiple_runs:
                self.population_stat.cla()
            self.population_stat.yaxis.set_major_locator(MaxNLocator(integer=True))
            self.population_stat.xaxis.set_major_locator(MaxNLocator(integer=True))
            self.population_stat.set_ylim(0, self.population_history[0] + 40)
            self.population_stat.yaxis.set_ticks(range(0, self.population_history[0] + 40, 5))
            if not self.multiple_runs:
                self.population_stat.set_xlim(0, self.env.generation)
            elif self.multiple_runs:
                self.population_stat.set_xlim(0, self.env.generations_number)
            self.population_stat.set_xlabel("generation")
            self.population_stat.set_ylabel("population")

            if not self.multiple_runs:
                self.population_stat.plot(self.population_history, linewidth=0.5, color="red")

            if self.env.generation > 1:
                self.population_stat.lines[self.env.run_num].remove()



            if self.multiple_runs:

                if self.env.run_num == 0:

                    if self.env.generation == self.env.generations_number:
                        self.population_stat.plot(self.population_history, linewidth=0.3, color="red")
                    else:
                        self.population_stat.plot(self.population_history, linewidth=2, color="red")
                elif self.env.run_num == 1:
                    if self.env.generation > 1:
                        self.population_stat.lines[self.env.run_num].remove()
                    self.population_stat.plot(self.population_history, linewidth=0.3, color="red")
                    self.population_stat.plot(self.average_population, linewidth=2, color="red")
                else:
                    if self.env.generation > 0:
                        self.population_stat.lines[self.env.run_num].remove()
                    self.population_stat.plot(self.population_history, linewidth=0.3, color="red")
                    self.population_stat.plot(self.average_population, linewidth=2, color="red")

            if not self.multiple_runs:
                self.population_stat.fill_between(
                    range(self.env.generation + 1),
                    self.population_history,
                    color="red",
                    alpha=0.3
                    )
            self.population_stat.grid(linewidth=0.2)
        else:
            self.population_stat.set_axis_off()

    def on_close(self, event):
        self.env.stop = True

    def display_figure(self, show_framerate=False):
        fps = 0

        if show_framerate:
            self.end_time = time.time()
            if self.start_time != 0:
                fps = 1 / (self.end_time - self.start_time)

            self.start_time = time.time()
            txt = self.textfield.text(0, 0.8, f"fps: {fps:.0f}")

            self.figure.canvas.draw_idle()
            self.figure.canvas.flush_events()

            txt.remove()
        else:
            self.figure.canvas.draw_idle()
            self.figure.canvas.flush_events()

    def on_close(self, event):
        print("Was closed")
        self.env.stop = True



    def show_final_graph(self):
        plt.show()

class PygameVisualisation():
    def __init__(self, env):
        self.env = env
        self.plot_environment_ = self.env.plot_environment_
        self.graph_population_ = self.env.graph_population
        self.multiple_runs = self.env.multiple_runs
        
        self.start_time = 0
        self.end_time = 0
        
        self.population_history = [self.env.population_size]
        self.past_population_history = [self.population_history]
        self.average_population = []
        
        if self.plot_environment_:
            pygame.init()
            self.width = self.env.length * 2
            self.height = self.env.width * 2
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Natural Selection Simulator (Pygame)")
            self.font = pygame.font.SysFont(None, 24)
            self.clock = pygame.time.Clock()
            
        if self.graph_population_:
            self.figure = plt.figure(figsize=(5, 4), layout='constrained')
            self.population_stat = self.figure.add_subplot(111)
            plt.show(block=False)

    def plot_environment(self):
        if not self.plot_environment_:
            return
            
        self.screen.fill((255, 255, 255))
        
        # Draw food
        active_foods = [f for f in self.env.food_items if not f.eaten]
        for f in active_foods:
            pygame.draw.circle(self.screen, (0, 194, 126), (int(f.x * 2), int(f.y * 2)), 2)
            
        # Draw organisms
        for i in range(len(self.env.organism_x)):
            pygame.draw.circle(self.screen, (255, 154, 25), (int(self.env.organism_x[i] * 2), int(self.env.organism_y[i] * 2)), 4)
            
    def graph_population(self):
        if self.graph_population_:
            self.population_history = self.past_population_history[self.env.run_num]
            self.population_history.append(self.env.population_size)
            
            if self.env.run_num == 0:
                self.average_population = self.population_history.copy()
            else:
                summed_population_gen = 0
                for run in range(self.env.run_num + 1):
                    summed_population_gen += self.past_population_history[run][self.env.generation]
                    self.average_population[self.env.generation] = summed_population_gen/(self.env.run_num + 1)
                    
            # Update the matplotlib live graph
            from matplotlib.ticker import MaxNLocator
            if not self.multiple_runs:
                self.population_stat.cla()
            self.population_stat.yaxis.set_major_locator(MaxNLocator(integer=True))
            self.population_stat.xaxis.set_major_locator(MaxNLocator(integer=True))
            self.population_stat.set_ylim(0, self.population_history[0] + 40)
            self.population_stat.yaxis.set_ticks(range(0, self.population_history[0] + 40, 5))
            if not self.multiple_runs:
                self.population_stat.set_xlim(0, self.env.generation)
            elif self.multiple_runs:
                self.population_stat.set_xlim(0, self.env.generations_number)
            self.population_stat.set_xlabel("generation")
            self.population_stat.set_ylabel("population")

            if not self.multiple_runs:
                self.population_stat.plot(self.population_history, linewidth=0.5, color="red")

            if self.env.generation > 1:
                self.population_stat.lines[self.env.run_num].remove()

            if self.multiple_runs:
                if self.env.run_num == 0:
                    if self.env.generation == self.env.generations_number:
                        self.population_stat.plot(self.population_history, linewidth=0.3, color="red")
                    else:
                        self.population_stat.plot(self.population_history, linewidth=2, color="red")
                elif self.env.run_num == 1:
                    if self.env.generation > 1:
                        self.population_stat.lines[self.env.run_num].remove()
                    self.population_stat.plot(self.population_history, linewidth=0.3, color="red")
                    self.population_stat.plot(self.average_population, linewidth=2, color="red")
                else:
                    if self.env.generation > 0:
                        self.population_stat.lines[self.env.run_num].remove()
                    self.population_stat.plot(self.population_history, linewidth=0.3, color="red")
                    self.population_stat.plot(self.average_population, linewidth=2, color="red")

            if not self.multiple_runs:
                self.population_stat.fill_between(
                    range(self.env.generation + 1),
                    self.population_history,
                    color="red",
                    alpha=0.3
                    )
            self.population_stat.grid(linewidth=0.2)
                    
            self.figure.canvas.draw_idle()
            self.figure.canvas.flush_events()

    def show_final_graph(self):
        import matplotlib.pyplot as plt
        
        # Connect matplotlib close event so we can detect it
        if self.graph_population_:
            self.figure.canvas.mpl_connect('close_event', self.on_close)
            
        # Keep the final state on screen and poll both event loops
        while not self.env.stop:
            if self.plot_environment_:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.env.stop = True
                        break
                        
            if self.graph_population_:
                # If the matplotlib window is closed, stop
                if not plt.fignum_exists(self.figure.number):
                    self.env.stop = True
                    break
                self.figure.canvas.draw_idle()
                self.figure.canvas.flush_events()
                
            pygame.time.wait(50) # Sleep 50ms to save CPU
            
        if self.plot_environment_:
            pygame.quit()

    def on_close(self, event):
        self.env.stop = True

    def display_figure(self, show_framerate=False):
        if not self.plot_environment_:
            return
            
        # Handle events so window doesn't freeze
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Was closed")
                self.env.stop = True
                pygame.quit()
                return

        # Always calculate FPS in pygame
        fps = self.clock.get_fps()
            
        # Draw FPS and Generation
        if show_framerate:
            text_str = f"Gen: {self.env.generation} | FPS: {fps:.0f} | Pop: {self.env.population_size}"
        else:
            text_str = f"Gen: {self.env.generation} | Pop: {self.env.population_size}"
            
        text = self.font.render(text_str, True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        
        version_text = self.font.render(f"v. {version}", True, (0, 0, 0))
        self.screen.blit(version_text, (self.width - 80, 10))
        
        pygame.display.flip()
        self.clock.tick(self.env.fps_limit) # Cap at user-defined FPS
