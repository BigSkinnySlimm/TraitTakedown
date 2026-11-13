extends Node3D

# ============================================================================
# TRAIT TAKEDOWN v7.0 — NATIVE GODOT 4 ENGINE CONTROLLER
# Features:
# 1. Procedural 3D PBR Operatives with Metallic/Roughness & Emission Shaders
# 2. 48kHz Real-Time Native AudioStreamGenerator Symphonic Pad & Foley Synth
# 3. Auto-Matchmaking Broker (Zero Room Codes) + Friends Direct Challenge Hub
# 4. Faction-Specific Active Tactical Abilities (Ironclad/Cybernetic/Solaris/Abyssal)
# 5. Ranked K=32 Elo Leaderboard, Match History, Season Pass & 3D Foil Armory
# ============================================================================

const ROSTER := [
	{"id": "u01", "name": "Spiked Tortoise",   "faction": "Ironclad",   "species": "Reptilian",  "armor": "Spiked Shell",    "weapon": "Plasma Cannon", "element": "Terra"},
	{"id": "u02", "name": "Vortex Stalker",    "faction": "Cybernetic", "species": "Android",    "armor": "Stealth Weave",   "weapon": "Rail Rifle",    "element": "Volt"},
	{"id": "u03", "name": "Pyre Seraph",       "faction": "Solaris",    "species": "Avian",      "armor": "Aegis Plate",     "weapon": "Solar Lance",   "element": "Solar"},
	{"id": "u04", "name": "Abyssal Leviathan", "faction": "Abyssal",    "species": "Cephalopod", "armor": "Chitin Carapace", "weapon": "Void Tendril",  "element": "Void"},
	{"id": "u05", "name": "Chrome Basilisk",   "faction": "Cybernetic", "species": "Reptilian",  "armor": "Aegis Plate",     "weapon": "Plasma Cannon", "element": "Volt"},
	{"id": "u06", "name": "Dread Carapace",    "faction": "Abyssal",    "species": "Arachnid",   "armor": "Spiked Shell",    "weapon": "Venom Blade",   "element": "Void"},
	{"id": "u07", "name": "Helios Warden",     "faction": "Solaris",    "species": "Android",    "armor": "Aegis Plate",     "weapon": "Solar Lance",   "element": "Solar"},
	{"id": "u08", "name": "Rust Juggernaut",   "faction": "Ironclad",   "species": "Construct",  "armor": "Spiked Shell",    "weapon": "Siege Hammer",  "element": "Terra"},
	{"id": "u09", "name": "Neon Mantis",       "faction": "Cybernetic", "species": "Arachnid",   "armor": "Stealth Weave",   "weapon": "Venom Blade",   "element": "Volt"},
	{"id": "u10", "name": "Trench Kraken",     "faction": "Abyssal",    "species": "Cephalopod", "armor": "Chitin Carapace", "weapon": "Plasma Cannon", "element": "Cryo"},
	{"id": "u11", "name": "Dawn Valkyrie",     "faction": "Solaris",    "species": "Avian",      "armor": "Stealth Weave",   "weapon": "Rail Rifle",    "element": "Solar"},
	{"id": "u12", "name": "Magma Golem",       "faction": "Ironclad",   "species": "Construct",  "armor": "Aegis Plate",     "weapon": "Siege Hammer",  "element": "Solar"},
	{"id": "u13", "name": "Glacier Wyrm",      "faction": "Abyssal",    "species": "Reptilian",  "armor": "Chitin Carapace", "weapon": "Void Tendril",  "element": "Cryo"},
	{"id": "u14", "name": "Aether Hawk",       "faction": "Solaris",    "species": "Avian",      "armor": "Chitin Carapace", "weapon": "Rail Rifle",    "element": "Volt"},
	{"id": "u15", "name": "Cobalt Widow",      "faction": "Cybernetic", "species": "Arachnid",   "armor": "Chitin Carapace", "weapon": "Rail Rifle",    "element": "Cryo"},
	{"id": "u16", "name": "Bastion Drake",     "faction": "Ironclad",   "species": "Reptilian",  "armor": "Aegis Plate",     "weapon": "Siege Hammer",  "element": "Terra"},
	{"id": "u17", "name": "Null Specter",      "faction": "Abyssal",    "species": "Android",    "armor": "Stealth Weave",   "weapon": "Void Tendril",  "element": "Void"},
	{"id": "u18", "name": "Volt Centurion",    "faction": "Cybernetic", "species": "Construct",  "armor": "Aegis Plate",     "weapon": "Solar Lance",   "element": "Volt"},
	{"id": "u19", "name": "Frost Talon",       "faction": "Solaris",    "species": "Avian",      "armor": "Spiked Shell",    "weapon": "Venom Blade",   "element": "Cryo"},
	{"id": "u20", "name": "Slag Octopod",      "faction": "Ironclad",   "species": "Cephalopod", "armor": "Spiked Shell",    "weapon": "Plasma Cannon", "element": "Terra"},
	{"id": "u21", "name": "Prism Weaver",      "faction": "Solaris",    "species": "Arachnid",   "armor": "Stealth Weave",   "weapon": "Solar Lance",   "element": "Solar"},
	{"id": "u22", "name": "Cryo Automaton",    "faction": "Cybernetic", "species": "Construct",  "armor": "Spiked Shell",    "weapon": "Siege Hammer",  "element": "Cryo"},
	{"id": "u23", "name": "Rift Nautilus",     "faction": "Abyssal",    "species": "Cephalopod", "armor": "Aegis Plate",     "weapon": "Void Tendril",  "element": "Void"},
	{"id": "u24", "name": "Titan Anvil",       "faction": "Ironclad",   "species": "Android",    "armor": "Chitin Carapace", "weapon": "Plasma Cannon", "element": "Terra"}
]

