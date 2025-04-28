import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Load the CSV data
csv_file_path = 'data.csv'
df = pd.read_csv(csv_file_path)

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))  # Square figure
ax.set_xlabel('x position (m)')
ax.set_ylabel('y position (m)')
ax.set_title('Rutherford Scattering Simulation')
ax.grid(True)
ax.set_aspect('equal')  # Make sure x and y scale equally
ax.invert_xaxis()       # Incoming from left

# Plot the nucleus at (0,0)
nucleus = ax.plot(0, 0, 'yo', markersize=30)[0]  # BIG yellow dot

# Create the alpha particle
particle, = ax.plot([], [], 'ro', markersize=8)  # Red moving particle



# Set nice limits around the data
x_min = df['x_position'].min()
if x_min > 0:
    x_min = 0
x_max = df['x_position'].max()
if x_max < 0:
    x_max = 0
y_min = df['y_position'].min()
if y_min > 0:
    y_min = 0
y_max = df['y_position'].max()
if y_max < 0:
    y_max = 0


padding = abs(x_min) * 0.3  # Add 30% padding around
ax.set_xlim(x_min - padding, x_max + padding)
ax.set_ylim(y_min - padding, y_max + padding)

# Initialization function
def init():
    particle.set_data([], [])
    return particle, nucleus

# Update function
def update(frame):
    x = df['x_position'].iloc[frame]
    y = df['y_position'].iloc[frame]
    particle.set_data(x, y)
    return particle, nucleus

# Create the animation
ani = animation.FuncAnimation(
    fig, update, frames=len(df), init_func=init, blit=True, interval=100, repeat=False
)

plt.show()
