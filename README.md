
# MEEP_Simulation
## How to compute the _steady-state fields_?
 The "steady-state" response is defines as the exp(-iwt) source after all transients have died away. There are three different approaches for computng the steady-state fields:
 - Use FDTD with a continuous-wave (CW) source via `ContinuousSource` with [smooth turn-on](https://meep.readthedocs.io/en/latest/FAQ/#why-doesnt-the-continuous-wave-cw-source-produce-an-exact-single-frequency-response) and run for a long time (i.e., >>1/f)
 - Use FDFD, the [frequency-domain solver](https://meep-hr.readthedocs.io/en/latest/Python_User_Interface/#frequency-domain-solver)
 - Use FDTD with a broad-bandwidth pulse (which has short time duration) via `GaussianSource` and compute the Fourier-transform of the fields via `add_dft_fields`.


 Often, (2) and (3) require fewer timesteps to converge than (1). Note that MEEP uses real fields by default and if one want complex amplitudes, one must set `force_complex_fields=True`. More detailed information can be found [here](https://meep.readthedocs.io/en/latest/FAQ/#how-do-i-compute-the-steady-state-fields).
