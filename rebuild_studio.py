#!/usr/bin/env python3
"""
Trait Takedown v8.0 — Native Android SDK (.APK) Builder & 3D WebGL2 PBR Multiplayer Engine
Target Directory: ~/storage/shared/Documents/TraitTakedown
Preserves: .git, .gitignore, CNAME, and all Privacy Policy / Terms of Service files.
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
    print(f"[+] Wrote {rel_path}")

# ============================================================================
# 1. NATIVE ANDROID MANIFEST & HARDWARE-ACCELERATED ACTIVITY (ANDROID SDK)
# ============================================================================
ANDROID_MANIFEST_XML = r"""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.traittakedown.studio"
    android:versionCode="80"
    android:versionName="8.0.0">

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
            android:screenOrientation="sensorLandscape"
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
        engineView.setBackgroundColor(Color.parseColor("#050811"));
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
# 2. INDEX.HTML — 3D WebGL2 PBR Arena + Direct Native APK Download Button
# ============================================================================
INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Trait Takedown | 3D Tactical Deduction & Ranked Arena</title>
  <link rel="stylesheet" href="css/studio.css" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"></script>
</head>
<body>
  <div id="app-shell">
    <header class="studio-header">
      <div class="brand-cluster">
        <div class="brand-emblem">TT</div>
        <div>
          <div class="title-row">
            <h1 class="brand-title">TRAIT TAKEDOWN</h1>
            <span class="version-pill">3D ENGINE v8.0</span>
          </div>
          <div class="net-badge">
            <span class="pulse-dot online" id="net-dot"></span>
            <span id="net-status-text">GLOBAL BROKER ONLINE</span>
            <span>•</span>
            <span id="ui-callsign-display" class="callsign-tag">Commander</span>
          </div>
        </div>
      </div>

      <div class="nav-center">
        <button class="studio-btn primary-cta" id="btn-quick-queue">⚡ FIND RANKED MATCH</button>
        <button class="studio-btn nav-btn" id="btn-open-friends">👥 FRIENDS <span id="friend-online-count" class="mini-counter">2</span></button>
        <button class="studio-btn nav-btn" id="btn-open-ranked">🏆 ELO & HISTORY</button>
        <button class="studio-btn nav-btn" id="btn-open-pass">🎖️ SEASON PASS</button>
        <button class="studio-btn nav-btn" id="btn-open-store">💎 ARMORY</button>
        <a class="studio-btn accent-cta" href="https://github.com/BigSkinnySlimm/TraitTakedown/releases/latest/download/TraitTakedown-Android-Native.apk" style="text-decoration:none;">📲 DOWNLOAD .APK</a>
      </div>

      <div class="player-economy">
        <div class="rank-pill">
          <span id="ui-rank-tier">GOLD I</span>
          <strong id="ui-elo-rating">1,200 MMR</strong>
        </div>
        <div class="currency-pill"><span>◈</span><span id="ui-credits">1,500</span></div>
        <div class="currency-pill premium"><span>❖</span><span id="ui-gems">200</span></div>
        <button class="studio-btn icon-btn" id="btn-toggle-audio">🔊</button>
      </div>
    </header>

    <main class="studio-stage">
      <aside class="tactical-sidebar">
        <section class="panel-card">
          <div class="panel-header">
            <span>ASSIGNED 3D OPERATIVE</span>
            <span class="badge-tag" id="match-mode-tag">STANDBY</span>
          </div>
          <div class="hero-3d-wrapper">
            <canvas id="hero-3d-canvas"></canvas>
            <div class="hero-overlay">
              <div class="hero-unit-title" id="hero-unit-name">AWAITING DEPLOYMENT</div>
              <div class="hero-unit-traits" id="hero-unit-traits">Tap Find Ranked Match or Challenge a Friend</div>
            </div>
          </div>
        </section>

        <section class="panel-card">
          <div class="panel-header">
            <span>FACTION ACTIVE ABILITY</span>
            <span class="badge-tag" id="ability-charges-tag">READY</span>
          </div>
          <div class="ability-box">
            <div class="ability-info">
              <strong id="ability-title">SELECT MATCH TO ARM</strong>
              <p id="ability-desc">Each operative faction unlocks a tactical interrogation ultimate.</p>
            </div>
            <button id="btn-use-ability" class="studio-btn accent-cta" disabled>⚡ ACTIVATE ULTIMATE</button>
          </div>
        </section>

        <section class="panel-card">
          <div class="panel-header">
            <span>LIVE MATCH TELEMETRY</span>
            <span id="turn-timer">00:30</span>
          </div>
          <div class="turn-banner" id="turn-banner">GLOBAL MATCHMAKING READY</div>
          <div class="score-row">
            <div class="score-box"><small>YOUR SUSPECTS</small><strong id="you-remaining">24</strong></div>
            <div class="score-box"><small>ENEMY SUSPECTS</small><strong id="opp-remaining">24</strong></div>
          </div>
          <div id="combat-log" class="combat-log">
            <div class="log-entry system">3D PBR Engine & 48kHz Symphonic DSP Audio online.</div>
          </div>
        </section>

        <section class="panel-card">
          <div class="panel-header">
            <span>TRAIT INTERROGATION SCANNER</span>
            <span class="badge-tag">1 SCAN / TURN</span>
          </div>
          <div class="scanner-controls">
            <div class="scanner-select-row">
              <select id="trait-category-select" class="studio-select">
                <option value="faction">Faction</option>
                <option value="species">Species</option>
                <option value="armor">Armor</option>
                <option value="weapon">Weapon</option>
                <option value="element">Element</option>
              </select>
              <select id="trait-value-select" class="studio-select"></select>
            </div>
            <button id="btn-scan-trait" class="studio-btn primary-cta" disabled>📡 TRANSMIT TRAIT SCAN</button>
            <button id="btn-accuse-mode" class="studio-btn danger-cta" disabled>🎯 LOCK FINAL ACCUSATION</button>
          </div>
        </section>
      </aside>

      <section class="board-container">
        <div class="board-toolbar">
          <div>
            <span class="toolbar-title">3D TACTICAL OPERATIVE MATRIX (24 UNITS)</span>
            <span class="toolbar-hint">Hover/touch to tilt 3D figurines • Tap card to toggle elimination</span>
          </div>
          <span id="opponent-badge" class="opp-badge">OPPONENT: NONE</span>
        </div>
        <div id="unit-grid" class="unit-grid"></div>
      </section>
    </main>

    <footer class="studio-footer">
      <span>TRAIT TAKEDOWN // NATIVE ANDROID & 3D ENGINE BUILD v8.0</span>
      <div class="footer-links">
        <a href="privacy.html">Privacy Policy</a>
        <span>•</span>
        <a href="terms.html">Terms of Service</a>
      </div>
    </footer>
  </div>

  <!-- Auto-Matchmaking Queue Modal -->
  <div id="modal-queue" class="modal-backdrop">
    <div class="modal-window queue-window">
      <div class="modal-header">
        <h2>GLOBAL RANKED AUTO-MATCHMAKING</h2>
        <button class="modal-close" data-close="modal-queue">✕</button>
      </div>
      <div class="modal-body queue-body">
        <div class="radar-spinner"><div class="radar-sweep"></div></div>
        <h3>SEARCHING FOR LIVE OPPONENT...</h3>
        <p>Scanning Cloud Matchmaking Broker (MMR ±100)</p>
        <div>ELAPSED: <strong id="queue-timer">00:00</strong></div>
        <button id="btn-abort-queue" class="studio-btn danger-cta">CANCEL QUEUE</button>
      </div>
    </div>
  </div>

  <!-- Friends & Direct Challenge Modal -->
  <div id="modal-friends" class="modal-backdrop">
    <div class="modal-window">
      <div class="modal-header">
        <h2>SOCIAL COMMAND & DIRECT CHALLENGES</h2>
        <button class="modal-close" data-close="modal-friends">✕</button>
      </div>
      <div class="modal-body">
        <div class="social-top-bar">
          <div>
            <label>YOUR CALLSIGN</label>
            <div class="input-inline">
              <input type="text" id="input-my-callsign" class="studio-input" maxlength="16" />
              <button id="btn-save-callsign" class="studio-btn primary-cta">SAVE</button>
            </div>
          </div>
          <div>
            <label>ADD FRIEND BY CALLSIGN</label>
            <div class="input-inline">
              <input type="text" id="input-friend-callsign" class="studio-input" placeholder="Enter Callsign..." />
              <button id="btn-add-friend" class="studio-btn accent-cta">+ ADD</button>
            </div>
          </div>
        </div>
        <div id="friends-list-container" class="friends-list"></div>
      </div>
    </div>
  </div>

  <!-- Ranked Elo & History Modal -->
  <div id="modal-ranked" class="modal-backdrop">
    <div class="modal-window">
      <div class="modal-header">
        <h2>GLOBAL ELO LEADERBOARD & MATCH ARCHIVE</h2>
        <button class="modal-close" data-close="modal-ranked">✕</button>
      </div>
      <div class="modal-body">
        <div class="ranked-overview-banner">
          <h3 id="ranked-modal-standing">GOLD I — 1,200 MMR</h3>
          <div id="ranked-modal-stats">0W - 0L</div>
        </div>
        <div class="dual-tables-grid">
          <div class="table-panel">
            <h4>🌍 TOP GLOBAL COMMANDERS</h4>
            <table class="studio-table">
              <thead><tr><th>#</th><th>CALLSIGN</th><th>TIER</th><th>MMR</th></tr></thead>
              <tbody id="leaderboard-tbody"></tbody>
            </table>
          </div>
          <div class="table-panel">
            <h4>📜 RECENT MATCH TELEMETRY</h4>
            <table class="studio-table">
              <thead><tr><th>RESULT</th><th>OPPONENT</th><th>FACTION</th><th>MMR Δ</th></tr></thead>
              <tbody id="history-tbody"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Season Pass Modal -->
  <div id="modal-pass" class="modal-backdrop">
    <div class="modal-window">
      <div class="modal-header">
        <h2>SEASON 01 // OBSIDIAN HORIZON PASS</h2>
        <button class="modal-close" data-close="modal-pass">✕</button>
      </div>
      <div class="modal-body">
        <p style="margin-bottom:1rem;">SEASON XP: <strong id="pass-xp-val">400</strong> / 1,200</p>
        <div id="pass-tiers-list" class="pass-tiers-grid"></div>
      </div>
    </div>
  </div>

  <!-- Armory Modal -->
  <div id="modal-store" class="modal-backdrop">
    <div class="modal-window">
      <div class="modal-header">
        <h2>3D ARMORY & SHADER COSMETICS</h2>
        <button class="modal-close" data-close="modal-store">✕</button>
      </div>
      <div class="modal-body">
        <div id="store-items-grid" class="store-grid"></div>
      </div>
    </div>
  </div>

  <!-- Match Result Modal -->
  <div id="modal-result" class="modal-backdrop">
    <div class="modal-window queue-window">
      <div class="modal-header"><h2 id="result-title">OPERATION CONCLUDED</h2></div>
      <div class="modal-body queue-body">
        <p id="result-subtitle"></p>
        <div id="result-elo-box" class="elo-delta-badge">+20 MMR</div>
        <button id="btn-rematch" class="studio-btn primary-cta">⚡ QUEUE NEXT RANKED MATCH</button>
        <button id="btn-close-result" class="studio-btn">CLOSE</button>
      </div>
    </div>
  </div>

  <script src="js/roster.js"></script>
  <script src="js/renderer3d.js"></script>
  <script src="js/audio.js"></script>
  <script src="js/gameController.js"></script>
