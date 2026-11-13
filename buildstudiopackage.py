import os
import shutil

FILES = {}

# ==============================================================================
# 1. MANIFEST.JSON
# ==============================================================================
FILES["manifest.json"] = """{
  "name": "Trait Takedown: 3D Tactical Deduction",
  "short_name": "Trait Takedown",
  "description": "AAA 3D WebGL collectible character deduction game with 9 factions, interactive 3D figurines, live friend duels, and global leaderboards.",
  "start_url": "/TraitTakedown/index.html",
  "scope": "/TraitTakedown/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#05070f",
  "theme_color": "#05070f",
  "categories": ["games", "board", "strategy"]
}
"""

# ==============================================================================
# 2. CSS/STUDIO.CSS (ZERO-CLIPPING VIEWPORT, HOLOGRAPHIC FOIL, ACCESSIBILITY)
# ==============================================================================
FILES["css/studio.css"] = """
:root {
  --bg-0: #04060d;
  --bg-1: #0b1222;
  --bg-2: #162444;
  --panel: rgba(15, 23, 42, 0.9);
  --panel-solid: #0f172a;
  --border: rgba(148, 163, 184, 0.22);
  --border-hi: rgba(56, 189, 248, 0.55);
  --primary: #0ea5e9;
  --primary-hi: #38bdf8;
  --gold: #f59e0b;
  --gold-hi: #fde047;
  --crimson: #e11d48;
  --crimson-hi: #fb7185;
  --emerald: #10b981;
  --emerald-hi: #34d399;
  --violet: #8b5cf6;
  --text: #f8fafc;
  --muted: #94a3b8;
  --card-trim: #38bdf8;
}

body.theme-crimson {
  --bg-0: #090205; --bg-1: #1c0710; --bg-2: #360c1c;
  --panel: rgba(36, 10, 20, 0.9); --panel-solid: #220913;
  --primary: #e11d48; --primary-hi: #fb7185;
  --border-hi: rgba(251, 113, 133, 0.55); --card-trim: #fb7185;
}
body.theme-emerald {
  --bg-0: #020907; --bg-1: #061d16; --bg-2: #0b3427;
  --panel: rgba(8, 34, 25, 0.9); --panel-solid: #072018;
  --primary: #10b981; --primary-hi: #34d399;
  --border-hi: rgba(52, 211, 153, 0.55); --card-trim: #34d399;
}
body.theme-royal {
  --bg-0: #070410; --bg-1: #160d2e; --bg-2: #291754;
  --panel: rgba(26, 15, 52, 0.9); --panel-solid: #1a0f34;
  --primary: #f59e0b; --primary-hi: #fde047;
  --border-hi: rgba(253, 224, 71, 0.55); --card-trim: #fde047;
}
body.theme-amoled {
  --bg-0: #000000; --bg-1: #040508; --bg-2: #0b0f17;
  --panel: rgba(10, 12, 18, 0.96); --panel-solid: #07090e;
}

body.high-contrast {
  --border: rgba(255, 255, 255, 0.55);
  --border-hi: #fde047;
  --muted: #e2e8f0;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

body {
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
  background: radial-gradient(circle at 50% 0%, var(--bg-2) 0%, var(--bg-1) 50%, var(--bg-0) 100%);
  color: var(--text);
  height: 100dvh;
  width: 100vw;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

h1, h2, h3, .display-font {
  font-family: 'Chakra Petch', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

#fxCanvas {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 2;
}

svg.ico { width: 17px; height: 17px; fill: currentColor; flex-shrink: 0; }
svg.ico-lg { width: 21px; height: 21px; fill: currentColor; flex-shrink: 0; }

/* Tactile 3D Studio Buttons */
.btn {
  font-family: 'Chakra Petch', sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 1px solid rgba(255, 255, 255, 0.26);
  border-radius: 11px;
  padding: 10px 14px;
  font-size: 0.84rem;
  color: #fff;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  transition: transform 0.1s ease, filter 0.15s ease;
}
.btn:active { transform: translateY(2px) scale(0.98); }
.btn:disabled { opacity: 0.35; pointer-events: none; }

.btn-primary { background: linear-gradient(180deg, var(--primary-hi) 0%, var(--primary) 100%); box-shadow: 0 3px 0 rgba(0,0,0,0.55); color: #031120; }
.btn-gold { background: linear-gradient(180deg, #fde047 0%, #f59e0b 100%); box-shadow: 0 3px 0 #78350f; color: #230d01; }
.btn-crimson { background: linear-gradient(180deg, #fb7185 0%, #e11d48 100%); box-shadow: 0 3px 0 #881337; color: #fff; }
.btn-emerald { background: linear-gradient(180deg, #34d399 0%, #059669 100%); box-shadow: 0 3px 0 #064e3b; color: #022c22; }
.btn-slate { background: linear-gradient(180deg, #334155 0%, #1e293b 100%); box-shadow: 0 3px 0 #090d16; color: #e2e8f0; }

/* Incoming Challenge Banner */
.challenge-banner {
  position: fixed;
  top: 12px;
  left: 50%;
  transform: translate(-50%, -160%);
  z-index: 160;
  background: linear-gradient(135deg, #1e293b, #0f172a);
  border: 2px solid var(--gold-hi);
  border-radius: 16px;
  padding: 12px 16px;
  max-width: 420px;
  width: 92vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.85);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.challenge-banner.show { transform: translate(-50%, 0); }

/* Persistent Top Header */
.app-header {
  flex-shrink: 0;
  background: rgba(4, 6, 13, 0.92);
  border-bottom: 1px solid var(--border);
  padding: 8px 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 30;
}

.profile-pill {
  display: flex; align-items: center; gap: 9px;
  background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
  border-radius: 11px; padding: 4px 10px 4px 5px; cursor: pointer;
}
.profile-avatar {
  width: 32px; height: 32px; border-radius: 8px;
  background: linear-gradient(135deg, var(--primary-hi), var(--violet));
  display: flex; align-items: center; justify-content: center;
  font-family: 'Chakra Petch', sans-serif; font-weight: 700; color: #fff; position: relative;
}
.online-dot {
  position: absolute; bottom: -2px; right: -2px; width: 9px; height: 9px;
  border-radius: 50%; background: var(--emerald-hi); border: 2px solid var(--bg-0);
}
.profile-meta strong { display: block; font-size: 0.8rem; }
.profile-meta span { font-size: 0.65rem; color: var(--gold-hi); font-weight: 700; }

.currency-cluster { display: flex; gap: 7px; align-items: center; }
.currency-pill {
  display: flex; align-items: center; gap: 5px;
  background: rgba(0, 0, 0, 0.55); border: 1px solid var(--border);
  padding: 5px 10px; border-radius: 9px;
  font-family: 'Chakra Petch', sans-serif; font-weight: 700; font-size: 0.82rem; cursor: pointer;
}
.currency-pill.gold { border-color: rgba(245, 158, 11, 0.5); color: var(--gold-hi); }
.currency-pill.mmr { border-color: rgba(56, 189, 248, 0.5); color: var(--primary-hi); }

/* Lobby Scrollable Views */
.tab-view {
  display: none;
  flex: 1;
  overflow-y: auto;
  padding: 12px 14px 86px;
  max-width: 1040px;
  width: 100%;
  margin: 0 auto;
  position: relative;
  z-index: 5;
}
.tab-view.active { display: block; }

/* ==============================================================
   ZERO-CLIPPING, ZERO-SCROLL FULLSCREEN GAMEPLAY ARENA
   ============================================================== */
#arenaView {
  display: none;
  flex-direction: column;
  height: 100dvh;
  width: 100vw;
  max-width: 980px;
  margin: 0 auto;
  padding: 6px 8px calc(8px + env(safe-area-inset-bottom));
  overflow: hidden;
  gap: 5px;
  position: relative;
  z-index: 10;
}
#arenaView.active { display: flex; }

.arena-top-bar {
  flex-shrink: 0;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 5px 10px;
  display: grid;
  grid-template-columns: 1.2fr auto 1.2fr;
  align-items: center;
  gap: 6px;
}

.secret-chip { display: flex; align-items: center; gap: 7px; cursor: pointer; }
.secret-chip img {
  width: 36px; height: 44px; border-radius: 7px;
  border: 1.5px solid var(--gold-hi); object-fit: cover; background: #000;
}

.arena-status-strip {
  flex-shrink: 0;
  background: linear-gradient(90deg, rgba(14, 165, 233, 0.22), rgba(139, 92, 246, 0.22));
  border: 1px solid var(--border-hi);
  border-radius: 10px;
  padding: 5px 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  font-size: 0.7rem;
  font-weight: 700;
}

.intel-consumables { display: flex; gap: 4px; flex-shrink: 0; align-items: center; }
.intel-btn {
  background: rgba(15, 23, 42, 0.92);
  border: 1px solid var(--gold);
  color: var(--gold-hi);
  border-radius: 7px;
  padding: 4px 6px;
  font-family: 'Chakra Petch', sans-serif;
  font-size: 0.64rem;
  font-weight: 700;
  cursor: pointer;
}
.intel-btn.skill-ready {
  background: linear-gradient(180deg, #fde047, #f59e0b);
  color: #230d01;
  border-color: #fff;
}

/* 4x6 Grid Locked to Viewport Height (All 24 Cards Fit Simultaneously) */
.board-grid-24 {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(6, 1fr);
  gap: 5px;
  perspective: 1000px;
}
@media (min-width: 640px) {
  .board-grid-24 {
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(4, 1fr);
    gap: 8px;
  }
}

.card-cell {
  width: 100%;
  height: 100%;
  min-height: 0;
  position: relative;
  perspective: 800px;
}

.game-card {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.45s cubic-bezier(0.34, 1.45, 0.64, 1);
  cursor: pointer;
}
.game-card.eliminated { transform: rotateY(180deg) scale(0.94); }
.game-card.target-glow .card-face-front {
  border-color: var(--crimson-hi);
  box-shadow: 0 0 14px rgba(244, 63, 94, 0.9);
}
.game-card.foil-upgraded .card-face-front {
  border-color: var(--gold-hi);
  box-shadow: 0 0 14px rgba(253, 224, 71, 0.55);
}

.card-face-front, .card-face-back {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border-radius: 9px;
  overflow: hidden;
}

.card-face-front {
  background: linear-gradient(165deg, #1e293b 0%, #090d16 100%);
  border: 2px solid var(--card-trim);
  display: flex;
  flex-direction: column;
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.6);
}

.card-face-front::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(125deg, transparent 36%, rgba(255, 255, 255, 0.1) 48%, rgba(56, 189, 248, 0.12) 52%, transparent 64%);
  background-size: 220% 220%;
  animation: foilSweep 6s infinite linear;
  pointer-events: none;
}
@keyframes foilSweep {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.card-portrait-wrap {
  flex: 1;
  min-height: 0;
  position: relative;
  background: radial-gradient(circle at 50% 35%, #1e293b, #050811);
  overflow: hidden;
}
.card-portrait-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  display: block;
}

.inspect-corner {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 20px;
  height: 20px;
  border-radius: 5px;
  background: rgba(5, 8, 17, 0.84);
  border: 1px solid rgba(255, 255, 255, 0.42);
  color: var(--primary-hi);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 4;
}

.trait-pip-row {
  position: absolute;
  bottom: 2px;
  left: 3px;
  display: flex;
  gap: 2px;
  z-index: 3;
  background: rgba(5, 8, 17, 0.72);
  padding: 1.5px 3px;
  border-radius: 4px;
}
.trait-pip {
  width: 5.5px;
  height: 5.5px;
  border-radius: 50%;
}

.card-title-plate {
  flex-shrink: 0;
  background: rgba(6, 9, 19, 0.96);
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  padding: 2px 3px;
  text-align: center;
  font-family: 'Chakra Petch', sans-serif;
  font-weight: 700;
  font-size: 0.58rem;
  color: #f8fafc;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-face-back {
  transform: rotateY(180deg);
  background: radial-gradient(circle at center, #1e293b 0%, #05070f 100%);
  border: 1.5px solid #334155;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #475569;
  font-family: 'Chakra Petch', sans-serif;
  font-size: 0.54rem;
  font-weight: 700;
}

.arena-bottom-dock {
  flex-shrink: 0;
  display: flex;
  gap: 6px;
}

/* Interactive 3D Turntable Stage inside Dossier Modal */
.turntable-stage {
  width: 210px;
  height: 230px;
  margin: 4px auto 10px;
  border-radius: 16px;
  overflow: hidden;
  border: 2.5px solid var(--primary-hi);
  background: radial-gradient(circle at 50% 35%, #1e293b 0%, #05070f 100%);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.75);
  position: relative;
  touch-action: none;
  cursor: grab;
}
.turntable-stage canvas {
  width: 100% !important;
  height: 100% !important;
  display: block;
}
.turntable-hint {
  position: absolute;
  bottom: 5px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 0.62rem;
  font-weight: 800;
  color: var(--gold-hi);
  text-transform: uppercase;
  pointer-events: none;
  text-shadow: 0 1px 3px #000;
}

/* Lobby Boxes & Grids */
.glass-box {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 14px;
  margin-bottom: 12px;
}

.mode-grid-5 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 10px;
}
@media (min-width: 680px) { .mode-grid-5 { grid-template-columns: repeat(5, 1fr); } }

.mode-tile {
  background: rgba(9, 14, 28, 0.85);
  border: 1.5px solid var(--border);
  border-radius: 12px;
  padding: 10px;
  cursor: pointer;
  transition: transform 0.14s, border-color 0.14s;
}
.mode-tile:hover { transform: translateY(-2px); border-color: var(--primary-hi); }

.missions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 8px;
  margin-top: 8px;
}
.mission-box {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 8px 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.74rem;
}
.mission-box.done { border-color: var(--emerald); background: rgba(16, 185, 129, 0.12); }

.faction-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 10px;
}
.faction-card {
  background: var(--panel);
  border: 2px solid var(--border);
  border-radius: 14px;
  padding: 10px;
  display: flex;
  gap: 10px;
  align-items: center;
  cursor: pointer;
  transition: transform 0.14s, border-color 0.14s;
}
.faction-card:hover { transform: translateY(-2px); }
.faction-card.selected { border-color: var(--primary-hi); background: rgba(14, 165, 233, 0.15); }
.faction-card img {
  width: 62px; height: 76px; border-radius: 9px; object-fit: cover;
  border: 1.5px solid rgba(255,255,255,0.25); background: #000; flex-shrink: 0;
}

/* Bottom Nav */
.bottom-dock {
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 40;
  background: rgba(4, 6, 13, 0.96); border-top: 1px solid var(--border);
  display: flex; justify-content: center;
  padding: 5px 8px calc(6px + env(safe-area-inset-bottom));
}
.dock-inner { display: grid; grid-template-columns: repeat(5, 1fr); max-width: 620px; width: 100%; gap: 4px; }
.nav-tab {
  background: transparent; border: none; color: var(--muted);
  padding: 6px 4px; border-radius: 10px; display: flex; flex-direction: column; align-items: center; gap: 3px;
  font-size: 0.65rem; font-weight: 800; text-transform: uppercase; cursor: pointer;
}
.nav-tab.active { color: var(--primary-hi); background: rgba(56, 189, 248, 0.12); }

/* Modals */
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(3, 6, 14, 0.88); backdrop-filter: blur(6px);
  display: none; align-items: center; justify-content: center; padding: 14px; z-index: 100;
}
.modal-backdrop.open { display: flex; }
.modal-panel {
  background: var(--panel-solid); border: 2px solid var(--border-hi); border-radius: 20px;
  max-width: 500px; width: 100%; padding: 16px; max-height: 92dvh; overflow-y: auto;
}

.q-btn {
  width: 100%; background: rgba(255,255,255,0.05); border: 1.5px solid var(--border);
  border-radius: 11px; padding: 9px 12px; color: #fff; display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 6px; cursor: pointer; font-size: 0.8rem; font-weight: 700; text-align: left;
}
.q-btn:hover { border-color: var(--primary-hi); background: rgba(14, 165, 233, 0.14); }
.q-btn.optimal { border-color: var(--gold-hi); background: rgba(245, 158, 11, 0.18); }
.q-btn.asked { opacity: 0.35; }

.row-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 9px 11px; background: rgba(0,0,0,0.35); border: 1px solid var(--border);
  border-radius: 10px; margin-bottom: 6px; font-size: 0.78rem;
}

.toast-banner {
  position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) scale(0.8);
  background: rgba(6, 9, 19, 0.96); border: 2px solid var(--primary-hi); border-radius: 18px;
  padding: 16px 22px; text-align: center; z-index: 150; pointer-events: none; opacity: 0;
  transition: transform 0.2s ease, opacity 0.18s ease; box-shadow: 0 20px 50px rgba(0,0,0,0.85);
}
.toast-banner.show { opacity: 1; transform: translate(-50%, -50%) scale(1); }
"""

