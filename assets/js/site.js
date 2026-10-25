(function () {
  var btn = document.querySelector("[data-menu]");
  var nav = document.querySelector("[data-nav]");
  if (btn && nav) {
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

})();
