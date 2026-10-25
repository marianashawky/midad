(function () {
  var root = document.querySelector("[data-reader]");
  if (!root) return;
  var key = "midad-reader";
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(key) || "{}"); } catch (e) { saved = {}; }

  var size = saved.size || 19;
  function apply() {
    root.style.setProperty("--read-size", size + "px");
    document.body.classList.toggle("night", !!saved.night);
    localStorage.setItem(key, JSON.stringify(saved));
  }
  apply();

  var story = root.getAttribute("data-story");
  var chapter = root.getAttribute("data-chapter");
  var title = root.getAttribute("data-title") || "";
  if (story) {
    var shelf = {};
    try { shelf = JSON.parse(localStorage.getItem("midad-shelf") || "{}"); } catch (e) { shelf = {}; }
    shelf[story] = { chapter: chapter, title: title, at: Date.now() };
    localStorage.setItem("midad-shelf", JSON.stringify(shelf));
  }

  document.querySelectorAll("[data-size]").forEach(function (button) {
    button.addEventListener("click", function () {
      size = Math.min(26, Math.max(16, size + Number(button.getAttribute("data-size"))));
      saved.size = size;
      apply();
    });
  });
  var night = document.querySelector("[data-night]");
  if (night) {
    night.addEventListener("click", function () {
      saved.night = !saved.night;
      apply();
    });
  }
})();

(function () {
  var slots = document.querySelectorAll("[data-continue]");
  if (!slots.length) return;
  var shelf = {};
  try { shelf = JSON.parse(localStorage.getItem("midad-shelf") || "{}"); } catch (e) { shelf = {}; }
  slots.forEach(function (slot) {
    var story = slot.getAttribute("data-continue");
    var item = shelf[story];
    if (!item || !item.chapter) return;
    var link = document.createElement("a");
    link.className = "cta";
    link.style.background = "#8d3158";
    link.href = item.chapter + "/";
    link.textContent = "كمّل القراءة";
    slot.appendChild(link);
  });
})();

(function () {
  var buttons = document.querySelectorAll("[data-filter]");
  if (!buttons.length) return;
  var cards = document.querySelectorAll("[data-genres]");
  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      var genre = button.getAttribute("data-filter");
      buttons.forEach(function (item) { item.setAttribute("aria-pressed", item === button ? "true" : "false"); });
      cards.forEach(function (card) {
        var genres = card.getAttribute("data-genres") || "";
        card.classList.toggle("hidden", genre !== "all" && genres.indexOf(genre) === -1);
      });
    });
  });
})();
