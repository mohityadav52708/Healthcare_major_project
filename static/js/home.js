const navbarToggle = document.querySelector("#navbar-toggle");
const navbarMenu = document.querySelector("#navbar-menu");
const homeContainer = document.querySelector(".home_container");
let isNavbarExpanded = navbarToggle.getAttribute("aria-expanded") === "true";

const toggleNavbarVisibility = () => {
    isNavbarExpanded = !isNavbarExpanded;
    navbarToggle.setAttribute("aria-expanded", isNavbarExpanded);
    navbarMenu.style.visibility = isNavbarExpanded ? 'visible' : 'hidden';
    navbarMenu.style.opacity = isNavbarExpanded ? '1' : '0';
    homeContainer.style.pointerEvents = isNavbarExpanded ? 'none' : 'auto';
};

navbarToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    toggleNavbarVisibility();
});

document.addEventListener("click", (e) => {
    if (isNavbarExpanded && !navbarMenu.contains(e.target) && !navbarToggle.contains(e.target)) {
        toggleNavbarVisibility();
    }
});

navbarMenu.addEventListener("click", (e) => e.stopPropagation());

window.addEventListener('resize', () => {
    if (window.innerWidth >= 700) {
        // Reset navbar for desktop view
        navbarToggle.setAttribute("aria-expanded", "false");
        navbarMenu.style.visibility = 'visible';
        navbarMenu.style.opacity = '1';
        homeContainer.style.pointerEvents = 'auto';
    } else if (!isNavbarExpanded) {
        // Ensure navbar is hidden in mobile view if not expanded
        navbarMenu.style.visibility = 'hidden';
        navbarMenu.style.opacity = '0';
    }
});

document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('.home_container').classList.add('loaded');
});
document.addEventListener("DOMContentLoaded", function() {
  const boxes = document.querySelectorAll(".second_container > .content_cover_of_second_container > div");

  const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
          if (entry.isIntersecting) {
              entry.target.classList.add("fade-in");
              entry.target.style.animationPlayState = "running"; // Start the animation
          } else {
              entry.target.classList.remove("fade-in");
              entry.target.style.animationPlayState = "paused"; // Pause the animation when out of view
              entry.target.style.opacity = "0"; // Reset opacity
              entry.target.style.transform = "translateY(20px)"; // Reset transform
          }
      });
  }, { threshold: 0.1 });

  boxes.forEach(box => {
      observer.observe(box);
  });
});
document.addEventListener("DOMContentLoaded", function() {
  const boxes = document.querySelectorAll(".fourth_container > .content_cover_of_fourth_container > div");

  const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
          if (entry.isIntersecting) {
              entry.target.classList.add("fade-in");
              entry.target.style.animationPlayState = "running"; // Start the animation
          } else {
              entry.target.classList.remove("fade-in");
              entry.target.style.animationPlayState = "paused"; // Pause the animation when out of view
              entry.target.style.opacity = "0"; // Reset opacity
              entry.target.style.transform = "translateY(20px)"; // Reset transform
          }
      });
  }, { threshold: 0.1 });

  boxes.forEach(box => {
      observer.observe(box);
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const boxes = document.querySelectorAll(".fifth_container > .content_cover_of_fifth_container > div");

  const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
          if (entry.isIntersecting) {
              entry.target.classList.add("fade-in");
              entry.target.style.animationPlayState = "running"; // Start the animation
          } else {
              entry.target.classList.remove("fade-in");
              entry.target.style.animationPlayState = "paused"; // Pause the animation when out of view
              entry.target.style.opacity = "0"; // Reset opacity
              entry.target.style.transform = "translateY(20px)"; // Reset transform
          }
      });
  }, { threshold: 0.1 });

  boxes.forEach(box => {
      observer.observe(box);
  });
});
