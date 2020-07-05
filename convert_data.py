"""Usage: convert_data.py

Convert downloaded csv data to the correctly readable data

Options:
  -h, --help  show this help message and exit
"""
import os
import re
import json
import datetime
from japanera import Japanera, EraDate, Era

from natsort import natsorted

def extract_date(title: str):
  """extract date object from title string

  Args:
      title (str): Title string, like マイナンバーカード交付状況（令和2年6月1日現在)

  Returns:
      datetime: Date object
  """
  janera = Japanera()
  match =  re.search(r'[（(](.*)[)）]', title)
  if (not match):
    return False
  datesource = re.search(r'([^0-9元]*)([0-9元]*)年(.*)月(.*)日', match.groups()[0])
  mydate = janera.strptime('{0}{1}年{2}月{3}日'.format(
    datesource.groups()[0],
    datesource.groups()[1].replace('元','1').zfill(2),
    datesource.groups()[2].zfill(2),
    datesource.groups()[3].zfill(2)
  ), "%-E%-o年%m月%d日")
  return mydate[0]


RAW_DIR = './data/raw'
OUT_DIR = './data/out'
# DATA FILE
DATA_FILE = "./data/loaded_files.json"

# If data file does not exist, finish process
if (not os.path.exists(DATA_FILE)):
  print('Error: data file {0} does not extst. Run download.py first'.format(DATA_FILE))
  exit(1)

# load data file
with open(DATA_FILE) as f:
  loaded: dict = json.load(f)

# create dir if it does not exist
if (not os.path.exists(OUT_DIR)):
  os.makedirs(OUT_DIR)

for key in loaded.keys():
  date = extract_date(loaded.get(key))
  if (not date):
    print('The system could not retrieve date string from the title "{0}" '.format(loaded.get(key)))
    continue
  print('Create file for the date {0}'.format(date))
  target_dir = RAW_DIR + '/' + key
  if (not os.path.exists(target_dir)):
    print('The data for the key {0} does not exists. Skip this key'.format(key))
    continue
  for csv in natsorted(os.listdir(target_dir)):
    print(csv)
    