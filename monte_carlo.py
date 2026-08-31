import numpy as np
rng = np.random.default_rng(20260824)   # fixed seed, reported in the paper
N = 200_000

# Jeffreys posteriors Beta(k+1/2, n-k+1/2) for each measured proportion
c    = rng.beta(57 + .5,  67-57 + .5,  N)      # database coverage 57/67
rdb  = rng.beta(2  + .5,  80-2  + .5,  N)      # database-path omission 2/80
rcam = rng.beta(107+ .5, 262-107+ .5,  N)      # camera-path FNR 107/262

R      = c*rdb + (1-c)*rcam
share  = (1-c)*rcam / R

def q(x, lab, pct=True):
    m = 100 if pct else 1
    lo, md, hi = np.percentile(x, [2.5, 50, 97.5])
    print(f"{lab:<44} median {m*md:6.1f}   95% CrI [{m*lo:5.1f}, {m*hi:5.1f}]")

print("Monte Carlo, 200k draws, Jeffreys posteriors, seed 20260824\n")
q(c,    "database coverage c")
q(rdb,  "database-path omission r_db")
q(rcam, "camera-path FNR r_cam")
print()
q(R,     "aggregate allergen risk R")
q(share, "camera-path share of R")
print()
print(f"P(r_cam > r_db)                              {100*np.mean(rcam>rdb):.2f}%")
print(f"P(camera share > 50%)                        {100*np.mean(share>0.5):.1f}%")
print(f"P(camera share > 2/3)                        {100*np.mean(share>2/3):.1f}%")
ratio = rdb/rcam
lo,md,hi = np.percentile(1/ratio, [2.5,50,97.5])
print(f"r_cam / r_db  median {md:.1f}x  95% CrI [{lo:.1f}, {hi:.1f}]")
print()
# how much does +10pp coverage buy, in the same units
dR = (rdb - rcam)*0.10
q(-dR, "risk reduction from +10pp coverage (pp)")
