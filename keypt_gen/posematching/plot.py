import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

thresholds = np.arange(0.6, 0.95, 0.01)
f1_scores = [0.124, 0.627, 0.401, 0.686, 0.341, 0.45, 0.601, 0.578, 0.492, 0.392, 0.387, 0.555, 0.699, 0.334, 0.675, 0.642, 0.774, 0.485, 0.797, 0.628, 0.555, 0.724, 0.947, 0.848, 0.768, 0.84, 0.739, 0.802, 0.705, 0.845, 0.952, 1.0, 0.982, 0.918, 0.96]
f2_scores = [0.259, 0.711, 0.572, 0.779, 0.535, 0.621, 0.733, 0.706, 0.685, 0.551, 0.55, 0.703, 0.809, 0.505, 0.794, 0.752, 0.812, 0.688, 0.89, 0.767, 0.686, 0.849, 0.945, 0.911, 0.882, 0.91, 0.83, 0.891, 0.836, 0.899, 0.955, 1.0, 0.992, 0.888, 0.982]


# Create figure and axis
fig, ax = plt.subplots()

# Plot F1 scores
ax.plot(thresholds, f1_scores, label='F1 Score', linestyle='--')

# Plot F2 scores
ax.plot(thresholds, f2_scores, label='F2 Score')

# Set labels and title
ax.set_xlabel('Threshold')
ax.set_ylabel('Accuracy')
ax.set_title('F1 and F2 Scores')

# Set legend
ax.legend()

# Show the plot
ax.grid(True)
plt.show()