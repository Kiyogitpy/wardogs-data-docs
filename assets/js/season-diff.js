// Season 1 -> Season 2 change browser and landing-page totals.
// Data: <base>index.json and one or more per-area files (see _tools/season_diff.py).
// Hooks: [data-sd-totals] renders the totals; [data-sd-browser] renders the full browser.
(function () {
  'use strict';

  var PAGE = 40;          // assets rendered per step
  var ROWS = 200;         // property rows rendered per step inside an asset
  var CLIP = 220;         // characters of a long value shown before "show more"
  var STATUSES = ['modified', 'moved', 'added', 'removed'];

  function h(tag, attrs, kids) {
    var e = document.createElement(tag);
    if (attrs) for (var k in attrs) {
      if (attrs[k] == null || attrs[k] === false) continue;
      if (k === 'class') e.className = attrs[k];
      else if (k === 'text') e.textContent = attrs[k];
      else e.setAttribute(k, attrs[k] === true ? '' : attrs[k]);
    }
    (kids || []).forEach(function (c) {
      if (c == null) return;
      e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    });
    return e;
  }

  var cache = {};
  function getJSON(url) {
    if (!cache[url]) {
      cache[url] = fetch(url).then(function (r) {
        if (!r.ok) throw new Error(url + ': HTTP ' + r.status);
        return r.json();
      });
    }
    return cache[url];
  }

  function fmtNum(n) {
    return Number(n).toLocaleString('en-US');
  }

  // ---------- landing totals ----------
  function renderTotals(root) {
    var base = root.getAttribute('data-sd-base');
    getJSON(base + 'index.json').then(function (idx) {
      var t = idx.totals || {};
      var tiles = [
        ['assets_modified', 'Assets modified'],
        ['assets_moved', 'Assets moved'],
        ['assets_added', 'Assets added'],
        ['assets_removed', 'Assets removed'],
        ['property_changes', 'Property changes'],
        ['removed_values', 'Values in removed assets'],
        ['noise_only_assets', 'Noise-only assets']
      ];
      var grid = h('dl', { class: 'sd-tiles' });
      tiles.forEach(function (x) {
        grid.appendChild(h('div', { class: 'sd-tile' }, [
          h('dd', { text: fmtNum(t[x[0]] || 0) }),
          h('dt', { text: x[1] })
        ]));
      });
      var from = idx.from || {}, to = idx.to || {};
      var meta = (from.label || 'Season 1') + ' → ' + (to.label || 'Season 2') +
        (to.build ? ', build ' + to.build : '') + (to.date ? ', ' + to.date : '');
      root.replaceChildren(h('p', { class: 'sd-meta', text: meta }), grid, h('p', { class: 'sd-note', text:
        'Property changes counts the differences inside assets that exist in both seasons. ' +
        'Values in removed assets are the properties of assets deleted in Season 2, counted separately.' }));
    }).catch(function (e) {
      root.replaceChildren(h('p', { class: 'sd-note', text: 'Totals unavailable (' + e.message + ').' }));
    });
  }

  // ---------- value formatting ----------
  function isNum(v) { return typeof v === 'number' && isFinite(v); }
  function strVal(v) {
    if (v === null || v === undefined) return 'null';
    if (typeof v === 'string') return v;
    return typeof v === 'object' ? JSON.stringify(v) : String(v);
  }
  function round(n) {
    var a = Math.abs(n);
    if (a !== 0 && a < 1e-4) return n.toExponential(2);
    return String(Math.round(n * 1e6) / 1e6);
  }

  // resequenced: before/after are the full identity lists, old order and new order
  function seqMoved(c) {
    var old = {};
    (c.before || []).forEach(function (k, i) { old[k] = i; });
    var n = 0;
    (c.after || []).forEach(function (k, i) { if (old[k] !== i) n++; });
    return n;
  }
  function seqCell(list) {
    var td = h('td', { class: 'sd-val' });
    var det = h('details', { class: 'sd-seq' }, [h('summary', { text: fmtNum(list.length) + ' items, in order' })]);
    var built = false;
    det.addEventListener('toggle', function () {
      if (!det.open || built) return;
      built = true;
      var ol = h('ol', { class: 'sd-seq-list' });
      var frag = document.createDocumentFragment();
      list.forEach(function (k) { frag.appendChild(h('li', null, [h('code', { text: String(k) })])); });
      ol.appendChild(frag);
      det.appendChild(ol);
    });
    td.appendChild(det);
    return td;
  }

  function valueCell(v, missing) {
    var td = h('td', { class: 'sd-val' });
    if (missing) { td.appendChild(h('span', { class: 'sd-none', text: '—', 'aria-label': 'none' })); return td; }
    var s = strVal(v);
    var code = h('code', { class: typeof v === 'string' ? 'sd-str' : null });
    if (s.length > CLIP) {
      var short = s.slice(0, CLIP);
      code.textContent = short + '…';
      var btn = h('button', { type: 'button', class: 'sd-more', text: 'show more', 'aria-expanded': 'false' });
      var open = false;
      btn.addEventListener('click', function () {
        open = !open;
        code.textContent = open ? s : short + '…';
        btn.textContent = open ? 'show less' : 'show more';
        btn.setAttribute('aria-expanded', String(open));
      });
      td.appendChild(code); td.appendChild(btn);
    } else {
      code.textContent = s;
      td.appendChild(code);
    }
    return td;
  }

  function changeCell(c) {
    var td = h('td', { class: 'sd-chg' });
    if (c.op === 'added') td.appendChild(h('span', { class: 'sd-tag sd-tag-added', text: 'added' }));
    else if (c.op === 'removed') td.appendChild(h('span', { class: 'sd-tag sd-tag-removed', text: 'removed' }));
    else if (c.op === 'resequenced') {
      td.appendChild(h('span', { class: 'sd-tag', text: 'reordered' }));
      td.appendChild(h('div', { class: 'sd-seq-note', text: fmtNum(seqMoved(c)) + ' of ' + fmtNum((c.after || []).length) + ' moved' }));
    }
    else if (isNum(c.before) && isNum(c.after)) {
      var d = c.after - c.before;
      var tone = d > 0 ? 'is-up' : d < 0 ? 'is-down' : '';
      var txt = (d > 0 ? '+' : '') + round(d);
      if (c.before !== 0) {
        var p = d / Math.abs(c.before) * 100;   // relative to |before|; the sign follows the change
        txt += ' (' + (p > 0 ? '+' : '') + (Math.abs(p) >= 100 ? Math.round(p) : Math.round(p * 10) / 10) + '%)';
      }
      td.appendChild(h('span', { class: 'sd-delta ' + tone, text: txt }));
    } else {
      td.appendChild(h('span', { class: 'sd-tag', text: 'changed' }));
    }
    return td;
  }

  function changesTable(changes) {
    var tbody = h('tbody');
    var table = h('table', { class: 'sd-table' }, [
      h('thead', null, [h('tr', null, [
        h('th', { scope: 'col', text: 'Property' }),
        h('th', { scope: 'col', text: 'Season 1' }),
        h('th', { scope: 'col', text: 'Season 2' }),
        h('th', { scope: 'col', text: 'Change' })
      ])]),
      tbody
    ]);
    var wrap = h('div', { class: 'sd-table-wrap', tabindex: '0', role: 'region', 'aria-label': 'Property changes' }, [table]);
    var shown = 0, group = null;
    var more = h('button', { type: 'button', class: 'sd-btn sd-loadrows' });
    function step() {
      var frag = document.createDocumentFragment();
      var end = Math.min(shown + ROWS, changes.length);
      for (; shown < end; shown++) {
        var c = changes[shown];
        // multi-export files prefix every path with "ExportName::"; show it once as a heading
        // (never split on "." - data-table row names contain dots)
        var path = c.path, i = path.indexOf('::');
        var exp = i > 0 ? path.slice(0, i) : null;
        if (exp !== group) {
          group = exp;
          if (exp) frag.appendChild(h('tr', { class: 'sd-group' }, [h('th', { scope: 'colgroup', colspan: '4' }, [h('code', { text: exp })])]));
        }
        if (exp) path = path.slice(i + 2);
        var seq = c.op === 'resequenced';
        frag.appendChild(h('tr', null, [
          h('th', { scope: 'row', class: 'sd-prop' }, [h('code', { text: path })]),
          seq ? seqCell(c.before || []) : valueCell(c.before, c.op === 'added'),
          seq ? seqCell(c.after || []) : valueCell(c.after, c.op === 'removed'),
          changeCell(c)
        ]));
      }
      tbody.appendChild(frag);
      if (shown >= changes.length) more.remove();
      else more.textContent = 'Show more properties (' + fmtNum(changes.length - shown) + ' left)';
    }
    step();
    var box = h('div', null, [wrap]);
    if (shown < changes.length) { more.addEventListener('click', step); box.appendChild(more); }
    return box;
  }

  // ---------- browser ----------
  function renderBrowser(root) {
    var base = root.getAttribute('data-sd-base');
    var gh = root.getAttribute('data-gh');
    var idx = null;
    var state = { area: '', q: '', st: STATUSES.slice(), noise: true };
    var areaAssets = {};   // id -> assets array
    var hay = new WeakMap();    // asset -> header text
    var rowHay = new WeakMap(); // asset -> lowercase text of each change row, built on first search
    var filtered = [], rendered = 0, token = 0;

    var els = {};
    function build() {
      els.area = h('select', { id: 'sd-area' });
      idx.areas.forEach(function (a) {
        var c = a.counts || {};
        var n = (c.added || 0) + (c.removed || 0) + (c.modified || 0) + (c.moved || 0);
        els.area.appendChild(h('option', { value: a.id, text: a.title + ' (' + fmtNum(n) + ')' }));
      });
      els.q = h('input', { type: 'search', id: 'sd-q', placeholder: 'Asset, property path or value', autocomplete: 'off' });
      els.chips = h('div', { class: 'sd-chips', role: 'group', 'aria-label': 'Status' });
      els.chipBtn = {};
      STATUSES.forEach(function (s) {
        var b = h('button', { type: 'button', class: 'sd-chip sd-s-' + s, 'aria-pressed': 'true', text: s });
        b.addEventListener('click', function () {
          var i = state.st.indexOf(s);
          if (i >= 0) state.st.splice(i, 1); else state.st.push(s);
          refresh(true);
        });
        els.chipBtn[s] = b; els.chips.appendChild(b);
      });
      els.noise = h('button', { type: 'button', class: 'sd-toggle', 'aria-pressed': 'true' }, ['Hide noise-only assets']);
      els.noise.addEventListener('click', function () { state.noise = !state.noise; refresh(true); });
      els.summary = h('p', { class: 'sd-summary', role: 'status', 'aria-live': 'polite' });
      els.list = h('div', { class: 'sd-list' });
      els.more = h('button', { type: 'button', class: 'sd-btn', hidden: true });
      els.more.addEventListener('click', renderMore);

      els.area.addEventListener('change', function () { state.area = els.area.value; refresh(true); });
      var t;
      els.q.addEventListener('input', function () {
        clearTimeout(t);
        t = setTimeout(function () { state.q = els.q.value; refresh(true); }, 200);
      });

      var controls = h('div', { class: 'sd-controls' }, [
        h('div', { class: 'sd-field' }, [h('label', { for: 'sd-area', text: 'Area' }), els.area]),
        h('div', { class: 'sd-field sd-field-q' }, [h('label', { for: 'sd-q', text: 'Filter' }), els.q]),
        h('div', { class: 'sd-field' }, [h('span', { class: 'sd-label', text: 'Status' }), els.chips]),
        h('div', { class: 'sd-field' }, [h('span', { class: 'sd-label', text: 'Noise' }), els.noise])
      ]);
      root.replaceChildren(
        h('p', { class: 'sd-meta', id: 'sd-meta' }),
        controls, els.summary, els.list,
        h('div', { class: 'sd-more-wrap' }, [els.more])
      );
      var from = idx.from || {}, to = idx.to || {};
      document.getElementById('sd-meta').textContent = (from.label || 'Season 1') + ' → ' + (to.label || 'Season 2') +
        (to.build ? ', build ' + to.build : '') + (to.date ? ', ' + to.date : '');
    }

    function parseHash() {
      var p = new URLSearchParams(location.hash.replace(/^#/, ''));
      var a = p.get('area');
      var ids = idx.areas.map(function (x) { return x.id; });
      state.area = ids.indexOf(a) >= 0 ? a : (ids.indexOf(state.area) >= 0 ? state.area : ids[0]);
      state.q = p.get('q') || '';
      var s = p.get('s');
      state.st = s ? s.split(',').filter(function (x) { return STATUSES.indexOf(x) >= 0; }) : STATUSES.slice();
      state.noise = p.get('noise') !== '0';
    }
    function writeHash() {
      var p = new URLSearchParams();
      p.set('area', state.area);
      if (state.q) p.set('q', state.q);
      if (state.st.length !== STATUSES.length) p.set('s', state.st.join(','));
      if (!state.noise) p.set('noise', '0');
      var nh = '#' + p.toString();
      if (nh !== location.hash) history.replaceState(null, '', nh);
    }
    function syncControls() {
      els.area.value = state.area;
      els.q.value = state.q;
      STATUSES.forEach(function (s) { els.chipBtn[s].setAttribute('aria-pressed', String(state.st.indexOf(s) >= 0)); });
      els.noise.setAttribute('aria-pressed', String(state.noise));
    }

    function loadArea(id) {
      if (areaAssets[id]) return Promise.resolve(areaAssets[id]);
      var a = idx.areas.filter(function (x) { return x.id === id; })[0];
      var files = Array.isArray(a.file) ? a.file : [a.file];
      return Promise.all(files.map(function (f) { return getJSON(base + f); })).then(function (parts) {
        var all = [];
        parts.forEach(function (p) { (p.assets || []).forEach(function (x) { all.push(x); }); });
        areaAssets[id] = all;
        return all;
      });
    }

    function haystack(a) {
      var s = hay.get(a);
      if (s == null) {
        s = [a.name, a.path, a.old_path || '', a.type || '', a.paired_by || '', a.note || ''].join('\n').toLowerCase();
        hay.set(a, s);
      }
      return s;
    }
    function rowText(a) {
      var r = rowHay.get(a);
      if (!r) {
        r = (a.changes || []).map(function (c) {
          var v = c.op === 'resequenced' ? (c.before || []).join(' ') + ' ' + (c.after || []).join(' ') : strVal(c.before) + '\n' + strVal(c.after);
          return (c.path + '\n' + v).toLowerCase();
        });
        rowHay.set(a, r);
      }
      return r;
    }
    // Terms found in the asset header are satisfied; the rest must all occur in one property row.
    // Returns null (no match) or { a, rows } where rows is the matching change indexes (null = every row).
    function matchAsset(a, terms) {
      if (!terms.length) return { a: a, rows: null };
      var head = haystack(a), rest = [];
      terms.forEach(function (t) { if (head.indexOf(t) < 0) rest.push(t); });
      if (!rest.length) return { a: a, rows: null };
      var rt = rowText(a), rows = [];
      for (var i = 0; i < rt.length; i++) {
        var ok = true;
        for (var k = 0; k < rest.length; k++) if (rt[i].indexOf(rest[k]) < 0) { ok = false; break; }
        if (ok) rows.push(i);
      }
      return rows.length ? { a: a, rows: rows } : null;
    }
    function isNoiseOnly(a) { return a.status === 'modified' && !a.note && (!a.changes || !a.changes.length); }

    function refresh(write) {
      syncControls();
      if (write) writeHash();
      var my = ++token;
      els.summary.textContent = 'Loading…';
      els.list.replaceChildren();
      els.more.hidden = true;
      loadArea(state.area).then(function (all) {
        if (my !== token) return;
        var terms = state.q.toLowerCase().split(/\s+/).filter(Boolean);
        var hiddenNoise = 0;
        var t0 = performance.now();
        filtered = [];
        all.forEach(function (a) {
          if (state.st.indexOf(a.status) < 0) return;
          if (state.noise && isNoiseOnly(a)) { hiddenNoise++; return; }
          var m = matchAsset(a, terms);
          if (m) filtered.push(m);
        });
        var props = 0;
        filtered.forEach(function (m) { props += m.rows ? m.rows.length : (m.a.changes || []).length; });
        root.setAttribute('data-sd-ms', String(Math.round(performance.now() - t0)));
        els.summary.textContent = fmtNum(filtered.length) + ' of ' + fmtNum(all.length) + ' assets, ' +
          fmtNum(props) + ' property changes' + (hiddenNoise ? ' (' + fmtNum(hiddenNoise) + ' noise-only hidden)' : '') + '.';
        rendered = 0;
        if (!filtered.length) els.list.appendChild(h('p', { class: 'sd-note', text: 'Nothing matches these filters.' }));
        renderMore();
      }).catch(function (e) {
        if (my !== token) return;
        els.summary.textContent = '';
        els.list.replaceChildren(h('p', { class: 'sd-note', text: 'Could not load this area (' + e.message + ').' }));
      });
    }

    function renderMore() {
      var frag = document.createDocumentFragment();
      var end = Math.min(rendered + PAGE, filtered.length);
      for (; rendered < end; rendered++) frag.appendChild(assetBlock(filtered[rendered].a, filtered[rendered].rows));
      els.list.appendChild(frag);
      var left = filtered.length - rendered;
      els.more.hidden = left <= 0;
      els.more.textContent = 'Show more assets (' + fmtNum(left) + ' left)';
    }

    function assetBlock(a, rows) {
      var changes = a.changes || [];
      if (rows) changes = rows.map(function (i) { return changes[i]; });
      var n = changes.length;
      var det = h('details', { class: 'sd-asset sd-s-' + a.status });
      var sum = h('summary', null, [
        h('span', { class: 'sd-name', text: a.name }),
        h('span', { class: 'sd-badge sd-s-' + a.status, text: a.status }),
        a.paired_by === 'inferred' ? h('span', { class: 'sd-badge sd-inferred', title: 'Matched to its Season 1 copy by content, not by a clear identifier', text: 'inferred pairing' }) : null,
        a.type ? h('span', { class: 'sd-type', text: a.type }) : null,
        h('span', { class: 'sd-count', text: a.status === 'added' ? (a.exports != null ? fmtNum(a.exports) + ' exports' : '') : a.status === 'removed' ? 'removed in Season 2' : n ? fmtNum(n) + (n === 1 ? ' change' : ' changes') + (rows ? ' match' : '') : 'no property changes' })
      ]);
      var meta = h('div', { class: 'sd-meta-row' });
      if (a.status === 'removed') {
        meta.appendChild(h('code', { class: 'sd-path', text: a.path }));
        meta.appendChild(h('span', { class: 'sd-removed-note', text: 'removed in Season 2' }));
      } else {
        meta.appendChild(h('a', { class: 'sd-path', href: gh + a.path.split('/').map(encodeURIComponent).join('/'), text: a.path }));
      }
      if (a.old_path) {
        var how = { 'same-name': 'matched by file name', 'git-rename': 'detected as a rename', inferred: 'matched by content' }[a.paired_by];
        meta.appendChild(h('div', { class: 'sd-old' }, ['Moved from ', h('code', { text: a.old_path }), how ? ' (' + how + ')' : null]));
      }
      if (a.note) meta.appendChild(h('div', { class: 'sd-asset-note', text: a.note }));
      var noiseParts = [['renamed_keys', 'renamed keys'], ['swapped_keys', 'swapped key names'], ['dup_keys', 'duplicate keys'], ['type_reinterpret', 'values stored as raw bits'], ['ref_shifts', 'reference shifts']]
        .filter(function (n) { return a.noise && a.noise[n[0]]; })
        .map(function (n) { return fmtNum(a.noise[n[0]]) + ' ' + n[1]; });
      if (noiseParts.length) {
        meta.appendChild(h('div', { class: 'sd-noise', text: 'Also: ' + noiseParts.join(', ') + ' from the different Season 1 export (not listed).' }));
      }
      var body = h('div', { class: 'sd-body' }, [meta]);
      var done = false;
      det.addEventListener('toggle', function () {
        if (!det.open || done) return;
        done = true;
        if (a.status === 'added') {
          body.appendChild(h('p', { class: 'sd-note', text: 'New in Season 2' + (a.exports != null ? ' with ' + fmtNum(a.exports) + ' exports.' : '.') }));
        } else if (n) {
          body.appendChild(changesTable(changes));
        } else {
          body.appendChild(h('p', { class: 'sd-note', text: a.note ? 'No comparison available (see note above).' : a.status === 'moved' ? 'Content unchanged; the file only moved.' : 'No property changes beyond noise.' }));
        }
      });
      det.appendChild(sum); det.appendChild(body);
      return det;
    }

    getJSON(base + 'index.json').then(function (i) {
      idx = i;
      build();
      parseHash();
      refresh(false);
      window.addEventListener('hashchange', function () { parseHash(); refresh(false); });
    }).catch(function (e) {
      root.replaceChildren(h('p', { class: 'sd-note', text: 'Could not load the change index (' + e.message + ').' }));
    });
  }

  function init() {
    var t = document.querySelector('[data-sd-totals]');
    if (t) renderTotals(t);
    var b = document.querySelector('[data-sd-browser]');
    if (b) renderBrowser(b);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
