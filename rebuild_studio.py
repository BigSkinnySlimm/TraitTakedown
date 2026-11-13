#!/usr/bin/env python3
"""
Trait Takedown v9.0 — Studio Fullscreen Tactical Arena, Bespoke Character Art Engine,
Real-Time Particle/Laser VFX, Symphonic WebAudio Synth, PeerJS Matchmaking & Native Android APK
"""

import shutil
from pathlib import Path

def get_project_dir() -> Path:
    termux_docs = Path.home() / "storage" / "shared" / "Documents" / "TraitTakedown"
    if termux_docs.parent.exists():
        termux_docs.mkdir(parents=True, exist_ok=True)
        return termux_docs
    return Path.cwd()

def is_protected(path: Path) -> bool:
    name = path.name.lower()
    if name in {".git", ".gitignore", "cname", "license", "rebuild_studio.py"}:
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
    print(f"[+] Generated {rel_path} ({len(content):,} bytes)")

# ============================================================================
# 1. NATIVE ANDROID MANIFEST & FULLSCREEN HARDWARE-ACCELERATED ACTIVITY
# ============================================================================
ANDROID_MANIFEST_XML = r"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.traittakedown.studio"
    android:versionCode="90"
    android:versionName="9.0.0">

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
# 2. INDEX.HTML — Zero-Scroll Studio App Shell (Lobby + Arena + Modals + VFX)
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
  <!-- Fullscreen Interactive VFX & Particle Shader Canvas -->
  <canvas id="vfx-canvas"></canvas>

  <!-- Ultimate Cut-In Cinematic Overlay -->
  <div id="ultimate-cutin" class="ultimate-cutin hidden">
    <div class="cutin-slash">
      <img id="cutin-img" src="" alt="Ultimate Operative" />
      <div class="cutin-text">
        <span id="cutin-faction">SOLARIS ULTIMATE</span>
        <h2 id="cutin-title">HELIOS ORBITAL SWEEP</h2>
      </div>
    </div>
  </div>

  <!-- Incoming Friend Challenge Toast -->
  <div id="challenge-toast" class="challenge-toast hidden">
    <div>
      <strong>⚔️ LIVE DUEL CHALLENGE</strong>
      <p id="challenge-toast-text">Challenger wants a Ranked Duel!</p>
    </div>
    <div class="toast-btns">
      <button id="btn-accept-challenge" class="btn-neon cyan">ACCEPT</button>
      <button id="btn-decline-challenge" class="btn-neon red">DECLINE</button>
    </div>
  </div>

  <div id="app-viewport">
    <!-- TOP PERSISTENT PLAYER TELEMETRY BAR -->
    <header class="top-hud">
      <div class="player-badge" id="btn-open-profile">
        <div class="avatar-ring">TT</div>
        <div class="player-meta">
          <div class="callsign-row">
            <strong id="ui-callsign">Commander</strong>
            <span class="online-dot" id="net-dot"></span>
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
        <a class="apk-pill" href="https://github.com/BigSkinnySlimm/TraitTakedown/releases/latest/download/TraitTakedown-Android-Native.apk" title="Download Native Android APK">📲 APK</a>
        <button class="icon-circle" id="btn-audio-toggle" title="Toggle Studio Audio">🔊</button>
      </div>
    </header>

    <!-- ================================================================== -->
    <!-- VIEW 1: STUDIO HOME LOBBY / SHOWCASE STAGE                         -->
    <!-- ================================================================== -->
    <section id="view-lobby" class="screen-view active">
      <div class="lobby-center-stage">
        <div class="lobby-pedestal-glow"></div>

        <!-- Featured Interactive 3D Holo Operative Showcase Card -->
        <div class="showcase-wrapper">
          <div class="showcase-tag">FEATURED OPERATIVE // TAP TO CYCLE</div>
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

        <!-- Primary Play CTA & Live Queue Status -->
        <div class="lobby-cta-stack">
          <button id="btn-play-ranked" class="btn-mega-play">
            <span class="play-main">⚡ PLAY RANKED ARENA</span>
            <span class="play-sub" id="net-status-label">GLOBAL AUTO-MATCHMAKING • ZERO ROOM CODES</span>
          </button>
          <div class="quick-modes-row">
            <button id="btn-quick-friend" class="btn-glass">⚔️ CHALLENGE FRIEND</button>
            <button id="btn-quick-inspect" class="btn-glass">🔍 INSPECT 24 ROSTER</button>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================== -->
    <!-- VIEW 2: FULLSCREEN TACTICAL BATTLE ARENA (ZERO PAGE SCROLL)        -->
    <!-- ================================================================== -->
    <section id="view-battle" class="screen-view">
      <!-- Compact Match Telemetry Subheader -->
      <div class="battle-topbar">
        <div class="vs-pill">
          <span class="vs-label">VS</span>
          <strong id="battle-opp-name">Valkyrie_IX</strong>
          <span id="battle-opp-elo" class="opp-mmr">(1,240)</span>
        </div>

        <div id="turn-pill" class="turn-indicator your-turn">YOUR TURN</div>

        <div class="suspect-counters">
          <span class="s-count cyan" title="Your Remaining Suspects">YOU: <b id="you-rem">24</b></span>
          <span class="s-count gold" title="Enemy Remaining Suspects">FOE: <b id="opp-rem">24</b></span>
          <span class="timer-pill" id="battle-timer">30s</span>
          <button id="btn-leave-match" class="btn-mini-exit" title="Forfeit / Return to Lobby">✕</button>
        </div>
      </div>

      <!-- Live Combat Ticker -->
      <div class="combat-ticker" id="combat-ticker">
        <span>📡 Tactical link established. Select a trait below to interrogate the enemy matrix.</span>
      </div>

      <!-- 24-Unit High-Density Interactive Holo Grid -->
      <div class="arena-grid-wrapper">
        <div id="battle-grid" class="battle-grid"></div>
      </div>

      <!-- Tactile Bottom Command & Trait Chip Dock (No <select> Dropdowns!) -->
      <div class="battle-command-dock">
        <!-- Left: Your Classified Secret Operative + Ultimate Button -->
        <div class="secret-dock-box">
          <div id="my-secret-mini" class="secret-mini-card" title="Tap to inspect your Operative">
            <img id="my-secret-img" src="" alt="Secret Unit" />
            <div class="secret-mini-meta">
              <small>YOUR OPERATIVE</small>
              <strong id="my-secret-name">Spiked Tortoise</strong>
              <span id="my-secret-traits">Ironclad • Terra</span>
            </div>
          </div>
          <button id="btn-fire-ultimate" class="btn-ultimate" disabled>
            <span>⚡ ULTIMATE</span>
            <small id="ult-name-label">READY</small>
          </button>
        </div>

        <!-- Right: Interactive Category Pills + Trait Value Chips + Fire Scan -->
        <div class="scanner-dock-box">
          <div class="cat-tabs" id="scanner-cat-tabs">
            <button class="cat-tab active" data-cat="faction">FACTION</button>
            <button class="cat-tab" data-cat="species">SPECIES</button>
            <button class="cat-tab" data-cat="armor">ARMOR</button>
            <button class="cat-tab" data-cat="weapon">WEAPON</button>
            <button class="cat-tab" data-cat="element">ELEMENT</button>
          </div>

          <div class="val-chips-row" id="scanner-val-chips"></div>

          <div class="action-buttons-row">
            <button id="btn-fire-scan" class="btn-action-scan" disabled>
              📡 SCAN TRAIT: <span id="selected-trait-preview">Ironclad</span>
            </button>
            <button id="btn-toggle-accuse" class="btn-action-accuse" disabled>
              🎯 ACCUSE
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ================================================================== -->
    <!-- VIEW 3: 24-OPERATIVE HOLO COLLECTION GALLERY                       -->
    <!-- ================================================================== -->
    <section id="view-collection" class="screen-view">
      <div class="subview-header">
        <h2>24 OPERATIVE CODEX & 3D HOLO GALLERY</h2>
        <p>Tap any operative to inspect full-resolution artwork, lore, and faction active ultimate.</p>
      </div>
      <div id="collection-grid" class="collection-grid"></div>
    </section>

    <!-- ================================================================== -->
    <!-- VIEW 4: FRIENDS NETWORK & RANKED ELO LEADERBOARD                   -->
    <!-- ================================================================== -->
    <section id="view-social" class="screen-view">
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
          <h3>🏆 GLOBAL RANKED ELO LADDER & HISTORY</h3>
          <div id="ranked-summary-bar" class="ranked-bar">GOLD I — 1,200 MMR (0W - 0L)</div>
          <div id="leaderboard-list" class="scroll-list compact"></div>
          <h4 class="sub-h4">RECENT MATCH TELEMETRY</h4>
          <div id="history-list" class="scroll-list compact"></div>
        </div>
      </div>
    </section>

    <!-- ================================================================== -->
    <!-- VIEW 5: SEASON PASS & COSMETIC ARMORY                              -->
    <!-- ================================================================== -->
    <section id="view-shop" class="screen-view">
      <div class="social-split">
        <div class="glass-panel">
          <div class="pass-header-row">
            <div>
              <h3>🎖️ SEASON 01: SOVEREIGN HORIZON PASS</h3>
              <p>SEASON XP: <strong id="ui-pass-xp">400</strong> / 1,200</p>
            </div>
            <button id="btn-buy-pass" class="btn-neon gold">ELITE PASS (150 ❖)</button>
          </div>
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
    </section>

    <!-- BOTTOM STUDIO NAVIGATION DOCK -->
    <nav class="bottom-nav" id="bottom-nav">
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
        <span class="nav-ico">🏆</span><small>RANKED & FRIENDS</small>
      </button>
      <button class="nav-tab" data-view="view-shop">
        <span class="nav-ico">💎</span><small>PASS & SHOP</small>
      </button>
    </nav>
  </div>

  <!-- MODAL: Matchmaking Radar Queue -->
  <div id="modal-queue" class="modal-overlay hidden">
    <div class="modal-card queue-card">
      <div class="radar-circle"><div class="radar-beam"></div></div>
      <h3>SEARCHING GLOBAL ARENA...</h3>
      <p>Pairing via Cloud Broker (MMR ±100)</p>
      <div class="queue-clock" id="queue-clock">00:00</div>
      <button id="btn-cancel-queue" class="btn-neon red">CANCEL SEARCH</button>
    </div>
  </div>

  <!-- MODAL: Full-Res 3D Card Inspector -->
  <div id="modal-inspect" class="modal-overlay hidden">
    <div class="modal-card inspect-card">
      <div id="inspect-card-mount" class="holo-card showcase-size"></div>
      <div class="inspect-ability-box">
        <strong id="inspect-ult-title">FACTION ULTIMATE</strong>
        <p id="inspect-ult-desc"></p>
      </div>
      <button id="btn-close-inspect" class="btn-neon cyan">CLOSE INSPECTOR</button>
    </div>
  </div>

  <!-- MODAL: Match Result Victory / Defeat Screen -->
  <div id="modal-result" class="modal-overlay hidden">
    <div class="modal-card result-card">
      <div class="result-badge" id="result-badge">VICTORY</div>
      <h2 id="result-heading">TARGET NEUTRALIZED</h2>
      <p id="result-details"></p>
      <div class="result-elo-pill" id="result-elo-pill">+24 MMR (1,224 ELO)</div>
      <div class="result-rewards">+200 ◈ CREDITS  •  +150 SEASON XP</div>
      <div class="result-btns">
        <button id="btn-play-again" class="btn-neon cyan">⚡ PLAY AGAIN</button>
        <button id="btn-result-lobby" class="btn-glass">HOME LOBBY</button>
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
# 3. CSS/STUDIO.CSS — Locked 100dvh Viewport, Holographic Foil Cards & Neon HUD
# ============================================================================
STUDIO_CSS = r"""
:root {
  --bg-void: #040711;
  --bg-glass: rgba(11, 19, 38, 0.86);
  --bg-panel: rgba(15, 25, 48, 0.92);
  --cyan: #00f0ff;
  --blue: #0066ff;
  --gold: #ffcc33;
  --red: #ff2a5f;
  --green: #00ff9d;
  --purple: #b84dff;
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
  background: radial-gradient(circle at 50% 25%, #132850 0%, #070d1d 55%, var(--bg-void) 100%);
  color: var(--text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

#vfx-canvas {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 40;
}

#app-viewport {
  position: relative;
  width: 100%;
  height: 100dvh;
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  z-index: 10;
}

/* TOP HUD */
.top-hud {
  height: 56px;
  padding: 0 0.85rem;
  background: linear-gradient(180deg, rgba(4, 8, 18, 0.95), rgba(8, 15, 30, 0.82));
  border-bottom: 1px solid rgba(0, 240, 255, 0.25);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.player-badge {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
}

.avatar-ring {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--cyan), var(--blue));
  color: #02060d;
  font-weight: 900;
  font-size: 0.95rem;
  display: grid;
  place-items: center;
  box-shadow: 0 0 14px rgba(0, 240, 255, 0.5);
}

.callsign-row {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.82rem;
}

.online-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px var(--green);
}

.rank-sub {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.68rem;
  color: var(--muted);
}

.tier-pill {
  background: rgba(255, 204, 51, 0.18);
  border: 1px solid rgba(255, 204, 51, 0.5);
  color: var(--gold);
  padding: 0.05rem 0.35rem;
  border-radius: 4px;
  font-weight: 800;
  font-size: 0.6rem;
}

.economy-cluster {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.res-pill {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(0, 240, 255, 0.28);
  padding: 0.25rem 0.55rem;
  border-radius: 99px;
  font-size: 0.74rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.res-pill.gold {
  border-color: rgba(255, 204, 51, 0.4);
  color: var(--gold);
}

.res-icon.cyan { color: var(--cyan); }

.apk-pill {
  text-decoration: none;
  background: linear-gradient(135deg, var(--gold), #ff8800);
  color: #040812;
  font-weight: 900;
  font-size: 0.68rem;
  padding: 0.28rem 0.55rem;
  border-radius: 6px;
}

.icon-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text);
  cursor: pointer;
}

/* VIEWS CONTAINER */
.screen-view {
  display: none;
  flex: 1;
  overflow: hidden;
  position: relative;
}

.screen-view.active {
  display: flex;
  flex-direction: column;
}

/* VIEW 1: HOME LOBBY */
.lobby-center-stage {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  padding: 0.5rem 1rem;
  position: relative;
}

.lobby-pedestal-glow {
  position: absolute;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0, 240, 255, 0.22) 0%, transparent 70%);
  pointer-events: none;
}

.showcase-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  z-index: 2;
}

.showcase-tag {
  font-size: 0.65rem;
  font-weight: 800;
  letter-spacing: 0.14em;
  color: var(--cyan);
  background: rgba(0, 240, 255, 0.12);
  border: 1px solid rgba(0, 240, 255, 0.35);
  padding: 0.2rem 0.65rem;
  border-radius: 99px;
}

/* 3D HOLOGRAPHIC CARDS */
.holo-card {
  position: relative;
  border-radius: 14px;
  background: #0b1428;
  border: 2px solid rgba(0, 240, 255, 0.55);
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.75), 0 0 20px rgba(0, 240, 255, 0.22);
  overflow: hidden;
  cursor: pointer;
  transform-style: preserve-3d;
  transition: transform 0.18s cubic-bezier(0.2, 0.85, 0.4, 1.2), box-shadow 0.2s ease, opacity 0.2s ease;
}

.holo-card.showcase-size {
  width: min(250px, 62vw);
  aspect-ratio: 400 / 520;
}

.holo-card.foil-active {
  border-color: var(--gold);
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.8), 0 0 26px rgba(255, 204, 51, 0.45);
}

.holo-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
}

.holo-card-inner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.holo-glare {
  position: absolute;
  inset: 0;
  background: linear-gradient(125deg, transparent 25%, rgba(0, 240, 255, 0.2) 45%, rgba(255, 204, 51, 0.22) 55%, transparent 75%);
  mix-blend-mode: screen;
  pointer-events: none;
}

.card-top-badges {
  position: absolute;
  top: 6px;
  left: 6px;
  right: 6px;
  display: flex;
  justify-content: space-between;
  pointer-events: none;
}

.c-badge {
  font-size: 0.58rem;
  font-weight: 900;
  padding: 0.14rem 0.42rem;
  border-radius: 5px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  backdrop-filter: blur(6px);
}

.c-badge.faction {
  background: rgba(5, 10, 22, 0.82);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #fff;
}

.c-badge.element {
  background: rgba(0, 240, 255, 0.22);
  border: 1px solid var(--cyan);
  color: var(--cyan);
}

.card-bottom-plate {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1.2rem 0.5rem 0.45rem;
  background: linear-gradient(0deg, rgba(3, 6, 14, 0.98) 45%, transparent 100%);
  text-align: center;
  pointer-events: none;
}

.card-bottom-plate h2 {
  font-size: 0.95rem;
  font-weight: 900;
  letter-spacing: 0.03em;
  text-shadow: 0 2px 6px #000;
}

.card-trait-line {
  font-size: 0.62rem;
  color: var(--cyan);
  font-weight: 700;
  margin-top: 0.1rem;
}

/* LOBBY CTA STACK */
.lobby-cta-stack {
  width: min(420px, 92vw);
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  z-index: 2;
}

.btn-mega-play {
  width: 100%;
  padding: 0.85rem 1.2rem;
  border-radius: 14px;
  border: 2px solid var(--cyan);
  background: linear-gradient(135deg, #00d2ff 0%, #0051ff 100%);
  color: #fff;
  cursor: pointer;
  box-shadow: 0 0 28px rgba(0, 240, 255, 0.45);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.15s ease;
}

.btn-mega-play:active { transform: scale(0.97); }

.play-main {
  font-size: 1.08rem;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.play-sub {
  font-size: 0.62rem;
  opacity: 0.9;
  font-weight: 700;
  margin-top: 0.12rem;
}

.quick-modes-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.btn-glass {
  background: rgba(15, 27, 52, 0.82);
  border: 1px solid rgba(0, 240, 255, 0.35);
  color: var(--text);
  padding: 0.58rem;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.74rem;
  cursor: pointer;
}

/* VIEW 2: FULLSCREEN BATTLE ARENA */
.battle-topbar {
  height: 40px;
  padding: 0 0.7rem;
  background: rgba(6, 12, 26, 0.92);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  flex-shrink: 0;
}

.vs-pill { display: flex; align-items: center; gap: 0.35rem; }
.vs-label { background: var(--red); color: #fff; font-weight: 900; font-size: 0.6rem; padding: 0.1rem 0.3rem; border-radius: 4px; }
.opp-mmr { color: var(--muted); font-size: 0.68rem; }

.turn-indicator {
  padding: 0.2rem 0.65rem;
  border-radius: 99px;
  font-weight: 900;
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  background: rgba(255, 204, 51, 0.18);
  color: var(--gold);
  border: 1px solid var(--gold);
}

.turn-indicator.your-turn {
  background: rgba(0, 255, 157, 0.18);
  color: var(--green);
  border-color: var(--green);
  box-shadow: 0 0 12px rgba(0, 255, 157, 0.35);
}

.suspect-counters {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.7rem;
}

.s-count.cyan b { color: var(--cyan); }
.s-count.gold b { color: var(--gold); }

.timer-pill {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.15rem 0.45rem;
  border-radius: 5px;
  font-weight: 800;
}

.btn-mini-exit {
  background: rgba(255, 42, 95, 0.22);
  border: 1px solid var(--red);
  color: #ff99b3;
  border-radius: 5px;
  padding: 0.12rem 0.4rem;
  cursor: pointer;
}

.combat-ticker {
  height: 24px;
  background: rgba(3, 7, 15, 0.9);
  border-bottom: 1px solid rgba(0, 240, 255, 0.18);
  padding: 0 0.75rem;
  display: flex;
  align-items: center;
  font-size: 0.68rem;
  color: var(--cyan);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
}

/* 24-CARD ARENA GRID (FITS SCREEN WITH COMPACT SCROLL OR FLUID FIT) */
.arena-grid-wrapper {
  flex: 1;
  padding: 0.45rem;
  overflow-y: auto;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.battle-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0.42rem;
}

@media (max-width: 720px) {
  .battle-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 0.35rem;
  }
}

.grid-holo-card {
  position: relative;
  aspect-ratio: 400 / 480;
  border-radius: 9px;
  background: #0c162c;
  border: 1.5px solid rgba(0, 240, 255, 0.42);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.16s ease, opacity 0.22s ease, filter 0.22s ease;
}

.grid-holo-card:hover {
  transform: translateY(-3px) scale(1.03);
  border-color: var(--cyan);
  box-shadow: 0 6px 16px rgba(0, 240, 255, 0.35);
  z-index: 3;
}

.grid-holo-card.matching-preview {
  border-color: var(--gold);
  box-shadow: 0 0 12px rgba(255, 204, 51, 0.55);
}

.grid-holo-card.eliminated {
  opacity: 0.18;
  filter: grayscale(95%) contrast(1.2);
  transform: scale(0.92);
}

.grid-holo-card.eliminated::after {
  content: "✕";
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  font-size: 1.8rem;
  font-weight: 900;
  color: var(--red);
  background: rgba(3, 6, 14, 0.65);
}

.grid-holo-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.grid-card-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(0deg, rgba(2, 5, 12, 0.96) 55%, transparent 100%);
  padding: 0.65rem 0.25rem 0.2rem;
  text-align: center;
}

.grid-card-name {
  font-size: 0.62rem;
  font-weight: 900;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.grid-card-sub {
  font-size: 0.5rem;
  color: var(--cyan);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* BOTTOM BATTLE COMMAND DOCK */
.battle-command-dock {
  background: linear-gradient(180deg, rgba(10, 18, 36, 0.96), rgba(4, 8, 18, 0.99));
  border-top: 1.5px solid rgba(0, 240, 255, 0.38);
  padding: 0.45rem 0.6rem;
  display: grid;
  grid-template-columns: 165px 1fr;
  gap: 0.55rem;
  flex-shrink: 0;
}

@media (max-width: 640px) {
  .battle-command-dock {
    grid-template-columns: 125px 1fr;
    gap: 0.4rem;
    padding: 0.38rem 0.45rem;
  }
}

.secret-dock-box {
  display: flex;
  flex-direction: column;
  gap: 0.32rem;
}

.secret-mini-card {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 240, 255, 0.35);
  border-radius: 8px;
  padding: 0.25rem;
  cursor: pointer;
}

.secret-mini-card img {
  width: 38px;
  height: 46px;
  border-radius: 5px;
  object-fit: cover;
  flex-shrink: 0;
}

.secret-mini-meta {
  overflow: hidden;
  line-height: 1.15;
}

.secret-mini-meta small {
  display: block;
  font-size: 0.48rem;
  color: var(--gold);
  font-weight: 800;
}

.secret-mini-meta strong {
  display: block;
  font-size: 0.65rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.secret-mini-meta span {
  font-size: 0.52rem;
  color: var(--cyan);
}

.btn-ultimate {
  background: linear-gradient(135deg, #ffbe3d, #ff5500);
  border: 1px solid #ffe082;
  color: #050912;
  border-radius: 7px;
  padding: 0.32rem;
  font-weight: 900;
  font-size: 0.64rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.btn-ultimate:disabled {
  opacity: 0.35;
  filter: grayscale(80%);
  cursor: not-allowed;
}

.btn-ultimate small {
  font-size: 0.5rem;
  opacity: 0.85;
}

/* TRAIT CHIP SCANNER CONSOLE */
.scanner-dock-box {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.32rem;
  overflow: hidden;
}

.cat-tabs {
  display: flex;
  gap: 0.25rem;
  overflow-x: auto;
}

.cat-tab {
  flex: 1;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--muted);
  padding: 0.25rem 0.35rem;
  border-radius: 6px;
  font-size: 0.58rem;
  font-weight: 800;
  cursor: pointer;
}

.cat-tab.active {
  background: rgba(0, 240, 255, 0.2);
  border-color: var(--cyan);
  color: #fff;
}

.val-chips-row {
  display: flex;
  gap: 0.3rem;
  overflow-x: auto;
  padding-bottom: 2px;
}

.trait-val-chip {
  background: #0c1730;
  border: 1px solid rgba(0, 240, 255, 0.3);
  color: var(--text);
  padding: 0.26rem 0.55rem;
  border-radius: 99px;
  font-size: 0.64rem;
  font-weight: 800;
  white-space: nowrap;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.trait-val-chip.selected {
  background: linear-gradient(135deg, rgba(0, 240, 255, 0.32), rgba(0, 102, 255, 0.45));
  border-color: var(--cyan);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
}

.chip-count {
  background: rgba(255, 255, 255, 0.14);
  padding: 0.04rem 0.3rem;
  border-radius: 99px;
  font-size: 0.54rem;
  color: var(--gold);
}

.action-buttons-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.38rem;
}

.btn-action-scan {
  background: linear-gradient(135deg, #00d2ff, #0055ff);
  border: 1px solid var(--cyan);
  color: #fff;
  border-radius: 7px;
  padding: 0.42rem;
  font-weight: 900;
  font-size: 0.7rem;
  cursor: pointer;
}

.btn-action-scan:disabled, .btn-action-accuse:disabled {
  opacity: 0.38;
  cursor: not-allowed;
}

.btn-action-accuse {
  background: rgba(255, 42, 95, 0.2);
  border: 1px solid var(--red);
  color: #ff8da6;
  border-radius: 7px;
  padding: 0.42rem 0.7rem;
  font-weight: 900;
  font-size: 0.7rem;
  cursor: pointer;
}

.btn-action-accuse.active {
  background: var(--red);
  color: #fff;
  box-shadow: 0 0 14px var(--red);
}

/* COLLECTION, SOCIAL & SHOP SUBVIEWS */
.subview-header {
  padding: 0.65rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.subview-header h2 { font-size: 0.95rem; color: var(--cyan); }
.subview-header p { font-size: 0.72rem; color: var(--muted); }

.collection-grid {
  flex: 1;
  padding: 0.75rem;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(125px, 1fr));
  gap: 0.65rem;
}

.social-split {
  flex: 1;
  padding: 0.75rem;
  overflow-y: auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

@media (max-width: 780px) {
  .social-split { grid-template-columns: 1fr; }
}

.glass-panel {
  background: var(--bg-panel);
  border: 1px solid rgba(0, 240, 255, 0.25);
  border-radius: 12px;
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.glass-panel h3 { font-size: 0.84rem; color: var(--cyan); }
.sub-h4 { font-size: 0.72rem; color: var(--gold); margin-top: 0.3rem; }

.form-row { display: flex; gap: 0.4rem; }
.neon-input {
  flex: 1;
  background: #060c1a;
  border: 1px solid rgba(0, 240, 255, 0.35);
  color: #fff;
  padding: 0.45rem 0.6rem;
  border-radius: 7px;
  font-size: 0.76rem;
}

.btn-neon {
  padding: 0.45rem 0.8rem;
  border-radius: 7px;
  font-weight: 800;
  font-size: 0.72rem;
  cursor: pointer;
  border: 1px solid transparent;
}

.btn-neon.cyan { background: linear-gradient(135deg, #00d2ff, #0055ff); color: #fff; border-color: var(--cyan); }
.btn-neon.gold { background: linear-gradient(135deg, var(--gold), #e67e22); color: #050912; }
.btn-neon.red { background: rgba(255, 42, 95, 0.25); border-color: var(--red); color: #ff99b3; }

.scroll-list {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  max-height: 220px;
  overflow-y: auto;
}

.list-item-row {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  padding: 0.5rem 0.65rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
}

/* BOTTOM NAVIGATION DOCK */
.bottom-nav {
  height: 54px;
  background: rgba(4, 8, 18, 0.96);
  border-top: 1px solid rgba(0, 240, 255, 0.25);
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  flex-shrink: 0;
}

.nav-tab {
  background: none;
  border: none;
  color: var(--muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.1rem;
  cursor: pointer;
  font-weight: 800;
}

.nav-tab .nav-ico { font-size: 1.05rem; }
.nav-tab small { font-size: 0.56rem; letter-spacing: 0.05em; }

.nav-tab.active {
  color: var(--cyan);
  background: radial-gradient(circle at 50% 100%, rgba(0, 240, 255, 0.22), transparent 70%);
}

/* MODALS & ULTIMATE CUT-IN */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(2, 5, 12, 0.86);
  backdrop-filter: blur(10px);
  display: grid;
  place-items: center;
  z-index: 60;
  padding: 1rem;
}

.modal-overlay.hidden, .ultimate-cutin.hidden, .challenge-toast.hidden {
  display: none !important;
}

.modal-card {
  background: #0b152b;
  border: 1.5px solid var(--cyan);
  border-radius: 16px;
  padding: 1.25rem;
  max-width: 380px;
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 20px 55px rgba(0, 0, 0, 0.85);
}

.radar-circle {
  width: 78px;
  height: 78px;
  border-radius: 50%;
  border: 2px solid var(--cyan);
  position: relative;
  overflow: hidden;
}

.radar-beam {
  position: absolute;
  inset: 0;
  background: conic-gradient(from 0deg, transparent 60%, rgba(0, 240, 255, 0.75) 100%);
  animation: radarSpin 1.3s linear infinite;
}

@keyframes radarSpin { to { transform: rotate(360deg); } }

.ultimate-cutin {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.78);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 90;
  pointer-events: none;
}

.cutin-slash {
  width: 100%;
  height: 170px;
  background: linear-gradient(90deg, #000 0%, #10254c 30%, #00d2ff 100%);
  border-top: 3px solid var(--gold);
  border-bottom: 3px solid var(--gold);
  transform: skewY(-4deg);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.2rem;
  box-shadow: 0 0 50px rgba(0, 240, 255, 0.7);
}

.cutin-slash img {
  height: 155px;
  border-radius: 10px;
  border: 2px solid var(--gold);
}

.cutin-text span {
  color: var(--gold);
  font-weight: 900;
  font-size: 0.75rem;
  letter-spacing: 0.18em;
}

.cutin-text h2 {
  font-size: 1.45rem;
  font-weight: 900;
  color: #fff;
  text-shadow: 0 4px 14px #000;
}

.challenge-toast {
  position: fixed;
  top: 64px;
  right: 16px;
  background: #0d1832;
  border: 2px solid var(--gold);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  z-index: 80;
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.legal-footer-links {
  font-size: 0.68rem;
  color: var(--muted);
  margin-top: auto;
}
.legal-footer-links a { color: var(--cyan); text-decoration: none; }
"""

