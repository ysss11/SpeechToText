# 説明資料
このプログラムは Google社の Cloud Speech-to-text (音声認識API)を利用して
日本語音声データからテキストデータへ変換するプログラムである。

このプログラムでは日本語音声データは **一般的である音声データのwav拡張子** で用意し、ローカルのファイルパスを指定して上げることにより音声データからテキストデータへ変換する。  
※このプログラムは音声データが用意しやすいwav拡張子の音声データを加工することをベースとして作成している  
※プログラムとしてはGCSから取得するサンプルもあるが動作保証はしていない  

このプログラムで利用する音声データは1分未満ではwav、1分以上であればGCSを利用する事をおススメする。  
※GCSから利用する場合は拡張子がflacとなる。

# GCPプロジェクトの作成と認証情報JSONのダウンロード  

https://zenn.dev/daisukesasaki/articles/fd0cafe486c934

# Cloud SDKのダウンロード  

https://cloud.google.com/sdk/docs/quickstart?hl=ja

# 環境作成準備参考資料
https://cloud.google.com/python/docs/setup?hl=ja#windows  
https://cloud.google.com/speech-to-text/docs/libraries?hl=ja#client-libraries-install-python  
https://zenn.dev/daisukesasaki/articles/fd0cafe486c934  
https://cloud.google.com/sdk/docs/quickstart?hl=ja  
https://cloud.google.com/speech-to-text/docs/libraries?hl=ja#windows  
