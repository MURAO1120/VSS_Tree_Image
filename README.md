# できること

COVESA VSS の JSON ツリーを Graphviz で PDF（または SVG/PNG）に可視化するツール<br>
Podmanで構築しているのでホスト側には特にインストールは必要ない

## 前提条件
Podman(Docker)がインストールされて、セットアップ時にインターネットに接続できる環境<br>
Docker環境は試していないが、セットアップ以降のpodmanコマンドをdockerに置き換えれば動くはず


# 構成
```
vss-tree/
├── Containerfile         # ランタイムのみを入れたベースイメージ
├── vss_draw.py           # 可視化ロジック
├── data/
│   └── vss.json          # jsonで書かれたVSS ツリー ファイル
└── net/
    └── proxy2.crt        # 社内プロキシ CA (不要なら削除)
```

# 初回セットアップ
環境構築にはコンテナ内にいくつかライブラリをインストールする必要があり、コンテナがインターネットに接続をする<br>
NTC内でセットアップする場合、コンテナ内にサーバの証明書を配置する必要がある<br>
逆にNTC外では、証明書は不要であるためコンテナビルドを行うContainerfileを編集を行う<br>
(証明書があっても問題なく接続できるが念のため削除する)

## NTC内の場合
```bash
# ベースイメージをビルド （code はコピーせず、ランタイムだけ）
# Graphviz + python3 + python-graphviz が入った軽量イメージ

podman build -t vss-tree .
```

## NTC外の場合
Containerfileの下記行を削除して上記podmanコマンドを実行する
```
COPY ./net/proxy2.crt /usr/local/share/ca-certificates/
```

# 使い方
下記のコマンドを実行すると./data/ディレクトリにpdfが出力される
```bash
podman run --rm \
    -v "$(pwd)":/work:Z \
    vss-tree \
    /work/vss_draw.py \
    /work/data/vss.json \
    /work/data/hood.pdf  \
    Vehicle.Body.Hood
```
* /work/vss_draw.py – スクリプト
* /work/data/vss.json – 入力 JSON
* /work/data/hood.pdf – 出力ファイル名
* 4 番目の引数（省略可）– ルートノードパス。デフォルト "Vehicle"

# 描画仕様
| type        | 形状             | 色 (`fillcolor`)    |
| ----------- | --------------- | ------------------ |
| `branch`    | 四角 (`box`)     | なし                 |
| `sensor`    | 楕円 (`ellipse`) | `#ffcccc` （淡いピンク）  |
| `actuator`  | 楕円             | `#b0c4ff` （ライトブルー） |
| `attribute` | 楕円             | `#eeeeee` （薄いグレー）  |

* エッジは曲線 (splines="curved")
* ノードがエッジより前面になるよう outputorder="edgesfirst"
* 余白は nodesep=0.35, ranksep=0.5（vss_draw.py 先頭で調整可）