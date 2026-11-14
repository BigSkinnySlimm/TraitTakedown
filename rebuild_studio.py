#!/usr/bin/env python3
"""
Trait Takedown v10.0 — Pre-Baked High-Res Creature Concept Art + Volumetric Shader Fallback,
Fixed Non-Collapsing Mobile Grids, Instant-Boot Arena & Signed Native Android APK Builder.
"""

import os
import shutil
import time
import urllib.parse
import urllib.request
from pathlib import Path

def get_project_dir() -> Path:
    termux_docs = Path.home() / "storage" / "shared" / "Documents" / "TraitTakedown"
    if termux_docs.parent.exists():
        termux_docs.mkdir(parents=True, exist_ok=True)
        return termux_docs
    return Path.cwd()

def is_protected(path: Path) -> bool:
    name = path.name.lower()
    if name in {".git", ".gitignore", "cname", "license", "rebuild_studio.py", "assets"}:
        return True
    protected_keywords = ("privacy", "terms", "tos", "legal", "policy")
    return any(k in name for k in protected_keywords)

def clean_project_directory(root: Path):
    for item in root.iterdir():
        if is_protected(item):
            continue
        try:
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        except Exception:
            pass

def write_file(root: Path, rel_path: str, content: str):
    target = root / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"[+] Wrote {rel_path} ({len(content):,} bytes)")

# ============================================================================
# 1. PRE-BAKE 24 ANATOMICALLY LOCKED CREATURE & MECHA ILLUSTRATIONS
# ============================================================================
CREATURE_PROMPTS = [
    ("u01", "giant armored snapping tortoise kaiju monster, massive spiked obsidian shell with glowing orange lava cracks, twin shoulder plasma cannons, reptilian scales, no human, masterpiece digital concept art, Marvel Snap card art, dramatic lighting"),
    ("u02", "sleek cybernetic stealth panther android mecha, glowing cyan neon optic visor, carbon fiber stealth armor, electromagnetic rail sniper rifle, lightning aura, no human face, AAA sci-fi card illustration"),
    ("u03", "majestic six-winged golden phoenix valkyrie seraph creature, radiant solar fire wings, ornate celestial plate armor, blazing sun lance, epic fantasy card game art, cinematic lighting"),
    ("u04", "colossal deep sea abyssal kraken leviathan monster, glowing purple bioluminescent tentacles, armored chitinous cephalopod mantle, dark void vortex, digital painting masterpiece"),
    ("u05", "cybernetic chrome basilisk dragon serpent, reflective liquid metal scales, high voltage blue electric arcs, twin heavy plasma cannons, sci-fi monster card art"),
    ("u06", "giant armored shadow scorpion arachnid monster, jagged purple spiked carapace, dripping venom blades, glowing crimson compound eyes, dark abyssal cave background, AAA game art"),
    ("u07", "towering golden mechanical paladin construct, glowing solar reactor core in chest, ornate aegis shield plating, blazing spear of light, cinematic sci-fi fantasy illustration"),
    ("u08", "hulking industrial ironclad juggernaut golem, heavy rusted steel spiked armor, molten furnace core in chest, colossal rocket siege hammer, earth shatter sparks, concept art"),
    ("u09", "neon cybernetic praying mantis assassin creature, translucent holographic stealth blades, glowing cyan and magenta exoskeleton, rain-slicked cyberpunk background, digital art"),
    ("u10", "arctic abyssal kraken octopod monster, encrusted with glowing blue glacial ice armor, freezing cryo plasma cannon, deep ocean trench, AAA creature illustration"),
    ("u11", "celestial armored griffin hawk valkyrie, radiant golden feathers, sleek stealth weave armor, high-tech solar railgun, sunrise clouds background, masterpiece card art"),
    ("u12", "colossal volcanic magma golem titan, body made of cracked black basalt rock and flowing lava rivers, glowing golden aegis runes, burning siege hammer, epic fantasy art"),
    ("u13", "ancient frost wyrm ice dragon, translucent crystalline chitin scales, swirling blizzard aura, glowing cyan eyes, jagged ice spires background, AAA digital painting"),
    ("u14", "cybernetic storm hawk raptor, gleaming silver chitinous wing blades, crackling blue lightning feathers, sniper railgun mount, high altitude thunderclouds, card game art"),
    ("u15", "giant mechanical black widow spider mecha, glossy cobalt blue armor plating, eight articulated razor legs, cryo rail rifle mounted on thorax, glowing red eyes"),
    ("u16", "heavily armored earth drake dragon, thick bronze fortress plate armor, glowing amber magma vents, massive spiked tail and siege hammer claws, epic monster illustration"),
    ("u17", "phantom void wraith android assassin, tattered dark energy cloak, glowing violet singularity core, shadowy energy tendrils, cosmic rift background, AAA sci-fi art"),
    ("u18", "towering cybernetic centurion mecha knight, polished titanium aegis armor, crackling blue plasma lance, glowing cyan crest visor, futuristic arena background"),
    ("u19", "armored frost owl raptor monster, razor sharp ice crystal feathers, spiked glacial shell armor, glowing cyan talons and venom blades, blizzard night sky"),
    ("u20", "molten slag octopod lava kraken, heavy ironclad spiked shell mantle, tentacles made of liquid fire and obsidian, twin heavy plasma cannons, volcanic forge"),
    ("u21", "crystalline prism weaver spider queen, iridescent golden glass arachnid armor, refracting rainbow solar laser beams, eight golden mechanical legs, sacred temple"),
    ("u22", "heavy cryo automaton siege robot, frost-covered spiked titanium armor, glowing sub-zero blue reactor, giant ice-crushing siege hammer, arctic storm"),
    ("u23", "cosmic rift nautilus cephalopod monster, ancient spiral armored shell with glowing purple runes, void gravity tendrils, floating in deep space nebula, digital art"),
    ("u24", "colossal titan anvil war mecha, ultra-heavy gunmetal chitin carapace, glowing molten orange reactor vents, dual shoulder siege plasma cannons, cinematic sci-fi art")
]

def download_prebaked_art(root: Path):
    art_dir = root / "assets" / "art"
    art_dir.mkdir(parents=True, exist_ok=True)
    print("[*] Checking / Pre-Baking 24 High-Resolution Creature Illustrations...")

    for idx, (uid, prompt) in enumerate(CREATURE_PROMPTS):
        target_file = art_dir / f"{uid}.jpg"
        if target_file.exists() and target_file.stat().st_size > 15000:
            print(f"    [CACHED] {uid}.jpg ({target_file.stat().st_size:,} bytes)")
            continue

        encoded = urllib.parse.quote(prompt)
        seed = 9000 + idx * 37
        urls = [
            f"https://image.pollinations.ai/prompt/{encoded}?width=480&height=640&seed={seed}&nologo=true&model=flux",
            f"https://image.pollinations.ai/prompt/{encoded}?width=480&height=640&seed={seed}&nologo=true"
        ]
        downloaded = False
        for url in urls:
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) TraitTakedownBuilder/10.0"}
                )
                with urllib.request.urlopen(req, timeout=12) as resp:
                    data = resp.read()
                    if len(data) > 12000:
                        target_file.write_bytes(data)
                        print(f"    [BAKED]  Downloaded {uid}.jpg ({len(data):,} bytes)")
                        downloaded = True
                        time.sleep(0.35)
                        break
            except Exception as e:
                pass
        if not downloaded:
            print(f"    [SHADER] {uid} will use high-density procedural volumetric shader canvas")

# ============================================================================
# 2. ANDROID MANIFEST & ACTIVITY
# ============================================================================
ANDROID_MANIFEST_XML = r"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.traittakedown.studio"
    android:versionCode="100"
    android:versionName="10.0.0">

    <uses-sdk android:minSdkVersion="24" android:targetSdkVersion="34" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:label="Trait Takedown"
        android:hardwareAccelerated="true"
        android:usesCleartextTraffic="true"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen">
        <activity
            android:name="com.traittakedown.studio.MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""

MAIN_ACTIVITY_JAVA = r"""package com.traittakedown.studio;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {
    private WebView engineView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(
            WindowManager.LayoutParams.FLAG_FULLSCREEN,
            WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
            | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
            | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
            | View.SYSTEM_UI_FLAG_FULLSCREEN
            | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
        );

        engineView = new WebView(this);
        engineView.setBackgroundColor(Color.parseColor("#040711"));
        WebSettings s = engineView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        s.setMediaPlaybackRequiresUserGesture(false);

        engineView.setWebViewClient(new WebViewClient());
        engineView.setWebChromeClient(new WebChromeClient());
        setContentView(engineView);
        engineView.loadUrl("file:///android_asset/www/index.html");
    }

    @Override
    public void onBackPressed() {
        if (engineView != null && engineView.canGoBack()) {
            engineView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
"""

# ============================================================================
# 3. INDEX.HTML — Studio Game Shell (Zero Broken Images, Fixed Grid Layouts)
# ============================================================================
INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
  <title>Trait Takedown | Tactical Card Arena</title>
  <link rel="stylesheet" href="css/studio.css" />
  <script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"></script>
