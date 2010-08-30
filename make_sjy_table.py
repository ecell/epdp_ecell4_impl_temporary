#!/usr/bin/python


import math
import numpy
import scipy.special as special

import string



def minz_j(n):
    
    # We can start table interpolation from zero because there is
    # no singularity in bessel_j for z>=0.
    return 0

def minz_y(n):

    #return max(3., n)
    return .5


def maxz_j(n):

    z = (n * n + n + 1) / 1.221e-4

    if z >= 1000:
        z = max(1000, n * n)

    return z


def maxz_y(n):

    # from gsl/special/bessel_y.c:
    #  else if(GSL_ROOT3_DBL_EPSILON * x > (l*l + l + 1.0)) {
    #     int status = gsl_sf_bessel_Ynu_asympx_e(l + 0.5, x, result);
    #     ...
    z = (n * n + n + 1) / 6.06e-6

    # ... but this is usually too big.
    if z >= 2000:
        z = max(2000, n * n)

    return z


def jnyn(n, resolution):

    delta = numpy.pi / resolution
    z_table = numpy.mgrid[min(minz_j(n),minz_y(n)):max(maxz_j(n), maxz_y(n)):delta]

    j_table = numpy.zeros((len(z_table), n+1))
    jdot_table = numpy.zeros((len(z_table), n+1))
    y_table = numpy.zeros((len(z_table), n+1))
    ydot_table = numpy.zeros((len(z_table), n+1))

    for i, z in enumerate(z_table):
        j_table[i], jdot_table[i], y_table[i], ydot_table[i] \
            = special.sph_jnyn(n, z)

    j_table = j_table.transpose()
    jdot_table = jdot_table.transpose()
    y_table = y_table.transpose()
    ydot_table = ydot_table.transpose()
    return z_table, j_table, jdot_table, y_table, ydot_table

def make_table(func, n, z0, z1, tol):

    z = z0

    dz = numpy.pi / 100

    j, jp = func(n, z)
    j_prev = j[n]
    jp_prev = jp[n]
    jpp_prev = 0

    z_table = numpy.array([z, ])
    y_table = numpy.array([j[n], ])

    while z < z1:
        j, jp = func(n, z + dz)
        abs_jpp_norm = abs((jp[n] - jp_prev) * dz)

        if abs_jpp_norm > tol:# or abs(j[n] - j_prev) > tol:
            dz *= .5
            continue 

        z += dz

        z_table = numpy.append(z_table, z)
        y_table = numpy.append(y_table, j[n])

        if abs_jpp_norm < tol * .5:
            dz *= 2

        jpp_prev = abs_jpp_norm
        jp_prev = jp[n]

    assert len(z_table) == len(y_table)

    return z_table, y_table


def write_header(file):

    template = '''#ifndef SPHERICAL_BESSEL_TABLE_HPP
#define SPHERICLA_BESSEL_TABLE_HPP

/* Auto-generated by a script.  Do not edit. */

namespace sb_table
{

struct Table
{
    const unsigned int N;
    const double x_start;
    const double delta_x;
    const double* const y;
};
'''

    file.write(template)

def write_footer(file):

    template = '''
}  // namespace sbjy_table

#endif /* SPHERICAL_BESSEL_TABLE_HPP */
'''

    file.write(template)

def write_table_array(file, name, minn, maxn):

    file.write('static unsigned int %s_min(%d);\n' % (name, minn)) 
    file.write('static unsigned int %s_max(%d);\n' % (name, maxn)) 
    file.write('static const Table* %s[%d + 1] =\n{\n' % (name, maxn)) 

    for n in range(minn):
        file.write('    0,\n')

    for n in range(minn, maxn+1):
        file.write('    &%s%d,\n' % (name, n))

    file.write('};\n\n')


def write_array(file, name, table):

    head_template = '''
static const double %s[%d + 1] =
{\n'''

    number_template = '''    %.18f'''
    foot_template = '''};\n'''

    N = len(table)

    file.write(head_template % (name, N))
    file.write(',\n'.join([number_template % n for n in table]))
    file.write(foot_template)

def write_arrays(file, name, table1, table2):

    head_template = '''
static const double %s[%d + 1] =
{\n'''

    number_template = '''    %.18e, %.18e'''
    foot_template = '''};\n'''

    # check if len(table1) == len(table2)
    N = len(table1)

    file.write(head_template % (name, N * 2))

    file.write(',\n'.join([number_template % (value, table2[i]) for i, value in enumerate(table1)]))

    file.write(foot_template)


def write_table(file, name, N, x_start, delta_x):

    struct_template = '''
static const Table %s = { %d, %.18f, %.18f, %s_f };

'''

    file.write(struct_template % (name, N, x_start, delta_x, name))



if __name__ == '__main__':

    import sys

    filename = sys.argv[1]

    file = open(filename, 'w')

    minn_j = 4
    # this should be larger (than maxn_y), but the table bloats.
    maxn_j = 51

    minn_y = 3
    # GSL always uses Olver asymptotic form for n > 40
    maxn_y = 40


    resolution = 35

    write_header(file)

    z_table, j_table, jdot_table, y_table, ydot_table \
        = jnyn(max(maxn_j, maxn_y), resolution)

    delta_z = z_table[1]-z_table[0]

    # j
    for n in range(minn_j, maxn_j + 1):

        start = numpy.searchsorted(z_table, minz_j(n))
        end = numpy.searchsorted(z_table, maxz_j(n))
        z_start = z_table[start]
        j = j_table[n][start:end]
        jdot = jdot_table[n][start:end]
        write_arrays(file, 'sj_table%d_f' % n, j, jdot)
        write_table(file, 'sj_table%d' % n, end-start, z_start, delta_z)
        print 'j', n, len(j)

    # y
    for n in range(minn_y, maxn_y + 1):

        start = numpy.searchsorted(z_table, minz_y(n))
        end = numpy.searchsorted(z_table, maxz_y(n))
        z_start = z_table[start]
        y = y_table[n][start:end]
        ydot = ydot_table[n][start:end]
        write_arrays(file, 'sy_table%d_f' % n, y, ydot)
        write_table(file, 'sy_table%d' % n, end-start, z_start, delta_z)

        print 'y', n, len(y)

    write_table_array(file, 'sj_table', minn_j, maxn_j)
    write_table_array(file, 'sy_table', minn_y, maxn_y)

    write_footer(file)

    file.write('\n')

    file.close()

