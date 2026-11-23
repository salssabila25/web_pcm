document.addEventListener("DOMContentLoaded", () => {

  /* ── Scroll controls ──────────────────────────────────── */
  const navbar = document.getElementById("navbar");
  const progressBar = document.getElementById("scroll-progress-bar");
  const backToTop = document.getElementById("back-to-top");
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let scrollFrame = 0;

  const updateScrollEffects = () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => {
      const scrollTop = window.scrollY;
      const scrollRange = document.documentElement.scrollHeight - window.innerHeight;
      const progress = scrollRange > 0 ? Math.min(scrollTop / scrollRange, 1) : 0;

      if (navbar) navbar.classList.toggle("scrolled", scrollTop > 30);
      if (progressBar) progressBar.style.transform = `scaleX(${progress})`;
      if (backToTop) backToTop.classList.toggle("is-visible", scrollTop > 400);
      scrollFrame = 0;
    });
  };

  updateScrollEffects();
  window.addEventListener("scroll", updateScrollEffects, { passive: true });
  window.addEventListener("resize", updateScrollEffects, { passive: true });

  backToTop?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
  });

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

  /* ── Homepage stat counters ───────────────────────────── */
  const counters = document.querySelectorAll("[data-count]");
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      counterObserver.unobserve(entry.target);

      const target = Number(entry.target.dataset.count);
      if (!Number.isSafeInteger(target) || target < 0) return;
      const format = (value) => new Intl.NumberFormat("id-ID").format(value);

      if (prefersReducedMotion || target === 0) {
        entry.target.textContent = format(target);
        return;
      }

      const duration = 900;
      let startTime;
      const animate = (timestamp) => {
        if (startTime === undefined) startTime = timestamp;
        const progress = Math.min((timestamp - startTime) / duration, 1);
        const eased = 1 - (1 - progress) ** 3;
        entry.target.textContent = format(Math.round(target * eased));
        if (progress < 1) requestAnimationFrame(animate);
      };

      entry.target.textContent = "0";
      requestAnimationFrame(animate);
    });
  }, { threshold: 0.6 });

  counters.forEach((counter) => counterObserver.observe(counter));

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
