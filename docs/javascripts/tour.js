(function () {
  var script = document.currentScript;
  var configUrl = new URL("../assets/tour.json", script.src).href;

  function visible(el) {
    return el && el.getClientRects().length > 0;
  }

  function start(config) {
    var steps = config.steps, index = 0, target = null;
    var card = document.createElement("div");
    card.className = "tour-card";
    card.setAttribute("role", "dialog");
    card.setAttribute("aria-label", "Guide tour");
    document.body.appendChild(card);

    function clear() {
      if (target) { target.classList.remove("tour-target"); target = null; }
    }
    function finish() {
      clear();
      card.remove();
      try { localStorage.setItem(config.storageKey, "1"); } catch (e) {}
    }
    function show() {
      clear();
      var step = steps[index];
      for (var i = 0; i < step.target.length; i++) {
        var el = document.querySelector(step.target[i]);
        if (visible(el)) { target = el; break; }
      }
      if (target) {
        target.classList.add("tour-target");
        target.scrollIntoView({ block: "center", behavior: "smooth" });
      }
      var last = index === steps.length - 1;
      card.innerHTML = "";
      var count = document.createElement("div");
      count.className = "tour-count";
      count.textContent = "Step " + (index + 1) + " of " + steps.length;
      var title = document.createElement("h4");
      title.textContent = step.title;
      var text = document.createElement("p");
      text.textContent = step.text;
      var actions = document.createElement("div");
      actions.className = "tour-actions";
      if (index > 0) {
        var back = document.createElement("button");
        back.textContent = "Back";
        back.onclick = function () { index--; show(); };
        actions.appendChild(back);
      }
      var next = document.createElement("button");
      next.className = "tour-next";
      next.textContent = last ? "Done" : "Next";
      next.onclick = function () { if (last) { finish(); } else { index++; show(); } };
      actions.appendChild(next);
      if (!last) {
        var skip = document.createElement("button");
        skip.className = "tour-skip";
        skip.textContent = "Skip tour";
        skip.onclick = finish;
        actions.appendChild(skip);
      }
      card.appendChild(count); card.appendChild(title); card.appendChild(text); card.appendChild(actions);
    }
    show();
  }

  function init() {
    var link = document.getElementById("tour-start");
    if (!link) { return; }
    fetch(configUrl).then(function (r) { return r.json(); }).then(function (config) {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        if (!document.querySelector(".tour-card")) { start(config); }
      });
      var seen = false;
      try { seen = localStorage.getItem(config.storageKey) === "1"; } catch (e) {}
      if (!seen) { setTimeout(function () { if (!document.querySelector(".tour-card")) { start(config); } }, 700); }
    }).catch(function () {});
  }

  if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", init); } else { init(); }
})();
