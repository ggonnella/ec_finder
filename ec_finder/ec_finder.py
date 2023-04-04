from pathlib import Path
from shutil import rmtree
from loguru import logger
import sys
import os
import sh
from platformdirs import PlatformDirs
from thefuzz import process

__version__="0.1"
__appname__="EcFinder"
__author__="ggonnella"

ED_BASEFILENAME = "enzyme.dat"
FTP_URL = "ftp.expasy.org/databases/enzyme/" + ED_BASEFILENAME
APPDATADIR = Path(PlatformDirs(__appname__, __author__, \
                              version=__version__).user_data_dir)
ENZYMESDAT = str(APPDATADIR / ED_BASEFILENAME)

def enable_logger(level):
  logger.remove()
  logger.enable("ec_finder")
  msgformat_prefix="<green><dim>{time:YYYY-MM-DD HH:mm:ss}</></>"
  msgformat_content="<level><normal>{level.name}: {message}</></>"
  logger.add(sys.stderr, format=f"{msgformat_prefix} {msgformat_content}",
             level=level)

def download(remotefile, localfile):
  timestampfile = localfile + ".timestamp"
  args = ["-o", localfile, "-w", "%{size_download}", "-R"]
  if os.path.exists(timestampfile):
    args += ["-z", timestampfile]
  try:
    ret = sh.curl("ftp://" + remotefile, *args)
    failed = False
  except sh.ErrorReturnCode:
    failed = True
  if failed:
    ret = sh.curl("https://" + remotefile, *args)
  downloaded = int(ret.rstrip())
  if downloaded > 0:
    sh.touch(timestampfile)
    return True
  else:
    return False

def update(force_download=False):
  enable_logger("INFO")
  logger.info("Data directory: {}".format(APPDATADIR))
  logger.info("Looking for updated enzyme data...")
  if force_download:
    cleanup()
  APPDATADIR.mkdir(parents=True, exist_ok=True)
  updated = download(FTP_URL, ENZYMESDAT)
  if updated:
    logger.info("Updated enzyme data file.")
  else:
    logger.info("No enzyme data file update needed.")

def cleanup():
  if APPDATADIR.exists():
    for path in Path(APPDATADIR).glob("**/*"):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            rmtree(path)

ec_index = None

def parse_local_enzyme_dat():
  logger.info("Parsing local enzyme data file...")
  global ec_index
  ec_index = parse_enzyme_dat(ENZYMESDAT)

def setup():
  enable_logger("INFO")
  logger.info("Initializing emzyme data...")
  logger.info("Data directory: {}".format(APPDATADIR))
  logger.info("Downloading enzyme data...")
  APPDATADIR.mkdir(parents=True, exist_ok=True)
  downloaded = download(FTP_URL, ENZYMESDAT)
  if downloaded:
    logger.info("Downloaded enzyme data file.")
  else:
    logger.error("No enzyme data file found.")
    raise Exception("No enzyme data file found.")
  parse_local_enzyme_dat()

def __auto_setup():
  if not Path(ENZYMESDAT).exists():
    setup()
  else:
    parse_local_enzyme_dat()

def parse_enzyme_dat(enzyme_dat_filename):
    ec_index = {}
    ec_index["main"] = {}
    ec_index["alt"] = {}
    with open(enzyme_dat_filename) as f:
        current_id = None
        for line in f:
            line = line.rstrip()
            if line == "//":
                current_id = None
                continue
            line_type = line[0:2]
            if line_type == "ID":
                current_id = line[5:]
            elif line_type == "DE" and current_id is not None:
                name = line[5:].rstrip(".")
                if "Transferred entry" not in name:
                  ec_index["main"][name] = current_id
            elif line_type == "AN" and current_id is not None:
                name = line[5:].rstrip(".")
                if "Transferred entry" not in name:
                  ec_index["alt"][name] = current_id
    return ec_index

def search(enzyme_name, min_score=90, index=None, separator="\t"):
    if index is None:
      global ec_index
      index = ec_index
    main_names = index["main"]
    alternative_names = index["alt"]
    if enzyme_name in main_names:
        return "MAIN"+separator+main_names[enzyme_name]+separator+enzyme_name
    elif enzyme_name in alternative_names:
        return "ALT"+separator+alternative_names[enzyme_name]+\
            separator+enzyme_name
    else:
        match = process.extractOne(enzyme_name, main_names.keys())
        if match is not None and match[1] >= min_score:
          return "FUZZY:" + match[0] + separator + main_names[match[0]] +\
              separator + enzyme_name
        else:
          match = process.extractOne(enzyme_name, alternative_names.keys())
          if match is not None and match[1] >= min_score:
            return "FUZZY:" + match[0] + separator + \
                alternative_names[match[0]] +\
                separator + enzyme_name
          else:
            return "NOT_FOUND" + separator + separator + enzyme_name