</head>
<body>
  <canvas id="vfx-canvas"></canvas>

  <!-- Ultimate Cut-In Overlay -->
  <div id="ultimate-cutin" class="ultimate-cutin hidden">
    <div class="cutin-slash">
      <img id="cutin-img" src="" alt="Operative" />
      <div class="cutin-text">
        <span id="cutin-faction">SOLARIS ULTIMATE</span>
        <h2 id="cutin-title">HELIOS ORBITAL SWEEP</h2>
      </div>
    </div>
  </div>

  <div id="app-viewport">
    <!-- TOP PERSISTENT TELEMETRY HUD -->
    <header class="top-hud">
      <div class="player-badge">
        <div class="avatar-ring">TT</div>
        <div class="player-meta">
          <div class="callsign-row">
            <strong id="ui-callsign">Commander</strong>
            <span class="online-dot"></span>
          </div>
          <div class="rank-sub">
            <span id="ui-rank-badge" class="tier-pill">GOLD I</span>
            <span id="ui-elo">1,200 MMR</span>
          </div>
        </div>
      </div>

      <div class="economy-cluster">
        <div class="res-pill">
          <span class="res-icon cyan">◈</span>
          <strong id="ui-credits">1,500</strong>
        </div>
        <div class="res-pill gold">
          <span class="res-icon">❖</span>
          <strong id="ui-gems">200</strong>
        </div>
        <a class="apk-pill" href="https://github.com/BigSkinnySlimm/TraitTakedown/releases/latest/download/TraitTakedown-Android-Native.apk">📲 APK</a>
        <button class="icon-circle" id="btn-audio-toggle">🔊</button>
      </div>
    </header>

    <!-- VIEW 1: HOME SHOWCASE STAGE -->
    <section id="view-lobby" class="screen-view active">
      <div class="lobby-center-stage">
        <div class="lobby-pedestal-glow"></div>

        <div class="showcase-wrapper">
          <div class="showcase-tag">FEATURED OPERATIVE // TAP CARD TO CYCLE (1/24)</div>
          <div id="lobby-showcase-card" class="holo-card showcase-size">
            <div class="holo-card-inner">
              <img id="showcase-art" src="" alt="Featured Operative" />
              <div class="holo-glare"></div>
              <div class="card-top-badges">
                <span id="showcase-faction" class="c-badge faction">IRONCLAD</span>
                <span id="showcase-element" class="c-badge element">TERRA</span>
              </div>
              <div class="card-bottom-plate">
                <h2 id="showcase-name">Spiked Tortoise</h2>
                <div id="showcase-traits" class="card-trait-line">Reptilian • Spiked Shell • Plasma Cannon</div>
              </div>
            </div>
          </div>
        </div>

        <div class="lobby-cta-stack">
          <button id="btn-play-ranked" class="btn-mega-play">
            <span class="play-main">⚡ ENTER RANKED ARENA</span>
            <span class="play-sub">LIVE AUTO-MATCHMAKING • 24 OPERATIVES READY</span>
          </button>
          <div class="quick-modes-row">
            <button id="btn-quick-friend" class="btn-glass">⚔️ FRIENDS & DUELS</button>
            <button id="btn-quick-inspect" class="btn-glass">🃏 24 CARD CODEX</button>
          </div>
        </div>
      </div>
    </section>

    <!-- VIEW 2: TACTICAL BATTLE ARENA (ALWAYS POPULATED ON BOOT) -->
    <section id="view-battle" class="screen-view">
      <div class="battle-topbar">
        <div class="vs-pill">
          <span class="vs-label">VS</span>
          <strong id="battle-opp-name">Valkyrie_IX</strong>
          <span id="battle-opp-elo" class="opp-mmr">(1,240)</span>
        </div>

        <div id="turn-pill" class="turn-indicator your-turn">YOUR TURN</div>

        <div class="suspect-counters">
          <span class="s-count cyan">YOU: <b id="you-rem">24</b></span>
          <span class="s-count gold">FOE: <b id="opp-rem">24</b></span>
          <span class="timer-pill" id="battle-timer">30s</span>
          <button id="btn-new-match" class="btn-mini-reset" title="New Match">↻</button>
        </div>
      </div>

      <div class="combat-ticker" id="combat-ticker">
        <span>📡 Tap any trait chip below to preview matching suspects, then tap SCAN TRAIT.</span>
      </div>

      <div class="arena-grid-wrapper">
        <div id="battle-grid" class="battle-grid"></div>
      </div>

      <div class="battle-command-dock">
        <div class="secret-dock-box">
          <div id="my-secret-mini" class="secret-mini-card">
            <img id="my-secret-img" src="" alt="" />
            <div class="secret-mini-meta">
              <small>YOUR OPERATIVE</small>
              <strong id="my-secret-name">Spiked Tortoise</strong>
              <span id="my-secret-traits">Ironclad • Terra</span>
            </div>
          </div>
          <button id="btn-fire-ultimate" class="btn-ultimate">
            <span>⚡ ULTIMATE</span>
            <small id="ult-name-label">READY</small>
          </button>
        </div>

        <div class="scanner-dock-box">
          <div class="cat-tabs">
            <button class="cat-tab active" data-cat="faction">FACTION</button>
            <button class="cat-tab" data-cat="species">SPECIES</button>
            <button class="cat-tab" data-cat="armor">ARMOR</button>
            <button class="cat-tab" data-cat="weapon">WEAPON</button>
            <button class="cat-tab" data-cat="element">ELEMENT</button>
          </div>

          <div class="val-chips-row" id="scanner-val-chips"></div>

          <div class="action-buttons-row">
            <button id="btn-fire-scan" class="btn-action-scan">
              📡 SCAN TRAIT: <span id="selected-trait-preview">IRONCLAD</span>
            </button>
            <button id="btn-toggle-accuse" class="btn-action-accuse">
              🎯 ACCUSE
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- VIEW 3: 24-OPERATIVE HOLO COLLECTION GALLERY (FIXED NON-COLLAPSING GRID) -->
    <section id="view-collection" class="screen-view">
      <div class="subview-header">
        <h2>24 OPERATIVE HOLO CODEX</h2>
        <p>Tap any card to open the full-resolution 3D Holographic Inspector & Faction Ultimate details.</p>
      </div>
      <div class="collection-scroll-area">
        <div id="collection-grid" class="collection-grid"></div>
      </div>
    </section>

    <!-- VIEW 4: RANKED ELO & FRIENDS -->
    <section id="view-social" class="screen-view">
      <div class="social-scroll-area">
        <div class="social-split">
          <div class="glass-panel">
            <h3>👥 FRIENDS & DIRECT DUEL CHALLENGES</h3>
            <div class="form-row">
              <input type="text" id="input-callsign" class="neon-input" placeholder="Your Callsign..." maxlength="16" />
              <button id="btn-save-callsign" class="btn-neon cyan">SAVE ID</button>
            </div>
            <div class="form-row">
              <input type="text" id="input-friend" class="neon-input" placeholder="Add Friend Callsign..." maxlength="16" />
              <button id="btn-add-friend" class="btn-neon gold">+ ADD FRIEND</button>
            </div>
            <div id="friends-list" class="scroll-list"></div>
          </div>

          <div class="glass-panel">
            <h3>🏆 GLOBAL RANKED ELO LADDER</h3>
            <div class="rank-crest-banner">
              <div class="crest-shield">🏆</div>
              <div>
                <strong id="ranked-summary-bar">GOLD I — 1,200 MMR</strong>
                <div id="ranked-winloss-sub" style="font-size:0.7rem;color:#8ea6cc;">0W - 0L • Season 01 Active</div>
              </div>
            </div>
            <div id="leaderboard-list" class="scroll-list"></div>
            <h4 class="sub-h4">RECENT MATCH TELEMETRY</h4>
            <div id="history-list" class="scroll-list"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- VIEW 5: SEASON PASS & ARMORY -->
    <section id="view-shop" class="screen-view">
      <div class="social-scroll-area">
        <div class="social-split">
          <div class="glass-panel">
            <div class="pass-header-row">
              <div>
                <h3>🎖️ SEASON 01: SOVEREIGN HORIZON PASS</h3>
                <p style="font-size:0.74rem;color:#8ea6cc;">SEASON XP: <strong id="ui-pass-xp" style="color:#00f0ff;">400</strong> / 1,200</p>
              </div>
              <button id="btn-buy-pass" class="btn-neon gold">ELITE PASS (150 ❖)</button>
            </div>
            <div class="xp-progress-track"><div id="xp-progress-fill" class="xp-progress-fill" style="width:33%;"></div></div>
            <div id="pass-tiers-container" class="scroll-list"></div>
          </div>

          <div class="glass-panel">
            <h3>💎 HOLOGRAPHIC ARMORY STORE</h3>
            <div id="armory-items-container" class="scroll-list"></div>
            <div class="legal-footer-links">
              <a href="privacy.html" target="_blank">Privacy Policy</a> •
              <a href="terms.html" target="_blank">Terms of Service</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- BOTTOM STUDIO NAVIGATION DOCK -->
    <nav class="bottom-nav">
      <button class="nav-tab active" data-view="view-lobby">
        <span class="nav-ico">🏠</span><small>HOME</small>
      </button>
      <button class="nav-tab" data-view="view-battle">
        <span class="nav-ico">⚔️</span><small>ARENA</small>
      </button>
      <button class="nav-tab" data-view="view-collection">
        <span class="nav-ico">🃏</span><small>ROSTER (24)</small>
      </button>
      <button class="nav-tab" data-view="view-social">
        <span class="nav-ico">🏆</span><small>RANKED</small>
      </button>
      <button class="nav-tab" data-view="view-shop">
        <span class="nav-ico">💎</span><small>PASS & SHOP</small>
      </button>
    </nav>
  </div>

  <!-- MODAL: Matchmaking Queue -->
  <div id="modal-queue" class="modal-overlay hidden">
    <div class="modal-card">
      <div class="radar-circle"><div class="radar-beam"></div></div>
      <h3>SEARCHING GLOBAL ARENA...</h3>
      <p style="font-size:0.76rem;color:#8ea6cc;">Pairing via Cloud Broker (MMR ±100)</p>
      <div id="queue-clock" style="font-size:1.3rem;font-weight:900;color:#00f0ff;">00:00</div>
      <button id="btn-cancel-queue" class="btn-neon red">CANCEL SEARCH</button>
    </div>
  </div>

  <!-- MODAL: Full-Res Card Inspector -->
  <div id="modal-inspect" class="modal-overlay hidden">
    <div class="modal-card">
      <div id="inspect-card-mount" class="holo-card showcase-size"></div>
      <div class="inspect-ability-box">
        <strong id="inspect-ult-title" style="color:#ffcc33;font-size:0.8rem;">FACTION ULTIMATE</strong>
        <p id="inspect-ult-desc" style="font-size:0.72rem;color:#c8daf2;margin-top:0.25rem;"></p>
      </div>
      <button id="btn-close-inspect" class="btn-neon cyan" style="width:100%;">CLOSE INSPECTOR</button>
    </div>
  </div>

  <!-- MODAL: Match Result -->
  <div id="modal-result" class="modal-overlay hidden">
    <div class="modal-card">
      <div id="result-badge" style="font-size:1.4rem;font-weight:900;color:#ffcc33;">🏆 VICTORY</div>
      <h2 id="result-heading">TARGET NEUTRALIZED</h2>
      <p id="result-details" style="font-size:0.78rem;color:#c8daf2;"></p>
      <div id="result-elo-pill" style="font-size:1rem;font-weight:900;color:#00ff9d;">+24 MMR (1,224 ELO)</div>
      <div style="font-size:0.75rem;color:#ffcc33;font-weight:800;">+200 ◈ CREDITS  •  +150 SEASON XP</div>
      <div style="display:flex;gap:0.5rem;width:100%;">
        <button id="btn-play-again" class="btn-neon cyan" style="flex:1;">⚡ NEXT MATCH</button>
        <button id="btn-result-lobby" class="btn-glass" style="flex:1;">LOBBY</button>
      </div>
    </div>
  </div>

  <script src="js/roster.js"></script>
  <script src="js/artEngine.js"></script>
  <script src="js/vfxEngine.js"></script>
  <script src="js/audio.js"></script>
  <script src="js/network.js"></script>
  <script src="js/gameController.js"></script>
