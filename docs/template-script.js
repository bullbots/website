window.onload = () => {
  let theme = localStorage.getItem("theme");
  if (theme && theme === "light-mode") {
    document.body.classList.toggle("dark-mode");
    document.body.classList.toggle("light-mode");

    document.querySelector('meta[name="theme-color"]')
      .setAttribute("content",
        getComputedStyle(document.documentElement)
        .getPropertyValue('--light-accent-color'));
  } else {
      document.querySelector('meta[name="theme-color"]')
      .setAttribute("content",
        getComputedStyle(document.documentElement)
        .getPropertyValue('--dark-accent-color'));}
}

function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
  document.body.classList.toggle("light-mode");

  document.getElementById("light-icon").classList.toggle("hidden");
  document.getElementById("dark-icon").classList.toggle("hidden");

  let theme = localStorage.getItem("theme");
  if (theme && theme === "dark-mode") {
    localStorage.setItem("theme", "light-mode");
    document.querySelector('meta[name="theme-color"]')
      .setAttribute("content", 
        getComputedStyle(document.documentElement)
        .getPropertyValue('--light-accent-color'));

  } else {
    localStorage.setItem("theme", "dark-mode");
    document.querySelector('meta[name="theme-color"]')
      .setAttribute("content", 
        getComputedStyle(document.documentElement)
        .getPropertyValue('--dark-accent-color'));
  }
}

/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function openNav() {
  var root = document.querySelector(':root');
  var x = document.getElementById("topnav");
  if (!x.classList.contains("responsive")) {
    x.classList.add("responsive");
  } else {
    x.classList.remove("responsive");
  }
}