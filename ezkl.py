# Imports
from sys import argv
from os import getenv
from pathlib import Path
from difflib import SequenceMatcher

# Settings
min_accuracy: float = 0.7
max_paths: int = 250

# Globals
mode: str
keyword: str
paths: "list[str]"
filepath: Path
pwd: str

# Main function
def main() -> None:
  getargs()
  getpaths()

  if mode == "info":
    showinfo()

  elif mode == "remember":
    updatefile(filterpath(pwd))

  elif mode == "forget":
    updatefile(forgetpath(keyword))
  
  elif mode == "paths":
    showpaths(keyword)

  elif mode == "jump":
    if keyword.startswith("/"):
      path = cleanpath(keyword)
    else:
      path = findpath(keyword)
    if len(path) == 0:
      path = guessdir(keyword)
    if len(path) > 0:
      updatefile(filterpath(path))
      print(path)

# Get arguments. Might exit here
def getargs() -> None:
  global mode
  global keyword

  args = argv[1:]
  mode = args[0] if len(args) > 0 else ""
  keyword = args[1] if len(args) > 1 else ""

  if mode not in ["remember", "forget", "jump", "info", "paths"]:
    exit(0)

  if mode in ["forget", "jump"] and keyword == "":
    exit(0)

# Read the paths file plus other paths
def getpaths() -> None:
  global paths
  global filepath
  global pwd
  thispath = Path(__file__).parent.resolve()
  filepath = Path(thispath) / Path("paths.txt")
  filepath.touch(exist_ok=True)
  file = open(filepath, "r")
  paths = file.read().split("\n")
  paths = list(map(str.strip, paths))
  paths = list(filter(None, paths))
  file.close()
  pwd = cleanpath(str(getenv("PWD")))

# Put path in first line
def filterpath(path: str) -> "list[str]":
  pths = [path]

  for p in paths:
    if p == path:
      continue
    pths.append(p)

  return pths

# Remove path and subdirs
def forgetpath(path: str) -> "list[str]":
  pths: list[str] = []

  for p in paths:
    if p == path or p.startswith(path + "/"):
      continue
    pths.append(p)

  return pths

class Match:
  def __init__(self, path: str, acc: float):
    self.path = path
    self.acc = acc
  
  def level(self) -> int:
    return len(self.path.split("/"))

# Try to find a matching path
def findpath(filter: str) -> str:
  matches: list[Match] = []

  def add_match(path: str, acc: float):
    match: Match = Match(path, acc)
    matches.append(match)

  checkslash = "/" in filter
  lowfilter = filter.lower()

  for path in paths:
    lowpath = path.lower()
    if checkslash and lowfilter in lowpath:
      add_match(path, 1)
    split = path.split("/")
    parts: list[str] = []
    for part in split:
      parts.append(part)
      lowpart = part.lower()
      acc = similar(lowpart, lowfilter)
      if acc >= min_accuracy or lowfilter in lowpart:
        add_match("/".join(parts), acc)

  if len(matches) > 0:
    matches.sort(key=lambda x: (-x.acc, x.level()))
    return matches[0].path

  return ""

# Check if path or similar exists in directory
# It checks current directory and then home
def guessdir(p: str) -> str:
  pths = [p, p.capitalize(), p.lower(), p.upper(), f".{p}"]

  for s in pths:
    dir = Path(pwd) / Path(s)
    if dir.is_dir():
      return str(dir)

  if not athome():
    for s in pths:
      dir = Path.home() / Path(s)
      if dir.is_dir():
        return str(dir)

  return ""

# Write paths to file
def updatefile(paths: "list[str]") -> None:
  lines: list[str] = paths[0:max_paths]
  file = open(filepath, "w")
  file.write("\n".join(lines).strip())
  file.close()

# Check string similarity from 0 to 1
def similar(a: str, b: str) -> float:
  return SequenceMatcher(None, a, b).ratio()

# Remove unecessary characters
def cleanpath(path: str) -> str:
  return path.rstrip("/")

# Check if pwd is set to home
def athome() -> bool:
  return Path(pwd) == Path(Path.home())

# Show some information
def showinfo() -> None:
  info = f"""\nezkl is installed and ready to use
---------------------------------------------
Jump around directories. For instance 'z music'
Directories get remembered by using cd normally
Paths are saved in ezkl/paths.txt
Use 'z --paths' to print saved paths
---------------------------------------------
Minimum accuracy is set to {min_accuracy}
paths.txt has {len(paths)}/{max_paths} paths saved\n"""
  print(info)

# Print all paths
def showpaths(filter: str) -> None:
  hasfilter = filter != ""
  lowfilter = filter.lower()

  for path in paths:
    if hasfilter:
      if lowfilter not in path.lower():
        continue
    print(path)

# Program starts here
if __name__ == "__main__": main()