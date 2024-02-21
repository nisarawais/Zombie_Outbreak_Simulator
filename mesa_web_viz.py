import mesa
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import solara
from matplotlib.figure import Figure

from mesa.datacollection import DataCollector
from mesa.experimental import JupyterViz


def compute_gini(model):
    agent_healths = [agent.health for agent in model.schedule.agents]
    x = sorted(agent_healths)
    human = 0
# checks for how many human left over from the grid
    for i, health in enumerate(x):
        if health == 1 or health == 2: # including human with ammo and without ammo
            human += 1

    print(human)
    return human


class PersonAgent(mesa.Agent):
    """An agent with fixed initial health."""

    def __init__(self, unique_id, model):

        # Pass the parameters to the parent class.
        super().__init__(unique_id, model)

        # Create the agent's variable and set the initial values.
        self.health = 1
        self.shots_left = 15

    def step(self):

        # if the agent is zombie, it will turn human into zombie if zombie lands on the same cell as human
        if self.health == 0:
            self.give_Zombie()

        # if the agent is human, it will shoot zombie if human lands on the same cell as zombie
        if self.health == 1:
            self.shootEm()

        # if the agent is human and don't have ammo anymore, it will not be able to do anything but run for life
        if self.health == 2:
            self.move()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_Zombie(self):
        self.move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 0:
            other = self.random.choice(cellmates)
            # humans that have bullets (green) and don't have bullets (orange)
            if other.health == 1 or other.health == 2:
                # human become a zombie 🧟
                other.health = 0

    def shootEm(self):
        self.move()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 0:
            other = self.random.choice(cellmates)
            if other.health == 0:

                # human shoot
                self.shots_left = self.shots_left - 1

                # 50% chance of successful shot
                if self.random.random() < 0.5:
                    other.model.grid.move_agent(self, self.pos)
                    # killed the zombie and it will turn into small red
                    other.health = -1

                #if human ran out of the ammo, it will be in orange which indicates that it doesn't have ammo anymore
                if (self.shots_left == 0):
                    self.health = 2

                # 50% chance that human has a success in taking zombie's ammo
                if self.random.random() < 0.5:
                    self.shots_left += other.shots_left


class PersonModel(mesa.Model):
    """A model with some number of agents."""

    def __init__(self, N, width, height, zombie_percentage=0.1):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini}, agent_reporters={"Zombie": "zombie"}
        )
        # Create agents
        for i in range(self.num_agents):
            is_zombie = self.random.random() < zombie_percentage
            a = PersonAgent(i, self)
            if is_zombie:
                a.health = 0
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()
        self.datacollector.collect(self)


model_params = {
    "N": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of agents:",
        "min": 50,
        "max": 100,
        "step": 1,
    },

    # changes size of model in web visualizer
    "width": 20,
    "height": 20,
}


# modify this function to change output on grid
def agent_portrayal(agent):
    if agent.health == 0:
        size = 50
        color = "tab:purple"
    if agent.health == 1:
        size = 50
        color = "tab:green"
    if agent.health == 2:
        size = 50
        color = "tab:orange"
    if agent.health == -1:
        size = 25
        color = "tab:red"

    return {"size": size, "color": color}

############ THIS IS A NEW FEATURE -  this allows me to see the number of (health = 1) human with ammo, (health = 2) without ammo, (health = 0) zombie, and (health = -1) zombie's deaths
def make_histogram(model):
    fig = Figure()
    ax = fig.subplots()
    health = [agent.health for agent in model.schedule.agents]
    ax.hist(health, bins=10)
    solara.FigureMatplotlib(fig)

page = JupyterViz(
    PersonModel,
    model_params,
    measures=["Gini"],
    name="Zombie Model",
    agent_portrayal=agent_portrayal,
)

############ THIS IS A NEW FEATURE -  this allows me to see the number of (health = 1) human with ammo, (health = 2) without ammo, (health = 0) zombie, and (health = -1) zombie's deaths
page = JupyterViz(
    PersonModel,
    model_params,
    measures=["Gini", make_histogram],
    name="Zombie Model",
    agent_portrayal=agent_portrayal,
)
# This is required to render the visualization in the Jupyter notebook
page
