It was built with Python, Mesa, and MatPlotLib. This application provides a visualation of the outbreak simulator on the grid. If the zombie lands on the same cell as human, it infects the human and the human turn into a zombie.  If a human lands on the same cell as a zombie, the human will shoot the zombie. There is a 50% chance that the shot is successful. If the shot is successful, the zombie dies. The zombie has a 50% chance of passing the ammo to the human. If the human runs out of ammo, it will not shoot the zombie.

Legend: 
Human with ammo ~ health = 1, green
Human without ammo ~ health = 2, orange
Zombie ~ health = 0, purple
Dead zombie ~ health = -1, red (smaller circle)

How to Run: 
Run the command "solara run mesa_web_viz.py" from the ai folder. It will open up the Mesa Web Viz in the browser. You can adjust the number of agents using the slider ranging from 50 to 100. 10% of the agents are zombies. You can either click step or play to run the simulator.
