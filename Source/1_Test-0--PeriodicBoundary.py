"""
  Goal : Still a plane wave with periodic boundary condition?
    INPUT:
        - 2D simulation
        - plane wave
        - y PML
        - z periodic boundary condition
    Output:
        - The change of electric field with time
"""

import meep as mp
import numpy as np
import math
import cmath
import pickle

"""======================== 0. Parameters =============================="""
resolution = 10         # pixels/um
# ------------------ 0. FILE PATH               ---------------------
prefix = 'SCRIPTS/16_CLE-PhC/1-0/'         # Epsilon file path
file_path = '/home/ubuntu/SCRIPTS/16_CLE-PhC/1-0/'
# ------------------ 2. Planewave ----------------------------
lamb = 1.55             # center frequency
df = 0.2
fcen = 1/lamb
# ------------------ 3. PML and padding -----------------------------
dpml = 1                # thickness of PML layers

dx = 10         # um
dy = 10         # um

"""======================== 1. Cell Size ==============================="""
sx = dx + dpml * 2
sy = dy

cell = mp.Vector3(sx, sy)
"""======================== 2. Souce : Plane wave ======================"""
src_pt = mp.Vector3(-dx/2)  # Center of Source; Right ourside of PML layer
sources = [mp.Source(src=mp.GaussianSource(fcen, fwidth=df, is_integrated=True),
                     component=mp.Ez,
                     center=src_pt,
                     size=mp.Vector3(0, dy))]
"""======================== 3. Boundary Condition ======================"""
k_point = mp.Vector3(0,0,0)
pml_layers = [mp.PML(thickness=dpml, direction=mp.X)]
"""======================== 4. Symmetry ================================"""
sym = [mp.Mirror(mp.Y, phase=1), mp.Mirror(mp.Z, phase=-1)]
"""======================== 5. Configure and run Sim ==================="""
sim = mp.Simulation(cell_size=cell,
            filename_prefix=prefix,
            # load_structure = Dump,    # Load dumped epsilon file
            split_chunks_evenly=True,  # Split into chunks by cost instead of evenly
            # geometry=geometry,
            boundary_layers=pml_layers,
            sources=sources,
            k_point=k_point,    # Periodic boundary condition
            symmetries=sym,
            force_complex_fields=True,
            resolution=resolution)

""" Create an array to save the real part of the electric field at (-dx/2,0) """
Ez_point_array = []
def my_step(sim):
       ez_point_data = sim.get_array(center=mp.Vector3(-dx/2), size=mp.Vector3(0, 0), component=mp.Ez)
       Ez_point_array.append(ez_point_data.real)
sim.run(my_step, until = 50)

"""======================== 6. Plot the Ez field    ==================="""



# eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)

# ======================== 1. Plot field ================================

# fig, ax = plt.subplots()
# # plt.imshow(eps_data.real.transpose(), interpolation='spline36', cmap='binary')
# cs = ax.imshow(ez_data.real.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
# ax.axis('off')
# cbar = fig.colorbar(cs)
# plt.show()
# ========= 2. Point plot of all the pixels along y at x = dx/2 ==========
import matplotlib as mpl
mpl.rcParams['axes.linewidth'] = 1.6 #set the value globally
mpl.rcParams.update({'font.size': 12})
import matplotlib.pyplot as plt
fig, ax = plt.subplots()

x = np.linspace(1, len(Ez_point_array), len(Ez_point_array))
x = x.transpose()/resolution/2
text1 = 'f_center = ' + str(round(fcen, 3)) + '/[c/a]'
text2 = 'df = ' + str(df) + '/[c/a]'
Savefilepath = file_path + 'Rising E Field.png'

ax.plot(x, Ez_point_array/np.amax(Ez_point_array))
ax.set_title('Rising up of the electrical field')
ax.set_xlabel('Meep time / [a/c]')
ax.set_ylabel('Normalized Ez field')
ax.tick_params(direction='in', length=6, width=2)
ax.text(32, -0.6, text1, fontsize=12)
ax.text(32, -0.75, text2, fontsize=12)
plt.savefig(Savefilepath)
plt.show()
