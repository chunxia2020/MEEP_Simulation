# 


## Is a narrow-bandwidth Gaussian pulse considered the same as a continuous-wave (CW) source?

No. A narrow-bandwidth Gaussian is still a Gaussian: it goes to zero at both the beginning and end of its time profile unlike a continuous-wave (CW) source which oscillates indefinitely (but has a [finite turn-on](https://meep.readthedocs.io/en/latest/FAQ/#why-doesnt-the-continuous-wave-cw-source-produce-an-exact-single-frequency-response)). Assuming you have linear materials, you should get the same results if you use a narrow or broadband pulse and look at a single frequency component of the Fourier transform via e.g. `dft_fields`. The latter has the advantage that it requires a shorter simulation for the fields to decay away due to the [Fourier Uncertainty Principle](https://en.wikipedia.org/wiki/Fourier_transform#Uncertainty_principle), which basically says the more spread out the frequency spectrum is, the short the pulse will be. 


Note also that an almost zero-bandwidth Gaussian beam will produce high-frequency spectral components due to its abrupt turn on and off which are poorly absorbed by PML.

## Why doesn't the continuous-wave (CW) source produce an exact single-frequency response?

The ``ContinuousSource``