# ============================================================================
# 4. JS/ROSTER.JS — 24 Operatives & Faction Active Ultimates
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
    desc: "Calls down an orbital laser strike that eliminates 3 confirmed non-target decoys on the matrix immediately."
  },
  Abyssal: {
    name: "VOID TEMPORAL JAMMER",
    desc: "Reveals whether enemy Biotype is Synthetic or Organic AND drains 8 seconds from their next turn clock."
  }
};

window.STUDIO_ROSTER = [
  { id: "u01", name: "Spiked Tortoise",   faction: "Ironclad",   species: "Reptilian",  armor: "Spiked Shell",    weapon: "Plasma Cannon", element: "Terra" },
  { id: "u02", name: "Vortex Stalker",    faction: "Cybernetic", species: "Android",    armor: "Stealth Weave",   weapon: "Rail Rifle",    element: "Volt" },
  { id: "u03", name: "Pyre Seraph",       faction: "Solaris",    species: "Avian",      armor: "Aegis Plate",     weapon: "Solar Lance",   element: "Solar" },
  { id: "u04", name: "Abyssal Leviathan", faction: "Abyssal",    species: "Cephalopod", armor: "Chitin Carapace", weapon: "Void Tendril",  element: "Void" },
  { id: "u05", name: "Chrome Basilisk",   faction: "Cybernetic", species: "Reptilian",  armor: "Aegis Plate",     weapon: "Plasma Cannon", element: "Volt" },
  { id: "u06", name: "Dread Carapace",    faction: "Abyssal",    species: "Arachnid",   armor: "Spiked Shell",    weapon: "Venom Blade",   element: "Void" },
  { id: "u07", name: "Helios Warden",     faction: "Solaris",    species: "Android",    armor: "Aegis Plate",     weapon: "Solar Lance",   element: "Solar" },
  { id: "u08", name: "Rust Juggernaut",   faction: "Ironclad",   species: "Construct",  armor: "Spiked Shell",    weapon: "Siege Hammer",  element: "Terra" },
  { id: "u09", name: "Neon Mantis",       faction: "Cybernetic", species: "Arachnid",   armor: "Stealth Weave",   weapon: "Venom Blade",   element: "Volt" },
  { id: "u10", name: "Trench Kraken",     faction: "Abyssal",    species: "Cephalopod", armor: "Chitin Carapace", weapon: "Plasma Cannon", element: "Cryo" },
  { id: "u11", name: "Dawn Valkyrie",     faction: "Solaris",    species: "Avian",      armor: "Stealth Weave",   weapon: "Rail Rifle",    element: "Solar" },
  { id: "u12", name: "Magma Golem",       faction: "Ironclad",   species: "Construct",  armor: "Aegis Plate",     weapon: "Siege Hammer",  element: "Solar" },
  { id: "u13", name: "Glacier Wyrm",      faction: "Abyssal",    species: "Reptilian",  armor: "Chitin Carapace", weapon: "Void Tendril",  element: "Cryo" },
  { id: "u14", name: "Aether Hawk",       faction: "Solaris",    species: "Avian",      armor: "Chitin Carapace", weapon: "Rail Rifle",    element: "Volt" },
  { id: "u15", name: "Cobalt Widow",      faction: "Cybernetic", species: "Arachnid",   armor: "Chitin Carapace", weapon: "Rail Rifle",    element: "Cryo" },
  { id: "u16", name: "Bastion Drake",     faction: "Ironclad",   species: "Reptilian",  armor: "Aegis Plate",     weapon: "Siege Hammer",  element: "Terra" },
  { id: "u17", name: "Null Specter",      faction: "Abyssal",    species: "Android",    armor: "Stealth Weave",   weapon: "Void Tendril",  element: "Void" },
  { id: "u18", name: "Volt Centurion",    faction: "Cybernetic", species: "Construct",  armor: "Aegis Plate",     weapon: "Solar Lance",   element: "Volt" },
  { id: "u19", name: "Frost Talon",       faction: "Solaris",    species: "Avian",      armor: "Spiked Shell",    weapon: "Venom Blade",   element: "Cryo" },
  { id: "u20", name: "Slag Octopod",      faction: "Ironclad",   species: "Cephalopod", armor: "Spiked Shell",    weapon: "Plasma Cannon", element: "Terra" },
  { id: "u21", name: "Prism Weaver",      faction: "Solaris",    species: "Arachnid",   armor: "Stealth Weave",   weapon: "Solar Lance",   element: "Solar" },
  { id: "u22", name: "Cryo Automaton",    faction: "Cybernetic", species: "Construct",  armor: "Spiked Shell",    weapon: "Siege Hammer",  element: "Cryo" },
  { id: "u23", name: "Rift Nautilus",     faction: "Abyssal",    species: "Cephalopod", armor: "Aegis Plate",     weapon: "Void Tendril",  element: "Void" },
  { id: "u24", name: "Titan Anvil",       faction: "Ironclad",   species: "Android",    armor: "Chitin Carapace", weapon: "Plasma Cannon", element: "Terra" }
];
"""

# ============================================================================
# 5. JS/ARTENGINE.JS — Bespoke Multi-Layered Character Illustration Engine
# ============================================================================
ART_ENGINE_JS = r"""
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
"""

# ============================================================================
# 6. JS/VFXENGINE.JS — Real-Time Laser Sweep, Particle Shatter & Screen Shake
# ============================================================================
VFX_ENGINE_JS = r"""
class StudioVFXEngine {
  constructor() {
    this.canvas = null;
    this.ctx = null;
    this.particles = [];
    this.lasers = [];
    this.ambient = [];
  }

