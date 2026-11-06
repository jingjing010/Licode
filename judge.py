"""判题核心：拼接代码 -> gcc 编译 -> 逐个测试点运行 -> 比对输出。"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

ROOT = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_DIR = os.path.join(ROOT, "problems")
COMMON_DIR = os.path.join(PROBLEMS_DIR, "_common")
TMP_DIR = os.path.join(ROOT, "data", "tmp")

HEADERS = """#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <math.h>
#include <ctype.h>
#include <stdint.h>
"""

MAX_OUTPUT = 1 << 20  # 1MB 输出上限

# Windows 下禁止程序崩溃时弹出 "xxx.exe 已停止工作" 对话框
if os.name == "nt":
    try:
        import ctypes
        ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
    except Exception:
        pass


# ---------------------------------------------------------------- gcc 查找
_gcc_cache = None


def find_gcc():
    global _gcc_cache
    if _gcc_cache and os.path.exists(_gcc_cache):
        return _gcc_cache
    cands = []
    if os.environ.get("OJ_GCC"):
        cands.append(os.environ["OJ_GCC"])
    cfg = os.path.join(ROOT, "config.json")
    if os.path.exists(cfg):
        try:
            with open(cfg, encoding="utf-8") as f:
                g = json.load(f).get("gcc")
            if g:
                cands.append(g)
        except Exception:
            pass
    w = shutil.which("gcc")
    if w:
        cands.append(w)
    cands += [
        r"C:\mingw64\bin\gcc.exe",
        r"C:\MinGW\bin\gcc.exe",
        r"C:\msys64\mingw64\bin\gcc.exe",
        r"C:\msys64\ucrt64\bin\gcc.exe",
        r"C:\TDM-GCC-64\bin\gcc.exe",
        r"C:\Program Files (x86)\Dev-Cpp\MinGW64\bin\gcc.exe",
        r"C:\Program Files\CodeBlocks\MinGW\bin\gcc.exe",
        r"D:\mingw64\bin\gcc.exe",
        "/usr/bin/gcc",
        "/usr/local/bin/gcc",
    ]
    for c in cands:
        if c and os.path.exists(c):
            _gcc_cache = c
            return c
    return None


def gcc_version():
    g = find_gcc()
    if not g:
        return None
    try:
        out = subprocess.run([g, "--version"], capture_output=True, timeout=15)
        return out.stdout.decode("utf-8", "replace").splitlines()[0]
    except Exception:
        return None


# ---------------------------------------------------------------- 题目加载
def _read(path, default=""):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_problem(pdir):
    meta_path = os.path.join(pdir, "meta.json")
    if not os.path.exists(meta_path):
        return None
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)
    meta["dir"] = pdir
    meta.setdefault("time_limit_ms", 1000)
    meta.setdefault("samples", 2)
    meta.setdefault("tags", [])
    meta.setdefault("hints", [])
    meta.setdefault("lists", [])
    return meta


# 500 道题时每个请求都重新解析 meta.json 太慢：按 (目录名, meta.json 修改时间) 做缓存
_problems_cache = {"sig": None, "list": [], "by_id": {}}


def _problems_signature():
    sig = []
    with os.scandir(PROBLEMS_DIR) as it:
        for e in it:
            if e.name.startswith("_") or not e.is_dir():
                continue
            try:
                sig.append((e.name, os.stat(os.path.join(e.path, "meta.json")).st_mtime_ns))
            except OSError:
                pass
    sig.sort()
    return tuple(sig)


def all_problems():
    if not os.path.isdir(PROBLEMS_DIR):
        return []
    sig = _problems_signature()
    if sig != _problems_cache["sig"]:
        res = []
        for name, _ in sig:
            try:
                p = load_problem(os.path.join(PROBLEMS_DIR, name))
            except Exception as e:  # 某道题 meta.json 写坏了不要拖垮整个题库
                sys.stderr.write("[OJ] 无法加载题目 %s: %r\n" % (name, e))
                continue
            if p:
                res.append(p)
        res.sort(key=lambda m: m["id"])
        _problems_cache.update(sig=sig, list=res, by_id={str(p["id"]): p for p in res})
    return list(_problems_cache["list"])


def get_problem(pid):
    all_problems()
    return _problems_cache["by_id"].get(str(pid))


def load_tests(problem):
    tdir = os.path.join(problem["dir"], "tests")
    if not os.path.isdir(tdir):
        return []
    names = [f[:-3] for f in os.listdir(tdir) if f.endswith(".in")]

    def key(n):
        return (0, int(n)) if n.isdigit() else (1, n)

    tests = []
    for n in sorted(names, key=key):
        tests.append({
            "name": n,
            "input": _read(os.path.join(tdir, n + ".in")),
            "output": _read(os.path.join(tdir, n + ".out")),
        })
    return tests


# ---------------------------------------------------------------- 编译
def build_source(problem, user_code):
    prelude = _read(os.path.join(problem["dir"], "prelude.c"))
    lib = _read(os.path.join(COMMON_DIR, "oj_lib.c"))
    driver = _read(os.path.join(problem["dir"], "driver.c"))
    return "".join([
        HEADERS,
        '#line 1 "prelude.c"\n', prelude, "\n",
        '#line 1 "solution.c"\n', user_code, "\n",
        '#line 1 "oj_lib.c"\n', lib, "\n",
        '#line 1 "driver.c"\n', driver, "\n",
    ])


ERROR_HINTS = [
    (r"expected ';'", "缺少分号 ;  —— 检查报错行或它的【上一行】末尾是不是忘了写分号。"),
    (r"expected '\)'|expected '\]'|expected '\}'", "括号不配对 —— 检查 ( ) [ ] { } 是否一一对应。"),
    (r"expected declaration or statement at end of input", "代码结尾缺少 }  —— 大括号没有闭合。"),
    (r"undeclared", "使用了未声明的变量/标识符 —— 是不是拼写错了，或者忘了先定义？"),
    (r"implicit declaration of function '(\w+)'", "调用了未声明的函数 —— 检查函数名拼写；自己写的辅助函数要定义在调用它的函数【前面】。"),
    (r"conflicting types for", "函数类型冲突 —— 函数名/参数/返回值必须和模板一致，不要改函数签名。"),
    (r"redefinition of 'main'|multiple definition of `main'|redefinition of .main.", "不要写 main 函数！本 OJ 和力扣一样，只需实现题目给出的函数，main 由系统提供。"),
    (r"redefinition of", "重复定义 —— 同一个变量/函数在同一作用域里定义了两次。"),
    (r"too few arguments", "调用函数时参数少了。"),
    (r"too many arguments", "调用函数时参数多了。"),
    (r"incompatible pointer type|makes pointer from integer|makes integer from pointer", "指针类型不匹配 —— 检查 * 和 & 的使用，以及 malloc 的结果类型。"),
    (r"control reaches end of non-void function", "函数可能没有 return —— 有返回值的函数，每条执行路径都要 return。"),
    (r"lvalue required", "赋值号左边必须是变量 —— 是不是把 == 写成了 = ，或者对表达式赋值了？"),
    (r"subscripted value is neither array nor pointer", "对不是数组/指针的变量使用了 [ ] 下标。"),
    (r"stray '\\\d+' in program|stray '\\3", "代码里有中文符号！（如中文分号 ；中文括号（）中文引号“”）请切换到英文输入法重新输入。"),
    (r"unknown type name", "未知类型名 —— 拼写错误？或者 C 语言没有这个类型（C 里没有 string、vector 这些 C++ 的东西）。"),
    (r"suggest parentheses around assignment", "if/while 条件里用了 = （赋值），你可能想写 == （比较）。"),
]

RUNTIME_HINTS = {
    3221225477: "访问违规 (0xC0000005)：数组越界、使用了空指针(NULL) 或野指针。",
    3221225725: "栈溢出 (0xC00000FD)：递归太深（可能是没有递归出口），或者在函数里开了特别大的局部数组。",
    3221225620: "整数除以零 (0xC0000094)：检查除法 / 和取模 % 的除数是否可能为 0。",
    3221225477 - 2**32: "访问违规 (0xC0000005)：数组越界、使用了空指针(NULL) 或野指针。",
    3221226505: "堆损坏 (0xC0000374)：可能写越界了 malloc 申请的内存，或重复 free。",
    3221225501: "非法指令 (0xC000001D)。",
    3: "OJ 驱动报告输入格式错误（自定义输入的格式不对？）。",
    134: "程序异常终止 (abort)。",
    139: "段错误 (Segmentation fault)：数组越界或空指针。",
    -11: "段错误 (Segmentation fault)：数组越界或空指针。",
    -8: "浮点异常：可能除以了 0。",
    -6: "程序异常终止 (abort)。",
}


def explain_compile_errors(text):
    hints = []
    for pat, hint in ERROR_HINTS:
        if re.search(pat, text) and hint not in hints:
            hints.append(hint)
    return hints


def compile_code(problem, user_code, workdir):
    gcc = find_gcc()
    if not gcc:
        return False, "未找到 gcc 编译器！请安装 MinGW-w64，或在 config.json 里配置 gcc 路径。", [], ""
    src = os.path.join(workdir, "main.c")
    exe = os.path.join(workdir, "main.exe" if os.name == "nt" else "main")
    with open(src, "w", encoding="utf-8") as f:
        f.write(build_source(problem, user_code))
    cmd = [gcc, "-std=gnu11", "-O2", "-Wall", "-Wno-unused-variable", "-Wno-unused-but-set-variable",
           "-Wno-unused-function", "-fdiagnostics-color=never", src, "-o", exe, "-lm"]
    if os.name == "nt":
        cmd.insert(-1, "-Wl,--stack,67108864")
    env = os.environ.copy()
    gdir = os.path.dirname(gcc)
    env["PATH"] = gdir + os.pathsep + env.get("PATH", "")
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=30, cwd=workdir, env=env)
    except subprocess.TimeoutExpired:
        return False, "编译超时", [], ""
    msg = r.stderr.decode("utf-8", "replace").replace(src, "main.c")
    if r.returncode != 0 or not os.path.exists(exe):
        return False, clean_diag(msg), explain_compile_errors(msg), ""
    warnings = "\n".join(l for l in clean_diag(msg).splitlines() if "solution.c" in l)
    return True, "", [], warnings


def clean_diag(msg):
    # 去掉无关的路径噪音
    msg = re.sub(r"^.*?In file included from.*$\n?", "", msg, flags=re.M)
    return msg.strip()


# ---------------------------------------------------------------- 运行
def normalize(s):
    lines = s.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    lines = [l.rstrip() for l in lines]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def run_one(exe, input_text, tl_ms):
    hard = tl_ms / 1000.0 * 2 + 1.0
    env = os.environ.copy()
    gcc = find_gcc()
    if gcc:
        env["PATH"] = os.path.dirname(gcc) + os.pathsep + env.get("PATH", "")
    start = time.perf_counter()
    try:
        p = subprocess.run([exe], input=input_text.encode("utf-8"), capture_output=True,
                           timeout=hard, cwd=os.path.dirname(exe), env=env)
    except subprocess.TimeoutExpired as e:
        return {"status": "TLE", "time_ms": int(hard * 1000), "stdout": (e.stdout or b"")[:4096].decode("utf-8", "replace"),
                "stderr": (e.stderr or b"")[:4096].decode("utf-8", "replace"), "code": None}
    t = int((time.perf_counter() - start) * 1000)
    out = p.stdout
    res = {
        "time_ms": t,
        "stdout": out[:MAX_OUTPUT].decode("utf-8", "replace"),
        "stderr": p.stderr[:8192].decode("utf-8", "replace"),
        "code": p.returncode,
    }
    if len(out) > MAX_OUTPUT:
        res["status"] = "OLE"
    elif p.returncode != 0:
        res["status"] = "RE"
        res["hint"] = RUNTIME_HINTS.get(p.returncode, "程序非正常退出，返回码 %s。" % p.returncode)
    elif t > tl_ms:
        res["status"] = "TLE"
    else:
        res["status"] = "OK"
    return res


VERDICT_NAMES = {
    "AC": "Accepted",
    "WA": "Wrong Answer",
    "CE": "Compilation Error",
    "RE": "Runtime Error",
    "TLE": "Time Limit Exceeded",
    "OLE": "Output Limit Exceeded",
    "SE": "System Error",
}


def _short(s, n=2000):
    return s if len(s) <= n else s[:n] + "\n...（内容过长已截断）"


def _workdir():
    os.makedirs(TMP_DIR, exist_ok=True)
    d = os.path.join(TMP_DIR, uuid.uuid4().hex[:12])
    os.makedirs(d)
    return d


def _cleanup(d):
    for _ in range(5):
        try:
            shutil.rmtree(d)
            return
        except Exception:
            time.sleep(0.2)


def judge(problem, user_code, mode="submit", custom_input=None):
    """mode = submit: 跑全部测试点，遇错即停（与杭电 OJ 一致）
       mode = run:    只跑样例 + 自定义输入，返回每个样例的详细结果"""
    wd = _workdir()
    try:
        ok, err, hints, warnings = compile_code(problem, user_code, wd)
        if not ok:
            return {"verdict": "CE", "verdict_name": VERDICT_NAMES["CE"], "compile_error": err, "hints": hints}
        exe = os.path.join(wd, "main.exe" if os.name == "nt" else "main")
        tl = int(problem.get("time_limit_ms", 1000))
        tests = load_tests(problem)
        result = {"warnings": warnings, "time_limit_ms": tl}

        if mode == "run":
            cases = []
            for t in tests[: problem.get("samples", 2)]:
                r = run_one(exe, t["input"], tl)
                c = {"name": "样例 " + t["name"], "input": t["input"], "expected": t["output"],
                     "output": _short(r["stdout"]), "stderr": _short(r["stderr"]), "time_ms": r["time_ms"]}
                if r["status"] == "OK":
                    c["status"] = "AC" if normalize(r["stdout"]) == normalize(t["output"]) else "WA"
                else:
                    c["status"] = r["status"]
                    c["hint"] = r.get("hint")
                cases.append(c)
            if custom_input is not None and custom_input.strip():
                r = run_one(exe, custom_input, tl)
                cases.append({"name": "自定义输入", "input": custom_input, "expected": None,
                              "output": _short(r["stdout"]), "stderr": _short(r["stderr"]),
                              "time_ms": r["time_ms"], "status": "DONE" if r["status"] == "OK" else r["status"],
                              "hint": r.get("hint")})
            result["cases"] = cases
            bad = [c for c in cases if c["status"] not in ("AC", "DONE")]
            result["verdict"] = bad[0]["status"] if bad else "AC"
            result["verdict_name"] = VERDICT_NAMES.get(result["verdict"], result["verdict"])
            return result

        # submit
        if not tests:
            return {"verdict": "SE", "verdict_name": VERDICT_NAMES["SE"], "message": "该题没有测试数据"}
        max_t = 0
        for i, t in enumerate(tests):
            r = run_one(exe, t["input"], tl)
            if r["status"] == "TLE" and i == 0 and r["code"] is not None:
                r = run_one(exe, t["input"], tl)  # 首次运行可能被杀毒软件拖慢，重试一次
            max_t = max(max_t, r["time_ms"]) if r["status"] != "TLE" else max_t
            verdict = None
            if r["status"] != "OK":
                verdict = r["status"]
            elif normalize(r["stdout"]) != normalize(t["output"]):
                verdict = "WA"
            if verdict:
                result.update({
                    "verdict": verdict, "verdict_name": VERDICT_NAMES[verdict],
                    "passed": i, "total": len(tests), "time_ms": max_t,
                    "failed_case": {
                        "index": i + 1, "input": _short(t["input"]), "expected": _short(t["output"]),
                        "output": _short(r["stdout"]), "stderr": _short(r["stderr"]), "hint": r.get("hint"),
                    },
                })
                return result
        result.update({"verdict": "AC", "verdict_name": VERDICT_NAMES["AC"], "passed": len(tests),
                       "total": len(tests), "time_ms": max_t})
        return result
    except Exception as e:  # pragma: no cover
        return {"verdict": "SE", "verdict_name": VERDICT_NAMES["SE"], "message": repr(e)}
    finally:
        _cleanup(wd)
