class Timestamp:
    # Timestamp object consists of a start_time and a end_time
    # Each is a string like "hh:mm:ss,sss" (the same as the timestamp in srt files, and hour must started at 00)

    def __init__(self, start_time, end_time):
        import re
        time_re = re.compile(r"\d{2,}:\d{2}:\d{2},\d{3}")
        if time_re.fullmatch(start_time)==None or time_re.fullmatch(end_time)==None:
            raise AttributeError('The start time and end time should match the regex r"\d{2,}:\d{2}:\d{2},\d{3}"')

        if not (0<=int(start_time[-9:-7])<=60 and 0<=int(end_time[-9:-7])<=60):
            raise AttributeError('The minutes of both start_time and end_time should be between 0 and 60')

        if not (0<=int(start_time[-6:-4])<=60 and 0<=int(end_time[-6:-4])<=60):
            raise AttributeError('The seconds of both start_time and end_time should be between 0 and 60')

        self.__start_time = start_time
        self.__end_time = end_time

    def change(self, start_time = None, end_time = None):
        # The default start_time and end_time is the current start_time and end_time
        if start_time == None:
            start_time = self.startTime()
        if end_time == None:
            end_time = self.endTime()

        import re
        time_re = re.compile(r"\d{2,}:\d{2}:\d{2},\d{3}")
        if time_re.fullmatch(start_time)==None or time_re.fullmatch(end_time)==None:
            raise AttributeError('The start time and end time should match the regex r"\d{2,}:\d{2}:\d{2},\d{3}"')

        if not (0<=int(start_time[-9:-7])<=60 and 0<=int(end_time[-9:-7])<=60):
            raise AttributeError('The minutes of both start_time and end_time should be between 0 and 60')

        if not (0<=int(start_time[-6:-4])<=60 and 0<=int(end_time[-6:-4])<=60):
            raise AttributeError('The seconds of both start_time and end_time should be between 0 and 60')

        self.__start_time = start_time
        self.__end_time = end_time

    def startTime(self):
        return self.__start_time

    def endTime(self):
        return self.__end_time

    def __str__(self):
        # srt-like timestamp
        return self.__start_time + ' --> ' + self.__end_time

class Sentence:

    def __init__(self, timestamp, content, speaker_tag = 0):
        if type(timestamp) != Timestamp or type(content) != str or type(speaker_tag) != int:
            raise AttributeError('Type of timestamp must be Timestamp. Type of content must be str. Type of speaker_tag must be int')

        self.__timestamp = timestamp
        self.__content = content
        self.__speaker_tag = speaker_tag

    def timestamp(self):
        return self.__timestamp

    def content(self):
        return self.__content

    def speakerTag(self):
        return self.__speaker_tag

    def changeTime(self, start_time = None, end_time = None):
        self.__timestamp.change(start_time = start_time, end_time = end_time)

    def changeContent(self, content = None, speaker_tag = None):
        if content == None:
            content = self.__content
        if speaker_tag == None:
            speaker_tag = self.__speaker_tag

        if type(content) != str or type(speaker_tag) != int:
            raise AttributeError('Type of content must be str. Type of speaker_tag must be int')

        self.__content = content
        self.__speaker_tag = speaker_tag

class Transcription:

    def __init__(self, sentences = [], speakers = {}):
        self.__sentences = sentences
        self.__speakers = speakers

    def sentences(self):
        return self.__sentences

    def addSpeaker(self, speaker_tag, name):
        if type(speaker_tag) != int or type(name) != str:
            raise AttributeError('Type of speaker_tag must be int, and type of name must be str')
        self.__speakers[speaker_tag] = name

    def appendSentence(self, sentence):
        if type(sentence) != Sentence:
            raise AttributeError('Type of sentence must Be Sentence')
        self.__sentences += [sentence]

    def addSentence(self, sentence, index):
        if type(sentence) != Sentence:
            raise AttributeError('Type of sentence must Be Sentence')
        self.__sentences.insert(index, sentence)

    def deleteSentence(self, index):
        del self.__sentences[index]

    def sentenceAt(self, index):
        return self.__sentences[index]

    def displaySentenceAt(self, index):
        sentence = self.sentenceAt(index)
        res = str(index+1) + '\n'

        timestamp = sentence.timestamp()
        res += str(timestamp) + '\n'

        # The speaker is the speaker tag if it is not existed in the dictionary
        speaker = sentence.speakerTag()
        if speaker in self.__speakers:
            speaker = self.__speakers[speaker]
        res += '[' + str(speaker) + ']: '

        content = sentence.content()
        res += content

        return res

    def storeRaw(self, file_name, dir):
        # The extension of file_name must be explicitly declared (.json)
        store = {'speakers':self.__speakers, 'sentences':[]}
        for sentence in self.__sentences:
            dic = {'timestamp': {'start_time':sentence.timestamp().startTime(), 'end_time':sentence.timestamp().endTime()},
                   'content':sentence.content(),
                   'speaker_tag':sentence.speakerTag()
                   }
            store['sentences'] += [dic]

        import json
        import os
        json_dic = json.dumps(store)
        file_dir = os.path.join(dir, file_name)
        f = open(file_dir, "w")
        f.write(json_dic)
        f.close()

    def recoverRaw(file_dir):
        import json
        f = open(file_dir, 'r')
        dic = json.loads(f.read())
        sentences = []
        for sentence in dic['sentences']:
            time = Timestamp(sentence['timestamp']['start_time'], sentence['timestamp']['end_time'])
            temp = Sentence(time, sentence['content'], sentence['speaker_tag'])
            sentences += [temp]

        speakers = {}
        for speaker_tag in dic['speakers']:
            # the json will automatically convert keys in a dict from int to string
            speakers[int(speaker_tag)] = dic['speakers'][speaker_tag]

        return Transcription(sentences = sentences, speakers = speakers)

    def srt(self, file_name, dir):
        # The extension of file_name must be explicitly declared (.srt/.txt)
        import os

        abs_dir = os.path.join(dir, file_name)
        f = open(abs_dir, "w")
        for i in range(len(self.__sentences)):
            f.write(self.displaySentenceAt(i))
            f.write('\n\n')
        f.close()