import csv
import xarray as xr
import os
import sys
import netCDF4 as netcdf

def netcdf_to_csv(netcdf_file_in, csv_file_out):
    ds = xr.open_dataset(netcdf_file_in, mode = 'r')
    df = ds.to_dataframe()
    df.to_csv(csv_file_out)

    return csv_file_out

if __name__ == "__main__":
    netcdf_to_csv(sys.argv[0], sys.argv[1])
