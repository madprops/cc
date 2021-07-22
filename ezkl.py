min_accuracy = 0.6
max_paths = 300

from sys import argv
from os import getenv
from pathlib import Path
from difflib import SequenceMatcher

def filterpath(path):
  pths = [path]

  for p in paths:
    if p == path:
      continue
    pths.append(p)

  return pths

def forgetpath(path):
  pths = []

  for p in paths:
    if p == path or p.startswith(path + "/"):
      continue
    pths.append(p)

  return pths

def findpath(filter):
  matches = []

  def add_match(path, acc, match):
    for m in matches:
      if m["path"] == path:
        return
    match = {"path":path, "acc":acc, "match":match}
    matches.append(match)

  checkslash = "/" in filter
  lowfilter = filter.lower()

  for path in paths:
    lowpath = path.lower()
    if checkslash and lowfilter in lowpath:
      add_match(path, 1, filter)
    split = path.split("/")
    parts = []
    for part in split:
      parts.append(part)
      lowpart = part.lower()
      acc = similar(part, filter)
      if acc >= min_accuracy or lowfilter in lowpart:
        add_match("/".join(parts), acc, part)

  if len(matches) > 0:
    matches.sort(key=lambda x: -x["acc"])

    for m in matches:
      if m["path"] != pwd:
        return m["path"]

  return ""

def checkhome(p):
  for s in [p, p.capitalize(), p.lower(), p.upper()]:
    dir = Path.home() / Path(s)
    if dir.is_dir():
      return str(dir)
  return ""

def updatefile(paths):
  lines = paths[0:max_paths]
  file = open(filepath, "w")
  file.write("\n".join(lines).strip())
  file.close()

def similar(a, b):
  return SequenceMatcher(None, a, b).ratio()

def cleanpath(path):
  return path.rstrip("/")

def showinfo():
  info = f"""\nezkl is installed and ready to use
---------------------------------------------
Jump around directories. For instance 'z music'
Directories get remembered by using cd normally
Paths are saved in ezkl/paths.txt
If you don't need this anymore remove, ezkl from ~/.bashrc
Remember to restart Bash for changes to apply
---------------------------------------------
Minimum accuracy is set to {min_accuracy}
paths.txt has {len(paths)}/{max_paths} paths saved\n"""
  print(info)

def getpaths():
  global paths
  global filepath
  thispath = Path(__file__).parent.resolve()
  filepath = Path(thispath) / Path("paths.txt")
  filepath.touch(exist_ok=True)
  file = open(filepath, "r")
  paths = file.read().split("\n")
  paths = list(map(str.strip, paths))
  paths = list(filter(None, paths))
  file.close()

if __name__ == "__main__":
  args = [x for x in argv[1:] if not x.startswith("-")]

  if len(args) >= 1:
    mode = args[0]
    if mode == "info":
      getpaths()
      showinfo()
      exit(0)

  if len(args) < 2:
    exit(0)

  getpaths()
  keyword = args[1]
  pwd = cleanpath(getenv("PWD"))

  if mode == "remember":
    updatefile(filterpath(pwd))
  elif mode == "forget":
    updatefile(forgetpath(keyword))
  elif mode == "jump":
    if keyword.startswith("/"):
      path = cleanpath(keyword)
    else:
      path = findpath(keyword)
    if len(path) == 0:
      path = checkhome(keyword)
    if len(path) > 0:
      updatefile(filterpath(path))
      print(path)