# main.pyのテスト
import os
import datetime
from unittest import TestCase
from test.support import captured_stdout
from transcribe import transcribe_file, search_word

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")

class Testtranscribe_file(TestCase):
    def test_OK_001(self):
        """ 正常パターン """
        with captured_stdout() as stdout:
            filepath = transcribe_file(os.path.join(RESOURCES, "public_audio_ja-JP_Narrowband-sample.wav"))
            lines = stdout.getvalue().splitlines()

        d = datetime.datetime.today()
        today = d.strftime("%Y%m%d-%H%M%S")
        path = 'output/SpeechToText_{}.txt'.format(today)
        self.assertEqual(filepath, path)
        self.assertEqual(lines[0], 'Waiting for operation to complete...')
        self.assertEqual(lines[1], 'Transcript: ご住所の変更でございますねご連絡ありがとうございます恐れ入りますがご契約内容を確認いたしますのでお電話を頂いてる方は契約者ご本人様でいらっしゃいますかはいそうです本人ですそれではお電話をいただいておりますお客様のお名前をお願い致します山田太郎です')
        self.assertEqual(lines[2], 'Transcript: 山田太郎様でいらっしゃいますねでは契約者ご本人様確認のため恐れ入りますが山田様の生年月日をお願いいたしますはい生年月日が1937年6月17日です')

class Testsearch_word(TestCase):
    def test_OK_001(self):
        """ 正常パターン """
        with captured_stdout() as stdout:
            filepath = transcribe_file(os.path.join(RESOURCES, "public_audio_ja-JP_Narrowband-sample.wav"))
            search_word(filepath, ['山田', '太郎', '生年月日'])
            lines = stdout.getvalue().splitlines()

        self.assertEqual(lines[0], 'Waiting for operation to complete...')
        self.assertEqual(lines[1], 'Transcript: ご住所の変更でございますねご連絡ありがとうございます恐れ入りますがご契約内容を確認いたしますのでお電話を頂いてる方は契約者ご本人様でいらっしゃいますかはいそうです本人ですそれではお電話をいただいておりますお客様のお名前をお願い致します山田太郎です')
        self.assertEqual(lines[2], 'Transcript: 山田太郎様でいらっしゃいますねでは契約者ご本人様確認のため恐れ入りますが山田様の生年月日をお願いいたしますはい生年月日が1937年6月17日です')
        self.assertEqual(lines[3], '【検索結果】')
        self.assertEqual(lines[4], '見つかった位置先頭 : 117 見つかった位置末尾 : 119 単語 : 山田 単語の前後5文字を含む文字列 : い致します山田太郎です山 ')
        self.assertEqual(lines[5], '見つかった位置先頭 : 123 見つかった位置末尾 : 125 単語 : 山田 単語の前後5文字を含む文字列 : 田太郎です山田太郎様でい ')
        self.assertEqual(lines[6], '見つかった位置先頭 : 159 見つかった位置末尾 : 161 単語 : 山田 単語の前後5文字を含む文字列 : 入りますが山田様の生年月 ')
        self.assertEqual(lines[7], '見つかった位置先頭 : 119 見つかった位置末尾 : 121 単語 : 太郎 単語の前後5文字を含む文字列 : します山田太郎です山田太 ')
        self.assertEqual(lines[8], '見つかった位置先頭 : 125 見つかった位置末尾 : 127 単語 : 太郎 単語の前後5文字を含む文字列 : 郎です山田太郎様でいらっ ')
        self.assertEqual(lines[9], '見つかった位置先頭 : 163 見つかった位置末尾 : 167 単語 : 生年月日 単語の前後5文字を含む文字列 : が山田様の生年月日をお願いい ')
        self.assertEqual(lines[10], '見つかった位置先頭 : 178 見つかった位置末尾 : 182 単語 : 生年月日 単語の前後5文字を含む文字列 : しますはい生年月日が1937 ')
        self.assertEqual(lines[11], '【単語カウント数】')
        self.assertEqual(lines[12], '1 . 山田 = 3')
        self.assertEqual(lines[13], '2 . 太郎 = 2')
        self.assertEqual(lines[14], '3 . 生年月日 = 2')
