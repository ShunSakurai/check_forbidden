# Check Forbidden
翻訳ファイル(.mqxlz、.mqxliff、.xlfなど)の訳文中に含まれる禁止されている訳語を、CSVファイルを使用して確認するためのツールです。

[英語のREADME](https://github.com/ShunSakurai/check_forbidden/blob/master/README.md)もあります。

![UI](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_ui.png)

## 説明
[memoQ](https://www.memoq.com/)では、用語ベースを使用した、禁止されている原語と訳語のペアの検証と、QA設定を使用した禁止語の検証が行えます。しかし、1つ1つ、設定を選びながら禁止語を追加していくのは、時間のかかる作業です。
このツールを使用すると、CSV形式の用語リストを使用して、memoQのバイリンガルファイルで使用されている禁止語を素早く見つけることができます。正規表現(regex)を使用できます。外部のPythonスクリプトから訳文セグメントに対して関数を呼び出すこともできます。これにより、翻訳の品質を効率的に維持することができます。
(memoQの最近の[アップデート](https://www.memoq.com/memoq-build-june)で、禁止されている訳語のみを、対応する原語に関係なく検証する機能が追加されました。用語ベースにCSVファイルをインポートできるように、QA設定でもCSVファイルをインポートできるようになることを期待しています。)

例えば、次のような状況でこのツールを使用できます。

- スタイルガイドにより、訳文中に「doesn't」や「can't」のような短縮系を使用できない場合
- スタイルガイドにより、半角文字と全角文字の間にスペースを使用できない場合
- JP (日本語):「次の/次に」は使用できるが、「以下の/以下に」は使用できない場合
- JP:「例えば」を漢字にする必要があり、「たとえば」は使用できない場合

必要なものは次のとおりです。

- memoQのバイリンガルファイル(.mqxlzまたは.mqxliff形式)、バージョン 1.2のXLIFFファイル、または翻訳を含むプレーンテキストファイル
- 禁止語の一覧を含むCSVファイルまたはテキストファイル

このツールは、バイリンガルファイル中の訳文セグメントに含まれる禁止語を、1セグメントずつ検索します。コマンドプロンプトに検索結果を表示し、さらに結果をHTMLファイルにエクスポートします。コマンドプロンプトは、ファイルが小さい場合に、検出された用語を簡単に確認するのに適しています。「ビュー」を使って作業している場合は、まとめ結果が便利です。コマンドプロンプト上では印字できない文字もあります。HTMLファイルは、検出結果が多い場合や、フィルタ機能を使用したい場合に便利です。

このプログラムは、Pythonとtkinterを使用して書かれており、[PyInstaller](http://www.pyinstaller.org/)と[Verpatch](https://ddverpatch.codeplex.com/releases)を使用して.exe形式で配布するものです。

アイコンは[アイコン ウィザード](http://freewareplace.web.fc2.com/)を、インストーラーは[Inno Setup](http://www.jrsoftware.org/isdl.php)を使用して作成しました。

## インストール
現在、Windowsにのみ対応しています。プログラムファイルは[Releases(リリース)](https://github.com/ShunSakurai/check_forbidden/releases)で入手できます。インストーラーをダウンロードして実行するだけで、インストールやアップデートを行えます。32ビットと64ビットの両方の環境をサポートしています。

Python環境をインストールしている場合、`python(3) check_forbidden.py`または`import check_forbidden`でソースコードをMacなど任意のOSで実行できます。

## ビルド
Pythonコードを.exeファイルに変換し、インストーラーを作成するには、次の手順に従います。

### 要件
- [Python 3](https://www.python.org/downloads/)
- [PyInstaller](http://www.pyinstaller.org/)
- [Verpatch](https://ddverpatch.codeplex.com/releases)、パスを通してください
- [Inno Setup](http://www.jrsoftware.org/isdl.php)

### 手順
- Windows環境で、`py -B setup.py`を実行します。`-B`はオプションです
- py = python3となるように、エイリアスを設定する必要があるかもしれません

## 使用方法

### 概要
- memoQやその他のCATツール(Transifexをサポート)からバイリンガルファイルをエクスポートします
- Check Forbidden.exeまたはそのエイリアスをダブルクリックしてプログラムを開きます
- 「Bilingual」(バイリンガル)をクリックするか、ファイルへのパスを入力するか貼り付けることで、翻訳ファイルを選択します
- 禁止語の一覧を含むCSVファイル、テキストファイル、またはPythonスクリプトを選択します
- 必要に応じて、エクスポートする結果ファイルのパスとファイル名を指定します既定のパスは、1つ目のバイリンガルファイルのパス + "checked_result.html"です
- 「Run!」(実行)をクリックします
- 結果はコマンドプロンプトに表示されます。一致する結果が見つかった場合は、HTMLファイルにもエクスポートされます
- プログラムを閉じるには、「X」(閉じる)ボタンをクリックします

![結果](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_result.png)

### オプション
オプション画面を表示するには、歯車⚙アイコンをクリックします。画面を隠すには、三角▲アイコンをクリックします。

最後に使用したオプションを保存するかどうかを指定できます。"C:\Users\<ユーザー名>\AppData\Roaming\Check Forbidden"に"cf_options.p"というファイルが作成されます(Windowsの場合)。

![オプション](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_options.png)

### 翻訳ファイルの種類
次のファイル形式がサポートされています。

- .mqxliff
- .mqxlz
- .xlf ([XLIFFバージョン1.2](http://docs.oasis-open.org/xliff/v1.2/os/xliff-core.html))
- .txt
- .srt
- .po

.mqxlzファイルは、document.mqxliffファイル、スケルトン(書式情報)、バージョン情報(場合により)を圧縮したファイルです。このプログラムでは、document.mqxliffをフォルダーに展開し、処理の終了後に削除しています。

テキストファイルはUTF-8でエンコードしてください。

### CSVファイルの形式
用語リストは、次の仕様に従っている必要があります。

- ファイル名にコンマは使用できません
- 区切り文字: コンマ
- エンコーディング:UTF-8
- すべての用語が正規表現パターンとみなされ、大文字と小文字は区別されます
- 正規表現で使用される特殊文字(`(`, `)`, `[`, `]`, `.`, `\*`, `?`, `!`など)は、すべて**バックスラッシュでエスケープ**する必要があります
- **1列目**の用語が禁止語とみなされます
- 他の列を使用して、インデックス番号、原語、正しい訳語などの詳細情報を指定することができます
- CSVファイルにコンマが含まれている場合、区切り文字として解釈されてしまう可能性があります
- CSVファイルにアクセント記号の付いた文字が含まれている場合、それらの文字は検証のために正常に使用されますが、コマンドプロンプトには正常に印字されません
- (txtファイル)コンマと二重引用符は、`""`や`"コンマを含む, 文字列"`のように、エスケープする必要があります

![CSV](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_csv.png)

### 正規表現
- このプログラムでは、[re](https://docs.python.org/3/library/re.html)モジュールの構文を使用します
- memoQのタグの正規表現(`\tag`)は現在サポートされていません
- (例)`[0-9A-Za-z]\s[^!-~]`と`[^!-~]\s[0-9A-Za-z]`というパターンを使用すると、ASCIIの半角文字と、ASCIIの半角文字以外のすべての文字(全角文字を含む)との間にあるスペースを調べることができます
- (例) `\\)\S`というパターンを使用すると、隣にスペースのない括弧を調べることができます

### 外部関数の呼び出し
関数のチェックボックスを選択すると、外部のPythonスクリプトから訳文セグメントに対して関数を呼び出すことができます。

- 外部のPythonスクリプト内の「Function」という名前の関数を呼び出します。この関数は、セグメントID(整数)、原文セグメント(文字列)、訳文セグメント(文字列)、マッチ率(整数)、ロック状態(ブーリアン)、訳文が原文と同じ(ブーリアン)、の6つを引数として取るものです
- この関数は、各セグメントに対して2次元のリストまたはNoneを返すようにしてください。内側のリスト1つは、コマンドプロンプト上およびHTMLテーブル中の結果表示において1行で表示されます

コード例:
calculate_width.py
```python
import re
pattern_half_width = re.compile(r'[ -~]')

def function(int_seg_id, str_source, str_target, int_percent, bool_locked, bool_same):
    length_half = len(re.findall(pattern_half_width, str_target))
    length_full = len(str_target) - length_half
    length_total = length_half + length_full * 2
    return [[int_seg_id, str_target, length_full, length_half, length_total]]
```

### キーボードショートカット
Altキーと一緒に下線の付いた文字を押すことで、ボタンを選択することができます。下線の付いていないその他のボタンについては、次のキーで呼び出すことができます。

- Run!:Alt + Return (Alt + Enter)
- オプションの表示/非表示:Alt + o
- 3つのフィールドのクリア:Alt + c
- フォルダーを開く: ショートカットキーなし

UIの項目は「Tab」キーで移動し、フォーカスされた項目を「スペースバー」で呼び出すことができます。

### ヒント
- バイリンガルファイルが「ビュー」にまとまっている場合、チェック時間が短くて済みます
- バイリンガルファイルが共有ドライブ上ではなくローカルPC上にある場合、チェック時間が短くて済みます
- 入力欄にパスを入力するか貼り付けたあとにファイルを選択するボタンを押すと、欄内のフォルダーを初期パスとして参照します
- 最後に使用した用語ファイル名を保存しておくと、そのファイルパスが用語ファイルを参照するデフォルトの場所になります。
- 入力欄にパスが記入されている場合、右の矢印を押してそのフォルダーを開くことができます
- 結果はファイルごとと、ファイル全体についての「Summary」(まとめ)として表示されます
- PyInstallerにより、`C:\Users\%username%\AppData\Local\Temp`フォルダーに"_MEI000000"といった名前のサイズの大きいフォルダーが作成される場合があります。それらは削除して問題ありません

### XProofとの統合
Windows上に[XProof](https://github.com/AlissaSabre/XProof)をインストールしている場合、Check ForbiddenからXProofCmdを、「Bilingual」フィールドで選択されたバイリンガルファイルに対して実行することができます。このフィールドでバイリンガルファイルが選択されたいない場合は、フィールド内にパスがあればそれをクリップボードにコピーした状態で、XProofが起動します。XProofは、xliffファイル(.mqxlzと.mqxliff)をサポートしています。.txt/.srt/.poはサポートされていません。

## トラブルシューティング

### コマンドプロンプトが文字化けする
Windowsのコマンドプロンプトでマルチバイト文字が文字化けしているように見える場合があります。タイトルバーを右クリックし、「プロパティ/フォント」を選択し、フォントサイズを大きくするか別のフォントを選択すると、この問題が解決します。[Alt + スペース]、[P]を順番に押すと、プロパティを素早く開くことができます。

![文字化け](https://raw.github.com/wiki/ShunSakurai/check_forbidden/check_forbidden_garbled.png)

### \_extractフォルダーが削除されない
.mqxlzファイルを開く際に、同じフォルダーに\_extractフォルダーが作成されます。エラーが発生すると、プログラムによってそのフォルダーが削除されない場合があります。そのような場合、お手数ですがご自身で削除をお願いします。

### 誤検出
誤検出を防ぐための工夫を次に示します。

- `display`との一致を防ぐには、CSVに` play`または`\splay`(半角スペース + play)を追加します
- 例えば「等」(など)が「等級」と一致しないように、短すぎる用語を使用しないようにします
- 1つの用語に対して多くの誤検出が発生する場合、CSVファイルを分割することも検討してください

### 検索に時間がかかりすぎる場合の対処法
- 複数のドキュメント(ファイル)に対してビューの作成を検討します

## 今後追加予定の機能
### 開発中の機能
- HTMLファイルで空白文字を表示
- 登録されているmemoQタグのみをサポート
- プログラム画面の大きさの自由変更
- 外部のPython関数でできることを増やす

### 追加予定のない機能
- ドラッグでファイルを追加。tkinterでドラッグアンドドロップ機能を使用するのは難しいため
- 誤検出をマークして無視。技術的に難しいため
- 禁止語の列を指定するための設定を追加
- 複数のバイリンガルファイルを別のフォルダーから選択する機能を追加。あまり重要でないため

すぐに使用したい機能がある場合は、[Github Issues](https://github.com/ShunSakurai/check_forbidden/issues)または[Asana](https://app.asana.com/0/264039980253157/list)からご連絡ください。

## 履歴
履歴の詳細は、[Releases(リリース)](https://github.com/ShunSakurai/check_forbidden/releases)でご覧ください。

文頭の「*」は、バグ修正を示します。

## 貢献
これは個人的なプロジェクトです。[Github Issues](https://github.com/ShunSakurai/check_forbidden/issues)または[Asana](https://app.asana.com/0/264039980253157/list)から、どんなご意見や貢献でもいただけると幸いです。

## 使用権限
### 使用方法
このツールは無料でお使いいただけます。
© 2016-2019 Shun Sakurai

### MITライセンス
このコードはMITライセンスによって保護されています。詳細は、[license.md](https://github.com/ShunSakurai/check_forbidden/blob/master/license.md)をご覧ください。
