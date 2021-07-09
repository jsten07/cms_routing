# -*- coding: utf-8 -*-
"""prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lcvaJYf5k-Y0mmlCYAF8kWQlr2P-eTwr
"""


# Load model
from joblib import dump, load
model_name = "DTR_model"
model = load(model_name + '.joblib')
from datetime import datetime
# model = load("DTR_model.joblib")

"""# Load CMEMS data
Try to use WMS or other more flexibel data retrieval
"""

import ftplib
import os
import numpy as np
import netCDF4 as nc
import pandas as pd

def download(url, user, passwd, ftp_path, filename):
    
    with ftplib.FTP(url) as ftp:
        
        try:
            ftp.login(user, passwd)
            
            # Change directory
            ftp.cwd(ftp_path)
            
            # Download file (if there is not yet a local copy)
            if os.path.isfile(filename):
                print("There is already a local copy of {}".format(filename))
            else:
                with open(filename, 'wb') as fp:
                    ftp.retrbinary('RETR {}'.format(filename), fp.write)
        
        except ftplib.all_errors as e:
            print('FTP error:', e)

# Check contents

"""
with ftplib.FTP('nrt.cmems-du.eu') as ftp:
    
    try:
        ftp.login(UN_CMEMS, PW_CMEMS)
        
        # Change directory
        ftp.cwd('Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/2021/07')
        
        # List directory contents with additional information
        ftp.retrlines('LIST') 
           
        # Get list of directory contents without additional information
        files = []
        ftp.retrlines('NLST', files.append) 
        print(files) 
        
        # Check file size
        print("{} MB".format(ftp.size('mfwamglocep_2020120100_R20201202.nc')/1000000))
            
    except ftplib.all_errors as e:
        print('FTP error:', e)
"""


def calc_relative_direction(ship_dir, ww_dir):
  """
  determine relative wind direction for ships going north, east, south or west

  Parameters
  ----------
  ship_dir : str, in ("N", "E", "S", "W")
    direction the ship is going
  ww_dir : array, float
    array of relative wind directions [0 - 360]
  """
  if ship_dir not in ("N", "E", "S", "W"):
    raise Exception("Direction not accepted.")
  ww_360 = ww_dir
  ww_360[ww_360 < 0] = 360 + ww_dir[0]
  if ship_dir in ("N"):
    dir_4 = np.full((len(ww_dir), 1), 2)
    dir_4[(ww_dir < 45) | (ww_dir > 315)] = 1
    dir_4[(ww_dir > 135) & (ww_dir < 225)] = 3
  if ship_dir in ("E"):
    dir_4 = np.full((len(ww_dir), 1), 2)
    dir_4[(ww_dir > 45) & (ww_dir < 135)] = 1
    dir_4[(ww_dir > 225) & (ww_dir < 315)] = 3
  if ship_dir in ("W"):
    dir_4 = np.full((len(ww_dir), 1), 2)
    dir_4[(ww_dir > 45) & (ww_dir < 135)] = 3
    dir_4[(ww_dir > 225) & (ww_dir < 315)] = 1
  if ship_dir in ("S"):
    dir_4 = np.full((len(ww_dir), 1), 2)
    dir_4[(ww_dir < 45) | (ww_dir > 315)] = 3
    dir_4[(ww_dir > 135) & (ww_dir < 225)] = 1
  return dir_4

def concatenate_cmems(cm_wave, cm_phy, ship_param, ship_dir):
  """
  concatenate the variables from cmems wave and physics datasets

  Parameters
  ----------
  cm_wave : net4CDF dataset
    netcdf file cmems wave
  cm_phy : net4CDF dataset
    netdcf file cmems physics
  ship_param : int
    ship variable that is used in model later (e.g. draft or length)
  ship_dir str, in ("N", "E", "S", "W")
    direction the ship is going
  """
  array = (np.flipud(cm_wave["VHM0"][0, :, :]).data) # extract data from CMEMS
  dim = array.shape
  l = np.prod(dim) # get number of "pixel"

  # extract parameters from cmems dataset and reshape to array with dimension of 1 x number of pixel
  vhm = (np.flipud(cm_wave["VHM0"][0, :, :]).data).reshape(l, 1)
  vtm = (np.flipud(cm_wave["VTPK"][0, :, :]).data).reshape(l, 1)
  temp = (np.flipud(cm_phy["thetao"][0, 1, :, :]).data).reshape(l, 1)
  sal = (np.flipud(cm_phy["so"][0, 1, :, :]).data).reshape(l, 1)
  # create column for ship parameter 
  ship = np.full((l, 1), ship_param) 
  # calculate relative direction of wind depending on ship direction
  dir = calc_relative_direction(ship_dir, (np.flipud(cm_wave["VMDR_WW"][0, :, :]).data).reshape(l, 1))

  # concatenate parameters
  a = np.concatenate((ship, vhm, vtm, temp, sal, dir), axis=1)

  # create pd df from array
  X_pred = pd.DataFrame(data=a,    # values
              index=list(range(0, l)),    # 1st column as index
              columns=["Draft", "VHM0", "VTPK", "thetao", "so", "dir_4"])  # 1st row as the column names
  return X_pred

