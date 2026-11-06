/* 简易代码编辑器：textarea + 高亮层 + 行号，支持 Tab 缩进、自动缩进、括号补全 */
(function (global) {
  "use strict";

  function CodeEditor(root, opts) {
    opts = opts || {};
    this.root = root;
    root.classList.add("editor");
    root.innerHTML =
      '<div class="ed-gutter"><div class="ed-lines"></div></div>' +
      '<div class="ed-main"><pre class="ed-hl" aria-hidden="true"><code></code></pre>' +
      '<textarea class="ed-ta" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" wrap="off"></textarea></div>';
    this.ta = root.querySelector(".ed-ta");
    this.hl = root.querySelector(".ed-hl code");
    this.pre = root.querySelector(".ed-hl");
    this.lines = root.querySelector(".ed-lines");
    this.gutter = root.querySelector(".ed-gutter");
    this.onChange = opts.onChange || function () {};
    this.indent = "    ";
    var self = this;
    this.ta.addEventListener("input", function () { self.refresh(); self.onChange(self.getValue()); });
    this.ta.addEventListener("scroll", function () { self.syncScroll(); });
    this.ta.addEventListener("keydown", function (e) { self.onKey(e); });
    this.ta.addEventListener("click", function () { self.markLine(); });
    this.ta.addEventListener("keyup", function () { self.markLine(); });
  }

  CodeEditor.prototype.getValue = function () { return this.ta.value; };

  CodeEditor.prototype.setValue = function (v) {
    this.ta.value = v;
    this.refresh();
    this.ta.scrollTop = 0;
    this.syncScroll();
  };

  CodeEditor.prototype.focus = function () { this.ta.focus(); };

  CodeEditor.prototype.refresh = function () {
    var v = this.ta.value;
    this.hl.innerHTML = MD.highlightC(v) + "\n ";
    var n = v.split("\n").length;
    if (n !== this._n) {
      var s = "";
      for (var i = 1; i <= n; i++) s += "<div>" + i + "</div>";
      this.lines.innerHTML = s;
      this._n = n;
    }
    this.markLine();
  };

  CodeEditor.prototype.markLine = function () {
    var ln = this.ta.value.slice(0, this.ta.selectionStart).split("\n").length;
    if (ln === this._cur) return;
    var old = this.lines.children[this._cur - 1];
    if (old) old.classList.remove("cur");
    var nw = this.lines.children[ln - 1];
    if (nw) nw.classList.add("cur");
    this._cur = ln;
  };

  CodeEditor.prototype.syncScroll = function () {
    this.pre.scrollTop = this.ta.scrollTop;
    this.pre.scrollLeft = this.ta.scrollLeft;
    this.lines.style.transform = "translateY(" + -this.ta.scrollTop + "px)";
  };

  // 使用 insertText 以保留浏览器的撤销栈（Ctrl+Z）
  CodeEditor.prototype.insert = function (text) {
    this.ta.focus();
    if (!document.execCommand("insertText", false, text)) {
      var s = this.ta.selectionStart, e = this.ta.selectionEnd, v = this.ta.value;
      this.ta.value = v.slice(0, s) + text + v.slice(e);
      this.ta.selectionStart = this.ta.selectionEnd = s + text.length;
      this.ta.dispatchEvent(new Event("input"));
    }
  };

  CodeEditor.prototype.gotoLine = function (ln) {
    var lines = this.ta.value.split("\n");
    ln = Math.max(1, Math.min(ln, lines.length));
    var pos = 0;
    for (var i = 0; i < ln - 1; i++) pos += lines[i].length + 1;
    this.ta.focus();
    this.ta.setSelectionRange(pos, pos + lines[ln - 1].length);
    var lh = parseFloat(getComputedStyle(this.ta).lineHeight) || 20;
    this.ta.scrollTop = Math.max(0, (ln - 5) * lh);
    this.markLine();
  };

  var PAIRS = { "(": ")", "[": "]", "{": "}", '"': '"', "'": "'" };

  CodeEditor.prototype.onKey = function (e) {
    var ta = this.ta, v = ta.value, s = ta.selectionStart, en = ta.selectionEnd;
    var lineStart = v.lastIndexOf("\n", s - 1) + 1;
    var curLine = v.slice(lineStart, s);
    var indentNow = curLine.match(/^\s*/)[0];

    if (e.key === "Tab") {
      e.preventDefault();
      if (s !== en && v.slice(s, en).indexOf("\n") >= 0 || e.shiftKey) {
        // 多行缩进 / 反缩进
        var blockEnd = v.indexOf("\n", en - 1 < s ? s : en - 1);
        if (blockEnd < 0) blockEnd = v.length;
        var block = v.slice(lineStart, blockEnd);
        var nb = e.shiftKey
          ? block.replace(/^( {1,4}|\t)/gm, "")
          : block.replace(/^/gm, this.indent);
        ta.setSelectionRange(lineStart, blockEnd);
        this.insert(nb);
        ta.setSelectionRange(lineStart, lineStart + nb.length);
      } else {
        this.insert(this.indent);
      }
      return;
    }

    if (e.key === "Enter" && !e.ctrlKey && !e.metaKey) {
      e.preventDefault();
      var before = v[s - 1], after = v[s];
      var extra = /[{(\[]\s*$/.test(curLine) ? this.indent : "";
      if (before === "{" && after === "}" || before === "(" && after === ")" || before === "[" && after === "]") {
        this.insert("\n" + indentNow + this.indent + "\n" + indentNow);
        var p = s + 1 + indentNow.length + this.indent.length;
        ta.setSelectionRange(p, p);
      } else {
        this.insert("\n" + indentNow + extra);
      }
      return;
    }

    if (e.key === "}" && /^\s+$/.test(curLine) && s === en) {
      e.preventDefault();
      var ni = curLine.replace(/( {1,4}|\t)$/, "");
      ta.setSelectionRange(lineStart, s);
      this.insert(ni + "}");
      return;
    }

    if (PAIRS[e.key] && !e.ctrlKey && !e.metaKey) {
      var nextCh = v[s] || "";
      if ((e.key === '"' || e.key === "'") && nextCh === e.key && s === en) {
        e.preventDefault();
        ta.setSelectionRange(s + 1, s + 1);
        return;
      }
      if (s !== en || /[\s)\]};,]|^$/.test(nextCh)) {
        if ((e.key === '"' || e.key === "'") && /\w/.test(v[s - 1] || "")) return;
        e.preventDefault();
        var sel = v.slice(s, en);
        this.insert(e.key + sel + PAIRS[e.key]);
        ta.setSelectionRange(s + 1, s + 1 + sel.length);
        return;
      }
    }

    if ((e.key === ")" || e.key === "]" || e.key === "}") && v[s] === e.key && s === en) {
      e.preventDefault();
      ta.setSelectionRange(s + 1, s + 1);
      return;
    }

    if (e.key === "Backspace" && s === en && s > 0) {
      var pc = v[s - 1], nc = v[s];
      if (PAIRS[pc] && PAIRS[pc] === nc) {
        e.preventDefault();
        ta.setSelectionRange(s - 1, s + 1);
        this.insert("");
        return;
      }
      if (/^ +$/.test(curLine) && curLine.length % 4 === 0 && curLine.length > 0) {
        e.preventDefault();
        ta.setSelectionRange(s - 4, s);
        this.insert("");
      }
    }

    if ((e.ctrlKey || e.metaKey) && e.key === "/") {
      e.preventDefault();
      var be = v.indexOf("\n", en);
      if (be < 0) be = v.length;
      var blk = v.slice(lineStart, be);
      var allCommented = blk.split("\n").every(function (l) { return /^\s*\/\//.test(l) || !l.trim(); });
      var nblk = allCommented ? blk.replace(/^(\s*)\/\/ ?/gm, "$1") : blk.replace(/^(\s*)(?=\S)/gm, "$1// ");
      ta.setSelectionRange(lineStart, be);
      this.insert(nblk);
      ta.setSelectionRange(lineStart, lineStart + nblk.length);
    }
  };

  global.CodeEditor = CodeEditor;
})(window);
