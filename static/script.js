// ====== PROFILE: Edit your details here ======
const PROFILE = {
  name: "Ankit Gupta",
  role: "Web Developer & DevOps Engineer",
  email: "ankit890123@gmail.com",
  location: "Mumbai, IN",
  resumeUrl: "https://drive.google.com/file/d/1isG58Xrr3ks3ORNXAGvE3tJqXfn9tQWi/view",
  github: "https://github.com/Ankit890123",
  linkedin: "https://www.linkedin.com/in/ankitgupta-devops//",
  twitter: "https://x.com/ankitgupta",
};

// ====== THEME TOGGLE (persists) ======
const root = document.documentElement;
const themeToggle = document.getElementById('themeToggle');
function applyStoredTheme() {
  const saved = localStorage.getItem('theme');
  if (saved === 'light') { root.classList.add('light'); }
}
function toggleTheme() {
  root.classList.toggle('light');
  localStorage.setItem('theme', root.classList.contains('light') ? 'light' : 'dark');
}
themeToggle?.addEventListener('click', toggleTheme);
applyStoredTheme();

// ====== NAV active link on scroll ======
const links = Array.from(document.querySelectorAll('.nav-links a'));
const sections = links.map(a => document.querySelector(a.getAttribute('href')));
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const id = '#' + entry.target.id;
    const link = links.find(l => l.getAttribute('href') === id);
    if (entry.isIntersecting) {
      links.forEach(l => l.classList.remove('active'));
      if (link) link.classList.add('active');
    }
  });
}, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });
sections.forEach(s => s && observer.observe(s));

// ====== Mobile menu ======
const menuBtn = document.getElementById('menuBtn');
const navLinks = document.getElementById('navLinks');
menuBtn?.addEventListener('click', () => {
  const open = navLinks.style.display === 'flex';
  navLinks.style.display = open ? 'none' : 'flex';
  navLinks.style.flexDirection = 'column';
  menuBtn.setAttribute('aria-expanded', String(!open));
});

// ====== Resume link & contact links ======
const resumeBtn = document.getElementById('resumeBtn');
if (resumeBtn) resumeBtn.href = PROFILE.resumeUrl;

const emailLink = document.getElementById('emailLink');
if (emailLink) {
  emailLink.textContent = PROFILE.email;
  emailLink.href = `mailto:${PROFILE.email}`;
}

const githubLink = document.getElementById('githubLink');
if (githubLink) githubLink.href = PROFILE.github;

const linkedinLink = document.getElementById('linkedinLink');
if (linkedinLink) linkedinLink.href = PROFILE.linkedin;

const xLink = document.getElementById('xLink');
if (xLink) xLink.href = PROFILE.twitter;

const locText = document.getElementById('locText');
if (locText) locText.textContent = PROFILE.location;

// ====== Copy email ======
const copyEmail = document.getElementById('copyEmail');
copyEmail?.addEventListener('click', async () => {
  try { await navigator.clipboard.writeText(PROFILE.email); toast('Email copied ✅'); }
  catch { toast('Copy failed.'); }
});

// ====== Project Filter ======
const grid = document.getElementById('projectGrid');
const filterBtns = Array.from(document.querySelectorAll('.filter'));
filterBtns.forEach(btn => btn.addEventListener('click', () => {
  filterBtns.forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const f = btn.dataset.filter;
  Array.from(grid.children).forEach(card => {
    const tags = (card.dataset.tags || '').split(',').map(t => t.trim());
    const show = f === 'all' || tags.includes(f);
    card.style.display = show ? '' : 'none';
  });
}));

// ====== Contact form -> Flask backend ======
const form = document.getElementById("contactForm");
form?.addEventListener("submit", async function (e) {
  e.preventDefault();
  let name = document.getElementById("name")?.value.trim();
  let email = document.getElementById("email")?.value.trim();
  let message = document.getElementById("message")?.value.trim();
  if (!name || !email || !message) {
    toast("⚠️ Please fill all fields");
    return;
  }
  try {
    let response = await fetch("/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, message })
    });
    let result = await response.json();
    if (result.status === "success") {
      toast("✅ Message sent successfully!");
      form.reset();
    } else {
      toast("❌ Error: " + result.message);
    }
  } catch (err) {
    toast("⚠️ Something went wrong: " + err);
  }
});

// ====== Back to top ======
const backTop = document.getElementById('backTop');
backTop?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
window.addEventListener('scroll', () => {
  if (window.scrollY > 400) backTop?.classList.add('show'); else backTop?.classList.remove('show');
});

// ====== Simple reveal on scroll ======
const revealEls = document.querySelectorAll('.card, .project, .title, .section-title');
const revealObs = new IntersectionObserver((entries) => {
  entries.forEach(({ target, isIntersecting }) => {
    if (isIntersecting) {
      target.animate([{ opacity: 0, transform: 'translateY(10px)' }, { opacity: 1, transform: 'none' }],
        { duration: 500, fill: 'forwards', easing: 'cubic-bezier(.2,.8,.2,1)' });
      revealObs.unobserve(target);
    }
  });
}, { threshold: .15 });
revealEls.forEach(el => revealObs.observe(el));

// ====== Footer year ======
const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

// ====== Tiny toast ======
function toast(msg) {
  const t = document.createElement('div');
  t.textContent = msg; t.role = 'status';
  Object.assign(t.style, {
    position: 'fixed', left: '50%', bottom: '20px', transform: 'translateX(-50%)',
    padding: '10px 14px', background: 'var(--card)', color: 'var(--text)',
    border: '1px solid rgba(231,237,243,.12)', borderRadius: '10px',
    boxShadow: 'var(--shadow)', zIndex: 9999
  });
  document.body.appendChild(t); setTimeout(() => t.remove(), 1800);
}

// ====== Self-check ======
(function selfCheck() {
  const checks = [
    ['Theme toggle exists', !!document.getElementById('themeToggle')],
    ['Nav links present', document.querySelectorAll('.nav-links a').length >= 5],
    ['Project cards present', document.querySelectorAll('.project').length >= 3],
    ['Filter buttons present', document.querySelectorAll('.filter').length >= 3],
    ['Contact form present', !!document.getElementById('contactForm')],
  ];
  const allGood = checks.every(([, ok]) => ok);
  console.table(checks);
  if (allGood) toast('✅ Portfolio ready'); else toast('⚠️ Check console for issues');
})();
