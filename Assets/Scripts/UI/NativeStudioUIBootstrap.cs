using System.Linq;
using UnityEngine;
using TraitTakedown.Core;
using TraitTakedown.Audio;
using TraitTakedown.Network;
using TraitTakedown.Gameplay;

namespace TraitTakedown.UI
{
    /// <summary>
    /// Automatically initializes the 3D Vulkan/Metal Tabletop Arena, Lighting Rig,
    /// Symphonic DSP Audio Thread, and Native Tactical HUD on application launch.
    /// </summary>
    public class NativeStudioUIBootstrap : MonoBehaviour
    {
        private int _activeModal = 0; // 0=None, 1=Friends, 2=Leaderboard/History, 3=SeasonPass/Armory
        private int _selectedCatIdx = 0;
        private int _selectedValIdx = 0;
        private readonly string[] _categories = { "faction", "species", "armor", "weapon", "element" };
        private string _newFriendInput = "";
        private string _lastLogLine = "Native 3D Engine (Vulkan/Metal) & Auto-Matchmaking Broker initialized.";
        private string _resultBanner = "";

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
        private static void AutoInitializeNativeEngine()
        {
            var engineRoot = new GameObject("TraitTakedown_NativeEngineRoot");
            DontDestroyOnLoad(engineRoot);

            // 1. Camera & Tabletop Perspective Rig
            if (Camera.main == null)
            {
                var camObj = new GameObject("Main Camera");
                camObj.tag = "MainCamera";
                var cam = camObj.AddComponent<Camera>();
                cam.clearFlags = CameraClearFlags.SolidColor;
                cam.backgroundColor = new Color(0.03f, 0.05f, 0.10f);
                cam.fieldOfView = 42f;
                camObj.transform.position = new Vector3(0f, 8.8f, -7.8f);
                camObj.transform.LookAt(new Vector3(0f, 0.2f, 0.3f));
                camObj.AddComponent<AudioListener>();
            }

            // 2. Three-Point Studio PBR Lighting Rig
            var keyLight = new GameObject("DirectionalKeyLight").AddComponent<Light>();
            keyLight.type = LightType.Directional;
            keyLight.intensity = 1.6f;
            keyLight.color = new Color(0.95f, 0.98f, 1.0f);
            keyLight.transform.rotation = Quaternion.Euler(48f, -32f, 0f);

            var rimLight = new GameObject("CyanRimLight").AddComponent<Light>();
            rimLight.type = LightType.Point;
            rimLight.range = 25f;
            rimLight.intensity = 2.4f;
            rimLight.color = new Color(0.0f, 0.9f, 1.0f);
            rimLight.transform.position = new Vector3(-6f, 4f, 5f);

            // 3. Attach Core Native Subsystems
            engineRoot.AddComponent<NativeSymphonicAudioDSP>();
            engineRoot.AddComponent<NativeMatchmakingAndSocialClient>();
            var controller = engineRoot.AddComponent<NativeGameController>();
            var hud = engineRoot.AddComponent<NativeStudioUIBootstrap>();

            controller.OnCombatLogAdded += msg => hud._lastLogLine = msg;
            controller.OnMatchConcluded += (won, text, delta) =>
            {
                hud._resultBanner = $"{(won ? "VICTORY" : "DEFEAT")} ({(delta >= 0 ? "+" : "")}{delta} MMR) — {text}";
            };
        }

