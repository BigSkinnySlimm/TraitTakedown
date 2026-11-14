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
