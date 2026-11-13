using UnityEngine;
using TraitTakedown.Core;

namespace TraitTakedown.Graphics
{
    /// <summary>
    /// Hardware-accelerated 3D Hooke's Law Spring Physics & Elimination Flip Controller
    /// </summary>
    public class CardPhysicsBody : MonoBehaviour
    {
        public OperativeData UnitData { get; private set; }
        public bool IsEliminated { get; private set; }
        public bool IsHovered { get; set; }

        private Vector3 _basePosition;
        private Quaternion _targetRotation = Quaternion.identity;
        private Transform _energyRing;
        private Renderer[] _renderers;
        private float _bobSeed;

        public void Initialize(OperativeData data, Vector3 worldPos, Transform energyRing)
        {
            UnitData = data;
            _basePosition = worldPos;
            _energyRing = energyRing;
            _renderers = GetComponentsInChildren<Renderer>();
            _bobSeed = Random.Range(0f, 10f);
        }

        public void SetEliminated(bool eliminated)
        {
            IsEliminated = eliminated;
            _targetRotation = eliminated
                ? Quaternion.Euler(82f, 0f, 0f)
                : Quaternion.identity;
        }

        public void ApplyFoilShaderBoost(bool unlocked)
        {
            if (_renderers == null) return;
            foreach (var r in _renderers)
            {
                if (r.material != null && r.material.HasProperty("_Metallic"))
                {
                    r.material.SetFloat("_Metallic", unlocked ? 0.95f : 0.75f);
                    r.material.SetFloat("_Smoothness", unlocked ? 0.92f : 0.68f);
                }
            }
        }

        private void Update()
        {
            float dt = Time.deltaTime;
            float hoverLift = (IsHovered && !IsEliminated) ? 0.42f : 0f;
            float idleWave = IsEliminated ? -0.18f : Mathf.Sin(Time.time * 2.2f + _bobSeed) * 0.04f;

            Vector3 targetPos = _basePosition + new Vector3(0f, hoverLift + idleWave, 0f);
            transform.position = Vector3.Lerp(transform.position, targetPos, dt * 12f);

            Quaternion hoverTilt = (IsHovered && !IsEliminated)
                ? Quaternion.Euler(-10f, Mathf.Sin(Time.time * 4f) * 8f, 0f)
                : _targetRotation;

            transform.rotation = Quaternion.Slerp(transform.rotation, hoverTilt, dt * 10f);

            if (_energyRing != null && !IsEliminated)
            {
                _energyRing.Rotate(Vector3.up, dt * 75f, Space.Self);
            }
        }
    }

    /// <summary>
    /// Procedural 3D PBR Figurine Builder (Vulkan / Metal Native GPU Pipeline)
    /// </summary>
    public static class Native3DFigurineGenerator
    {
        private static Shader _cachedShader;

        private static Shader GetPBRShader()
        {
            if (_cachedShader == null)
            {
                _cachedShader = Shader.Find("Universal Render Pipeline/Lit");
                if (_cachedShader == null) _cachedShader = Shader.Find("Standard");
            }
            return _cachedShader;
        }

        public static Material CreatePBRMaterial(Color albedo, float metallic, float smoothness, Color emission = default)
        {
            var mat = new Material(GetPBRShader());
            mat.color = albedo;
            if (mat.HasProperty("_Metallic")) mat.SetFloat("_Metallic", metallic);
            if (mat.HasProperty("_Smoothness")) mat.SetFloat("_Smoothness", smoothness);
            if (mat.HasProperty("_Glossiness")) mat.SetFloat("_Glossiness", smoothness);

            if (emission != default)
            {
                mat.EnableKeyword("_EMISSION");
                if (mat.HasProperty("_EmissionColor"))
                {
                    mat.SetColor("_EmissionColor", emission * 1.8f);
                }
            }
            return mat;
        }

