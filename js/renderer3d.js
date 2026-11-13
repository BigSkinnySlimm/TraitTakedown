window.Renderer3D = (function() {
  let bakeRenderer = null;
  let bakeScene = null;
  let bakeCamera = null;
  const cache = {};

  // Live Interactive 3D Dossier Turntable State
  let liveRenderer = null;
  let liveScene = null;
  let liveCamera = null;
  let liveGroup = null;
  let liveAnimId = null;
  let isDragging = false;
  let prevX = 0;

  function ensureBakeEngine() {
    if (bakeRenderer || !window.THREE) return;
    bakeRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, preserveDrawingBuffer: true });
    bakeRenderer.setSize(240, 290);
    bakeRenderer.setPixelRatio(1);
    bakeRenderer.shadowMap.enabled = true;

    bakeScene = new THREE.Scene();
    bakeCamera = new THREE.PerspectiveCamera(34, 240 / 290, 0.1, 100);
    bakeCamera.position.set(0, 0.55, 5.3);
    bakeCamera.lookAt(0, 0.35, 0);
  }

  function setupStudioLighting(scene, palette) {
    const amb = new THREE.AmbientLight(0xffffff, 0.65);
    scene.add(amb);

    const keyLight = new THREE.DirectionalLight(0xfffbeb, 1.25);
    keyLight.position.set(3, 5, 4);
    scene.add(keyLight);

    const rimLight = new THREE.PointLight(palette ? palette[2] : 0x38bdf8, 2.2, 12);
    rimLight.position.set(-3, 2.5, -2.5);
    scene.add(rimLight);

    const fillLight = new THREE.DirectionalLight(0x93c5fd, 0.55);
    fillLight.position.set(-3, -1, 3);
    scene.add(fillLight);
  }

  // Builds a complete, trait-locked 3D Collectible Figurine Group in Three.js
  function buildFigurineMesh(fac, char) {
    const group = new THREE.Group();
    const t = char.traits;
    const idx = char.id;
    const arch = char.archetype;

    // Materials Palette
    const humanSkins = [0xffdcb8, 0xf3b886, 0xd48e58, 0x9c5c30, 0x693b1a];
    const suitColors = [0xe11d48, 0x0284c7, 0x16a34a, 0x7c3aed, 0xea580c, 0x0d9488, 0x2563eb];
    const suitHex = suitColors[(idx * 3 + 1) % suitColors.length];

    let skinHex = humanSkins[idx % humanSkins.length];
    let skinRough = 0.45;
    let skinMetal = 0.05;

    if (arch === "tortoise" || arch === "reptile") {
      skinHex = [0x22c55e, 0x16a34a, 0x4ade80, 0x0d9488][idx % 4];
      skinRough = 0.35;
    } else if (arch === "rat_sensei" || arch === "lupin_beast") {
      skinHex = [0x94a3b8, 0x78350f, 0x64748b, 0xa16207][idx % 4];
      skinRough = 0.65;
    } else if (arch === "boar") {
      skinHex = 0x9a3412;
      skinRough = 0.55;
    } else if (arch === "hare_fox") {
      skinHex = [0xf8fafc, 0xfb923c, 0xfde047, 0xf472b6][idx % 4];
    } else if (arch === "mech_droid") {
      skinHex = [0xcbd5e1, 0xfbbf24, 0x38bdf8, 0x94a3b8][idx % 4];
      skinRough = 0.2;
      skinMetal = 0.85;
    } else if (t.is_nonhuman) {
      skinHex = [0xa855f7, 0x38bdf8, 0xf43f5e, 0x4ade80][idx % 4];
    }

    const skinMat = new THREE.MeshStandardMaterial({ color: skinHex, roughness: skinRough, metalness: skinMetal });
    const suitMat = new THREE.MeshStandardMaterial({ color: suitHex, roughness: 0.4, metalness: 0.2 });
    const darkMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.3, metalness: 0.4 });
    const goldMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, roughness: 0.22, metalness: 0.88 });
    const steelMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.2, metalness: 0.9 });

    // =========================================================================
    // 1. TRAIT 10: GLOWING POWER AURA (3D Energy Torus Halo + Floating Crystals)
    // =========================================================================
    if (t.has_aura) {
      const auraMat = new THREE.MeshStandardMaterial({
        color: 0xfde047,
        emissive: 0xf59e0b,
        emissiveIntensity: 1.4,
        roughness: 0.1
      });
      const halo = new THREE.Mesh(new THREE.TorusGeometry(1.38, 0.06, 12, 36), auraMat);
      halo.position.set(0, 0.55, -0.55);
      group.add(halo);

      for (let i = 0; i < 6; i++) {
        const ang = (i / 6) * Math.PI * 2;
        const shard = new THREE.Mesh(new THREE.OctahedronGeometry(0.16, 0), auraMat);
        shard.position.set(Math.cos(ang) * 1.4, 0.55 + Math.sin(ang) * 1.1, -0.4);
        group.add(shard);
      }
    }

    // =========================================================================
    // 2. TORSO & TRAIT 8: HEAVY ARMOR OR 3D SPIKED TORTOISE CARAPACE SHELL
    // =========================================================================
    const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.85, 1.35, 20), t.has_armor ? steelMat : suitMat);
    torso.position.set(0, -0.68, 0);
    group.add(torso);

    if (arch === "tortoise" || (t.has_armor && fac.id === "turtles")) {
      // MASSIVE 3D SPIKED TORTOISE SHELL ON BACK + PLastron Chestplate!
      const shellMat = new THREE.MeshStandardMaterial({ color: 0x14532d, roughness: 0.35, metalness: 0.3 });
      const shell = new THREE.Mesh(new THREE.SphereGeometry(1.08, 20, 16), shellMat);
      shell.scale.set(1.05, 1.15, 0.75);
      shell.position.set(0, -0.35, -0.35);
      group.add(shell);

      // Gold Plastron Front Ribs
      const plastron = new THREE.Mesh(new THREE.BoxGeometry(0.88, 0.95, 0.35), goldMat);
      plastron.position.set(0, -0.65, 0.48);
      group.add(plastron);

      // 3D Conical Metallic Shell Spikes protruding around rim!
      const spikePositions = [
        [-0.88, 0.15, -0.25], [0.88, 0.15, -0.25],
        [-0.98, -0.35, -0.25], [0.98, -0.35, -0.25],
        [-0.75, 0.55, -0.35], [0.75, 0.55, -0.35],
        [0, 0.72, -0.4]
      ];
      spikePositions.forEach(([sx, sy, sz]) => {
        const spike = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.52, 10), goldMat);
        spike.position.set(sx, sy, sz);
        spike.rotation.z = sx > 0 ? -0.85 : sx < 0 ? 0.85 : 0;
        group.add(spike);
      });
    } else if (t.has_armor) {
      // Heavy 3D Shoulder Pauldrons + Glowing Chest Core
      [-0.82, 0.82].forEach((px) => {
        const pauldron = new THREE.Mesh(new THREE.SphereGeometry(0.42, 16, 14), steelMat);
        pauldron.scale.set(1.1, 0.85, 1.0);
        pauldron.position.set(px, -0.18, 0.08);
        group.add(pauldron);

        const pSpike = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.36, 8), goldMat);
        pSpike.position.set(px * 1.15, 0.15, 0.08);
        pSpike.rotation.z = px > 0 ? -0.5 : 0.5;
        group.add(pSpike);
      });
      const chestPlate = new THREE.Mesh(new THREE.BoxGeometry(0.96, 0.72, 0.45), goldMat);
      chestPlate.position.set(0, -0.55, 0.45);
      group.add(chestPlate);
    }

    // =========================================================================
    // 3. HEAD & SPECIES ANATOMY (TORTOISE, GATOR, BOAR, RAT SENSEI, MECH, HUMAN)
    // =========================================================================
    const headGroup = new THREE.Group();
    headGroup.position.set(0, 0.58, 0);
    group.add(headGroup);

    if (arch === "mech_droid") {
      const roboHead = new THREE.Mesh(new THREE.BoxGeometry(1.15, 1.1, 1.1), skinMat);
      headGroup.add(roboHead);
      const ant = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.55), goldMat);
      ant.position.set(0, 0.75, 0);
      headGroup.add(ant);
    } else {
      const cranium = new THREE.Mesh(new THREE.SphereGeometry(0.68, 24, 20), skinMat);
      cranium.scale.set(1.0, 1.06, 0.96);
      headGroup.add(cranium);
    }

    // Species-Specific 3D Snouts, Beaks, Ears & Horns
    if (arch === "tortoise") {
      // Sculpted 3D Turtle Snout / Upper Beak Ridge
      const snout = new THREE.Mesh(new THREE.SphereGeometry(0.38, 16, 12), skinMat);
      snout.scale.set(1.15, 0.72, 0.95);
      snout.position.set(0, -0.12, 0.52);
      headGroup.add(snout);
    } else if (arch === "reptile") {
      // Long 3D Alligator / Dragon Snout + Dorsal Spikes
      const gSnout = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.36, 0.75), skinMat);
      gSnout.position.set(0, -0.15, 0.58);
      headGroup.add(gSnout);
    } else if (arch === "rat_sensei" || arch === "lupin_beast" || arch === "hare_fox") {
      // 3D Furred Muzzle + Tall Species Ears
      const muzzle = new THREE.Mesh(new THREE.ConeGeometry(0.36, 0.58, 14), skinMat);
      muzzle.rotation.x = Math.PI / 2;
      muzzle.position.set(0, -0.12, 0.64);
      headGroup.add(muzzle);

      const noseTip = new THREE.Mesh(new THREE.SphereGeometry(0.1, 10, 10), darkMat);
      noseTip.position.set(0, -0.08, 0.92);
      headGroup.add(noseTip);

      const earH = arch === "hare_fox" ? 0.78 : 0.42;
      [-0.45, 0.45].forEach((ex) => {
        const ear = new THREE.Mesh(new THREE.ConeGeometry(0.2, earH, 12), skinMat);
        ear.position.set(ex, 0.68, -0.05);
        ear.rotation.z = ex > 0 ? -0.25 : 0.25;
        headGroup.add(ear);
      });
    } else if (arch === "boar") {
      // 3D Boar Snout Disc
      const bSnout = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.32, 0.35, 14), skinMat);
      bSnout.rotation.x = Math.PI / 2;
      bSnout.position.set(0, -0.12, 0.62);
      headGroup.add(bSnout);
    } else if (t.is_nonhuman) {
      // Curved 3D Demon/Alien Horns + Pointed Ears
      [-0.52, 0.52].forEach((hx) => {
        const horn = new THREE.Mesh(new THREE.ConeGeometry(0.14, 0.58, 10), goldMat);
        horn.position.set(hx, 0.62, 0.05);
        horn.rotation.z = hx > 0 ? -0.45 : 0.45;
        headGroup.add(horn);
      });
    }

    // 3D Eyes with Glowing Iris & Catchlights
    const eyeWhiteMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const pupilMat = new THREE.MeshBasicMaterial({ color: t.is_nonhuman ? 0xef4444 : 0x090d16 });
    [-0.25, 0.25].forEach((ex) => {
      const eye = new THREE.Mesh(new THREE.SphereGeometry(0.13, 14, 12), eyeWhiteMat);
      eye.scale.set(1.1, 0.95, 0.6);
      eye.position.set(ex, 0.08, 0.58);
      headGroup.add(eye);

      const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 10), pupilMat);
      pupil.position.set(ex, 0.08, 0.65);
      headGroup.add(pupil);
    });

    // =========================================================================
    // 4. TRAIT 6: EYEWEAR (3D Glowing Cyber Visor / Gold Spectacles)
    // =========================================================================
    if (t.has_eyewear) {
      const visorMat = new THREE.MeshStandardMaterial({
        color: 0x38bdf8,
        emissive: 0x0ea5e9,
        emissiveIntensity: 0.95,
        roughness: 0.1,
        transparent: true,
        opacity: 0.9
      });
      const visor = new THREE.Mesh(new THREE.BoxGeometry(0.96, 0.24, 0.35), visorMat);
      visor.position.set(0, 0.09, 0.58);
      headGroup.add(visor);
    }

    // =========================================================================
    // 5. TRAIT 7: BEARD / WHISKERS / TUSKS / CHIN SPIKES
    // =========================================================================
    if (t.has_beard) {
      if (arch === "tortoise" || arch === "reptile") {
        // 3D Spiked Chin Horns & Mandible Spikes for Spiked Tortoise!
        [-0.24, 0, 0.24].forEach((bx) => {
          const chinSpike = new THREE.Mesh(new THREE.ConeGeometry(0.11, 0.38, 10), goldMat);
          chinSpike.rotation.x = Math.PI * 0.85;
          chinSpike.position.set(bx, -0.45, 0.52);
          headGroup.add(chinSpike);
        });
      } else if (arch === "boar") {
        // Massive Curved 3D Ivory Boar Tusks
        [-0.28, 0.28].forEach((tx) => {
          const tusk = new THREE.Mesh(new THREE.ConeGeometry(0.1, 0.48, 10), steelMat);
          tusk.position.set(tx, -0.18, 0.72);
          tusk.rotation.x = -0.35;
          tusk.rotation.z = tx > 0 ? -0.3 : 0.3;
          headGroup.add(tusk);
        });
      } else {
        // Full 3D Sculpted Beard + Long Sensei Whiskers
        const beardMat = new THREE.MeshStandardMaterial({
          color: [0xe2e8f0, 0x475569, 0x9a3412, 0x1e293b][idx % 4],
          roughness: 0.6
        });
        const beard = new THREE.Mesh(new THREE.ConeGeometry(0.52, 0.82, 16), beardMat);
        beard.rotation.x = Math.PI;
        beard.position.set(0, -0.52, 0.35);
        headGroup.add(beard);

        [-0.45, 0.45].forEach((wx) => {
          const whisker = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.01, 0.65), steelMat);
          whisker.rotation.z = Math.PI / 2 + (wx > 0 ? -0.25 : 0.25);
          whisker.position.set(wx, -0.22, 0.62);
          headGroup.add(whisker);
        });
      }
    }

    // =========================================================================
    // 6. TRAIT 4 & 5: 3D HELMET / CROWN vs MYSTIC HOOD vs 3D SCULPTED HAIR
    // =========================================================================
    if (t.has_helmet) {
      const crown = new THREE.Mesh(new THREE.CylinderGeometry(0.66, 0.58, 0.42, 12), goldMat);
      crown.position.set(0, 0.58, 0);
      headGroup.add(crown);
      for (let i = 0; i < 6; i++) {
        const a = (i / 6) * Math.PI * 2;
        const pt = new THREE.Mesh(new THREE.ConeGeometry(0.14, 0.36, 8), goldMat);
        pt.position.set(Math.cos(a) * 0.58, 0.88, Math.sin(a) * 0.58);
        headGroup.add(pt);
      }
    } else if (t.has_hood) {
      const hoodMat = new THREE.MeshStandardMaterial({ color: 0x312e81, roughness: 0.5 });
      const hood = new THREE.Mesh(new THREE.SphereGeometry(0.82, 20, 16, 0, Math.PI * 2, 0, Math.PI * 0.72), hoodMat);
      hood.position.set(0, 0.12, -0.08);
      headGroup.add(hood);
    } else if (arch === "human") {
      // Sculpted 3D Hair Crown
      const hairColors = [0x0f172a, 0xb91c1c, 0xfacc15, 0x78350f, 0xe2e8f0, 0x7c3aed];
      const hairMat = new THREE.MeshStandardMaterial({ color: hairColors[idx % hairColors.length], roughness: 0.5 });
      const hairCap = new THREE.Mesh(new THREE.SphereGeometry(0.71, 18, 14, 0, Math.PI * 2, 0, Math.PI * 0.55), hairMat);
      hairCap.position.set(0, 0.08, -0.04);
      headGroup.add(hairCap);
    }

    // =========================================================================
    // 7. TRAITS 1, 2, 3: 3D FOREGROUND WEAPONS (BLADE, RANGED, BLUNT/STAFF)
    // =========================================================================
    if (t.has_blade) {
      const bladeGroup = new THREE.Group();
      bladeGroup.position.set(1.08, 0.05, 0.35);
      bladeGroup.rotation.z = 0.14;
      const bladeMat = new THREE.MeshStandardMaterial({
        color: 0xf43f5e,
        emissive: 0xe11d48,
        emissiveIntensity: 1.2,
        roughness: 0.15
      });
      const blade = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.08, 2.1, 12), bladeMat);
      blade.position.y = 0.45;
      bladeGroup.add(blade);
      const guard = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.1, 0.16), goldMat);
      guard.position.y = -0.58;
      bladeGroup.add(guard);
      group.add(bladeGroup);
    }

    if (t.has_ranged) {
      const gunGroup = new THREE.Group();
      gunGroup.position.set(-1.05, -0.15, 0.45);
      const barrel = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.14, 1.15, 12), steelMat);
      barrel.rotation.x = Math.PI / 4;
      gunGroup.add(barrel);
      const muzzleGlow = new THREE.Mesh(
        new THREE.SphereGeometry(0.16, 12, 12),
        new THREE.MeshStandardMaterial({ color: 0x38bdf8, emissive: 0x0ea5e9, emissiveIntensity: 1.5 })
      );
      muzzleGlow.position.set(0, 0.42, 0.42);
      gunGroup.add(muzzleGlow);
      group.add(gunGroup);
    }

    if (t.has_blunt) {
      // 3D Wooden Bo-Staff with Golden Rings & Warhammer Head
      const staffGroup = new THREE.Group();
      staffGroup.position.set(-1.08, 0.1, 0.38);
      staffGroup.rotation.z = -0.12;
      const woodMat = new THREE.MeshStandardMaterial({ color: 0x92400e, roughness: 0.55 });
      const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.085, 2.45, 12), woodMat);
      staffGroup.add(shaft);

      // Gold Staff Rings & Top Finial
      [-0.85, 0, 0.85, 1.15].forEach((ry) => {
        const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.115, 0.115, 0.12, 12), goldMat);
        ring.position.y = ry;
        staffGroup.add(ring);
      });

      if (!arch.includes("tortoise") && idx % 2 === 0) {
        const hammerHead = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.36, 0.36), steelMat);
        hammerHead.position.y = 0.95;
        staffGroup.add(hammerHead);
      }
      group.add(staffGroup);
    }

    return group;
  }

  // Bakes a high-contrast 3D WebGL Portrait DataURL in <15ms
  function renderCardPortrait(fac, char) {
    const key = `${fac.id}_${char.id}`;
    if (cache[key]) return cache[key];
    ensureBakeEngine();
    if (!bakeRenderer) return "";

    while (bakeScene.children.length > 0) {
      bakeScene.remove(bakeScene.children[0]);
    }
    bakeScene.background = new THREE.Color(fac.palette[0]);
    setupStudioLighting(bakeScene, fac.palette);

    const mesh = buildFigurineMesh(fac, char);
    mesh.rotation.y = (char.id % 2 === 0 ? 0.18 : -0.18);
    bakeScene.add(mesh);

    bakeRenderer.render(bakeScene, bakeCamera);
    const dataUrl = bakeRenderer.domElement.toDataURL("image/webp", 0.92);
    cache[key] = dataUrl;
    return dataUrl;
  }

  // Mounts an Interactive 60fps 3D Turntable inside the Dossier Modal
  function mountInteractiveTurntable(containerEl, fac, char) {
    stopInteractiveTurntable();
    if (!window.THREE || !containerEl) return;

    liveRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    liveRenderer.setSize(210, 230);
    liveRenderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    containerEl.innerHTML = `<div class="turntable-hint">⇄ Drag to Rotate 3D Figurine</div>`;
    containerEl.prepend(liveRenderer.domElement);

    liveScene = new THREE.Scene();
    liveCamera = new THREE.PerspectiveCamera(35, 210 / 230, 0.1, 100);
    liveCamera.position.set(0, 0.5, 5.4);
    liveCamera.lookAt(0, 0.3, 0);

    setupStudioLighting(liveScene, fac.palette);
    liveGroup = buildFigurineMesh(fac, char);
    liveScene.add(liveGroup);

    const canvas = liveRenderer.domElement;
    canvas.onpointerdown = (e) => { isDragging = true; prevX = e.clientX; };
    window.onpointerup = () => { isDragging = false; };
    canvas.onpointermove = (e) => {
      if (!isDragging || !liveGroup) return;
      const dx = e.clientX - prevX;
      prevX = e.clientX;
      liveGroup.rotation.y += dx * 0.018;
    };

    let t = 0;
    function animateTurntable() {
      liveAnimId = requestAnimationFrame(animateTurntable);
      t += 0.03;
      if (liveGroup) {
        if (!isDragging) liveGroup.rotation.y = Math.sin(t * 0.55) * 0.45;
        liveGroup.position.y = Math.sin(t * 1.5) * 0.05;
      }
      liveRenderer.render(liveScene, liveCamera);
    }
    animateTurntable();
  }

  function stopInteractiveTurntable() {
    if (liveAnimId) cancelAnimationFrame(liveAnimId);
    liveAnimId = null;
    if (liveRenderer) {
      liveRenderer.dispose();
      liveRenderer = null;
    }
  }

  return {
    renderCardPortrait,
    mountInteractiveTurntable,
    stopInteractiveTurntable
  };
})();
