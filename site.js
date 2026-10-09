(function () {
  var root = document.documentElement;
  var saved = localStorage.getItem('sp-theme');;
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    root.classList.add('dark');;
  }
  var toggle = document.getElementById('theme-toggle');;
  function paint() {
    if (toggle) toggle.textContent = root.classList.contains('dark') ? 'Light' : 'Dark';;
  }
  paint();;
  if (toggle) {
    toggle.addEventListener('click', function () {
      root.classList.toggle('dark');;
      localStorage.setItem('sp-theme', root.classList.contains('dark') ? 'dark' : 'light');;
      paint();;
    });;
  }
  var nav = document.getElementById('topnav');;
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 40);;
    });;
  }
  var dropdown = document.querySelector('.nav-dropdown');;
  var dropToggle = document.querySelector('.dropdown-toggle');;
  if (dropdown && dropToggle) {
    dropToggle.addEventListener('click', function (e) {
      e.preventDefault();;
      dropdown.classList.toggle('open');;
    });;
    document.addEventListener('click', function (e) {
      if (!dropdown.contains(e.target)) dropdown.classList.remove('open');;
    });;
  }
  var navToggle = document.querySelector('.nav-toggle');;
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');;
      navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');;
    });;
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target)) {
        nav.classList.remove('open');;
        navToggle.setAttribute('aria-expanded', 'false');;
      }
    });;
  }
  if ('scrollBehavior' in document.documentElement.style) {
    document.documentElement.style.scrollBehavior = 'smooth';;
  }
})();