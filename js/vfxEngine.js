class StudioVFXEngine {
  constructor() {
    this.canvas = null;
    this.ctx = null;
    this.particles = [];
    this.lasers = [];
    this.ambient = [];
  }

  init() {
    this.canvas = document.getElementById("vfx-canvas");
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");
    this.resize();
    window.addEventListener("resize", () => this.resize());

    for (let i = 0; i < 32; i++) {
      this.ambient.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.35,
        vy: -0.3 - Math.random() * 0.5,
        r: 1 + Math.random() * 2,
        c: i % 2 === 0 ? "#00f0ff" : "#ffcc33"
      });
    }
    this.loop();
  }

  resize() {
    if (!this.canvas) return;
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  spawnEliminationBurst(rect, color = "#00f0ff") {
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    // Laser bolt from bottom command console to card center
    this.lasers.push({
      x1: window.innerWidth / 2,
      y1: window.innerHeight - 60,
      x2: cx,
      y2: cy,
      alpha: 1.0,
      color
    });

    // Shatter particles
    for (let i = 0; i < 24; i++) {
      const ang = Math.random() * Math.PI * 2;
      const spd = 2 + Math.random() * 6.5;
      this.particles.push({
        x: cx,
        y: cy,
        vx: Math.cos(ang) * spd,
        vy: Math.sin(ang) * spd,
        life: 1.0,
        r: 2 + Math.random() * 3.5,
        color
      });
    }
  }

  triggerUltimateCutIn(unit, abilityName) {
    const el = document.getElementById("ultimate-cutin");
    if (!el) return;
    document.getElementById("cutin-img").src = window.StudioArt.getArt(unit.id);
    document.getElementById("cutin-faction").textContent = unit.faction.toUpperCase() + " ACTIVE ULTIMATE";
    document.getElementById("cutin-title").textContent = abilityName;
    el.classList.remove("hidden");
    setTimeout(() => el.classList.add("hidden"), 1650);
  }

  loop() {
    requestAnimationFrame(() => this.loop());
    if (!this.ctx || !this.canvas) return;
    const w = this.canvas.width;
    const h = this.canvas.height;
    this.ctx.clearRect(0, 0, w, h);

    // Ambient floating motes
    this.ambient.forEach((m) => {
      m.x += m.vx;
      m.y += m.vy;
      if (m.y < 0) m.y = h;
      if (m.x < 0) m.x = w;
      if (m.x > w) m.x = 0;
      this.ctx.fillStyle = m.c + "44";
      this.ctx.beginPath();
      this.ctx.arc(m.x, m.y, m.r, 0, Math.PI * 2);
      this.ctx.fill();
    });

    // Laser Beams
    for (let i = this.lasers.length - 1; i >= 0; i--) {
      const l = this.lasers[i];
      this.ctx.save();
      this.ctx.strokeStyle = l.color;
      this.ctx.shadowColor = l.color;
      this.ctx.shadowBlur = 16;
      this.ctx.globalAlpha = l.alpha;
      this.ctx.lineWidth = 4 * l.alpha;
      this.ctx.beginPath();
      this.ctx.moveTo(l.x1, l.y1);
      this.ctx.lineTo(l.x2, l.y2);
      this.ctx.stroke();
      this.ctx.restore();
      l.alpha -= 0.06;
      if (l.alpha <= 0) this.lasers.splice(i, 1);
    }

    // Explosion Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life -= 0.035;
      if (p.life <= 0) {
        this.particles.splice(i, 1);
        continue;
      }
      this.ctx.save();
      this.ctx.fillStyle = p.color;
      this.ctx.shadowColor = p.color;
      this.ctx.shadowBlur = 10;
      this.ctx.globalAlpha = p.life;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    }
  }
}

window.StudioVFX = new StudioVFXEngine();