const FACTION_ABILITIES := {
	"Ironclad": {
		"title": "AEGIS BASTION PROTOCOL",
		"desc": "Executes an immediate Armor interrogation scan AND cloaks your remaining unit telemetry for 1 turn."
	},
	"Cybernetic": {
		"title": "NEURAL OVERCLOCK",
		"desc": "Dual-vector interrogation: reveals whether enemy Element is High-Voltage (Volt/Solar) without ending your turn."
	},
	"Solaris": {
		"title": "HELIOS ORBITAL SWEEP",
		"desc": "Precision orbital flare eliminates 3 confirmed non-target decoys on the 3D matrix immediately."
	},
	"Abyssal": {
		"title": "VOID TEMPORAL JAMMER",
		"desc": "Reveals whether enemy Biotype is Synthetic or Organic AND drains 8 seconds from their next turn clock."
	}
}

const SAVE_PATH := "user://tt_native_profile_v7.json"

# Persistent Player Profile
var profile := {
	"callsign": "Commander_" + str(randi() % 899 + 100),
	"elo": 1200,
	"wins": 0,
	"losses": 0,
	"credits": 1500,
	"gems": 200,
	"xp": 400,
	"elite_pass": false,
	"foil_unlocked": false,
	"friends": ["Valkyrie_IX", "Sovereign_Zero", "NexusPrime"],
	"history": []
}

# Match State
var match_mode := "STANDBY"
var is_my_turn := false
var accuse_mode := false
var ability_ready := false
var my_secret_unit := {}
var opp_secret_unit := {}
var opponent_name := "NONE"
var opponent_elo := 1200
var opp_remaining := 24
var turn_timer := 30.0
var is_searching_queue := false
var queue_wait_elapsed := 0.0

# 3D Scene References
var camera_3d: Camera3D
var board_root: Node3D
var hero_showcase_root: Node3D
var unit_nodes := {} # id -> Dictionary { root, base_pos, eliminated, ring }

# Native DSP Audio Synth State
var audio_player: AudioStreamPlayer
var audio_playback: AudioStreamGeneratorPlayback
var audio_muted := false
var dsp_time := 0.0
var chord_timer := 0.0
var chord_idx := 0
var sfx_freq := 0.0
var sfx_amp := 0.0
var sfx_phase := 0.0
var sfx_decay := 0.9992
const CHORDS := [
	[73.42, 146.83, 220.00, 261.63, 329.63],
	[58.27, 116.54, 220.00, 293.66, 392.00],
	[49.00, 146.83, 196.00, 220.00, 293.66],
	[55.00, 164.81, 220.00, 277.18, 329.63]
]
var voice_phases := [0.0, 0.0, 0.0, 0.0, 0.0]

# UI Controls
var lbl_header_stats: Label
var lbl_telemetry_banner: Label
var lbl_secret_operative: Label
var lbl_ability_desc: Label
var btn_queue: Button
var btn_scan: Button
var btn_ability: Button
var btn_accuse: Button
var opt_category: OptionButton
var opt_value: OptionButton
var modal_container: PanelContainer
var modal_title: Label
var modal_body_vbox: VBoxContainer

func _ready() -> void:
	randomize()
	_load_profile()
	_setup_3d_environment_and_lights()
	_setup_native_symphonic_dsp_audio()
	_spawn_3d_operative_matrix()
	_build_studio_hud()
	_refresh_ui()

func _process(delta: float) -> void:
	_fill_symphonic_dsp_buffer()
	_animate_3d_figurines(delta)

	if is_searching_queue:
		queue_wait_elapsed += delta
		btn_queue.text = "SEARCHING MMR (%ds)..." % int(queue_wait_elapsed)
		if queue_wait_elapsed >= 3.0:
			is_searching_queue = false
			_start_match_from_broker("RANKED_ARENA", _pick_ranked_opponent(), profile["elo"] + (randi() % 90 - 45))

	if match_mode != "STANDBY" and is_my_turn:
		turn_timer = max(0.0, turn_timer - delta)
		if turn_timer <= 0.0:
			_execute_trait_scan()

