# できること
COVESA VSS の JSON ツリーを Graphviz で PDFに可視化するツール<br>

## 前提条件
gitpod上での動作検証済み

# 構成
```
vss-tree/
├── Containerfile         # ランタイムのみを入れたベースイメージ
├── vss_draw.py           # 可視化ロジック
├── vss.json              # jsonで書かれたVSS ツリー ファイル
```
# 使い方
## 1.gidpodを起動
githubのURLの先頭に以下を付け加える
```
https://gitpod.io/#
```
## 2.必要なパッケージをインストール
```
sudo apt-get update 
sudo apt-get install -y graphviz
pip install graphviz
```
## 3.pythonファイルを実行
```
python vss_draw.py vss_1.json vss_vehicle.pdf Vehicle
```
## 4.pdfをダウンロードする


# 描画仕様
| type        | 形状             | 色 (`fillcolor`)    |
| ----------- | --------------- | ------------------ |
| `branch`    | 四角 (`box`)     | なし                 |
| `sensor`    | 楕円 (`ellipse`) | `#ffcccc` （淡いピンク）  |
| `actuator`  | 楕円             | `#b0c4ff` （ライトブルー） |
| `attribute` | 楕円             | `#eeeeee` （薄いグレー）  |

