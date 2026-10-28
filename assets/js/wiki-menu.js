/* Header menu bar (_includes/header_custom.html). Hover, keyboard focus or the caret button
   open a dropdown; Escape or a click elsewhere closes it. On narrow screens the bar sits
   behind the "Browse the wiki" button and the dropdowns open in place. */
(function () {
  var bar = document.getElementById("wiki-menu");
  if (!bar) return;
  var burger = bar.querySelector(".wm-burger");
  var items = Array.prototype.slice.call(bar.querySelectorAll(".wm-item"));

  function setOpen(item, open) {
    item.classList.toggle("wm-open", open);
    item.querySelector(".wm-caret").setAttribute("aria-expanded", String(open));
  }
  function closeAll(except) {
    items.forEach(function (i) { if (i !== except) setOpen(i, false); });
  }

  items.forEach(function (item) {
    var caret = item.querySelector(".wm-caret");
    caret.addEventListener("click", function () {
      var open = !item.classList.contains("wm-open");
      closeAll(item);
      setOpen(item, open);
    });
    // Tabbing out of an item closes it.
    item.addEventListener("focusout", function (e) {
      if (e.relatedTarget && !item.contains(e.relatedTarget)) setOpen(item, false);
    });
    // Arrow keys move through the dropdown links.
    item.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowDown" && e.key !== "ArrowUp") return;
      var links = Array.prototype.slice.call(item.querySelectorAll(".wm-drop a"));
      var at = links.indexOf(document.activeElement);
      e.preventDefault();
      if (!item.classList.contains("wm-open")) { closeAll(item); setOpen(item, true); }
      var next = e.key === "ArrowDown" ? at + 1 : (at < 0 ? links.length - 1 : at - 1);
      links[(next + links.length) % links.length].focus();
    });
  });

  burger.addEventListener("click", function () {
    var open = burger.getAttribute("aria-expanded") !== "true";
    burger.setAttribute("aria-expanded", String(open));
    bar.classList.toggle("wm-shown", open);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var item = document.activeElement && document.activeElement.closest && document.activeElement.closest(".wm-item");
    closeAll();
    // Focus back on the title link; an item's wm-esc class hides the dropdown that :focus-within would keep.
    if (item) { item.classList.add("wm-esc"); item.querySelector(".wm-top").focus(); }
  });
  bar.addEventListener("focusin", function (e) {
    var cur = e.target.closest(".wm-item");
    items.forEach(function (i) { if (i !== cur) i.classList.remove("wm-esc"); });
  });
  // Sidebar lists only Wiki Home and the hubs, so an article has no link of its own: mark the
  // hub whose path is the longest prefix of this page (the theme already marks exact matches).
  var navLinks = Array.prototype.slice.call(document.querySelectorAll("#site-nav .nav-list-link"));
  if (!navLinks.some(function (a) { return a.classList.contains("active"); })) {
    var best = null, path = location.pathname;
    navLinks.forEach(function (a) {
      var h = a.pathname;
      if (/\/wiki\/[^/]+\/$/.test(h) && path.indexOf(h) === 0 && (!best || h.length > best.pathname.length)) best = a;
    });
    if (best) { best.classList.add("active"); best.parentNode.classList.add("active"); }
  }
  document.addEventListener("click", function (e) { if (!bar.contains(e.target)) closeAll(); });
})();
