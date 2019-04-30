from Transcription import *

import soundfile
import librosa
import librosa.display
import librosa.output

from moviepy.editor import *

import os.path as path
import os

# from pydub import AudioSegment

def parseSrt(file):

    f = open(file, 'r')

    trans = Transcription()
    timestamp = None
    line_num = 0

    for line in f:
        line_num += 1

        if line == '\n':
            line_num = 0
        elif line_num == 2:
            line = line[:-1]
            start_time = line[:12]
            end_time = line[-12:]
            timestamp = Timestamp(start_time, end_time)
        elif line_num == 3:
            line = line[:-1]
            trans.appendSentence(Sentence(timestamp, line))

    return trans

def parseAudio(file, start_time = -1, end_time = -1):
    if not path.exists(r'./temp_files'):
        os.mkdir(r'./temp_files')
    temp_file = path.join(r'./temp_files', path.splitext(path.basename(file))[0] + '.wav')

    # audio files must be mono or stereo (5.1 is not supported)
    # .flac is not supported
    #sound = AudioSegment.from_file(file, path.splitext(file)[1][1:])
    #sound = sound.set_sample_width(2)
    #sound.export(temp_file, format = 'wav')

    y, sr = librosa.load(file, mono = True, sr = None)

    if start_time == -1:
        start_time = 0
    else:
        if not 0<=start_time<=len(y)/sr:
            raise TypeError('Illegal start_time')
        start_time = int(start_time*sr)
    if end_time == -1:
        end_time = len(y) + 1
    else:
        if not 0<=end_time<=len(y)/sr:
            raise TypeError('Illegal end_time')
        end_time = int(end_time*sr) + 1

    y = y[start_time:end_time]

    librosa.output.write_wav(temp_file, y, sr)

    data, samplerate = soundfile.read(temp_file)
    soundfile.write(temp_file, data, samplerate, subtype='PCM_16')

    return librosa.display.waveplot(y, sr = sr)

def parseVideo(file, start_time = -1, end_time = -1):
    if not path.exists(r'./temp_files'):
        os.mkdir(r'./temp_files')
    temp_file = path.join(r'./temp_files', path.splitext(path.basename(file))[0] + '.wav')

    audioclip = AudioFileClip(file)
    audioclip.write_audiofile(temp_file)
    parseAudio(temp_file, start_time = -1, end_time = -1)
