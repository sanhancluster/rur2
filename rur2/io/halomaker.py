from rur2.io.io_hm import io_hm
import numpy as np

halo_dtype = [
    ('nparts', 'i4'), ('id', 'i4'), ('iout', 'i4'), ('level', 'i4'),
    ('host', 'i4'), ('hostsub', 'i4'), ('nbsub', 'i4'), ('nextsub', 'i4'),
    ('aexp', 'f4'), ('m', 'f4'), ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
    ('vx', 'f4'), ('vy', 'f4'), ('vz', 'f4'),
    ('Lx', 'f4'), ('Ly', 'f4'), ('Lz', 'f4'),
    ('r', 'f4'), ('a', 'f4'), ('b', 'f4'), ('c', 'f4'),
    ('ek', 'f4'), ('ep', 'f4'), ('et', 'f4'), ('spin', 'f4'),
    ('rvir', 'f4'), ('mvir', 'f4'), ('tvir', 'f4'), ('cvel', 'f4'),
    ('rho0', 'f4'), ('rc', 'f4')]

galaxy_dtype = [
    ('nparts', 'i4'), ('id', 'i4'), ('iout', 'i4'), ('level', 'i4'),
    ('host', 'i4'), ('hostsub', 'i4'), ('nbsub', 'i4'), ('nextsub', 'i4'),
    ('aexp', 'f4'), ('m', 'f4'), ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
    ('vx', 'f4'), ('vy', 'f4'), ('vz', 'f4'),
    ('Lx', 'f4'), ('Ly', 'f4'), ('Lz', 'f4'),
    ('r', 'f4'), ('a', 'f4'), ('b', 'f4'), ('c', 'f4'),
    ('ek', 'f4'), ('ep', 'f4'), ('et', 'f4'), ('spin', 'f4'),
    ('sigma', 'f4'), ('sigma_bulge', 'f4'), ('m_bulge', 'f4'),
    ('rvir', 'f4'), ('mvir', 'f4'), ('tvir', 'f4'), ('cvel', 'f4'),
    ('rho0', 'f4'), ('rc', 'f4')]

galaxy_dtype_dp = [
    ('nparts', 'i4'), ('id', 'i4'), ('iout', 'i4'), ('level', 'i4'),
    ('host', 'i4'), ('hostsub', 'i4'), ('nbsub', 'i4'), ('nextsub', 'i4'),
    ('aexp', 'f8'), ('m', 'f8'), ('x', 'f8'), ('y', 'f8'), ('z', 'f8'),
    ('vx', 'f8'), ('vy', 'f8'), ('vz', 'f8'),
    ('Lx', 'f8'), ('Ly', 'f8'), ('Lz', 'f8'),
    ('r', 'f8'), ('a', 'f8'), ('b', 'f8'), ('c', 'f8'),
    ('ek', 'f8'), ('ep', 'f8'), ('et', 'f8'), ('spin', 'f8'),
    ('sigma', 'f8'), ('sigma_bulge', 'f8'), ('m_bulge', 'f8'),
    ('rvir', 'f8'), ('mvir', 'f8'), ('tvir', 'f8'), ('cvel', 'f8'),
    ('rho0', 'f8'), ('rc', 'f8')]

def read(path, istart, iend, galaxy=True, read_members=False, double_precision=True):
    # boxsize: comoving length of the box in Mpc
    if(iend is None):
        iend = istart+1

    if(galaxy):
        if(not double_precision):
            dtype = galaxy_dtype
        else:
            dtype = galaxy_dtype_dp
    else:
        dtype = halo_dtype

    #print("Searching for tree_brick in ", path)
    io_hm.read_bricks(path, galaxy, istart, iend, read_members, double_precision)

    if(not double_precision):
        array = np.rec.fromarrays([*io_hm.integer_table.T, *io_hm.real_table.T], dtype=dtype)
    else:
        array = np.rec.fromarrays([*io_hm.integer_table.T, *io_hm.real_table_dp.T], dtype=dtype)

    if(array.size==0):
        print("No tree_brick file found, or no halo found in %s" % path)

    if(read_members):
        return array, io_hm.part_ids
    else:
        return array

