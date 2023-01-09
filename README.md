# ジェネリック恋チョコ
「恋と選挙とチョコレート」みたいな言葉を自動生成する

# `convertdict.py`の使い方
Sudachi用の辞書データSudachiDictを利用している。

http://sudachi.s3-website-ap-northeast-1.amazonaws.com/sudachidict-raw/

ここから`20221021`の`small_lex.zip`, `core_lex.zip`, `notcore_lex.zip`をダウンロードしてきて展開し、`.csv`ファイルを`sudachidict`ディレクトリ以下に入れる。

`sudachipy`をインストールしたpythonで`convertdict.py`を実行する。