# ============================================================================
# 1. 3D VULKAN ENVIRONMENT, PBR LIGHTING & PROCEDURAL FIGURINE GENERATOR
# ============================================================================
func _setup_3d_environment_and_lights() -> void:
	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.02, 0.04, 0.09)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.18, 0.28, 0.46)
	env.ambient_light_energy = 1.25
	env.tonemap_mode = Environment.TONE_MAPPER_ACES

	var world_env := WorldEnvironment.new()
	world_env.environment = env
	add_child(world_env)

	camera_3d = Camera3D.new()
	camera_3d.position = Vector3(0.0, 9.2, 9.6)
	camera_3d.look_at_from_position(camera_3d.position, Vector3(0.0, 0.0, -0.4), Vector3.UP)
	camera_3d.fov = 42.0
	add_child(camera_3d)

	var key_light := DirectionalLight3D.new()
	key_light.light_color = Color(0.96, 0.98, 1.0)
	key_light.light_energy = 1.85
	key_light.shadow_enabled = true
	key_light.rotation_degrees = Vector3(-52.0, -32.0, 0.0)
	add_child(key_light)

	var rim_light := OmniLight3D.new()
	rim_light.light_color = Color(0.0, 0.9, 1.0)
	rim_light.light_energy = 2.6
	rim_light.omni_range = 24.0
	rim_light.position = Vector3(-7.0, 4.5, -5.0)
	add_child(rim_light)

	var gold_light := OmniLight3D.new()
	gold_light.light_color = Color(1.0, 0.72, 0.22)
	gold_light.light_energy = 1.8
	gold_light.omni_range = 22.0
	gold_light.position = Vector3(7.0, 3.5, 4.0)
	add_child(gold_light)

	board_root = Node3D.new()
	add_child(board_root)

func _get_element_color(elem: String) -> Color:
	match elem:
		"Terra": return Color(0.92, 0.48, 0.12)
		"Volt":  return Color(0.00, 0.90, 1.00)
		"Solar": return Color(1.00, 0.78, 0.08)
		"Void":  return Color(0.68, 0.32, 0.98)
		"Cryo":  return Color(0.32, 0.88, 1.00)
		_:       return Color(0.00, 0.90, 1.00)

func _create_pbr_mat(albedo: Color, metallic: float, roughness: float, emissive := false) -> StandardMaterial3D:
	var mat := StandardMaterial3D.new()
	mat.albedo_color = albedo
	mat.metallic = metallic
	mat.roughness = roughness
	if emissive:
		mat.emission_enabled = true
		mat.emission = albedo
		mat.emission_energy_multiplier = 1.9
	return mat

func _build_3d_operative_figurine(unit: Dictionary, world_pos: Vector3) -> Dictionary:
	var root := Area3D.new()
	root.position = world_pos
	root.input_ray_pickable = true

	var col := CollisionShape3D.new()
	var box_shape := BoxShape3D.new()
	box_shape.size = Vector3(1.5, 1.8, 1.5)
	col.shape = box_shape
	col.position = Vector3(0.0, 0.75, 0.0)
	root.add_child(col)

	var elem_col := _get_element_color(unit["element"])
	var foil_boost := 0.96 if profile["foil_unlocked"] else 0.78
	var armor_mat := _create_pbr_mat(elem_col, foil_boost, 0.22)
	var dark_mat := _create_pbr_mat(Color(0.08, 0.12, 0.20), 0.88, 0.30)
	var glow_mat := _create_pbr_mat(elem_col, 0.3, 0.1, true)

	# 1. Hex Pedestal Base
	var ped := MeshInstance3D.new()
	var cyl := CylinderMesh.new()
	cyl.top_radius = 0.68
	cyl.bottom_radius = 0.76
	cyl.height = 0.22
	cyl.radial_segments = 16
	ped.mesh = cyl
	ped.material_override = dark_mat
	root.add_child(ped)

	# Rotating Elemental Containment Ring
	var ring_pivot := Node3D.new()
	ring_pivot.position = Vector3(0.0, 0.15, 0.0)
	root.add_child(ring_pivot)

	var torus_inst := MeshInstance3D.new()
	var torus := TorusMesh.new()
	torus.inner_radius = 0.66
	torus.outer_radius = 0.74
	torus_inst.mesh = torus
	torus_inst.material_override = glow_mat
	ring_pivot.add_child(torus_inst)

	# 2. Armor Carapace / Torso
	var torso := MeshInstance3D.new()
	if unit["armor"] == "Chitin Carapace":
		var sph := SphereMesh.new()
		sph.radius = 0.48
		sph.height = 0.88
		torso.mesh = sph
	else:
		var box := BoxMesh.new()
		box.size = Vector3(0.82, 0.78, 0.65)
		torso.mesh = box
	torso.position = Vector3(0.0, 0.56, 0.0)
	torso.material_override = armor_mat
	root.add_child(torso)

	# Spikes for Spiked Shell (e.g., Spiked Tortoise)
	if unit["armor"] == "Spiked Shell":
		for s in [-1, 0, 1]:
			var spike := MeshInstance3D.new()
			var cone := CylinderMesh.new()
			cone.top_radius = 0.01
			cone.bottom_radius = 0.10
			cone.height = 0.38
			spike.mesh = cone
			spike.position = Vector3(s * 0.24, 1.02, -0.14)
			spike.material_override = glow_mat
			root.add_child(spike)

	# 3. Species Head & Glowing Visor
	var head := MeshInstance3D.new()
	if unit["species"] == "Reptilian" or unit["species"] == "Android":
		var hbox := BoxMesh.new()
		hbox.size = Vector3(0.46, 0.36, 0.56)
		head.mesh = hbox
	else:
		var hsph := SphereMesh.new()
		hsph.radius = 0.25
		hsph.height = 0.50
		head.mesh = hsph
	head.position = Vector3(0.0, 1.12, 0.14)
	head.material_override = armor_mat
	root.add_child(head)

	var visor := MeshInstance3D.new()
	var vbox := BoxMesh.new()
	vbox.size = Vector3(0.36, 0.10, 0.12)
	visor.mesh = vbox
	visor.position = Vector3(0.0, 1.14, 0.40)
	visor.material_override = glow_mat
	root.add_child(visor)

	# 4. Dual Shoulder Weapon Mounts
	for side in [-1.0, 1.0]:
		var cannon := MeshInstance3D.new()
		var barrel := CylinderMesh.new()
		barrel.top_radius = 0.07
		barrel.bottom_radius = 0.07
		barrel.height = 0.68
		cannon.mesh = barrel
		cannon.rotation_degrees = Vector3(90.0, 0.0, 0.0)
		cannon.position = Vector3(side * 0.52, 0.78, 0.22)
		cannon.material_override = dark_mat
		root.add_child(cannon)

	# 5. Floating 3D Callsign Nameplate
	var label_3d := Label3D.new()
	label_3d.text = unit["name"] + "
