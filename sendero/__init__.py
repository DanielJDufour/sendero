def find_paths(obj, prev="", delim="."):
  paths = set()
  if isinstance(obj, list):
    for item in obj:
      paths |= find_paths(item, prev + delim if prev else "")
  elif isinstance(obj, dict):
    for key, value in obj.items():
      subpath = prev + delim + key if prev else key
      if isinstance(value, list):
        for item in value:
          paths |= find_paths(item, subpath)
      elif isinstance(value, dict):
        paths |= find_paths(value, subpath)
      else:
        paths.add(subpath)
  return paths

def list_paths(obj, prev="", delim="."):
  return sorted(list(find_paths(obj, prev=prev, delim=delim)))

