#!/usr/bin/python2.7
import platform, os, shutil
from .cembed import process, safename

OUTPUT = "bin/nantag"
EMBED_DIR = ""
TEMPSRC_DIR = ".tempsrc"
COMPILER = "gcc"
INCLUDE_PATH = [
  TEMPSRC_DIR,
  "src/include",
]
SOURCE = [
  "src",
]
FLAGS = [ "-Wall", "-Wextra", "--std=c99", "-fno-strict-aliasing", "-Wno-unused-parameter" ]
LINK = [ "m" ]
LINK_PATH = [  ]
LINK_FLAGS = [ ]
DEFINE = [  ]
EXTRA = [  ]


def config_setup(build):
  global OUTPUT, LINK, FLAGS, LINK_FLAGS
  if platform.system() == "Windows":
    # sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    OUTPUT += ".exe"
    LINK += [ "mingw32" ]
  
  # Handle build type
  if build == "debug":
    FLAGS += [ "-g"  ]
  else:
    FLAGS += [ "-O3", "-flto" ]
    LINK_FLAGS += [ "-flto" ]


def config_build():
  # Create embedded-file header files
  if os.path.exists(EMBED_DIR):
    for filename in os.listdir(EMBED_DIR):
      fullname = EMBED_DIR + "/" + filename
      res = process(fullname)
      open(TEMPSRC_DIR + "/" + safename(fullname) + ".h", "wb").write(res)


def config_cleanup():
  if os.path.exists(TEMPSRC_DIR):
    shutil.rmtree(TEMPSRC_DIR)
