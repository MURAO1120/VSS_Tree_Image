#!/usr/bin/env python3
import json, sys, pathlib
from graphviz import Digraph

# ---------------- ユーティリティ ----------------
def load_vss(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def descend(vss, dotted_path):
    node = vss
    for part in dotted_path.split('.'):
        # VSS 2.0 以降は "children" が入る場合と入らない場合がある
        node = node.get("children", {}).get(part, node.get(part, {}))
    return node

# 深さ優先で (path, entry, type) を yield
def walk(node, prefix=""):
    typ = node.get("type", "branch")
    yield prefix.rstrip("."), node, typ
    for name, child in (node.get("children") or {}).items():
        yield from walk(child, f"{prefix}{name}.")

# ---------------- グラフ生成 ----------------
def classify_color(typ):
    """
    type から塗りつぶし色を返す。
    branch は None を返して「塗りなし」にする。
    """
    if typ == "branch":
        return None                 # 塗りつぶさない
    if typ == "sensor":
        return "#b0c4ff"            # ライトブルー
    if typ == "actuator":
        return "#ffcccc"            # 淡いピンク
    if typ == "attribute":
        return "#eeeeee"            # 薄いグレー
    return "#ffffff"                # 念のためのデフォルト（白）

def build_graph(root_node, root_name):
    g = Digraph(
        "VSS",
        graph_attr={
            "rankdir": "TB",
            "splines": "curved",
            "overlap": "false",          # ノード重なり防止
            "nodesep": "0.35",           # 同レイヤ内の間隔
            "ranksep": "0.5",            # レイヤ間の間隔
            "outputorder": "edgesfirst"  # エッジ→ノードの順で描く
        }
    )

    for full, entry, typ in walk(root_node, f"{root_name}."):
        label = full.split('.')[-1]

        # 形状と色を type で決定
        shape = "box" if typ == "branch" else "ellipse"
        fill  = classify_color(typ)
        style = "filled" if fill else ""   # branch は塗りなし

        g.node(
            full,
            label=label if typ == "branch" else f"{label}\n({entry.get('datatype','')})",
            shape=shape,
            style=style,
            fillcolor=fill or "white",
            fontname="Helvetica",
            fontsize="10"
        )

        parent = '.'.join(full.split('.')[:-1])
        if parent:
            g.edge(parent, full)

    return g

# ---------------- エントリポイント ----------------
def main():
    if len(sys.argv) < 3:
        print("usage: vss_draw.py <VSS.json> <output.pdf> [root_path]", file=sys.stderr)
        sys.exit(1)

    json_path, pdf_path = sys.argv[1], sys.argv[2]
    root = sys.argv[3] if len(sys.argv) > 3 else "Vehicle"

    vss = load_vss(json_path)
    root_node = descend(vss, root)
    graph = build_graph(root_node, root)
    out = pathlib.Path(pdf_path)
    graph.render(filename=out.stem,
                 directory=str(out.parent),
                 format=out.suffix.lstrip('.'),
                 cleanup=True)

if __name__ == "__main__":
    main()