# ==============================================================================
# 3. JS/DATA.JS (10 TRAITS, 9 FACTIONS, 216 ANATOMY-MAPPED OPERATIVES)
# ==============================================================================
FILES["js/data.js"] = """
window.TRAIT_SCHEMA = [
  { key: "has_blade",   label: "Bladed Sword / Katana",      q: "wield a Bladed Sword or Katana",          color: "#f43f5e", sym: "▲" },
  { key: "has_ranged",  label: "Blaster / Bow / Wand",       q: "carry a Blaster, Bow, or Wand",           color: "#38bdf8", sym: "◆" },
  { key: "has_blunt",   label: "Staff / Hammer / Shield",    q: "hold a Staff, Hammer, or Shield",         color: "#f59e0b", sym: "■" },
  { key: "has_helmet",  label: "Helmet / Crown / Hat",       q: "wear a Helmet, Crown, or Hat",            color: "#fbbf24", sym: "★" },
  { key: "has_hood",    label: "Mystic Hood / Cloak",        q: "wear a Mystic Hood or Cloak",             color: "#818cf8", sym: "●" },
  { key: "has_eyewear", label: "Visor / Glasses / Eyepatch", q: "wear a Visor, Glasses, or Eyepatch",      color: "#06b6d4", sym: "◈" },
  { key: "has_beard",   label: "Beard / Whiskers / Tusks",   q: "have a Beard, Whiskers, or Tusks",        color: "#a855f7", sym: "▼" },
  { key: "has_armor",   label: "Heavy Armor / Spiked Shell", q: "wear Heavy Armor or a Spiked Shell",      color: "#94a3b8", sym: "⬟" },
  { key: "is_nonhuman", label: "Non-Human / Mutant / Mech",  q: "belong to a Non-Human or Mutant species", color: "#4ade80", sym: "✦" },
  { key: "has_aura",    label: "Glowing Power Aura",         q: "radiate a Glowing Power Aura",            color: "#fde047", sym: "☀" }
];

window.RAW_FACTIONS = [
  {
    id: "galactic", name: "Starlight Outlaws", desc: "Space Knights & Bounty Hunters",
    free: true, price: 0, perkName: "Orbital Scan",
    perkDesc: "Highlights the mathematically optimal 50/50 trait question",
    palette: [0x090d1a, 0x1e3a8a, 0x38bdf8],
    names: [
      "Lord Obsidian", "Lucas Starstrider", "Master Solis", "Princess Vesper", "Captain Dash", "Ursa Fang",
      "Apex Tracker", "Chrome Nomad", "Elder Moss", "Count Severus", "General Gearheart", "Templar Violet",
      "Kira Dune", "Vane Crossguard", "Astra Twinblade", "Emperor Volt", "Baron Velvet", "Grand Marshal Iron",
      "Admiral Coral", "Crimson Horn", "Master Qorin", "Empress Aura", "Rover-02", "Unit-99 Gold"
    ]
  },
  {
    id: "turtles", name: "Sewer Shinobi", desc: "Mutant Ninjas & Urban Vigilantes",
    free: true, price: 0, perkName: "Smoke Snipe",
    perkDesc: "Instantly eliminates 2 innocent suspects without using your turn",
    palette: [0x041f11, 0x15803d, 0x4ade80],
    names: [
      "Azure Katana", "Crimson Sai", "Amber Nunchuck", "Violet Bo-Staff", "Sensei Whiskers", "Reporter Paige",
      "Vigilante Puck", "Iron Talon", "Tusker Boar", "Granite Horn", "Cerebro Mech", "Viper Lotus",
      "Doctor Mutator", "Razor Snapper", "Bayou Gator", "Chrome Terrapin", "Jade Gecko", "Sewer Monarch",
      "Ronin Hare", "Shadow Automaton", "Skater Lizard", "Spiked Tortoise", "Feral Lupin", "Canary Shinobi"
    ]
  },
  {
    id: "rangers", name: "Chroma Squadron", desc: "Sentai Pilots & Mecha Defenders",
    free: true, price: 0, perkName: "Mecha Lock",
    perkDesc: "Skips your opponent's next turn completely",
    palette: [0x2a0606, 0xb91c1c, 0xfacc15],
    names: [
      "Red Rex Pilot", "Emerald Wyvern", "Ivory Tiger", "Rose Ptero", "Cobalt Tricera", "Onyx Mammoth",
      "Solar Saber", "Empress Eclipse", "Lord Chrome", "Winged Sphinx", "Unit Alpha-5", "Sage Beacon",
      "Bruiser Bulk", "Jester Spike", "Mercury Astro", "Aurum Zeo", "Phantom Hound", "Crimson Thunder",
      "Quantum Rex", "Taurus Defender", "Chaos Red", "Stinger Vixen", "Clay Sculptor", "Shinobi Azure"
    ]
  },
  {
    id: "sorcery", name: "Arcane Academy", desc: "Wizards, Wands & Mystic Houses",
    free: true, price: 0, perkName: "Scrying Lens",
    perkDesc: "Reveals 1 true trait of your opponent's secret operative",
    palette: [0x141138, 0x4c1d95, 0xc084fc],
    names: [
      "Gideon Bolt", "Rowan Copper", "Clara Grimoire", "Julian Silver", "Headmaster Aldous", "Master Nightshade",
      "Lord Hollow", "Morgana Hex", "Bramble Giant", "Padfoot Hound", "Professor Howl", "Pip House-Imp",
      "Barnaby Root", "Astrid Spectacles", "Finley Champion", "Minerva Lynx", "Mad-Lens Sentry", "Cassius Cane",
      "Scarlet Striker", "Felix Jester", "Jasper Prank", "Lin Seeker", "Viktor Storm", "Genevieve Swan"
    ]
  },
  {
    id: "pirates", name: "High Seas Corsairs", desc: "Swashbucklers & Cursed Admirals",
    free: false, price: 1500, perkName: "Broadside Volley",
    perkDesc: "Eliminates 3 innocent suspects on the board immediately",
    palette: [0x171310, 0x78350f, 0xfbbf24],
    names: [
      "Capt. Sparrowhawk", "Kraken Warden", "Capt. Redbeard", "William Forge", "Corsair Queen", "Commodore Powder",
      "Bosun Barrel", "Mystic Calypso", "Barnacle Bill", "One-Eye Patch", "Timber Pete", "Admiral Blacksmoke",
      "Sirena Cutlass", "Phantom Galleon", "Governor Sterling", "Silent Mate", "Capuchin Thief", "Shorty Anchor",
      "Helmswoman Maria", "Sentry Redcoat", "Guard Bayonet", "Dragon Corsair", "Rajah Bengal", "Baron Dubloon"
    ]
  },
  {
    id: "defenders", name: "Vanguard Heroes", desc: "Superheroes & Cosmic Titans",
    free: false, price: 2000, perkName: "Aegis Pulse",
    perkDesc: "Highlights optimal 50/50 split + grants +15 Bonus Coins",
    palette: [0x082f49, 0x0284c7, 0x38bdf8],
    names: [
      "Cobalt Dynamo", "Major Liberty", "Tempest Hammer", "Emerald Goliath", "Shadow Recluse", "Apex Fletcher",
      "Arachnid Kid", "Onyx Jaguar", "Doctor Arcane", "Crimson Chaos", "Synth Android", "Sky Raptor",
      "Cyber Soldier", "Star Corsair", "Timber Giant", "Bandit Raccoon", "Lord Oblivion", "Trickster Horn",
      "Chrome Overlord", "Master Polarity", "Adamant Claw", "Crimson Merc", "Daywalker Fang", "Comet Surfer"
    ]
  },
  {
    id: "critters", name: "Elemental Critters", desc: "Evolution Monsters & Mythic Beasts",
    free: false, price: 2500, perkName: "Evolution Surge",
    perkDesc: "Eliminates 2 innocent suspects + adds +6s in Blitz mode",
    palette: [0x2e054e, 0x7e22ce, 0xf472b6],
    names: [
      "Volt-Squeak", "Blaze-Wyrm", "Hydro-Tortoise", "Sprout-Toad", "Phantom-Grin", "Aether-Mew",
      "Slumber-Bear", "Lullaby-Puff", "Prism-Fox", "Tidal-Serpent", "Gale-Dragon", "Aura-Jackal",
      "Coin-Tabby", "Mystic-Duck", "Titan-Brawler", "Sage-Spoon", "Glacier-Shell", "Morph-Slime",
      "Solar-Hound", "Mantis-Blade", "Granite-Serpent", "Spark-Pip", "Nova-Sprite", "Silver-Phoenix"
    ]
  },
  {
    id: "relic", name: "Realm of the Ancients", desc: "Elves, Dwarves & Shadow Kings",
    free: false, price: 3000, perkName: "Elven Sight",
    perkDesc: "Reveals 1 true trait of your opponent's secret operative",
    palette: [0x0f391e, 0x166534, 0xfde047],
    names: [
      "Perrin Ringbearer", "Bram Skillet", "Aldric Greybeard", "Garrick Ranger", "Sylvan Archer", "Torin Battleaxe",
      "Valen Shieldhorn", "Slink Wretch", "Malcor Whitebeard", "Dread Eye", "Wraith Sovereign", "Lord Starleaf",
      "Lady Mirror", "Freya Shieldmaiden", "Caelen Captain", "Toby Shire", "Milo Underhill", "Bramble Burglar",
      "Oaken Ent", "Krag Uruk", "King Goldmane", "Lyra Evenstar", "Cinder Dragon", "Inferno Balrog"
    ]
  },
  {
    id: "brawlers", name: "Apex Martial Artists", desc: "Super Aura Tournament Fighters",
    free: false, price: 3500, perkName: "Overdrive Jammer",
    perkDesc: "Skips your opponent's next turn completely",
    palette: [0x361005, 0xc2410c, 0xfde047],
    names: [
      "Kairo Sunstrike", "Prince Vexor", "Sora Scholar", "Kenshin Namek", "Vance Futureblade", "Monk Six-Dot",
      "Emperor Frost", "Bio-Beetle", "Nebula Djinn", "Titan Berserker", "Capsule Heiress", "Master Shell-Beard",
      "Cyborg Eighteen", "Cyborg Ranger", "Wolf-Fang Scar", "Master Tri-Eye", "Deity Sphinx", "Attendant Halo",
      "Rebel Bandana", "Koda Striker", "Brute Bald", "Captain Pose", "Chrome Conqueror", "Eternal Shen-Dragon"
    ]
  }
];

// Detects exact 3D species anatomy from character name so Spiked Tortoise is ALWAYS a 3D spiked tortoise!
window.detectSpeciesArchetype = function(packId, name, isNonHuman) {
  const n = name.toLowerCase();
  if (n.includes("tortoise") || n.includes("terrapin") || n.includes("snapper") || n.includes("shell") || n.includes("katana") && packId === "turtles" || n.includes("sai") && packId === "turtles" || n.includes("nunchuck") && packId === "turtles" || n.includes("bo-staff") && packId === "turtles") {
    return "tortoise";
  }
  if (n.includes("whiskers") || n.includes("rat") || n.includes("squeak") || n.includes("pip")) return "rat_sensei";
  if (n.includes("boar") || n.includes("tusker") || n.includes("uruk") || n.includes("brute")) return "boar";
  if (n.includes("gator") || n.includes("gecko") || n.includes("lizard") || n.includes("wyrm") || n.includes("dragon") || n.includes("serpent") || n.includes("wyvern") || n.includes("rex") || n.includes("toad") || n.includes("kraken")) return "reptile";
  if (n.includes("hare") || n.includes("rabbit") || n.includes("mew") || n.includes("fox") || n.includes("jackal") || n.includes("tabby")) return "hare_fox";
  if (n.includes("lupin") || n.includes("hound") || n.includes("howl") || n.includes("ursa") || n.includes("bear") || n.includes("jaguar") || n.includes("raccoon") || n.includes("tiger") || n.includes("lynx")) return "lupin_beast";
  if (n.includes("rover") || n.includes("unit") || n.includes("mech") || n.includes("automaton") || n.includes("android") || n.includes("gearheart") || n.includes("chrome") || n.includes("dynamo")) return "mech_droid";
  if (isNonHuman) return "alien_mutant";
  return "human";
};

window.buildBijectiveFactionRoster = function(fac) {
  const usedMasks = new Set();
  const keys = window.TRAIT_SCHEMA.map(t => t.key);

  return fac.names.map((name, idx) => {
    const nl = name.toLowerCase();
    const wType = (idx * 5 + 1) % 4;
    const hType = (idx * 7 + 2) % 3;
    let t = {
      has_blade:   wType === 0 || wType === 3,
      has_ranged:  wType === 1,
      has_blunt:   wType === 2,
      has_helmet:  hType === 0,
      has_hood:    hType === 1,
      has_eyewear: ((idx * 3 + 1) % 5 === 0) || ((idx + 2) % 4 === 0),
      has_beard:   ((idx * 7 + 3) % 5 === 0),
      has_armor:   ((idx * 3 + 2) % 2 === 0),
      is_nonhuman: ((idx * 5 + 1) % 3 === 0),
      has_aura:    ((idx * 11 + 1) % 3 === 0)
    };

    const isFem = ["princess", "vesper", "kira", "astra", "empress", "paige", "lotus", "canary", "clara", "morgana", "astrid", "minerva", "genevieve", "queen", "calypso", "sirena", "maria", "recluse", "lady", "freya", "lyra", "heiress", "eighteen", "rose", "vixen"].some(w => nl.includes(w));
    if (isFem) t.has_beard = false;

    if (["whiskers", "greybeard", "whitebeard", "redbeard", "shell-beard", "aldous", "moss", "qorin", "barnacle", "boar", "tusker"].some(w => nl.includes(w))) {
      t.has_beard = true;
    }

    // Force all mutant/beast/tortoise/mech names to be 100% Non-Human
    if (["whiskers", "boar", "gator", "gecko", "tortoise", "terrapin", "snapper", "hare", "lupin", "ursa", "ent", "dragon", "wyrm", "rover", "unit", "mech", "automaton", "coral", "horn", "kraken", "goliath", "android", "raccoon", "beetle", "djinn", "sphinx", "balrog", "uruk", "katana", "sai", "nunchuck", "bo-staff"].some(w => nl.includes(w))) {
      if (!(nl.includes("katana") || nl.includes("sai") || nl.includes("nunchuck") || nl.includes("bo-staff")) || fac.id === "turtles") {
        t.is_nonhuman = true;
      }
    }
    if (isFem && !["eighteen", "vixen"].some(w => nl.includes(w))) {
      t.is_nonhuman = false;
    }

    // Explicit Spiked Tortoise & Turtle Shell Armor guarantees
    if (nl.includes("tortoise") || nl.includes("terrapin") || nl.includes("snapper") || nl.includes("shell")) {
      t.is_nonhuman = true;
      t.has_armor = true; // 3D Spiked Carapace Shell!
    }
    if (nl === "spiked tortoise") {
      t.is_nonhuman = true;
      t.has_armor = true;
      t.has_blunt = true;
      t.has_blade = false;
      t.has_ranged = false;
      t.has_beard = true;
      t.has_helmet = false;
      t.has_hood = false;
      t.has_eyewear = false;
      t.has_aura = false;
    }

    if (["katana", "blade", "sword", "cutlass", "saber", "talon", "claw", "sai", "obsidian"].some(w => nl.includes(w))) {
      t.has_blade = true; t.has_ranged = false; t.has_blunt = false;
    }
    if (["staff", "hammer", "nunchuck", "puck", "shield", "skillet", "cane", "battleaxe"].some(w => nl.includes(w))) {
      t.has_blunt = true; t.has_blade = false; t.has_ranged = false;
    }
    if (["archer", "fletcher", "wand", "dash", "tracker", "powder"].some(w => nl.includes(w))) {
      t.has_ranged = true; t.has_blade = false; t.has_blunt = false;
    }
    if (fac.id === "critters") t.is_nonhuman = true;

    const toMask = (obj) => keys.reduce((acc, k, i) => acc | (obj[k] ? (1 << i) : 0), 0);
    let mask = toMask(t);
    let probe = 0;
    while (usedMasks.has(mask) && probe < 10) {
      const tk = keys[(idx + probe) % keys.length];
      if (tk !== "is_nonhuman" && tk !== "has_beard" && nl !== "spiked tortoise") {
        t[tk] = !t[tk];
      } else {
        t.has_aura = !t.has_aura;
      }
      mask = toMask(t);
      probe++;
    }
    usedMasks.add(mask);

    const archetype = window.detectSpeciesArchetype(fac.id, name, t.is_nonhuman);
    return {
      id: idx,
      name,
      isFemale: isFem,
      archetype,
      traits: t
    };
  });
};
"""

