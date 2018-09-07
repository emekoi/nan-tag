#!/usr/bin/python2.7
import os, sys, shutil, platform, time
from config import *


def fmt(fmt, dic):
  for k in dic:
    fmt = fmt.replace("{" + k + "}", str(dic[k]))
  return fmt


def listFiles(directory):
  for root, subdir, sources in os.walk(directory):
    for source in sources:
      yield os.path.join(root, source)


def compile_object_file(verbose, source, output):
  cmd = fmt(
    "{compiler} -c -o {tempsrc}/{output} {flags} {include_path} {define} {source} " +
    "{extra}", {

    "compiler"     : COMPILER,
    "tempsrc"      : TEMPSRC_DIR,
    "output"       : output,
    "source"       : source,
    "include_path" : " ".join(map(lambda x:"-I" + x, INCLUDE_PATH)),
    "define"       : " ".join(map(lambda x:"-D" + x, DEFINE)),
    "flags"        : " ".join(FLAGS),
    "extra"        : " ".join(EXTRA),
  })

  if verbose:
    print(cmd)

  return os.system(cmd)

def compile_executable(verbose):
  cmd = fmt(
    "{compiler} -o {output} {flags} {tempsrc}/*.o {linker_path} {link}", {
    "compiler"     : COMPILER,
    "tempsrc"      : TEMPSRC_DIR,
    "output"       : OUTPUT,
    "flags"        : " ".join(LINK_FLAGS),
    "linker_path"  : " ".join(map(lambda x:"-L" + x, LINK_PATH)),
    "link"         : " ".join(map(lambda x:"-l" + x, LINK)),
  })

  if verbose:
    print(cmd)

  return os.system(cmd)


def main():
  global FLAGS, LINK_FLAGS, LINK, DEFINE

  # handle args
  build_mode = "release" if "release" in sys.argv else "debug"
  verbose = "verbose" in sys.argv

  print("initing...")

  # configure build
  config_setup(build_mode)
  
  # make sure there arn't any temp files left over from a previous build
  config_cleanup()

  starttime = time.time()
  
  print("building (" + build_mode + ")...")

  # make sure the previous binary is deleted (windows)
  if os.path.isfile(OUTPUT):
    os.remove(OUTPUT)

  # create directories
  os.makedirs(TEMPSRC_DIR)
  outdir = os.path.dirname(OUTPUT)
  if not os.path.exists(outdir):
    os.makedirs(outdir)

  # run prebuild steps
  config_build()

  # build object files
  for directory in SOURCE:
    for filename in listFiles(directory):
      base, ext = os.path.splitext(os.path.basename(filename))
      if ext == ".c":
        res = compile_object_file(verbose, filename, base + ".o")
        if res != 0:
          sys.exit(res)

  res = compile_executable(verbose)
  if res != 0:
    sys.exit(res)

  if build_mode == "release":
    print("stripping...")
    os.system("strip %s" % OUTPUT)

  print("cleaning up...")
  config_cleanup()

  print("done (%.2fs)" % (time.time() - starttime))

if __name__ == "__main__":
  main()