def prepare_grid(model, cm_wave, cm_phy, ship_param, ship_dir):
  """
  prepare grid of SOGs

  Parameters
  ----------
  model : joblib model
    model used for prediction; currently need the independent variables 
    "Draft", "VHM0", "VTPK", "thetao", "so", "dir_4"
  cm_wave : net4CDF dataset
    netcdf file cmems wave
  cm_phy : net4CDF dataset
    netdcf file cmems physics
  ship_param : int
    ship variable that is used in model later (e.g. draft or length)
  ship_dir str, in ("N", "E", "S", "W")
    direction the ship is going
  """

  X_pred = concatenate_cmems(cm_wave, cm_phy, ship_param, ship_dir)
  
  # extract shape from cmems data
  input = (np.flipud(cm_wave["VHM0"][0, :, :]).data)
  dim = input.shape

  # predict SOG
  SOG_pred = model.predict(X_pred)
  SOG_pred = SOG_pred.reshape(dim) # reshape to 'coordinates'
  SOG_pred[input < -30000] = -5 # -32767.0 # mask data with negative value

  return SOG_pred

'''
# created masked array
import numpy.ma as ma
SOG_pred = np.ma.masked_where(np.flipud(np.ma.getmask(ds[parameter][0, :, :])), SOG_pred.reshape(dim))
SOG_pred.fill_value = -32767
# SOG_pred =np.flipud(SOG_pred)
'''

# # create actual grids for different ship directions
# ship_param = 12
# SOG_N = prepare_grid(model, ds, ds_p, ship_param, "N")
# SOG_E = prepare_grid(model, ds, ds_p, ship_param, "E")
# SOG_S = prepare_grid(model, ds, ds_p, ship_param, "S")
# SOG_W = prepare_grid(model, ds, ds_p, ship_param, "W")

# def cmems_paths(date):


def get_cmems(date_start, date_end, UN_CMEMS, PW_CMEMS):
    date_s = datetime.strptime(date_start, "%d.%m.%Y %H:%M")
    date_e = datetime.strptime(date_end, "%d.%m.%Y %H:%M")

    date_m = date_s + (date_e - date_s) / 2
    date = date_m.strftime("%Y%m%d")
    today = datetime.now().strftime("%Y%m%d")

    path_date = date[0:4] + "/" + date[4:6]
    url = 'nrt.cmems-du.eu'
    path_w = 'Core/GLOBAL_ANALYSIS_FORECAST_WAV_001_027/global-analysis-forecast-wav-001-027/' + path_date
    path_p = 'Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/' + path_date

    with ftplib.FTP(url) as ftp:
        try:

            ftp.login(UN_CMEMS, PW_CMEMS)
            ftp.cwd(path_w)
            files = ftp.nlst()
            files = [i for i in files if date in i]
            filename_w = files[0]
            ftp.cwd('/')
            ftp.cwd(path_p)
            files = ftp.nlst()
            files = [i for i in files if date in i]
            filename_p = files[0]
        except ftplib.all_errors as e:
            print('FTP error:', e)

    download(url, UN_CMEMS, PW_CMEMS, path_w, filename_w)
    download(url, UN_CMEMS, PW_CMEMS, path_p, filename_p)

    ds_w = nc.Dataset(filename_w)
    ds_p = nc.Dataset(filename_p)
    return (ds_w, ds_p)


""""
# set CMEMS credentials
UN_CMEMS = "jstenkamp"
PW_CMEMS = ""

# cmems wave data download
url = 'nrt.cmems-du.eu'
path = 'Core/GLOBAL_ANALYSIS_FORECAST_WAV_001_027/global-analysis-forecast-wav-001-027/2021/07'
filename = 'mfwamglocep_2021070200_R20210703.nc'
download(url, UN_CMEMS, PW_CMEMS, path, filename)

# cmems physics download
url = 'nrt.cmems-du.eu'
path = 'Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/2021/07'
filename_p = 'mercatorpsy4v3r1_gl12_mean_20210702_R20210703.nc'
download(url, UN_CMEMS, PW_CMEMS, path, filename_p)



# load files as netcdf dataset
ds = nc.Dataset(filename)
ds_p = nc.Dataset(filename_p)
# ds
"""
