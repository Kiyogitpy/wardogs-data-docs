/* Reading aids for the data pages (styles in _sass/custom/custom.scss):
   - number columns right-aligned
   - long, narrow tables split into two side-by-side halves
   - long tables scroll in their own box under a sticky header, wide ones keep
     their first column in view, and both get a row filter
   - long code dumps collapsed behind a "Full export" toggle
   - an "On this page" list: pinned at the right on wide screens, a collapsed
     block under the title elsewhere */
(function () {
  "use strict";

  var SPLIT_ROWS = [12, 80];   // a table of <= 3 columns and this many rows is split in two
  var FILTER_ROWS = 25;        // more rows than this: a filter box
  var TALL_ROWS = 40;          // more rows than this: its own scroll box, header pinned
  var WIDE_COLS = 5;           // this many columns or more: the first one stays in view
  var DUMP_LINES = 30;         // a code block longer than this starts collapsed
  var TOC_MIN_H2 = 4;          // pages with fewer sections get no "On this page"
  var TOC_SIDE = "(min-width: 120rem)";
  var NUMBER = /^[-+−~≈]?\d[\d,.\s]*(e[-+]?\d+)?\s*(%|x|×|s|ms|m|cm|km|kg|°|deg|mil|rpm|hp)?$/i;
  var BLANK = /^(|-|—|–|n\/a|none)$/i;

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  function markNumberColumns(table) {
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);
    var cols = table.tHead.rows[0].cells.length;
    for (var c = 0; c < cols; c++) {
      var numbers = 0, others = 0;
      rows.forEach(function (row) {
        var cell = row.cells[c];
        if (!cell) return;
        var text = cell.textContent.trim();
        if (BLANK.test(text)) return;
        if (NUMBER.test(text)) numbers++; else others++;
      });
      if (numbers && numbers >= 4 * others) {
        table.tHead.rows[0].cells[c].classList.add("num");
        rows.forEach(function (row) { if (row.cells[c]) row.cells[c].classList.add("num"); });
      }
    }
  }

  // The second half moves into its own table (header cloned) beside the first.
  function split(table) {
    var wrapper = table.parentNode;
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);
    var right = table.cloneNode(false), rightBody = document.createElement("tbody");
    right.appendChild(table.tHead.cloneNode(true));
    right.appendChild(rightBody);
    rows.slice(Math.ceil(rows.length / 2)).forEach(function (row) { rightBody.appendChild(row); });
    var pair = document.createElement("div"), rightWrapper = wrapper.cloneNode(false);
    pair.className = "table-pair";
    wrapper.parentNode.insertBefore(pair, wrapper);
    pair.appendChild(wrapper);
    rightWrapper.appendChild(right);
    pair.appendChild(rightWrapper);
    return pair;
  }

  // Every word typed must appear somewhere in a row for it to stay shown.
  function addFilter(block, bodies) {
    var rows = [];
    bodies.forEach(function (body) { rows.push.apply(rows, body.rows); });
    var texts = rows.map(function (row) { return row.textContent.toLowerCase(); });
    var bar = document.createElement("div");
    var input = document.createElement("input");
    var count = document.createElement("span");
    bar.className = "wd-filter";
    input.type = "search";
    input.placeholder = "Filter " + rows.length.toLocaleString() + " rows";
    input.setAttribute("aria-label", "Filter the rows of the table below");
    count.className = "wd-filter-count";
    count.setAttribute("aria-live", "polite");
    bar.appendChild(input);
    bar.appendChild(count);
    block.parentNode.insertBefore(bar, block);

    var timer;
    function apply() {
      var terms = input.value.toLowerCase().split(/\s+/).filter(Boolean);
      var shown = 0;
      rows.forEach(function (row, i) {
        var hit = terms.every(function (t) { return texts[i].indexOf(t) !== -1; });
        row.hidden = !hit;
        if (hit) shown++;
      });
      count.textContent = terms.length ? shown.toLocaleString() + " of " + rows.length.toLocaleString() : "";
      block.classList.toggle("wd-filtered", terms.length > 0);
    }
    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(apply, rows.length > 1000 ? 150 : 50);
    });
  }

  function prepareTable(table) {
    var head = table.tHead, body = table.tBodies[0];
    if (!head || !body || !head.rows.length) return;
    var wrapper = table.parentNode;
    var cols = head.rows[0].cells.length, rows = body.rows.length;
    markNumberColumns(table);
    if (cols >= WIDE_COLS) wrapper.classList.add("wd-wide");

    var block = wrapper, bodies = [body];
    if (cols <= 3 && rows >= SPLIT_ROWS[0] && rows <= SPLIT_ROWS[1]) {
      block = split(table);
      bodies = Array.prototype.map.call(block.querySelectorAll("tbody"), function (b) { return b; });
    } else if (rows > TALL_ROWS) {
      wrapper.classList.add("wd-tall");
    }
    if (rows > FILTER_ROWS) addFilter(block, bodies);
  }

  function collapseDumps(main) {
    main.querySelectorAll("div.highlighter-rouge").forEach(function (block) {
      var lines = block.textContent.replace(/\n$/, "").split("\n").length;
      if (lines <= DUMP_LINES) return;
      var details = document.createElement("details");
      var summary = document.createElement("summary");
      details.className = "wd-dump";
      summary.textContent = "Full export · " + lines.toLocaleString() + " lines";
      block.parentNode.insertBefore(details, block);
      details.appendChild(summary);
      details.appendChild(block);
    });
  }

  function buildToc(main) {
    if (main.querySelector(".wd-hero")) return;
    var heads = Array.prototype.slice.call(main.querySelectorAll("h2[id], h3[id]"));
    if (heads.filter(function (h) { return h.tagName === "H2"; }).length < TOC_MIN_H2) return;

    var nav = document.createElement("nav");
    var details = document.createElement("details");
    var summary = document.createElement("summary");
    var list = document.createElement("ol");
    nav.className = "wd-toc";
    nav.setAttribute("aria-label", "On this page");
    summary.textContent = "On this page";
    heads.forEach(function (h) {
      var li = document.createElement("li"), a = document.createElement("a");
      if (h.tagName === "H3") li.className = "wd-toc-sub";
      a.href = "#" + h.id;
      a.textContent = h.textContent.trim();
      li.appendChild(a);
      list.appendChild(li);
    });
    details.appendChild(summary);
    details.appendChild(list);
    nav.appendChild(details);

    // Under the title and its source line.
    var h1 = main.querySelector("h1");
    var after = h1 && h1.nextElementSibling && h1.nextElementSibling.tagName === "P" ? h1.nextElementSibling : h1;
    if (after) after.parentNode.insertBefore(nav, after.nextSibling);
    else main.insertBefore(nav, main.firstChild);

    var side = window.matchMedia(TOC_SIDE);
    function place() {
      nav.classList.toggle("wd-toc-side", side.matches);
      details.open = side.matches;
    }
    if (side.addEventListener) side.addEventListener("change", place); else side.addListener(place);
    place();

    // Highlight the section being read; keep it in view inside a long list.
    var links = list.querySelectorAll("a"), current = -1, queued = false;
    function spy() {
      queued = false;
      var i = -1;
      for (var k = 0; k < heads.length; k++) {
        if (heads[k].getBoundingClientRect().top <= 120) i = k; else break;
      }
      if (i === current) return;
      if (current >= 0) links[current].classList.remove("is-active");
      current = i;
      if (i < 0) return;
      var a = links[i];
      a.classList.add("is-active");
      if (side.matches && (a.offsetTop < list.scrollTop || a.offsetTop > list.scrollTop + list.clientHeight - a.offsetHeight)) {
        list.scrollTop = a.offsetTop - list.clientHeight / 3;
      }
    }
    window.addEventListener("scroll", function () {
      if (!queued) { queued = true; requestAnimationFrame(spy); }
    }, { passive: true });
    spy();
  }

  ready(function () {
    var main = document.querySelector(".main-content");
    if (!main) return;
    main.querySelectorAll(".table-wrapper > table").forEach(prepareTable);
    collapseDumps(main);
    buildToc(main);
  });
})();
