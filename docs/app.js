const sections = [...document.querySelectorAll('main > section[id]')];
const links = [...document.querySelectorAll('.nav-link')];
const progress = document.querySelector('.reading-progress');
let queued = false;
function updateReadingPosition() {
  const top = window.scrollY;
  const max = document.documentElement.scrollHeight - window.innerHeight;
  progress.style.width = `${max > 0 ? Math.min(100, top / max * 100) : 0}%`;
  const threshold = window.innerWidth <= 760 ? 160 : 150;
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= threshold) current = section;
  }
  for (const link of links) {
    const active = link.hash === `#${current.id}`;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
  queued = false;
}
function queueUpdate() {
  if (!queued) { queued = true; requestAnimationFrame(updateReadingPosition); }
}
window.addEventListener('scroll', queueUpdate, {passive:true});
window.addEventListener('resize', queueUpdate);
updateReadingPosition();