        private void OnGUI()
        {
            var ctrl = NativeGameController.Instance;
            var net = NativeMatchmakingAndSocialClient.Instance;
            if (ctrl == null || net == null) return;

            GUI.skin.button.fontStyle = FontStyle.Bold;
            float w = Screen.width;
            float h = Screen.height;

            // TOP NATIVE STUDIO HEADER BAR
            GUI.Box(new Rect(12, 10, w - 24, 54), "");
            GUI.Label(new Rect(26, 16, 360, 24), $"<b>TRAIT TAKEDOWN // NATIVE 3D ENGINE</b>");
            GUI.Label(new Rect(26, 36, 460, 22), $"Callsign: <b>{ctrl.Profile.callsign}</b>  |  {ctrl.GetRankTier(ctrl.Profile.elo)} ({ctrl.Profile.elo} MMR)  |  ◈ {ctrl.Profile.credits}  ❖ {ctrl.Profile.gems}");

            if (GUI.Button(new Rect(w - 690, 18, 175, 36), net.IsSearchingQueue ? "SEARCHING MMR..." : "⚡ FIND RANKED MATCH"))
            {
                if (net.IsSearchingQueue) net.CancelQueue();
                else net.StartAutoMatchmakingQueue(ctrl.Profile.elo);
            }
            if (GUI.Button(new Rect(w - 505, 18, 155, 36), $"👥 FRIENDS ({ctrl.Profile.friends.Count})"))
                _activeModal = _activeModal == 1 ? 0 : 1;
            if (GUI.Button(new Rect(w - 340, 18, 155, 36), "🏆 ELO & HISTORY"))
                _activeModal = _activeModal == 2 ? 0 : 2;
            if (GUI.Button(new Rect(w - 175, 18, 150, 36), "🎖️ PASS & ARMORY"))
                _activeModal = _activeModal == 3 ? 0 : 3;

            // BOTTOM TACTICAL COMMAND CONSOLE
            GUI.Box(new Rect(12, h - 145, w - 24, 135), "");
            string opInfo = ctrl.MySecretUnit != null
                ? $"CLASSIFIED 3D OPERATIVE: <b>{ctrl.MySecretUnit.name}</b> [{ctrl.MySecretUnit.faction} • {ctrl.MySecretUnit.species} • {ctrl.MySecretUnit.armor} • {ctrl.MySecretUnit.weapon} • {ctrl.MySecretUnit.element}]"
                : "STANDBY: Click 'FIND RANKED MATCH' or Challenge a Friend to deploy 3D operatives.";
            GUI.Label(new Rect(26, h - 136, w - 50, 24), opInfo);
            GUI.Label(new Rect(26, h - 112, w - 50, 24), $"TELEMETRY: { _lastLogLine }   |   YOUR SUSPECTS: {ctrl.GetMyRemainingCount()}   |   ENEMY SUSPECTS: {ctrl.OppRemainingUnits}");

            // Trait Scanner & Faction Active Ability Controls
            string currentCat = _categories[_selectedCatIdx % _categories.Length];
            var values = RosterDatabase.Operatives.Select(u => u.GetTraitValue(currentCat)).Distinct().ToList();
            string currentVal = values[_selectedValIdx % values.Count];

            if (GUI.Button(new Rect(26, h - 80, 165, 36), $"TRAIT: {currentCat.ToUpper()}"))
            {
                _selectedCatIdx++;
                _selectedValIdx = 0;
            }
            if (GUI.Button(new Rect(200, h - 80, 185, 36), $"VALUE: {currentVal}"))
            {
                _selectedValIdx++;
            }

            GUI.enabled = ctrl.IsMyTurn && ctrl.ActiveMode != "STANDBY";
            if (GUI.Button(new Rect(395, h - 80, 195, 36), "📡 TRANSMIT SCAN"))
            {
                ctrl.ExecuteTraitInterrogation(currentCat, currentVal);
            }

            GUI.enabled = ctrl.IsMyTurn && ctrl.AbilityReady && ctrl.MySecretUnit != null;
            string abLabel = ctrl.MySecretUnit != null
                ? $"⚡ {RosterDatabase.FactionAbilities[ctrl.MySecretUnit.faction].title}"
                : "⚡ FACTION ULTIMATE";
            if (GUI.Button(new Rect(600, h - 80, 260, 36), abLabel))
            {
                ctrl.ActivateFactionUltimate();
            }

            GUI.enabled = ctrl.IsMyTurn && ctrl.ActiveMode != "STANDBY";
            if (GUI.Button(new Rect(870, h - 80, 215, 36), ctrl.AccuseMode ? "🎯 CLICK 3D UNIT (CANCEL)" : "🎯 LOCK FINAL ACCUSATION"))
            {
                ctrl.AccuseMode = !ctrl.AccuseMode;
            }
            GUI.enabled = true;

            if (!string.IsNullOrEmpty(_resultBanner))
            {
                GUI.Label(new Rect(26, h - 38, w - 50, 24), $"<b>{_resultBanner}</b>");
            }

            RenderActiveModal(w, h, ctrl, net);
        }

