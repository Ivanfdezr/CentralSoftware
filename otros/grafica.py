# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.colors import LightSource


fig = plt.figure()


# Make data
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 10 * np.outer(np.cos(u), np.sin(v))
y = 10 * np.outer(np.sin(u), np.sin(v))
z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

#
#
#

# Plot the surface
ls = LightSource(270, 45)
# To use a custom hillshading mode, override the built-in shading and pass
# in the rgb colors of the shaded surface calculated from "shade".
rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
ax = fig.add_subplot(121, projection='3d')
o=ax.plot_surface(x, y, z, linewidth=0, facecolors=rgb, antialiased=False, shade=True)
#
ax = fig.add_subplot(122, projection='3d')
ax.plot_surface(x, y, z, color='b' )#, linewidth=0, facecolors=rgb, antialiased=False, shade=False)


plt.show()


