# Source: Unchirped pulse
## Free space pulse propagation
The simulation script is in [Source/1_Test-0--PeriodicBoundary.py](https://github.com/chunxia2020/MEEP_Simulation/blob/master/Source/Examples/1_Test-0--PeriodicBoundary.py). Before starting the simulation, one needs to specify each of the simulation objects
- IMPORT MEEP :

The first thing to do always is to load the Meep library:
```python
import meep as mp
```
- COMPUTATIONAL CELL

I am going to put a source at one end and let the fields propagate in the _x_ direction. In _x_ direction, I just need to have enough length to show the whole pulse propagation. Let's give it a size of 10 um. As for the boundary conditions. PML is along the _x_-direction, and the periodic boundary condition is along the _y_-direction.
```python
dpml = 1            # thickness of PML layers
dx = 10             # um
dy = 10             # um
sx = dx + dpml * 2  # Total length along x
sy = dy             # Total length along y
cell = mp.Vector3(sx, sy)
```
The `Vector3` object stores the size of the cell in each of the three coordinate direction. This is a 2d cell in _x_ and _y_ where the _z_ direction has size 0.


- GEOMETRY

The pulse will propagate in air, which is the default material in Meep, so no geometry needs to be specified.

- SOURCE

The source is specified using the `sources` object. The source has a wavelength of 1.55 um. In Meep unit, the wavelength = 1.55 /[a], fcen = 1/wavelength = 1/1.55 = 0.645 /[c/a], frequency width df = 0.2 [c/a], where a is the basic space unit in Meep defaulted to 1 um.
```python
lamb = 1.55             # center wavelength
df = 0.2                # frequency bandwidth
fcen = 1/lamb           # center frequency

src_pt = mp.Vector3(-dx/2)  # Center of Source; Right ourside of PML layer
sources = [mp.Source(src=mp.GaussianSource(fcen, fwidth=df, is_integrated=True),
                     component=mp.Ez,
                     center=src_pt,
                     size=mp.Vector3(0, dy))]
```
The [`GaussianSource`](https://meep.readthedocs.io/en/latest/Python_User_Interface/#gaussiansource) is a Gaussian-pulse source with the input of `frequency`, `width`, `start_time`, `cutoff`, `is_integrated` and `fourier_transform(f)`

- `frequency` -- The center frequency _f_ in units of c/a. No default value. One can instead specify `wavelength=x` of `frequency=1/x`
- `width` -- The spectral width _w_ used in the Gaussian. No default value. You can instead specify `fwidth=x`, which is a synonym for `width=1/x` (i.e. the frequency width is proportional to the inverse of the temporal width)
- `start_time` -- The starting time for the source; default is 0 (turn on at _t = 0_). This is not the time of the peak. See below.
- `cutoff` -- How many `width`s the current decays for before it is cut off and set to zero - this applies for both turn-on and turn-off of the pulse. Default is 5.0. A large value of `cutoff` will redue the amount of high-frequency components that are introduced by the start/stop of the source, but will of cource lead to longer simulation times. The peak of the Gaussian is reached at the time _t0_ = `start_time + curoff * width`.
- `is_integrated` -- If `True`, the source is the integral of the current (the dipole moment) which is gauranteed to be zero after the current turns off. In practice, there is little difference between integrated and non-integrated sources except for [planewave extending into PML](https://meep.readthedocs.io/en/latest/Perfectly_Matched_Layer/#planewave-sources-extending-into-pml). Default is `False`.