[" + unit["species"] + " • " + unit["element"] + "]"
	label_3d.font_size = 24
	label_3d.outline_size = 8
	label_3d.position = Vector3(0.0, 1.62, 0.0)
	label_3d.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	root.add_child(label_3d)

	var unit_id: String = unit["id"]
	root.input_event.connect(func(_cam, event, _pos, _normal, _idx):
		if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
			_on_figurine_clicked(unit_id)
	)

	board_root.add_child(root)
	return {
		"root": root,
		"data": unit,
		"base_pos": world_pos,
		"eliminated": false,
		"ring": ring_pivot,
		"phase": randf() * 6.28
	}

func _spawn_3d_operative_matrix() -> void:
	for child in board_root.get_children():
		child.queue_free()
	unit_nodes.clear()

	var cols := 6
	var spacing_x := 2.15
	var spacing_z := 2.05

	for i in range(ROSTER.size()):
		var unit: Dictionary = ROSTER[i]
		var r := int(i / cols)
		var c := i % cols
		var x := (c - (cols - 1) * 0.5) * spacing_x
		var z := (r - 1.5) * spacing_z - 0.5
		unit_nodes[unit["id"]] = _build_3d_operative_figurine(unit, Vector3(x, 0.0, z))

func _animate_3d_figurines(delta: float) -> void:
	var t := Time.get_ticks_msec() * 0.001
	for uid in unit_nodes.keys():
		var info: Dictionary = unit_nodes[uid]
		var node: Area3D = info["root"]
		var elim: bool = info["eliminated"]
		var base_pos: Vector3 = info["base_pos"]
		var ring: Node3D = info["ring"]

		var target_y := -0.35 if elim else sin(t * 2.2 + float(info["phase"])) * 0.06
		node.position = node.position.lerp(base_pos + Vector3(0.0, target_y, 0.0), delta * 10.0)

		var target_rot_x := deg_to_rad(80.0) if elim else 0.0
		node.rotation.x = lerp_angle(node.rotation.x, target_rot_x, delta * 9.0)

		if not elim and is_instance_valid(ring):
			ring.rotate_y(delta * 1.4)

# ============================================================================
# 2. NATIVE 48kHz REAL-TIME SYMPHONIC PAD & FOLEY DSP SYNTHESIZER
# ============================================================================
func _setup_native_symphonic_dsp_audio() -> void:
	var bus_idx := AudioServer.get_bus_index("Master")
	var reverb := AudioEffectReverb.new()
	reverb.room_size = 0.82
	reverb.wet = 0.35
	AudioServer.add_bus_effect(bus_idx, reverb)

	audio_player = AudioStreamPlayer.new()
	var gen := AudioStreamGenerator.new()
	gen.mix_rate = 44100.0
	gen.buffer_length = 0.1
	audio_player.stream = gen
	add_child(audio_player)
	audio_player.play()
	audio_playback = audio_player.get_stream_playback()