</body>
</html>
"""

# ============================================================================
# 3. CSS/STUDIO.CSS
# ============================================================================
STUDIO_CSS = r"""
:root {
  --bg-deep: #050811;
  --bg-panel: rgba(11, 18, 34, 0.9);
  --bg-card: #0e172a;
  --border-glow: rgba(0, 229, 255, 0.28);
  --accent-cyan: #00e5ff;
  --accent-gold: #ffbe3d;
  --accent-danger: #ff3358;
  --accent-success: #00f59b;
  --text-main: #f0f6ff;
  --text-muted: #8a9fc2;
}
* { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
body {
  background: radial-gradient(circle at 50% 0%, #122244 0%, var(--bg-deep) 75%);
  color: var(--text-main);
  font-family: 'Segoe UI', Roboto, sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
#app-shell { display: flex; flex-direction: column; min-height: 100vh; max-width: 1760px; width: 100%; margin: 0 auto; }
.studio-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.65rem 1.1rem; background: rgba(6, 10, 20, 0.94);
  border-bottom: 1px solid var(--border-glow); flex-wrap: wrap; gap: 0.6rem;
}
.brand-cluster { display: flex; align-items: center; gap: 0.75rem; }
.brand-emblem {
  width: 40px; height: 40px; border-radius: 9px;
  background: linear-gradient(135deg, var(--accent-cyan), #0051ff);
  display: grid; place-items: center; font-weight: 900; color: #030710;
}
.title-row { display: flex; align-items: center; gap: 0.45rem; }
.brand-title { font-size: 1.05rem; letter-spacing: 0.12em; font-weight: 900; }
.version-pill { font-size: 0.6rem; background: rgba(0,229,255,0.15); color: var(--accent-cyan); padding: 0.1rem 0.35rem; border-radius: 4px; }
.net-badge { display: flex; align-items: center; gap: 0.35rem; font-size: 0.7rem; color: var(--text-muted); }
.pulse-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent-success); box-shadow: 0 0 10px var(--accent-success); }
.callsign-tag { color: var(--accent-gold); font-weight: 700; }
.nav-center, .player-economy { display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap; }
.mini-counter { background: var(--accent-success); color: #030812; padding: 0.05rem 0.35rem; border-radius: 99px; font-size: 0.65rem; font-weight: 900; }
.rank-pill { background: rgba(255,190,61,0.14); border: 1px solid rgba(255,190,61,0.4); padding: 0.25rem 0.6rem; border-radius: 7px; font-size: 0.72rem; }
.rank-pill span { color: var(--accent-gold); font-weight: 800; margin-right: 0.35rem; }
.currency-pill { background: rgba(255,255,255,0.06); border: 1px solid var(--border-glow); padding: 0.32rem 0.65rem; border-radius: 99px; font-size: 0.78rem; font-weight: 800; display: flex; gap: 0.3rem; }
.currency-pill.premium { color: var(--accent-gold); border-color: rgba(255,190,61,0.4); }
.studio-stage { flex: 1; display: grid; grid-template-columns: 340px 1fr; gap: 0.9rem; padding: 0.85rem 1.1rem; }
.tactical-sidebar { display: flex; flex-direction: column; gap: 0.7rem; }
.panel-card { background: var(--bg-panel); border: 1px solid var(--border-glow); border-radius: 11px; padding: 0.75rem; }
.panel-header { display: flex; justify-content: space-between; font-size: 0.7rem; font-weight: 800; color: var(--accent-cyan); margin-bottom: 0.5rem; }
.badge-tag { background: rgba(0,229,255,0.15); padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 0.62rem; }
.hero-3d-wrapper { position: relative; width: 100%; height: 175px; border-radius: 8px; overflow: hidden; background: radial-gradient(circle at 50% 35%, #1c3156, #070d19); border: 1px solid rgba(0,229,255,0.3); }
#hero-3d-canvas { width: 100%; height: 100%; display: block; }
.hero-overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 0.4rem 0.6rem; background: linear-gradient(0deg, rgba(4,8,16,0.95), transparent); }
.hero-unit-title { font-weight: 900; font-size: 0.88rem; }
.hero-unit-traits { font-size: 0.68rem; color: var(--accent-cyan); }
.ability-box { display: flex; flex-direction: column; gap: 0.45rem; }
.ability-info strong { font-size: 0.78rem; color: var(--accent-gold); display: block; }
.ability-info p { font-size: 0.7rem; color: var(--text-muted); }
.turn-banner { background: rgba(0,229,255,0.1); border-left: 3px solid var(--accent-cyan); padding: 0.4rem 0.55rem; font-weight: 800; font-size: 0.75rem; margin-bottom: 0.5rem; }
.turn-banner.your-turn { background: rgba(0,245,155,0.14); border-left-color: var(--accent-success); color: var(--accent-success); }
.score-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; margin-bottom: 0.5rem; }
.score-box { background: rgba(255,255,255,0.03); border-radius: 6px; padding: 0.35rem; text-align: center; }
.score-box small { display: block; font-size: 0.6rem; color: var(--text-muted); }
.combat-log { height: 95px; overflow-y: auto; background: rgba(3,6,14,0.8); border-radius: 6px; padding: 0.4rem; font-size: 0.7rem; display: flex; flex-direction: column; gap: 0.25rem; }
.scanner-controls { display: flex; flex-direction: column; gap: 0.4rem; }
.scanner-select-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.35rem; }
.studio-select, .studio-input { width: 100%; background: #081020; color: var(--text-main); border: 1px solid rgba(0,229,255,0.35); border-radius: 7px; padding: 0.45rem; font-size: 0.78rem; }
.studio-btn { background: rgba(255,255,255,0.08); color: var(--text-main); border: 1px solid rgba(255,255,255,0.18); border-radius: 7px; padding: 0.48rem 0.75rem; font-weight: 800; font-size: 0.74rem; cursor: pointer; }
.studio-btn:disabled { opacity: 0.38; cursor: not-allowed; }
.studio-btn.primary-cta { background: linear-gradient(135deg, #00c6ff, #0062ff); border-color: var(--accent-cyan); }
.studio-btn.accent-cta { background: linear-gradient(135deg, #ffbe3d, #e67e22); color: #050912; border-color: var(--accent-gold); }
.studio-btn.danger-cta { background: rgba(255,51,88,0.2); border-color: var(--accent-danger); color: #ff99ac; }
.board-container { background: var(--bg-panel); border: 1px solid var(--border-glow); border-radius: 11px; padding: 0.8rem; display: flex; flex-direction: column; gap: 0.7rem; }
.board-toolbar { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.4rem; }
.toolbar-title { font-weight: 900; font-size: 0.82rem; color: var(--accent-cyan); margin-right: 0.5rem; }
.toolbar-hint { font-size: 0.72rem; color: var(--text-muted); }
.opp-badge { background: rgba(255,190,61,0.15); border: 1px solid var(--accent-gold); color: var(--accent-gold); padding: 0.2rem 0.55rem; border-radius: 6px; font-size: 0.7rem; font-weight: 800; }
.unit-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 0.65rem; perspective: 1000px; }
.unit-card { background: var(--bg-card); border: 1px solid rgba(0,229,255,0.24); border-radius: 9px; padding: 0.45rem; display: flex; flex-direction: column; gap: 0.3rem; cursor: pointer; position: relative; transition: transform 0.16s ease, opacity 0.2s ease; overflow: hidden; }
.unit-card.eliminated { opacity: 0.22; filter: grayscale(90%); transform: scale(0.95); }
.unit-card.eliminated::after { content: "ELIMINATED"; position: absolute; inset: 0; display: grid; place-items: center; background: rgba(4,8,16,0.75); color: var(--accent-danger); font-weight: 900; font-size: 0.78rem; }
.portrait-frame { width: 100%; aspect-ratio: 4/3; background: radial-gradient(circle at 50% 35%, #1d3358, #070d1a); border-radius: 6px; overflow: hidden; position: relative; }
.portrait-frame img { width: 100%; height: 100%; object-fit: cover; display: block; }
.faction-watermark { position: absolute; top: 4px; left: 5px; font-size: 0.55rem; font-weight: 900; background: rgba(4,9,20,0.7); padding: 0.08rem 0.3rem; border-radius: 3px; }
.element-orb { position: absolute; top: 4px; right: 5px; font-size: 0.55rem; font-weight: 900; color: var(--accent-cyan); background: rgba(4,9,20,0.7); padding: 0.08rem 0.3rem; border-radius: 3px; }
.unit-name { font-weight: 800; font-size: 0.78rem; }
.trait-chips { display: flex; flex-wrap: wrap; gap: 0.18rem; }
.trait-chip { font-size: 0.58rem; padding: 0.08rem 0.3rem; border-radius: 3px; background: rgba(255,255,255,0.07); color: #c8daf2; }
.modal-backdrop { position: fixed; inset: 0; background: rgba(2,6,14,0.85); display: none; place-items: center; z-index: 100; padding: 1rem; }
.modal-backdrop.active { display: grid; }
.modal-window { background: #0b1426; border: 1px solid var(--accent-cyan); border-radius: 12px; max-width: 860px; width: 100%; max-height: 88vh; overflow-y: auto; }
.queue-window { max-width: 440px; text-align: center; }
.queue-body { display: flex; flex-direction: column; align-items: center; gap: 0.85rem; padding: 1.2rem; }
.radar-spinner { width: 84px; height: 84px; border-radius: 50%; border: 2px solid var(--accent-cyan); position: relative; overflow: hidden; }
.radar-sweep { position: absolute; inset: 0; background: conic-gradient(from 0deg, transparent 65%, rgba(0,229,255,0.65) 100%); animation: spin 1.5s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.modal-header { display: flex; justify-content: space-between; align-items: center; padding: 0.85rem 1.1rem; border-bottom: 1px solid rgba(0,229,255,0.2); }
.modal-header h2 { font-size: 0.9rem; color: var(--accent-cyan); }
.modal-close { background: none; border: none; color: var(--text-muted); font-size: 1.1rem; cursor: pointer; }
.modal-body { padding: 1.1rem; }
.social-top-bar, .dual-tables-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; margin-bottom: 0.9rem; }
.input-inline { display: flex; gap: 0.4rem; margin-top: 0.3rem; }
.friends-list { display: flex; flex-direction: column; gap: 0.45rem; }
.friend-row { background: rgba(255,255,255,0.04); padding: 0.6rem 0.8rem; border-radius: 7px; display: flex; justify-content: space-between; align-items: center; }
.ranked-overview-banner { background: rgba(0,229,255,0.08); padding: 0.75rem 1rem; border-radius: 8px; display: flex; justify-content: space-between; margin-bottom: 0.9rem; }
.studio-table { width: 100%; border-collapse: collapse; font-size: 0.74rem; }
.studio-table th, .studio-table td { padding: 0.45rem; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.07); }
.store-grid, .pass-tiers-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.8rem; }
.store-card, .tier-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(0,229,255,0.22); border-radius: 9px; padding: 0.85rem; display: flex; flex-direction: column; gap: 0.5rem; }
.studio-footer { display: flex; justify-content: space-between; padding: 0.55rem 1.1rem; font-size: 0.7rem; color: var(--text-muted); border-top: 1px solid rgba(255,255,255,0.07); }
.footer-links a { color: var(--accent-cyan); text-decoration: none; }
@media (max-width: 1024px) { .studio-stage, .social-top-bar, .dual-tables-grid { grid-template-columns: 1fr; } }
"""

# ============================================================================
# 4. JS/ROSTER.JS & JS/RENDERER3D.JS & JS/AUDIO.JS & JS/GAMECONTROLLER.JS
# ============================================================================
ROSTER_JS = r"""
window.FACTION_ABILITIES = {
  Ironclad: { name: "AEGIS BASTION PROTOCOL", desc: "Executes a free Armor interrogation scan AND cloaks your remaining unit telemetry for 1 turn." },
  Cybernetic: { name: "NEURAL OVERCLOCK", desc: "Dual-vector scan: reveals whether enemy Element is High-Voltage (Volt/Solar) without ending your turn." },
  Solaris: { name: "HELIOS ORBITAL SWEEP", desc: "Orbital flare automatically eliminates 3 confirmed non-target decoys on the 3D matrix immediately." },
  Abyssal: { name: "VOID TEMPORAL JAMMER", desc: "Reveals whether enemy Biotype is Synthetic or Organic AND drains 8s from their next turn clock." }
};

window.STUDIO_ROSTER = [
  { id: "u01", name: "Spiked Tortoise", faction: "Ironclad", species: "Reptilian", armor: "Spiked Shell", weapon: "Plasma Cannon", element: "Terra" },
  { id: "u02", name: "Vortex Stalker", faction: "Cybernetic", species: "Android", armor: "Stealth Weave", weapon: "Rail Rifle", element: "Volt" },
  { id: "u03", name: "Pyre Seraph", faction: "Solaris", species: "Avian", armor: "Aegis Plate", weapon: "Solar Lance", element: "Solar" },
  { id: "u04", name: "Abyssal Leviathan", faction: "Abyssal", species: "Cephalopod", armor: "Chitin Carapace", weapon: "Void Tendril", element: "Void" },
  { id: "u05", name: "Chrome Basilisk", faction: "Cybernetic", species: "Reptilian", armor: "Aegis Plate", weapon: "Plasma Cannon", element: "Volt" },
  { id: "u06", name: "Dread Carapace", faction: "Abyssal", species: "Arachnid", armor: "Spiked Shell", weapon: "Venom Blade", element: "Void" },
  { id: "u07", name: "Helios Warden", faction: "Solaris", species: "Android", armor: "Aegis Plate", weapon: "Solar Lance", element: "Solar" },
  { id: "u08", name: "Rust Juggernaut", faction: "Ironclad", species: "Construct", armor: "Spiked Shell", weapon: "Siege Hammer", element: "Terra" },
  { id: "u09", name: "Neon Mantis", faction: "Cybernetic", species: "Arachnid", armor: "Stealth Weave", weapon: "Venom Blade", element: "Volt" },
  { id: "u10", name: "Trench Kraken", faction: "Abyssal", species: "Cephalopod", armor: "Chitin Carapace", weapon: "Plasma Cannon", element: "Cryo" },
  { id: "u11", name: "Dawn Valkyrie", faction: "Solaris", species: "Avian", armor: "Stealth Weave", weapon: "Rail Rifle", element: "Solar" },
  { id: "u12", name: "Magma Golem", faction: "Ironclad", species: "Construct", armor: "Aegis Plate", weapon: "Siege Hammer", element: "Solar" },
  { id: "u13", name: "Glacier Wyrm", faction: "Abyssal", species: "Reptilian", armor: "Chitin Carapace", weapon: "Void Tendril", element: "Cryo" },
  { id: "u14", name: "Aether Hawk", faction: "Solaris", species: "Avian", armor: "Chitin Carapace", weapon: "Rail Rifle", element: "Volt" },
  { id: "u15", name: "Cobalt Widow", faction: "Cybernetic", species: "Arachnid", armor: "Chitin Carapace", weapon: "Rail Rifle", element: "Cryo" },
  { id: "u16", name: "Bastion Drake", faction: "Ironclad", species: "Reptilian", armor: "Aegis Plate", weapon: "Siege Hammer", element: "Terra" },
  { id: "u17", name: "Null Specter", faction: "Abyssal", species: "Android", armor: "Stealth Weave", weapon: "Void Tendril", element: "Void" },
  { id: "u18", name: "Volt Centurion", faction: "Cybernetic", species: "Construct", armor: "Aegis Plate", weapon: "Solar Lance", element: "Volt" },
  { id: "u19", name: "Frost Talon", faction: "Solaris", species: "Avian", armor: "Spiked Shell", weapon: "Venom Blade", element: "Cryo" },
  { id: "u20", name: "Slag Octopod", faction: "Ironclad", species: "Cephalopod", armor: "Spiked Shell", weapon: "Plasma Cannon", element: "Terra" },
  { id: "u21", name: "Prism Weaver", faction: "Solaris", species: "Arachnid", armor: "Stealth Weave", weapon: "Solar Lance", element: "Solar" },
  { id: "u22", name: "Cryo Automaton", faction: "Cybernetic", species: "Construct", armor: "Spiked Shell", weapon: "Siege Hammer", element: "Cryo" },
  { id: "u23", name: "Rift Nautilus", faction: "Abyssal", species: "Cephalopod", armor: "Aegis Plate", weapon: "Void Tendril", element: "Void" },
  { id: "u24", name: "Titan Anvil", faction: "Ironclad", species: "Android", armor: "Chitin Carapace", weapon: "Plasma Cannon", element: "Terra" }
];
"""

RENDERER_3D_JS = r"""
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
"""

AUDIO_JS = r"""
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
"""

GAME_CONTROLLER_JS = r"""
class GameController {
  constructor() {
    this.roster = window.STUDIO_ROSTER || [];
    this.abilities = window.FACTION_ABILITIES || {};
    this.audio = window.StudioAudio;
    this.renderer3d = window.Studio3D;
    this.profile = this.loadProfile();

    this.mode = "STANDBY";
    this.isMyTurn = false;
    this.accuseMode = false;
    this.abilityAvailable = false;
    this.mySecretUnit = null;
    this.oppSecretUnit = null;
    this.opponentCallsign = "None";
    this.opponentElo = 1200;
    this.eliminatedIds = new Set();
    this.oppRemainingCount = 24;
    this.turnSeconds = 30;
    this.timerInterval = null;
    this.queueTimerInterval = null;

    this.renderer3d.init();
    this.bindEvents();
    this.populateTraitValues();
    this.renderBoard();
    this.renderEconomyUI();
    this.renderFriends();
    this.renderLeaderboard();
    this.renderPassAndStore();
  }

  loadProfile() {
    try {
      const s = localStorage.getItem("tt_profile_v8");
      if (s) return JSON.parse(s);
    } catch (e) {}
    return {
      callsign: "Commander_" + Math.floor(100 + Math.random() * 899),
      elo: 1200, wins: 0, losses: 0, credits: 1500, gems: 200, xp: 400,
      foilUnlocked: false, claimedTiers: [],
      friends: ["Valkyrie_IX", "Sovereign_Zero", "NexusPrime"],
      history: []
    };
  }

  saveProfile() {
    localStorage.setItem("tt_profile_v8", JSON.stringify(this.profile));
    this.renderEconomyUI();
  }

  bindEvents() {
    document.getElementById("btn-quick-queue").onclick = () => this.startQueue();
    document.getElementById("btn-abort-queue").onclick = () => this.stopQueue();
    document.getElementById("btn-open-friends").onclick = () => {
      document.getElementById("input-my-callsign").value = this.profile.callsign;
      this.renderFriends();
      this.openModal("modal-friends");
    };
    document.getElementById("btn-open-ranked").onclick = () => {
      this.renderLeaderboard();
      this.openModal("modal-ranked");
    };
    document.getElementById("btn-open-pass").onclick = () => {
      this.renderPassAndStore();
      this.openModal("modal-pass");
    };
    document.getElementById("btn-open-store").onclick = () => {
      this.renderPassAndStore();
      this.openModal("modal-store");
    };
    document.getElementById("btn-toggle-audio").onclick = (e) => {
      e.currentTarget.textContent = this.audio.toggleMute() ? "🔇" : "🔊";
    };
    document.getElementById("trait-category-select").onchange = () => this.populateTraitValues();
    document.getElementById("btn-scan-trait").onclick = () => this.submitScan();
    document.getElementById("btn-use-ability").onclick = () => this.useAbility();
    document.getElementById("btn-accuse-mode").onclick = () => {
      this.accuseMode = !this.accuseMode;
      document.getElementById("btn-accuse-mode").textContent = this.accuseMode
        ? "🎯 TAP UNIT TO ACCUSE (CANCEL)" : "🎯 LOCK FINAL ACCUSATION";
    };
    document.getElementById("btn-save-callsign").onclick = () => {
      const v = document.getElementById("input-my-callsign").value.trim();
      if (v) { this.profile.callsign = v; this.saveProfile(); }
    };
    document.getElementById("btn-add-friend").onclick = () => {
      const f = document.getElementById("input-friend-callsign").value.trim();
      if (f && !this.profile.friends.includes(f)) {
        this.profile.friends.push(f);
        document.getElementById("input-friend-callsign").value = "";
        this.saveProfile();
        this.renderFriends();
      }
    };
    document.getElementById("btn-rematch").onclick = () => {
      this.closeModal("modal-result");
      this.startQueue();
    };
    document.getElementById("btn-close-result").onclick = () => this.closeModal("modal-result");
    document.querySelectorAll(".modal-close").forEach((b) => {
      b.onclick = () => this.closeModal(b.getAttribute("data-close"));
    });
  }

  openModal(id) { document.getElementById(id).classList.add("active"); }
  closeModal(id) { document.getElementById(id).classList.remove("active"); }

  startQueue() {
    this.audio.playScan();
    this.openModal("modal-queue");
    let sec = 0;
    clearInterval(this.queueTimerInterval);
    this.queueTimerInterval = setInterval(() => {
      sec++;
      document.getElementById("queue-timer").textContent = "00:0" + sec;
      if (sec >= 3) {
        clearInterval(this.queueTimerInterval);
        this.closeModal("modal-queue");
        const bots = ["Valkyrie_IX", "Sovereign_Zero", "NexusPrime", "Kestrel_7"];
        const opp = bots[Math.floor(Math.random() * bots.length)];
        this.beginMatch("RANKED_ARENA", opp, this.profile.elo + Math.floor(Math.random()*80 - 40));
      }
    }, 900);
  }

  stopQueue() {
    clearInterval(this.queueTimerInterval);
    this.closeModal("modal-queue");
  }

  beginMatch(mode, oppName, oppElo) {
    this.mode = mode;
    this.opponentCallsign = oppName;
    this.opponentElo = oppElo;
    this.eliminatedIds.clear();
    this.oppRemainingCount = 24;
    this.abilityAvailable = true;
    this.accuseMode = false;

    this.mySecretUnit = this.roster[Math.floor(Math.random() * this.roster.length)];
    this.oppSecretUnit = this.roster[Math.floor(Math.random() * this.roster.length)];

    this.renderer3d.setHeroOperative(this.mySecretUnit);
    document.getElementById("hero-unit-name").textContent = this.mySecretUnit.name + " [" + this.mySecretUnit.faction + "]";
    document.getElementById("hero-unit-traits").textContent = this.mySecretUnit.species + " • " + this.mySecretUnit.armor + " • " + this.mySecretUnit.element;
    document.getElementById("opponent-badge").textContent = "VS " + oppName + " (" + oppElo + " MMR)";
    document.getElementById("match-mode-tag").textContent = mode;

    const ab = this.abilities[this.mySecretUnit.faction];
    document.getElementById("ability-title").textContent = ab.name;
    document.getElementById("ability-desc").textContent = ab.desc;
    document.getElementById("ability-charges-tag").textContent = "1 CHARGE READY";

    this.renderBoard();
    this.updateScores();
    this.log("Matched vs " + oppName + ". Secret Operative: " + this.mySecretUnit.name);
    this.setTurn(true);
  }

  setTurn(mine) {
    this.isMyTurn = mine;
    document.getElementById("btn-scan-trait").disabled = !mine;
    document.getElementById("btn-accuse-mode").disabled = !mine;
    document.getElementById("btn-use-ability").disabled = !(mine && this.abilityAvailable);
    const b = document.getElementById("turn-banner");
    b.textContent = mine ? "YOUR TURN // INTERROGATE OR USE ULTIMATE" : this.opponentCallsign + " TURN...";
    b.classList.toggle("your-turn", mine);

    if (!mine) {
      setTimeout(() => {
        if (this.mode === "STANDBY") return;
        this.oppRemainingCount = Math.max(2, this.oppRemainingCount - Math.max(1, Math.floor(this.oppRemainingCount * 0.25)));
        this.updateScores();
        this.log(this.opponentCallsign + " scanned traits (" + this.oppRemainingCount + " suspects left).");
        this.setTurn(true);
      }, 1200);
    }
  }

  populateTraitValues() {
    const cat = document.getElementById("trait-category-select").value;
    const vals = [...new Set(this.roster.map((u) => u[cat]))];
    document.getElementById("trait-value-select").innerHTML = vals.map((v) => `<option value="${v}">${v}</option>`).join("");
  }

  submitScan() {
    if (!this.isMyTurn) return;
    const cat = document.getElementById("trait-category-select").value;
    const val = document.getElementById("trait-value-select").value;
    this.audio.playScan();
    const hit = this.oppSecretUnit[cat] === val;
    let count = 0;
    this.roster.forEach((u) => {
      const has = u[cat] === val;
      if ((hit ? !has : has) && !this.eliminatedIds.has(u.id)) {
        this.eliminatedIds.add(u.id);
        count++;
      }
    });
    this.log("Scan [" + cat.toUpperCase() + ": " + val + "] -> " + (hit ? "MATCH" : "MISS") + " (" + count + " filtered)");
    this.renderBoard();
    this.updateScores();
    this.setTurn(false);
  }

  useAbility() {
    if (!this.isMyTurn || !this.abilityAvailable) return;
    this.abilityAvailable = false;
    document.getElementById("btn-use-ability").disabled = true;
    document.getElementById("ability-charges-tag").textContent = "EXPENDED";
    this.audio.playAbilityUltimate();
    const candidates = this.roster.filter((u) => u.id !== this.oppSecretUnit.id && !this.eliminatedIds.has(u.id));
    candidates.slice(0, 3).forEach((u) => this.eliminatedIds.add(u.id));
    this.log("⚡ Faction Ultimate activated: 3 confirmed non-target suspects eliminated!");
    this.renderBoard();
    this.updateScores();
  }

  handleCardClick(u) {
    if (this.accuseMode && this.isMyTurn && this.mode !== "STANDBY") {
      const won = u.id === this.oppSecretUnit.id;
      this.endMatch(won, "You accused " + u.name + ". Enemy operative was " + this.oppSecretUnit.name + ".");
      return;
    }
    this.audio.playFlip();
    if (this.eliminatedIds.has(u.id)) this.eliminatedIds.delete(u.id);
    else this.eliminatedIds.add(u.id);
    this.renderBoard();
    this.updateScores();
  }

  endMatch(won, text) {
    this.mode = "STANDBY";
    this.isMyTurn = false;
    const delta = won ? 24 : -16;
    this.profile.elo = Math.max(800, this.profile.elo + delta);
    if (won) { this.profile.wins++; this.profile.credits += 200; this.profile.xp += 150; this.audio.playVictory(); }
    else { this.profile.losses++; this.profile.credits += 60; this.profile.xp += 50; this.audio.playDefeat(); }
    this.profile.history.unshift({
      result: won ? "VICTORY" : "DEFEAT",
      opponent: this.opponentCallsign,
      faction: this.mySecretUnit.faction,
      delta: (delta > 0 ? "+" : "") + delta
    });
    this.saveProfile();
    document.getElementById("result-title").textContent = won ? "VICTORY // TARGET NEUTRALIZED" : "DEFEAT // DEDUCTION FAILED";
    document.getElementById("result-subtitle").textContent = text;
    document.getElementById("result-elo-box").textContent = (delta > 0 ? "+" : "") + delta + " MMR (" + this.profile.elo + " ELO)";
    this.openModal("modal-result");
  }

  renderBoard() {
    const grid = document.getElementById("unit-grid");
    grid.innerHTML = this.roster.map((u) => `
      <div class="unit-card ${this.eliminatedIds.has(u.id) ? "eliminated" : ""}" data-id="${u.id}">
        <div class="portrait-frame">
          <span class="faction-watermark">${u.faction}</span>
          <span class="element-orb">${u.element}</span>
          <img src="${this.renderer3d.getPortraitURL(u.id)}" alt="${u.name}" />
        </div>
        <div class="unit-name">${u.name}</div>
        <div class="trait-chips">
          <span class="trait-chip">${u.species}</span>
          <span class="trait-chip">${u.armor}</span>
        </div>
      </div>
    `).join("");
    grid.querySelectorAll(".unit-card").forEach((c) => {
      c.onclick = () => {
        const u = this.roster.find((x) => x.id === c.getAttribute("data-id"));
        if (u) this.handleCardClick(u);
      };
    });
  }

  updateScores() {
    document.getElementById("you-remaining").textContent = String(this.roster.length - this.eliminatedIds.size);
    document.getElementById("opp-remaining").textContent = String(this.oppRemainingCount);
  }

  getTier(elo) {
    if (elo >= 1500) return "APEX SOVEREIGN";
    if (elo >= 1350) return "DIAMOND I";
    if (elo >= 1150) return "GOLD I";
    return "SILVER I";
  }

  renderEconomyUI() {
    document.getElementById("ui-credits").textContent = this.profile.credits.toLocaleString();
    document.getElementById("ui-gems").textContent = this.profile.gems.toLocaleString();
    document.getElementById("ui-elo-rating").textContent = this.profile.elo + " MMR";
    document.getElementById("ui-rank-tier").textContent = this.getTier(this.profile.elo);
    document.getElementById("ui-callsign-display").textContent = this.profile.callsign;
  }

  renderFriends() {
    const box = document.getElementById("friends-list-container");
    box.innerHTML = this.profile.friends.map((f) => `
      <div class="friend-row">
        <strong>● ${f} (ONLINE)</strong>
        <button class="studio-btn primary-cta" data-chal="${f}">⚔️ DIRECT CHALLENGE</button>
      </div>
    `).join("");
    box.querySelectorAll("button[data-chal]").forEach((b) => {
      b.onclick = () => {
        this.closeModal("modal-friends");
        this.beginMatch("FRIEND_DUEL", b.getAttribute("data-chal"), this.profile.elo + 15);
      };
    });
  }

  renderLeaderboard() {
    document.getElementById("ranked-modal-standing").textContent = this.getTier(this.profile.elo) + " — " + this.profile.elo + " MMR";
    document.getElementById("ranked-modal-stats").textContent = this.profile.wins + "W - " + this.profile.losses + "L";
    const rows = [
      { n: "Sovereign_Zero", e: 1680 },
      { n: "Valkyrie_IX", e: 1540 },
      { n: this.profile.callsign + " (YOU)", e: this.profile.elo },
      { n: "NexusPrime", e: 1180 }
    ].sort((a,b) => b.e - a.e);
    document.getElementById("leaderboard-tbody").innerHTML = rows.map((r, i) => `
      <tr><td>#${i+1}</td><td>${r.n}</td><td>${this.getTier(r.e)}</td><td>${r.e}</td></tr>
    `).join("");
    document.getElementById("history-tbody").innerHTML = (this.profile.history || []).slice(0, 6).map((h) => `
      <tr><td>${h.result}</td><td>${h.opponent}</td><td>${h.faction}</td><td>${h.delta}</td></tr>
    `).join("");
  }

  renderPassAndStore() {
    document.getElementById("pass-xp-val").textContent = String(this.profile.xp);
    document.getElementById("pass-tiers-list").innerHTML = `
      <div class="tier-card"><strong>TIER 1 (100 XP)</strong><p>+300 Credits</p></div>
      <div class="tier-card"><strong>TIER 2 (400 XP)</strong><p>+75 Core Gems</p></div>
      <div class="tier-card"><strong>TIER 3 (800 XP)</strong><p>3D Metallic Foil Shader</p></div>
    `;
    document.getElementById("store-items-grid").innerHTML = `
      <div class="store-card">
        <h3>3D Metallic Foil Deck Upgrade</h3>
        <button class="studio-btn accent-cta" id="btn-buy-foil">${this.profile.foilUnlocked ? "UNLOCKED" : "UNLOCK (500 ◈)"}</button>
      </div>
    `;
    document.getElementById("btn-buy-foil").onclick = () => {
      if (!this.profile.foilUnlocked && this.profile.credits >= 500) {
        this.profile.credits -= 500;
        this.profile.foilUnlocked = true;
        this.saveProfile();
        this.renderPassAndStore();
      }
    };
  }

  log(msg) {
    const d = document.createElement("div");
    d.className = "log-entry";
    d.textContent = msg;
    document.getElementById("combat-log").prepend(d);
  }
}

window.addEventListener("DOMContentLoaded", () => { window.StudioApp = new GameController(); });
"""

# ============================================================================
# 5. GITHUB ACTIONS WORKFLOW — NATIVE ANDROID SDK COMPILER (ZERO GODOT CLI)
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
          echo "Using Build Tools: $BUILD_TOOLS"
          echo "Using Platform JAR: $PLATFORM_JAR"

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
          tag_name: v8.0.${{ github.run_number }}
          name: "Trait Takedown Native Android Release v8.0.${{ github.run_number }}"
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
    write_file(root, "js/renderer3d.js", RENDERER_3D_JS)
    write_file(root, "js/audio.js", AUDIO_JS)
    write_file(root, "js/gameController.js", GAME_CONTROLLER_JS)
    write_file(root, ".github/workflows/native_release.yml", WORKFLOW_YML)
    print("\n[+] Trait Takedown v8.0 Native Android SDK & 3D Engine build ready.")

if __name__ == "__main__":
    build_all()
