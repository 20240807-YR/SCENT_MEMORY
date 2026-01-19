const canvas = document.getElementById("scentCanvas");
const ctx = canvas.getContext("2d");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;

const ZONES = {
  top: { yMin: 0, yMax: 200 },
  middle: { yMin: 200, yMax: 400 },
  base: { yMin: 400, yMax: 600 },
};

const entities = window.visualEntities;

const particles = [];

class Particle {
  constructor(x, y, color, ingredient, zone, motion) {
    this.x = x;
    this.y = y;
    this.radius = 6 + Math.random() * 6;
    this.color = color;
    this.ingredient = ingredient;
    this.zone = zone;

    const speedMap = {
      fast_float: 1.2,
      slow_drift: 0.4,
      heavy_float: 0.2,
    };

    const speed = speedMap[motion] || 0.5;

    this.vx = (Math.random() - 0.5) * speed;
    this.vy = (Math.random() - 0.5) * speed;
  }

  move() {
    this.x += this.vx;
    this.y += this.vy;

    if (this.x < 0 || this.x > WIDTH) this.vx *= -1;
    if (this.y < ZONES[this.zone].yMin || this.y > ZONES[this.zone].yMax)
      this.vy *= -1;
  }

  draw(ctx) {
    ctx.beginPath();
    ctx.fillStyle = this.color;
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fill();
  }

  isClicked(mx, my) {
    const dx = mx - this.x;
    const dy = my - this.y;
    return Math.sqrt(dx * dx + dy * dy) < this.radius;
  }
}

function initParticles() {
  Object.entries(entities).forEach(([zone, list]) => {
    list.forEach((item) => {
      for (let i = 0; i < 10; i++) {
        const x = Math.random() * WIDTH;
        const y =
          ZONES[zone].yMin +
          Math.random() * (ZONES[zone].yMax - ZONES[zone].yMin);

        particles.push(
          new Particle(
            x,
            y,
            item.color,
            item.ingredient,
            zone,
            item.motion
          )
        );
      }
    });
  });
}

function animate() {
  ctx.clearRect(0, 0, WIDTH, HEIGHT);

  particles.forEach((p) => {
    p.move();
    p.draw(ctx);
  });

  requestAnimationFrame(animate);
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

initParticles();
animate();