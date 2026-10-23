// Wiki tables: click a column header to sort (numbers by value, text alphabetically).
// The infobox is left alone. Loaded by _layouts/wiki.html.
(function () {
  function key(cell) {
    var text = cell.textContent.trim();
    var num = parseFloat(text.replace(/,/g, '').replace(/^[^\d\-.]+/, ''));
    return isNaN(num) ? text.toLowerCase() : num;
  }

  function sortBy(table, col, button) {
    var body = table.tBodies[0];
    var dir = button.getAttribute('aria-sort') === 'ascending' ? 'descending' : 'ascending';
    var rows = Array.prototype.slice.call(body.rows);
    rows.sort(function (a, b) {
      var x = key(a.cells[col] || a), y = key(b.cells[col] || b);
      // Numbers before text, so "not yet known" cells sink to the end either way.
      if (typeof x !== typeof y) return typeof x === 'number' ? -1 : 1;
      var r = x < y ? -1 : x > y ? 1 : 0;
      return dir === 'ascending' ? r : -r;
    });
    rows.forEach(function (r) { body.appendChild(r); });
    table.querySelectorAll('thead th').forEach(function (th) { th.removeAttribute('aria-sort'); });
    button.closest('th').setAttribute('aria-sort', dir);
    button.setAttribute('aria-sort', dir);
  }

  document.querySelectorAll('.wiki table:not(.wiki-infobox)').forEach(function (table) {
    if (!table.tHead || !table.tBodies[0] || table.tBodies[0].rows.length < 3) return;
    Array.prototype.forEach.call(table.tHead.rows[0].cells, function (th, col) {
      if (!th.textContent.trim()) return;
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'wiki-sort';
      while (th.firstChild) button.appendChild(th.firstChild);
      th.appendChild(button);
      button.addEventListener('click', function () { sortBy(table, col, button); });
    });
  });
})();