        public static CardPhysicsBody SpawnOperative3DFigurine(OperativeData unit, Vector3 position, Transform parent)
        {
            var root = new GameObject($"Figurine_{unit.id}_{unit.name}");
            root.transform.SetParent(parent, false);
            root.transform.position = position;

            Color elemColor = RosterDatabase.GetElementPrimaryColor(unit.element);
            Material armorMat = CreatePBRMaterial(elemColor, 0.78f, 0.72f);
            Material obsidianMat = CreatePBRMaterial(new Color(0.09f, 0.13f, 0.22f), 0.88f, 0.65f);
            Material glowMat = CreatePBRMaterial(elemColor, 0.35f, 0.90f, elemColor);

            // 1. Tactical Hex Pedestal Base
            var pedestal = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            pedestal.transform.SetParent(root.transform, false);
            pedestal.transform.localPosition = new Vector3(0f, 0f, 0f);
            pedestal.transform.localScale = new Vector3(1.25f, 0.12f, 1.25f);
            pedestal.GetComponent<Renderer>().material = obsidianMat;

            // Rotating Elemental Containment Ring
            var ringPivot = new GameObject("EnergyRing").transform;
            ringPivot.SetParent(root.transform, false);
            ringPivot.localPosition = new Vector3(0f, 0.15f, 0f);
            for (int i = 0; i < 4; i++)
            {
                var node = GameObject.CreatePrimitive(PrimitiveType.Cube);
                node.transform.SetParent(ringPivot, false);
                float angle = i * Mathf.PI * 0.5f;
                node.transform.localPosition = new Vector3(Mathf.Cos(angle) * 0.65f, 0f, Mathf.Sin(angle) * 0.65f);
                node.transform.localScale = new Vector3(0.14f, 0.06f, 0.14f);
                node.GetComponent<Renderer>().material = glowMat;
                Object.Destroy(node.GetComponent<Collider>());
            }

            // 2. Armor Carapace / Torso Sculpture
            GameObject torso = GameObject.CreatePrimitive(
                unit.armor == "Chitin Carapace" ? PrimitiveType.Sphere : PrimitiveType.Cube
            );
            torso.transform.SetParent(root.transform, false);
            torso.transform.localPosition = new Vector3(0f, 0.55f, 0f);
            torso.transform.localScale = unit.armor == "Spiked Shell"
                ? new Vector3(0.95f, 0.65f, 1.05f)
                : new Vector3(0.78f, 0.82f, 0.58f);
            torso.GetComponent<Renderer>().material = armorMat;
            Object.Destroy(torso.GetComponent<Collider>());

            // Dorsal Spikes for Spiked Shell (e.g. Spiked Tortoise)
            if (unit.armor == "Spiked Shell")
            {
                for (int s = -1; s <= 1; s++)
                {
                    var spike = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
                    spike.transform.SetParent(root.transform, false);
                    spike.transform.localPosition = new Vector3(s * 0.26f, 0.92f, -0.15f);
                    spike.transform.localScale = new Vector3(0.12f, 0.25f, 0.12f);
                    spike.transform.localRotation = Quaternion.Euler(-22f, 0f, s * -12f);
                    spike.GetComponent<Renderer>().material = glowMat;
                    Object.Destroy(spike.GetComponent<Collider>());
                }
            }

            // 3. Species Head Geometry
            var head = GameObject.CreatePrimitive(
                unit.species == "Reptilian" || unit.species == "Android" ? PrimitiveType.Cube : PrimitiveType.Sphere
            );
            head.transform.SetParent(root.transform, false);
            head.transform.localPosition = new Vector3(0f, 1.12f, 0.18f);
            head.transform.localScale = unit.species == "Reptilian"
                ? new Vector3(0.46f, 0.34f, 0.58f)
                : new Vector3(0.42f, 0.42f, 0.42f);
            head.GetComponent<Renderer>().material = armorMat;
            Object.Destroy(head.GetComponent<Collider>());

            // Glowing Visor / Eyes
            var visor = GameObject.CreatePrimitive(PrimitiveType.Cube);
            visor.transform.SetParent(head.transform, false);
            visor.transform.localPosition = new Vector3(0f, 0.1f, 0.48f);
            visor.transform.localScale = new Vector3(0.75f, 0.24f, 0.18f);
            visor.GetComponent<Renderer>().material = glowMat;
            Object.Destroy(visor.GetComponent<Collider>());

            // 4. Primary Weapon Mounts
            var weaponL = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            weaponL.transform.SetParent(root.transform, false);
            weaponL.transform.localPosition = new Vector3(-0.56f, 0.78f, 0.22f);
            weaponL.transform.localRotation = Quaternion.Euler(90f, 0f, 0f);
            weaponL.transform.localScale = new Vector3(0.14f, 0.48f, 0.14f);
            weaponL.GetComponent<Renderer>().material = obsidianMat;
            Object.Destroy(weaponL.GetComponent<Collider>());

            var weaponR = Object.Instantiate(weaponL, root.transform);
            weaponR.transform.localPosition = new Vector3(0.56f, 0.78f, 0.22f);

            // Unified Selection BoxCollider for Physics Raycasting
            var box = root.AddComponent<BoxCollider>();
            box.center = new Vector3(0f, 0.65f, 0f);
            box.size = new Vector3(1.35f, 1.45f, 1.35f);

            var body = root.AddComponent<CardPhysicsBody>();
            body.Initialize(unit, position, ringPivot);
            return body;
        }
    }
}
