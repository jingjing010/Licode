/* 轻量 Markdown 渲染 + C 语言语法高亮（无第三方依赖，离线可用） */
(function (global) {
  "use strict";

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // ------------------------------------------------------------ C 高亮
  var KEYWORDS = new Set(("auto break case const continue default do else enum extern for goto if inline " +
    "register restrict return sizeof static struct switch typedef union volatile while NULL true false").split(" "));
  var TYPES = new Set(("int char long short float double void bool unsigned signed size_t int64_t uint64_t " +
    "int32_t uint32_t uint8_t FILE").split(" "));
  var TOKEN = /(\/\/[^\n]*|\/\*[\s\S]*?(?:\*\/|$))|("(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?)|(^[ \t]*#[^\n]*)|(\b(?:0[xX][0-9a-fA-F]+|\d+\.?\d*(?:[eE][+-]?\d+)?)[uUlLfF]*\b)|([A-Za-z_]\w*)(\s*\()?|([\s\S])/gm;

  function highlightC(code) {
    var out = "";
    var m;
    TOKEN.lastIndex = 0;
    while ((m = TOKEN.exec(code)) !== null) {
      if (m[0] === "") { TOKEN.lastIndex++; continue; }
      if (m[1]) out += '<span class="tk-com">' + esc(m[1]) + "</span>";
      else if (m[2]) out += '<span class="tk-str">' + esc(m[2]) + "</span>";
      else if (m[3]) out += '<span class="tk-pre">' + esc(m[3]) + "</span>";
      else if (m[4]) out += '<span class="tk-num">' + esc(m[4]) + "</span>";
      else if (m[5]) {
        var w = m[5];
        var cls = KEYWORDS.has(w) ? "tk-kw" : TYPES.has(w) ? "tk-type" : m[6] ? "tk-fn" : null;
        out += cls ? '<span class="' + cls + '">' + w + "</span>" : w;
        if (m[6]) out += esc(m[6]);
      } else out += esc(m[7]);
    }
    return out;
  }

  // ------------------------------------------------------------ Markdown
  function inline(s) {
    var codes = [];
    s = s.replace(/`([^`]+)`/g, function (_, c) {
      codes.push("<code>" + esc(c) + "</code>");
      return "\u0000" + (codes.length - 1) + "\u0000";
    });
    s = esc(s);
    s = s.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img alt="$1" src="$2">');
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, "$1<em>$2</em>");
    s = s.replace(/~~([^~]+)~~/g, "<del>$1</del>");
    s = s.replace(/\u0000(\d+)\u0000/g, function (_, i) { return codes[+i]; });
    return s;
  }

  function splitRow(line) {
    line = line.trim().replace(/^\|/, "").replace(/\|$/, "");
    var cells = [], cur = "", inCode = false;
    for (var i = 0; i < line.length; i++) {
      var ch = line[i];
      if (ch === "`") inCode = !inCode;
      if (ch === "\\" && line[i + 1] === "|") { cur += "|"; i++; continue; }
      if (ch === "|" && !inCode) { cells.push(cur.trim()); cur = ""; continue; }
      cur += ch;
    }
    cells.push(cur.trim());
    return cells;
  }

  function renderList(lines, start) {
    // 支持多级（按缩进）有序/无序列表
    var i = start;
    var baseIndent = lines[i].match(/^\s*/)[0].length;
    var ordered = /^\s*\d+\.\s/.test(lines[i]);
    var html = ordered ? "<ol>" : "<ul>";
    while (i < lines.length) {
      var line = lines[i];
      var m = line.match(/^(\s*)([-*+]|\d+\.)\s+(.*)$/);
      if (!m) {
        // 列表项的续行
        if (line.trim() !== "" && /^\s+/.test(line) && html.endsWith("</li>")) {
          html = html.slice(0, -5) + "<br>" + inline(line.trim()) + "</li>";
          i++;
          continue;
        }
        break;
      }
      var indent = m[1].length;
      if (indent < baseIndent) break;
      if (indent > baseIndent) {
        var sub = renderList(lines, i);
        html = html.slice(0, -5) + sub.html + "</li>";
        i = sub.next;
        continue;
      }
      html += "<li>" + inline(m[3]) + "</li>";
      i++;
    }
    html += ordered ? "</ol>" : "</ul>";
    return { html: html, next: i };
  }

  function render(md) {
    var lines = md.replace(/\r\n/g, "\n").split("\n");
    var html = "";
    var i = 0;
    while (i < lines.length) {
      var line = lines[i];
      var fm = line.match(/^\s*(```+|~~~+)\s*([\w+-]*)/);
      if (fm) {
        var fence = fm[1], lang = fm[2].toLowerCase(), buf = [];
        i++;
        while (i < lines.length && lines[i].trim().indexOf(fence) !== 0) { buf.push(lines[i]); i++; }
        i++;
        var code = buf.join("\n");
        var body = (lang === "c" || lang === "cpp" || lang === "h") ? highlightC(code) : esc(code);
        html += '<div class="codeblock"><button class="copy-btn" title="复制代码">复制</button><pre><code class="lang-' +
          (lang || "text") + '">' + body + "</code></pre></div>";
        continue;
      }
      if (/^\s*$/.test(line)) { i++; continue; }
      var h = line.match(/^(#{1,6})\s+(.*)$/);
      if (h) { html += "<h" + h[1].length + ">" + inline(h[2]) + "</h" + h[1].length + ">"; i++; continue; }
      if (/^\s*(---+|\*\*\*+|___+)\s*$/.test(line)) { html += "<hr>"; i++; continue; }
      if (/^\s*>/.test(line)) {
        var q = [];
        while (i < lines.length && /^\s*>/.test(lines[i])) { q.push(lines[i].replace(/^\s*>\s?/, "")); i++; }
        var inner = render(q.join("\n"));
        var alert = inner.match(/^<p>\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]/);
        if (alert) {
          inner = inner.replace(/^<p>\[!\w+\](<br>)?/, "<p>");
          html += '<blockquote class="alert alert-' + alert[1].toLowerCase() + '">' + inner + "</blockquote>";
        } else html += "<blockquote>" + inner + "</blockquote>";
        continue;
      }
      if (/^\s*\|/.test(line) && i + 1 < lines.length && /^\s*\|?\s*:?-+/.test(lines[i + 1])) {
        var head = splitRow(line);
        var aligns = splitRow(lines[i + 1]).map(function (c) {
          return /^:-+:$/.test(c) ? "center" : /-+:$/.test(c) ? "right" : "";
        });
        i += 2;
        var t = '<div class="table-wrap"><table><thead><tr>';
        head.forEach(function (c, k) { t += "<th" + (aligns[k] ? ' style="text-align:' + aligns[k] + '"' : "") + ">" + inline(c) + "</th>"; });
        t += "</tr></thead><tbody>";
        while (i < lines.length && /^\s*\|/.test(lines[i])) {
          t += "<tr>";
          splitRow(lines[i]).forEach(function (c, k) { t += "<td" + (aligns[k] ? ' style="text-align:' + aligns[k] + '"' : "") + ">" + inline(c) + "</td>"; });
          t += "</tr>";
          i++;
        }
        html += t + "</tbody></table></div>";
        continue;
      }
      if (/^\s*([-*+]|\d+\.)\s+/.test(line)) {
        var r = renderList(lines, i);
        html += r.html;
        i = r.next;
        continue;
      }
      var para = [];
      while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#{1,6}\s|\s*```|\s*>|\s*\|)/.test(lines[i]) &&
             !/^\s*([-*+]|\d+\.)\s+/.test(lines[i]) && !/^\s*(---+|\*\*\*+)\s*$/.test(lines[i])) {
        para.push(inline(lines[i].trim()));
        i++;
      }
      html += "<p>" + para.join("<br>") + "</p>";
    }
    return html;
  }

  global.MD = { render: render, highlightC: highlightC, esc: esc };
})(window);
