import json

def loadLangs():
  f = open('Langs.json', 'r')
  res = json.loads(f.read())
  f.close()
  return res

def chooseLangs(name):
  # The name must be exactly the same as shown on the Google webpage
  langs = loadLangs()
  return langs[name]