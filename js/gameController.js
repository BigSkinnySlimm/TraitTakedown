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
