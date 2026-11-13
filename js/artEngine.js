class StudioArtEngine {
  constructor() {
    this.cache = new Map();
    this.palettes = {
      Terra: { bg1: "#2c0e04", bg2: "#0d0608", main: "#e66817", hi: "#ffb84d", glow: "#ff4500", rim: "#ffd27f" },
      Volt:  { bg1: "#041c38", bg2: "#040814", main: "#00b4d8", hi: "#72efdd", glow: "#00f5ff", rim: "#b8fbff" },
      Solar: { bg1: "#3b2004", bg2: "#100804", main: "#f59e0b", hi: "#fef08a", glow: "#ffbe0b", rim: "#ffffff" },
      Void:  { bg1: "#1f0836", bg2: "#06030f", main: "#8b5cf6", hi: "#e9d5ff", glow: "#c026d3", rim: "#f5d0fe" },
      Cryo:  { bg1: "#06283d", bg2: "#030b17", main: "#38bdf8", hi: "#e0f2fe", glow: "#00e5ff", rim: "#ffffff" }
    };
  }

  bakeAll(roster) {
    roster.forEach((u, idx) => {
      this.cache.set(u.id, this.renderCardIllustration(u, idx));
    });
  }

  getArt(unitId) {
    return this.cache.get(unitId) || "";
  }

  renderCardIllustration(u, seedIdx) {
    const c = document.createElement("canvas");
    c.width = 400;
    c.height = 520;
    const ctx = c.getContext("2d");
    const pal = this.palettes[u.element] || this.palettes.Volt;

    // 1. Deep Atmospheric Environment Backdrop
    const bgGrad = ctx.createRadialGradient(200, 210, 20, 200, 260, 320);
    bgGrad.addColorStop(0, pal.glow + "55");
    bgGrad.addColorStop(0.45, pal.bg1);
    bgGrad.addColorStop(1, pal.bg2);
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, 400, 520);

    // Elemental Environment Geometry (Hex Grid / Sun Halo / Void Vortex / Lava Fissures)
    ctx.save();
    ctx.strokeStyle = pal.glow + "33";
    ctx.lineWidth = 1.5;
    for (let r = 50; r <= 230; r += 45) {
      ctx.beginPath();
      ctx.arc(200, 220, r, 0, Math.PI * 2);
      ctx.stroke();
    }
    // Energy Rays
    for (let a = 0; a < 12; a++) {
      const ang = (a / 12) * Math.PI * 2 + seedIdx * 0.2;
      ctx.beginPath();
      ctx.moveTo(200 + Math.cos(ang) * 40, 220 + Math.sin(ang) * 40);
      ctx.lineTo(200 + Math.cos(ang) * 240, 220 + Math.sin(ang) * 240);
      ctx.stroke();
    }
    ctx.restore();

    // 2. Back-Layer Weaponry & Silhouette Aura
    this.drawWeaponBackLayer(ctx, u, pal);

    // 3. Anatomically Distinct Species Body & Armor Layer
    if (u.species === "Reptilian") {
      this.drawReptilianBehemoth(ctx, u, pal);
    } else if (u.species === "Avian") {
      this.drawAvianSeraph(ctx, u, pal);
    } else if (u.species === "Cephalopod") {
      this.drawCephalopodKraken(ctx, u, pal);
    } else if (u.species === "Arachnid") {
      this.drawArachnidPredator(ctx, u, pal);
    } else {
      this.drawMechaTitan(ctx, u, pal);
    }

    // 4. Foreground Weaponry & Muzzle Energy Effects
    this.drawWeaponFrontLayer(ctx, u, pal);

    // 5. Floating Elemental Sparks & Rim Vignette
    this.drawParticlesAndFrame(ctx, u, pal, seedIdx);

    return c.toDataURL("image/png");
  }

  fillArmoredPoly(ctx, pts, fillCol, strokeCol, glowCol) {
    ctx.save();
    ctx.beginPath();
    pts.forEach((p, i) => (i === 0 ? ctx.moveTo(p[0], p[1]) : ctx.lineTo(p[0], p[1])));
    ctx.closePath();
    const g = ctx.createLinearGradient(120, 120, 280, 360);
    g.addColorStop(0, fillCol);
    g.addColorStop(1, "#0b1324");
    ctx.fillStyle = g;
    if (glowCol) {
      ctx.shadowColor = glowCol;
      ctx.shadowBlur = 14;
    }
    ctx.fill();
    ctx.shadowBlur = 0;
    ctx.strokeStyle = strokeCol;
    ctx.lineWidth = 2.5;
    ctx.stroke();
    ctx.restore();
  }

  drawReptilianBehemoth(ctx, u, pal) {
    // Dorsal Spikes if Spiked Shell
    if (u.armor === "Spiked Shell") {
      [[-85, 165], [-55, 115], [0, 90], [55, 115], [85, 165]].forEach(([dx, y]) => {
        this.fillArmoredPoly(
          ctx,
          [[200 + dx - 18, y + 60], [200 + dx * 1.35, y - 35], [200 + dx + 18, y + 60]],
          pal.hi, pal.rim, pal.glow
        );
      });
    }

    // Massive Tortoise / Drake Hexagonal Armored Carapace Dome
    this.fillArmoredPoly(
      ctx,
      [[75, 310], [95, 185], [150, 130], [250, 130], [305, 185], [325, 310], [270, 375], [130, 375]],
      pal.main, pal.hi, pal.glow
    );

    // Glowing Magma / Energy Scute Seams on Shell
    ctx.save();
    ctx.strokeStyle = pal.glow;
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 12;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(150, 130); ctx.lineTo(170, 240); ctx.lineTo(130, 375);
    ctx.moveTo(250, 130); ctx.lineTo(230, 240); ctx.lineTo(270, 375);
    ctx.moveTo(95, 240); ctx.lineTo(305, 240);
    ctx.stroke();
    ctx.restore();

    // Heavy Armored Clawed Forelegs
    this.fillArmoredPoly(ctx, [[80, 300], [55, 410], [125, 415], [140, 330]], "#1c2840", pal.hi, null);
    this.fillArmoredPoly(ctx, [[320, 300], [345, 410], [275, 415], [260, 330]], "#1c2840", pal.hi, null);

    // Fierce Snapping Reptilian / Tortoise Armored Head & Glowing Fangs
    this.fillArmoredPoly(
      ctx,
      [[145, 215], [200, 165], [255, 215], [240, 305], [200, 330], [160, 305]],
      "#131c31", pal.rim, pal.glow
    );

    // Glowing Slit Reptilian Eyes
    ctx.save();
    ctx.fillStyle = pal.rim;
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 15;
    ctx.beginPath();
    ctx.moveTo(162, 235); ctx.lineTo(190, 245); ctx.lineTo(168, 252); ctx.closePath();
    ctx.moveTo(238, 235); ctx.lineTo(210, 245); ctx.lineTo(232, 252); ctx.closePath();
    ctx.fill();
    ctx.restore();

    // Jagged Armored Jaw & Energy Vent
    this.fillArmoredPoly(
      ctx,
      [[160, 285], [180, 270], [200, 290], [220, 270], [240, 285], [225, 330], [175, 330]],
      pal.main, pal.hi, null
    );
  }

  drawAvianSeraph(ctx, u, pal) {
    // 6 Sweeping Layered Energy-Feathered Wings
    for (let side of [-1, 1]) {
      for (let w = 0; w < 3; w++) {
        const yOff = w * 48;
        this.fillArmoredPoly(
          ctx,
          [
            [200 + side * 35, 195 + yOff * 0.5],
            [200 + side * (185 - w * 18), 95 + yOff],
            [200 + side * (160 - w * 15), 165 + yOff],
            [200 + side * 45, 250 + yOff * 0.5]
          ],
          w === 0 ? pal.hi : pal.main, pal.rim, pal.glow
        );
      }
    }

    // Valkyrie / Seraph Radiant Halo Crest
    ctx.save();
    ctx.strokeStyle = pal.hi;
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 18;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(200, 155, 58, Math.PI * 1.1, Math.PI * 1.9);
    ctx.stroke();
    ctx.restore();

    // Sleek Armored Avian Chest & Pauldrons
    this.fillArmoredPoly(
      ctx,
      [[135, 220], [200, 195], [265, 220], [240, 385], [200, 415], [160, 385]],
      pal.main, pal.rim, pal.glow
    );

    // Crested Raptor / Valkyrie Helm & Golden Beak Visor
    this.fillArmoredPoly(
      ctx,
      [[168, 155], [200, 105], [232, 155], [220, 220], [200, 245], [180, 220]],
      "#152238", pal.hi, pal.glow
    );
    this.fillArmoredPoly(
      ctx,
      [[182, 178], [200, 170], [218, 178], [200, 232]],
      pal.hi, "#ffffff", pal.glow
    );
  }

  drawCephalopodKraken(ctx, u, pal) {
    // 6 Writhing Bioluminescent Tentacles
    ctx.save();
    for (let i = 0; i < 6; i++) {
      const side = i < 3 ? -1 : 1;
      const idx = i % 3;
      ctx.strokeStyle = pal.main;
      ctx.lineWidth = 18 - idx * 3;
      ctx.lineCap = "round";
      ctx.shadowColor = pal.glow;
      ctx.shadowBlur = 12;
      ctx.beginPath();
      ctx.moveTo(200 + side * 30, 280);
      ctx.bezierCurveTo(
        200 + side * (110 + idx * 35), 290 + idx * 25,
        200 + side * (165 - idx * 20), 380,
        200 + side * (85 + idx * 40), 435
      );
      ctx.stroke();
    }
    ctx.restore();

    // Ribbed Nautilus / Kraken Bio-Carapace Mantle
    this.fillArmoredPoly(
      ctx,
      [[125, 250], [110, 145], [200, 85], [290, 145], [275, 250], [235, 315], [165, 315]],
      pal.main, pal.hi, pal.glow
    );

    // Glowing Abyssal Eyes & Void Core
    ctx.save();
    ctx.fillStyle = pal.rim;
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 20;
    [[-38, 255, 12], [38, 255, 12], [0, 215, 22]].forEach(([dx, y, r]) => {
      ctx.beginPath();
      ctx.arc(200 + dx, y, r, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();
  }

  drawArachnidPredator(ctx, u, pal) {
    // 8 Articulated Razor Mechanical Spider Legs
    ctx.save();
    ctx.strokeStyle = pal.hi;
    ctx.lineWidth = 6;
    ctx.lineJoin = "bevel";
    for (let side of [-1, 1]) {
      for (let l = 0; l < 4; l++) {
        const yBase = 220 + l * 28;
        ctx.beginPath();
        ctx.moveTo(200 + side * 40, yBase);
        ctx.lineTo(200 + side * (145 + l * 12), yBase - 55 + l * 18);
        ctx.lineTo(200 + side * (175 - l * 8), yBase + 65);
        ctx.stroke();
      }
    }
    ctx.restore();

    // Segmented Arachnid Thorax & Stealth Carapace
    this.fillArmoredPoly(
      ctx,
      [[135, 240], [200, 145], [265, 240], [235, 370], [200, 405], [165, 370]],
      "#121c2e", pal.main, pal.glow
    );

    // 6 Glowing Compound Optic Lenses & Venom Mandibles
    ctx.save();
    ctx.fillStyle = "#ff2a5f";
    ctx.shadowColor = "#ff2a5f";
    ctx.shadowBlur = 14;
    [[-24, 215], [24, 215], [-38, 202], [38, 202], [-12, 198], [12, 198]].forEach(([dx, y]) => {
      ctx.beginPath();
      ctx.arc(200 + dx, y, 6.5, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();

    // Twin Scythe Mandibles
    this.fillArmoredPoly(ctx, [[155, 250], [130, 325], [175, 295]], pal.hi, "#fff", pal.glow);
    this.fillArmoredPoly(ctx, [[245, 250], [270, 325], [225, 295]], pal.hi, "#fff", pal.glow);
  }

  drawMechaTitan(ctx, u, pal) {
    // Broad Articulated Mecha Pauldrons
    this.fillArmoredPoly(ctx, [[55, 195], [135, 165], [150, 285], [70, 305]], pal.main, pal.hi, pal.glow);
    this.fillArmoredPoly(ctx, [[345, 195], [265, 165], [250, 285], [330, 305]], pal.main, pal.hi, pal.glow);

    // Heavy Armored Chassis & Reactor Core
    this.fillArmoredPoly(
      ctx,
      [[125, 195], [275, 195], [255, 385], [200, 415], [145, 385]],
      "#162238", pal.rim, pal.glow
    );

    // Chest Reactor Core
    ctx.save();
    ctx.fillStyle = pal.rim;
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 24;
    ctx.beginPath();
    ctx.arc(200, 285, 28, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // Mecha Head & V-Fin Crest
    this.fillArmoredPoly(ctx, [[162, 135], [238, 135], [228, 210], [172, 210]], pal.main, pal.hi, null);
    this.fillArmoredPoly(ctx, [[200, 145], [125, 95], [155, 145], [200, 162], [245, 145], [275, 95]], pal.hi, "#fff", pal.glow);

    // Glowing Cyber Visor
    ctx.save();
    ctx.fillStyle = "#00ff9d";
    ctx.shadowColor = "#00ff9d";
    ctx.shadowBlur = 16;
    ctx.fillRect(174, 165, 52, 12);
    ctx.restore();
  }

  drawWeaponBackLayer(ctx, u, pal) {
    if (u.weapon === "Plasma Cannon") {
      // Twin Shoulder-Mounted Heavy Artillery Cannons with Glowing Coils
      [[-95, -12], [95, 12]].forEach(([dx, rot]) => {
        ctx.save();
        ctx.translate(200 + dx, 145);
        ctx.rotate((rot * Math.PI) / 180);
        this.fillArmoredPoly(ctx, [[-22, -65], [22, -65], [26, 55], [-26, 55]], "#1b2842", pal.hi, pal.glow);
        ctx.fillStyle = pal.rim;
        ctx.shadowColor = pal.glow;
        ctx.shadowBlur = 18;
        ctx.beginPath();
        ctx.arc(0, -58, 14, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      });
    }
  }

  drawWeaponFrontLayer(ctx, u, pal) {
    ctx.save();
    if (u.weapon === "Solar Lance" || u.weapon === "Rail Rifle") {
      ctx.translate(200, 295);
      ctx.rotate(-0.38);
      this.fillArmoredPoly(ctx, [[-175, -10], [185, -14], [215, 0], [185, 14], [-175, 10]], pal.hi, "#fff", pal.glow);
    } else if (u.weapon === "Siege Hammer") {
      this.fillArmoredPoly(ctx, [[270, 125], [375, 125], [365, 215], [280, 215]], pal.main, pal.rim, pal.glow);
    } else if (u.weapon === "Venom Blade") {
      this.fillArmoredPoly(ctx, [[65, 340], [185, 245], [145, 365]], pal.hi, "#fff", pal.glow);
      this.fillArmoredPoly(ctx, [[335, 340], [215, 245], [255, 365]], pal.hi, "#fff", pal.glow);
    }
    ctx.restore();
  }

  drawParticlesAndFrame(ctx, u, pal, seed) {
    // Rising Embers / Energy Motes
    ctx.save();
    ctx.fillStyle = pal.rim;
    ctx.shadowColor = pal.glow;
    ctx.shadowBlur = 10;
    for (let p = 0; p < 18; p++) {
      const px = ((p * 73 + seed * 31) % 360) + 20;
      const py = ((p * 97 + seed * 43) % 440) + 30;
      const rad = (p % 3) + 1.5;
      ctx.beginPath();
      ctx.arc(px, py, rad, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();

    // Inner Metallic Bevel Frame
    ctx.strokeStyle = pal.hi + "88";
    ctx.lineWidth = 4;
    ctx.strokeRect(6, 6, 388, 508);
  }
}

window.StudioArt = new StudioArtEngine();
