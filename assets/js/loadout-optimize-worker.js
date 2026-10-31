/* Dedicated worker keeps combination search off the UI thread. Imports share the
   page's build stamp so a newly deployed worker cannot mix old evaluator code. */
"use strict";
importScripts("loadout-eval.js" + self.location.search, "loadout-optimize.js" + self.location.search);
self.onmessage = function (event) {
  var data = event.data;
  try {
    var allowedIds = new Set(data.allowedIds);
    var result = self.WDLoadoutOptimizer.optimize(self.WDLoadout.model(data.json), data.loadout, {
      allowed: function (id) { return allowedIds.has(id); }
    });
    self.postMessage({ id: data.id, result: result });
  } catch (error) {
    self.postMessage({ id: data.id, error: error.message || String(error) });
  }
};
