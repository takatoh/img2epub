# img2epub

Generate EPUB book from image file set.

ひとそろいの画像ファイル (PNG) から EPUB （電子書籍）を作ります。

## Install

    $ pip install img2epub

## Usage

いちばん簡単な使い方: `img2epub build` コマンドに画像ファイルの入っているディレクトリ名を指定します。

    $ img2epub build source_dir

画像ファイルは名前でソートされるので、連番になっている必要はありません。
ただし、例えば Windows のエクスプローラーで表示される順とは一致しないことがあるので、注意してください。

### Options

`img2epub build` コマンドには次のオプションを指定できます。

- --title : 電子書籍のタイトルを指定します
- --output : 電子書籍のファイル名をしていします
- --keep : 処理中に作られるテンポラリディレクトリを削除せずに残します

`--title` オプションを指定しない場合、電子書籍のタイトルにはソースディレクトリの名前が使われます。
`--output` オプションを指定しない場合、ファイル名には `--title` オプションの値またはソースディレクトリの名前が使われます。

### img2epub clean

`img2epub build` コマンドに `--keep` オプションを指定したときに、削除されずに残ったテンポラリディレクトリは `img2epub clean` コマンドで削除できます。

    $ img2epub clean

## License

[MIT License](LICENSE.txt)
