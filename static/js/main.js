document.addEventListener("DOMContentLoaded", () => {

  /* ── Navbar scroll effect ─────────────────────────────── */
  const navbar = document.getElementById("navbar");
  const onScroll = () => navbar.classList.toggle("scrolled", window.scrollY > 30);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ── Hero slideshow ───────────────────────────────────── */
  const heroSlides = document.querySelectorAll(".hero-slide");
  if (heroSlides.length > 1 && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    let idx = 0;
    setInterval(() => {
      heroSlides[idx].classList.remove("is-active");
      idx = (idx + 1) % heroSlides.length;
      heroSlides[idx].classList.add("is-active");
    }, 6000);
  }

  /* ── Scroll reveal ────────────────────────────────────── */
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        revealObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });

  document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

  /* ── Toast auto-dismiss ───────────────────────────────── */
  document.querySelectorAll(".toast-close").forEach((btn) => {
    btn.addEventListener("click", () => {
      const toast = btn.closest(".pcm-toast");
      toast.style.opacity = "0";
      toast.style.transform = "translateX(20px)";
      toast.style.transition = "all .3s ease";
      setTimeout(() => toast.remove(), 300);
    });
  });
  setTimeout(() => {
    document.querySelectorAll(".pcm-toast").forEach((t) => {
      t.style.opacity = "0";
      t.style.transform = "translateX(20px)";
      t.style.transition = "all .4s ease";
      setTimeout(() => t.remove(), 400);
    });
  }, 5000);

  /* ── Close navbar on mobile nav click ────────────────── */
  document.querySelectorAll(".navbar-collapse .nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      const collapse = document.querySelector(".navbar-collapse");
      if (collapse?.classList.contains("show")) {
        bootstrap.Collapse.getOrCreateInstance(collapse).hide();
      }
    });
  });

  /* ── Active nav highlight fix ─────────────────────────── */
  const path = window.location.pathname;
  document.querySelectorAll(".navbar-pcm .nav-link").forEach((link) => {
    const href = link.getAttribute("href");
    if (href && href !== "/" && path.startsWith(href)) {
      link.classList.add("active");
    }
  });

});