        private void RenderActiveModal(float w, float h, NativeGameController ctrl, NativeMatchmakingAndSocialClient net)
        {
            if (_activeModal == 0) return;
            Rect modalRect = new Rect(w * 0.5f - 320, h * 0.5f - 200, 640, 380);
            GUI.Box(modalRect, "");

            if (_activeModal == 1)
            {
                GUI.Label(new Rect(modalRect.x + 20, modalRect.y + 16, 450, 26), "<b>👥 FRIENDS NETWORK & DIRECT CHALLENGES</b>");
                _newFriendInput = GUI.TextField(new Rect(modalRect.x + 20, modalRect.y + 50, 260, 28), _newFriendInput);
                if (GUI.Button(new Rect(modalRect.x + 290, modalRect.y + 50, 140, 28), "+ ADD FRIEND"))
                {
                    if (!string.IsNullOrWhiteSpace(_newFriendInput) && !ctrl.Profile.friends.Contains(_newFriendInput))
                    {
                        ctrl.Profile.friends.Add(_newFriendInput.Trim());
                        ctrl.SaveProfile();
                        _newFriendInput = "";
                    }
                }

                for (int i = 0; i < ctrl.Profile.friends.Count; i++)
                {
                    string fName = ctrl.Profile.friends[i];
                    float rowY = modalRect.y + 95 + i * 38;
                    GUI.Label(new Rect(modalRect.x + 24, rowY, 260, 28), $"● <b>{fName}</b> (ONLINE READY)");
                    if (GUI.Button(new Rect(modalRect.x + 320, rowY, 190, 28), "⚔️ DIRECT CHALLENGE"))
                    {
                        _activeModal = 0;
                        net.SendDirectFriendChallenge(fName, ctrl.Profile.elo);
                    }
                }
            }
            else if (_activeModal == 2)
            {
                GUI.Label(new Rect(modalRect.x + 20, modalRect.y + 16, 520, 26),
                    $"<b>🏆 GLOBAL ELO LEADERBOARD & MATCH ARCHIVE ({ctrl.Profile.wins}W - {ctrl.Profile.losses}L)</b>");
                GUI.Label(new Rect(modalRect.x + 20, modalRect.y + 50, 580, 24),
                    $"#1 Sovereign_Zero (1,680 MMR)  |  #2 Valkyrie_IX (1,540 MMR)  |  YOU: {ctrl.Profile.callsign} ({ctrl.Profile.elo} MMR)");

                for (int i = 0; i < Mathf.Min(6, ctrl.Profile.history.Count); i++)
                {
                    var rec = ctrl.Profile.history[i];
                    GUI.Label(new Rect(modalRect.x + 24, modalRect.y + 90 + i * 28, 580, 24),
                        $"[{rec.result}] vs {rec.opponent}  |  Faction: {rec.faction}  |  MMR Δ: {rec.eloDelta}");
                }
            }
            else if (_activeModal == 3)
            {
                GUI.Label(new Rect(modalRect.x + 20, modalRect.y + 16, 520, 26),
                    $"<b>🎖️ SEASON PASS (XP: {ctrl.Profile.seasonXp}/1200) & 3D ARMORY</b>");
                if (GUI.Button(new Rect(modalRect.x + 20, modalRect.y + 65, 360, 36),
                    ctrl.Profile.foilShaderUnlocked ? "✓ 3D METALLIC FOIL SHADER UNLOCKED" : "UNLOCK 3D FOIL SHADER (500 ◈)"))
                {
                    ctrl.UnlockFoilArmoryUpgrade();
                }
            }

            if (GUI.Button(new Rect(modalRect.xMax - 90, modalRect.y + 12, 75, 28), "CLOSE"))
            {
                _activeModal = 0;
            }
        }
    }
}
