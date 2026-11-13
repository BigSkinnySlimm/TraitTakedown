using System;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using TraitTakedown.Core;
using TraitTakedown.Graphics;
using TraitTakedown.Audio;
using TraitTakedown.Network;

namespace TraitTakedown.Gameplay
{
    [Serializable]
    public class MatchHistoryRecord
    {
        public string result;
        public string opponent;
        public string faction;
        public string eloDelta;
    }

    [Serializable]
    public class PlayerProfileData
    {
        public string callsign = "Commander_77";
        public int elo = 1200;
        public int wins = 0;
        public int losses = 0;
        public int credits = 1500;
        public int gems = 200;
        public int seasonXp = 400;
        public bool elitePassUnlocked = false;
        public bool foilShaderUnlocked = false;
        public List<string> friends = new List<string> { "Valkyrie_IX", "NexusPrime", "Sovereign_Zero" };
        public List<MatchHistoryRecord> history = new List<MatchHistoryRecord>();
    }

    public class NativeGameController : MonoBehaviour
    {
        public static NativeGameController Instance { get; private set; }

        public PlayerProfileData Profile { get; private set; }
        public OperativeData MySecretUnit { get; private set; }
        public OperativeData OppSecretUnit { get; private set; }

        public string ActiveMode { get; private set; } = "STANDBY";
        public string OpponentName { get; private set; } = "NONE";
        public int OpponentElo { get; private set; } = 1200;
        public bool IsMyTurn { get; private set; }
        public bool AccuseMode { get; set; }
        public bool AbilityReady { get; private set; }
        public int OppRemainingUnits { get; private set; } = 24;
        public float TurnTimeRemaining { get; private set; } = 30f;

        public event Action OnStateUpdated;
        public event Action<string> OnCombatLogAdded;
        public event Action<bool, string, int> OnMatchConcluded;

