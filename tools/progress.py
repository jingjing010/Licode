"""出题进度：对照 tools/plan.json 列出每一批已完成 / 缺失的题

用法：python tools/progress.py          # 汇总
      python tools/progress.py -v       # 同时列出缺失的题号
"""
import json
import os
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(TOOLS))
import judge  # noqa: E402


REQUIRED = ["meta.json", "description.md", "template.c", "solution.c", "driver.c", "explanation.md"]


def incomplete(p):
    """缺文件或缺测试点时返回原因，完整返回空串（不编译，只看文件）"""
    d = p["dir"]
    miss = [f for f in REQUIRED if not os.path.exists(os.path.join(d, f))]
    tdir = os.path.join(d, "tests")
    ins = [f for f in os.listdir(tdir) if f.endswith(".in")] if os.path.isdir(tdir) else []
    outs = [f for f in ins if os.path.exists(os.path.join(tdir, f[:-3] + ".out"))]
    if len(ins) < 10 or len(outs) < len(ins):
        miss.append("tests(%d in / %d out)" % (len(ins), len(outs)))
    return ", ".join(miss)


def main():
    verbose = "-v" in sys.argv
    with open(os.path.join(TOOLS, "plan.json"), encoding="utf-8") as f:
        plan = json.load(f)
    have = {p["id"]: p for p in judge.all_problems()}
    broken = {i: incomplete(p) for i, p in have.items() if incomplete(p)}
    for i in broken:
        del have[i]
    planned = set()
    total_done = total = 0
    for group, g in plan.items():
        if group.startswith("_"):
            continue
        print("== %s" % group)
        for name, ids in g["batches"].items():
            planned.update(ids)
            done = [i for i in ids if i in have]
            bad_list = [i for i in done if set(g["lists"]) - set(have[i].get("lists", []))]
            total_done += len(done)
            total += len(ids)
            line = "  %-24s %2d / %2d" % (name, len(done), len(ids))
            if verbose and len(done) < len(ids):
                line += "   缺: " + " ".join(str(i) for i in ids if i not in have)
            if bad_list:
                line += "   lists 字段缺失: " + " ".join(map(str, bad_list))
            print(line)
    extra = sorted(set(have) - planned)
    print("\n计划内 %d / %d 题，题库共 %d 题%s" % (
        total_done, total, len(have), ("（计划外: %s）" % " ".join(map(str, extra))) if extra else ""))
    if broken:
        print("不完整（已计入缺失）: %d 题" % len(broken))
        if verbose:
            for i in sorted(broken):
                print("  %d: %s" % (i, broken[i]))


if __name__ == "__main__":
    main()
