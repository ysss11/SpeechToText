import argparse
import codecs
import datetime
import io
import re

from janome.tokenizer import Tokenizer

## テキストに変換し出力したファイルから検索対象で検索
#
# @param speech_file str 音声ファイルのパス
#
# @return str テキストに変換し出力したファイルパス
#
def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech

    client = speech.SpeechClient()

    # ファイルを開き取得する
    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    # google.api_core.exceptions.InvalidArgument: 400 sample_rate_hertz (16000) in RecognitionConfig must either be omitted or match the value in the WAV header ( 8000).
    # が出力されたため sample_rate_hertz=16000 を省略
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=16000,
        language_code="ja-JP",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    d = datetime.datetime.today()
    today = d.strftime("%Y%m%d-%H%M%S")
    filepath = 'output/SpeechToText_{}.txt'.format(today)
    textfile = codecs.open(filepath, 'a', 'utf-8')

    #speechs = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        #print("Confidence: {}".format(result.alternatives[0].confidence))
        #speechs.append(result.alternatives[0].transcript)
        textfile.write(u'{}\n'.format(result.alternatives[0].transcript))
    # [END speech_python_migration_async_response]
    textfile.close()

    return filepath
# [END speech_transcribe_async]


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="ja-JP",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))


## テキストに変換し出力したファイルから検索対象で検索
#
# @param filepath str テキストに変換し出力したファイルパス
# @param searchs list 検索対象
#
def search_word(filepath, searchs):
    """ テキストに変換し出力したファイルから検索対象で検索 """
    tokenizer = Tokenizer()
    text = ''
    test_data = codecs.open(filepath, 'r', 'utf-8')

    # ファイルの内容を文字列に変換
    for line in test_data:
        text += line.strip()
    test_data.close()

    tokens = tokenizer.tokenize(text)
    word_dic = {}
    word_list = []
    re_search = ''

    # 検索単語リスト
    for arg in searchs:
        re_search += arg + '|'
        m_iter = re.finditer(arg, text)
        tmp_list = []
        for m in m_iter:
            tmp_list.append({"見つかった位置先頭": m.start(),
                              "見つかった位置末尾": m.end(),
                              "単語": m.group(),
                              "単語の前後5文字を含む文字列": text[m.start()-5:m.end()+5]})
        # 単語毎にソートを操作し、全体に追加する
        word_list.append(sorted(tmp_list, key=lambda x: x["見つかった位置先頭"], reverse=False))

    for token in tokens:
        word = token.surface
        check = re.match(re_search.rstrip('|'), word)

        if check:
            if word in word_dic:
                word_dic[word] += 1
            else:
                word_dic[word] = 1

    print("【検索結果】")
    for words in word_list:
        for word in words:
            for key, value in word.items():
                print(key, ':', value , '', end='')
            print()

    print("【単語カウント数】")
    # カウントの多い順に並び替える
    sc = sorted(word_dic.items(), key=lambda x: x[1], reverse=True)
    for i, t in enumerate(sc):
        if i >= 100: break
        key, cnt = t
        print((i + 1), ".", key, "=", cnt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--path", help="File or GCS path for audio file to be recognized")
    parser.add_argument('--search', nargs='*', help="Specify words to be searched")
    args = parser.parse_args()

    if args.path.startswith("gs://"):
        transcribe_gcs(args.path)
    else:
        # テキストに変換しテキストを出力したファイルパスを返却
        filepath = transcribe_file(args.path)
        # --search の後に検索する単語を記載する。複数も可能
        search_word(filepath, args.search)
