// "Ask the docs": ranks the site's search index (BM25) in the browser, shows the best sections,
// and, when an answer endpoint is configured, asks it to write a short cited answer from them.
(function () {
  var cfg = window.WD_ASK || {};
  var TOP = 5;
  var SEND_CHARS = 1500;
  var STOP = new Set("a an the of for to in on at is are was were be what which who how do does did can i it its and or with from by this that these those there about into as".split(" "));

  var dialog, form, input, out, index;

  function tokens(s) {
    return s.replace(/([a-z])([A-Z])/g, "$1 $2").toLowerCase().split(/[^a-z0-9]+/).filter(function (t) {
      return t && !STOP.has(t);
    }).map(function (t) { return t.length > 3 && t.slice(-1) === "s" ? t.slice(0, -1) : t; });
  }

  function load() {
    if (index) return index;
    index = fetch(cfg.searchData).then(function (r) { return r.json(); }).then(function (data) {
      var docs = Object.keys(data).map(function (k) { return data[k]; });
      var df = Object.create(null), total = 0;
      docs.forEach(function (d) {
        // Page titles count six times and section titles three times as much as body text.
        var page = tokens(d.doc), sect = tokens(d.title), tf = Object.create(null);
        page.concat(page, page, page, page, page, sect, sect, sect, tokens(d.content)).forEach(function (t) { tf[t] = (tf[t] || 0) + 1; });
        d.tf = tf;
        d.len = 0;
        for (var t in tf) { d.len += tf[t]; df[t] = (df[t] || 0) + 1; }
        total += d.len;
      });
      return { docs: docs, df: df, avg: total / docs.length };
    });
    return index;
  }

  function rank(ix, question) {
    var q = tokens(question).filter(function (t, i, all) { return all.indexOf(t) === i; });
    var n = ix.docs.length, k1 = 1.2, b = 0.75;
    var scored = ix.docs.map(function (d) {
      var s = 0, hit = 0;
      q.forEach(function (t) {
        var f = d.tf[t];
        if (!f) return;
        hit++;
        var idf = Math.log(1 + (n - ix.df[t] + 0.5) / (ix.df[t] + 0.5));
        s += idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * d.len / ix.avg));
      });
      // Prefer sections that match most of the question's words over ones that match one word often.
      return { d: d, s: s * Math.pow(hit / q.length, 2) };
    }).filter(function (x) { return x.s > 0; });
    scored.sort(function (a, b) { return b.s - a.s; });
    var seen = Object.create(null), res = [];
    for (var i = 0; i < scored.length && res.length < TOP; i++) {
      if (seen[scored[i].d.url]) continue;
      seen[scored[i].d.url] = 1;
      res.push(scored[i].d);
    }
    return { sections: res, terms: q };
  }

  function snippet(d, terms) {
    var text = d.content.replace(/[|\-:]{2,}/g, " ").replace(/\s*\|\s*/g, " · ").replace(/\s+/g, " "), low = text.toLowerCase(), at = -1;
    for (var i = 0; i < terms.length && at < 0; i++) at = low.indexOf(terms[i]);
    var from = Math.max(0, at - 60);
    return (from ? "… " : "") + text.slice(from, from + 220) + (text.length > from + 220 ? " …" : "");
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function renderAnswer(text, sections) {
    var p = el("p", "wd-ask-answer");
    text.split(/(\[\d+\])/).forEach(function (part) {
      var m = /^\[(\d+)\]$/.exec(part), s = m && sections[+m[1] - 1];
      if (s) {
        var a = el("a", "wd-ask-cite", part);
        a.href = s.url;
        p.appendChild(a);
      } else {
        p.appendChild(document.createTextNode(part));
      }
    });
    return p;
  }

  function renderSources(sections, terms) {
    var list = el("ol", "wd-ask-sources");
    sections.forEach(function (d) {
      var li = el("li"), a = el("a", "wd-ask-source-title", d.doc + " › " + d.title);
      a.href = d.url;
      li.appendChild(a);
      li.appendChild(el("span", "wd-ask-snippet", snippet(d, terms)));
      list.appendChild(li);
    });
    return list;
  }

  function ask(question) {
    out.replaceChildren(el("p", "wd-ask-status", "Searching the docs…"));
    load().then(function (ix) {
      var found = rank(ix, question);
      if (!found.sections.length) {
        out.replaceChildren(el("p", "wd-ask-status", "No matching sections. Try a different word, such as an asset name."));
        return;
      }
      var sources = renderSources(found.sections, found.terms);
      if (!cfg.endpoint) {
        out.replaceChildren(el("p", "wd-ask-status", "Best-matching sections:"), sources);
        return;
      }
      out.replaceChildren(el("p", "wd-ask-status", "Writing an answer…"), sources);
      var payload = {
        question: question,
        sources: found.sections.map(function (d) { return { title: d.doc + " › " + d.title, text: d.content.slice(0, SEND_CHARS) }; }),
      };
      var ctl = new AbortController(), timer = setTimeout(function () { ctl.abort(); }, 25000);
      fetch(cfg.endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload), signal: ctl.signal })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (j) {
          out.replaceChildren(renderAnswer(j.answer || "", found.sections), el("p", "wd-ask-status", "Sources:"), sources);
        })
        .catch(function () {
          out.replaceChildren(el("p", "wd-ask-status", "The answer service is unavailable, so here are the best-matching sections:"), sources);
        })
        .finally(function () { clearTimeout(timer); });
    }).catch(function () {
      out.replaceChildren(el("p", "wd-ask-status", "Could not load the search index."));
    });
  }

  function build() {
    dialog = el("dialog", "wd-ask");
    dialog.setAttribute("aria-label", "Ask the docs");
    form = el("form", "wd-ask-form");
    input = el("input", "wd-ask-input");
    input.type = "text";
    input.maxLength = 300;
    input.required = true;
    input.placeholder = "e.g. What are the sources for vehicle damage?";
    input.setAttribute("aria-label", "Your question");
    var go = el("button", "wd-btn wd-btn-primary", "Ask");
    go.type = "submit";
    form.append(input, go);
    out = el("div", "wd-ask-out");
    out.setAttribute("aria-live", "polite");
    var hint = el("p", "wd-ask-hint", cfg.endpoint
      ? "Answers are written by an AI from the matching sections and can be wrong. Check the sources."
      : "Finds the best-matching sections across all pages.");
    dialog.append(form, out, hint);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var q = input.value.trim();
      if (q) ask(q);
    });
    dialog.addEventListener("click", function (e) { if (e.target === dialog) dialog.close(); });
    document.body.appendChild(dialog);
    load();
  }

  function open() {
    if (!dialog) build();
    dialog.showModal();
    input.focus();
    input.select();
  }

  function init() {
    if (!window.HTMLDialogElement) return;
    var list = document.querySelector(".aux-nav-list");
    if (list) {
      var li = el("li", "aux-nav-list-item"), b = el("button", "site-button wd-ask-open", "Ask");
      b.type = "button";
      li.appendChild(b);
      list.insertBefore(li, list.firstChild);
    }
    document.querySelectorAll("[data-wd-ask]").forEach(function (b) { b.hidden = false; });
    document.addEventListener("click", function (e) {
      if (e.target.closest(".wd-ask-open, [data-wd-ask]")) { e.preventDefault(); open(); }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
