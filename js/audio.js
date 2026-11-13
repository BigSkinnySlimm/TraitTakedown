class SymphonicAudioEngine {
  constructor() {
    this.ctx = null; this.muted = false; this.running = false; this.idx = 0;
    this.chords = [
      [146.83, 220.00, 261.63, 329.63],
      [116.54, 220.00, 293.66, 392.00],
      [98.00,  196.00, 220.00, 293.66],
      [110.00, 164.81, 220.00, 329.63]
    ];
  }
  ensure() {
    if (!this.ctx) {
      const C = window.AudioContext || window.webkitAudioContext;
      if (C) this.ctx = new C();
    }
    if (this.ctx && this.ctx.state === "suspended") this.ctx.resume();
    if (this.ctx && !this.running) {
      this.running = true;
      setInterval(() => { if (!this.muted) this.playPad(); }, 4600);
    }
  }
  playPad() {
    if (!this.ctx || this.muted) return;
    const now = this.ctx.currentTime;
    const notes = this.chords[this.idx++ % this.chords.length];
    notes.forEach((f) => {
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = "triangle"; o.frequency.setValueAtTime(f, now);
      g.gain.setValueAtTime(0.0001, now);
      g.gain.linearRampToValueAtTime(0.025, now + 1.2);
      g.gain.exponentialRampToValueAtTime(0.0001, now + 4.4);
      o.connect(g); g.connect(this.ctx.destination);
      o.start(now); o.stop(now + 4.5);
    });
  }
  sfx(freq, dur) {
    this.ensure();
    if (!this.ctx || this.muted) return;
    const now = this.ctx.currentTime;
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = "sine"; o.frequency.setValueAtTime(freq, now);
    g.gain.setValueAtTime(0.12, now);
    g.gain.exponentialRampToValueAtTime(0.001, now + dur);
    o.connect(g); g.connect(this.ctx.destination);
    o.start(now); o.stop(now + dur);
  }
  toggleMute() { this.muted = !this.muted; return this.muted; }
  playFlip() { this.sfx(180, 0.1); }
  playScan() { this.sfx(520, 0.22); }
  playAbilityUltimate() { this.sfx(130, 0.45); }
  playVictory() { this.sfx(587.33, 0.5); }
  playDefeat() { this.sfx(146.83, 0.45); }
}
window.StudioAudio = new SymphonicAudioEngine();
