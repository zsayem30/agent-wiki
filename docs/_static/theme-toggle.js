(function () {
  var STORAGE_KEY = "agentWikiTheme";

  function currentTheme() {
    return document.documentElement.dataset.theme === "dark" ? "dark" : "light";
  }

  function applyTheme(theme) {
    var nextTheme = theme === "dark" ? "dark" : "light";
    document.documentElement.dataset.theme = nextTheme;
    try {
      localStorage.setItem(STORAGE_KEY, nextTheme);
    } catch (error) {
      // Local storage can be unavailable in strict browser modes.
    }

    document.querySelectorAll(".aw-theme-option").forEach(function (button) {
      var active = button.dataset.themeValue === nextTheme;
      button.setAttribute("aria-pressed", active ? "true" : "false");
      button.classList.toggle("is-active", active);
    });
  }

  function makeButton(label, theme) {
    var button = document.createElement("button");
    button.type = "button";
    button.className = "aw-theme-option";
    button.dataset.themeValue = theme;
    button.textContent = label;
    button.addEventListener("click", function () {
      applyTheme(theme);
    });
    return button;
  }

  function installToggle() {
    var target = document.querySelector(".wy-breadcrumbs-aside");
    if (!target || target.querySelector(".aw-theme-toggle")) {
      return;
    }

    var toggle = document.createElement("span");
    toggle.className = "aw-theme-toggle";
    toggle.setAttribute("role", "group");
    toggle.setAttribute("aria-label", "Color theme");
    toggle.appendChild(makeButton("Light", "light"));
    toggle.appendChild(makeButton("Dark", "dark"));
    target.insertBefore(toggle, target.firstChild);
    applyTheme(currentTheme());
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installToggle);
  } else {
    installToggle();
  }
})();
