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
