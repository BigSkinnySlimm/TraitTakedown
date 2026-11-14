class StudioVFXEngine {
  constructor() {
    this.canvas = null;
    this.ctx = null;
    this.particles = [];
    this.lasers = [];
  }
  init() {
    this.canvas = document.getElementById("vfx-canvas");
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");
    this.resize();
    window.addEventListener("resize", () => this.resize());
    this.loop();
  }
  resize() {
    if (!this.canvas) return;
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }
  spawnEliminationBurst(rect, color = "#00f0ff") {
    if (!rect || rect.width === 0) return;
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    this.lasers.push({ x1: window.innerWidth / 2, y1: window.innerHeight - 70, x2: cx, y2: cy, alpha: 1.0, color });
    for (let i = 0; i < 20; i++) {
      const a = Math.random() * Math.PI * 2;
      const s = 2 + Math.random() * 6;
      this.particles.push({ x: cx, y: cy, vx: Math.cos(a) * s, vy: Math.sin(a) * s, life: 1.0, r: 2 + Math.random() * 3, color });
    }
  }
  triggerUltimateCutIn(unit, abilityName) {
    const el = document.getElementById("ultimate-cutin");
    if (!el) return;
    document.getElementById("cutin-img").src = window.StudioArt.getArt(unit.id);
    document.getElementById("cutin-faction").textContent = unit.faction.toUpperCase() + " ACTIVE ULTIMATE";
    document.getElementById("cutin-title").textContent = abilityName;
    el.classList.remove("hidden");
    setTimeout(() => el.classList.add("hidden"), 1600);
  }
  loop() {
    requestAnimationFrame(() => this.loop());
    if (!this.ctx || !this.canvas) return;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    for (let i = this.lasers.length - 1; i >= 0; i--) {
      const l = this.lasers[i];
      this.ctx.save();
      this.ctx.strokeStyle = l.color;
      this.ctx.shadowColor = l.color;
      this.ctx.shadowBlur = 14;
      this.ctx.globalAlpha = l.alpha;
      this.ctx.lineWidth = 3.5 * l.alpha;
      this.ctx.beginPath();
      this.ctx.moveTo(l.x1, l.y1);
      this.ctx.lineTo(l.x2, l.y2);
      this.ctx.stroke();
      this.ctx.restore();
      l.alpha -= 0.06;
      if (l.alpha <= 0) this.lasers.splice(i, 1);
    }
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx; p.y += p.vy; p.life -= 0.04;
      if (p.life <= 0) { this.particles.splice(i, 1); continue; }
      this.ctx.save();
      this.ctx.fillStyle = p.color;
      this.ctx.globalAlpha = p.life;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    }
  }
}
window.StudioVFX = new StudioVFXEngine();
