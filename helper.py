import threading
import matplotlib.pyplot as plt

# Thread-local data
local_data = threading.local()

def collect_positions(north, east, down):
    if not hasattr(local_data, 'positions'):
        local_data.positions = {'north': [], 'east': [], 'down': []}
    local_data.positions['north'].append(north)
    local_data.positions['east'].append(east)
    local_data.positions['down'].append(down)


#ChatGPT wrote this:
def plot_trajectory():
    if hasattr(local_data, 'positions'):
        # Retrieve the position data
        north = local_data.positions['north']
        east = local_data.positions['east']
        down = local_data.positions['down']
        
        # Create the figure and the 3D axes
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        
        # Plot the trajectory
        ax.plot(east, north, down, marker='o', markersize=5)  # Switched order of north and east for consistency with axis labels
        
        # Label the axes
        ax.set_xlabel('East (m)')
        ax.set_ylabel('North (m)')
        ax.set_zlabel('Down (m)')
        
        # Set the same scale for East and North by finding the max range and setting the axis limits accordingly
        max_range = max(max(north) - min(north), max(east) - min(east), max(down) - min(down))
        Xb = 0.5 * max_range
        Yb = 0.5 * max_range
        Zb = 0.5 * max_range
        
        # Get the center of each axis for the data
        Xc = 0.5 * (max(north) + min(north))
        Yc = 0.5 * (max(east) + min(east))
        Zc = 0.5 * (max(down) + min(down))
        
        # Set the limits
        ax.set_xlim([Xc - Xb, Xc + Xb])
        ax.set_ylim([Yc - Yb, Yc + Yb])
        ax.set_zlim([Zc - Zb, Zc + Zb])

        # Set the title
        ax.set_title('Drone Trajectory - Local NED Coordinates')
        
        # Show the plot
        plt.show()



def reset_trajectory():
    if hasattr(local_data, 'positions'):
        local_data.positions = {'north': [], 'east': [], 'down': []}
