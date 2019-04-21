from Transcription import *
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
    import librosa
    import librosa.display
    y, sr = librosa.load(file)
    y = librosa.to_mono(y)

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

    return librosa.display.waveplot(y, sr = sr)

def parseVideo(file, start_time = -1, end_time = -1):
    