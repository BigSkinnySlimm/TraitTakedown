window.StudioAudio = (function() {
  let ctx = null;
  let musicGain = null;
  let delayNode = null;
  let musicVol = 0.42;
  let sfxVol = 0.88;
  let hapticsOn = true;
  let seqTimer = null;
  let stepIdx = 0;
  let inArenaMode = false;

  function vibrate(ms = 10) {
    if (!hapticsOn) return;
    try { if (navigator.vibrate) navigator.vibrate(ms); } catch (e) {}
  }

  function init() {
    if (!ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return null;
      ctx = new AC();

      musicGain = ctx.createGain();
      musicGain.gain.value = musicVol;

      // Stereo Echo Delay for Studio Atmosphere
      delayNode = ctx.createDelay(1.0);
      delayNode.delayTime.value = 0.36;
      const fb = ctx.createGain();
      fb.gain.value = 0.28;
      const echoFilter = ctx.createBiquadFilter();
      echoFilter.type = "lowpass";
      echoFilter.frequency.value = 1100;

      delayNode.connect(echoFilter);
      echoFilter.connect(fb);
      fb.connect(delayNode);
      delayNode.connect(musicGain);
      musicGain.connect(ctx.destination);
    }
    if (ctx && ctx.state === "suspended") {
      ctx.resume();
    }
    if (ctx && !seqTimer) {
      startSoundtrackLoop();
    }
    return ctx;
  }

  // Auto-unlock audio & start music on very first user touch anywhere
  window.addEventListener("pointerdown", () => init(), { once: false });

  function playSynthTone(freq, type = "triangle", duration = 0.12, delay = 0, gainScale = 0.16) {
    const c = init();
    if (!c || sfxVol <= 0.01) return;
    const osc = c.createOscillator();
    const gain = c.createGain();
    const start = c.currentTime + delay;
    osc.type = type;
    osc.frequency.setValueAtTime(freq, start);
    gain.gain.setValueAtTime(gainScale * sfxVol, start);
    gain.gain.exponentialRampToValueAtTime(0.0008, start + duration);
    osc.connect(gain);
    gain.connect(c.destination);
    osc.start(start);
    osc.stop(start + duration);
  }

  // THE EXACT BELOVED CARD FLIP SOUND EFFECT (Domino pitch escalation + 110Hz body)
  function sfxCardSnap(step = 0) {
    vibrate(8);
    playSynthTone(240 + Math.min(step * 28, 360), "triangle", 0.06, 0, 0.14);
    playSynthTone(110, "sine", 0.04, 0, 0.18);
  }

  // Subtle Low-Pass Wooden/Tactile Tap (No harsh beep)
  function sfxTap() {
    vibrate(6);
    const c = init();
    if (!c || sfxVol <= 0.01) return;
    const now = c.currentTime;
    const osc = c.createOscillator();
    const gain = c.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(165, now);
    osc.frequency.exponentialRampToValueAtTime(55, now + 0.032);
    gain.gain.setValueAtTime(0.14 * sfxVol, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.032);
    osc.connect(gain);
    gain.connect(c.destination);
    osc.start(now);
    osc.stop(now + 0.032);
  }

  // Harmonized A-Minor9 Marimba Chord (In key with background music)
  function sfxYes() {
    vibrate([14, 28, 14]);
    [440, 523.25, 659.25, 783.99].forEach((f, i) => {
      playSynthTone(f, "triangle", 0.19, i * 0.055, 0.14);
    });
  }

  // Deep Warm Sub-Bass Drop (In key: E3 -> A2, zero harsh sawtooth buzzer)
  function sfxNo() {
    vibrate(25);
    const c = init();
    if (!c || sfxVol <= 0.01) return;
    const now = c.currentTime;
    const osc = c.createOscillator();
    const gain = c.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(164.81, now);
    osc.frequency.exponentialRampToValueAtTime(82.41, now + 0.22);
    gain.gain.setValueAtTime(0.22 * sfxVol, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.23);
    osc.connect(gain);
    gain.connect(c.destination);
    osc.start(now);
    osc.stop(now + 0.23);
  }

  function sfxWin() {
    vibrate([25, 40, 25, 40, 60]);
    [440, 523.25, 659.25, 880, 1046.5].forEach((f, i) => {
      playSynthTone(f, "triangle", 0.26, i * 0.08, 0.18);
    });
  }

  // Multi-Track Procedural Ambient Synth Soundtrack (Pad + Sub-Bass + Echo Arpeggio)
  function startSoundtrackLoop() {
    const prog = [
      { bass: 110.00, pad: [220.00, 261.63, 329.63, 392.00], arp: [440.00, 523.25, 659.25, 783.99] }, // Am7
      { bass: 87.31,  pad: [174.61, 220.00, 261.63, 329.63], arp: [349.23, 440.00, 523.25, 659.25] }, // Fmaj7
      { bass: 98.00,  pad: [196.00, 246.94, 293.66, 392.00], arp: [392.00, 493.88, 587.33, 783.99] }, // G
      { bass: 82.41,  pad: [164.81, 220.00, 246.94, 329.63], arp: [329.63, 440.00, 493.88, 659.25] }  // Em7
    ];

    seqTimer = setInterval(() => {
      if (!ctx || musicVol <= 0.01 || ctx.state !== "running") return;
      const now = ctx.currentTime;
      const bar = Math.floor(stepIdx / 8) % prog.length;
      const beat = stepIdx % 8;
      const cur = prog[bar];

      // 1. Warm Stereo Pad on Beat 0
      if (beat === 0) {
        cur.pad.forEach((freq) => {
          const osc = ctx.createOscillator();
          const flt = ctx.createBiquadFilter();
          const g = ctx.createGain();
          osc.type = "sawtooth";
          osc.frequency.setValueAtTime(freq, now);
          flt.type = "lowpass";
          flt.frequency.setValueAtTime(520, now);
          g.gain.setValueAtTime(0.001, now);
          g.gain.linearRampToValueAtTime(0.022, now + 0.6);
          g.gain.exponentialRampToValueAtTime(0.0008, now + 2.8);
          osc.connect(flt);
          flt.connect(g);
          g.connect(musicGain);
          osc.start(now);
          osc.stop(now + 2.85);
        });
      }

      // 2. Deep Sub-Bass Pulse on Beats 0 and 4
      if (beat === 0 || beat === 4) {
        const bOsc = ctx.createOscillator();
        const bGain = ctx.createGain();
        bOsc.type = "sine";
        bOsc.frequency.setValueAtTime(cur.bass, now);
        bGain.gain.setValueAtTime(0.001, now);
        bGain.gain.linearRampToValueAtTime(inArenaMode ? 0.09 : 0.065, now + 0.03);
        bGain.gain.exponentialRampToValueAtTime(0.001, now + 0.75);
        bOsc.connect(bGain);
        bGain.connect(musicGain);
        bOsc.start(now);
        bOsc.stop(now + 0.78);
      }

      // 3. Crystal Pluck Arpeggio with Stereo Delay Echo
      const arpNote = cur.arp[(stepIdx * 3) % cur.arp.length];
      const pOsc = ctx.createOscillator();
      const pGain = ctx.createGain();
      pOsc.type = "triangle";
      pOsc.frequency.setValueAtTime(arpNote, now);
      pGain.gain.setValueAtTime(0.001, now);
      pGain.gain.linearRampToValueAtTime(0.032, now + 0.015);
      pGain.gain.exponentialRampToValueAtTime(0.0005, now + 0.35);
      pOsc.connect(pGain);
      pGain.connect(delayNode);
      pGain.connect(musicGain);
      pOsc.start(now);
      pOsc.stop(now + 0.38);

      stepIdx++;
    }, 360);
  }

  return {
    init,
    sfxCardSnap,
    sfxTap,
    sfxYes,
    sfxNo,
    sfxWin,
    setArenaIntensity: (flag) => { inArenaMode = flag; },
    setVolumes: (m, s) => {
      musicVol = m;
      sfxVol = s;
      if (musicGain && ctx) musicGain.gain.setValueAtTime(musicVol, ctx.currentTime);
    },
    toggleHaptics: () => { hapticsOn = !hapticsOn; return hapticsOn; }
  };
})();
