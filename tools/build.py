"""根据每道题的 gen.py 生成测试数据，并自检

用法：
  python tools/build.py 20 21        # 构建指定题号
  python tools/build.py --all        # 构建所有带 gen.py 的题

gen.py 需要定义：
  samples() -> [(输入, 预期输出), ...]   与 description.md 中的示例一一对应（预期输出照抄题面）
  cases()   -> [输入, ...]              隐藏测试点的输入（预期输出由 solution.c 生成）

流程：清空 tests/ -> 写入样例与隐藏点 -> 用 solution.c 生成 .out
      -> 核对 solution 在样例上的输出与题面一致 -> 运行 verify.py 的完整检查。
"""
import importlib.util
import os
import random
import shutil
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(TOOLS))
sys.path.insert(0, TOOLS)
import judge  # noqa: E402
import verify  # noqa: E402

MAX_IN = 4 << 20   # 单个测试点输入上限 4MB（oj_lib 单行缓冲 2MB）


def load_gen(problem):
    path = os.path.join(problem["dir"], "gen.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location("gen_%d" % problem["id"], path)
    mod = importlib.util.module_from_spec(spec)
    random.seed(problem["id"])
    spec.loader.exec_module(mod)
    return mod


def build(problem):
    mod = load_gen(problem)
    if mod is None:
        print("  没有 gen.py，跳过生成，只做检查")
        return verify.check(problem)
    samples = list(mod.samples())
    hidden = list(mod.cases())
    if len(samples) != problem.get("samples", 2):
        print("  meta.json 的 samples=%s，但 gen.py 给了 %d 个样例" % (problem.get("samples"), len(samples)))
        return False
    tdir = os.path.join(problem["dir"], "tests")
    shutil.rmtree(tdir, ignore_errors=True)
    os.makedirs(tdir)
    inputs = [x[0] for x in samples] + hidden
    for i, text in enumerate(inputs, 1):
        if not text.endswith("\n"):
            text += "\n"
        if len(text.encode("utf-8")) > MAX_IN:
            print("  测试点 %d 输入太大" % i)
            return False
        with open(os.path.join(tdir, "%d.in" % i), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    if not verify.gen(problem, quiet=True):
        return False
    for i, (_, want) in enumerate(samples, 1):
        with open(os.path.join(tdir, "%d.out" % i), encoding="utf-8") as f:
            got = f.read()
        if judge.normalize(got) != judge.normalize(want):
            print("  样例 %d：solution.c 输出与题面不一致\n    题面: %s\n    实际: %s"
                  % (i, judge.normalize(want), judge.normalize(got)))
            return False
    return verify.check(problem)


def main():
    args = sys.argv[1:]
    probs = judge.all_problems()
    if "--all" not in args:
        probs = [p for p in probs if str(p["id"]) in args]
        missing = set(args) - {str(p["id"]) for p in probs}
        if missing:
            print("找不到题号:", " ".join(sorted(missing)))
    bad = []
    for p in probs:
        print("[%d] %s" % (p["id"], p["title"]))
        try:
            ok = build(p)
        except Exception as e:
            print("  构建异常: %r" % e)
            ok = False
        if not ok:
            bad.append(p["id"])
    print("\n共 %d 题, 失败 %d 题%s" % (len(probs), len(bad), (": " + " ".join(map(str, bad))) if bad else ""))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
