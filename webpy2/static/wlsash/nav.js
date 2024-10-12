let nav = document.createElement("div");
nav.classList.add("topbar");
nav.innerHTML = `<a href="./" class="left">
      <img class="favicon" src="https://s3.bmp.ovh/imgs/2024/09/28/2ae5ef77ccb35774.png">
      <span class="title">WLSA School House</span>
    </a>
    <div class="right">
      <a href="./log${window.logmessage || 'in'}" target="_blank" class="pc-only">Log${window.logmessage || 'in'}</a>
      <a href="./dashboard" target="_blank" class="pc-only">Dashboard</a>
      <a href="./archives" target="_blank" class="pc-only">Archives</a>
      <a href="./pt-booking" target="_blank" class="pc-only">PT Booking</a>
      <a href="./community" target="_blank" class="pc-only">Community</a>
      <span id="toggle-mobile-nav" class="mobile-only">
        <svg width="16" height="12">
          <g stroke="white">
            <line x1="0" y1="0" x2="16" y2="0" stroke-width="3"></line>
            <line x1="0" y1="6" x2="16" y2="6" stroke-width="1.5"></line>
            <line x1="0" y1="12" x2="16" y2="12" stroke-width="3"></line>
          </g>
        </svg>
      </span>
    </div>`
let mobileNav = document.createElement("div");
mobileNav.className = "mobile-only mobile-nav";
mobileNav.innerHTML = `
    <a href="./log${window.logmessage || 'in'}" target="_blank">Log${window.logmessage || 'in'}</a>
    <a href="./dashboard" target="_blank">Dashboard</a>
    <a href="./archives" target="_blank">Archives</a>
    <a href="./pt-booking" target="_blank">PT Booking</a>
    <a href="./community" target="_blank">Community</a>`
mobileNav.style.height = "0%";
document.body.prepend(mobileNav);
document.body.prepend(nav);         // normal nav first, then mobile nav

let navToggler = document.getElementById("toggle-mobile-nav");
navToggler.onclick = () => {
    if (mobileNav.style.height == "0%") mobileNav.style.height = "100%";
    else mobileNav.style.height = "0%";
}