  init() {
    this.canvas = document.getElementById("vfx-canvas");
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext("2d");
    this.resize();
    window.addEventListener("resize", () => this.resize());

    for (let i = 0; i < 32; i++) {
      this.ambient.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.35,
        vy: -0.3 - Math.random() * 0.5,
        r: 1 + Math.random() * 2,
        c: i % 2 === 0 ? "#00f0ff" : "#ffcc33"
      });
    }
    this.loop();
  }

  resize() {
    if (!this.canvas) return;
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  spawnEliminationBurst(rect, color = "#00f0ff") {
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    // Laser bolt from bottom command console to card center
    this.lasers.push({
      x1: window.innerWidth / 2,
      y1: window.innerHeight - 60,
      x2: cx,
      y2: cy,
      alpha: 1.0,
      color
    });

    // Shatter particles
    for (let i = 0; i < 24; i++) {
      const ang = Math.random() * Math.PI * 2;
      const spd = 2 + Math.random() * 6.5;
      this.particles.push({
        x: cx,
        y: cy,
        vx: Math.cos(ang) * spd,
        vy: Math.sin(ang) * spd,
        life: 1.0,
        r: 2 + Math.random() * 3.5,
        color
      });
    }
  }

  triggerUltimateCutIn(unit, abilityName) {
    const el = document.getElementById("ultimate-cutin");
    if (!el) return;
    document.getElementById("cutin-img").src = window.StudioArt.getArt(unit.id);
    document.getElementById("cutin-faction").textContent = unit.faction.toUpperCase() + " ACTIVE ULTIMATE";
    document.getElementById("cutin-title").textContent = abilityName;
    el.classList.remove("hidden");
    setTimeout(() => el.classList.add("hidden"), 1650);
  }

  loop() {
    requestAnimationFrame(() => this.loop());
    if (!this.ctx || !this.canvas) return;
    const w = this.canvas.width;
    const h = this.canvas.height;
    this.ctx.clearRect(0, 0, w, h);

    // Ambient floating motes
    this.ambient.forEach((m) => {
      m.x += m.vx;
      m.y += m.vy;
      if (m.y < 0) m.y = h;
      if (m.x < 0) m.x = w;
      if (m.x > w) m.x = 0;
      this.ctx.fillStyle = m.c + "44";
      this.ctx.beginPath();
      this.ctx.arc(m.x, m.y, m.r, 0, Math.PI * 2);
      this.ctx.fill();
    });

    // Laser Beams
    for (let i = this.lasers.length - 1; i >= 0; i--) {
      const l = this.lasers[i];
      this.ctx.save();
      this.ctx.strokeStyle = l.color;
      this.ctx.shadowColor = l.color;
      this.ctx.shadowBlur = 16;
      this.ctx.globalAlpha = l.alpha;
      this.ctx.lineWidth = 4 * l.alpha;
      this.ctx.beginPath();
      this.ctx.moveTo(l.x1, l.y1);
      this.ctx.lineTo(l.x2, l.y2);
      this.ctx.stroke();
      this.ctx.restore();
      l.alpha -= 0.06;
      if (l.alpha <= 0) this.lasers.splice(i, 1);
    }

    // Explosion Particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.life -= 0.035;
      if (p.life <= 0) {
        this.particles.splice(i, 1);
        continue;
      }
      this.ctx.save();
      this.ctx.fillStyle = p.color;
      this.ctx.shadowColor = p.color;
      this.ctx.shadowBlur = 10;
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

# ============================================================================
# 7. JS/AUDIO.JS — Symphonic WebAudio Synthesizer & Tactical Foley
# ============================================================================
AUDIO_JS = r"""
class SymphonicAudioEngine {
  constructor() {
    this.ctx = null;
    this.muted = false;
    this.running = false;
    this.step = 0;
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
      g.gain.linearRampToValueAtTime(0.025, now + 1.1);
      g.gain.exponentialRampToValueAtTime(0.0001, now + 4.2);
      o.connect(g);
      g.connect(this.ctx.destination);
      o.start(now);
      o.stop(now + 4.3);
    });
  }

  tone(freq, dur, type = "triangle", vol = 0.12) {
    this.ensure();
    if (!this.ctx || this.muted) return;
    const now = this.ctx.currentTime;
    const o = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    o.type = type;
    o.frequency.setValueAtTime(freq, now);
    g.gain.setValueAtTime(vol, now);
    g.gain.exponentialRampToValueAtTime(0.0001, now + dur);
    o.connect(g);
    g.connect(this.ctx.destination);
    o.start(now);
    o.stop(now + dur);
  }

  toggleMute() {
    this.muted = !this.muted;
    return this.muted;
  }

  playClick() { this.tone(620, 0.06, "sine", 0.08); }
  playFlip() { this.tone(240, 0.11, "triangle", 0.14); }
  playScan() {
    this.tone(440, 0.15, "sawtooth", 0.09);
    setTimeout(() => this.tone(880, 0.25, "triangle", 0.12), 80);
  }
  playUltimate() {
    [110, 220, 440, 659.25].forEach((f, i) => {
      setTimeout(() => this.tone(f, 0.45, "sawtooth", 0.12), i * 55);
    });
  }
  playVictory() {
    [293.66, 369.99, 440, 587.33].forEach((f, i) => {
      setTimeout(() => this.tone(f, 0.55, "triangle", 0.14), i * 110);
    });
  }
  playDefeat() {
    [220, 196, 146.83].forEach((f, i) => {
      setTimeout(() => this.tone(f, 0.5, "sawtooth", 0.11), i * 140);
    });
  }
}

window.StudioAudio = new SymphonicAudioEngine();
"""

# ============================================================================
# 8. JS/NETWORK.JS — Public Auto-Matchmaking Broker & Friends Presence
# ============================================================================
NETWORK_JS = r"""
class StudioNetworkBroker {
  constructor(callsign, callbacks) {
    this.callsign = callsign;
    this.cb = callbacks;
    this.peer = null;
    this.conn = null;
    this.initPeer();
  }

  clean(id) {
    return String(id || "Commander").replace(/[^a-zA-Z0-9_-]/g, "").slice(0, 16) || "Commander";
  }

  peerId(name) {
    return "tt-v9-user-" + this.clean(name).toLowerCase();
  }

  initPeer() {
    if (typeof Peer === "undefined") return;
    try {
      if (this.peer) this.peer.destroy();
      this.peer = new Peer(this.peerId(this.callsign), { debug: 0 });
      this.peer.on("open", () => this.cb.onOnline(this.callsign));
      this.peer.on("connection", (c) => {
        c.on("open", () => {
          c.on("data", (msg) => {
            if (msg.type === "DIRECT_CHALLENGE") {
              this.cb.onChallenge(msg.from, c);
            } else {
              this.cb.onData(msg);
            }
          });
        });
      });
    } catch (e) {}
  }

  setCallsign(name) {
    this.callsign = this.clean(name);
    this.initPeer();
    return this.callsign;
  }

  challengeFriend(friendName) {
    if (!this.peer) return false;
    const c = this.peer.connect(this.peerId(friendName), { reliable: true });
    c.on("open", () => {
      this.conn = c;
      c.send({ type: "DIRECT_CHALLENGE", from: this.callsign });
    });
    return true;
  }
}

window.StudioNetworkBroker = StudioNetworkBroker;
"""

# ============================================================================
# 9. JS/GAMECONTROLLER.JS — Fullscreen Controller, Smart AI & Tactile Scanner
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

    // Live Battle State
    this.inMatch = false;
    this.isMyTurn = false;
    this.accuseMode = false;
    this.abilityReady = false;
    this.selectedCat = "faction";
    this.selectedVal = "Ironclad";
    this.mySecret = this.roster[0];
    this.oppSecret = this.roster[1];
    this.oppName = "Valkyrie_IX";
    this.oppElo = 1240;
    this.eliminated = new Set();
    this.oppRemaining = 24;
    this.turnClock = 30;
    this.turnInterval = null;
    this.queueInterval = null;

    this.art.bakeAll(this.roster);
    this.vfx.init();

    this.net = new window.StudioNetworkBroker(this.profile.callsign, {
      onOnline: () => {},
      onChallenge: (from) => {
        document.getElementById("challenge-toast-text").textContent = from + " challenged you to a Live Duel!";
        document.getElementById("challenge-toast").classList.remove("hidden");
      },
      onData: () => {}
    });

    this.bindUI();
    this.updateShowcaseCard(0);
    this.renderCollection();
    this.renderSocialAndRanked();
    this.renderShopAndPass();
    this.renderTopHUD();
    this.renderScannerConsole();
  }

  loadProfile() {
    try {
      const raw = localStorage.getItem("tt_studio_v9");
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
      elitePass: false,
      foilUnlocked: false,
      friends: ["Valkyrie_IX", "Sovereign_Zero", "NexusPrime"],
      history: []
    };
  }

  saveProfile() {
    localStorage.setItem("tt_studio_v9", JSON.stringify(this.profile));
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
  }

  bindUI() {
    // Bottom Navigation Tabs
    document.querySelectorAll(".nav-tab").forEach((btn) => {
      btn.onclick = () => this.switchView(btn.getAttribute("data-view"));
    });

    // Showcase Card Tap Cycles Through All 24 Operatives
    const sc = document.getElementById("lobby-showcase-card");
    sc.onclick = () => {
      this.audio.playFlip();
      this.showcaseIdx = (this.showcaseIdx + 1) % this.roster.length;
      this.updateShowcaseCard(this.showcaseIdx);
    };

    // Main Lobby Play Buttons
    document.getElementById("btn-play-ranked").onclick = () => this.openMatchmakingQueue();
    document.getElementById("btn-quick-friend").onclick = () => this.switchView("view-social");
    document.getElementById("btn-quick-inspect").onclick = () => this.switchView("view-collection");
    document.getElementById("btn-cancel-queue").onclick = () => this.cancelQueue();

    // Audio Toggle
    document.getElementById("btn-audio-toggle").onclick = (e) => {
      e.currentTarget.textContent = this.audio.toggleMute() ? "🔇" : "🔊";
    };

    // Scanner Category Tabs
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

    // Fire Interrogation Scan, Ultimate & Accuse
    document.getElementById("btn-fire-scan").onclick = () => this.executeTraitScan();
    document.getElementById("btn-fire-ultimate").onclick = () => this.executeFactionUltimate();
    document.getElementById("btn-toggle-accuse").onclick = () => {
      this.accuseMode = !this.accuseMode;
      const b = document.getElementById("btn-toggle-accuse");
      b.classList.toggle("active", this.accuseMode);
      b.textContent = this.accuseMode ? "🎯 TAP CARD" : "🎯 ACCUSE";
      this.setTicker(this.accuseMode ? "🎯 ACCUSATION LOCKED: Tap the enemy suspect card on the grid!" : "📡 Select a trait chip to interrogate.");
    };

    document.getElementById("my-secret-mini").onclick = () => this.inspectOperative(this.mySecret);
    document.getElementById("btn-close-inspect").onclick = () => {
      document.getElementById("modal-inspect").classList.add("hidden");
    };

    document.getElementById("btn-leave-match").onclick = () => {
      clearInterval(this.turnInterval);
      this.inMatch = false;
      this.switchView("view-lobby");
    };

    // Social & Friends
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

    // Result Modal Buttons
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
        this.startMatch(rName, rElo);
      }
    }, 850);
  }

  cancelQueue() {
    clearInterval(this.queueInterval);
    document.getElementById("modal-queue").classList.add("hidden");
  }

  startMatch(oppName, oppElo) {
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

    this.switchView("view-battle");
    this.renderBattleGrid();
    this.renderScannerConsole();
    this.updateBattleCounters();
    this.setTicker(`⚔️ Deployed ${this.mySecret.name}. Interrogate traits to isolate ${this.oppName}'s operative!`);
    this.setTurn(true);
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
      if (this.turnClock === 0 && this.isMyTurn) {
        this.executeTraitScan();
      }
    }, 1000);

    if (!mine) {
      setTimeout(() => this.runSmartOpponentTurn(), 1300);
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
    }, 500);
  }

  animateEliminations(ids, beamColor) {
    ids.forEach((id) => {
      const cardEl = document.querySelector(`#battle-grid .grid-holo-card[data-id="${id}"]`);
      if (cardEl) {
        const rect = cardEl.getBoundingClientRect();
        this.vfx.spawnEliminationBurst(rect, beamColor);
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
            <img src="${this.art.getArt(u.id)}" alt="${u.name}" />
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
    this.inMatch = false;
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
        <img src="${this.art.getArt(u.id)}" alt="${u.name}" />
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
          <img src="${this.art.getArt(u.id)}" alt="${u.name}" />
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
      b.onclick = () => this.startMatch(b.getAttribute("data-duel"), this.profile.elo + 20);
    });

    document.getElementById("ranked-summary-bar").textContent =
      `${this.getTier(this.profile.elo)} — ${this.profile.elo} MMR (${this.profile.wins}W - ${this.profile.losses}L)`;

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
      .join("") || `<div class="list-item-row">No matches recorded yet.</div>`;
  }

  renderShopAndPass() {
    document.getElementById("ui-pass-xp").textContent = String(this.profile.xp);
    const tiers = [
      { t: 1, xp: 100, label: "+300 Tactical Credits" },
      { t: 2, xp: 350, label: "+100 Core Gems" },
      { t: 3, xp: 700, label: "Prismatic Holographic Foil Frame" },
      { t: 4, xp: 1200, label: "Apex Sovereign Title & +800 Credits" }
    ];
    document.getElementById("pass-tiers-container").innerHTML = tiers
      .map((x) => `
        <div class="list-item-row">
          <div><strong>TIER 0${x.t} (${x.xp} XP)</strong><div>${x.label}</div></div>
          <span class="tier-pill">${this.profile.xp >= x.xp ? "UNLOCKED" : "LOCKED"}</span>
        </div>
      `)
      .join("");

    document.getElementById("armory-items-container").innerHTML = `
      <div class="list-item-row">
        <div>
          <strong>Prismatic Gold Foil Deck Upgrade</strong>
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
# 10. GITHUB ACTIONS WORKFLOW — NATIVE ANDROID SDK COMPILER & RELEASE
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
          tag_name: v9.0.${{ github.run_number }}
          name: "Trait Takedown Studio Release v9.0.${{ github.run_number }}"
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
    print("\n[+] Trait Takedown v9.0 Studio Fullscreen Arena & Bespoke Art Engine built.")

if __name__ == "__main__":
    build_all()
