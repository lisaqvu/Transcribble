from Transcription import *
# Using Google Api to get the transcription of the audio given its uri
def speechToText(audio_uri, lang = 'en-US', speaker_num = 1):
  from google.cloud import speech_v1p1beta1 as speech

  # Instantiates a client
  client = speech.SpeechClient()

  # The name of the audio file to transcribe
  audio = speech.types.RecognitionAudio(uri=audio_uri)


  config = speech.types.RecognitionConfig(
  language_code = lang,
  enable_speaker_diarization = True,
  diarization_speaker_count=speaker_num,
  enable_word_time_offsets=True,
  enable_automatic_punctuation=True
  )

  # Get the transcription
  operation = client.long_running_recognize(config, audio)
  response = operation.result(timeout=90)

  return response

# Parse the transcription to a dictionary and store it to json
def parseSecond(sec, nano):
  minute = sec // 60
  sec = sec % 60
  hour = minute // 60
  minute = minute % 60
  mili = nano * 1e-6

  if hour < 10:
    hour = '0' + str(hour)
  else:
    hour = str(hour)

  if minute < 10:
    minute = '0' + str(minute)
  else:
    minute = str(minute)

  if sec < 10:
    sec = '0' + str(sec)
  else:
    sec = str(sec)

  if mili == 0:
    mili = '000'
  else:
    mili = str(int(mili))

  return hour + ':' + minute + ':' + sec + ',' + mili

def parseTranscription(response):
  trans = Transcription()

  for i in range(len(response.results)):
    result = response.results[i].alternatives[0]
    speaker = result.words[0].speaker_tag
    content = ''
    start_word = 0
    end_word = 0

    while end_word < len(result.words):
      while end_word < len(result.words) and result.words[end_word].speaker_tag == speaker:
        content += result.words[end_word].word + " "
        end_word += 1

      if end_word < len(result.words):
        end_word -= 1
        start_time = parseSecond(result.words[start_word].start_time.seconds, result.words[start_word].start_time.nanos)
        end_time = parseSecond(result.words[end_word].start_time.seconds, result.words[end_word].start_time.nanos)
        sentence = Sentence(Timestamp(start_time, end_time), content, speaker_tag = speaker)
        trans.appendSentence(sentence)
        start_word = end_word + 1
        end_word = end_word + 1
        content = ''
        speaker = result.words[start_word].speaker_tag
      elif end_word == len(result.words):
        end_word -= 1
        start_time = parseSecond(result.words[start_word].start_time.seconds, result.words[start_word].start_time.nanos)
        end_time = parseSecond(result.words[end_word].start_time.seconds, result.words[end_word].start_time.nanos)
        sentence = Sentence(Timestamp(start_time, end_time), content, speaker_tag = speaker)
        trans.appendSentence(sentence)
        end_word = end_word + 1

  return trans
