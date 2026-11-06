"""题库自检工具

用法：
  python tools/verify.py              # 用每题的 solution.c 提交，检查是否全部 AC
  python tools/verify.py 1 9 13       # 只检查指定题号
  python tools/verify.py --gen 1      # 用 solution.c 运行 tests/*.in，生成/覆盖 tests/*.out
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import judge  # noqa: E402

REQUIRED = ["meta.json", "description.md", "explanation.md", "template.c", "driver.c", "solution.c"]
DIFFICULTIES = {"简单", "中等", "困难"}
LISTS = {"hot100", "embedded"}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def gen(problem, quiet=False):
    wd = judge._workdir()
    try:
        ok, err, hints, warn = judge.compile_code(problem, read(os.path.join(problem["dir"], "solution.c")), wd)
        if not ok:
            print("  编译失败:\n" + err)
            return False
        exe = os.path.join(wd, "main.exe" if os.name == "nt" else "main")
        tdir = os.path.join(problem["dir"], "tests")
        for t in judge.load_tests(problem):
            r = judge.run_one(exe, t["input"], 5000)
            if r["status"] != "OK":
                print("  测试点 %s 运行失败: %s %s" % (t["name"], r["status"], r["stderr"]))
                return False
            with open(os.path.join(tdir, t["name"] + ".out"), "w", encoding="utf-8", newline="\n") as f:
                f.write(judge.normalize(r["stdout"]) + "\n")
            if not quiet:
                print("  %s.out <- %s" % (t["name"], judge.normalize(r["stdout"])[:80]))
        return True
    finally:
        judge._cleanup(wd)


def check(problem):
    ok = True
    for f in REQUIRED:
        if not os.path.exists(os.path.join(problem["dir"], f)):
            print("  缺少文件:", f)
            ok = False
    if not ok:
        return False
    if problem.get("difficulty") not in DIFFICULTIES:
        print("  difficulty 必须是 简单/中等/困难")
        return False
    bad_lists = set(problem.get("lists", [])) - LISTS
    if bad_lists:
        print("  未知的 lists:", bad_lists)
        return False
    if os.path.basename(problem["dir"]) != "%04d-%s" % (problem["id"], problem.get("slug", "")):
        print("  目录名应为 %04d-%s" % (problem["id"], problem.get("slug", "")))
        return False
    tests = judge.load_tests(problem)
    if len(tests) < problem.get("samples", 2):
        print("  测试点数量少于样例数")
        return False
    for t in tests:
        if not t["output"].strip():
            print("  测试点 %s 缺少 .out" % t["name"])
            return False
    r = judge.judge(problem, read(os.path.join(problem["dir"], "solution.c")), "submit")
    if r["verdict"] != "AC":
        print("  solution.c 未通过:", r.get("verdict"), r.get("compile_error", ""), r.get("failed_case", ""), r.get("message", ""))
        return False
    # 模板应能编译（即使答案不对）
    wd = judge._workdir()
    try:
        cok, err, _, _ = judge.compile_code(problem, read(os.path.join(problem["dir"], "template.c")), wd)
        if not cok:
            print("  template.c 无法编译:\n" + err)
            return False
    finally:
        judge._cleanup(wd)
    n_blocks = 0
    for k, code in enumerate(explanation_solutions(problem), 1):
        rr = judge.judge(problem, code, "submit")
        if rr["verdict"] != "AC":
            print("  explanation.md 中第 %d 段完整代码未通过: %s %s %s" % (
                k, rr.get("verdict"), rr.get("compile_error", "")[:600], rr.get("failed_case", "")))
            return False
        n_blocks += 1
    print("  AC  (%d 个测试点, 最大耗时 %d ms, 题解代码 %d 段均 AC)" % (r["total"], r["time_ms"], n_blocks))
    return True


FUNC_DEF = re.compile(r"^[A-Za-z_][\w \t\*]*?\b([A-Za-z_]\w*)\s*\([^;{)]*\)\s*\{", re.M)


def explanation_solutions(problem):
    """explanation.md 里定义了 template.c 中全部函数的 ```c 代码块，视为完整解法。
       含 "..." 或 "❌" 的代码块是示意/错误示范，不检查。"""
    names = set(FUNC_DEF.findall(read(os.path.join(problem["dir"], "template.c"))))
    if not names:
        return []
    md = read(os.path.join(problem["dir"], "explanation.md"))
    res = []
    for code in re.findall(r"^```c[ \t]*\n(.*?)^```", md, flags=re.S | re.M):
        if "main(" in code or "..." in code or "❌" in code:
            continue
        if names <= set(FUNC_DEF.findall(code)):
            res.append(code)
    return res


def main():
    args = sys.argv[1:]
    do_gen = "--gen" in args
    ids = [a for a in args if a != "--gen"]
    probs = judge.all_problems()
    if ids:
        probs = [p for p in probs if str(p["id"]) in ids]
    bad = 0
    for p in probs:
        print("[%d] %s" % (p["id"], p["title"]))
        good = gen(p) if do_gen else check(p)
        bad += 0 if good else 1
    print("\n共 %d 题, 失败 %d 题" % (len(probs), bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
