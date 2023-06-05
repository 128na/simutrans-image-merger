# Simutrans Imager Merger

画像の重ね合わせ、Simutrans特有の特殊色の削除、透過色の変換などができます。


## 使い方

画像加工のjson設定ファイルを指定して実行するだけです。

```
simutrans-image-merger.exe definition.json
```

### jsonのバリデーション
`-v` オプションを付けるとJsonSchemaによるバリデーションのみ行われます。

```
simutrans-image-merger.exe -v .\demo\sample2\invalid.json

False is not of type 'string'

Failed validating 'type' in schema[0]['properties']['pathes']['items']:
    {'type': 'string'}

On instance['pathes'][0]:
    False
```

### 設定jsonフォーマット

参考：[demo/](demo/)

## 開発者向け
npm が導入済みであればnpmスクリプトで実行できます。

```
npm py:install

npm py:build
```

スクリプトを使用しない場合はpackage.json内のコマンドを直接実行して下さい。
