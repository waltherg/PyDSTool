""" Georg Walther (http://georg.io)

    Local Perturbation Analysis of Mori et al. Wave-Pinning System [1].
    The analysis that this code recreates was described in [2].
    The code in this file is adapted from [3], [4], and [5].


    [1] http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2292363/
    [2] http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3480592/
    [3] https://github.com/waltherg/PyDSTool/commit/9b23051e90822664993215a4e31d87abf6524c3b#tests/PyCont_vanDerPol.py
    [4] http://www2.gsu.edu/~matrhc/Tutorial.html
    [5] http://www.ni.gsu.edu/~rclewley/PyDSTool/PyCont.html
"""

## Add path to PyDSTool directory to sys.path
# Here we assume that this source file is located in
# LOCATION/examples
# and that the library code of PyDSTool is located in
# LOCATION/PyDSTool
from os.path import abspath, dirname
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

import PyDSTool as dst
from matplotlib import pylab as pl

## Define ODE System

pars = {'k0': 0.067, 'delta': 1.0, 'g': 1.0, 'K': 1.0,
        'T': 2.26, 'omega': 1}
fnspecs = {
    'f': (['u','v'], 'omega*v*(k0/delta + g*u*u/(delta*(K*K + u*u))) -u'), 
    'vG': (['uG'], 'T - uG')
    }
varspecs = {
    'uL': 'f(uL,vG(uG))',
    'uG': 'f(uG,vG(uG))'
    }
ics = {
    'uL': 1.0,
    'uG': 0.1
    }
t_final = 200

## Set up ODE System as PyDSTool objects

system = dst.args(name='LPA_Mori')
system.pars = pars
system.fnspecs = fnspecs
system.varspecs = varspecs
system.ics = ics
# Some tutorials ask you to set system.tdomain in this version of PyDSTool
# dst.args.tdomain does not exist anymore and needs to be replaced with
# dst.args.tdata
system.tdata = [0.0, t_final]

## Integrate ODE System

ode = dst.Generator.Vode_ODEsystem(system)
trajectory = ode.compute('LPA')
data = trajectory.sample()

pl.plot(data['t'], data['uL'])
pl.plot(data['t'], data['uG'])
pl.draw()

## For bifurcation diagrams, set initial conditions to stable steady state
## attained in the above integration step

ode.set(ics = {'uL': data['uL'][-1], 'uG': data['uG'][-1]})
cont = dst.ContClass(ode)

## Continuation
# Our initial conditions for the above integration were chosen so that
# the in the steady state uL > uG (i.e. the system is said to be perturbable).
# Below we will first continue this heterogeneous (uL != uG) branch

# note: EP-C: Equilibrium Point Curve
cont_args = dst.args(name='equilibrium 1', type='EP-C')
cont_args.freepars = ['T']
cont_args.MaxNumPoints = 1000
cont_args.MaxStepSize = .01
cont_args.MinStepSize = 1e-6
cont_args.StepSize = 1e-3
cont_args.LocBifPoints = ['LP', 'BP']
cont_args.SaveEigen = True
# set parameter domain for each parameter
cont_args.pdomain = {'T': [0.0, 4.0]}
# increase verbosity to see what Continuation is doing
cont_args.verbosity = 1

cont.newCurve(cont_args)
cont['equilibrium 1'].forward()
cont['equilibrium 1'].backward()

# Now, choose one of the branch points on the curve we computed above
# and switch to the homogeneous branch (uL == uG)
cont_args.name = 'equilibrium 2'
cont_args.initpoint = 'equilibrium 1:BP1'
cont_args.initdirec = cont['equilibrium 1'].getSpecialPoint('BP2').\
    labels['BP']['data'].branch
cont_args.LocBifPoints = ['BP']
cont.newCurve(cont_args)
cont['equilibrium 2'].forward()
cont['equilibrium 2'].backward()

pl.figure(frameon=False)
cont.display(['T','uL'], stability=True)
pl.savefig('LPA_Mori_constant_tau_constant_domain_length.pdf', bbox_inces=0)

## Keep Pylab / Matplotlib plots open until user closes them
#pl.show()