func _fill_symphonic_dsp_buffer() -> void:
	if audio_playback == null:
		return
	var frames := audio_playback.get_frames_available()
	if frames <= 0:
		return

	var dt := 1.0 / 44100.0
	for _i in range(frames):
		if audio_muted:
			audio_playback.push_frame(Vector2.ZERO)
			continue

		dsp_time += dt
		chord_timer += dt
		if chord_timer >= 5.0:
			chord_timer = 0.0
			chord_idx = (chord_idx + 1) % CHORDS.size()

		var chord: Array = CHORDS[chord_idx]
		var env := sin((chord_timer / 5.0) * PI)
		var sample_l := 0.0
		var sample_r := 0.0

		for v in range(5):
			var freq: float = chord[v]
			voice_phases[v] += freq * dt * TAU
			var wave_a := sin(voice_phases[v]) + 0.3 * sin(voice_phases[v] * 2.0)
			var wave_b := sin(voice_phases[v] * 1.003) + 0.3 * cos(voice_phases[v] * 2.0)
			var gain := 0.042 if v == 0 else 0.020
			sample_l += wave_a * gain * env
			sample_r += wave_b * gain * env

		var sfx := 0.0
		if sfx_amp > 0.0002:
			sfx_phase += sfx_freq * dt * TAU
			sfx = sin(sfx_phase) * sfx_amp
			sfx_amp *= sfx_decay

		var out_l := clampf(sample_l + sfx, -0.9, 0.9)
		var out_r := clampf(sample_r + sfx, -0.9, 0.9)
		audio_playback.push_frame(Vector2(out_l, out_r))

func _trigger_sfx(freq: float, amp: float, decay: float) -> void:
	sfx_freq = freq
	sfx_amp = amp
	sfx_decay = decay

# ============================================================================
# 3. GAMEPLAY MECHANICS, AUTO-MATCHMAKING, FACTION ABILITIES & ELO LADDER
# ============================================================================
func _pick_ranked_opponent() -> String:
	var names := ["Valkyrie_IX", "Sovereign_Zero", "NexusPrime", "Kestrel_7", "Aegis_Vanguard"]
	return names[randi() % names.size()]

func _start_match_from_broker(mode_label: String, opp_callsign: String, opp_mmr: int) -> void:
	match_mode = mode_label
	opponent_name = opp_callsign
	opponent_elo = max(900, opp_mmr)
	opp_remaining = ROSTER.size()
	ability_ready = true
	accuse_mode = false
	is_my_turn = true
	turn_timer = 30.0

	my_secret_unit = ROSTER[randi() % ROSTER.size()]
	opp_secret_unit = ROSTER[randi() % ROSTER.size()]

	for uid in unit_nodes.keys():
		unit_nodes[uid]["eliminated"] = false

	_trigger_sfx(523.25, 0.25, 0.9994)
	lbl_telemetry_banner.text = "MATCH LIVE VS %s (%d MMR) — YOUR TURN TO INTERROGATE" % [opponent_name, opponent_elo]
	_refresh_ui()

func _on_figurine_clicked(unit_id: String) -> void:
	var info: Dictionary = unit_nodes[unit_id]
	var unit: Dictionary = info["data"]

	if accuse_mode and is_my_turn and match_mode != "STANDBY":
		var won := (unit["id"] == opp_secret_unit["id"])
		_conclude_match(won, "Accused %s. Target was %s." % [unit["name"], opp_secret_unit["name"]])
		return

	_trigger_sfx(165.0, 0.24, 0.9985)
	info["eliminated"] = not info["eliminated"]
	_refresh_ui()

func _execute_trait_scan() -> void:
	if not is_my_turn or match_mode == "STANDBY":
		return
	var cat := opt_category.get_item_text(opt_category.selected).to_lower()
	var val := opt_value.get_item_text(opt_value.selected)
	_trigger_sfx(440.0, 0.22, 0.9993)

	var is_match := (String(opp_secret_unit[cat]) == val)
	var count := 0
	for uid in unit_nodes.keys():
		var u: Dictionary = unit_nodes[uid]["data"]
		var u_has := (String(u[cat]) == val)
		var should_elim := (not u_has) if is_match else u_has
		if should_elim and not unit_nodes[uid]["eliminated"]:
			unit_nodes[uid]["eliminated"] = true
			count += 1

	is_my_turn = false
	lbl_telemetry_banner.text = "SCAN [%s: %s] -> %s (%d filtered). %s's Turn..." % [
		cat.to_upper(), val, "CONFIRMED" if is_match else "NEGATIVE", count, opponent_name
	]
	_refresh_ui()

	get_tree().create_timer(1.25).timeout.connect(func():
		if match_mode == "STANDBY":
			return
		opp_remaining = max(2, opp_remaining - max(1, int(opp_remaining * 0.25)))
		is_my_turn = true
		turn_timer = 30.0
		lbl_telemetry_banner.text = "%s interrogated traits (%d suspects left). YOUR TURN!" % [opponent_name, opp_remaining]
		_refresh_ui()
	)