# ==============================================================================
# 4. JS/AUDIO.JS (MULTI-TRACK SYNTH SOUNDTRACK + BELOVED CARD FLIP SNAP)
# ==============================================================================
FILES["js/audio.js"] = """
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
"""

# ==============================================================================
# 5. JS/RENDERER3D.JS (THREE.JS WEBGL 3D COLLECTIBLE FIGURINE & TURNTABLE ENGINE)
# ==============================================================================
FILES["js/renderer3d.js"] = """
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
"""

# ==============================================================================
# 6. JS/GAME.JS (CORE ENGINE, 5 MODES, P2P DUELS, SEASON PASS, ACCESSIBILITY)
# ==============================================================================
FILES["js/game.js"] = """
// 60fps Background Particle & Confetti Engine
const fxCanvas = document.getElementById("fxCanvas");
const fxCtx = fxCanvas.getContext("2d");
let particles = [];
let motes = [];
let reducedMotion = false;

function resizeFx() {
  fxCanvas.width = window.innerWidth;
  fxCanvas.height = window.innerHeight;
}
window.addEventListener("resize", resizeFx);
resizeFx();

for (let i = 0; i < 20; i++) {
  motes.push({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    r: 1 + Math.random() * 1.6,
    vy: -0.15 - Math.random() * 0.25,
    vx: (Math.random() - 0.5) * 0.2,
    a: 0.1 + Math.random() * 0.25
  });
}

function spawnBurst(x, y, color = "#38bdf8", count = 18) {
  if (reducedMotion) return;
  for (let i = 0; i < count; i++) {
    const ang = Math.random() * Math.PI * 2;
    const spd = 1.5 + Math.random() * 4.5;
    particles.push({
      x, y,
      vx: Math.cos(ang) * spd,
      vy: Math.sin(ang) * spd - 1.1,
      r: 2 + Math.random() * 3,
      color,
      life: 1
    });
  }
}

function tickFx() {
  fxCtx.clearRect(0, 0, fxCanvas.width, fxCanvas.height);
  if (!reducedMotion) {
    motes.forEach(m => {
      m.x += m.vx; m.y += m.vy;
      if (m.y < 0) m.y = fxCanvas.height;
      if (m.x < 0) m.x = fxCanvas.width;
      if (m.x > fxCanvas.width) m.x = 0;
      fxCtx.fillStyle = `rgba(56, 189, 248, ${m.a})`;
      fxCtx.beginPath(); fxCtx.arc(m.x, m.y, m.r, 0, Math.PI * 2); fxCtx.fill();
    });
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx; p.y += p.vy; p.vy += 0.12; p.life -= 0.028;
      if (p.life <= 0) { particles.splice(i, 1); continue; }
      fxCtx.globalAlpha = p.life;
      fxCtx.fillStyle = p.color;
      fxCtx.beginPath(); fxCtx.arc(p.x, p.y, p.r, 0, Math.PI * 2); fxCtx.fill();
      fxCtx.globalAlpha = 1;
    }
  }
  requestAnimationFrame(tickFx);
}
requestAnimationFrame(tickFx);

// Persistent Player State
let state = {
  username: localStorage.getItem("tt_3d_user") || localStorage.getItem("tt_v4_user") || "",
  coins: parseInt(localStorage.getItem("tt_3d_coins") || "120", 10),
  mmr: parseInt(localStorage.getItem("tt_3d_mmr") || "1000", 10),
  wins: parseInt(localStorage.getItem("tt_3d_wins") || "0", 10),
  streak: parseInt(localStorage.getItem("tt_3d_streak") || "0", 10),
  xp: parseInt(localStorage.getItem("tt_3d_xp") || "20", 10),
  tier: parseInt(localStorage.getItem("tt_3d_tier") || "1", 10),
  vip: localStorage.getItem("tt_3d_vip") === "true",
  ownedFactions: JSON.parse(localStorage.getItem("tt_3d_factions") || '["galactic","turtles","rangers","sorcery"]'),
  foilFactions: JSON.parse(localStorage.getItem("tt_3d_foils") || '[]'),
  friends: JSON.parse(localStorage.getItem("tt_3d_friends") || '["ViperZero","AstraKnight","PixelSleuth"]'),
  chips: JSON.parse(localStorage.getItem("tt_3d_chips") || '{"radar":2,"snipe":1,"jam":1}'),
  missions: JSON.parse(localStorage.getItem("tt_3d_missions") || '{"m1":false,"m2":false,"m3":false}'),
  theme: localStorage.getItem("tt_3d_theme") || "slate",
  autoFlip: localStorage.getItem("tt_3d_autoflip") !== "false",
  highContrast: localStorage.getItem("tt_3d_hc") === "true"
};

let FACTIONS = [];
let activeFaction = null;

function saveState() {
  localStorage.setItem("tt_3d_user", state.username);
  localStorage.setItem("tt_3d_coins", String(state.coins));
  localStorage.setItem("tt_3d_mmr", String(state.mmr));
  localStorage.setItem("tt_3d_wins", String(state.wins));
  localStorage.setItem("tt_3d_streak", String(state.streak));
  localStorage.setItem("tt_3d_xp", String(state.xp));
  localStorage.setItem("tt_3d_tier", String(state.tier));
  localStorage.setItem("tt_3d_vip", String(state.vip));
  localStorage.setItem("tt_3d_factions", JSON.stringify(state.ownedFactions));
  localStorage.setItem("tt_3d_foils", JSON.stringify(state.foilFactions));
  localStorage.setItem("tt_3d_friends", JSON.stringify(state.friends));
  localStorage.setItem("tt_3d_chips", JSON.stringify(state.chips));
  localStorage.setItem("tt_3d_missions", JSON.stringify(state.missions));
  localStorage.setItem("tt_3d_theme", state.theme);
  localStorage.setItem("tt_3d_autoflip", String(state.autoFlip));
  localStorage.setItem("tt_3d_hc", String(state.highContrast));
  renderLobbyUI();
}

function switchTab(tab) {
  StudioAudio.sfxTap();
  StudioAudio.setArenaIntensity(false);
  Renderer3D.stopInteractiveTurntable();
  document.getElementById("arenaView").classList.remove("active");
  document.getElementById("lobbyHeader").style.display = "flex";
  document.getElementById("bottomNav").style.display = "flex";
  document.querySelectorAll(".tab-view").forEach(el => el.classList.remove("active"));
  document.getElementById(`tab-${tab}`).classList.add("active");
  document.querySelectorAll(".nav-tab").forEach(b => b.classList.toggle("active", b.dataset.tab === tab));
  renderLobbyUI();
}

function renderLobbyUI() {
  if (!activeFaction) activeFaction = FACTIONS[0];
  const u = state.username || "Agent";
  document.getElementById("uiUsername").textContent = u;
  document.getElementById("uiAvatar").textContent = u.charAt(0).toUpperCase();
  document.getElementById("uiPassBadge").textContent = state.vip
    ? `VIP Commander • Tier ${state.tier} • ${state.wins} Wins`
    : `Season Tier ${state.tier} • ${state.wins} Wins`;
  document.getElementById("uiMmr").textContent = state.mmr;
  document.getElementById("uiCoins").textContent = state.coins;
  document.getElementById("uiMyFriendId").textContent = u;
  document.getElementById("uiActiveFaction").textContent = activeFaction.name;
  document.getElementById("uiActiveSkill").textContent = activeFaction.perkName;
  document.getElementById("uiStreakPill").textContent = `Streak: ${state.streak}`;

  document.getElementById("uiSeasonTier").textContent = state.tier;
  document.getElementById("uiSeasonXp").textContent = `${state.xp} / 100 XP`;
  document.getElementById("uiSeasonBar").style.width = `${Math.min(100, state.xp)}%`;

  document.getElementById("cntRadar").textContent = state.chips.radar;
  document.getElementById("cntSnipe").textContent = state.chips.snipe;
  document.getElementById("cntJam").textContent = state.chips.jam;

  const isFoil = state.foilFactions.includes(activeFaction.id);
  const foilBtn = document.getElementById("foilBtn");
  foilBtn.textContent = isFoil ? "Gold Foil Active" : "Foil Upgrade (500 Coins)";
  foilBtn.disabled = isFoil;

  // Daily Missions
  const mDefs = [
    { id: "m1", title: "Win 1 Match in Any Mode", reward: 25 },
    { id: "m2", title: "Activate Faction Skill or Chip", reward: 20 },
    { id: "m3", title: "Reach a 2-Win Streak", reward: 35 }
  ];
  document.getElementById("dailyMissionsGrid").innerHTML = mDefs.map(d => {
    const done = !!state.missions[d.id];
    return `
      <div class="mission-box ${done ? 'done' : ''}">
        <span>${d.title}</span>
        <strong style="color:${done ? 'var(--emerald-hi)' : 'var(--gold-hi)'};">${done ? 'CLAIMED' : `+${d.reward} Coins`}</strong>
      </div>
    `;
  }).join("");

  // Render All 9 Factions with 3D WebGL Preview Thumbnails
  const fGrid = document.getElementById("factionGrid");
  fGrid.innerHTML = FACTIONS.map(fac => {
    const owned = fac.free || state.vip || state.ownedFactions.includes(fac.id);
    const thumbUrl = Renderer3D.renderCardPortrait(fac, fac.characters[0]);
    return `
      <div class="faction-card ${activeFaction.id === fac.id ? 'selected' : ''}" onclick="selectFaction('${fac.id}')">
        <img src="${thumbUrl}" alt="${fac.name}" />
        <div style="flex:1; min-width:0;">
          <div style="font-size:0.6rem; font-weight:800; color:${owned ? 'var(--emerald-hi)' : 'var(--gold-hi)'};">${owned ? 'UNLOCKED' : `LOCKED • ${fac.price} COINS`}</div>
          <h3 style="font-size:0.9rem;">${fac.name}</h3>
          <p style="font-size:0.68rem; color:var(--muted); margin:2px 0 4px;">${fac.desc}</p>
          <div style="font-size:0.65rem; color:var(--primary-hi); font-weight:700;">Skill: ${fac.perkName}</div>
        </div>
      </div>
    `;
  }).join("");

  // Shop Faction List
  document.getElementById("shopFactionList").innerHTML = FACTIONS.filter(f => !f.free).map(fac => {
    const owned = state.vip || state.ownedFactions.includes(fac.id);
    return `
      <div class="row-item">
        <div>
          <strong>${fac.name}</strong>
          <div style="font-size:0.7rem; color:var(--muted);">${fac.perkName}: ${fac.perkDesc}</div>
        </div>
        ${owned ? `<strong style="color:var(--emerald-hi);">OWNED</strong>` : `<button class="btn btn-gold" style="padding:7px 12px; font-size:0.75rem;" onclick="unlockFactionCoins('${fac.id}', ${fac.price})">${fac.price} Coins</button>`}
      </div>
    `;
  }).join("");

  // Leaderboard
  const rivals = [
    { name: "GrandmasterKael", mmr: 1840, vip: true },
    { name: "AstraKnight", mmr: 1620, vip: true },
    { name: "ViperZero", mmr: 1490, vip: false },
    { name: "CyberRonin_AZ", mmr: 1385, vip: true },
    { name: "PixelSleuth", mmr: 1290, vip: false },
    { name: "NovaHunter99", mmr: 1210, vip: false },
    { name: "TacticalFox", mmr: 1140, vip: false },
    { name: "ShadowVesper", mmr: 1080, vip: false },
    { name: "BlitzMonarch", mmr: 1020, vip: false },
    { name: u, mmr: state.mmr, vip: state.vip, me: true }
  ].sort((a, b) => b.mmr - a.mmr);

  const myPos = rivals.findIndex(r => r.me);
  document.getElementById("uiMyRankPos").textContent = `#${myPos + 1}`;
  document.getElementById("ranksListBox").innerHTML = rivals.map((r, i) => `
    <div class="row-item" style="${r.me ? 'border-color:var(--primary-hi); background:rgba(14,165,233,0.15);' : ''}">
      <span><strong>#${i + 1} ${r.name}</strong> ${r.vip ? '<span style="color:var(--gold-hi); font-size:0.68rem;">[VIP]</span>' : ''}</span>
      <strong style="color:var(--primary-hi);">${r.mmr} MMR</strong>
    </div>
  `).join("");

  // Friends
  document.getElementById("friendsListBox").innerHTML = state.friends.map(f => `
    <div class="row-item">
      <div>
        <strong>${f}</strong>
        <div style="font-size:0.68rem; color:var(--emerald-hi);">Direct P2P Challenge Ready</div>
      </div>
      <button class="btn btn-emerald" style="padding:7px 12px; font-size:0.74rem;" onclick="challengeFriendByUsername('${f}')">Challenge</button>
    </div>
  `).join("");
}

function selectFaction(id) {
  StudioAudio.sfxTap();
  const fac = FACTIONS.find(f => f.id === id);
  if (!fac) return;
  const owned = fac.free || state.vip || state.ownedFactions.includes(fac.id);
  if (!owned) { switchTab("shop"); return; }
  activeFaction = fac;
  renderLobbyUI();
}

function upgradeCurrentFactionFoil() {
  StudioAudio.sfxTap();
  if (state.coins < 500) { showToast("NEED 500 COINS", "Win matches or visit the Shop!"); return; }
  state.coins -= 500;
  if (!state.foilFactions.includes(activeFaction.id)) state.foilFactions.push(activeFaction.id);
  StudioAudio.sfxWin();
  saveState();
  showToast("GOLD FOIL UNLOCKED!", `${activeFaction.name} cards now feature Gold Foil borders!`);
}

function buyIntelChip(type, cost) {
  StudioAudio.sfxTap();
  if (state.coins < cost) { showToast("NEED MORE COINS", "Win matches or get a Treasury Coin Bundle!"); return; }
  state.coins -= cost;
  state.chips[type] = (state.chips[type] || 0) + 1;
  StudioAudio.sfxYes();
  saveState();
  showToast("INTEL CHIP EQUIPPED", "Ready for deployment in your next match!");
}

function unlockFactionCoins(id, price) {
  StudioAudio.sfxTap();
  if (state.coins < price) { showToast("INSUFFICIENT COINS", `Need ${price} Coins to unlock this faction!`); return; }
  state.coins -= price;
  state.ownedFactions.push(id);
  activeFaction = FACTIONS.find(f => f.id === id);
  StudioAudio.sfxWin();
  saveState();
  showToast("FACTION UNLOCKED!", `${activeFaction.name} is now permanently unlocked!`);
}

async function buyRealSku(sku) {
  StudioAudio.sfxTap();
  if ("getDigitalGoodsService" in window) {
    try {
      const service = await window.getDigitalGoodsService("https://play.google.com/billing");
      if (service) {
        const prices = { vip_all_access: "4.99", coins_1500: "0.99", coins_5000: "2.99" };
        const req = new PaymentRequest([{ supportedMethods: "https://play.google.com/billing", data: { sku } }], {
          total: { label: sku, amount: { currency: "USD", value: prices[sku] || "4.99" } }
        });
        const resp = await req.show();
        await resp.complete("success");
        applySkuReward(sku);
        return;
      }
    } catch (e) { return; }
  }
  window.location.href = "https://ko-fi.com/";
}

function applySkuReward(sku) {
  if (sku === "vip_all_access") {
    state.vip = true;
    state.coins += 2500;
    state.chips.radar += 4; state.chips.snipe += 3; state.chips.jam += 3;
    FACTIONS.forEach(f => { if (!state.ownedFactions.includes(f.id)) state.ownedFactions.push(f.id); });
  } else if (sku === "coins_1500") state.coins += 1500;
  else if (sku === "coins_5000") state.coins += 5000;
  StudioAudio.sfxWin();
  saveState();
  spawnBurst(window.innerWidth / 2, window.innerHeight / 2, "#fde047", 40);
}

// =========================================================================
// PEERJS DIRECT USERNAME MULTIPLAYER
// =========================================================================
let peer = null;
let activeConn = null;
let pendingConn = null;
let isLiveP2P = false;
let isHostPlayer = true;

function initPeerNetwork() {
  if (!state.username) return;
  if (peer) peer.destroy();
  peer = new Peer(`tt-agent-${state.username.toLowerCase()}`);
  peer.on("connection", (incoming) => {
    pendingConn = incoming;
    incoming.on("data", (msg) => {
      if (msg.type === "CHALLENGE_INVITE") {
        StudioAudio.sfxYes();
        document.getElementById("challengerNameDisplay").textContent = `${msg.fromUser} (${msg.factionName})`;
        document.getElementById("challengeBanner").classList.add("show");
      }
    });
  });
}

function challengeFriendByUsername(friendName) {
  StudioAudio.sfxTap();
  if (!peer) initPeerNetwork();
  showToast("CALLING AGENT...", `Sending live duel invite to ${friendName}...`);
  const outConn = peer.connect(`tt-agent-${friendName.toLowerCase()}`);
  outConn.on("open", () => {
    outConn.send({
      type: "CHALLENGE_INVITE",
      fromUser: state.username,
      factionId: activeFaction.id,
      factionName: activeFaction.name
    });
  });
  outConn.on("data", (msg) => {
    if (msg.type === "CHALLENGE_ACCEPTED") {
      activeConn = outConn;
      bindLiveDuel(true, friendName);
    }
  });
}

function acceptIncomingChallenge() {
  StudioAudio.sfxYes();
  document.getElementById("challengeBanner").classList.remove("show");
  if (!pendingConn) return;
  activeConn = pendingConn;
  activeConn.send({ type: "CHALLENGE_ACCEPTED", fromUser: state.username });
  bindLiveDuel(false, "Friend");
}

function dismissChallenge() {
  StudioAudio.sfxTap();
  document.getElementById("challengeBanner").classList.remove("show");
  if (pendingConn) pendingConn.close();
  pendingConn = null;
}

function bindLiveDuel(asHost, rivalHandle) {
  isLiveP2P = true;
  isHostPlayer = asHost;
  startMatch("duel", rivalHandle, true);

  activeConn.on("data", (data) => {
    if (data.type === "ASK_TRAIT") {
      const myChar = cards[mySecretIdx];
      const has = !!myChar.traits[data.traitKey];
      activeConn.send({ type: "ANS_TRAIT", traitKey: data.traitKey, matches: has });
      isMyTurn = true;
      updateArenaUI();
    } else if (data.type === "ANS_TRAIT") {
      processTraitClue(data.traitKey, data.matches);
    } else if (data.type === "TAKEDOWN_GUESS") {
      const win = data.guessIdx === mySecretIdx;
      activeConn.send({ type: "TAKEDOWN_RESULT", win, secretIdx: mySecretIdx, guessIdx: data.guessIdx });
      if (win) finishRound(false, cards[mySecretIdx]);
      else {
        isMyTurn = true;
        updateArenaUI();
        showToast("RIVAL MISSED!", `${rivalName} guessed wrong! Your turn!`);
      }
    } else if (data.type === "TAKEDOWN_RESULT") {
      if (data.win) finishRound(true, cards[data.secretIdx]);
      else {
        cards[data.guessIdx].eliminated = true;
        renderBoard24();
        showToast("WRONG SUSPECT!", "Suspect eliminated. Rival's turn!");
      }
    }
  });
}

// =========================================================================
// CORE GAMEPLAY LOOP (3D PORTRAITS, 5 MODES, SMART DEDUCTION AI)
// =========================================================================
let matchMode = "quick";
let cards = [];
let mySecretIdx = 0;
let aiSecretIdx = 0;
let aiSuspects = [];
let aiAsked = [];
let myAsked = [];
let isMyTurn = true;
let isTakedown = false;
let awaitingManual = false;
let radarActive = false;
let jamNext = false;
let factionSkillUsed = false;
let inspectedIdx = 0;
let blitzTimer = null;
let blitzSec = 60;
let rivalName = "AstraKnight";
let seriesRound = 1;
let mySeriesScore = 0;
let oppSeriesScore = 0;

function startMatch(mode, customRival, keepP2P = false) {
  if (!keepP2P) isLiveP2P = false;
  if (mode === "wager") {
    if (state.coins < 50) { switchTab("shop"); showToast("NEED 50 COINS", "High-Roller Arena requires a 50 Coin entry!"); return; }
    state.coins -= 50;
    saveState();
  }
  StudioAudio.sfxYes();
  StudioAudio.setArenaIntensity(true);
  matchMode = mode;
  rivalName = customRival || ["GrandmasterKael", "AstraKnight", "ViperZero", "CyberRonin_AZ", "PixelSleuth"][Math.floor(Math.random() * 5)];
  seriesRound = 1;
  mySeriesScore = 0;
  oppSeriesScore = 0;
  beginRound();
}

function beginRound() {
  clearInterval(blitzTimer);
  cards = activeFaction.characters.map(c => ({
    ...c,
    eliminated: false,
    imgUrl: Renderer3D.renderCardPortrait(activeFaction, c)
  }));

  mySecretIdx = Math.floor(Math.random() * 24);
  aiSecretIdx = Math.floor(Math.random() * 24);
  aiSuspects = cards.map(c => c.id);
  aiAsked = [];
  myAsked = [];
  isMyTurn = isLiveP2P ? isHostPlayer : true;
  isTakedown = false;
  awaitingManual = false;
  radarActive = false;
  jamNext = false;
  factionSkillUsed = false;

  document.getElementById("lobbyHeader").style.display = "none";
  document.getElementById("bottomNav").style.display = "none";
  document.querySelectorAll(".tab-view").forEach(el => el.classList.remove("active"));
  document.getElementById("arenaView").classList.add("active");

  document.getElementById("hudSkillName").textContent = activeFaction.perkName.split(" ")[0];
  document.getElementById("btnFactionSkill").disabled = false;

  if (matchMode === "blitz") {
    blitzSec = 60;
    blitzTimer = setInterval(() => {
      blitzSec--;
      updateArenaUI();
      if (blitzSec <= 0) { clearInterval(blitzTimer); finishRound(false, cards[aiSecretIdx]); }
    }, 1000);
  }

  renderBoard24();
  updateArenaUI();
  openDossier(mySecretIdx, true);
}

function renderBoard24() {
  const grid = document.getElementById("boardGrid24");
  const isFoil = state.foilFactions.includes(activeFaction.id);
  grid.innerHTML = cards.map((c, idx) => {
    const pips = window.TRAIT_SCHEMA.filter(t => c.traits[t.key]).slice(0, 6).map(t => `<span class="trait-pip" style="background:${t.color};" title="${t.label}"></span>`).join("");
    return `
      <div class="card-cell" onclick="onCardTap(${idx}, event)">
        <div class="game-card ${c.eliminated ? 'eliminated' : ''} ${isTakedown && !c.eliminated ? 'target-glow' : ''} ${isFoil ? 'foil-upgraded' : ''}" id="gCard_${idx}">
          <div class="card-face-front">
            <div class="card-portrait-wrap">
              <div class="inspect-corner" onclick="event.stopPropagation(); openDossier(${idx}, false)" title="Inspect 3D Figurine & Dossier">
                <svg class="ico" style="width:12px;height:12px;" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2.5" fill="none"/><line x1="21" y1="21" x2="16.65" y2="16.65" stroke="currentColor" stroke-width="2.5"/></svg>
              </div>
              <img src="${c.imgUrl}" alt="${c.name}" />
              <div class="trait-pip-row">${pips}</div>
            </div>
            <div class="card-title-plate">${c.name}</div>
          </div>
          <div class="card-face-back">
            <svg class="ico" viewBox="0 0 24 24"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            <span>OUT</span>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function updateArenaUI() {
  const myC = cards[mySecretIdx];
  document.getElementById("arenaSecretImg").src = myC.imgUrl;
  document.getElementById("arenaSecretName").textContent = myC.name;
  document.getElementById("arenaRivalName").textContent = rivalName;
  document.getElementById("arenaRivalLeft").textContent = `${aiSuspects.length} Left`;

  const myLeft = cards.filter(c => !c.eliminated).length;
  if (matchMode === "blitz") {
    document.getElementById("arenaModeTitle").textContent = `${blitzSec}s BLITZ`;
    document.getElementById("arenaSubCounter").textContent = `YOU ${myLeft} • RIVAL ${aiSuspects.length}`;
  } else if (matchMode === "ranked") {
    document.getElementById("arenaModeTitle").textContent = `ROUND ${seriesRound} (BO3)`;
    document.getElementById("arenaSubCounter").textContent = `SERIES ${mySeriesScore} - ${oppSeriesScore}`;
  } else if (matchMode === "wager") {
    document.getElementById("arenaModeTitle").textContent = "100 COINS POT";
    document.getElementById("arenaSubCounter").textContent = `YOU ${myLeft} • RIVAL ${aiSuspects.length}`;
  } else {
    document.getElementById("arenaModeTitle").textContent = matchMode.toUpperCase();
    document.getElementById("arenaSubCounter").textContent = `YOU ${myLeft} • RIVAL ${aiSuspects.length}`;
  }

  document.getElementById("hudRadarCnt").textContent = state.chips.radar;
  document.getElementById("hudSnipeCnt").textContent = state.chips.snipe;
  document.getElementById("hudJamCnt").textContent = state.chips.jam;

  document.getElementById("btnAskTrait").style.display = awaitingManual ? "none" : "inline-flex";
  document.getElementById("btnDoneManual").style.display = awaitingManual ? "inline-flex" : "none";
  document.getElementById("btnAskTrait").disabled = !isMyTurn;
  document.getElementById("btnTakedown").textContent = isTakedown ? "Cancel" : "Takedown";
}

function useFactionAbility() {
  if (factionSkillUsed || !isMyTurn) return;
  factionSkillUsed = true;
  document.getElementById("btnFactionSkill").disabled = true;
  StudioAudio.sfxYes();

  if (!state.missions.m2) { state.missions.m2 = true; state.coins += 20; saveState(); }

  const fId = activeFaction.id;
  if (fId === "galactic" || fId === "defenders") {
    radarActive = true;
    if (fId === "defenders") { state.coins += 15; saveState(); }
    openQuestionModal();
  } else if (fId === "turtles" || fId === "pirates" || fId === "critters") {
    const cnt = fId === "pirates" ? 3 : 2;
    if (fId === "critters" && matchMode === "blitz") blitzSec += 6;
    const innocents = cards.filter(c => !c.eliminated && c.id !== aiSecretIdx).slice(0, cnt);
    innocents.forEach((c, i) => {
      setTimeout(() => { c.eliminated = true; StudioAudio.sfxCardSnap(i); renderBoard24(); updateArenaUI(); }, i * 130);
    });
    showToast(activeFaction.perkName.toUpperCase(), `Eliminated ${cnt} innocent suspects automatically!`);
  } else if (fId === "rangers" || fId === "brawlers") {
    jamNext = true;
    showToast(activeFaction.perkName.toUpperCase(), "Opponent's next turn is jammed!");
  } else if (fId === "sorcery" || fId === "relic") {
    const target = cards[aiSecretIdx];
    const trueTrait = window.TRAIT_SCHEMA.find(t => target.traits[t.key] && !myAsked.includes(t.key)) || window.TRAIT_SCHEMA[0];
    showToast("SCRYING VISION", `Rival's secret operative HAS: ${trueTrait.label}!`);
  }
}

function useIntelChip(type) {
  if (!isMyTurn) return;
  if ((state.chips[type] || 0) <= 0) {
    showToast("OUT OF CHIPS", "Restock Tactical Intel Chips in the Shop!");
    return;
  }
  state.chips[type]--;
  if (!state.missions.m2) { state.missions.m2 = true; state.coins += 20; }
  saveState();
  StudioAudio.sfxYes();

  if (type === "radar") {
    radarActive = true;
    openQuestionModal();
  } else if (type === "snipe") {
    const innocents = cards.filter(c => !c.eliminated && c.id !== aiSecretIdx).slice(0, 2);
    innocents.forEach((c, i) => {
      setTimeout(() => { c.eliminated = true; StudioAudio.sfxCardSnap(i); renderBoard24(); updateArenaUI(); }, i * 130);
    });
    showToast("SNIPER CHIP USED", "2 innocent suspects eliminated!");
  } else if (type === "jam") {
    jamNext = true;
    showToast("JAMMER ARMED", "Opponent's next turn is skipped!");
  }
  updateArenaUI();
}

function openQuestionModal() {
  if (!isMyTurn) return;
  StudioAudio.sfxTap();
  const active = cards.filter(c => !c.eliminated);
  const half = active.length / 2;
  let bestKey = null; let bestDiff = 99;
  window.TRAIT_SCHEMA.forEach(t => {
    const cnt = active.filter(c => c.traits[t.key]).length;
    const d = Math.abs(cnt - half);
    if (cnt > 0 && cnt < active.length && d < bestDiff) { bestDiff = d; bestKey = t.key; }
  });

  document.getElementById("questionListBox").innerHTML = window.TRAIT_SCHEMA.map(t => {
    const cnt = active.filter(c => c.traits[t.key]).length;
    const opt = radarActive && t.key === bestKey;
    const asked = myAsked.includes(t.key);
    return `
      <button class="q-btn ${opt ? 'optimal' : ''} ${asked ? 'asked' : ''}" onclick="submitTrait('${t.key}')">
        <div>
          <span><strong style="color:${t.color}; margin-right:5px;">${t.sym}</strong>Does the suspect <strong>${t.q}</strong>?</span>
          ${opt ? `<div style="font-size:0.66rem; color:var(--gold-hi);">OPTIMAL 50/50 RADAR SPLIT</div>` : ""}
        </div>
        <strong style="color:var(--primary-hi); margin-left:8px;">${cnt}/${active.length}</strong>
      </button>
    `;
  }).join("");
  openModal("questionModal");
}

function submitTrait(key) {
  closeModal("questionModal");
  radarActive = false;
  if (!myAsked.includes(key)) myAsked.push(key);

  if (isLiveP2P && activeConn && activeConn.open) {
    isMyTurn = false;
    updateArenaUI();
    activeConn.send({ type: "ASK_TRAIT", traitKey: key });
    return;
  }

  const has = !!cards[aiSecretIdx].traits[key];
  processTraitClue(key, has);
}

function processTraitClue(key, has) {
  const traitObj = window.TRAIT_SCHEMA.find(t => t.key === key);
  if (has) StudioAudio.sfxYes(); else StudioAudio.sfxNo();
  if (matchMode === "blitz" && has) blitzSec += 4;

  const manualMode = matchMode === "hardcore" || !state.autoFlip;
  if (manualMode) {
    awaitingManual = true;
    document.getElementById("arenaCoach").textContent = `CLUE: ${traitObj.label} = ${has ? 'YES' : 'NO'}! Tap cards to flip, then tap Done Flipping.`;
    showToast(has ? "YES! CONFIRMED" : "NO! RULED OUT", "Manually flip suspects down, then tap Done Flipping.");
    updateArenaUI();
    return;
  }

  const toFlip = [];
  cards.forEach((c, i) => { if (!c.eliminated && (!!c.traits[key] !== has)) toFlip.push(i); });
  showToast(has ? "YES! CONFIRMED" : "NO! RULED OUT", `Eliminating ${toFlip.length} suspects...`);

  toFlip.forEach((cIdx, step) => {
    setTimeout(() => {
      cards[cIdx].eliminated = true;
      const el = document.getElementById(`gCard_${cIdx}`);
      if (el) {
        const rect = el.getBoundingClientRect();
        spawnBurst(rect.left + rect.width / 2, rect.top + rect.height / 2, "#38bdf8", 8);
        el.classList.add("eliminated");
      }
      StudioAudio.sfxCardSnap(step);
    }, 260 + step * 54);
  });

  setTimeout(() => {
    renderBoard24();
    updateArenaUI();
    const rem = cards.filter(c => !c.eliminated);
    if (!isLiveP2P && rem.length === 1 && rem[0].id === aiSecretIdx) { finishRound(true, rem[0]); return; }
    endPlayerTurn();
  }, 380 + toFlip.length * 54);
}

function finishManualTurn() {
  StudioAudio.sfxTap();
  awaitingManual = false;
  updateArenaUI();
  endPlayerTurn();
}

function endPlayerTurn() {
  if (jamNext) {
    jamNext = false;
    isMyTurn = true;
    showToast("OPPONENT JAMMED!", "Take another turn immediately!");
    updateArenaUI();
    return;
  }
  if (!isLiveP2P) {
    isMyTurn = false;
    updateArenaUI();
    setTimeout(aiTurn, 950);
  }
}

function aiTurn() {
  if (aiSuspects.length <= 2) {
    const g = aiSuspects[0];
    if (g === mySecretIdx) { finishRound(false, cards[mySecretIdx]); return; }
    aiSuspects.shift();
    isMyTurn = true;
    updateArenaUI();
    showToast("RIVAL MISSED!", `${rivalName} accused ${cards[g].name} and missed!`);
    return;
  }

  const unasked = window.TRAIT_SCHEMA.filter(t => !aiAsked.includes(t.key));
  const poolObjs = cards.filter(c => aiSuspects.includes(c.id));
  let bestTrait = unasked[0] || window.TRAIT_SCHEMA[0];
  let bestDiff = 99;
  unasked.forEach(t => {
    const cnt = poolObjs.filter(c => c.traits[t.key]).length;
    const d = Math.abs(cnt - poolObjs.length / 2);
    if (d < bestDiff) { bestDiff = d; bestTrait = t; }
  });

  aiAsked.push(bestTrait.key);
  const myHas = !!cards[mySecretIdx].traits[bestTrait.key];
  aiSuspects = poolObjs.filter(c => (!!c.traits[bestTrait.key]) === myHas).map(c => c.id);
  StudioAudio.sfxTap();
  isMyTurn = true;
  document.getElementById("arenaCoach").textContent = `${rivalName}: "${bestTrait.label}?" (You: ${myHas ? 'YES' : 'NO'})`;
  updateArenaUI();
}

function toggleTakedown() {
  StudioAudio.sfxTap();
  isTakedown = !isTakedown;
  renderBoard24();
  updateArenaUI();
}

function onCardTap(idx, ev) {
  const c = cards[idx];
  if (isTakedown) {
    isTakedown = false;
    if (isLiveP2P && activeConn && activeConn.open) {
      isMyTurn = false;
      activeConn.send({ type: "TAKEDOWN_GUESS", guessIdx: idx });
      updateArenaUI();
      return;
    }
    if (idx === aiSecretIdx) finishRound(true, c);
    else {
      StudioAudio.sfxNo();
      c.eliminated = true;
      renderBoard24();
      showToast("WRONG SUSPECT!", "Rival takes a turn!");
      endPlayerTurn();
    }
    return;
  }
  c.eliminated = !c.eliminated;
  StudioAudio.sfxCardSnap(0);
  if (ev && ev.clientX) spawnBurst(ev.clientX, ev.clientY, "#f59e0b", 10);
  renderBoard24();
  updateArenaUI();
}

// Opens the Interactive 3D Figurine Turntable & Verified 10-Trait Dossier
function openDossier(idx, isSecret) {
  StudioAudio.sfxTap();
  inspectedIdx = idx;
  const c = cards[idx];
  document.getElementById("dossierTag").textContent = isSecret ? "YOUR SECRET OPERATIVE" : "VERIFIED SUSPECT DOSSIER";
  document.getElementById("dossierName").textContent = c.name;

  document.getElementById("dossierTraitsList").innerHTML = window.TRAIT_SCHEMA.map(t => `
    <div class="row-item" style="margin:0; padding:6px 8px; font-size:0.72rem;">
      <span><strong style="color:${t.color}; margin-right:5px;">${t.sym}</strong>${t.label}</span>
      <strong style="color:${c.traits[t.key] ? 'var(--emerald-hi)' : 'var(--muted)'};">${c.traits[t.key] ? 'YES' : 'NO'}</strong>
    </div>
  `).join("");
  document.getElementById("dossierFlipBtn").style.display = isSecret ? "none" : "inline-flex";
  openModal("dossierModal");

  Renderer3D.mountInteractiveTurntable(document.getElementById("dossier3DStage"), activeFaction, c);
}

function closeDossierModal() {
  Renderer3D.stopInteractiveTurntable();
  closeModal("dossierModal");
}

function flipInspectedCard() {
  cards[inspectedIdx].eliminated = !cards[inspectedIdx].eliminated;
  StudioAudio.sfxCardSnap(0);
  closeDossierModal();
  renderBoard24();
  updateArenaUI();
}

function finishRound(won, revealChar) {
  clearInterval(blitzTimer);
  if (won) {
    mySeriesScore++;
    state.streak++;
    StudioAudio.sfxWin();
    spawnBurst(window.innerWidth / 2, window.innerHeight / 2, "#fde047", 45);
  } else {
    oppSeriesScore++;
    state.streak = 0;
    StudioAudio.sfxNo();
  }

  const targetWins = matchMode === "ranked" ? 2 : 1;
  const seriesDone = mySeriesScore >= targetWins || oppSeriesScore >= targetWins;

  let coins = won
    ? (matchMode === "wager" ? 100 : matchMode === "hardcore" ? 45 : matchMode === "ranked" ? 40 : matchMode === "blitz" ? 35 : 25)
    : 5;

  if (won && !state.missions.m1) { state.missions.m1 = true; coins += 25; }
  if (state.streak >= 2 && !state.missions.m3) { state.missions.m3 = true; coins += 35; }
  if (state.vip && won) coins *= 2;

  const mmrDelta = won ? (seriesDone ? 28 : 14) : -12;
  state.coins += coins;
  state.mmr = Math.max(800, state.mmr + mmrDelta);
  if (won) state.wins++;
  state.xp += won ? 45 : 15;
  if (state.xp >= 100) {
    state.xp -= 100;
    state.tier = Math.min(20, state.tier + 1);
    state.coins += state.vip ? 150 : 50;
  }
  saveState();

  document.getElementById("resBadge").textContent = seriesDone ? "MATCH COMPLETE" : `ROUND ${seriesRound} COMPLETE (${mySeriesScore} - ${oppSeriesScore})`;
  document.getElementById("resTitle").textContent = won ? "TAKEDOWN CONFIRMED!" : "IDENTITY COMPROMISED";
  document.getElementById("resSub").textContent = `Secret Operative: ${revealChar.name}`;
  document.getElementById("resImg").src = revealChar.imgUrl;
  document.getElementById("resRewards").textContent = `+${coins} Coins • ${mmrDelta >= 0 ? '+' : ''}${mmrDelta} MMR • +${won ? 45 : 15} Pass XP`;
  document.getElementById("resNextBtn").textContent = seriesDone ? "Play Again" : `Start Round ${seriesRound + 1}`;
  openModal("resultModal");
}

function nextRoundOrRematch() {
  closeModal("resultModal");
  const targetWins = matchMode === "ranked" ? 2 : 1;
  if (mySeriesScore >= targetWins || oppSeriesScore >= targetWins) {
    startMatch(matchMode, rivalName, isLiveP2P);
  } else {
    seriesRound++;
    beginRound();
  }
}

function leaveArena() { clearInterval(blitzTimer); closeModal("resultModal"); switchTab("play"); }

// =========================================================================
// SETTINGS & ACCESSIBILITY CONTROLS
// =========================================================================
function updateVolumes() {
  const m = parseInt(document.getElementById("musicSlider").value, 10) / 100;
  const s = parseInt(document.getElementById("sfxSlider").value, 10) / 100;
  StudioAudio.setVolumes(m, s);
}

function saveUsername() {
  const v = document.getElementById("usernameInput").value.trim().replace(/[^a-zA-Z0-9_]/g, "");
  if (v.length < 3) return;
  state.username = v;
  saveState();
  closeModal("userModal");
  initPeerNetwork();
}

function addFriend() {
  const v = document.getElementById("friendInput").value.trim().replace(/[^a-zA-Z0-9_]/g, "");
  if (v && !state.friends.includes(v)) { state.friends.unshift(v); saveState(); }
  document.getElementById("friendInput").value = "";
}

function cycleTheme() {
  const themes = ["slate", "crimson", "emerald", "royal", "amoled"];
  state.theme = themes[(themes.indexOf(state.theme) + 1) % themes.length];
  applyVisualSettings();
  saveState();
}

function toggleFlipRule() {
  state.autoFlip = !state.autoFlip;
  document.getElementById("flipRuleBtn").textContent = state.autoFlip ? "Auto-Flip" : "Manual Flip";
  saveState();
}

function toggleHaptics() {
  const on = StudioAudio.toggleHaptics();
  document.getElementById("hapticBtn").textContent = on ? "Enabled" : "Disabled";
  StudioAudio.sfxTap();
}

function toggleHighContrast() {
  state.highContrast = !state.highContrast;
  applyVisualSettings();
  saveState();
}

function toggleReducedMotion() {
  reducedMotion = !reducedMotion;
  document.getElementById("motionBtn").textContent = reducedMotion ? "Reduced" : "Full 60fps";
  StudioAudio.sfxTap();
}

function applyVisualSettings() {
  document.body.className = "";
  if (state.theme !== "slate") document.body.classList.add(`theme-${state.theme}`);
  if (state.highContrast) document.body.classList.add("high-contrast");
  document.getElementById("themeBtn").textContent = state.theme.toUpperCase();
  document.getElementById("contrastBtn").textContent = state.highContrast ? "High Contrast" : "Standard";
}

function openModal(id) { document.getElementById(id).classList.add("open"); }
function closeModal(id) { document.getElementById(id).classList.remove("open"); }
function showToast(title, sub) {
  const b = document.getElementById("toastBanner");
  document.getElementById("toastTitle").textContent = title;
  document.getElementById("toastSub").textContent = sub;
  b.classList.add("show");
  setTimeout(() => b.classList.remove("show"), 1700);
}

window.addEventListener("DOMContentLoaded", () => {
  FACTIONS = window.RAW_FACTIONS.map(fac => ({
    ...fac,
    characters: window.buildBijectiveFactionRoster(fac)
  }));
  activeFaction = FACTIONS[0];
  applyVisualSettings();
  document.getElementById("flipRuleBtn").textContent = state.autoFlip ? "Auto-Flip" : "Manual Flip";
  renderLobbyUI();
  if (!state.username) openModal("userModal");
  else initPeerNetwork();
});
"""

