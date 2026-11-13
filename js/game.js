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
