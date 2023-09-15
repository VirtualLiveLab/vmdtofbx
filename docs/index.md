# Mikubot

VLL Discord サーバーのためのBot

## Mikubot(旧)からの変更点

<details open>
<summary>利用者向け</summary>

### データベースを操作するコマンドが削除されました

これは`sushi_chan_sub`の技術力不足が原因です。必要なら実装します。

### 投票コマンドが新しくなりました

すべての投票が`/vote`コマンドに統合されて、最大20個の選択肢を投票できるようになりました。また、投票の集計も手軽になりました。詳しくは`/help`から参照してください。これに伴って、投票がタイムアウトした際に自動で集計する機能が削除されています。今後は明示的に集計を行ってください。ご迷惑をおかけします。

⚠️ 集計コマンドには比較的最近Discordに追加された機能が使用されています。もし利用できない場合はクライアントの更新をお試しください。

### Timetree

TimeTreeAPIが2023年12月22日に廃止されることが判明しました。
それ以降はTimeTreeに関わるすべての機能は使えなくなります。

</details>

<details>
<summary>会計担当者向け</summary>

### **部費未納ロールの処理が一部廃止されました**

詳しくは[こちら](#ロール関係の処理が一部変更されました)をご覧ください。
</details>

<details>
<summary>ロール処理</summary>

### ロール関係の処理が一部変更されました

WIP

</details>

<details>
<summary>開発者向け</summary>

### `poetry`と`pre-commit`を使用するようになりました

pipではなくpoetryを使用するようになりました。また、pre-commitを使用して
デプロイ用`requirements.txt`の自動生成を行うようになりました。

### 依存ライブラリを更新しました

`discord.py v1.7.3`及び`dislash.py`は今後利用できなくなる可能性があるため、`discord.py v2`ベースですべて書き直しました。

### ファイル分割

単一ファイルにすべての処理が書かれていたものを[Extension](https://discordpy.readthedocs.io/ja/latest/ext/commands/extensions.html)ベースのファイル分割に変更しました。

**app/\*\*/cog.py** という名前のファイル<u>**のみ**</u>が読み込まれます。

### スニペット

VSCode向けの新規Cog作成スニペットを追加してあります。

### CI

- `pre-commit`を使用して、基本的なコードチェックと`requirements.txt`の自動生成を行っています。
- Dockerイメージのビルドまでを事前にテストしています。(起動確認はしていません)
- typoチェッカーも回しています。

### ビルド

現在は`sushi_chan_sub`が開発用に使っている`PaaS`向けのDockerfileになっています。
あとからGCP向けに書き直します。

### 謎のライブラリ(experimental)

`components/ui`以下に実験的な謎のUIライブラリがあります。今後ドキュメントを書くかもしれません。

</details>
