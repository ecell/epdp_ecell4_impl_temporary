#!/usr/bin/env/python

import sys

import numpy
import scipy.io
from matplotlib.pylab import *


N_A = 6.0221367e23

def plot_data( N, T, fmt ):

    mean = T.mean(1)
    std_err = T.std()/math.sqrt(len(T))

    #errorbar( N, mean, yerr=std_err, fmt=fmt )
    print N, mean
    loglog( N, mean, fmt )


T=0.001
V=40e-15
#N=100
#C=

Nv = numpy.array([30,100,300,1000,3000,10000,30000,100000,300000])

#constant V
data_V = numpy.array([\
        [0.0107769966125,0.00956392288208,0.00994992256165],
        [0.0418100357056,0.0333521366119,0.0401129722595],
        [0.244478940964, 0.157634019852, 0.203888893127],
        [1.33599901199, 1.13320398331, 1.05681300163],
        [8.47177600861, 8.13043808937, 8.34679794312],
        [66.2307178974, 68.863904953, 70.5964510441],
        [538.8913939,487.579167128,507.513700962],

        #t=0.0001
        [6049.60290909,6236.16215944,6179.99894142],
        #t=0.00001
        [76965.5402899,75303.6808014,76835.8097076]
        ])

Nc = numpy.array([30,100,300,1000,3000,10000,30000,100000,300000,1000000])
#constant C
data_C = numpy.array([\
        [0.0254530906677, 0.11660194397, 0.130806922913],
        [0.207776069641,0.234488964081,0.212745904922],
        [0.821439981461,0.785063028336,0.791114091873],
        [2.82834792137,2.67091798782,3.09029388428],
        [8.47177600861, 8.13043808937, 8.34679794312],
        [27.3884930611,27.0409841537,27.0913190842],
        [82.5484800339, 80.5896220207, 82.0461671352],
        [280.046241999,282.64764905,285.342193127],
        [1995.58594942,2061.35334015,2008.32894087],
        [941063.632011,0,0]
        ])


# (40e-18 ** (1/3.0))**2 / 1e-12
# = 11.69607095285148
data_V *= 11696
data_C *= 11696

Nb = numpy.array([10,30,100,300,1000,3000,10000,30000,100000])
data2 = numpy.array([\
        [0.0333709716797,0.0316069126129,0.0350742340088],
        [0.133962154388,0.144722938538, 0.129770040512],
        [0.453906059265,0.476196050644,0.480502128601],
        [1.31794595718,1.31320905685,1.24801301956],
        [4.22622799873,4.18033003807,4.1173210144],
        [12.1447920799,11.9920589924,12.0459198952],
        [39.7432990074,40.1183140278,39.9150369167],
        [0,0,0],
        [0,0,0]])
data2 *= 1169607
data3 = data2 * 10
data4 = data2 * 100

X = numpy.array([5,100,300,1000,3000,10000,30000,100000,5e6])

#for i in range( len(Nv) ):
plot_data( Nv, data_V,'kx' )
loglog( X, 0.15* X**(5.0/3), 'k--' )

figtext( .2, .15, r'(2) $t \ \propto \ N^{5/3}$', color='k' )

#for i in range( len(Nc) ):
plot_data( Nc, data_C,'ko' )
loglog( X, 30* X, 'k-' )

figtext( .15, .32, r'(1) $t \  \propto \ N$', color='k' )

#for i in range( len(Ns) ):
#    plot_data( Ns[i], data2[i],'k.' )
loglog( X, 4500* X, 'b:' )

#for i in range( len(Nb) ):
plot_data( Nb, data4,'k.' )
loglog( X, 45000* X, 'b:' )

#for i in range( len(Ns) ):
#    plot_data( Ns[i], data4[i],'k.' )
loglog( X, 450000* X, 'b:' )

figtext( .25, .6, r'BD', color='k' )

#loglog( data1[0] , data1[1], 'o-', label='Vol. = 1e-15 L' )
#loglog( data2[0] , data2[1], 'o-', label='# particles = 600' )
#loglog( data3[0] , data3[1], 'o-', label='Conc. = 1e-6 M' )

xlabel( 'N [# particles]' )
#xlabel( 'Concentration [M]' )
ylabel( 'time [sec]' )
#legend()
xlim(4,1e7)
ylim(.1,2e12)

Cx3000=numpy.array([
    9.35e-11,
    9.35e-10,
    9.35e-9,
    9.35e-8,#N=3000,V=40e-15
    9.35e-7,#N=3000,V=40e-16
    9.35e-6,#N=3000,V=40e-17
    9.35e-5,#N=3000,V=40e-18
    9.35e-4

    ])
data_N3000 = numpy.array([\
        [1.06707596779,1.03018307686,1.02773308754],
        [1.19945502281,1.1856508255,1.14539408684],
        [1.87653017044,1.97639083862,1.94779777527],
        [8.47177600861, 8.13043808937, 8.34679794312],
        [50.2359919548,48.7671229839,47.8010251522],
        [585.424571037,660.102545023,601.128531218],

        # t=0.0001
        [14289.9441504,19102.6055598,2176.95770907],
        # t=0.000001
        [292934.114933,293264.955997,291557.028055]
        ])

Cx300=numpy.array([
    9.35e-10,#N=300,V=40e-14
    9.35e-9,#N=300,V=40e-15
    9.35e-8,#16
    9.35e-7,#17
    9.35e-6,#18
    9.35e-5,#19
    9.35e-4,#20
    #3.74e-3#1e-21
    #9.35e-3,#4e-21
    ])
data_N300 = numpy.array([\
        #t=0.01
        [0.0410865068436,0.0368433952332,0.24408197403],
        [0.141018199921,0.18783621788,0.198884987831],
        #t=0.001
        [0.776051998138,0.873686790466,0.605585098267],
        [4.27306294441,4.44240307808,4.74449515343],
        [52.8117170334,77.8340110779,56.4832119942],
        #t=0.0001
        [1731.63747787,173.117349148,1693.01162958],
        [24478.3381939,25384.5009089,23533.4578991],
        #[474846.178055,491588.463068,473160.961151]
        ])

data_N3000 *= 11696
data_N300 *= 11696

axes([.61,.18,.27,.28])

for i in range( len(Cx3000) ):
    plot_data( Cx3000, data_N3000,'k+' )
loglog( Cx3000, 5e6** Cx3000, 'b:' )
bd3000 = numpy.array([12.1447920799,11.9920589924,12.0459198952]).mean()
bd3000 *= 1169607 * 10
loglog( [1e-11,1e-2],[bd3000,bd3000], 'b:' )


for i in range( len(Cx300) ):
    plot_data( Cx300, data_N300,'kd' )
loglog( Cx300, 3e12* Cx300**(4.0/3.0), 'k-.', label='C^(4/3)' )

figtext( .69, .2, r'(3) $t \ \propto \ C^{4/3}$', color='k' )

#bd 300
bd300 = numpy.array([1.31794595718,1.31320905685,1.24801301956]).mean()
bd300 *= 1169607 * 10
loglog( [1e-11,1e-2],[bd300,bd300], 'b:' )

figtext( .65, .4, r'BD', color='k' )

xlabel( 'Concentration [M]' )
ylabel( 'time [sec]' )

#xlim(5e-10,5e-2)
#ylim(1e2,5e9)
xlim(5e-10,5e-3)
ylim(1e2,1e10)


show()




#>>> _gfrd.S_irr( .0001 * 1e-8**2/1e-12, 1e-8, 10 * 1e-8 * 1e-12, 1e-12, 1e-8 )
#0.99116163945434221