</body>
</html>
"""

# ============================================================================
# 4. CSS/STUDIO.CSS — Fixed Non-Collapsing Grid Tracks & Tactical Blast Doors
# ============================================================================
STUDIO_CSS = r"""
:root {
  --bg-void: #040711;
  --bg-panel: rgba(13, 23, 45, 0.94);
  --cyan: #00f0ff;
  --blue: #0066ff;
  --gold: #ffcc33;
  --red: #ff2a5f;
  --green: #00ff9d;
  --text: #f2f7ff;
  --muted: #8ea6cc;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

html, body {
  width: 100%;
  height: 100dvh;
  overflow: hidden;
  background: radial-gradient(circle at 50% 20%, #162e5c 0%, #070e1f 55%, var(--bg-void) 100%);
  color: var(--text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

#vfx-canvas {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 45;
}

#app-viewport {
  position: relative;
  width: 100%;
  height: 100dvh;
  max-width: 1440px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 10;
}

/* TOP HUD */
.top-hud {
  height: 54px;
  padding: 0 0.75rem;
  background: rgba(4, 8, 18, 0.96);
  border-bottom: 1px solid rgba(0, 240, 255, 0.28);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.player-badge { display: flex; align-items: center; gap: 0.55rem; }
.avatar-ring {
  width: 36px; height: 36px; border-radius: 9px;
  background: linear-gradient(135deg, var(--cyan), var(--blue));
  color: #02060d; font-weight: 900; font-size: 0.9rem;
  display: grid; place-items: center;
  box-shadow: 0 0 12px rgba(0, 240, 255, 0.45);
}
.callsign-row { display: flex; align-items: center; gap: 0.35rem; font-size: 0.8rem; }
.online-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); }
.rank-sub { display: flex; align-items: center; gap: 0.35rem; font-size: 0.65rem; color: var(--muted); }
.tier-pill {
  background: rgba(255, 204, 51, 0.18);
  border: 1px solid rgba(255, 204, 51, 0.55);
  color: var(--gold);
  padding: 0.05rem 0.35rem;
  border-radius: 4px;
  font-weight: 800;
  font-size: 0.58rem;
}

.economy-cluster { display: flex; align-items: center; gap: 0.38rem; }
.res-pill {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(0, 240, 255, 0.28);
  padding: 0.24rem 0.52rem;
  border-radius: 99px;
  font-size: 0.72rem;
  display: flex;
  align-items: center;
  gap: 0.22rem;
}
.res-pill.gold { border-color: rgba(255, 204, 51, 0.45); color: var(--gold); }
.res-icon.cyan { color: var(--cyan); }
.apk-pill {
  text-decoration: none;
  background: linear-gradient(135deg, var(--gold), #ff8800);
  color: #040812; font-weight: 900; font-size: 0.66rem;
  padding: 0.26rem 0.5rem; border-radius: 6px;
}
.icon-circle {
  width: 30px; height: 30px; border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text); cursor: pointer;
}

/* SCREEN VIEWS */
.screen-view {
  display: none;
  flex: 1;
  min-height: 0;
  overflow: hidden;
  position: relative;
}
.screen-view.active {
  display: flex;
  flex-direction: column;
}

/* HOME LOBBY */
.lobby-center-stage {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  padding: 0.5rem 1rem;
  position: relative;
}
.lobby-pedestal-glow {
  position: absolute;
  width: 300px; height: 300px; border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 240, 255, 0.22) 0%, transparent 70%);
  pointer-events: none;
}
.showcase-wrapper { display: flex; flex-direction: column; align-items: center; gap: 0.38rem; z-index: 2; }
.showcase-tag {
  font-size: 0.62rem; font-weight: 800; letter-spacing: 0.12em; color: var(--cyan);
  background: rgba(0, 240, 255, 0.12); border: 1px solid rgba(0, 240, 255, 0.35);
  padding: 0.18rem 0.6rem; border-radius: 99px;
}

/* HOLOGRAPHIC CARDS */
.holo-card {
  position: relative;
  border-radius: 14px;
  background: #0b1428;
  border: 2px solid rgba(0, 240, 255, 0.65);
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.8), 0 0 22px rgba(0, 240, 255, 0.25);
  overflow: hidden;
  cursor: pointer;
}
.holo-card.showcase-size {
  width: min(235px, 58vw);
  height: min(305px, 42dvh);
}
.holo-card.foil-active {
  border-color: var(--gold);
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.85), 0 0 28px rgba(255, 204, 51, 0.5);
}
.holo-card-inner { position: relative; width: 100%; height: 100%; }
.holo-card-inner img { width: 100%; height: 100%; object-fit: cover; display: block; }
.holo-glare {
  position: absolute; inset: 0;
  background: linear-gradient(125deg, transparent 25%, rgba(0, 240, 255, 0.18) 45%, rgba(255, 204, 51, 0.2) 55%, transparent 75%);
  mix-blend-mode: screen; pointer-events: none;
}
.card-top-badges {
  position: absolute; top: 6px; left: 6px; right: 6px;
  display: flex; justify-content: space-between; pointer-events: none; z-index: 2;
}
.c-badge {
  font-size: 0.56rem; font-weight: 900; padding: 0.12rem 0.38rem;
  border-radius: 4px; letter-spacing: 0.05em; text-transform: uppercase;
}
.c-badge.faction { background: rgba(4, 9, 20, 0.85); border: 1px solid rgba(255, 255, 255, 0.3); color: #fff; }
.c-badge.element { background: rgba(4, 9, 20, 0.85); border: 1px solid var(--cyan); color: var(--cyan); }
.card-bottom-plate {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 1.4rem 0.45rem 0.45rem;
  background: linear-gradient(0deg, rgba(2, 5, 12, 0.98) 50%, transparent 100%);
  text-align: center; pointer-events: none; z-index: 2;
}
.card-bottom-plate h2 { font-size: 0.92rem; font-weight: 900; text-shadow: 0 2px 6px #000; }
.card-trait-line { font-size: 0.6rem; color: var(--cyan); font-weight: 700; margin-top: 0.1rem; }

.lobby-cta-stack { width: min(400px, 92vw); display: flex; flex-direction: column; gap: 0.5rem; z-index: 2; }
.btn-mega-play {
  width: 100%; padding: 0.8rem 1rem; border-radius: 13px;
  border: 2px solid var(--cyan);
  background: linear-gradient(135deg, #00d2ff 0%, #0051ff 100%);
  color: #fff; cursor: pointer;
  box-shadow: 0 0 26px rgba(0, 240, 255, 0.45);
  display: flex; flex-direction: column; align-items: center;
}
.play-main { font-size: 1.02rem; font-weight: 900; letter-spacing: 0.06em; }
.play-sub { font-size: 0.6rem; opacity: 0.92; font-weight: 700; margin-top: 0.1rem; }
.quick-modes-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.45rem; }
.btn-glass {
  background: rgba(15, 27, 52, 0.86);
  border: 1px solid rgba(0, 240, 255, 0.38);
  color: var(--text); padding: 0.55rem; border-radius: 10px;
  font-weight: 800; font-size: 0.72rem; cursor: pointer;
}

/* BATTLE ARENA */
.battle-topbar {
  height: 38px; padding: 0 0.65rem;
  background: rgba(6, 12, 26, 0.95);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex; justify-content: space-between; align-items: center;
  font-size: 0.72rem; flex-shrink: 0;
}
.vs-pill { display: flex; align-items: center; gap: 0.3rem; }
.vs-label { background: var(--red); color: #fff; font-weight: 900; font-size: 0.58rem; padding: 0.1rem 0.28rem; border-radius: 4px; }
.opp-mmr { color: var(--muted); font-size: 0.64rem; }
.turn-indicator {
  padding: 0.18rem 0.6rem; border-radius: 99px; font-weight: 900; font-size: 0.65rem;
  background: rgba(255, 204, 51, 0.18); color: var(--gold); border: 1px solid var(--gold);
}
.turn-indicator.your-turn {
  background: rgba(0, 255, 157, 0.18); color: var(--green); border-color: var(--green);
}
.suspect-counters { display: flex; align-items: center; gap: 0.4rem; font-size: 0.68rem; }
.s-count.cyan b { color: var(--cyan); }
.s-count.gold b { color: var(--gold); }
.timer-pill { background: rgba(255, 255, 255, 0.1); padding: 0.12rem 0.4rem; border-radius: 5px; font-weight: 800; }
.btn-mini-reset {
  background: rgba(0, 240, 255, 0.18); border: 1px solid var(--cyan); color: var(--cyan);
  border-radius: 5px; padding: 0.1rem 0.42rem; font-weight: 900; cursor: pointer;
}
.combat-ticker {
  height: 24px; background: rgba(3, 7, 15, 0.94);
  border-bottom: 1px solid rgba(0, 240, 255, 0.18);
  padding: 0 0.65rem; display: flex; align-items: center;
  font-size: 0.66rem; color: var(--cyan);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex-shrink: 0;
}

/* FIXED NON-COLLAPSING ARENA & COLLECTION GRIDS */
.arena-grid-wrapper, .collection-scroll-area, .social-scroll-area {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
  padding: 0.45rem;
}

.battle-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: max-content;
  align-content: start;
  gap: 0.42rem;
  padding-bottom: 0.5rem;
}

@media (min-width: 768px) {
  .battle-grid {
    grid-template-columns: repeat(6, 1fr);
    gap: 0.5rem;
  }
}

.collection-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: max-content;
  align-content: start;
  gap: 0.55rem;
  padding-bottom: 1rem;
}

@media (min-width: 768px) {
  .collection-grid {
    grid-template-columns: repeat(6, 1fr);
  }
}

.grid-holo-card {
  position: relative;
  width: 100%;
  height: 128px;
  border-radius: 9px;
  background: #0c162c;
  border: 1.5px solid rgba(0, 240, 255, 0.48);
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.65);
  transition: transform 0.16s ease, border-color 0.18s ease;
}

