/* Mobile tables: on narrow screens, a data table that is wider than its container becomes one card per row,
   each cell labelled with its column header (data-label). Tables that fit are left alone; without JS tables scroll.
   Works for static and script-built tables (re-checks after DOM changes and on resize). No dependencies. */
(function () {
  var MAX = 600;
  function header(t) {
    var head = t.tHead && t.tHead.rows[0];
    if (!head && t.rows[0] && [].every.call(t.rows[0].cells, function (c) { return c.tagName === 'TH'; })) head = t.rows[0];
    return head;
  }
  function label(t, head) {
    var names = [].map.call(head.cells, function (c) { return c.textContent.replace(/\s+/g, ' ').trim(); });
    [].forEach.call(t.rows, function (r) {
      if (r === head) return;
      var col = 0;   // column index, counting colspans; spanning cells get no label and show full width
      [].forEach.call(r.cells, function (c) {
        var span = c.colSpan || 1;
        if (span === 1 && !c.hasAttribute('data-label') && names[col]) c.setAttribute('data-label', names[col]);
        col += span;
      });
    });
  }
  function fits(t) {
    var box = t.parentElement;
    return t.scrollWidth <= t.clientWidth + 2 && (!box || t.scrollWidth <= box.clientWidth + 2);
  }
  function run() {
    var small = window.innerWidth <= MAX;
    [].forEach.call(document.querySelectorAll('table'), function (t) {
      if (t.closest('[data-no-stack], header, nav, footer')) return;
      t.classList.remove('mt-stack');
      if (!small) return;
      var head = header(t);
      if (!head || head.cells.length < 2 || head.querySelector('[colspan],[rowspan]') || t.querySelector('[rowspan]')) return;
      if (fits(t)) return;
      label(t, head);
      t.classList.add('mt-stack');
      if (t.parentElement) t.parentElement.classList.add('mt-stack-wrap');
    });
  }
  var timer;
  function later() { clearTimeout(timer); timer = setTimeout(run, 120); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
  window.addEventListener('load', run);
  window.addEventListener('resize', later);
  if (window.MutationObserver) new MutationObserver(function (m) {
    for (var i = 0; i < m.length; i++) if (m[i].addedNodes.length && !(m[i].target.closest && m[i].target.closest('.mt-stack'))) { later(); return; }
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
