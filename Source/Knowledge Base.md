# 


## Is a narrow-bandwidth Gaussian pulse considered the same as a continuous-wave (CW) source?

No. A narrow-bandwidth Gaussian is still a Gaussian: it goes to zero at both the beginning and end of its time profile unlike a continuous-wave (CW) source which oscillates indefinitely (but has a [finite turn-on](https://meep.readthedocs.io/en/latest/FAQ/#why-doesnt-the-continuous-wave-cw-source-produce-an-exact-single-frequency-response)). Assuming you have linear materials, you should get the same results if you use a narrow or broadband pulse and look at a single frequency component of the Fourier transform via e.g. `dft_fields`. The latter has the advantage that it requires a shorter simulation for the fields to decay away due to the [Fourier Uncertainty Principle](https://en.wikipedia.org/wiki/Fourier_transform#Uncertainty_principle), which basically says the more spread out the frequency spectrum is, the short the pulse will be. 


Note also that an almost zero-bandwidth Gaussian beam will produce high-frequency spectral components due to its abrupt turn on and off which are poorly absorbed by PML.

## Why doesn't the continuous-wave (CW) source produce an exact single-frequency response?

The [`ContinuousSource`](https://meep.readthedocs.io/en/latest/Python_User_Interface/#continuoussource) does not produce an exact single-frequency response exp(-iwt) due to its finite turn-on time which is described by a hyperbolic-tangent function. In the asymptotic limit, the resulting fields are the single-frequency response; it's just that if you Fourier transform the response over the entire simulation you will see a finite bandwidth due to the turn-on. 


For the turning-on process: If the `width` is 0 (the default) then the source turns on sharply which creates high-frequency transient effects. Otherwise, the source turns on with a shape of (1+tanh( t/`width` - `slowness` ))/2. That is, the `width` parameter controls the width of the turn-on. The `slowness` parameter controls how far into the exponential tail of the tanh function the source turns on. The default `slowness` of 3.0 means that the source turns on at (1+tanh(-3))/2 = 0.00247 of its maximum amplitude. A larger value for `slowness` means that the source turns on even more gradually at the beginning (i.e., farther in the exponential tail). The effect of varying the two parameters `width` and `slowness` independently in the turn-on function is shown below.