.collection-grid .grid-holo-card {
  height: 168px;
}

.grid-holo-card.matching-preview {
  border-color: var(--gold);
  box-shadow: 0 0 14px rgba(255, 204, 51, 0.75);
}

.grid-holo-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.grid-card-footer {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(0deg, rgba(2, 5, 12, 0.98) 60%, transparent 100%);
  padding: 0.75rem 0.25rem 0.22rem;
  text-align: center;
  z-index: 2;
}

.grid-card-name {
  font-size: 0.62rem;
  font-weight: 900;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.grid-card-sub {
  font-size: 0.5rem;
  color: var(--cyan);
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* BLAST DOOR SHUTTER FOR ELIMINATED SUSPECTS */
.grid-holo-card.eliminated {
  border-color: rgba(255, 42, 95, 0.45);
}
.grid-holo-card.eliminated img {
  filter: grayscale(100%) brightness(0.35);
}
.grid-holo-card.eliminated::after {
  content: "ELIMINATED";
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  background: repeating-linear-gradient(
    -45deg,
    rgba(12, 18, 32, 0.86),
    rgba(12, 18, 32, 0.86) 8px,
    rgba(255, 42, 95, 0.22) 8px,
    rgba(255, 42, 95, 0.22) 16px
  );
  color: var(--red);
  font-weight: 900;
  font-size: 0.64rem;
  letter-spacing: 0.1em;
  z-index: 4;
}

/* BOTTOM COMMAND DOCK */
.battle-command-dock {
  background: rgba(6, 12, 25, 0.98);
  border-top: 1.5px solid rgba(0, 240, 255, 0.4);
  padding: 0.4rem 0.5rem;
  display: grid;
  grid-template-columns: 130px 1fr;
  gap: 0.45rem;
  flex-shrink: 0;
}

.secret-dock-box { display: flex; flex-direction: column; gap: 0.3rem; }
.secret-mini-card {
  display: flex; align-items: center; gap: 0.35rem;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(0, 240, 255, 0.45);
  border-radius: 8px; padding: 0.22rem; cursor: pointer;
}
.secret-mini-card img {
  width: 36px; height: 44px; border-radius: 5px; object-fit: cover; flex-shrink: 0;
  background: #0d1a36;
}
.secret-mini-meta { overflow: hidden; line-height: 1.15; }
.secret-mini-meta small { display: block; font-size: 0.46rem; color: var(--gold); font-weight: 800; }
.secret-mini-meta strong { display: block; font-size: 0.62rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.secret-mini-meta span { font-size: 0.5rem; color: var(--cyan); }

.btn-ultimate {
  background: linear-gradient(135deg, #ffbe3d, #ff5500);
  border: 1px solid #ffe082; color: #050912;
  border-radius: 7px; padding: 0.3rem;
  font-weight: 900; font-size: 0.62rem; cursor: pointer;
  display: flex; flex-direction: column; align-items: center;
}
.btn-ultimate:disabled { opacity: 0.35; filter: grayscale(80%); }
.btn-ultimate small { font-size: 0.48rem; }

.scanner-dock-box { display: flex; flex-direction: column; justify-content: space-between; gap: 0.3rem; overflow: hidden; }
.cat-tabs { display: flex; gap: 0.22rem; overflow-x: auto; }
.cat-tab {
  flex: 1; background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--muted); padding: 0.24rem 0.3rem;
  border-radius: 6px; font-size: 0.56rem; font-weight: 800; cursor: pointer;
}
.cat-tab.active { background: rgba(0, 240, 255, 0.22); border-color: var(--cyan); color: #fff; }
.val-chips-row { display: flex; gap: 0.28rem; overflow-x: auto; padding-bottom: 2px; }
.trait-val-chip {
  background: #0c1730; border: 1px solid rgba(0, 240, 255, 0.32);
  color: var(--text); padding: 0.24rem 0.5rem; border-radius: 99px;
  font-size: 0.62rem; font-weight: 800; white-space: nowrap; cursor: pointer;
  display: flex; align-items: center; gap: 0.25rem;
}
.trait-val-chip.selected {
  background: linear-gradient(135deg, rgba(0, 240, 255, 0.35), rgba(0, 102, 255, 0.5));
  border-color: var(--cyan);
}
.chip-count {
  background: rgba(255, 255, 255, 0.16); padding: 0.03rem 0.28rem;
  border-radius: 99px; font-size: 0.52rem; color: var(--gold);
}
.action-buttons-row { display: grid; grid-template-columns: 1fr auto; gap: 0.35rem; }
.btn-action-scan {
  background: linear-gradient(135deg, #00d2ff, #0055ff);
  border: 1px solid var(--cyan); color: #fff;
  border-radius: 7px; padding: 0.4rem; font-weight: 900; font-size: 0.68rem; cursor: pointer;
}
.btn-action-accuse {
  background: rgba(255, 42, 95, 0.22); border: 1px solid var(--red);
  color: #ff8da6; border-radius: 7px; padding: 0.4rem 0.65rem;
  font-weight: 900; font-size: 0.68rem; cursor: pointer;
}
.btn-action-accuse.active { background: var(--red); color: #fff; box-shadow: 0 0 14px var(--red); }

/* SUBVIEWS & RANK CRESTS */
.subview-header { padding: 0.55rem 0.85rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); flex-shrink: 0; }
.subview-header h2 { font-size: 0.9rem; color: var(--cyan); }
.subview-header p { font-size: 0.68rem; color: var(--muted); }
.social-split { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; }
@media (max-width: 768px) { .social-split { grid-template-columns: 1fr; } }
.glass-panel {
  background: var(--bg-panel); border: 1px solid rgba(0, 240, 255, 0.25);
  border-radius: 12px; padding: 0.8rem; display: flex; flex-direction: column; gap: 0.5rem;
}
.glass-panel h3 { font-size: 0.82rem; color: var(--cyan); }
.sub-h4 { font-size: 0.7rem; color: var(--gold); margin-top: 0.25rem; }
.rank-crest-banner {
  background: linear-gradient(135deg, rgba(255, 204, 51, 0.16), rgba(0, 240, 255, 0.1));
  border: 1px solid rgba(255, 204, 51, 0.45);
  border-radius: 10px; padding: 0.6rem 0.8rem;
  display: flex; align-items: center; gap: 0.65rem;
}
.crest-shield {
  width: 42px; height: 42px; border-radius: 10px;
  background: rgba(255, 204, 51, 0.2); border: 1px solid var(--gold);
  display: grid; place-items: center; font-size: 1.3rem;
}
.xp-progress-track { width: 100%; height: 8px; background: rgba(255,255,255,0.08); border-radius: 99px; overflow: hidden; }
.xp-progress-fill { height: 100%; background: linear-gradient(90deg, var(--cyan), var(--gold)); }
.form-row { display: flex; gap: 0.4rem; }
.neon-input {
  flex: 1; background: #060c1a; border: 1px solid rgba(0, 240, 255, 0.35);
  color: #fff; padding: 0.42rem 0.55rem; border-radius: 7px; font-size: 0.74rem;
}
.btn-neon {
  padding: 0.42rem 0.75rem; border-radius: 7px; font-weight: 800; font-size: 0.7rem; cursor: pointer; border: 1px solid transparent;
}
.btn-neon.cyan { background: linear-gradient(135deg, #00d2ff, #0055ff); color: #fff; border-color: var(--cyan); }
.btn-neon.gold { background: linear-gradient(135deg, var(--gold), #e67e22); color: #050912; }
.btn-neon.red { background: rgba(255, 42, 95, 0.25); border-color: var(--red); color: #ff99b3; }
.scroll-list { display: flex; flex-direction: column; gap: 0.38rem; }
.list-item-row {
  background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px; padding: 0.48rem 0.65rem;
  display: flex; justify-content: space-between; align-items: center; font-size: 0.74rem;
}

/* BOTTOM NAVIGATION */
.bottom-nav {
  height: 52px; background: rgba(4, 8, 18, 0.98);
  border-top: 1px solid rgba(0, 240, 255, 0.25);
  display: grid; grid-template-columns: repeat(5, 1fr); flex-shrink: 0;
}
.nav-tab {
  background: none; border: none; color: var(--muted);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  gap: 0.08rem; cursor: pointer; font-weight: 800;
}
.nav-tab .nav-ico { font-size: 1rem; }
.nav-tab small { font-size: 0.54rem; letter-spacing: 0.04em; }
.nav-tab.active {
  color: var(--cyan);
  background: radial-gradient(circle at 50% 100%, rgba(0, 240, 255, 0.24), transparent 70%);
}

/* MODALS */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(2, 5, 12, 0.88);
  backdrop-filter: blur(10px); display: grid; place-items: center; z-index: 60; padding: 1rem;
}
.modal-overlay.hidden, .ultimate-cutin.hidden { display: none !important; }
.modal-card {
  background: #0b152b; border: 1.5px solid var(--cyan); border-radius: 16px;
  padding: 1.15rem; max-width: 360px; width: 100%; text-align: center;
  display: flex; flex-direction: column; align-items: center; gap: 0.7rem;
}
.radar-circle { width: 72px; height: 72px; border-radius: 50%; border: 2px solid var(--cyan); position: relative; overflow: hidden; }
.radar-beam { position: absolute; inset: 0; background: conic-gradient(from 0deg, transparent 60%, rgba(0, 240, 255, 0.75) 100%); animation: radarSpin 1.3s linear infinite; }
@keyframes radarSpin { to { transform: rotate(360deg); } }
.ultimate-cutin { position: fixed; inset: 0; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 90; pointer-events: none; }
.cutin-slash {
  width: 100%; height: 165px; background: linear-gradient(90deg, #000 0%, #10254c 30%, #00d2ff 100%);
  border-top: 3px solid var(--gold); border-bottom: 3px solid var(--gold);
  transform: skewY(-4deg); display: flex; align-items: center; justify-content: center; gap: 1rem;
}
.cutin-slash img { height: 145px; border-radius: 10px; border: 2px solid var(--gold); }
.cutin-text span { color: var(--gold); font-weight: 900; font-size: 0.72rem; letter-spacing: 0.16em; }
.cutin-text h2 { font-size: 1.35rem; font-weight: 900; color: #fff; }
.legal-footer-links { font-size: 0.68rem; color: var(--muted); margin-top: 0.5rem; }
.legal-footer-links a { color: var(--cyan); text-decoration: none; }
"""

# ============================================================================
# 5. JS/ROSTER.JS — 24 Operatives & Creature-Locked Prompts
# ============================================================================
ROSTER_JS = r"""
window.FACTION_ABILITIES = {
  Ironclad: {
    name: "AEGIS BASTION PROTOCOL",
    desc: "Interrogates enemy Armor plating immediately AND shields your telemetry readout for 1 turn."
  },
  Cybernetic: {
    name: "NEURAL OVERCLOCK",
    desc: "Dual-vector scan: reveals whether enemy Element is High-Voltage (Volt/Solar) without ending your turn."
  },
  Solaris: {
    name: "HELIOS ORBITAL SWEEP",
    desc: "Calls down an orbital laser strike that eliminates 4 confirmed non-target decoys on the matrix immediately."
  },
  Abyssal: {
    name: "VOID TEMPORAL JAMMER",
    desc: "Reveals whether enemy Biotype is Synthetic or Organic AND drains 8 seconds from their next turn clock."
  }
};

window.STUDIO_ROSTER = [
  { id: "u01", name: "Spiked Tortoise",   faction: "Ironclad",   species: "Reptilian",  armor: "Spiked Shell",    weapon: "Plasma Cannon", element: "Terra", prompt: "giant armored snapping tortoise kaiju monster, massive spiked obsidian shell with glowing orange lava cracks, twin shoulder plasma cannons, reptilian scales, no human, digital concept art" },
  { id: "u02", name: "Vortex Stalker",    faction: "Cybernetic", species: "Android",    armor: "Stealth Weave",   weapon: "Rail Rifle",    element: "Volt",  prompt: "sleek cybernetic stealth panther mecha, glowing cyan optic visor, carbon fiber stealth armor, electromagnetic rail sniper rifle, lightning aura, no human face, sci-fi concept art" },
  { id: "u03", name: "Pyre Seraph",       faction: "Solaris",    species: "Avian",      armor: "Aegis Plate",     weapon: "Solar Lance",   element: "Solar", prompt: "majestic six-winged golden phoenix valkyrie seraph creature, radiant solar fire wings, ornate celestial plate armor, blazing sun lance, epic fantasy card art" },
  { id: "u04", name: "Abyssal Leviathan", faction: "Abyssal",    species: "Cephalopod", armor: "Chitin Carapace", weapon: "Void Tendril",  element: "Void",  prompt: "colossal deep sea abyssal kraken leviathan monster, glowing purple bioluminescent tentacles, armored chitinous cephalopod mantle, dark void vortex, digital painting" },
  { id: "u05", name: "Chrome Basilisk",   faction: "Cybernetic", species: "Reptilian",  armor: "Aegis Plate",     weapon: "Plasma Cannon", element: "Volt",  prompt: "cybernetic chrome basilisk dragon serpent, reflective liquid metal scales, high voltage blue electric arcs, twin heavy plasma cannons, sci-fi monster card art" },
  { id: "u06", name: "Dread Carapace",    faction: "Abyssal",    species: "Arachnid",   armor: "Spiked Shell",    weapon: "Venom Blade",   element: "Void",  prompt: "giant armored shadow scorpion arachnid monster, jagged purple spiked carapace, dripping venom blades, glowing crimson compound eyes, dark abyssal cave, game art" },
  { id: "u07", name: "Helios Warden",     faction: "Solaris",    species: "Android",    armor: "Aegis Plate",     weapon: "Solar Lance",   element: "Solar", prompt: "towering golden mechanical paladin construct mecha, glowing solar reactor core in chest, ornate aegis shield plating, blazing spear of light, sci-fi fantasy art" },
  { id: "u08", name: "Rust Juggernaut",   faction: "Ironclad",   species: "Construct",  armor: "Spiked Shell",    weapon: "Siege Hammer",  element: "Terra", prompt: "hulking industrial ironclad juggernaut golem, heavy rusted steel spiked armor, molten furnace core in chest, colossal rocket siege hammer, earth shatter sparks" },
  { id: "u09", name: "Neon Mantis",       faction: "Cybernetic", species: "Arachnid",   armor: "Stealth Weave",   weapon: "Venom Blade",   element: "Volt",  prompt: "neon cybernetic praying mantis assassin creature, translucent holographic stealth scythe blades, glowing cyan exoskeleton, cyberpunk background, digital art" },
  { id: "u10", name: "Trench Kraken",     faction: "Abyssal",    species: "Cephalopod", armor: "Chitin Carapace", weapon: "Plasma Cannon", element: "Cryo",  prompt: "arctic abyssal kraken octopod monster, encrusted with glowing blue glacial ice armor, freezing cryo plasma cannon, deep ocean trench, creature illustration" },
  { id: "u11", name: "Dawn Valkyrie",     faction: "Solaris",    species: "Avian",      armor: "Stealth Weave",   weapon: "Rail Rifle",    element: "Solar", prompt: "celestial armored griffin hawk valkyrie, radiant golden feathers, sleek stealth weave armor, high-tech solar railgun, sunrise clouds background, card art" },
  { id: "u12", name: "Magma Golem",       faction: "Ironclad",   species: "Construct",  armor: "Aegis Plate",     weapon: "Siege Hammer",  element: "Solar", prompt: "colossal volcanic magma golem titan, body made of cracked black basalt rock and flowing lava rivers, glowing golden runes, burning siege hammer, fantasy art" },
  { id: "u13", name: "Glacier Wyrm",      faction: "Abyssal",    species: "Reptilian",  armor: "Chitin Carapace", weapon: "Void Tendril",  element: "Cryo",  prompt: "ancient frost wyrm ice dragon, translucent crystalline chitin scales, swirling blizzard aura, glowing cyan eyes, jagged ice spires background, digital painting" },
  { id: "u14", name: "Aether Hawk",       faction: "Solaris",    species: "Avian",      armor: "Chitin Carapace", weapon: "Rail Rifle",    element: "Volt",  prompt: "cybernetic storm hawk eagle raptor, gleaming silver chitinous wing blades, crackling blue lightning feathers, sniper railgun mount, thunderclouds, card art" },
  { id: "u15", name: "Cobalt Widow",      faction: "Cybernetic", species: "Arachnid",   armor: "Chitin Carapace", weapon: "Rail Rifle",    element: "Cryo",  prompt: "giant mechanical black widow spider mecha, glossy cobalt blue armor plating, eight articulated razor legs, cryo rail rifle mounted on thorax, glowing red eyes" },
  { id: "u16", name: "Bastion Drake",     faction: "Ironclad",   species: "Reptilian",  armor: "Aegis Plate",     weapon: "Siege Hammer",  element: "Terra", prompt: "heavily armored earth drake dragon, thick bronze fortress plate armor, glowing amber magma vents, massive spiked tail and siege claws, monster illustration" },
  { id: "u17", name: "Null Specter",      faction: "Abyssal",    species: "Android",    armor: "Stealth Weave",   weapon: "Void Tendril",  element: "Void",  prompt: "phantom void wraith mecha assassin, tattered dark energy cloak, glowing violet singularity core, shadowy energy tendrils, cosmic rift background, sci-fi art" },
  { id: "u18", name: "Volt Centurion",    faction: "Cybernetic", species: "Construct",  armor: "Aegis Plate",     weapon: "Solar Lance",   element: "Volt",  prompt: "towering cybernetic centurion mecha knight, polished titanium aegis armor, crackling blue plasma lance, glowing cyan crest visor, futuristic arena background" },
  { id: "u19", name: "Frost Talon",       faction: "Solaris",    species: "Avian",      armor: "Spiked Shell",    weapon: "Venom Blade",   element: "Cryo",  prompt: "armored frost owl raptor monster, razor sharp ice crystal feathers, spiked glacial shell armor, glowing cyan talons and ice blades, blizzard night sky" },
  { id: "u20", name: "Slag Octopod",      faction: "Ironclad",   species: "Cephalopod", armor: "Spiked Shell",    weapon: "Plasma Cannon", element: "Terra", prompt: "molten slag octopod lava kraken, heavy ironclad spiked shell mantle, tentacles made of liquid fire and obsidian, twin heavy plasma cannons, volcanic forge" },
  { id: "u21", name: "Prism Weaver",      faction: "Solaris",    species: "Arachnid",   armor: "Stealth Weave",   weapon: "Solar Lance",   element: "Solar", prompt: "crystalline prism weaver spider queen, iridescent golden glass arachnid armor, refracting rainbow solar laser beams, eight golden mechanical legs, sacred temple" },
  { id: "u22", name: "Cryo Automaton",    faction: "Cybernetic", species: "Construct",  armor: "Spiked Shell",    weapon: "Siege Hammer",  element: "Cryo",  prompt: "heavy cryo automaton siege robot, frost-covered spiked titanium armor, glowing sub-zero blue reactor, giant ice-crushing siege hammer, arctic storm" },
  { id: "u23", name: "Rift Nautilus",     faction: "Abyssal",    species: "Cephalopod", armor: "Aegis Plate",     weapon: "Void Tendril",  element: "Void",  prompt: "cosmic rift nautilus cephalopod monster, ancient spiral armored shell with glowing purple runes, void gravity tendrils, floating in deep space nebula" },
  { id: "u24", name: "Titan Anvil",       faction: "Ironclad",   species: "Android",    armor: "Chitin Carapace", weapon: "Plasma Cannon", element: "Terra", prompt: "colossal titan anvil war mecha, ultra-heavy gunmetal chitin carapace, glowing molten orange reactor vents, dual shoulder siege plasma cannons, sci-fi art" }
];
"""

# ============================================================================
# 6. JS/ARTENGINE.JS — Pre-Baked Local Art + High-Density Volumetric Renderer
# ============================================================================
ART_ENGINE_JS = r"""
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
"""

# ============================================================================
# 7. JS/VFXENGINE.JS & JS/AUDIO.JS & JS/NETWORK.JS
# ============================================================================
VFX_ENGINE_JS = r"""
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
"""

AUDIO_JS = r"""
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
"""

NETWORK_JS = r"""
class StudioNetworkBroker {
  constructor(callsign) {
    this.callsign = callsign;
  }
  setCallsign(name) {
    this.callsign = String(name || "Commander").replace(/[^a-zA-Z0-9_-]/g, "").slice(0, 16) || "Commander";
    return this.callsign;
  }
}
window.StudioNetworkBroker = StudioNetworkBroker;
"""

# ============================================================================
# 8. JS/GAMECONTROLLER.JS — Instant Arena Boot + Live Image Upgrade Listener
# ============================================================================
GAME_CONTROLLER_JS = r"""
class GameController {
  constructor() {
    this.roster = window.STUDIO_ROSTER || [];
    this.abilities = window.FACTION_ABILITIES || {};
    this.art = window.StudioArt;
    this.vfx = window.StudioVFX;
    this.audio = window.StudioAudio;

    this.profile = this.loadProfile();
    this.showcaseIdx = 0;

    // Live Battle State — Always Initialized so Arena Tab is NEVER Blank!
    this.inMatch = true;
    this.isMyTurn = true;
    this.accuseMode = false;
    this.abilityReady = true;
    this.selectedCat = "faction";
    this.selectedVal = "Ironclad";
    this.mySecret = this.roster[0];
    this.oppSecret = this.roster[3];
    this.oppName = "Valkyrie_IX";
    this.oppElo = 1240;
    this.eliminated = new Set();
    this.oppRemaining = 24;
    this.turnClock = 30;
    this.turnInterval = null;
    this.queueInterval = null;

    // Bake & upgrade art dynamically as high-res illustrations finish loading
    this.art.bakeAll(this.roster, (unitId, newUrl) => {
      document.querySelectorAll(`img[data-unit-img="${unitId}"]`).forEach((img) => {
        img.src = newUrl;
      });
      if (this.roster[this.showcaseIdx] && this.roster[this.showcaseIdx].id === unitId) {
        document.getElementById("showcase-art").src = newUrl;
      }
      if (this.mySecret && this.mySecret.id === unitId) {
        document.getElementById("my-secret-img").src = newUrl;
      }
    });

    this.vfx.init();
    this.net = new window.StudioNetworkBroker(this.profile.callsign);

    this.bindUI();
    this.updateShowcaseCard(0);
    // Initialize Arena Match on Boot so tapping ARENA tab at 00:03 is 100% populated
    this.setupMatchBoard("Valkyrie_IX", 1240, false);
    this.renderCollection();
    this.renderSocialAndRanked();
    this.renderShopAndPass();
    this.renderTopHUD();
  }

  loadProfile() {
    try {
      const raw = localStorage.getItem("tt_studio_v10");
      if (raw) return JSON.parse(raw);
    } catch (e) {}
    return {
      callsign: "Commander_" + Math.floor(100 + Math.random() * 899),
      elo: 1200,
      wins: 0,
      losses: 0,
      credits: 1500,
      gems: 200,
      xp: 400,
      foilUnlocked: false,
      friends: ["Valkyrie_IX", "Sovereign_Zero", "NexusPrime"],
      history: []
    };
  }

  saveProfile() {
    localStorage.setItem("tt_studio_v10", JSON.stringify(this.profile));
    this.renderTopHUD();
  }

  switchView(viewId) {
    this.audio.playClick();
    document.querySelectorAll(".screen-view").forEach((v) => v.classList.remove("active"));
    const target = document.getElementById(viewId);
    if (target) target.classList.add("active");

    document.querySelectorAll(".nav-tab").forEach((t) => {
      t.classList.toggle("active", t.getAttribute("data-view") === viewId);
    });

    if (viewId === "view-battle") {
      this.highlightMatchingCards();
    }
  }

  bindUI() {
    document.querySelectorAll(".nav-tab").forEach((btn) => {
      btn.onclick = () => this.switchView(btn.getAttribute("data-view"));
    });

    document.getElementById("lobby-showcase-card").onclick = () => {
      this.audio.playFlip();
      this.showcaseIdx = (this.showcaseIdx + 1) % this.roster.length;
      this.updateShowcaseCard(this.showcaseIdx);
    };

    document.getElementById("btn-play-ranked").onclick = () => this.openMatchmakingQueue();
    document.getElementById("btn-quick-friend").onclick = () => this.switchView("view-social");
    document.getElementById("btn-quick-inspect").onclick = () => this.switchView("view-collection");
    document.getElementById("btn-cancel-queue").onclick = () => this.cancelQueue();
    document.getElementById("btn-new-match").onclick = () => this.openMatchmakingQueue();

    document.getElementById("btn-audio-toggle").onclick = (e) => {
      e.currentTarget.textContent = this.audio.toggleMute() ? "🔇" : "🔊";
    };

    document.querySelectorAll(".cat-tab").forEach((tab) => {
      tab.onclick = () => {
        this.audio.playClick();
        this.selectedCat = tab.getAttribute("data-cat");
        document.querySelectorAll(".cat-tab").forEach((t) => t.classList.remove("active"));
        tab.classList.add("active");
        const vals = [...new Set(this.roster.map((u) => u[this.selectedCat]))];
        this.selectedVal = vals[0];
        this.renderScannerConsole();
        this.highlightMatchingCards();
      };
    });

    document.getElementById("btn-fire-scan").onclick = () => this.executeTraitScan();
    document.getElementById("btn-fire-ultimate").onclick = () => this.executeFactionUltimate();
    document.getElementById("btn-toggle-accuse").onclick = () => {
      this.accuseMode = !this.accuseMode;
      const b = document.getElementById("btn-toggle-accuse");
      b.classList.toggle("active", this.accuseMode);
      b.textContent = this.accuseMode ? "🎯 TAP SUSPECT" : "🎯 ACCUSE";
      this.setTicker(this.accuseMode ? "🎯 ACCUSATION ARMED: Tap any suspect card on the board to accuse!" : "📡 Tap a trait chip below to preview matching suspects.");
    };

    document.getElementById("my-secret-mini").onclick = () => this.inspectOperative(this.mySecret);
    document.getElementById("btn-close-inspect").onclick = () => {
      document.getElementById("modal-inspect").classList.add("hidden");
    };

    document.getElementById("btn-save-callsign").onclick = () => {
      const val = document.getElementById("input-callsign").value.trim();
      if (val) {
        this.profile.callsign = this.net.setCallsign(val);
        this.saveProfile();
        this.renderSocialAndRanked();
      }
    };

    document.getElementById("btn-add-friend").onclick = () => {
      const f = document.getElementById("input-friend").value.trim();
      if (f && !this.profile.friends.includes(f)) {
        this.profile.friends.push(f);
        document.getElementById("input-friend").value = "";
        this.saveProfile();
        this.renderSocialAndRanked();
      }
    };

    document.getElementById("btn-play-again").onclick = () => {
      document.getElementById("modal-result").classList.add("hidden");
      this.openMatchmakingQueue();
    };
    document.getElementById("btn-result-lobby").onclick = () => {
      document.getElementById("modal-result").classList.add("hidden");
      this.switchView("view-lobby");
    };
  }

  updateShowcaseCard(idx) {
    const u = this.roster[idx] || this.roster[0];
    document.querySelector(".showcase-tag").textContent = `FEATURED OPERATIVE // TAP CARD TO CYCLE (${idx + 1}/24)`;
    document.getElementById("showcase-art").src = this.art.getArt(u.id);
    document.getElementById("showcase-faction").textContent = u.faction;
    document.getElementById("showcase-element").textContent = u.element;
    document.getElementById("showcase-name").textContent = u.name;
    document.getElementById("showcase-traits").textContent = `${u.species} • ${u.armor} • ${u.weapon}`;
    document.getElementById("lobby-showcase-card").classList.toggle("foil-active", this.profile.foilUnlocked);
  }

  openMatchmakingQueue() {
    this.audio.playScan();
    const modal = document.getElementById("modal-queue");
    modal.classList.remove("hidden");
    let elapsed = 0;
    document.getElementById("queue-clock").textContent = "00:00";
    clearInterval(this.queueInterval);
    this.queueInterval = setInterval(() => {
      elapsed++;
      document.getElementById("queue-clock").textContent = `00:0${elapsed}`;
      if (elapsed >= 2) {
        clearInterval(this.queueInterval);
        modal.classList.add("hidden");
        const rivals = ["Valkyrie_IX", "Sovereign_Zero", "NexusPrime", "Kestrel_7", "Aegis_Vanguard"];
        const rName = rivals[Math.floor(Math.random() * rivals.length)];
        const rElo = this.profile.elo + Math.floor(Math.random() * 80 - 40);
        this.setupMatchBoard(rName, rElo, true);
      }
    }, 750);
  }

  cancelQueue() {
    clearInterval(this.queueInterval);
    document.getElementById("modal-queue").classList.add("hidden");
  }

  setupMatchBoard(oppName, oppElo, switchNow = true) {
    this.inMatch = true;
    this.oppName = oppName;
    this.oppElo = Math.max(900, oppElo);
    this.eliminated.clear();
    this.oppRemaining = 24;
    this.abilityReady = true;
    this.accuseMode = false;

    this.mySecret = this.roster[Math.floor(Math.random() * this.roster.length)];
    this.oppSecret = this.roster[Math.floor(Math.random() * this.roster.length)];

    document.getElementById("battle-opp-name").textContent = this.oppName;
    document.getElementById("battle-opp-elo").textContent = `(${this.oppElo})`;
    document.getElementById("my-secret-img").src = this.art.getArt(this.mySecret.id);
    document.getElementById("my-secret-name").textContent = this.mySecret.name;
    document.getElementById("my-secret-traits").textContent = `${this.mySecret.faction} • ${this.mySecret.element}`;
    document.getElementById("ult-name-label").textContent = this.mySecret.faction.toUpperCase();

    this.renderBattleGrid();
    this.renderScannerConsole();
    this.updateBattleCounters();
    this.highlightMatchingCards();
    this.setTicker(`⚔️ Assigned ${this.mySecret.name}. Tap any trait chip below to interrogate ${this.oppName}'s matrix!`);
    this.setTurn(true);

    if (switchNow) {
      this.switchView("view-battle");
    }
  }

  setTurn(mine) {
    this.isMyTurn = mine;
    this.turnClock = 30;
    const pill = document.getElementById("turn-pill");
    pill.textContent = mine ? "YOUR TURN" : `${this.oppName.toUpperCase()}'S TURN`;
    pill.classList.toggle("your-turn", mine);

    document.getElementById("btn-fire-scan").disabled = !mine;
    document.getElementById("btn-toggle-accuse").disabled = !mine;
    document.getElementById("btn-fire-ultimate").disabled = !(mine && this.abilityReady);

    clearInterval(this.turnInterval);
    this.turnInterval = setInterval(() => {
      this.turnClock = Math.max(0, this.turnClock - 1);
      document.getElementById("battle-timer").textContent = `${this.turnClock}s`;
    }, 1000);

    if (!mine) {
      setTimeout(() => this.runSmartOpponentTurn(), 1200);
    }
  }

  renderScannerConsole() {
    const vals = [...new Set(this.roster.map((u) => u[this.selectedCat]))];
    if (!vals.includes(this.selectedVal)) this.selectedVal = vals[0];

    const row = document.getElementById("scanner-val-chips");
    row.innerHTML = vals
      .map((v) => {
        const activeMatches = this.roster.filter(
          (u) => !this.eliminated.has(u.id) && u[this.selectedCat] === v
        ).length;
        const sel = v === this.selectedVal ? "selected" : "";
        return `
          <button class="trait-val-chip ${sel}" data-val="${v}">
            <span>${v}</span>
            <span class="chip-count">${activeMatches}</span>
          </button>
        `;
      })
      .join("");

    row.querySelectorAll(".trait-val-chip").forEach((chip) => {
      chip.onclick = () => {
        this.audio.playClick();
        this.selectedVal = chip.getAttribute("data-val");
        this.renderScannerConsole();
        this.highlightMatchingCards();
      };
    });

    document.getElementById("selected-trait-preview").textContent = this.selectedVal.toUpperCase();
  }

  highlightMatchingCards() {
    document.querySelectorAll("#battle-grid .grid-holo-card").forEach((card) => {
      const uid = card.getAttribute("data-id");
      const u = this.roster.find((x) => x.id === uid);
      const match = u && !this.eliminated.has(uid) && u[this.selectedCat] === this.selectedVal;
      card.classList.toggle("matching-preview", Boolean(match));
    });
  }

  executeTraitScan() {
    if (!this.isMyTurn || !this.inMatch) return;
    this.audio.playScan();
    const cat = this.selectedCat;
    const val = this.selectedVal;
    const hit = this.oppSecret[cat] === val;

    const newlyEliminated = [];
    this.roster.forEach((u) => {
      const has = u[cat] === val;
      const shouldElim = hit ? !has : has;
      if (shouldElim && !this.eliminated.has(u.id)) {
        this.eliminated.add(u.id);
        newlyEliminated.push(u.id);
      }
    });

    this.animateEliminations(newlyEliminated, hit ? "#00ff9d" : "#00f0ff");
    this.setTicker(
      `📡 SCAN [${cat.toUpperCase()}: ${val}] -> ${hit ? "CONFIRMED MATCH!" : "NEGATIVE MISS"} (${newlyEliminated.length} suspects eliminated)`
    );
    this.updateBattleCounters();
    this.renderScannerConsole();
    this.setTurn(false);
  }

  executeFactionUltimate() {
    if (!this.isMyTurn || !this.abilityReady || !this.inMatch) return;
    this.abilityReady = false;
    document.getElementById("btn-fire-ultimate").disabled = true;
    document.getElementById("ult-name-label").textContent = "USED";

    const f = this.mySecret.faction;
    const ab = this.abilities[f];
    this.audio.playUltimate();
    this.vfx.triggerUltimateCutIn(this.mySecret, ab.name);

    const newlyEliminated = [];
    if (f === "Ironclad") {
      const arm = this.mySecret.armor;
      const hit = this.oppSecret.armor === arm;
      this.roster.forEach((u) => {
        if ((u.armor === arm) !== hit && !this.eliminated.has(u.id)) {
          this.eliminated.add(u.id);
          newlyEliminated.push(u.id);
        }
      });
      this.setTicker(`⚡ AEGIS BASTION: Armor [${arm}] ${hit ? "CONFIRMED" : "NEGATIVE"}! (${newlyEliminated.length} eliminated)`);
    } else if (f === "Cybernetic") {
      const hv = ["Volt", "Solar"].includes(this.oppSecret.element);
      this.roster.forEach((u) => {
        if (["Volt", "Solar"].includes(u.element) !== hv && !this.eliminated.has(u.id)) {
          this.eliminated.add(u.id);
          newlyEliminated.push(u.id);
        }
      });
      this.setTicker(`⚡ NEURAL OVERCLOCK: Enemy Element is ${hv ? "HIGH-VOLTAGE" : "LOW-THERMAL"}! (${newlyEliminated.length} eliminated)`);
    } else if (f === "Solaris") {
      const decoys = this.roster.filter((u) => u.id !== this.oppSecret.id && !this.eliminated.has(u.id)).slice(0, 4);
      decoys.forEach((d) => {
        this.eliminated.add(d.id);
        newlyEliminated.push(d.id);
      });
      this.setTicker("⚡ HELIOS ORBITAL SWEEP: 4 confirmed non-target decoys obliterated!");
    } else {
      const synth = ["Android", "Construct"].includes(this.oppSecret.species);
      this.roster.forEach((u) => {
        if (["Android", "Construct"].includes(u.species) !== synth && !this.eliminated.has(u.id)) {
          this.eliminated.add(u.id);
          newlyEliminated.push(u.id);
        }
      });
      this.setTicker(`⚡ VOID JAMMER: Enemy Biotype is ${synth ? "SYNTHETIC" : "ORGANIC"}! (${newlyEliminated.length} eliminated)`);
    }

    setTimeout(() => {
      this.animateEliminations(newlyEliminated, "#ffcc33");
      this.updateBattleCounters();
      this.renderScannerConsole();
    }, 450);
  }

  animateEliminations(ids, beamColor) {
    ids.forEach((id) => {
      const cardEl = document.querySelector(`#battle-grid .grid-holo-card[data-id="${id}"]`);
      if (cardEl) {
        this.vfx.spawnEliminationBurst(cardEl.getBoundingClientRect(), beamColor);
        cardEl.classList.add("eliminated");
        cardEl.classList.remove("matching-preview");
      }
    });
  }

  runSmartOpponentTurn() {
    if (!this.inMatch) return;
    const cats = ["faction", "species", "armor", "weapon", "element"];
    const cat = cats[Math.floor(Math.random() * cats.length)];
    const val = this.mySecret[cat];
    const hit = Math.random() > 0.45;
    const cut = Math.max(1, Math.floor(this.oppRemaining * 0.28));
    this.oppRemaining = Math.max(2, this.oppRemaining - cut);
    this.updateBattleCounters();
    this.setTicker(`⚠️ ${this.oppName} scanned [${cat.toUpperCase()}: ${hit ? val : "Aegis Plate"}] — ${this.oppRemaining} suspects left.`);
    this.setTurn(true);
  }

  renderBattleGrid() {
    const grid = document.getElementById("battle-grid");
    grid.innerHTML = this.roster
      .map((u) => {
        const elim = this.eliminated.has(u.id) ? "eliminated" : "";
        return `
          <div class="grid-holo-card ${elim}" data-id="${u.id}">
            <img data-unit-img="${u.id}" src="${this.art.getArt(u.id)}" alt="${u.name}" />
            <div class="holo-glare"></div>
            <div class="card-top-badges">
              <span class="c-badge faction">${u.faction.slice(0, 4)}</span>
              <span class="c-badge element">${u.element}</span>
            </div>
            <div class="grid-card-footer">
              <div class="grid-card-name">${u.name}</div>
              <div class="grid-card-sub">${u.species} • ${u.armor}</div>
            </div>
          </div>
        `;
      })
      .join("");

    grid.querySelectorAll(".grid-holo-card").forEach((card) => {
      const uid = card.getAttribute("data-id");
      const u = this.roster.find((x) => x.id === uid);
      card.onclick = () => {
        if (!u) return;
        if (this.accuseMode && this.isMyTurn && this.inMatch) {
          const won = u.id === this.oppSecret.id;
          this.concludeMatch(won, `You locked final accusation on ${u.name}. ${this.oppName}'s classified operative was ${this.oppSecret.name}.`);
          return;
        }
        this.audio.playFlip();
        if (this.eliminated.has(u.id)) {
          this.eliminated.delete(u.id);
          card.classList.remove("eliminated");
        } else {
          this.eliminated.add(u.id);
          card.classList.add("eliminated");
          this.vfx.spawnEliminationBurst(card.getBoundingClientRect(), "#ff2a5f");
        }
        this.updateBattleCounters();
        this.renderScannerConsole();
      };
    });
  }

  concludeMatch(won, details) {
    clearInterval(this.turnInterval);
    const expected = 1 / (1 + Math.pow(10, (this.oppElo - this.profile.elo) / 400));
    const delta = Math.round(32 * ((won ? 1 : 0) - expected));
    this.profile.elo = Math.max(800, this.profile.elo + delta);

    if (won) {
      this.profile.wins++;
      this.profile.credits += 200;
      this.profile.xp += 150;
      this.audio.playVictory();
    } else {
      this.profile.losses++;
      this.profile.credits += 65;
      this.profile.xp += 55;
      this.audio.playDefeat();
    }

    this.profile.history.unshift({
      result: won ? "VICTORY" : "DEFEAT",
      opp: this.oppName,
      faction: this.mySecret.faction,
      delta: (delta >= 0 ? "+" : "") + delta
    });
    this.saveProfile();
    this.renderSocialAndRanked();
    this.renderShopAndPass();

    document.getElementById("result-badge").textContent = won ? "🏆 VICTORY" : "💀 DEFEAT";
    document.getElementById("result-heading").textContent = won ? "TARGET NEUTRALIZED" : "DEDUCTION COMPROMISED";
    document.getElementById("result-details").textContent = details;
    document.getElementById("result-elo-pill").textContent = `${delta >= 0 ? "+" : ""}${delta} MMR (${this.profile.elo} ELO)`;
    document.getElementById("modal-result").classList.remove("hidden");
  }

  inspectOperative(u) {
    const mount = document.getElementById("inspect-card-mount");
    mount.innerHTML = `
      <div class="holo-card-inner">
        <img data-unit-img="${u.id}" src="${this.art.getArt(u.id)}" alt="${u.name}" />
        <div class="holo-glare"></div>
        <div class="card-top-badges">
          <span class="c-badge faction">${u.faction}</span>
          <span class="c-badge element">${u.element}</span>
        </div>
        <div class="card-bottom-plate">
          <h2>${u.name}</h2>
          <div class="card-trait-line">${u.species} • ${u.armor} • ${u.weapon}</div>
        </div>
      </div>
    `;
    const ab = this.abilities[u.faction];
    document.getElementById("inspect-ult-title").textContent = `⚡ ${u.faction.toUpperCase()}: ${ab.name}`;
    document.getElementById("inspect-ult-desc").textContent = ab.desc;
    document.getElementById("modal-inspect").classList.remove("hidden");
  }

  renderCollection() {
    const box = document.getElementById("collection-grid");
    box.innerHTML = this.roster
      .map((u) => `
        <div class="grid-holo-card" data-inspect="${u.id}">
          <img data-unit-img="${u.id}" src="${this.art.getArt(u.id)}" alt="${u.name}" />
          <div class="holo-glare"></div>
          <div class="card-top-badges">
            <span class="c-badge faction">${u.faction.slice(0, 4)}</span>
            <span class="c-badge element">${u.element}</span>
          </div>
          <div class="grid-card-footer">
            <div class="grid-card-name">${u.name}</div>
            <div class="grid-card-sub">${u.species} • ${u.weapon}</div>
          </div>
        </div>
      `)
      .join("");

    box.querySelectorAll("[data-inspect]").forEach((el) => {
      el.onclick = () => {
        const u = this.roster.find((x) => x.id === el.getAttribute("data-inspect"));
        if (u) this.inspectOperative(u);
      };
    });
  }

  renderSocialAndRanked() {
    document.getElementById("input-callsign").value = this.profile.callsign;
    const fBox = document.getElementById("friends-list");
    fBox.innerHTML = this.profile.friends
      .map((f) => `
        <div class="list-item-row">
          <span>● <strong>${f}</strong> <small style="color:#00ff9d;">ONLINE</small></span>
          <button class="btn-neon cyan" data-duel="${f}">⚔️ DUEL</button>
        </div>
      `)
      .join("");

    fBox.querySelectorAll("[data-duel]").forEach((b) => {
      b.onclick = () => this.setupMatchBoard(b.getAttribute("data-duel"), this.profile.elo + 20, true);
    });

    document.getElementById("ranked-summary-bar").textContent = `${this.getTier(this.profile.elo)} — ${this.profile.elo} MMR`;
    document.getElementById("ranked-winloss-sub").textContent = `${this.profile.wins}W - ${this.profile.losses}L • Season 01 Active`;

    const ladder = [
      { n: "Sovereign_Zero", e: 1680 },
      { n: "Valkyrie_IX", e: 1540 },
      { n: "Kestrel_7", e: 1390 },
      { n: `${this.profile.callsign} (YOU)`, e: this.profile.elo },
      { n: "NexusPrime", e: 1160 }
    ].sort((a, b) => b.e - a.e);

    document.getElementById("leaderboard-list").innerHTML = ladder
      .map((r, i) => `
        <div class="list-item-row">
          <span><strong>#${i + 1} ${r.n}</strong></span>
          <span>${this.getTier(r.e)} (${r.e})</span>
        </div>
      `)
      .join("");

    const hBox = document.getElementById("history-list");
    hBox.innerHTML = (this.profile.history || []).slice(0, 6)
      .map((h) => `
        <div class="list-item-row">
          <strong style="color:${h.result === "VICTORY" ? "#00ff9d" : "#ff2a5f"}">${h.result} vs ${h.opp}</strong>
          <span>${h.faction} (${h.delta} MMR)</span>
        </div>
      `)
      .join("") || `<div class="list-item-row">Complete a match in the Arena to log telemetry.</div>`;
  }

  renderShopAndPass() {
    document.getElementById("ui-pass-xp").textContent = String(this.profile.xp);
    const pct = Math.min(100, Math.round((this.profile.xp / 1200) * 100));
    document.getElementById("xp-progress-fill").style.width = `${pct}%`;

    const tiers = [
      { t: 1, xp: 100, ico: "◈", label: "+300 Tactical Credits" },
      { t: 2, xp: 350, ico: "❖", label: "+100 Core Gems" },
      { t: 3, xp: 700, ico: "✨", label: "Prismatic Holographic Foil Frame" },
      { t: 4, xp: 1200, ico: "👑", label: "Apex Sovereign Title & +800 Credits" }
    ];
    document.getElementById("pass-tiers-container").innerHTML = tiers
      .map((x) => `
        <div class="list-item-row">
          <div><strong>${x.ico} TIER 0${x.t} (${x.xp} XP)</strong><div style="font-size:0.68rem;color:#8ea6cc;">${x.label}</div></div>
          <span class="tier-pill">${this.profile.xp >= x.xp ? "UNLOCKED" : "LOCKED"}</span>
        </div>
      `)
      .join("");

    document.getElementById("armory-items-container").innerHTML = `
      <div class="list-item-row">
        <div>
          <strong>✨ Prismatic Gold Foil Deck Upgrade</strong>
          <div style="font-size:0.68rem;color:#8ea6cc;">Equips golden holographic borders across all 24 operatives.</div>
        </div>
        <button id="btn-unlock-foil" class="btn-neon gold">
          ${this.profile.foilUnlocked ? "✓ EQUIPPED" : "500 ◈"}
        </button>
      </div>
    `;

    document.getElementById("btn-unlock-foil").onclick = () => {
      if (!this.profile.foilUnlocked && this.profile.credits >= 500) {
        this.profile.credits -= 500;
        this.profile.foilUnlocked = true;
        this.saveProfile();
        this.updateShowcaseCard(this.showcaseIdx);
        this.renderShopAndPass();
        this.audio.playVictory();
      }
    };
  }

  updateBattleCounters() {
    document.getElementById("you-rem").textContent = String(this.roster.length - this.eliminated.size);
    document.getElementById("opp-rem").textContent = String(this.oppRemaining);
  }

  getTier(elo) {
    if (elo >= 1600) return "APEX SOVEREIGN";
    if (elo >= 1400) return "DIAMOND I";
    if (elo >= 1150) return "GOLD I";
    return "SILVER I";
  }

  renderTopHUD() {
    document.getElementById("ui-callsign").textContent = this.profile.callsign;
    document.getElementById("ui-elo").textContent = `${this.profile.elo} MMR`;
    document.getElementById("ui-rank-badge").textContent = this.getTier(this.profile.elo);
    document.getElementById("ui-credits").textContent = this.profile.credits.toLocaleString();
    document.getElementById("ui-gems").textContent = this.profile.gems.toLocaleString();
  }

  setTicker(msg) {
    document.getElementById("combat-ticker").innerHTML = `<span>${msg}</span>`;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  window.StudioApp = new GameController();
});
"""

# ============================================================================
# 9. GITHUB ACTIONS WORKFLOW — BUNDLES ASSETS/ART INTO NATIVE ANDROID APK
# ============================================================================
WORKFLOW_YML = r"""name: Build Native Android APK & Release

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build-android-apk:
    name: Compile Signed Android APK via Native Android SDK
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Compile & Sign Native Android APK (aapt + javac + d8 + apksigner)
        run: |
          set -e
          BUILD_TOOLS=$(ls -d "$ANDROID_HOME/build-tools/"* | sort -V | tail -n 1)
          PLATFORM_JAR=$(ls "$ANDROID_HOME/platforms/"*/android.jar | sort -V | tail -n 1)

          mkdir -p build/obj build/dex build/android assets/www res/values
          cp index.html assets/www/
          cp -r css js assets/www/
          if [ -d "assets/art" ]; then
            mkdir -p assets/www/assets
            cp -r assets/art assets/www/assets/
          fi

          cat << 'RES_EOF' > res/values/strings.xml
          <?xml version="1.0" encoding="utf-8"?>
          <resources>
              <string name="app_name">Trait Takedown</string>
          </resources>
          RES_EOF

          javac --release 8 -classpath "$PLATFORM_JAR" -d build/obj android_src/com/traittakedown/studio/MainActivity.java
          "$BUILD_TOOLS/d8" --lib "$PLATFORM_JAR" --output build/dex build/obj/com/traittakedown/studio/*.class
          "$BUILD_TOOLS/aapt" package -f -M AndroidManifest.xml -S res -A assets -I "$PLATFORM_JAR" -F build/unaligned.apk

          cd build/dex
          zip -q ../unaligned.apk classes.dex
          cd "$GITHUB_WORKSPACE"

          "$BUILD_TOOLS/zipalign" -f 4 build/unaligned.apk build/android/TraitTakedown-Android-Native.apk

          mkdir -p "$HOME/.android"
          rm -f "$HOME/.android/debug.keystore"
          keytool -keyalg RSA -genkeypair -alias androiddebugkey -keypass android -keystore "$HOME/.android/debug.keystore" -storepass android -dname "CN=Trait Takedown Studio,O=TraitTakedown,C=US" -validity 9999 -deststoretype pkcs12

          "$BUILD_TOOLS/apksigner" sign --ks "$HOME/.android/debug.keystore" --ks-key-alias androiddebugkey --ks-pass pass:android --key-pass pass:android build/android/TraitTakedown-Android-Native.apk
          ls -lh build/android/TraitTakedown-Android-Native.apk

      - name: Publish Native APK to GitHub Releases
        uses: softprops/action-gh-release@v2
        with:
          tag_name: v10.0.${{ github.run_number }}
          name: "Trait Takedown Studio Release v10.0.${{ github.run_number }}"
          body: "Standalone Signed Native Android APK (`com.traittakedown.studio`). Tap **TraitTakedown-Android-Native.apk** below to download and install."
          files: build/android/TraitTakedown-Android-Native.apk
"""

def build_all():
    root = get_project_dir()
    clean_project_directory(root)
    write_file(root, "AndroidManifest.xml", ANDROID_MANIFEST_XML)
    write_file(root, "android_src/com/traittakedown/studio/MainActivity.java", MAIN_ACTIVITY_JAVA)
    write_file(root, "index.html", INDEX_HTML)
    write_file(root, "css/studio.css", STUDIO_CSS)
    write_file(root, "js/roster.js", ROSTER_JS)
    write_file(root, "js/artEngine.js", ART_ENGINE_JS)
    write_file(root, "js/vfxEngine.js", VFX_ENGINE_JS)
    write_file(root, "js/audio.js", AUDIO_JS)
    write_file(root, "js/network.js", NETWORK_JS)
    write_file(root, "js/gameController.js", GAME_CONTROLLER_JS)
    write_file(root, ".github/workflows/native_release.yml", WORKFLOW_YML)
    download_prebaked_art(root)
    print("\n[+] Trait Takedown v10.0 complete.")

if __name__ == "__main__":
    build_all()