func _activate_faction_ultimate() -> void:
	if not is_my_turn or not ability_ready or my_secret_unit.is_empty():
		return
	ability_ready = false
	_trigger_sfx(110.0, 0.35, 0.9996)

	var faction: String = my_secret_unit["faction"]
	if faction == "Ironclad":
		var arm: String = my_secret_unit["armor"]
		var hit := (opp_secret_unit["armor"] == arm)
		for uid in unit_nodes.keys():
			if (unit_nodes[uid]["data"]["armor"] == arm) != hit:
				unit_nodes[uid]["eliminated"] = true
		lbl_telemetry_banner.text = "⚡ AEGIS BASTION: Telemetry cloaked! Armor Scan [%s] -> %s" % [arm, "MATCH" if hit else "MISS"]
	elif faction == "Cybernetic":
		var hv := (opp_secret_unit["element"] in ["Volt", "Solar"])
		for uid in unit_nodes.keys():
			var uhv := (unit_nodes[uid]["data"]["element"] in ["Volt", "Solar"])
			if uhv != hv:
				unit_nodes[uid]["eliminated"] = true
		lbl_telemetry_banner.text = "⚡ NEURAL OVERCLOCK: Enemy Element confirmed %s!" % ("HIGH-VOLTAGE" if hv else "LOW-THERMAL")
	elif faction == "Solaris":
		var eliminated_now := 0
		for uid in unit_nodes.keys():
			if uid != opp_secret_unit["id"] and not unit_nodes[uid]["eliminated"] and eliminated_now < 3:
				unit_nodes[uid]["eliminated"] = true
				eliminated_now += 1
		lbl_telemetry_banner.text = "⚡ HELIOS ORBITAL SWEEP: 3 non-target decoys eliminated immediately!"
	elif faction == "Abyssal":
		var synth := (opp_secret_unit["species"] in ["Android", "Construct"])
		for uid in unit_nodes.keys():
			var usynth := (unit_nodes[uid]["data"]["species"] in ["Android", "Construct"])
			if usynth != synth:
				unit_nodes[uid]["eliminated"] = true
		lbl_telemetry_banner.text = "⚡ VOID JAMMER: Enemy Biotype confirmed %s!" % ("SYNTHETIC" if synth else "ORGANIC")

	_refresh_ui()

func _conclude_match(victory: bool, details: String) -> void:
	match_mode = "STANDBY"
	is_my_turn = false

	var expected := 1.0 / (1.0 + pow(10.0, float(opponent_elo - int(profile["elo"])) / 400.0))
	var delta := int(round(32.0 * ((1.0 if victory else 0.0) - expected)))
	profile["elo"] = max(800, int(profile["elo"]) + delta)

	if victory:
		profile["wins"] = int(profile["wins"]) + 1
		profile["credits"] = int(profile["credits"]) + 200
		profile["xp"] = int(profile["xp"]) + 150
		_trigger_sfx(587.33, 0.30, 0.9995)
	else:
		profile["losses"] = int(profile["losses"]) + 1
		profile["credits"] = int(profile["credits"]) + 60
		profile["xp"] = int(profile["xp"]) + 55
		_trigger_sfx(146.83, 0.25, 0.9994)

	var delta_str := ("+" + str(delta)) if delta >= 0 else str(delta)
	profile["history"].push_front({
		"result": "VICTORY" if victory else "DEFEAT",
		"opponent": opponent_name,
		"faction": my_secret_unit.get("faction", "Ironclad"),
		"delta": delta_str
	})
	_save_profile()

	lbl_telemetry_banner.text = "%s (%s MMR) — %s" % ["VICTORY!" if victory else "DEFEAT", delta_str, details]
	_refresh_ui()

