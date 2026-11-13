class Studio3DRenderer {
  constructor() {
    this.portraitCache = new Map();
    this.heroRenderer = null;
    this.heroScene = null;
    this.heroCamera = null;
    this.heroGroup = null;
    this.palettes = {
      Terra: { p: 0xe67e22, e: 0xff5500 },
      Volt:  { p: 0x00e5ff, e: 0x0077ff },
      Solar: { p: 0xffc300, e: 0xff5733 },
      Void:  { p: 0x9b59b6, e: 0x6f1e51 },
      Cryo:  { p: 0x48dbfb, e: 0x0abde3 }
    };
  }
  init() {
    if (typeof THREE === "undefined") return;
    const off = document.createElement("canvas");
    off.width = 280; off.height = 210;
    const ren = new THREE.WebGLRenderer({ canvas: off, antialias: true, alpha: true });
    ren.setSize(280, 210);
    const sc = new THREE.Scene();
    const cam = new THREE.PerspectiveCamera(40, 280/210, 0.1, 50);
    cam.position.set(0, 0.55, 4.0); cam.lookAt(0, -0.1, 0);
    const l1 = new THREE.DirectionalLight(0xffffff, 2.2); l1.position.set(3, 5, 4);
    const l2 = new THREE.PointLight(0x00e5ff, 2.4, 12); l2.position.set(-3, 2, -2);
    sc.add(l1, l2, new THREE.AmbientLight(0x3a5078, 1.5));

    (window.STUDIO_ROSTER || []).forEach((u) => {
      const g = this.buildMesh(u);
      g.rotation.y = -0.35;
      sc.add(g);
      ren.render(sc, cam);
      this.portraitCache.set(u.id, off.toDataURL("image/png"));
      sc.remove(g);
    });
    ren.dispose();

    const hc = document.getElementById("hero-3d-canvas");
    if (!hc) return;
    this.heroRenderer = new THREE.WebGLRenderer({ canvas: hc, antialias: true, alpha: true });
    this.heroRenderer.setSize(hc.clientWidth || 300, hc.clientHeight || 175, false);
    this.heroScene = new THREE.Scene();
    this.heroCamera = new THREE.PerspectiveCamera(38, (hc.clientWidth||300)/(hc.clientHeight||175), 0.1, 50);
    this.heroCamera.position.set(0, 0.5, 4.0); this.heroCamera.lookAt(0, -0.1, 0);
    this.heroScene.add(l1.clone(), l2.clone(), new THREE.AmbientLight(0x3a5078, 1.5));
    this.setHeroOperative(window.STUDIO_ROSTER[0]);
    this.loop();
  }
  buildMesh(u) {
    const g = new THREE.Group();
    const pal = this.palettes[u.element] || this.palettes.Volt;
    const armorMat = new THREE.MeshStandardMaterial({ color: pal.p, metalness: 0.78, roughness: 0.22 });
    const darkMat = new THREE.MeshStandardMaterial({ color: 0x162032, metalness: 0.85, roughness: 0.3 });
    const glowMat = new THREE.MeshStandardMaterial({ color: pal.p, emissive: pal.e, emissiveIntensity: 1.3 });

    const base = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.3, 0.22, 20), darkMat);
    base.position.y = -1.2; g.add(base);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(1.18, 0.05, 12, 36), glowMat);
    ring.rotation.x = Math.PI/2; ring.position.y = -1.08; g.add(ring);

    const torso = new THREE.Mesh(
      u.armor === "Chitin Carapace" ? new THREE.SphereGeometry(0.9, 20, 16) : new THREE.BoxGeometry(1.3, 1.2, 0.88),
      armorMat
    );
    torso.position.y = -0.25; g.add(torso);

    if (u.armor === "Spiked Shell") {
      [-0.4, 0, 0.4].forEach((x) => {
        const sp = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.5, 6), glowMat);
        sp.position.set(x, 0.45, -0.3); g.add(sp);
      });
    }

    const head = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.55, 0.75), armorMat);
    head.position.set(0, 0.65, 0.22); g.add(head);
    const visor = new THREE.Mesh(new THREE.BoxGeometry(0.58, 0.16, 0.78), glowMat);
    visor.position.set(0, 0.68, 0.24); g.add(visor);

    [-0.85, 0.85].forEach((x) => {
      const w = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 1.25, 12), darkMat);
      w.rotation.x = Math.PI/2; w.position.set(x, 0.32, 0.28); g.add(w);
    });
    return g;
  }
  setHeroOperative(u) {
    if (!this.heroScene || !u) return;
    if (this.heroGroup) this.heroScene.remove(this.heroGroup);
    this.heroGroup = this.buildMesh(u);
    this.heroScene.add(this.heroGroup);
  }
  loop() {
    requestAnimationFrame(() => this.loop());
    if (!this.heroRenderer || !this.heroGroup) return;
    const t = Date.now() * 0.001;
    this.heroGroup.rotation.y = Math.sin(t * 0.85) * 0.55;
    this.heroRenderer.render(this.heroScene, this.heroCamera);
  }
  getPortraitURL(id) { return this.portraitCache.get(id) || ""; }
}
window.Studio3D = new Studio3DRenderer();
