from pylab import *

# --- load and process halo catalogue from Rockstar ---

halocat = loadtxt("~/halos_37.0.ascii") #change location of where the rockstar halo cat is stored 

boxsize = 100.0              # comoving boxsize in Mpc / h

m200c = halocat[:,27]       # spherical overdensity mass M200c in Msun / h

ind = where(m200c > 0)[0]                                  # exclude FoF groups that for which no M200c value is found
massfunc,binedges = histogram(log10(m200c[ind]),bins=20)   # compute histogram of halo masses
binright = binedges[1:]                                    # right edge of mass bin

n_gtr_m = (massfunc.sum() - massfunc.cumsum()) / boxsize**3 # compute n(>m)

# --- plot results ---

fig = figure()
ax = fig.add_subplot(111)

ax.plot(binright, n_gtr_m, c="blue", label="sim")

ax.set_yscale("log")
ax.legend()
ax.set_xlabel(r"log10(mass/($M_\odot / h$)]")
ax.set_ylabel(r"n(>m) [$h^3 / {\rm Mpc}^3$]")

fig.show()

fig.savefig("hmf.jpg", dpi = 100)