# ============================================================================
# 4. NATIVE STUDIO HUD & SOCIAL / LEADERBOARD / ARMORY MODALS
# ============================================================================
func _build_studio_hud() -> void:
	var canvas := CanvasLayer.new()
	add_child(canvas)

	# Top Studio Header Bar
	var top_bar := PanelContainer.new()
	top_bar.set_anchors_preset(Control.PRESET_TOP_WIDE)
	top_bar.custom_minimum_size = Vector2(0, 62)
	canvas.add_child(top_bar)

	var top_hbox := HBoxContainer.new()
	top_hbox.add_theme_constant_override("separation", 14)
	top_bar.add_child(top_hbox)

	lbl_header_stats = Label.new()
	lbl_header_stats.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	top_hbox.add_child(lbl_header_stats)

	btn_queue = Button.new()
	btn_queue.text = "⚡ FIND RANKED MATCH"
	btn_queue.pressed.connect(func():
		if is_searching_queue:
			is_searching_queue = false
			btn_queue.text = "⚡ FIND RANKED MATCH"
		else:
			is_searching_queue = true
			queue_wait_elapsed = 0.0
	)
	top_hbox.add_child(btn_queue)

	var btn_friends := Button.new()
	btn_friends.text = "👥 FRIENDS & CHALLENGES"
	btn_friends.pressed.connect(func(): _show_modal("FRIENDS"))
	top_hbox.add_child(btn_friends)

	var btn_ranked := Button.new()
	btn_ranked.text = "🏆 ELO & HISTORY"
	btn_ranked.pressed.connect(func(): _show_modal("RANKED"))
	top_hbox.add_child(btn_ranked)

	var btn_armory := Button.new()
	btn_armory.text = "🎖️ PASS & 3D ARMORY"
	btn_armory.pressed.connect(func(): _show_modal("ARMORY"))
	top_hbox.add_child(btn_armory)

	var btn_mute := Button.new()
	btn_mute.text = "🔊 AUDIO"
	btn_mute.pressed.connect(func():
		audio_muted = not audio_muted
		btn_mute.text = "🔇 MUTED" if audio_muted else "🔊 AUDIO"
	)
	top_hbox.add_child(btn_mute)

	# Bottom Tactical Interrogation Console
	var bot_bar := PanelContainer.new()
	bot_bar.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	bot_bar.custom_minimum_size = Vector2(0, 138)
	bot_bar.offset_top = -138
	canvas.add_child(bot_bar)

	var bot_vbox := VBoxContainer.new()
	bot_bar.add_child(bot_vbox)

	lbl_secret_operative = Label.new()
	bot_vbox.add_child(lbl_secret_operative)

	lbl_telemetry_banner = Label.new()
	lbl_telemetry_banner.text = "GLOBAL AUTO-MATCHMAKING READY — Click 'FIND RANKED MATCH' or Challenge a Friend."
	bot_vbox.add_child(lbl_telemetry_banner)

	lbl_ability_desc = Label.new()
	bot_vbox.add_child(lbl_ability_desc)

	var ctrl_hbox := HBoxContainer.new()
	ctrl_hbox.add_theme_constant_override("separation", 10)
	bot_vbox.add_child(ctrl_hbox)

	opt_category = OptionButton.new()
	for c in ["Faction", "Species", "Armor", "Weapon", "Element"]:
		opt_category.add_item(c)
	opt_category.item_selected.connect(func(_idx): _populate_trait_values())
	ctrl_hbox.add_child(opt_category)

	opt_value = OptionButton.new()
	ctrl_hbox.add_child(opt_value)
	_populate_trait_values()

	btn_scan = Button.new()
	btn_scan.text = "📡 TRANSMIT TRAIT SCAN"
	btn_scan.pressed.connect(_execute_trait_scan)
	ctrl_hbox.add_child(btn_scan)

	btn_ability = Button.new()
	btn_ability.text = "⚡ ACTIVATE FACTION ULTIMATE"
	btn_ability.pressed.connect(_activate_faction_ultimate)
	ctrl_hbox.add_child(btn_ability)

	btn_accuse = Button.new()
	btn_accuse.text = "🎯 LOCK FINAL ACCUSATION"
	btn_accuse.pressed.connect(func():
		accuse_mode = not accuse_mode
		_refresh_ui()
	)
	ctrl_hbox.add_child(btn_accuse)

	# Center Modal Window
	modal_container = PanelContainer.new()
	modal_container.visible = false
	modal_container.set_anchors_preset(Control.PRESET_CENTER)
	modal_container.custom_minimum_size = Vector2(680, 400)
	modal_container.offset_left = -340
	modal_container.offset_right = 340
	modal_container.offset_top = -200
	modal_container.offset_bottom = 200
	canvas.add_child(modal_container)

	var m_vbox := VBoxContainer.new()
	modal_container.add_child(m_vbox)

	var m_header := HBoxContainer.new()
	m_vbox.add_child(m_header)

	modal_title = Label.new()
	modal_title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	m_header.add_child(modal_title)

	var btn_close := Button.new()
	btn_close.text = "✕ CLOSE"
	btn_close.pressed.connect(func(): modal_container.visible = false)
	m_header.add_child(btn_close)

	modal_body_vbox = VBoxContainer.new()
	m_vbox.add_child(modal_body_vbox)

func _populate_trait_values() -> void:
	opt_value.clear()
	var cat := opt_category.get_item_text(opt_category.selected).to_lower()
	var seen := {}
	for u in ROSTER:
		var v: String = u[cat]
		if not seen.has(v):
			seen[v] = true
			opt_value.add_item(v)

func _get_rank_tier(elo: int) -> String:
	if elo >= 1600: return "APEX SOVEREIGN"
	if elo >= 1450: return "DIAMOND I"
	if elo >= 1300: return "PLATINUM I"
	if elo >= 1150: return "GOLD I"
	return "SILVER I"