# ==============================================================================
# 7. INDEX.HTML (CLEAN STUDIO SHELL LOADING THREE.JS & MODULAR ENGINE)
# ==============================================================================
FILES["index.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <meta name="theme-color" content="#04060d" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <link rel="manifest" href="manifest.json" />
  <title>TRAIT TAKEDOWN — 3D Studio Edition</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700&family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/studio.css" />
</head>
<body>

  <canvas id="fxCanvas"></canvas>

  <!-- Live Incoming Friend Challenge Notification -->
  <div class="challenge-banner" id="challengeBanner">
    <div>
      <div style="font-size:0.66rem; color:var(--gold-hi); font-weight:800; text-transform:uppercase;">Incoming Live Duel</div>
      <strong id="challengerNameDisplay">Agent</strong>
    </div>
    <div style="display:flex; gap:6px;">
      <button class="btn btn-emerald" style="padding:7px 12px; font-size:0.75rem;" onclick="acceptIncomingChallenge()">Accept</button>
      <button class="btn btn-slate" style="padding:7px 10px; font-size:0.75rem;" onclick="dismissChallenge()">Decline</button>
    </div>
  </div>

  <!-- Top Header -->
  <header class="app-header" id="lobbyHeader">
    <div class="profile-pill" onclick="openModal('userModal')">
      <div class="profile-avatar">
        <span id="uiAvatar">A</span>
        <span class="online-dot"></span>
      </div>
      <div class="profile-meta">
        <strong id="uiUsername">Agent</strong>
        <span id="uiPassBadge">Season Tier 1 • 0 Wins</span>
      </div>
    </div>
    <div class="currency-cluster">
      <div class="currency-pill mmr" onclick="switchTab('ranks')">
        <svg class="ico" viewBox="0 0 24 24"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/></svg>
        <span id="uiMmr">1000</span>
      </div>
      <div class="currency-pill gold" onclick="switchTab('shop')">
        <svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v10M9 10h6M9 14h6" stroke="#060913" stroke-width="2"/></svg>
        <span id="uiCoins">120</span>
      </div>
    </div>
  </header>

  <!-- TAB 1: COMMAND CENTER, 5 GAME MODES, SEASON PASS & 9 FACTIONS -->
  <main class="tab-view active" id="tab-play">
    <div class="glass-box" style="border-color:var(--border-hi);">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
        <div>
          <h1 style="font-size:1.55rem;">TRAIT <span style="color:var(--primary-hi);">TAKEDOWN</span></h1>
          <p style="font-size:0.76rem; color:var(--muted);">
            Active Faction: <strong style="color:#fff;" id="uiActiveFaction">Starlight Outlaws</strong> •
            Skill: <strong style="color:var(--gold-hi);" id="uiActiveSkill">Orbital Scan</strong>
          </p>
        </div>
        <div style="display:flex; gap:6px; align-items:center;">
          <span class="currency-pill gold" style="font-size:0.74rem;" id="uiStreakPill">Streak: 0</span>
          <button class="btn btn-gold" style="font-size:0.72rem; padding:7px 11px;" onclick="upgradeCurrentFactionFoil()" id="foilBtn">Foil Upgrade (500 Coins)</button>
        </div>
      </div>

      <button class="btn btn-emerald" style="width:100%; padding:14px; font-size:1.02rem;" onclick="startMatch('quick')">
        <svg class="ico-lg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        QUICK PLAY — INSTANT 3D MATCH (+25 COINS)
      </button>

      <div class="mode-grid-5">
        <div class="mode-tile" onclick="startMatch('wager')">
          <strong class="display-font" style="color:var(--gold-hi); font-size:0.82rem;">High-Roller Arena</strong>
          <p style="font-size:0.68rem; color:var(--muted); margin-top:3px;">50 Coins Entry • Winner takes 100 Coins Pot!</p>
        </div>
        <div class="mode-tile" onclick="startMatch('ranked')">
          <strong class="display-font" style="color:var(--primary-hi); font-size:0.82rem;">Ranked Series (Bo3)</strong>
          <p style="font-size:0.68rem; color:var(--muted); margin-top:3px;">Best-of-3 Championship • +35 MMR & +40 Coins</p>
        </div>
        <div class="mode-tile" onclick="startMatch('blitz')">
          <strong class="display-font" style="color:var(--crimson-hi); font-size:0.82rem;">60s Blitz Clock</strong>
          <p style="font-size:0.68rem; color:var(--muted); margin-top:3px;">60s speed clock • +4s per YES clue (+35 Coins)</p>
        </div>
        <div class="mode-tile" onclick="startMatch('hardcore')">
          <strong class="display-font" style="color:#c084fc; font-size:0.82rem;">Hardcore Tabletop</strong>
          <p style="font-size:0.68rem; color:var(--muted); margin-top:3px;">Manual card flipping • +45 Coins per win</p>
        </div>
        <div class="mode-tile" onclick="switchTab('friends')">
          <strong class="display-font" style="color:var(--emerald-hi); font-size:0.82rem;">Friend Duel (P2P)</strong>
          <p style="font-size:0.68rem; color:var(--muted); margin-top:3px;">Direct Agent Username live challenge</p>
        </div>
      </div>
    </div>

    <div class="glass-box">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <strong class="display-font" style="color:var(--gold-hi); font-size:0.85rem;">Season 1 Tactical Pass — Tier <span id="uiSeasonTier">1</span> / 20</strong>
        <span style="font-size:0.72rem; color:var(--muted);" id="uiSeasonXp">0 / 100 XP</span>
      </div>
      <div style="height:9px; background:#05070f; border-radius:99px; overflow:hidden; border:1px solid var(--border); margin-bottom:10px;">
        <div id="uiSeasonBar" style="height:100%; width:15%; background:linear-gradient(90deg, var(--primary-hi), var(--gold-hi));"></div>
      </div>
      <div class="missions-grid" id="dailyMissionsGrid"></div>
    </div>

    <div style="display:flex; justify-content:space-between; align-items:center; margin:8px 0;">
      <h2 style="font-size:1.02rem;">Select 3D Combat Faction (9 Factions • 216 Figurines)</h2>
      <span style="font-size:0.72rem; color:var(--muted);">Real-time WebGL 3D rendered</span>
    </div>
    <div class="faction-grid" id="factionGrid"></div>
  </main>

  <!-- TAB 2: FRIENDS -->
  <section class="tab-view" id="tab-friends">
    <div class="glass-box">
      <h2>Direct Agent Network (Zero Room Codes)</h2>
      <p style="font-size:0.78rem; color:var(--muted); margin:4px 0 10px;">
        Your Unique Agent Username: <strong style="color:var(--primary-hi);" id="uiMyFriendId">Agent</strong>. Share your username so friends can challenge you live with one tap.
      </p>
      <div style="display:flex; gap:8px;">
        <input type="text" id="friendInput" style="flex:1; background:#05070f; border:1.5px solid var(--border); border-radius:10px; padding:10px 12px; color:#fff; font-weight:700;" placeholder="Enter Friend's Agent Username (e.g. ViperZero)" />
        <button class="btn btn-primary" onclick="addFriend()">Add Friend</button>
      </div>
    </div>
    <div class="glass-box">
      <h3 style="margin-bottom:10px;">Your Friends List</h3>
      <div id="friendsListBox"></div>
    </div>
  </section>

  <!-- TAB 3: LEADERBOARD -->
  <section class="tab-view" id="tab-ranks">
    <div class="glass-box">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div>
          <h2>Global Championship Standings</h2>
          <p style="font-size:0.76rem; color:var(--muted);">Live MMR standings updated after every match.</p>
        </div>
        <div class="currency-pill mmr">Rank: <span id="uiMyRankPos">#10</span></div>
      </div>
      <div id="ranksListBox"></div>
    </div>
  </section>

  <!-- TAB 4: SHOP -->
  <section class="tab-view" id="tab-shop">
    <div class="glass-box" style="border-color:var(--gold); background:linear-gradient(135deg, rgba(245, 158, 11, 0.16), var(--panel));">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
        <div>
          <span style="font-size:0.65rem; font-weight:800; color:var(--gold-hi);">LIFETIME ACCOUNT & SEASON PASS UPGRADE</span>
          <h2 style="font-size:1.3rem;">Commander VIP Pass ($4.99)</h2>
          <p style="font-size:0.76rem; color:var(--muted);">Unlocks all 9 Factions (216 3D Figurines) + Permanent 2x Match Coins + 2,500 Bonus Coins + 10 Tactical Intel Chips!</p>
        </div>
        <button class="btn btn-gold" onclick="buyRealSku('vip_all_access')">1-Tap Instant Unlock ($4.99)</button>
      </div>
    </div>

    <div class="glass-box">
      <h3>Tactical Intel Chips (Repeatable Consumables)</h3>
      <p style="font-size:0.74rem; color:var(--muted); margin-bottom:10px;">Deploy single-use Intel Chips during High-Roller Wager and Ranked matches:</p>
      <div class="row-item">
        <div>
          <strong>50/50 Radar Chip (Owned: <span id="cntRadar">2</span>)</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Highlights the mathematically optimal 50/50 trait question</div>
        </div>
        <button class="btn btn-primary" style="padding:7px 12px; font-size:0.75rem;" onclick="buyIntelChip('radar', 60)">Buy (60 Coins)</button>
      </div>
      <div class="row-item">
        <div>
          <strong>Sniper Chip (Owned: <span id="cntSnipe">1</span>)</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Eliminates 2 innocent suspects without using your turn</div>
        </div>
        <button class="btn btn-primary" style="padding:7px 12px; font-size:0.75rem;" onclick="buyIntelChip('snipe', 85)">Buy (85 Coins)</button>
      </div>
      <div class="row-item">
        <div>
          <strong>Turn Jammer Chip (Owned: <span id="cntJam">1</span>)</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Skips your opponent's next turn completely</div>
        </div>
        <button class="btn btn-primary" style="padding:7px 12px; font-size:0.75rem;" onclick="buyIntelChip('jam', 100)">Buy (100 Coins)</button>
      </div>
    </div>

    <div class="glass-box">
      <h3>Treasury Coin Bundles</h3>
      <div class="row-item">
        <div><strong>1,500 Coins Cache</strong><div style="font-size:0.7rem; color:var(--muted);">Instant Faction or Intel restock</div></div>
        <button class="btn btn-emerald" onclick="buyRealSku('coins_1500')">$0.99</button>
      </div>
      <div class="row-item">
        <div><strong>5,000 Coins Vault</strong><div style="font-size:0.7rem; color:var(--muted);">Unlock multiple Factions & Gold Foil upgrades</div></div>
        <button class="btn btn-gold" onclick="buyRealSku('coins_5000')">$2.99</button>
      </div>
    </div>

    <div class="glass-box">
      <h3>Unlock Faction Rosters with Coins</h3>
      <div id="shopFactionList" style="margin-top:8px;"></div>
    </div>
  </section>

  <!-- TAB 5: SETTINGS & ACCESSIBILITY -->
  <section class="tab-view" id="tab-settings">
    <div class="glass-box">
      <h2>Studio Audio, Visual & Accessibility Settings</h2>
      <div class="row-item" style="margin-top:10px;">
        <div>
          <strong>Multi-Track Synth Soundtrack Volume</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Stereo pad, sub-bass pulse, and delay arpeggiator</div>
        </div>
        <input type="range" min="0" max="100" value="42" id="musicSlider" oninput="updateVolumes()" />
      </div>
      <div class="row-item">
        <div>
          <strong>Domino Card-Snap & Harmonic SFX Volume</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Pitch-escalating card snaps and marimba chords</div>
        </div>
        <input type="range" min="0" max="100" value="88" id="sfxSlider" oninput="updateVolumes()" />
      </div>
      <div class="row-item">
        <div>
          <strong>Visual Arena Theme</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Switch background lighting and card trim</div>
        </div>
        <button class="btn btn-slate" id="themeBtn" onclick="cycleTheme()">SLATE</button>
      </div>
      <div class="row-item">
        <div>
          <strong>Default Card Elimination Rule</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Auto-flip eliminated cards or flip manually</div>
        </div>
        <button class="btn btn-slate" id="flipRuleBtn" onclick="toggleFlipRule()">Auto-Flip</button>
      </div>
      <div class="row-item">
        <div>
          <strong>High-Contrast / Colorblind Symbols</strong>
          <div style="font-size:0.7rem; color:var(--muted);">High-visibility borders and geometric trait symbols</div>
        </div>
        <button class="btn btn-slate" id="contrastBtn" onclick="toggleHighContrast()">Standard</button>
      </div>
      <div class="row-item">
        <div>
          <strong>Particle & Motion Intensity</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Toggle 60fps particle bursts</div>
        </div>
        <button class="btn btn-slate" id="motionBtn" onclick="toggleReducedMotion()">Full 60fps</button>
      </div>
      <div class="row-item">
        <div>
          <strong>Haptic Vibration Feedback</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Tactile pulse on card flips</div>
        </div>
        <button class="btn btn-slate" id="hapticBtn" onclick="toggleHaptics()">Enabled</button>
      </div>
      <div class="row-item">
        <div>
          <strong>Agent Username</strong>
          <div style="font-size:0.7rem; color:var(--muted);">Update your public multiplayer handle</div>
        </div>
        <button class="btn btn-primary" onclick="openModal('userModal')">Edit Username</button>
      </div>
    </div>
  </section>

  <!-- FULLSCREEN ZERO-CLIPPING GAMEPLAY ARENA -->
  <section id="arenaView">
    <div class="arena-top-bar">
      <div class="secret-chip" onclick="openDossier(mySecretIdx, true)">
        <img id="arenaSecretImg" alt="Secret" />
        <div>
          <div style="font-size:0.56rem; color:var(--muted); font-weight:800;">YOUR SECRET (3D VIEW)</div>
          <strong style="font-size:0.76rem; color:var(--gold-hi);" id="arenaSecretName">Operative</strong>
        </div>
      </div>

      <div style="text-align:center;">
        <strong class="display-font" style="font-size:0.82rem; color:var(--primary-hi);" id="arenaModeTitle">QUICK PLAY</strong>
        <div style="font-size:0.6rem; color:var(--muted); font-weight:800;" id="arenaSubCounter">YOU 24 • RIVAL 24</div>
      </div>

      <div style="text-align:right;">
        <div style="font-size:0.64rem; color:var(--muted); font-weight:700;" id="arenaRivalName">Rival</div>
        <strong style="font-size:0.78rem; color:var(--crimson-hi);" id="arenaRivalLeft">24 Left</strong>
      </div>
    </div>

    <div class="arena-status-strip">
      <span id="arenaCoach" style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">YOUR TURN: Ask a trait, tap 🔍 for 3D view, or use a Skill!</span>
      <div class="intel-consumables">
        <button class="intel-btn skill-ready" onclick="useFactionAbility()" id="btnFactionSkill">★ <span id="hudSkillName">Scan</span></button>
        <button class="intel-btn" onclick="useIntelChip('radar')">Radar:<span id="hudRadarCnt">2</span></button>
        <button class="intel-btn" onclick="useIntelChip('snipe')">Snipe:<span id="hudSnipeCnt">1</span></button>
        <button class="intel-btn" onclick="useIntelChip('jam')">Jam:<span id="hudJamCnt">1</span></button>
      </div>
    </div>

    <div class="board-grid-24" id="boardGrid24"></div>

    <div class="arena-bottom-dock">
      <button class="btn btn-slate" style="padding:10px 12px;" onclick="leaveArena()">Exit</button>
      <button class="btn btn-primary" style="flex:1.5;" id="btnAskTrait" onclick="openQuestionModal()">Ask Trait (10)</button>
      <button class="btn btn-emerald" style="flex:1.2; display:none;" id="btnDoneManual" onclick="finishManualTurn()">Done Flipping</button>
      <button class="btn btn-crimson" style="flex:1;" id="btnTakedown" onclick="toggleTakedown()">Takedown</button>
    </div>
  </section>

  <!-- Bottom Navigation Dock -->
  <nav class="bottom-dock" id="bottomNav">
    <div class="dock-inner">
      <button class="nav-tab active" data-tab="play" onclick="switchTab('play')">
        <svg class="ico" viewBox="0 0 24 24"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        Play
      </button>
      <button class="nav-tab" data-tab="friends" onclick="switchTab('friends')">
        <svg class="ico" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        Friends
      </button>
      <button class="nav-tab" data-tab="ranks" onclick="switchTab('ranks')">
        <svg class="ico" viewBox="0 0 24 24"><path d="M18 20V10M12 20V4M6 20v-6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>
        Ranks
      </button>
      <button class="nav-tab" data-tab="shop" onclick="switchTab('shop')">
        <svg class="ico" viewBox="0 0 24 24"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6" stroke="#060913" stroke-width="2"/></svg>
        Shop
      </button>
      <button class="nav-tab" data-tab="settings" onclick="switchTab('settings')">
        <svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        Settings
      </button>
    </div>
  </nav>

  <!-- Modals -->
  <div class="modal-backdrop" id="userModal">
    <div class="modal-panel" style="text-align:center;">
      <h2>Agent Registration</h2>
      <p style="font-size:0.78rem; color:var(--muted); margin:6px 0 12px;">Enter your public Agent Username for Leaderboards and Direct Friend Duels:</p>
      <input type="text" id="usernameInput" style="width:100%; background:#05070f; border:1.5px solid var(--border-hi); border-radius:10px; padding:11px; color:#fff; text-align:center; font-size:1rem; font-weight:700; margin-bottom:12px;" maxlength="15" placeholder="e.g. ViperZero" />
      <button class="btn btn-primary" style="width:100%;" onclick="saveUsername()">Save Agent Username</button>
    </div>
  </div>

  <div class="modal-backdrop" id="questionModal">
    <div class="modal-panel">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <h2>Select Trait Question (10 Traits)</h2>
        <button class="btn btn-slate" style="padding:5px 10px; font-size:0.72rem;" onclick="closeModal('questionModal')">Close</button>
      </div>
      <div id="questionListBox"></div>
    </div>
  </div>

  <!-- Interactive 3D Figurine Turntable & Dossier Modal -->
  <div class="modal-backdrop" id="dossierModal">
    <div class="modal-panel" style="text-align:center;">
      <span style="font-size:0.65rem; font-weight:800; color:var(--primary-hi);" id="dossierTag">YOUR SECRET OPERATIVE</span>
      <h2 id="dossierName" style="margin:2px 0 6px;">Operative</h2>
      <div class="turntable-stage" id="dossier3DStage"></div>
      <div id="dossierTraitsList" style="display:grid; grid-template-columns:1fr 1fr; gap:5px; text-align:left; margin-bottom:12px;"></div>
      <div style="display:flex; gap:8px;">
        <button class="btn btn-crimson" style="flex:1;" id="dossierFlipBtn" onclick="flipInspectedCard()">Flip Card</button>
        <button class="btn btn-primary" style="flex:1.2;" onclick="closeDossierModal()">Continue</button>
      </div>
    </div>
  </div>

  <div class="modal-backdrop" id="resultModal">
    <div class="modal-panel" style="text-align:center;">
      <span style="font-size:0.65rem; font-weight:800; color:var(--gold-hi);" id="resBadge">MATCH COMPLETE</span>
      <h2 id="resTitle" style="font-size:1.6rem; margin-top:4px;">TAKEDOWN CONFIRMED!</h2>
      <p id="resSub" style="font-size:0.8rem; color:var(--muted); margin:4px 0 10px;"></p>
      <div style="width:140px; height:172px; margin:0 auto 10px; border-radius:14px; overflow:hidden; border:2.5px solid var(--gold-hi); background:#000;">
        <img id="resImg" style="width:100%; height:100%; object-fit:cover;" alt="Secret" />
      </div>
      <div id="resRewards" style="color:var(--gold-hi); font-family:'Chakra Petch',sans-serif; font-weight:700; font-size:0.95rem; margin-bottom:12px;"></div>
      <div style="display:flex; gap:8px;">
        <button class="btn btn-slate" style="flex:1;" onclick="leaveArena()">Lobby</button>
        <button class="btn btn-emerald" style="flex:1.4;" id="resNextBtn" onclick="nextRoundOrRematch()">Play Again</button>
      </div>
    </div>
  </div>

  <div class="toast-banner" id="toastBanner">
    <h3 id="toastTitle" style="color:var(--primary-hi);">CONFIRMED</h3>
    <p id="toastSub" style="font-size:0.8rem; margin-top:3px; font-weight:700;"></p>
  </div>

  <script src="js/data.js"></script>
  <script src="js/audio.js"></script>
  <script src="js/renderer3d.js"></script>
  <script src="js/game.js"></script>
</body>
</html>
"""

def build():
    # Remove old hallucinated AI assets & obsolete files so nothing conflicts
    for obsolete in ["assets", "sfx", "rosters.json", "build_studio_assets.py", "generate_art.py"]:
        if os.path.isdir(obsolete):
            shutil.rmtree(obsolete)
        elif os.path.isfile(obsolete):
            os.remove(obsolete)

    for rel_path, content in FILES.items():
        dir_name = os.path.dirname(rel_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content.lstrip("\n"))
        print(f"[BUILT] {rel_path} ({len(content)//1024 + 1} KB)")

    print("\n✅ Trait Takedown 3D WebGL Studio Edition built in <1 second!")

if __name__ == "__main__":
    build()
