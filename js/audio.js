class SymphonicAudioEngine {
  constructor() {
    this.ctx = null; this.muted = false; this.running = false; this.step = 0;
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
      setInterval(() => { if (!this.muted) this.playPad(); }, 4400);
    }
  }
  playPad() {
    if (!this.ctx || this.muted) return;
    const now = this.ctx.currentTime;
    const notes = this.chords[this.step++ % this.chords.length];
    notes.forEach((f, i) => {
      const o = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o.type = i === 0 ? "triangle" : "sine";
      o.frequency.setValueAtTime(f, now);
      g.gain.setValueAtTime(0.0001, now);
      g.gain.linearRampToValueAtTime(0.022, now + 1.1);
      g.gain.exponentialRampToValueAtTime(0.0001, now + 4.2);
      o.connect(g); g.connect(this.ctx.destination);
      o.start(now); o.stop(now + 4.3);
    });
  }
  tone(freq, dur, type = "triangle", vol = 0.12) {
    this.ensure();
    if (!this.ctx || this.muted) return;
    const now = this.ctx.currentTime;
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = type; o.frequency.setValueAtTime(freq, now);
    g.gain.setValueAtTime(vol, now);
    g.gain.exponentialRampToValueAtTime(0.0001, now + dur);
    o.connect(g); g.connect(this.ctx.destination);
    o.start(now); o.stop(now + dur);
  }
  toggleMute() { this.muted = !this.muted; return this.muted; }
  playClick() { this.tone(620, 0.06, "sine", 0.08); }
  playFlip() { this.tone(240, 0.11, "triangle", 0.14); }
  playScan() {
    this.tone(440, 0.15, "sawtooth", 0.09);
    setTimeout(() => this.tone(880, 0.25, "triangle", 0.12), 80);
  }
  playUltimate() {
    [110, 220, 440, 659.25].forEach((f, i) => {
      setTimeout(() => this.tone(f, 0.42, "sawtooth", 0.12), i * 55);
    });
  }
  playVictory() {
    [293.66, 369.99, 440, 587.33].forEach((f, i) => {
      setTimeout(() => this.tone(f, 0.5, "triangle", 0.14), i * 110);
    });
  }
  playDefeat() {
    [220, 196, 146.83].forEach((f, i) => {
      setTimeout(() => this.tone(f, 0.45, "sawtooth", 0.11), i * 140);
    });
  }
}
window.StudioAudio = new SymphonicAudioEngine();
