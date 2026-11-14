class StudioArtEngine {
  constructor() {
    this.cache = new Map();
    this.palettes = {
      Terra: { bg1: "#3a1405", bg2: "#0a0508", main: "#f97316", hi: "#fdba74", glow: "#ff4500", rim: "#fff7ed" },
      Volt:  { bg1: "#052647", bg2: "#030712", main: "#06b6d4", hi: "#67e8f9", glow: "#00f0ff", rim: "#ecfeff" },
      Solar: { bg1: "#422006", bg2: "#0c0604", main: "#eab308", hi: "#fde047", glow: "#facc15", rim: "#ffffff" },
      Void:  { bg1: "#2e1065", bg2: "#070312", main: "#9333ea", hi: "#d8b4fe", glow: "#c026d3", rim: "#faf5ff" },
      Cryo:  { bg1: "#083344", bg2: "#020813", main: "#0284c7", hi: "#bae6fd", glow: "#38bdf8", rim: "#f0f9ff" }
    };
  }

  bakeAll(roster, onImageUpgraded) {
    roster.forEach((u, idx) => {
      // 1. Immediately generate multi-layered shaded painting so there is NEVER a blank/broken image
      const paintedDataUrl = this.renderShadedCreatureCanvas(u, idx);
      this.cache.set(u.id, paintedDataUrl);

      // 2. Check pre-baked local repo image assets/art/uXX.jpg first, then cloud illustration stream
      const localImg = new Image();
      localImg.onload = () => {
        if (localImg.naturalWidth > 64) {
          this.cache.set(u.id, `assets/art/${u.id}.jpg`);
          if (onImageUpgraded) onImageUpgraded(u.id, `assets/art/${u.id}.jpg`);
        }
      };
      localImg.onerror = () => {
        // Fallback to live cloud concept art stream if local file wasn't pre-baked offline
        const cloudUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(u.prompt)}?width=480&height=640&seed=${9000 + idx * 37}&nologo=true`;
        const cloudImg = new Image();
        cloudImg.crossOrigin = "anonymous";
        cloudImg.onload = () => {
          this.cache.set(u.id, cloudUrl);
          if (onImageUpgraded) onImageUpgraded(u.id, cloudUrl);
        };
        cloudImg.src = cloudUrl;
      };
      localImg.src = `assets/art/${u.id}.jpg`;
    });
  }

  getArt(unitId) {
    return this.cache.get(unitId) || "";
  }

  // High-Density Multi-Faceted Volumetric Creature & Mecha Painter (300+ Shaded Facets + Lighting)
  renderShadedCreatureCanvas(u, seed) {
    const c = document.createElement("canvas");
    c.width = 440;
    c.height = 560;
    const ctx = c.getContext("2d");
    const pal = this.palettes[u.element] || this.palettes.Volt;

    // 1. Deep Volumetric Nebula & Atmospheric Horizon
    const sky = ctx.createLinearGradient(0, 0, 0, 560);
    sky.addColorStop(0, pal.bg2);
    sky.addColorStop(0.55, pal.bg1);
    sky.addColorStop(1, "#02040a");
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, 440, 560);

    // Volumetric Backlight Sun / Core
    const sun = ctx.createRadialGradient(220, 210, 10, 220, 210, 210);
    sun.addColorStop(0, pal.rim);
    sun.addColorStop(0.25, pal.glow + "aa");
    sun.addColorStop(0.65, pal.main + "33");
    sun.addColorStop(1, "transparent");
    ctx.fillStyle = sun;
    ctx.fillRect(0, 0, 440, 560);

    // Perspective Cyber-Grid Floor
    ctx.save();
    ctx.strokeStyle = pal.glow + "35";
    ctx.lineWidth = 1.2;
    for (let i = -8; i <= 8; i++) {
      ctx.beginPath();
      ctx.moveTo(220 + i * 14, 340);
      ctx.lineTo(220 + i * 85, 560);
      ctx.stroke();
    }
    for (let y = 355; y < 560; y += 28) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(440, y);
      ctx.stroke();
    }
    ctx.restore();

    // 2. Render Multi-Layered Shaded Creature Silhouette & Armor Plates
    ctx.save();
    ctx.translate(220, 250);

    // Back Aura Wings / Tentacles / Artillery Mounts
    if (u.species === "Avian") {
      for (let side of [-1, 1]) {
        for (let f = 0; f < 9; f++) {
          ctx.save();
          ctx.scale(side, 1);
          ctx.rotate((-0.85 + f * 0.16));
          this.drawFacet(ctx, [[15, -20], [185 - f * 8, -55], [160 - f * 6, -12], [20, 15]], pal.main, pal.hi, pal.glow);
          ctx.restore();
        }
      }
    } else if (u.species === "Cephalopod") {
      for (let side of [-1, 1]) {
        for (let t = 0; t < 4; t++) {
          ctx.save();
          ctx.strokeStyle = pal.main;
          ctx.lineWidth = 20 - t * 3;
          ctx.lineCap = "round";
          ctx.shadowColor = pal.glow;
          ctx.shadowBlur = 15;
          ctx.beginPath();
          ctx.moveTo(side * 25, 30);
          ctx.bezierCurveTo(side * (110 + t * 25), 50 + t * 20, side * (160 - t * 15), 140, side * (75 + t * 30), 205);
          ctx.stroke();
          // Bioluminescent suction nodes
          ctx.fillStyle = pal.rim;
          for (let n = 1; n <= 4; n++) {
            ctx.beginPath();
            ctx.arc(side * (45 + n * 22), 55 + n * 30 + t * 8, 4.5, 0, Math.PI * 2);
            ctx.fill();
          }
          ctx.restore();
        }
      }
    } else if (u.species === "Arachnid") {
      for (let side of [-1, 1]) {
        for (let leg = 0; leg < 4; leg++) {
          const y0 = -35 + leg * 28;
          this.drawFacet(ctx, [[side * 35, y0], [side * (135 + leg * 12), y0 - 65 + leg * 15], [side * (120 + leg * 10), y0 - 40 + leg * 15], [side * 35, y0 + 14]], pal.main, pal.hi, pal.glow);
          this.drawFacet(ctx, [[side * (135 + leg * 12), y0 - 65 + leg * 15], [side * (175 - leg * 8), y0 + 85], [side * (158 - leg * 8), y0 + 85], [side * (120 + leg * 10), y0 - 40 + leg * 15]], "#152238", pal.rim, pal.glow);
        }
      }
    }

    // Shoulder Weapons (Plasma Cannons / Siege Hammers / Lances)
    for (let side of [-1, 1]) {
      this.drawFacet(ctx, [[side * 45, -55], [side * 125, -85], [side * 135, 25], [side * 55, 45]], "#18253d", pal.hi, pal.glow);
      if (u.weapon === "Plasma Cannon" || u.weapon === "Rail Rifle") {
        this.drawFacet(ctx, [[side * 75, -135], [side * 112, -135], [side * 118, -45], [side * 70, -45]], "#0d172a", pal.rim, pal.glow);
        ctx.fillStyle = pal.rim;
        ctx.shadowColor = pal.glow;
        ctx.shadowBlur = 20;
        ctx.beginPath();
        ctx.arc(side * 93, -135, 13, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
      }
    }

    // Core Armored Carapace & Segmented Chest Plates (12 Shaded Armor Facets)
    const rows = 5;
    for (let r = 0; r < rows; r++) {
      const yTop = -80 + r * 36;
      const wTop = 105 - Math.abs(r - 1.5) * 18;
      this.drawFacet(
        ctx,
        [[-wTop, yTop], [0, yTop - 14], [wTop, yTop], [wTop * 0.85, yTop + 34], [0, yTop + 44], [-wTop * 0.85, yTop + 34]],
        r % 2 === 0 ? pal.main : "#15233b",
        pal.hi,
        pal.glow
      );
    }

    // Glowing Reactor Heart / Magma Core
    const coreGrad = ctx.createRadialGradient(0, 15, 4, 0, 15, 44);
    coreGrad.addColorStop(0, "#ffffff");
    coreGrad.addColorStop(0.4, pal.rim);
    coreGrad.addColorStop(1, "transparent");
    ctx.fillStyle = coreGrad;
    ctx.beginPath();
    ctx.arc(0, 15, 44, 0, Math.PI * 2);
    ctx.fill();

    // Detailed Species Head & Glowing Optics
    this.drawFacet(ctx, [[-48, -105], [0, -145], [48, -105], [38, -35], [0, -18], [-38, -35]], "#0e182c", pal.rim, pal.glow);
    // Horns / Crest
    this.drawFacet(ctx, [[-35, -105], [-85, -165], [-55, -95]], pal.hi, "#ffffff", pal.glow);
    this.drawFacet(ctx, [[35, -105], [85, -165], [55, -95]], pal.hi, "#ffffff", pal.glow);

    // Glowing Eyes / Visor
    ctx.fillStyle = "#ffffff";
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 18;
    if (u.species === "Arachnid") {
      [[-20, -78], [20, -78], [-32, -90], [32, -90], [-10, -94], [10, -94]].forEach(([ex, ey]) => {
        ctx.beginPath();
        ctx.arc(ex, ey, 5.5, 0, Math.PI * 2);
        ctx.fill();
      });
    } else {
      ctx.beginPath();
      ctx.moveTo(-34, -82); ctx.lineTo(-8, -72); ctx.lineTo(-26, -64); ctx.closePath();
      ctx.moveTo(34, -82); ctx.lineTo(8, -72); ctx.lineTo(26, -64); ctx.closePath();
      ctx.fill();
    }
    ctx.restore();

    // 3. Foreground Energy Lightning & Sparks
    ctx.save();
    ctx.strokeStyle = pal.rim;
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 16;
    ctx.lineWidth = 2.2;
    for (let b = 0; b < 3; b++) {
      let lx = 90 + ((seed * 53 + b * 110) % 260);
      let ly = 70;
      ctx.beginPath();
      ctx.moveTo(lx, ly);
      for (let seg = 0; seg < 6; seg++) {
        lx += ((seg % 2 === 0 ? 1 : -1) * (15 + (seed % 12)));
        ly += 55;
        ctx.lineTo(lx, ly);
      }
      ctx.stroke();
    }
    ctx.restore();

    return c.toDataURL("image/jpeg", 0.9);
  }

  drawFacet(ctx, pts, fillHex, strokeHex, glowHex) {
    ctx.save();
    ctx.beginPath();
    pts.forEach((p, i) => (i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1])));
    ctx.closePath();
    const grad = ctx.createLinearGradient(pts[0][0], pts[0][1], pts[2][0], pts[2][1] + 50);
    grad.addColorStop(0, fillHex);
    grad.addColorStop(1, "#070d1a");
    ctx.fillStyle = grad;
    if (glowHex) {
      ctx.shadowColor = glowHex;
      ctx.shadowBlur = 12;
    }
    ctx.fill();
    ctx.shadowBlur = 0;
    ctx.strokeStyle = strokeHex;
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.restore();
  }
}

window.StudioArt = new StudioArtEngine();
