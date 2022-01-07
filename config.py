import core
import external


unit_dimension = external.AliasDict({
    ('g', 'Msol') : (1, 0, 0),
    ('cm', 'm', 'km', 'pc', 'kpc', 'Mpc') : (0, 1, 0),
    ('s', 'yr', 'kyr', 'Myr', 'Gyr') : (0, 0, 1),
    ('km/s', 'm/s') : (0, 1, -1),
    ('K') : (0, 2, -2),
    ('g/cc', 'H/cc', 'Msol/pc3', 'Msol/kpc3', 'Msol/Gpc3') : (1, -3, 0),
    ('Msol/pc2', 'Msol/kpc2', 'Msol/Gpc2') : (1, -2, 0),
})

# Unit scales
cgs = {
    'g' : 1.,
    'Msol' : 2E33,

    'cm' : 1.,
    'm' : 1E3,
    'km' : 1E5,
    'pc' : 3.08E22,
    'kpc' : 3.08E25,
    'Mpc' : 3.08E28,
}

# Aliases
alias_common = core.Alias({
    'm'   : 'mass',
    'pos' : 'position',
    'vel' : 'velocity',
    'aexp' : 'scale_factor',
    'scale' : 'scale_factor',
    'iout' : 'timestep',
})

# 'x', 'y', 'z', 'vx', 'vy', 'vz', 'npart', 'rmax', 'Lx', 'Ly', 'Lz'

alias_velociraptor = core.Alias({
    'x' : 'Xc',
    'y' : 'Yc',
    'z' : 'Zc'
})

alias_HaloMaker = core.Alias({
    'npart' : 'nparts',
    'sig' : 'sigma',
})
alias_HaloMaker.update(alias_common)

extra_fields_common = {
    'x' : lambda table: table.data['position'][..., 0],
    'y' : lambda table: table.data['position'][..., 1],
    'z' : lambda table: table.data['position'][..., 2],
    'vx' : lambda table: table.data['velocity'][..., 0],
    'vy' : lambda table: table.data['velocity'][..., 1],
    'vz' : lambda table: table.data['velocity'][..., 2],
}