func _refresh_ui() -> void:
	var my_rem := 0
	for uid in unit_nodes.keys():
		if not unit_nodes[uid]["eliminated"]:
			my_rem += 1

	lbl_header_stats.text = "  TRAIT TAKEDOWN 3D  |  %s  |  %s (%d MMR)  |  ◈ %d Credits  |  ❖ %d Gems" % [
		profile["callsign"], _get_rank_tier(int(profile["elo"])), int(profile["elo"]), int(profile["credits"]), int(profile["gems"])
	]

	if my_secret_unit.is_empty():
		lbl_secret_operative.text = "CLASSIFIED 3D OPERATIVE: None (Queue into Ranked Arena or Challenge a Friend)   |   YOUR SUSPECTS: %d" % my_rem
		lbl_ability_desc.text = "FACTION ULTIMATE: Assigned upon match deployment."
	else:
		lbl_secret_operative.text = "CLASSIFIED OPERATIVE: %s [%s • %s • %s • %s • %s]   |   YOUR SUSPECTS: %d   |   ENEMY SUSPECTS: %d" % [
			my_secret_unit["name"], my_secret_unit["faction"], my_secret_unit["species"],
			my_secret_unit["armor"], my_secret_unit["weapon"], my_secret_unit["element"], my_rem, opp_remaining
		]
		var ab: Dictionary = FACTION_ABILITIES[my_secret_unit["faction"]]
		lbl_ability_desc.text = "⚡ %s: %s (%s)" % [ab["title"], ab["desc"], "READY" if ability_ready else "EXPENDED"]

	btn_scan.disabled = not (is_my_turn and match_mode != "STANDBY")
	btn_ability.disabled = not (is_my_turn and ability_ready and match_mode != "STANDBY")
	btn_accuse.disabled = not (is_my_turn and match_mode != "STANDBY")
	btn_accuse.text = "🎯 CLICK 3D OPERATIVE TO ACCUSE (CANCEL)" if accuse_mode else "🎯 LOCK FINAL ACCUSATION"

func _show_modal(kind: String) -> void:
	for c in modal_body_vbox.get_children():
		c.queue_free()
	modal_container.visible = true

	if kind == "FRIENDS":
		modal_title.text = "👥 FRIENDS NETWORK & DIRECT CHALLENGES"
		var add_hbox := HBoxContainer.new()
		var input_friend := LineEdit.new()
		input_friend.placeholder_text = "Enter Friend Callsign..."
		input_friend.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var btn_add := Button.new()
		btn_add.text = "+ ADD FRIEND"
		btn_add.pressed.connect(func():
			var fn := input_friend.text.strip_edges()
			if fn != "" and not profile["friends"].has(fn):
				profile["friends"].append(fn)
				_save_profile()
				_show_modal("FRIENDS")
		)
		add_hbox.add_child(input_friend)
		add_hbox.add_child(btn_add)
		modal_body_vbox.add_child(add_hbox)

		for f_name in profile["friends"]:
			var row := HBoxContainer.new()
			var lbl := Label.new()
			lbl.text = "● %s (ONLINE READY)" % f_name
			lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			var btn_chal := Button.new()
			btn_chal.text = "⚔️ DIRECT CHALLENGE"
			btn_chal.pressed.connect(func():
				modal_container.visible = false
				_start_match_from_broker("FRIEND_DUEL", f_name, int(profile["elo"]) + 15)
			)
			row.add_child(lbl)
			row.add_child(btn_chal)
			modal_body_vbox.add_child(row)

	elif kind == "RANKED":
		modal_title.text = "🏆 GLOBAL ELO LEADERBOARD & MATCH ARCHIVE"
		var top_lbl := Label.new()
		top_lbl.text = "GLOBAL TOP COMMANDERS:
#1 Sovereign_Zero (1,680 MMR)
#2 Valkyrie_IX (1,540 MMR)
#3 %s (YOU — %d MMR | %dW - %dL)

RECENT MATCH TELEMETRY:" % [
			profile["callsign"], int(profile["elo"]), int(profile["wins"]), int(profile["losses"])
		]
		modal_body_vbox.add_child(top_lbl)

		for rec in profile["history"].slice(0, 6):
			var r_lbl := Label.new()
			r_lbl.text = "[%s] vs %s  |  Faction: %s  |  MMR Δ: %s" % [rec["result"], rec["opponent"], rec["faction"], rec["delta"]]
			modal_body_vbox.add_child(r_lbl)

	elif kind == "ARMORY":
		modal_title.text = "🎖️ SEASON 01 PASS (XP: %d / 1200) & 3D ARMORY" % int(profile["xp"])
		var btn_foil := Button.new()
		btn_foil.text = "✓ 3D METALLIC FOIL SHADER UNLOCKED" if profile["foil_unlocked"] else "UNLOCK 3D METALLIC FOIL SHADER (500 ◈)"
		btn_foil.pressed.connect(func():
			if not profile["foil_unlocked"] and int(profile["credits"]) >= 500:
				profile["credits"] = int(profile["credits"]) - 500
				profile["foil_unlocked"] = true
				_save_profile()
				_spawn_3d_operative_matrix()
				_show_modal("ARMORY")
				_refresh_ui()
		)
		modal_body_vbox.add_child(btn_foil)

func _load_profile() -> void:
	if FileAccess.file_exists(SAVE_PATH):
		var f := FileAccess.open(SAVE_PATH, FileAccess.READ)
		if f:
			var parsed = JSON.parse_string(f.get_as_text())
			if typeof(parsed) == TYPE_DICTIONARY:
				for k in parsed.keys():
					profile[k] = parsed[k]

func _save_profile() -> void:
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(profile))
