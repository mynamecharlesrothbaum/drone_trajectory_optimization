import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

latitudes = []
longitudes = []
altitudes = []



def collect_positions(lat, lon, alt):
    latitudes.append(lat)
    longitudes.append(lon)
    altitudes.append(alt)


def plot_trajectory():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(longitudes, latitudes, altitudes, marker='o')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Altitude')

    plt.show()

def reset_trajectory():
    latitudes.clear
    longitudes.clear
    altitudes.clear
