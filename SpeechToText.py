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
def parseTranscription(response, file_name, dir):
  # parse the result to Transcription class

  res = Transcription()

  for i in range(len(response.results)):
    content = response.results[i].alternatives[0]
    start_time = sentence.words[0].start_time
    end_time = sentence.words[-1].end_time
    res[str(sentence.words[0].speaker_tag) + ' ' + str(start_time.seconds + start_time.nanos * 1e-9) + "-" + str(end_time.seconds + start_time.nanos * 1e-9)] = sentence.transcript

  return res