        private readonly Dictionary<string, CardPhysicsBody> _boardCards = new Dictionary<string, CardPhysicsBody>();
        private Transform _boardRoot;

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }
            Instance = this;
            LoadProfile();
        }

        private void Start()
        {
            Spawn3DTabletopMatrix();
            if (NativeMatchmakingAndSocialClient.Instance != null)
            {
                NativeMatchmakingAndSocialClient.Instance.SetCallsign(Profile.callsign);
                NativeMatchmakingAndSocialClient.Instance.OnMatchPaired += StartNativeMatch;
            }
        }

        private void Update()
        {
            Handle3DMouseAndTouchRaycasting();

            if (ActiveMode != "STANDBY" && IsMyTurn)
            {
                TurnTimeRemaining -= Time.deltaTime;
                if (TurnTimeRemaining <= 0f)
                {
                    ExecuteTraitInterrogation("faction", MySecretUnit.faction);
                }
            }
        }

        public void LoadProfile()
        {
            string json = PlayerPrefs.GetString("TT_NATIVE_PROFILE_V6", "");
            if (!string.IsNullOrEmpty(json))
            {
                try { Profile = JsonUtility.FromJson<PlayerProfileData>(json); }
                catch { Profile = new PlayerProfileData(); }
            }
            else
            {
                Profile = new PlayerProfileData
                {
                    callsign = $"Commander_{UnityEngine.Random.Range(100, 999)}"
                };
            }
        }

        public void SaveProfile()
        {
            PlayerPrefs.SetString("TT_NATIVE_PROFILE_V6", JsonUtility.ToJson(Profile));
            PlayerPrefs.Save();
            OnStateUpdated?.Invoke();
        }

        public void Spawn3DTabletopMatrix()
        {
            if (_boardRoot != null) Destroy(_boardRoot.gameObject);
            _boardRoot = new GameObject("Tabletop3DMatrix").transform;
            _boardCards.Clear();

            // 6 columns x 4 rows 3D spatial grid
            int cols = 6;
            float spacingX = 2.05f;
            float spacingZ = 2.15f;

            for (int i = 0; i < RosterDatabase.Operatives.Count; i++)
            {
                var unit = RosterDatabase.Operatives[i];
                int r = i / cols;
                int c = i % cols;
                float x = (c - (cols - 1) * 0.5f) * spacingX;
                float z = (1.5f - r) * spacingZ;

                var cardBody = Native3DFigurineGenerator.SpawnOperative3DFigurine(unit, new Vector3(x, 0f, z), _boardRoot);
                cardBody.ApplyFoilShaderBoost(Profile.foilShaderUnlocked);
                _boardCards[unit.id] = cardBody;
            }
        }

        private void Handle3DMouseAndTouchRaycasting()
        {
            if (Camera.main == null) return;
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
            bool hitAny = Physics.Raycast(ray, out RaycastHit hit, 100f);

            foreach (var kv in _boardCards)
            {
                bool hovered = hitAny && hit.collider != null && hit.collider.transform == kv.Value.transform;
                kv.Value.IsHovered = hovered;

                if (hovered && Input.GetMouseButtonDown(0))
                {
                    On3DFigurineClicked(kv.Value);
                }
            }
        }

        private void On3DFigurineClicked(CardPhysicsBody body)
        {
            if (AccuseMode && IsMyTurn && ActiveMode != "STANDBY")
            {
                bool won = body.UnitData.id == OppSecretUnit.id;
                ConcludeMatch(won, $"Final accusation locked on {body.UnitData.name}. Enemy operative was {OppSecretUnit.name}.");
                return;
            }

            NativeSymphonicAudioDSP.Instance?.PlayCardFlipFoley();
            body.SetEliminated(!body.IsEliminated);
            OnStateUpdated?.Invoke();
        }

        public void StartNativeMatch(MatchPairingResult pairing)
        {
            ActiveMode = pairing.mode;
            OpponentName = pairing.opponentCallsign;
            OpponentElo = pairing.opponentElo;
            OppRemainingUnits = RosterDatabase.Operatives.Count;
            AbilityReady = true;
            AccuseMode = false;
            IsMyTurn = pairing.isHost;
            TurnTimeRemaining = 30f;

            MySecretUnit = RosterDatabase.Operatives[UnityEngine.Random.Range(0, RosterDatabase.Operatives.Count)];
            OppSecretUnit = RosterDatabase.Operatives[UnityEngine.Random.Range(0, RosterDatabase.Operatives.Count)];

            foreach (var kv in _boardCards)
            {
                kv.Value.SetEliminated(false);
            }

            NativeSymphonicAudioDSP.Instance?.PlayRadarScanFoley();
            LogCombat($"Matched vs {OpponentName} ({OpponentElo} MMR). Assigned 3D Operative: {MySecretUnit.name} [{MySecretUnit.faction}].");
            OnStateUpdated?.Invoke();
        }

        public void ExecuteTraitInterrogation(string category, string value)
        {
            if (!IsMyTurn || ActiveMode == "STANDBY") return;
            NativeSymphonicAudioDSP.Instance?.PlayRadarScanFoley();

            bool isMatch = OppSecretUnit.GetTraitValue(category) == value;
            int eliminatedCount = 0;

            foreach (var unit in RosterDatabase.Operatives)
            {
                bool unitHas = unit.GetTraitValue(category) == value;
                bool shouldEliminate = isMatch ? !unitHas : unitHas;
                if (shouldEliminate && !_boardCards[unit.id].IsEliminated)
                {
                    _boardCards[unit.id].SetEliminated(true);
                    eliminatedCount++;
                }
            }

            LogCombat($"Interrogation [{category.ToUpper()}: {value}] -> {(isMatch ? "CONFIRMED" : "NEGATIVE")} ({eliminatedCount} units eliminated).");
            IsMyTurn = false;
            TurnTimeRemaining = 30f;
            OnStateUpdated?.Invoke();

            Invoke(nameof(SimulateOpponentTurn), 1.35f);
        }

        public void ActivateFactionUltimate()
        {
            if (!IsMyTurn || !AbilityReady || MySecretUnit == null) return;
            AbilityReady = false;
            NativeSymphonicAudioDSP.Instance?.PlayAbilityUltimateBoom();

            string faction = MySecretUnit.faction;
            if (faction == "Ironclad")
            {
                string armorVal = MySecretUnit.armor;
                bool match = OppSecretUnit.armor == armorVal;
                LogCombat($"⚡ AEGIS BASTION: Telemetry cloaked! Bonus Armor Scan [{armorVal}] -> {(match ? "MATCH" : "MISS")}.");
                foreach (var u in RosterDatabase.Operatives)
                {
                    if ((u.armor == armorVal) != match) _boardCards[u.id].SetEliminated(true);
                }
            }
            else if (faction == "Cybernetic")
            {
                bool highVolt = OppSecretUnit.element == "Volt" || OppSecretUnit.element == "Solar";
                LogCombat($"⚡ NEURAL OVERCLOCK: Enemy Element is {(highVolt ? "HIGH-VOLTAGE (Volt/Solar)" : "LOW-THERMAL (Terra/Void/Cryo)")}!");
                foreach (var u in RosterDatabase.Operatives)
                {
                    bool uHigh = u.element == "Volt" || u.element == "Solar";
                    if (uHigh != highVolt) _boardCards[u.id].SetEliminated(true);
                }
            }
            else if (faction == "Solaris")
            {
                var decoys = RosterDatabase.Operatives
                    .Where(u => u.id != OppSecretUnit.id && !_boardCards[u.id].IsEliminated)
                    .Take(3)
                    .ToList();
                foreach (var d in decoys) _boardCards[d.id].SetEliminated(true);
                LogCombat("⚡ HELIOS ORBITAL SWEEP: 3 confirmed non-target decoys eliminated immediately!");
            }
            else if (faction == "Abyssal")
            {
                bool isSynth = OppSecretUnit.species == "Android" || OppSecretUnit.species == "Construct";
                LogCombat($"⚡ VOID JAMMER: Enemy Biotype is {(isSynth ? "SYNTHETIC" : "ORGANIC")}! Enemy turn clock drained.");
                foreach (var u in RosterDatabase.Operatives)
                {
                    bool uSynth = u.species == "Android" || u.species == "Construct";
                    if (uSynth != isSynth) _boardCards[u.id].SetEliminated(true);
                }
            }

            OnStateUpdated?.Invoke();
        }

        private void SimulateOpponentTurn()
        {
            if (ActiveMode == "STANDBY") return;
            int cut = Mathf.Max(1, Mathf.RoundToInt(OppRemainingUnits * 0.25f));
            OppRemainingUnits = Mathf.Max(2, OppRemainingUnits - cut);
            LogCombat($"{OpponentName} executed trait scan ({OppRemainingUnits} suspects remaining).");

            IsMyTurn = true;
            TurnTimeRemaining = 30f;
            OnStateUpdated?.Invoke();
        }

        public int GetMyRemainingCount()
        {
            return _boardCards.Values.Count(c => !c.IsEliminated);
        }

        public string GetRankTier(int elo)
        {
            if (elo >= 1600) return "APEX SOVEREIGN";
            if (elo >= 1450) return "DIAMOND I";
            if (elo >= 1300) return "PLATINUM I";
            if (elo >= 1150) return "GOLD I";
            return "SILVER I";
        }

        private void ConcludeMatch(bool victory, string summary)
        {
            ActiveMode = "STANDBY";
            IsMyTurn = false;

            double expected = 1.0 / (1.0 + Math.Pow(10.0, (OpponentElo - Profile.elo) / 400.0));
            int delta = Mathf.RoundToInt(32f * ((victory ? 1f : 0f) - (float)expected));
            Profile.elo = Mathf.Max(800, Profile.elo + delta);

            if (victory)
            {
                Profile.wins++;
                Profile.credits += 200;
                Profile.seasonXp += 150;
                NativeSymphonicAudioDSP.Instance?.PlayAbilityUltimateBoom();
            }
            else
            {
                Profile.losses++;
                Profile.credits += 60;
                Profile.seasonXp += 55;
            }

            Profile.history.Insert(0, new MatchHistoryRecord
            {
                result = victory ? "VICTORY" : "DEFEAT",
                opponent = OpponentName,
                faction = MySecretUnit != null ? MySecretUnit.faction : "Ironclad",
                eloDelta = delta >= 0 ? $"+{delta}" : $"{delta}"
            });

            SaveProfile();
            OnMatchConcluded?.Invoke(victory, summary, delta);
        }

        public void UnlockFoilArmoryUpgrade()
        {
            if (Profile.credits >= 500 && !Profile.foilShaderUnlocked)
            {
                Profile.credits -= 500;
                Profile.foilShaderUnlocked = true;
                foreach (var c in _boardCards.Values) c.ApplyFoilShaderBoost(true);
                SaveProfile();
            }
        }

        private void LogCombat(string message)
        {
            OnCombatLogAdded?.Invoke(message);
        }
    }
}
