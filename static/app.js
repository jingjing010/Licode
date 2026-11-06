/* C 语言刷题 OJ —— 前端主逻辑（单页应用，hash 路由，无第三方依赖） */
(function () {
  "use strict";

  var app = document.getElementById("app");

  // ------------------------------------------------------------ 工具
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function el(html) {
    var t = document.createElement("template");
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  }

  var store = {
    get: function (k, def) {
      try {
        var v = localStorage.getItem("oj." + k);
        return v == null ? def : JSON.parse(v);
      } catch (e) { return def; }
    },
    set: function (k, v) {
      try { localStorage.setItem("oj." + k, JSON.stringify(v)); } catch (e) { /* 存储满了就算了 */ }
    },
    del: function (k) {
      try { localStorage.removeItem("oj." + k); } catch (e) { /* ignore */ }
    },
  };

  async function api(path, body) {
    var opt = {};
    if (body !== undefined) {
      opt = { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
    }
    var r;
    try {
      r = await fetch("/api/" + path, opt);
    } catch (e) {
      throw new Error("无法连接到本地服务器，请确认 server.py 仍在运行。");
    }
    var d;
    try { d = await r.json(); } catch (e) { throw new Error("服务器返回了无法解析的数据（HTTP " + r.status + "）"); }
    if (!r.ok) throw new Error((d && d.error) || ("HTTP " + r.status));
    return d;
  }

  function toast(msg, isErr) {
    var t = el('<div class="toast' + (isErr ? " err" : "") + '">' + esc(msg) + "</div>");
    $("#toasts").appendChild(t);
    setTimeout(function () { t.remove(); }, isErr ? 4000 : 2000);
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); } finally { ta.remove(); }
    return Promise.resolve();
  }

  function loadingHtml(text) {
    return '<div class="loading"><span class="spinner"></span>' + esc(text || "加载中…") + "</div>";
  }

  function errorPage(e) {
    app.innerHTML = '<div class="page"><div class="error-box">出错了：' + esc(e.message || e) + "</div></div>";
  }

  function diffClass(d) {
    return d === "简单" ? "diff-easy" : d === "中等" ? "diff-mid" : d === "困难" ? "diff-hard" : "";
  }

  var VERDICT = {
    AC: { cn: "通过", cls: "v-ac" },
    WA: { cn: "答案错误", cls: "v-wa" },
    CE: { cn: "编译错误", cls: "v-ce" },
    RE: { cn: "运行错误", cls: "v-re" },
    TLE: { cn: "超出时间限制", cls: "v-tle" },
    OLE: { cn: "输出超限", cls: "v-tle" },
    SE: { cn: "系统错误", cls: "v-se" },
    DONE: { cn: "运行完成", cls: "v-done" },
  };

  function vinfo(v) { return VERDICT[v] || { cn: v || "?", cls: "v-se" }; }
  function vbadge(v, withEn) {
    var m = vinfo(v);
    return '<span class="verdict ' + m.cls + '">' + esc(withEn ? v + " · " + m.cn : m.cn) + "</span>";
  }

  // 给 Markdown 渲染出的代码块加上"复制""放入编辑器"按钮
  function enhanceMd(root, onUse) {
    $all(".codeblock", root).forEach(function (cb) {
      if (cb.querySelector(".cb-actions")) return;
      var bar = el('<div class="cb-actions"></div>');
      var copy = cb.querySelector(".copy-btn");
      if (onUse && cb.querySelector("code.lang-c")) {
        var use = el('<button class="use-btn" title="用这段代码替换编辑器中的代码">放入编辑器</button>');
        use.addEventListener("click", function () {
          onUse(cb.querySelector("code").textContent);
        });
        bar.appendChild(use);
      }
      if (copy) bar.appendChild(copy);
      cb.insertBefore(bar, cb.firstChild);
    });
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest(".copy-btn");
    if (!btn) return;
    var cb = btn.closest(".codeblock");
    var code = cb && cb.querySelector("code");
    if (!code) return;
    copyText(code.textContent).then(function () { toast("已复制到剪贴板"); }, function () { toast("复制失败", true); });
  });

  function modal(title, bodyHtml, footHtml) {
    var m = el(
      '<div class="modal-mask"><div class="modal">' +
      '<div class="modal-head"><b>' + title + '</b><span class="spacer"></span>' +
      '<button class="icon-btn modal-close" title="关闭">✕</button></div>' +
      '<div class="modal-body">' + bodyHtml + "</div>" +
      (footHtml ? '<div class="modal-foot">' + footHtml + "</div>" : "") +
      "</div></div>"
    );
    function close() {
      m.remove();
      document.removeEventListener("keydown", onKey);
    }
    function onKey(e) { if (e.key === "Escape") close(); }
    m.addEventListener("mousedown", function (e) { if (e.target === m) close(); });
    $(".modal-close", m).addEventListener("click", close);
    document.addEventListener("keydown", onKey);
    document.body.appendChild(m);
    return { el: m, close: close };
  }

  // ------------------------------------------------------------ 判题结果渲染
  function normLines(s) {
    var lines = String(s || "").replace(/\r\n?/g, "\n").split("\n").map(function (l) { return l.replace(/\s+$/, ""); });
    while (lines.length && lines[lines.length - 1] === "") lines.pop();
    return lines;
  }

  function ioBlock(label, text, opts) {
    opts = opts || {};
    var html = '<div class="io-label">' + esc(label) + "</div>";
    if (text == null || text === "") {
      return html + '<pre class="io empty-out">（空）</pre>';
    }
    if (opts.compare) {
      var mine = normLines(text), other = normLines(opts.compare);
      var body = mine.map(function (l, i) {
        var cls = l === other[i] ? "" : opts.mark || "bad";
        return '<span class="ln ' + cls + '">' + esc(l) + "</span>";
      }).join("");
      return html + '<pre class="io">' + body + "</pre>";
    }
    return html + '<pre class="io' + (opts.err ? " err" : "") + '">' + esc(text) + "</pre>";
  }

  // 编译信息：把 solution.c:行:列 变成可点击链接，高亮 error / warning
  function compileHtml(text, clickable) {
    return esc(text)
      .replace(/solution\.c:(\d+)(?::(\d+))?/g, function (m, ln) {
        return clickable ? '<span class="errline" data-line="' + ln + '">' + m + "</span>" : m;
      })
      .replace(/\b(error|错误)(:|：)/g, '<span class="errword">$1$2</span>')
      .replace(/\b(warning|警告)(:|：)/g, '<span class="warnword">$1$2</span>');
  }

  function caseDetail(c) {
    var html = "";
    if (c.hint) html += '<div class="note">💡 ' + esc(c.hint) + "</div>";
    html += ioBlock("输入", c.input);
    var wa = c.status === "WA";
    if (c.expected != null) {
      html += ioBlock("你的输出", c.output, wa ? { compare: c.expected, mark: "bad" } : null);
      html += ioBlock("预期输出", c.expected, wa ? { compare: c.output, mark: "good" } : null);
    } else {
      html += ioBlock("输出", c.output);
    }
    if (c.stderr) html += ioBlock("标准错误 (stderr)", c.stderr, { err: true });
    return html;
  }

  function warningsHtml(r, clickable) {
    if (!r.warnings) return "";
    return '<details class="warn-box"><summary>⚠️ 编译器给出了警告（不影响结果，但值得一看）</summary>' +
      '<pre class="io">' + compileHtml(r.warnings, clickable) + "</pre></details>";
  }

  /* 把 judge.py 返回的结果渲染进 container。mode = "run" | "submit"
     opts.onLine(n)：点击编译错误行号时回调 */
  function renderResult(container, r, mode, opts) {
    opts = opts || {};
    var clickable = !!opts.onLine;
    var v = r.verdict;
    var html = '<div class="result-head">' + vbadge(v, true);
    if (mode === "submit" && r.total) html += '<span class="sub">通过测试点 ' + (r.passed || 0) + " / " + r.total + "</span>";
    if (mode === "submit" && r.time_ms != null && v !== "CE") html += '<span class="sub">最大耗时 ' + r.time_ms + " ms</span>";
    if (r.time_limit_ms) html += '<span class="sub">时间限制 ' + r.time_limit_ms + " ms</span>";
    html += "</div>";

    if (v === "CE") {
      if (r.hints && r.hints.length) {
        html += '<div class="note"><b>💡 可能的原因：</b><ul>' +
          r.hints.map(function (h) { return "<li>" + esc(h) + "</li>"; }).join("") + "</ul></div>";
      }
      html += '<div class="io-label">编译器输出' + (clickable ? "（点击蓝色的 solution.c:行号 可跳转）" : "") + "</div>" +
        '<pre class="io">' + compileHtml(r.compile_error || "", clickable) + "</pre>";
      container.innerHTML = html;
    } else if (v === "SE") {
      html += '<div class="error-box">' + esc(r.message || "未知错误") + "</div>";
      container.innerHTML = html;
    } else if (mode === "run") {
      var cases = r.cases || [];
      html += '<div class="chips">' + cases.map(function (c, i) {
        return '<button class="chip" data-i="' + i + '"><span class="dot ' + vinfo(c.status).cls + '"></span>' +
          esc(c.name) + "</button>";
      }).join("") + "</div><div class=\"case-detail\"></div>" + warningsHtml(r, clickable);
      container.innerHTML = html;
      var detail = $(".case-detail", container);
      var show = function (i) {
        $all(".chip", container).forEach(function (b) { b.classList.toggle("active", +b.dataset.i === i); });
        var c = cases[i];
        if (!c) { detail.innerHTML = ""; return; }
        detail.innerHTML = '<div class="io-label">' + vbadge(c.status) + " · 耗时 " + (c.time_ms != null ? c.time_ms : "?") + " ms</div>" + caseDetail(c);
      };
      $all(".chip", container).forEach(function (b) {
        b.addEventListener("click", function () { show(+b.dataset.i); });
      });
      var firstBad = cases.findIndex(function (c) { return c.status !== "AC" && c.status !== "DONE"; });
      show(firstBad >= 0 ? firstBad : 0);
    } else {
      if (v === "AC") {
        html += '<div class="note ok celebrate">🎉 恭喜！全部 ' + (r.total || 0) + " 个测试点都通过了。" +
          (opts.afterAc || "") + "</div>";
      } else if (r.failed_case) {
        var fc = r.failed_case;
        html += '<div class="note info">在第 <b>' + fc.index + "</b> 个测试点（共 " + r.total + " 个）出错，下面是该测试点的数据：</div>";
        html += caseDetail({ status: v, input: fc.input, expected: fc.expected, output: fc.output, stderr: fc.stderr, hint: fc.hint });
      }
      html += warningsHtml(r, clickable);
      container.innerHTML = html;
    }

    if (clickable) {
      $all(".errline", container).forEach(function (s) {
        s.addEventListener("click", function () { opts.onLine(+s.dataset.line); });
      });
    }
  }

  // ------------------------------------------------------------ 提交详情弹窗
  async function showSubmission(id, onLoadCode) {
    var m = modal("提交 #" + esc(id), loadingHtml());
    var d;
    try { d = await api("submissions/" + id); } catch (e) {
      $(".modal-body", m.el).innerHTML = '<div class="error-box">' + esc(e.message) + "</div>";
      return;
    }
    var body = $(".modal-body", m.el);
    body.innerHTML =
      '<div class="prob-meta">' +
      '<a href="#/problem/' + d.problem_id + '">题目 ' + d.problem_id + "</a>" +
      "<span>" + esc(d.created_at) + "</span><span>代码 " + d.code_len + " 字节</span></div>" +
      '<div class="sub-result"></div>' +
      '<div class="io-label" style="margin-top:14px">提交的代码</div>' +
      '<pre class="code-view"><code>' + MD.highlightC(d.code || "") + "</code></pre>";
    renderResult($(".sub-result", body), d.detail || { verdict: d.verdict }, "submit");
    var foot = el('<div class="modal-foot"></div>');
    var copyBtn = el('<button class="btn">复制代码</button>');
    copyBtn.addEventListener("click", function () { copyText(d.code).then(function () { toast("已复制"); }); });
    foot.appendChild(copyBtn);
    if (onLoadCode) {
      var loadBtn = el('<button class="btn primary">载入到编辑器</button>');
      loadBtn.addEventListener("click", function () { onLoadCode(d.code); m.close(); });
      foot.appendChild(loadBtn);
    }
    $(".modal", m.el).appendChild(foot);
  }

  function submissionsTable(rows, showTitle) {
    if (!rows.length) return '<div class="empty">还没有提交记录</div>';
    return '<table class="tbl"><thead><tr><th>#</th>' + (showTitle ? "<th>题目</th>" : "") +
      '<th>结果</th><th class="num">测试点</th><th class="num">耗时</th><th class="num">代码长度</th><th>提交时间</th></tr></thead><tbody>' +
      rows.map(function (r) {
        return '<tr data-id="' + r.id + '"><td class="muted">' + r.id + "</td>" +
          (showTitle ? '<td><a href="#/problem/' + r.problem_id + '" class="no-row">' + r.problem_id + ". " + esc(r.title) + "</a></td>" : "") +
          "<td>" + vbadge(r.verdict) + "</td>" +
          '<td class="num">' + (r.total ? (r.passed || 0) + "/" + r.total : "-") + "</td>" +
          '<td class="num">' + (r.time_ms != null && r.verdict !== "CE" ? r.time_ms + " ms" : "-") + "</td>" +
          '<td class="num">' + (r.code_len != null ? r.code_len + " B" : "-") + "</td>" +
          '<td class="muted">' + esc(r.created_at) + "</td></tr>";
      }).join("") + "</tbody></table>";
  }

  function bindSubmissionRows(root, onLoadCode) {
    $all("tbody tr[data-id]", root).forEach(function (tr) {
      tr.addEventListener("click", function (e) {
        if (e.target.closest("a.no-row")) return;
        showSubmission(tr.dataset.id, onLoadCode);
      });
    });
  }

  // ------------------------------------------------------------ 路由
  var routeSeq = 0;
  var cleanup = null;

  function setNav(name) {
    $all(".nav a").forEach(function (a) { a.classList.toggle("active", a.dataset.nav === name); });
  }

  function route() {
    if (cleanup) {
      try { cleanup(); } catch (e) { /* ignore */ }
      cleanup = null;
    }
    $all(".modal-mask").forEach(function (m) { m.remove(); });
    var seq = ++routeSeq;
    var alive = function () { return seq === routeSeq; };
    var parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
    var page = parts[0] || "problems";
    document.body.classList.toggle("page-problem", page === "problem");
    setNav(page === "problem" ? "problems" : page);
    window.scrollTo(0, 0);

    var p;
    if (page === "problems") p = pageList(alive);
    else if (page === "problem" && parts[1]) p = pageProblem(parts[1], alive);
    else if (page === "submissions") p = pageSubmissions(alive);
    else if (page === "stats") p = pageStats(alive);
    else if (page === "guide") p = pageGuide(alive);
    else {
      app.innerHTML = '<div class="page"><div class="empty">页面不存在，<a href="#/">返回题库</a></div></div>';
      return;
    }
    p.catch(function (e) { if (alive()) errorPage(e); });
  }

  // ------------------------------------------------------------ 题库
  var PAGE_SIZE = 50;
  var LISTS = [
    { id: "", name: "全部题目", tip: "题库中的所有题目" },
    { id: "hot100", name: "🔥 力扣 Hot 100", tip: "力扣「热题 100」，面试最高频" },
    { id: "embedded", name: "🔧 嵌入式 C", tip: "位运算、内存、指针、字节序、环形缓冲区等嵌入式面试常考题" },
    { id: "fav", name: "⭐ 我的收藏", tip: "在做题页或列表中点 ☆ 收藏的题" },
    { id: "wrong", name: "📕 错题本", tip: "提交过但还没有通过的题" },
  ];

  function inList(p, l) { return (p.lists || []).indexOf(l) >= 0; }

  /* 每天固定推荐一道没做过的题（同一天刷新不变），优先 Hot 100 */
  function dailyPick(probs) {
    var todo = probs.filter(function (p) { return p.status !== "ac"; });
    var hot = todo.filter(function (p) { return inList(p, "hot100"); });
    var pool = hot.length ? hot : todo;
    if (!pool.length) return null;
    var d = new Date(), seed = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
    return pool[(seed * 2654435761 >>> 0) % pool.length];
  }

  function setFavorite(id, on) {
    return api("problems/" + id + "/favorite", { favorite: on });
  }

  function currentList() {
    var l = store.get("listFilter", {}).list;
    return l === "hot100" || l === "embedded" ? l : "";
  }

  async function pageList(alive) {
    document.title = "题库 - C 刷题 OJ";
    app.innerHTML = '<div class="page">' + loadingHtml() + "</div>";
    var probs = await api("problems");
    if (!alive()) return;

    var tags = [];
    probs.forEach(function (p) { (p.tags || []).forEach(function (t) { if (tags.indexOf(t) < 0) tags.push(t); }); });
    var solved = probs.filter(function (p) { return p.status === "ac"; }).length;
    var byDiff = {};
    probs.forEach(function (p) {
      var b = byDiff[p.difficulty] = byDiff[p.difficulty] || { total: 0, solved: 0 };
      b.total++;
      if (p.status === "ac") b.solved++;
    });

    var f = store.get("listFilter", { q: "", diff: "", status: "", tag: "", list: "", page: 1 });
    var pick = dailyPick(probs);
    var daily = pick ? '<div class="card daily"><span class="lbl">📅 今日推荐</span>' +
      '<a href="#/problem/' + pick.id + '">' + pick.id + ". " + esc(pick.title) + "</a>" +
      '<span class="diff ' + diffClass(pick.difficulty) + '">' + esc(pick.difficulty) + "</span>" +
      '<span class="spacer"></span><button class="btn small" id="btn-random" title="从当前筛选结果里随机挑一道没做过的题">🎲 随机一题</button></div>' : "";
    var summary = '<div class="summary"><div class="card"><div class="lbl">已解决</div><div class="big">' + solved +
      ' <span class="muted" style="font-size:14px">/ ' + probs.length + '</span></div><div class="bar"><i style="width:' +
      (probs.length ? solved / probs.length * 100 : 0) + '%"></i></div></div>' +
      ["简单", "中等", "困难"].filter(function (d) { return byDiff[d]; }).map(function (d) {
        var b = byDiff[d];
        return '<div class="card"><div class="lbl ' + diffClass(d) + '">' + d + '</div><div class="big">' + b.solved +
          ' <span class="muted" style="font-size:14px">/ ' + b.total + "</span></div></div>";
      }).join("") + "</div>";

    var counts = {
      "": probs.length,
      hot100: probs.filter(function (p) { return inList(p, "hot100"); }).length,
      embedded: probs.filter(function (p) { return inList(p, "embedded"); }).length,
      fav: probs.filter(function (p) { return p.favorite; }).length,
      wrong: probs.filter(function (p) { return p.status === "tried"; }).length,
    };
    app.innerHTML = '<div class="page">' + summary + daily +
      '<div class="card"><div class="tabs list-tabs" id="list-tabs">' + LISTS.map(function (l) {
        return '<button data-list="' + l.id + '" title="' + esc(l.tip) + '">' + l.name +
          ' <span class="muted">' + counts[l.id] + "</span></button>";
      }).join("") + "</div>" +
      '<div class="filters">' +
      '<input type="search" id="f-q" placeholder="搜索题号或题目名…">' +
      '<select id="f-diff"><option value="">全部难度</option><option>简单</option><option>中等</option><option>困难</option></select>' +
      '<select id="f-status"><option value="">全部状态</option><option value="ac">已解决</option><option value="tried">尝试过</option><option value="todo">未开始</option></select>' +
      '<select id="f-tag"><option value="">全部标签</option>' + tags.map(function (t) { return "<option>" + esc(t) + "</option>"; }).join("") + "</select>" +
      '</div><div id="plist"></div><div class="pager" id="pager"></div></div></div>';

    var ids = { q: "#f-q", diff: "#f-diff", status: "#f-status", tag: "#f-tag" };
    Object.keys(ids).forEach(function (k) {
      var input = $(ids[k]);
      input.value = f[k] || "";
      if (input.value !== (f[k] || "")) { input.value = ""; f[k] = ""; }
      input.addEventListener("input", function () { f[k] = input.value; f.page = 1; store.set("listFilter", f); draw(); });
    });
    if (!LISTS.some(function (l) { return l.id === (f.list || ""); })) f.list = "";
    $all("#list-tabs button").forEach(function (b) {
      b.addEventListener("click", function () { f.list = b.dataset.list; f.page = 1; store.set("listFilter", f); draw(); });
    });

    function filtered() {
      var q = (f.q || "").trim().toLowerCase();
      return probs.filter(function (p) {
        if (f.list === "fav" && !p.favorite) return false;
        if (f.list === "wrong" && p.status !== "tried") return false;
        if ((f.list === "hot100" || f.list === "embedded") && !inList(p, f.list)) return false;
        if (q && (String(p.id) + " " + p.title + " " + (p.slug || "")).toLowerCase().indexOf(q) < 0) return false;
        if (f.diff && p.difficulty !== f.diff) return false;
        if (f.status === "todo" && p.status) return false;
        if (f.status && f.status !== "todo" && p.status !== f.status) return false;
        if (f.tag && (p.tags || []).indexOf(f.tag) < 0) return false;
        return true;
      });
    }

    var btnRandom = $("#btn-random");
    if (btnRandom) btnRandom.addEventListener("click", function () {
      var pool = filtered().filter(function (p) { return p.status !== "ac"; });
      if (!pool.length) pool = filtered();
      if (!pool.length) { toast("当前筛选下没有题目", true); return; }
      location.hash = "#/problem/" + pool[Math.floor(Math.random() * pool.length)].id;
    });

    function draw() {
      $all("#list-tabs button").forEach(function (b) { b.classList.toggle("active", b.dataset.list === (f.list || "")); });
      var rows = filtered();
      var box = $("#plist"), pager = $("#pager");
      if (!rows.length) {
        box.innerHTML = '<div class="empty">' + (f.list === "fav" ? "还没有收藏题目，在做题页点 ☆ 即可收藏" :
          f.list === "wrong" ? "错题本是空的：提交过但还没通过的题会出现在这里" : "没有符合条件的题目") + "</div>";
        pager.innerHTML = "";
        return;
      }
      var pages = Math.ceil(rows.length / PAGE_SIZE);
      f.page = Math.max(1, Math.min(f.page || 1, pages));
      var shown = rows.slice((f.page - 1) * PAGE_SIZE, f.page * PAGE_SIZE);
      box.innerHTML = '<table class="tbl"><thead><tr><th class="st">状态</th><th class="st">收藏</th><th>题目</th><th>标签</th><th>难度</th><th class="num">通过率</th></tr></thead><tbody>' +
        shown.map(function (p) {
          var st = p.status === "ac" ? '<span class="st-ac" title="已解决">✔</span>' :
            p.status === "tried" ? '<span class="st-tried" title="尝试过">●</span>' : "";
          var rate = p.submit_count ? Math.round(p.ac_count / p.submit_count * 100) + "%" : "-";
          return '<tr data-id="' + p.id + '"><td class="st">' + st + "</td>" +
            '<td class="st"><button class="star' + (p.favorite ? " on" : "") + '" data-fav="' + p.id + '" title="收藏 / 取消收藏">' +
            (p.favorite ? "★" : "☆") + "</button></td>" +
            '<td><a href="#/problem/' + p.id + '">' + p.id + ". " + esc(p.title) + "</a>" +
            (inList(p, "hot100") ? ' <span class="badge-hot" title="力扣 Hot 100">HOT</span>' : "") +
            (p.has_note ? ' <span title="有笔记">📝</span>' : "") + "</td>" +
            "<td>" + (p.tags || []).map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("") + "</td>" +
            '<td><span class="diff ' + diffClass(p.difficulty) + '">' + esc(p.difficulty) + "</span></td>" +
            '<td class="num muted" title="' + (p.ac_count || 0) + " / " + (p.submit_count || 0) + '">' + rate + "</td></tr>";
        }).join("") + "</tbody></table>";
      $all("tbody tr", box).forEach(function (tr) {
        tr.addEventListener("click", function (e) {
          if (e.target.closest("a") || e.target.closest(".star")) return;
          location.hash = "#/problem/" + tr.dataset.id;
        });
      });
      $all(".star", box).forEach(function (s) {
        s.addEventListener("click", function () {
          var p = probs.find(function (x) { return String(x.id) === s.dataset.fav; });
          setFavorite(p.id, !p.favorite).then(function (r) {
            p.favorite = r.favorite;
            if (f.list === "fav") draw();
            else { s.classList.toggle("on", p.favorite); s.textContent = p.favorite ? "★" : "☆"; }
          }, function (e) { toast(e.message, true); });
        });
      });
      pager.innerHTML = pages <= 1 ? '<span class="muted">共 ' + rows.length + " 题</span>" :
        '<button class="btn small" data-pg="' + (f.page - 1) + '"' + (f.page <= 1 ? " disabled" : "") + ">‹ 上一页</button>" +
        '<span class="muted">第 ' + f.page + " / " + pages + " 页 · 共 " + rows.length + " 题</span>" +
        '<button class="btn small" data-pg="' + (f.page + 1) + '"' + (f.page >= pages ? " disabled" : "") + ">下一页 ›</button>";
      $all("[data-pg]", pager).forEach(function (b) {
        b.addEventListener("click", function () {
          f.page = +b.dataset.pg;
          store.set("listFilter", f);
          draw();
          window.scrollTo(0, $("#list-tabs").getBoundingClientRect().top + window.scrollY - 70);
        });
      });
    }
    draw();
  }

  // ------------------------------------------------------------ 做题页
  async function pageProblem(id, alive) {
    app.innerHTML = loadingHtml();
    var ctxList = currentList();
    var p = await api("problems/" + encodeURIComponent(id) + (ctxList ? "?list=" + ctxList : ""));
    if (!alive()) return;
    document.title = p.id + ". " + p.title + " - C 刷题 OJ";

    var leftW = store.get("leftWidth", 45);
    var samples = p.samples || [];
    app.innerHTML =
      '<div class="workspace">' +
      '<section class="pane pane-left" style="width:' + leftW + '%">' +
      '<div class="tabs" id="ltabs">' +
      '<button data-tab="desc" class="active">📄 题目描述</button>' +
      '<button data-tab="sol">💡 题解</button>' +
      '<button data-tab="subs">🕘 提交记录</button>' +
      '<button data-tab="note">📝 笔记</button></div>' +
      '<div class="pane-body" id="lbody">' +
      '<div class="tabpane" data-pane="desc"></div>' +
      '<div class="tabpane hidden" data-pane="sol"></div>' +
      '<div class="tabpane hidden" data-pane="subs"></div>' +
      '<div class="tabpane hidden" data-pane="note"></div></div>' +
      '<div class="pane-foot">' +
      (p.prev != null ? '<a class="btn small" href="#/problem/' + p.prev + '">‹ 上一题</a>' : '<button class="btn small" disabled>‹ 上一题</button>') +
      '<a class="btn small" href="#/">' + (ctxList === "hot100" ? "Hot 100" : ctxList === "embedded" ? "嵌入式题单" : "题库") + "</a>" +
      (p.next != null ? '<a class="btn small" href="#/problem/' + p.next + '">下一题 ›</a>' : '<button class="btn small" disabled>下一题 ›</button>') +
      '<span class="spacer"></span>' +
      (p.leetcode ? '<a class="btn small" href="' + esc(p.leetcode) + '" target="_blank" rel="noopener">力扣原题 ↗</a>' : "") +
      "</div></section>" +
      '<div class="splitter" id="splitter" title="拖动调整宽度"></div>' +
      '<section class="pane pane-right">' +
      '<div class="toolbar"><span class="lang">C</span><span class="muted">gcc · C11</span>' +
      '<span class="saved" id="saved"></span><span class="spacer"></span>' +
      '<button class="btn small" id="font-dec" title="缩小字号">A−</button>' +
      '<button class="btn small" id="font-inc" title="放大字号">A+</button>' +
      '<button class="btn small" id="btn-export" title="把当前代码下载为 .c 文件">⤓ 导出</button>' +
      '<button class="btn small" id="btn-reset" title="恢复为初始模板">↺ 重置</button></div>' +
      '<div class="editor-wrap"><div id="editor"></div></div>' +
      '<div class="console" id="console">' +
      '<div class="console-head"><div class="tabs small">' +
      '<button data-ctab="case" class="active">测试用例</button>' +
      '<button data-ctab="result">运行结果</button></div>' +
      '<span class="spacer"></span>' +
      '<button class="icon-btn" id="btn-fold" title="折叠 / 展开">▾</button>' +
      '<button class="btn small" id="btn-run" title="Ctrl + Enter">▶ 运行</button>' +
      '<button class="btn small green" id="btn-submit" title="Ctrl + Shift + Enter">⬆ 提交</button></div>' +
      '<div class="console-body">' +
      '<div data-cpane="case"></div>' +
      '<div data-cpane="result" class="hidden"><div class="muted">点击「运行」测试样例，或「提交」进行完整评测。</div></div>' +
      "</div></div></section></div>";

    var paneDesc = $('[data-pane="desc"]'), paneSol = $('[data-pane="sol"]'), paneSubs = $('[data-pane="subs"]');
    var resultPane = $('[data-cpane="result"]'), casePane = $('[data-cpane="case"]');

    // ---------------- 编辑器
    var codeKey = "code." + p.id;
    var saveTimer = null;
    var savedEl = $("#saved");
    var ed = new CodeEditor($("#editor"), {
      onChange: function (v) {
        clearTimeout(saveTimer);
        savedEl.textContent = "";
        saveTimer = setTimeout(function () {
          store.set(codeKey, v);
          savedEl.textContent = "已自动保存";
        }, 400);
      },
    });
    var saved = store.get(codeKey, null);
    ed.setValue(saved != null ? saved : p.template);
    if (saved != null) savedEl.textContent = "已恢复上次的代码";

    var fontSize = store.get("fontSize", 14);
    function applyFont() { $("#editor").style.setProperty("--ed-font", fontSize + "px"); }
    applyFont();
    $("#font-dec").addEventListener("click", function () { fontSize = Math.max(11, fontSize - 1); store.set("fontSize", fontSize); applyFont(); });
    $("#font-inc").addEventListener("click", function () { fontSize = Math.min(24, fontSize + 1); store.set("fontSize", fontSize); applyFont(); });

    function replaceCode(code, msg) {
      ed.setValue(code);
      store.set(codeKey, code);
      savedEl.textContent = msg || "";
      ed.focus();
    }
    $("#btn-export").addEventListener("click", function () {
      var blob = new Blob(["/* " + p.id + ". " + p.title + (p.leetcode ? "  " + p.leetcode : "") + " */\n" + ed.getValue()],
        { type: "text/x-csrc;charset=utf-8" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = String(p.id).padStart(4, "0") + "-" + (p.slug || "solution") + ".c";
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
    $("#btn-reset").addEventListener("click", function () {
      if (!confirm("确定要把代码恢复为初始模板吗？当前代码将丢失。")) return;
      replaceCode(p.template, "已重置");
    });

    // ---------------- 左侧标签页
    var solLoaded = false, subsLoaded = false;
    function showLeft(tab) {
      $all("#ltabs button").forEach(function (b) { b.classList.toggle("active", b.dataset.tab === tab); });
      $all("#lbody .tabpane").forEach(function (x) { x.classList.toggle("hidden", x.dataset.pane !== tab); });
      $("#lbody").scrollTop = 0;
      if (tab === "sol" && !solLoaded) loadSolution();
      if (tab === "subs" && !subsLoaded) loadSubs();
      if (tab === "note") $("#note-input").focus();
    }
    $all("#ltabs button").forEach(function (b) {
      b.addEventListener("click", function () { showLeft(b.dataset.tab); });
    });

    function renderDesc() {
      var html = '<div class="prob-head"><h1>' + p.id + ". " + esc(p.title) +
        ' <button class="star big' + (p.favorite ? " on" : "") + '" id="btn-fav" title="收藏 / 取消收藏">' + (p.favorite ? "★" : "☆") + "</button></h1>" +
        '<div class="prob-meta"><span class="diff ' + diffClass(p.difficulty) + '">' + esc(p.difficulty) + "</span>" +
        ((p.lists || []).indexOf("hot100") >= 0 ? '<span class="badge-hot">HOT 100</span>' : "") +
        ((p.lists || []).indexOf("embedded") >= 0 ? '<span class="tag">嵌入式</span>' : "") +
        (p.status === "ac" ? '<span class="solved-badge">✔ 已解决</span>' : p.status === "tried" ? '<span class="st-tried">● 尝试过</span>' : "") +
        "<span>时间限制 " + p.time_limit_ms + " ms</span>" +
        (p.tags || []).map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("") +
        "</div></div>" +
        '<div class="md">' + MD.render(p.description || "") + "</div>";
      var hints = p.hints || [];
      if (hints.length) {
        html += '<div class="hints"><h3>💡 提示</h3><div id="hint-list"></div>' +
          '<button class="btn small" id="btn-hint"></button></div>';
      }
      paneDesc.innerHTML = html;
      enhanceMd(paneDesc);
      $("#btn-fav").addEventListener("click", function () {
        setFavorite(p.id, !p.favorite).then(function (r) {
          p.favorite = r.favorite;
          renderDesc();
          toast(p.favorite ? "已收藏" : "已取消收藏");
        }, function (e) { toast(e.message, true); });
      });
      if (!hints.length) return;
      var hintKey = "hints." + p.id;
      var shown = Math.min(store.get(hintKey, 0), hints.length);
      var list = $("#hint-list"), btn = $("#btn-hint");
      function drawHints() {
        list.innerHTML = hints.slice(0, shown).map(function (h, i) {
          return '<div class="hint-item"><b>提示 ' + (i + 1) + "</b>" + esc(h) + "</div>";
        }).join("");
        if (shown >= hints.length) btn.classList.add("hidden");
        else btn.textContent = shown === 0 ? "卡住了？看第 1 条提示（共 " + hints.length + " 条）" : "再看一条提示（" + (shown + 1) + "/" + hints.length + "）";
      }
      btn.addEventListener("click", function () { shown++; store.set(hintKey, shown); drawHints(); });
      drawHints();
    }
    renderDesc();

    // ---------------- 笔记（保存在服务器的数据库里）
    var paneNote = $('[data-pane="note"]');
    paneNote.innerHTML = '<div class="note-head"><b>我的笔记</b><span class="muted">支持 Markdown，自动保存</span>' +
      '<span class="spacer"></span><span class="saved" id="note-saved"></span>' +
      '<button class="btn small" id="note-preview">预览</button></div>' +
      '<textarea class="input note-input" id="note-input" spellcheck="false" placeholder="记录思路、踩过的坑、复杂度分析……">' +
      esc(p.note || "") + "</textarea>" +
      '<div class="md note-view hidden" id="note-view"></div>';
    var noteInput = $("#note-input"), noteSaved = $("#note-saved"), noteView = $("#note-view");
    var noteTimer = null, noteDirty = false;
    function saveNote() {
      clearTimeout(noteTimer);
      if (!noteDirty) return Promise.resolve();
      noteDirty = false;
      var text = noteInput.value;
      return api("problems/" + p.id + "/note", { note: text }).then(function () {
        p.note = text;
        noteSaved.textContent = "已保存";
      }, function (e) {
        noteDirty = true;
        noteSaved.textContent = "保存失败：" + e.message;
      });
    }
    noteInput.addEventListener("input", function () {
      noteDirty = true;
      noteSaved.textContent = "";
      clearTimeout(noteTimer);
      noteTimer = setTimeout(saveNote, 800);
    });
    $("#note-preview").addEventListener("click", function () {
      var preview = noteView.classList.contains("hidden");
      noteView.innerHTML = preview ? (noteInput.value.trim() ? MD.render(noteInput.value) : '<div class="muted">（空）</div>') : "";
      noteView.classList.toggle("hidden", !preview);
      noteInput.classList.toggle("hidden", preview);
      this.textContent = preview ? "编辑" : "预览";
    });

    async function loadSolution(force) {
      var openKey = "solOpen." + p.id;
      if (!force && p.status !== "ac" && !store.get(openKey, false)) {
        paneSol.innerHTML = '<div class="gate"><div class="icon">🤔</div><h3>先自己试一试？</h3>' +
          "<p>独立思考是进步最快的方式。卡住时可以先看「题目描述」底部的提示。<br>通过本题后，题解会自动解锁。</p>" +
          '<button class="btn primary" id="btn-open-sol">我已经想过了，查看题解</button></div>';
        $("#btn-open-sol").addEventListener("click", function () { store.set(openKey, true); loadSolution(true); });
        return;
      }
      solLoaded = true;
      paneSol.innerHTML = loadingHtml();
      try {
        var d = await api("problems/" + p.id + "/explanation");
        if (!alive()) return;
        if (!d.content || !d.content.trim()) {
          paneSol.innerHTML = '<div class="empty">这道题暂时还没有题解</div>';
          return;
        }
        paneSol.innerHTML = '<div class="md">' + MD.render(d.content) + "</div>";
        enhanceMd(paneSol, function (code) {
          if (!confirm("用题解中的这段代码替换编辑器里的代码吗？（建议先自己写一遍）")) return;
          replaceCode(code, "已放入题解代码");
        });
      } catch (e) {
        solLoaded = false;
        paneSol.innerHTML = '<div class="error-box">' + esc(e.message) + "</div>";
      }
    }

    async function loadSubs() {
      subsLoaded = true;
      paneSubs.innerHTML = loadingHtml();
      try {
        var rows = await api("submissions?problem_id=" + p.id + "&limit=100");
        if (!alive()) return;
        paneSubs.innerHTML = submissionsTable(rows, false);
        bindSubmissionRows(paneSubs, function (code) { replaceCode(code, "已载入历史代码"); });
      } catch (e) {
        subsLoaded = false;
        paneSubs.innerHTML = '<div class="error-box">' + esc(e.message) + "</div>";
      }
    }

    // ---------------- 测试用例面板
    var customKey = "custom." + p.id;
    var useCustomKey = "useCustom." + p.id;
    var custom = store.get(customKey, samples.length ? samples[0].input.replace(/\s+$/, "") : "");
    var useCustom = store.get(useCustomKey, false);
    var curCase = 0;

    function drawCases() {
      var chips = samples.map(function (s, i) {
        return '<button class="chip' + (curCase === i ? " active" : "") + '" data-c="' + i + '">样例 ' + (i + 1) + "</button>";
      }).join("") + '<button class="chip' + (curCase === "custom" ? " active" : "") + '" data-c="custom">✎ 自定义输入' + (useCustom ? " ✓" : "") + "</button>";
      var body;
      if (curCase === "custom") {
        body = '<label class="custom-row"><input type="checkbox" id="use-custom"' + (useCustom ? " checked" : "") +
          "> 点「运行」时，除了样例外再跑一遍下面的自定义输入</label>" +
          '<textarea class="input" id="custom-input" rows="5" spellcheck="false" placeholder="按题目描述末尾「自定义输入格式」填写">' +
          esc(custom) + "</textarea>";
      } else if (samples[curCase]) {
        body = ioBlock("输入", samples[curCase].input) + ioBlock("预期输出", samples[curCase].output);
      } else {
        body = '<div class="muted">这道题没有公开样例。</div>';
      }
      casePane.innerHTML = '<div class="chips">' + chips + "</div>" + body;
      $all(".chip", casePane).forEach(function (b) {
        b.addEventListener("click", function () {
          curCase = b.dataset.c === "custom" ? "custom" : +b.dataset.c;
          drawCases();
        });
      });
      var cb = $("#use-custom"), ta = $("#custom-input");
      if (cb) cb.addEventListener("change", function () {
        useCustom = cb.checked;
        store.set(useCustomKey, useCustom);
        var chip = $('.chip[data-c="custom"]', casePane);
        if (chip) chip.textContent = "✎ 自定义输入" + (useCustom ? " ✓" : "");
      });
      if (ta) ta.addEventListener("input", function () { custom = ta.value; store.set(customKey, custom); });
    }
    drawCases();

    // ---------------- 控制台 & 运行 / 提交
    var consoleEl = $("#console");
    function showConsole(tab) {
      consoleEl.classList.remove("collapsed");
      $("#btn-fold").textContent = "▾";
      $all("[data-ctab]").forEach(function (b) { b.classList.toggle("active", b.dataset.ctab === tab); });
      $all("[data-cpane]").forEach(function (x) { x.classList.toggle("hidden", x.dataset.cpane !== tab); });
    }
    $all("[data-ctab]").forEach(function (b) {
      b.addEventListener("click", function () { showConsole(b.dataset.ctab); });
    });
    $("#btn-fold").addEventListener("click", function () {
      var c = consoleEl.classList.toggle("collapsed");
      this.textContent = c ? "▴" : "▾";
    });

    var busy = false;
    var btnRun = $("#btn-run"), btnSubmit = $("#btn-submit");
    async function doJudge(mode) {
      if (busy) return;
      var code = ed.getValue();
      if (!code.trim()) { toast("代码是空的", true); return; }
      busy = true;
      btnRun.disabled = btnSubmit.disabled = true;
      store.set(codeKey, code);
      showConsole("result");
      resultPane.innerHTML = loadingHtml(mode === "submit" ? "正在编译并评测全部测试点…" : "正在编译并运行样例…");
      var body = { problem_id: p.id, code: code };
      if (mode === "run" && useCustom && custom.trim()) body.custom_input = custom;
      try {
        var r = await api(mode, body);
        if (!alive()) return;
        var afterAc = "";
        if (mode === "submit" && r.verdict === "AC") {
          var firstAc = p.status !== "ac";
          p.status = "ac";
          renderDesc();
          if (!solLoaded) {
            if (paneSol.classList.contains("hidden")) paneSol.innerHTML = "";
            else loadSolution();
          }
          afterAc = firstAc ? " 题解已解锁，去看看有没有更好的解法吧。" : "";
          if (p.next != null) afterAc += ' <a href="#/problem/' + p.next + '">下一题 ›</a>';
        } else if (mode === "submit" && !p.status) {
          p.status = "tried";
          renderDesc();
        }
        renderResult(resultPane, r, mode, { onLine: function (n) { ed.gotoLine(n); }, afterAc: afterAc });
        if (mode === "submit") {
          subsLoaded = false;
          if (!$('[data-pane="subs"]').classList.contains("hidden")) loadSubs();
        }
      } catch (e) {
        if (alive()) resultPane.innerHTML = '<div class="error-box">' + esc(e.message) + "</div>";
      } finally {
        busy = false;
        btnRun.disabled = btnSubmit.disabled = false;
      }
    }
    btnRun.addEventListener("click", function () { doJudge("run"); });
    btnSubmit.addEventListener("click", function () { doJudge("submit"); });

    function onKey(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        doJudge(e.shiftKey ? "submit" : "run");
      } else if ((e.ctrlKey || e.metaKey) && (e.key === "s" || e.key === "S")) {
        e.preventDefault();
        store.set(codeKey, ed.getValue());
        savedEl.textContent = "已保存";
        toast("代码已保存（平时也会自动保存）");
      }
    }
    document.addEventListener("keydown", onKey);

    // ---------------- 左右拖动分隔条
    var splitter = $("#splitter"), left = $(".pane-left"), ws = $(".workspace");
    function onDown(e) {
      e.preventDefault();
      splitter.classList.add("drag");
      document.body.classList.add("dragging");
      document.addEventListener("mousemove", onMove);
      document.addEventListener("mouseup", onUp);
    }
    function onMove(e) {
      var rect = ws.getBoundingClientRect();
      var pct = (e.clientX - rect.left) / rect.width * 100;
      leftW = Math.max(20, Math.min(75, pct));
      left.style.width = leftW + "%";
    }
    function onUp() {
      splitter.classList.remove("drag");
      document.body.classList.remove("dragging");
      document.removeEventListener("mousemove", onMove);
      document.removeEventListener("mouseup", onUp);
      store.set("leftWidth", Math.round(leftW * 10) / 10);
    }
    splitter.addEventListener("mousedown", onDown);

    cleanup = function () {
      clearTimeout(saveTimer);
      saveNote();
      store.set(codeKey, ed.getValue());
      document.removeEventListener("keydown", onKey);
      document.removeEventListener("mousemove", onMove);
      document.removeEventListener("mouseup", onUp);
      document.body.classList.remove("dragging");
    };
  }

  // ------------------------------------------------------------ 提交记录
  async function pageSubmissions(alive) {
    document.title = "提交记录 - C 刷题 OJ";
    app.innerHTML = '<div class="page">' + loadingHtml() + "</div>";
    var rows = await api("submissions?limit=300");
    if (!alive()) return;
    app.innerHTML = '<div class="page"><h2 class="page-title">提交记录</h2><div class="card">' +
      '<div class="filters"><select id="f-v"><option value="">全部结果</option>' +
      Object.keys(VERDICT).filter(function (k) { return k !== "DONE"; }).map(function (k) {
        return '<option value="' + k + '">' + k + " · " + VERDICT[k].cn + "</option>";
      }).join("") + '</select><span class="muted" id="sub-count" style="align-self:center"></span></div>' +
      '<div id="sublist"></div></div></div>';
    var sel = $("#f-v");
    function draw() {
      var list = rows.filter(function (r) { return !sel.value || r.verdict === sel.value; });
      $("#sub-count").textContent = "共 " + list.length + " 条";
      var box = $("#sublist");
      box.innerHTML = submissionsTable(list, true);
      bindSubmissionRows(box);
    }
    sel.addEventListener("change", draw);
    draw();
  }

  // ------------------------------------------------------------ 统计
  async function pageStats(alive) {
    document.title = "统计 - C 刷题 OJ";
    app.innerHTML = '<div class="page">' + loadingHtml() + "</div>";
    var s = await api("stats");
    if (!alive()) return;
    var rate = s.submissions ? Math.round(s.accepted / s.submissions * 100) : 0;
    var html = '<div class="page"><h2 class="page-title">学习统计</h2><div class="stat-grid">' +
      '<div class="card"><div class="lbl">已解决题目</div><div class="big">' + s.solved + ' <span class="muted" style="font-size:15px">/ ' + s.total + "</span></div></div>" +
      '<div class="card"><div class="lbl">总提交次数</div><div class="big">' + s.submissions + "</div></div>" +
      '<div class="card"><div class="lbl">提交通过率</div><div class="big">' + rate + "%</div></div>" +
      '<div class="card"><div class="lbl">活跃天数（近 30 天内有提交）</div><div class="big">' + (s.days || []).length + "</div></div></div>";

    html += '<div class="card card-pad"><h3 style="margin-top:0">按难度</h3>';
    var order = ["简单", "中等", "困难"];
    var keys = Object.keys(s.by_difficulty || {}).sort(function (a, b) {
      var x = order.indexOf(a), y = order.indexOf(b);
      return (x < 0 ? 9 : x) - (y < 0 ? 9 : y);
    });
    if (!keys.length) html += '<div class="muted">暂无题目</div>';
    keys.forEach(function (k) {
      var b = s.by_difficulty[k];
      html += '<div class="diff-row"><span class="name diff ' + diffClass(k) + '">' + esc(k) + "</span>" +
        '<div class="bar"><i style="width:' + (b.total ? b.solved / b.total * 100 : 0) + "%\"></i></div>" +
        '<span class="cnt">' + b.solved + " / " + b.total + "</span></div>";
    });
    html += "</div>";

    var lists = s.by_list || {};
    var listNames = { hot100: "🔥 Hot 100", embedded: "🔧 嵌入式 C" };
    var lkeys = Object.keys(listNames).filter(function (k) { return lists[k]; });
    if (lkeys.length) {
      html += '<div class="card card-pad"><h3 style="margin-top:0">题单进度</h3>';
      lkeys.forEach(function (k) {
        var b = lists[k];
        html += '<div class="diff-row"><span class="name">' + listNames[k] + "</span>" +
          '<div class="bar"><i style="width:' + (b.total ? b.solved / b.total * 100 : 0) + "%\"></i></div>" +
          '<span class="cnt">' + b.solved + " / " + b.total + "</span></div>";
      });
      html += "</div>";
    }

    html += '<div class="card card-pad"><h3 style="margin-top:0">每日提交</h3>';
    var days = (s.days || []).slice().reverse();
    if (!days.length) {
      html += '<div class="muted">还没有提交记录，去 <a href="#/">题库</a> 做第一道题吧！</div>';
    } else {
      var max = Math.max.apply(null, days.map(function (d) { return d.n; }));
      html += '<div class="days">' + days.map(function (d) {
        return '<div class="d" title="' + esc(d.d) + "：" + d.n + ' 次提交"><i style="height:' + (d.n / max * 100) + '%"></i><span>' +
          esc(d.d.slice(5)) + "</span></div>";
      }).join("") + "</div>";
    }
    html += "</div></div>";
    app.innerHTML = html;
  }

  // ------------------------------------------------------------ 新手指南
  async function pageGuide(alive) {
    document.title = "新手指南 - C 刷题 OJ";
    app.innerHTML = '<div class="page">' + loadingHtml() + "</div>";
    var d = await api("guide");
    if (!alive()) return;
    app.innerHTML = '<div class="page"><div class="card card-pad md">' +
      (d.content ? MD.render(d.content) : '<div class="empty">docs/GUIDE.md 不存在</div>') + "</div></div>";
    enhanceMd(app);
  }

  // ------------------------------------------------------------ 启动
  async function checkEnv() {
    var envEl = $("#env");
    try {
      var d = await api("env");
      if (d.gcc) {
        envEl.className = "env ok";
        envEl.textContent = d.gcc_version || "gcc 已就绪";
        envEl.title = d.gcc;
      } else {
        envEl.className = "env bad";
        envEl.textContent = "未找到 gcc";
        $("#env-banner").innerHTML = '<div class="banner"><b>未找到 gcc 编译器，暂时无法运行和提交代码。</b><br>' +
          "请安装 MinGW-w64 并把它的 bin 目录加入 PATH，或在项目根目录的 config.json 中写入 " +
          '<code>{"gcc": "C:\\\\mingw64\\\\bin\\\\gcc.exe"}</code>，然后重启 server.py。详见 <a href="#/guide">新手指南</a>。</div>';
      }
    } catch (e) {
      envEl.className = "env bad";
      envEl.textContent = "服务器未连接";
    }
  }

  $("#theme-btn").addEventListener("click", function () {
    var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", cur);
    store.set("theme", cur);
  });

  window.addEventListener("hashchange", route);
  window.addEventListener("beforeunload", function () { if (cleanup) cleanup(); });
  checkEnv();
  route();
})();
