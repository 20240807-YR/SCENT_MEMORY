const canvas = document.getElementById("scentCanvas");
const ctx = canvas.getContext("2d");
const offCanvas = document.createElement('canvas');
const offCtx = offCanvas.getContext('2d');

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();

let WIDTH = canvas.width;
let HEIGHT = canvas.height;
window.addEventListener('resize', () => {
  WIDTH = canvas.width;
  HEIGHT = canvas.height;
});

function getZones() {
  return {
    top: { yMin: 0, yMax: HEIGHT * 0.33 },
    middle: { yMin: HEIGHT * 0.33, yMax: HEIGHT * 0.66 },
    base: { yMin: HEIGHT * 0.66, yMax: HEIGHT },
  };
}

const entities = window.visualEntities;

const particles = [];

let mouseX = 0;
let mouseY = 0;
let hoveredParticle = null;
const infoCard = document.getElementById('scentInfoCard');
const cardTitle = document.getElementById('cardTitle');
const cardIngredients = document.getElementById('cardIngredients');
const cardDesc = document.getElementById('cardDesc');

class Cluster {
  constructor(cx, cy, item, zone) {
    this.cx = cx;
    this.cy = cy;
    this.zone = zone;
    this.ingredient = item.ingredients ? item.ingredients.join(", ") : "";
    this.motion = item.motion;

    this.img = new Image();
    this.img.src = item.image;

    this.baseSize = 60;
    this.size = this.baseSize;
    this.angle = Math.random() * Math.PI * 2;

    this.vx = (Math.random() - 0.5) * 0.2;
    this.vy = (Math.random() - 0.5) * 0.15;

    this.isHovered = false;
  }

  move() {
    this.cx += this.vx;
    this.cy += this.vy;

    if (this.cx < -200) this.cx = WIDTH + 200;
    else if (this.cx > WIDTH + 200) this.cx = -200;

    if (this.cy < -200) this.cy = HEIGHT + 200;
    else if (this.cy > HEIGHT + 200) this.cy = -200;

    const d = Math.hypot(mouseX - this.cx, mouseY - this.cy);
    this.isHovered = d < 120;
    if (this.isHovered) hoveredParticle = this;
  }

  draw(ctx) {
    if (!this.img.complete || !this.img.src) return;

    const drawSize = this.isHovered ? 300 : 250;
    const radius = drawSize / 2;

    // prepare off-screen canvas
    offCanvas.width = drawSize;
    offCanvas.height = drawSize;
    offCtx.clearRect(0, 0, drawSize, drawSize);

    // draw image onto off-screen canvas
    offCtx.save();
    offCtx.drawImage(this.img, 0, 0, drawSize, drawSize);

    // feathered radial mask
    offCtx.globalCompositeOperation = 'destination-in';
    const gradient = offCtx.createRadialGradient(
      radius, radius, 0,
      radius, radius, radius
    );
    gradient.addColorStop(0, 'rgba(255,255,255,1)');
    gradient.addColorStop(0.5, 'rgba(255,255,255,1)');
    gradient.addColorStop(1, 'rgba(255,255,255,0)');
    offCtx.fillStyle = gradient;
    offCtx.fillRect(0, 0, drawSize, drawSize);
    offCtx.restore();

    // draw processed image to main canvas
    ctx.save();
    ctx.translate(this.cx, this.cy);
    ctx.globalCompositeOperation = 'screen';

    if (this.isHovered) {
      ctx.globalAlpha = 1.0;
    } else {
      ctx.globalAlpha = 0.9;
    }

    ctx.drawImage(offCanvas, -radius, -radius);
    ctx.restore();
  }

  isClicked(mx, my) {
    return (
      mx > this.cx - this.size / 2 &&
      mx < this.cx + this.size / 2 &&
      my > this.cy - this.size / 2 &&
      my < this.cy + this.size / 2
    );
  }
}

function initParticles() {
  const ZONES = getZones();
  Object.entries(entities).forEach(([zone, list]) => {
    const safeList = Array.isArray(list) ? list : [list];
    safeList.forEach((item) => {
      for (let i = 0; i < 3; i++) {
        const x = Math.random() * WIDTH;
        const y =
          ZONES[zone].yMin +
          Math.random() * (ZONES[zone].yMax - ZONES[zone].yMin);

        particles.push(
          new Cluster(x, y, item, zone)
        );
      }
    });
  });
}

function animate(time) {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);

  let activeParticle = null;

  particles.forEach((p) => {
    const dx = mouseX - p.cx;
    const dy = mouseY - p.cy;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist < 120) {
      p.isHovered = true;
      activeParticle = p;
    } else {
      p.isHovered = false;
    }

    p.move();
    p.draw(ctx);
  });

  updateInfoCard(activeParticle);
  requestAnimationFrame(animate);
}

function updateInfoCard(particle) {
  if (particle && infoCard) {
    cardTitle.innerText = particle.zone.toUpperCase() + " NOTE";
    cardIngredients.innerText = particle.ingredient || "";
    cardDesc.innerText = particle.motion || "";

    const offset = 20;
    let left = mouseX + offset;
    let top = mouseY + offset;

    infoCard.style.left = left + 'px';
    infoCard.style.top = top + 'px';
    infoCard.classList.add('visible');

    canvas.style.cursor = 'pointer';
  } else if (infoCard) {
    infoCard.classList.remove('visible');
    canvas.style.cursor = 'default';
  }
}

canvas.addEventListener("click", (e) => {
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  for (const p of particles) {
    if (p.isClicked(mx, my)) {
      alert(p.ingredient);
      break;
    }
  }
});

canvas.addEventListener('mousemove', (e) => {
  const rect = canvas.getBoundingClientRect();
  mouseX = e.clientX - rect.left;
  mouseY = e.clientY - rect.top;
});

initParticles();
animate();