import os
import sys
import argparse
from subprocess import call

def structure_gen(casename, grids, atmos_res, ocean_res):
    """
    generate the esgf publication structure

    Parameters
    ----------
        casename (str): the name of the run
        grids (list(str)): any grids in addition to native that are being published
        atmos_res (str): the atmospheric resolution i.e. 1deg
        ocean_res (str): the ocean resolution i.e. 60-30km
    """
    data_types = ['atmos', 'land', 'ocean', 'sea-ice']
    makedir(casename)
    res_dir = os.path.join(
        casename,
        '{atm_res}_atm_{ocn_res}_ocean'.format(
            atm_res=atmos_res,
            ocn_res=ocean_res))
    makedir(res_dir)
    for dtype in data_types:
        dtype_dir = os.path.join(res_dir, dtype)
        makedir(dtype_dir)
        grid_dir = os.path.join(dtype_dir, 'native')
        makedir(grid_dir)
        makedir(os.path.join(
            grid_dir, 'model-output', 'mon', 'ens1', 'v1'))
        if dtype in ['atmos', 'land']:
            for grid in grids:
                grid_dir = os.path.join(dtype_dir, grid)
                makedir(grid_dir)
                makedir(os.path.join(
                    grid_dir, 'model-output', 'mon', 'ens1', 'v1'))
                if dtype == 'atmos' and grid != 'native':
                    makedir(os.path.join(grid_dir, 'climo',
                                         'monClim', 'ens1', 'v1'))
                    makedir(os.path.join(grid_dir, 'climo',
                                         'seasonClim', 'ens1', 'v1'))
                    makedir(os.path.join(
                        grid_dir, 'time-series', 'mon', 'ens1', 'v1'))
        cmd = 'chmod -R a+rx {}'.format(casename)
        call(cmd)

def makedir(directory):
    """
    Make a directory if it doesnt already exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--case-name',
        help='The name of the case')
    parser.add_argument(
        '-g',
        '--grids',
        nargs='+',
        help='names of grids in addition to "native" directories to create, only applies to atmos and land')
    parser.add_argument(
        '-a',
        '--atmos-resolution',
        help='resolution name for atmos i.e. 1deg')
    parser.add_argument(
        '-o',
        '--ocean-resolution',
        help='resolution name for ocean i.e. 60-30km')

    try:
        _args = sys.argv[1:]
    except:
        parser.print_help()
        sys.exit(1)
    else:
        _args = parser.parse_args(_args)

    structure_gen(
        _args.case_name,
        _args.grids,
        _args.atmos_resolution,
        _args.ocean_resolution)
