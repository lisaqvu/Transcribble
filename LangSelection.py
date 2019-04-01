import json

def loadLangs(mode):
  f = None
  if mode == 'transcribe':
    f = open('TranscriptionLangs.json', 'r')
  elif mode == 'translate':
    f = open('TranslationLangs.json', 'r')
  res = json.loads(f.read())
  f.close()
  return res

def chooseLang(name, mode):
  # The name must be exactly the same as shown on the Google webpage
  if mode != 'transcribe' and mode != 'translate':
    raise Exception('mode must be \'transcribe\' or \'translate\'')
  langs = loadLangs(mode)
  return langs[name]
