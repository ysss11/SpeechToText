# Google社の Cloud Speech-to-text (音声認識API)を利用して 日本語音声データからテキストデータへ変換するプログラム
# 前提
 - OS：Windows
 - Pythonがインストールされている事。
 - 下記にてGCPプロジェクトの作成と認証情報JSONのダウンロード  
    https://zenn.dev/daisukesasaki/articles/fd0cafe486c934
 - 下記にてCloud SDKのダウンロード  
    https://cloud.google.com/sdk/docs/quickstart?hl=ja

# 仮想環境の作成
コマンドプロント
```
py -m venv myenv
```

# 起動
コマンドプロント
```
.\myenv\Scripts\activate
```

# Pythonバージョン
コマンドプロント
```
(myenv) D:\SpeechToText\Project>python --version
Python 3.7.5
```

# requirementsファイルによってパッケージをインストールする
コマンドプロント
```
pip install -r requirements.txt
```

# Credentialsを環境変数に設定する
## jsonファイルの場所を取得
コマンドプロント
```
(myenv) D:\SpeechToText\Project>for %a in (%CD%\\*.json) do (echo %a) | clip
```

## jsonファイルまでのパスを指定してセットする
コマンドプロント
```
(myenv) D:\SpeechToText\Project>set GOOGLE_APPLICATION_CREDENTIALS={DLしたjsonファイルまでのパス}
```
## 環境変数の設定確認
コマンドプロント
```
(myenv) D:\SpeechToText\Project>set
```

# プログラムの実行方法と出力結果
## 実行方法
```
python transcribe.py --path <ローカルにあるwav拡張子の音声ファイル> --search <検索対象単語1> <検索対象単語2> <検索対象単語3>
例：(myenv) D:\SpeechToText\Project>python transcribe.py --path resources/public_audio_ja-JP_Narrowband-sample.wav --search 山田 太郎 生年月日
```

## 引数について
```
(myenv) D:\SpeechToText\Project>python transcribe.py -h
usage: transcribe.py [-h] [--path PATH] [--search [SEARCH [SEARCH ...]]]

optional arguments:
  -h, --help            show this help message and exit
  --path PATH           File or GCS path for audio file to be recognized
  --search [SEARCH [SEARCH ...]]
                        Specify words to be searched
```

## 出力結果
```
Waiting for operation to complete...
Transcript: ご住所の変更でございますねご連絡ありがとうございます恐れ入りますがご契約内容を確認いたしますのでお電話を頂いてる方は契約者ご本人様でいらっしゃいますかはいそうです本人ですそれではお電話をいただいておりますお客様のお
名前をお願い致します山田太郎です
Transcript: 山田太郎様でいらっしゃいますねでは契約者ご本人様確認のため恐れ入りますが山田様の生年月日をお願いいたしますはい生年月日が1937年6月17日です
【検索結果】
見つかった位置先頭 : 117 見つかった位置末尾 : 119 単語 : 山田 単語の前後5文字を含む文字列 : い致します山田太郎です山 
見つかった位置先頭 : 123 見つかった位置末尾 : 125 単語 : 山田 単語の前後5文字を含む文字列 : 田太郎です山田太郎様でい
見つかった位置先頭 : 159 見つかった位置末尾 : 161 単語 : 山田 単語の前後5文字を含む文字列 : 入りますが山田様の生年月
見つかった位置先頭 : 119 見つかった位置末尾 : 121 単語 : 太郎 単語の前後5文字を含む文字列 : します山田太郎です山田太
見つかった位置先頭 : 125 見つかった位置末尾 : 127 単語 : 太郎 単語の前後5文字を含む文字列 : 郎です山田太郎様でいらっ
見つかった位置先頭 : 163 見つかった位置末尾 : 167 単語 : 生年月日 単語の前後5文字を含む文字列 : が山田様の生年月日をお願いい
見つかった位置先頭 : 178 見つかった位置末尾 : 182 単語 : 生年月日 単語の前後5文字を含む文字列 : しますはい生年月日が1937
【単語カウント数】
1 . 山田 = 3
2 . 太郎 = 2
3 . 生年月日 = 2
```

# 単体テスト実施方法と結果
```
(myenv) D:\SpeechToText\Project>python -m unittest tests/test_transcribe.py
..
----------------------------------------------------------------------
Ran 2 tests in 29.132s

OK
```

# 音声ファイル
https://github.com/IBM/speech-to-text-code-pattern/tree/master/public/audio  
