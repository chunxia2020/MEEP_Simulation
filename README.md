# MEEP_Simulation
## How to compute the _steady-state fields_?
The "steady-state" response is defines as the exp(-iwt) source after all transients have died away. There are three different approaches for computng the steady-state fields:
 - (1). Use FDTD with a continuous-wave (CW) source via `ContinuousSource` with smooth turn-on and run for a long time (i.e., >>1/f)