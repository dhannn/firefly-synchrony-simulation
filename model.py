import math
import agentpy as ap
import IPython

from matplotlib import rcParams
from matplotlib.pyplot import scatter
import matplotlib.pyplot as plt

# Constants representing firefly states
RECOVERING = 0
READY = 1
FLASH = 2

# Color mapping for visualization
COLOR_DICT = {
    RECOVERING: '#877666',
    READY: '#FD96A9',
    FLASH: '#F9DB6D'
}

class Firefly(ap.Agent):
    """A class representing a firefly agent in the model."""

    def setup(self, **kwargs):
        """Initialize the firefly agent with specified parameters."""
        self.state = RECOVERING
        self.flash_threshold = kwargs['flash_threshold']
        self.neighbor_radius = self.initialize_neighbor_radius(kwargs)
        self.recovery_period = self.get_random_recovery_period(kwargs)
        self.timer = self.initialize_timer(kwargs)

    def initialize_neighbor_radius(self, kwargs):
        """Initialize the random neighbor radius for the firefly."""
        return self.model.random.randint(1, kwargs['neighbor_r'])

    def initialize_timer(self, kwargs):
        """Initialize the recovery timer for the firefly."""
        return math.floor(self.model.random.gauss(kwargs['recovery_period'] / math.sqrt(kwargs['recovery_period']), 4))

    def get_random_recovery_period(self, kwargs):
        """Generate a random recovery period for the firefly."""
        rand = round(self.model.random.gauss(kwargs['recovery_period'], 0.6))
        return rand
        # return kwargs['recovery_period']
    
    def update(self, neighbors):
        """Update the state of the firefly based on its neighbors."""
        if self.state == RECOVERING:
            if self.timer == self.recovery_period:
                self.state = READY
                self.timer = 0
                return
            else: 
                self.timer += 1
                return

        if self.state == READY:
            for neighbor in neighbors:
                if neighbor.state == FLASH:
                    self.state = FLASH
                    return
            
            if self.model.random.random() <= self.flash_threshold:
                self.state = FLASH
                return
            
        if self.state == FLASH:
            self.state = RECOVERING
            self.timer = 0


class FirefliesModel(ap.Model):
    """A class representing the overall firefly synchronization model."""

    def setup(self):
        """Initialize the model with specified parameters."""
        self.n_fireflies = self.p['n_fireflies']
        self.recovery_period = self.p['recovery_period']
        self.flash_threshold = self.p['flash_threshold']
        self.neighbor_r = self.p['neighbor_r']
        self.curr_time_steps = 0
        
        # Create an agent list of fireflies
        self.fireflies = ap.AgentList(
            self, 
            self.n_fireflies, 
            Firefly, 
            recovery_period=self.recovery_period,
            flash_threshold=self.flash_threshold, 
            neighbor_r=self.neighbor_r)
        
        # Create a grid to represent the environment
        self.forest = ap.Grid(self, [self.p.size]*2, track_empty=True)
        self.forest.add_agents(self.fireflies, random=True, empty=True)
    
    def step(self):
        """Advance the simulation by one time step."""
        for firefly in self.fireflies:
            neighbors = self.forest.neighbors(firefly, firefly.neighbor_radius)
            firefly.update(neighbors)

    def showAnimation(self):
        """Visualize the firefly synchronization animation."""
        
        def animate(model: FirefliesModel, ax: plt.Axes):
            x = [model.forest.positions[firefly][0] for firefly in model.forest.positions]
            y = [model.forest.positions[firefly][1] for firefly in model.forest.positions]
            colors = [COLOR_DICT[state] for state in model.fireflies.state]
            opacity = [0.1 + state / 2 * 0.9 for state in model.fireflies.state]
            marker_scale = [(rcParams['lines.markersize'] ** 2) * 1.5 if state == FLASH else (rcParams['lines.markersize'] ** 2) for state in model.fireflies.state]

            ax.figure.set_figheight(7)
            ax.figure.set_figwidth(7)
            ax.tick_params(left = False, right = False , labelleft = False, labelbottom = False, bottom = False)
            ax.set_facecolor('#1A1D1A')
            ax.scatter(x, y, c=colors, alpha=opacity, s=marker_scale)

        fig, ax = plt.subplots()
        animation = ap.animate(self, fig, ax, animate)
        return IPython.display.HTML(animation.to_jshtml())
