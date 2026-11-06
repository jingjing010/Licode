"""C 语言刷题 OJ —— 本地服务器（仅依赖 Python 标准库）

运行：python server.py   然后浏览器打开 http://127.0.0.1:8080
"""
import json
import mimetypes
import os
import sqlite3
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import judge

ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(ROOT, "static")
DB_PATH = os.path.join(ROOT, "data", "oj.db")
_db_lock = threading.Lock()
# Windows 注册表可能把 .js 识别成 text/plain，这里强制指定
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("text/html", ".html")


# ---------------------------------------------------------------- 数据库
def db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            verdict TEXT NOT NULL,
            passed INTEGER, total INTEGER, time_ms INTEGER,
            code_len INTEGER,
            detail TEXT,
            created_at TEXT NOT NULL)""")
        c.execute("CREATE INDEX IF NOT EXISTS idx_sub_pid ON submissions(problem_id)")
        c.execute("""CREATE TABLE IF NOT EXISTS notes (
            problem_id INTEGER PRIMARY KEY,
            favorite INTEGER NOT NULL DEFAULT 0,
            note TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL)""")


def get_notes():
    """返回 {problem_id: {"favorite": bool, "has_note": bool}}"""
    with db() as c:
        return {r["problem_id"]: {"favorite": bool(r["favorite"]), "has_note": bool(r["note"].strip())}
                for r in c.execute("SELECT problem_id, favorite, note FROM notes")}


def save_note(pid, **fields):
    with _db_lock, db() as c:
        c.execute("INSERT OR IGNORE INTO notes(problem_id, updated_at) VALUES (?, ?)",
                  (pid, time.strftime("%Y-%m-%d %H:%M:%S")))
        for k, v in fields.items():
            c.execute("UPDATE notes SET %s = ?, updated_at = ? WHERE problem_id = ?" % k,
                      (v, time.strftime("%Y-%m-%d %H:%M:%S"), pid))
        r = c.execute("SELECT favorite, note, updated_at FROM notes WHERE problem_id = ?", (pid,)).fetchone()
    return {"favorite": bool(r["favorite"]), "note": r["note"], "updated_at": r["updated_at"]}


def problem_status():
    """返回 {problem_id: 'ac' | 'tried'}"""
    st = {}
    with db() as c:
        for r in c.execute("SELECT problem_id, MAX(verdict='AC') AS ac FROM submissions GROUP BY problem_id"):
            st[r["problem_id"]] = "ac" if r["ac"] else "tried"
    return st


def read_text(path):
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def public_meta(p, status=None):
    keys = ["id", "slug", "title", "difficulty", "tags", "lists", "leetcode", "time_limit_ms"]
    d = {k: p.get(k) for k in keys}
    if status is not None:
        d["status"] = status.get(p["id"])
    return d


# ---------------------------------------------------------------- HTTP
class Handler(BaseHTTPRequestHandler):
    server_version = "C-OJ/1.0"

    def log_message(self, fmt, *args):  # 安静一点
        if "/api/" in (args[0] if args else ""):
            sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    def send_json(self, obj, code=200):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def read_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0:
            return {}
        return json.loads(self.rfile.read(n).decode("utf-8"))

    # ---------------- GET
    def do_GET(self):
        u = urlparse(self.path)
        path = u.path
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            if path.startswith("/api/"):
                return self.api_get(path, q)
            return self.serve_static(path)
        except Exception as e:
            self.send_json({"error": repr(e)}, 500)

    def serve_static(self, path):
        if path in ("/", ""):
            path = "/index.html"
        full = os.path.normpath(os.path.join(STATIC, path.lstrip("/")))
        if not full.startswith(STATIC) or not os.path.isfile(full):
            full = os.path.join(STATIC, "index.html")
        ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript",):
            ctype += "; charset=utf-8"
        with open(full, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def api_get(self, path, q):
        parts = [p for p in path.split("/") if p][1:]  # 去掉 'api'
        if parts == ["env"]:
            return self.send_json({"gcc": judge.find_gcc(), "gcc_version": judge.gcc_version()})

        if parts == ["guide"]:
            return self.send_json({"content": read_text(os.path.join(ROOT, "docs", "GUIDE.md"))})

        if parts == ["problems"]:
            st = problem_status()
            probs = judge.all_problems()
            notes = get_notes()
            counts = {}
            with db() as c:
                for r in c.execute("SELECT problem_id, COUNT(*) n, SUM(verdict='AC') ac, MAX(created_at) last"
                                   " FROM submissions GROUP BY problem_id"):
                    counts[r["problem_id"]] = (r["n"], r["ac"] or 0, r["last"])
            res = []
            for p in probs:
                m = public_meta(p, st)
                m["submit_count"], m["ac_count"], m["last_submit"] = counts.get(p["id"], (0, 0, None))
                n = notes.get(p["id"], {})
                m["favorite"] = n.get("favorite", False)
                m["has_note"] = n.get("has_note", False)
                res.append(m)
            return self.send_json(res)

        if len(parts) >= 2 and parts[0] == "problems":
            p = judge.get_problem(parts[1])
            if not p:
                return self.send_json({"error": "题目不存在"}, 404)
            if len(parts) == 2:
                d = public_meta(p, problem_status())
                d["description"] = read_text(os.path.join(p["dir"], "description.md"))
                d["template"] = read_text(os.path.join(p["dir"], "template.c"))
                d["hints"] = p.get("hints", [])
                tests = judge.load_tests(p)[: p.get("samples", 2)]
                d["samples"] = [{"input": t["input"], "output": t["output"]} for t in tests]
                lst = q.get("list")
                ids = [x["id"] for x in judge.all_problems() if not lst or lst in x["lists"] or x["id"] == p["id"]]
                i = ids.index(p["id"])
                d["prev"] = ids[i - 1] if i > 0 else None
                d["next"] = ids[i + 1] if i + 1 < len(ids) else None
                with db() as c:
                    r = c.execute("SELECT favorite, note FROM notes WHERE problem_id = ?", (p["id"],)).fetchone()
                d["favorite"] = bool(r and r["favorite"])
                d["note"] = r["note"] if r else ""
                return self.send_json(d)
            if parts[2] == "explanation":
                return self.send_json({"content": read_text(os.path.join(p["dir"], "explanation.md"))})

        if parts == ["submissions"]:
            sql = "SELECT id, problem_id, verdict, passed, total, time_ms, code_len, created_at FROM submissions"
            args = []
            if q.get("problem_id"):
                sql += " WHERE problem_id = ?"
                args.append(int(q["problem_id"]))
            sql += " ORDER BY id DESC LIMIT ?"
            args.append(int(q.get("limit", 100)))
            titles = {p["id"]: p["title"] for p in judge.all_problems()}
            with db() as c:
                rows = [dict(r) for r in c.execute(sql, args)]
            for r in rows:
                r["title"] = titles.get(r["problem_id"], "?")
                r["verdict_name"] = judge.VERDICT_NAMES.get(r["verdict"], r["verdict"])
            return self.send_json(rows)

        if len(parts) == 2 and parts[0] == "submissions":
            with db() as c:
                r = c.execute("SELECT * FROM submissions WHERE id = ?", (int(parts[1]),)).fetchone()
            if not r:
                return self.send_json({"error": "提交不存在"}, 404)
            d = dict(r)
            d["detail"] = json.loads(d["detail"] or "{}")
            d["verdict_name"] = judge.VERDICT_NAMES.get(d["verdict"], d["verdict"])
            return self.send_json(d)

        if parts == ["stats"]:
            probs = judge.all_problems()
            st = problem_status()
            by, by_list = {}, {}
            for p in probs:
                buckets = [by.setdefault(p["difficulty"], {"total": 0, "solved": 0})]
                buckets += [by_list.setdefault(l, {"total": 0, "solved": 0}) for l in p["lists"]]
                for b in buckets:
                    b["total"] += 1
                    if st.get(p["id"]) == "ac":
                        b["solved"] += 1
            with db() as c:
                r = c.execute("SELECT COUNT(*) n, SUM(verdict='AC') ac FROM submissions").fetchone()
                days = [dict(x) for x in c.execute(
                    "SELECT substr(created_at,1,10) d, COUNT(*) n FROM submissions GROUP BY d ORDER BY d DESC LIMIT 30")]
            return self.send_json({
                "total": len(probs), "solved": sum(1 for v in st.values() if v == "ac"),
                "by_difficulty": by, "by_list": by_list, "submissions": r["n"], "accepted": r["ac"] or 0, "days": days,
            })

        return self.send_json({"error": "not found"}, 404)

    # ---------------- POST
    def do_POST(self):
        path = urlparse(self.path).path
        try:
            body = self.read_json()
            parts = [x for x in path.split("/") if x][1:]
            if len(parts) == 3 and parts[0] == "problems" and parts[2] in ("favorite", "note"):
                p = judge.get_problem(parts[1])
                if not p:
                    return self.send_json({"error": "题目不存在"}, 404)
                if parts[2] == "favorite":
                    return self.send_json(save_note(p["id"], favorite=1 if body.get("favorite") else 0))
                note = str(body.get("note", ""))
                if len(note) > 64 * 1024:
                    return self.send_json({"error": "笔记太长（上限 64KB）"}, 400)
                return self.send_json(save_note(p["id"], note=note))
            if path in ("/api/run", "/api/submit"):
                p = judge.get_problem(body.get("problem_id"))
                if not p:
                    return self.send_json({"error": "题目不存在"}, 404)
                code = body.get("code", "")
                if len(code) > 64 * 1024:
                    return self.send_json({"error": "代码太长（上限 64KB）"}, 400)
                if path == "/api/run":
                    return self.send_json(judge.judge(p, code, "run", body.get("custom_input")))
                res = judge.judge(p, code, "submit")
                with _db_lock, db() as c:
                    cur = c.execute(
                        "INSERT INTO submissions(problem_id, code, verdict, passed, total, time_ms, code_len, detail, created_at)"
                        " VALUES (?,?,?,?,?,?,?,?,?)",
                        (p["id"], code, res["verdict"], res.get("passed"), res.get("total"), res.get("time_ms"),
                         len(code.encode("utf-8")), json.dumps(res, ensure_ascii=False),
                         time.strftime("%Y-%m-%d %H:%M:%S")))
                    res["submission_id"] = cur.lastrowid
                return self.send_json(res)
            return self.send_json({"error": "not found"}, 404)
        except Exception as e:
            self.send_json({"error": repr(e)}, 500)


def main():
    port = 8080
    for a in sys.argv[1:]:
        if a.isdigit():
            port = int(a)
    init_db()
    g = judge.find_gcc()
    print("=" * 56)
    print("  C 语言刷题 OJ 已启动")
    print("  编译器: %s" % (g or "未找到 gcc！请安装 MinGW-w64 或在 config.json 中配置"))
    print("  题目数: %d" % len(judge.all_problems()))
    while True:
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            port += 1
    url = "http://127.0.0.1:%d" % port
    print("  地址:   %s" % url)
    print("  关闭本窗口即可退出")
    print("=" * 56)
    if "--no-browser" not in sys.argv:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
