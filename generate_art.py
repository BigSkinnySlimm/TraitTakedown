import os
import sys
import time
import urllib.parse
import urllib.request

# =====================================================================
# 1. EXACT GAME PACK & TRAIT DEFINITIONS (SYNCED WITH INDEX.HTML)
# =====================================================================
PACKS = [
    {
        "id": "galactic",
        "theme": "sci-fi space opera character",
        "names": [
            "Darth Malice", "Luke Skyrunner", "Obi-One", "Princess Laya", "Solo Smuggler", "Chew-Barka",
            "Boba Hunter", "Mando Creed", "Yodel Master", "Count Dookey", "General Gremlin", "Mace Purple",
            "Rey Scavenger", "Kylo Tantrum", "Ahsoka Dual", "Palpa-Zap", "Lando Smooth", "Tarkin Grand",
            "Admiral Trap", "Maul Horns", "Qui-Gon Zen", "Padme Royal", "R2-Beep", "C3-Golden"
        ],
        "traits": [
            ("red_blade", "holding a glowing red crimson plasma sword", "no red sword"),
            ("blue_green_blade", "holding a glowing blue or green plasma sword", "no blue sword"),
            ("helmet", "wearing a full enclosed sci-fi combat helmet mask", "bare face visible with no helmet"),
            ("cyborg", "visible metallic robotic cyborg limbs and mechanical parts", "organic body"),
            ("hood", "wearing a dramatic dark mystic hooded cloak over head", "no hood"),
            ("blaster", "aiming a futuristic sci-fi laser pistol blaster", "no gun"),
            ("alien", "exotic non-human alien creature species with colorful skin", "human face")
        ]
    },
    {
        "id": "turtles",
        "theme": "urban martial arts comic character",
        "names": [
            "Leo Blueblade", "Raph Redsai", "Mikey Orange", "Donnie Purplestaff", "Master Whiskers", "April Scoop",
            "Casey Hockey", "Shred-Claw", "Bebop Warthog", "Rocksteady Rhino", "Krang Brain", "Karai Viper",
            "Baxter Fly", "Slash Palm", "Leather Gator", "Metal Turtle", "Mona Lizard", "Rat Sovereign",
            "Usagi Ronin", "Foot Bot", "Mondo Gecko", "Tokka Snapper", "Rahzar Wolf", "Jennika Yellow"
        ],
        "traits": [
            ("shell", "wearing a heavy green armored turtle shell on back", "no turtle shell"),
            ("mask", "wearing a colorful ninja domino eye bandana mask", "no eye bandana"),
            ("mutant", "anthropomorphic mutant animal creature hybrid", "regular human"),
            ("bladed", "holding twin sharp katana ninja blades", "no bladed swords"),
            ("blunt", "holding wooden bo staff or nunchucks", "no wooden staff"),
            ("villain", "menacing dark armored syndicate villain with glowing eyes", "heroic friendly expression"),
            ("human", "human street vigilante character", "non-human creature")
        ]
    },
    {
        "id": "rangers",
        "theme": "tokusatsu super sentai action hero",
        "names": [
            "Red Tyranno", "Green Dragon", "White Tiger", "Pink Pterodactyl", "Blue Tricera", "Black Mammoth",
            "Yellow Saber", "Empress Rita", "Lord Zedd-Chrome", "Goldar Wings", "Alpha-5 Bot", "Zordon Tube",
            "Bulk Prankster", "Skull Laugh", "Silver Space", "Gold Zeo", "Shadow Ranger", "Crimson Thunder",
            "Quantum Rex", "Magna Defender", "Psycho Red", "Scorpina Sting", "Finster Clay", "Ninjor Blue"
        ],
        "traits": [
            ("visor", "wearing a glossy full-face spandex superhero helmet with dark visor", "bare face visible with no helmet"),
            ("sixth", "wearing a gleaming heavy golden dragon chest shield armor", "standard chest suit"),
            ("dino", "prehistoric dinosaur crest motif on suit", "cosmic motif"),
            ("monster", "bizarre theatrical alien monster villain", "sleek hero posture"),
            ("flute", "holding a golden dagger flute weapon", "unarmed pose"),
            ("cape", "wearing a flowing royal cape behind shoulders", "no cape"),
            ("primary_color", "bright vibrant red blue or yellow glossy armor", "dark metallic suit")
        ]
    },
    {
        "id": "sorcery",
        "theme": "magical wizard academy character",
        "names": [
            "Harry Scar", "Ronnie Ginger", "Hermione Tome", "Draco Smirk", "Headmaster Beard", "Professor Potion",
            "Lord No-Nose", "Bellatrix Hex", "Hagrid Giant", "Sirius Hound", "Lupin Moon", "Dobby Sock",
            "Neville Herb", "Luna Spectacles", "Cedric Golden", "McGonagall Cat", "Mad-Eye Goggle", "Lucius Cane",
            "Ginny Bludger", "Fred Prank", "George Joke", "Cho Seeker", "Viktor Broom", "Fleur Charm"
        ],
        "traits": [
            ("serpent", "wearing emerald green and silver serpent house tie and robes", "dark plain robes"),
            ("lion", "wearing crimson red and gold lion house scarf and tie", "no red scarf"),
            ("wand", "holding a glowing wooden magic channeling wand with sparks", "hands empty without wand"),
            ("glasses", "wearing round wire-rimmed eyeglasses on face", "no glasses on face"),
            ("dark_arts", "surrounded by eerie green dark magic smoke and sinister expression", "warm cheerful lighting"),
            ("broom", "holding a polished wooden flying broomstick", "no broomstick"),
            ("staff", "older wise wizard academy professor in ornate robes", "young student apprentice")
        ]
    },
    {
        "id": "pirates",
        "theme": "swashbuckling golden age pirate legend",
        "names": [
            "Capt. Jack Bird", "Davy Tentacle", "Barbossa Apple", "Will Blacksmith", "Lizzie Pirate King", "Norrington Wig",
            "Joshamee Firstmate", "Tia Voodoo", "Bootstrap Barnacle", "Pintel Eye", "Ragetti Wooden", "Blackbeard Smoke",
            "Angelica Saber", "Salazar Ghost", "Cutler East-India", "Cotton Mute", "Jack the Monkey", "Marty Short",
            "Anamaria Helm", "Murtogg Guard", "Mullroy Redcoat", "Sao Feng Bath", "Sri Sumbhajee", "Gentleman Jocard"
        ],
        "traits": [
            ("tricorn", "wearing a weathered leather tricorn pirate hat", "bare head or bandana with no tricorn hat"),
            ("cursed", "ghostly undead sea curse with glowing spectral barnacles", "healthy living skin"),
            ("flintlock", "holding an ornate brass flintlock pirate pistol", "no pistol"),
            ("beard", "thick braided pirate beard on chin", "clean-shaven face with no beard"),
            ("pet", "colorful parrot or small monkey sitting on shoulder", "nothing on shoulder"),
            ("navy", "wearing a crisp blue and gold royal navy officer coat", "ragged pirate shirt"),
            ("compass", "holding a glowing golden magic compass", "no compass")
        ]
    },
    {
        "id": "defenders",
        "theme": "comic book superhero character",
        "names": [
            "Titanium Tony", "Capt. Patriot", "Thor Thunder", "Gamma Smash", "Widow Spy", "Hawk Archer",
            "Spider Kid", "Panther Claw", "Strange Mystic", "Scarlet Chaos", "Vision Android", "Falcon Wings",
            "Winter Cyborg", "Star Bandit", "Groot Twig", "Rocket Trash", "Thanos Chin", "Loki Horns",
            "Ultron Chrome", "Magnet Helmet", "Wolverine Claws", "Deadpool Merc", "Blade Vampire", "Silver Board"
        ],
        "traits": [
            ("armor", "wearing high-tech glowing metallic powered exo-armor suit", "fabric superhero suit"),
            ("cape", "wearing a dramatic flowing superhero cape", "no cape"),
            ("cosmic", "glowing cosmic infinity energy aura around hands", "normal lighting"),
            ("mutant_gene", "glowing mutant eyes or gamma-mutated physique", "standard athletic build"),
            ("shield_hammer", "holding a mighty battle hammer or circular star shield", "empty hands"),
            ("mask_id", "wearing a comic superhero domino mask or full face cowl", "unmasked bare face"),
            ("villain_boss", "imposing comic book supervillain overlord", "noble heroic expression")
        ]
    },
    {
        "id": "critters",
        "theme": "cute 3D elemental pocket monster creature",
        "names": [
            "Spark-Chu", "Flame-Zard", "Hydro-Tortoise", "Bulb-Toad", "Shadow-Gar", "Psychic-Two",
            "Snor-Nap", "Jiggly-Song", "Eevee-Fox", "Gyarados-Serpent", "Dragon-Knight", "Lucario-Aura",
            "Meow-Coin", "Psy-Headache", "Machamp-Four", "Alakazam-Spoons", "Lapras-Ferry", "Ditto-Slime",
            "Arcanine-Blaze", "Scyther-Mantis", "Onix-Boulder", "Pika-Clone", "Mew-Pink", "Lug-Silver"
        ],
        "traits": [
            ("fire_elec", "crackling with bright fire flames and yellow electric sparks", "calm aura"),
            ("water_grass", "surrounded by splashing water bubbles and green vine leaves", "dry surface"),
            ("evolved", "large powerful final-stage evolved monster beast", "small cute baby monster"),
            ("wings", "large feathered or dragon wings spread behind back", "wingless body"),
            ("tail_flame", "glowing crystal gem on forehead and fiery tail tip", "plain forehead"),
            ("legendary", "majestic mythic legendary creature with golden halo aura", "common wild critter"),
            ("biped", "standing upright on two legs", "crouched creature pose")
        ]
    },
    {
        "id": "relic",
        "theme": "high fantasy middle-earth adventurer",
        "names": [
            "Frodo Ringbearer", "Samwise Skillet", "Gandalf Greybeard", "Aragorn Ranger", "Legolas Bow", "Gimli Battleaxe",
            "Boromir Horn", "Gollum Precious", "Saruman White", "Sauron Eye", "Witch-King Crown", "Elrond Half-Elf",
            "Galadriel Mirror", "Eowyn Shieldmaiden", "Faramir Captain", "Pippin Second-Breakfast", "Merry Shire", "Bilbo Burglar",
            "Treebeard Ent", "Lurtz Uruk", "Theoden Horse-Lord", "Arwen Evenstar", "Smaug Hoarder", "Balrog Flame"
        ],
        "traits": [
            ("halfling", "small cheerful shire halfling with curly hair and cloak", "tall warrior"),
            ("immortal", "ethereal pointy-eared elf or glowing ancient wizard", "mortal human"),
            ("beard_helm", "wearing a braided dwarven beard and iron war helmet", "clean-shaven face with no helmet"),
            ("ring_corrupt", "holding a glowing inscribed golden magic ring on chain", "no ring visible"),
            ("sword_bow", "holding a gleaming elven longsword or wooden longbow", "unarmed"),
            ("mordor", "dark armored shadow orc wraith warrior with fiery background", "bright Rivendell lighting"),
            ("royal", "wearing a silver and gold elven or royal king crown", "no crown")
        ]
    },
    {
        "id": "brawlers",
        "theme": "3D anime martial arts super fighter",
        "names": [
            "Goku Kakarot", "Vegeta Prince", "Gohan Scholar", "Piccolo Namek", "Trunks Future-Sword", "Krillin Six-Dot",
            "Frieza Emperor", "Cell Bio-Bug", "Majin Pink-Gum", "Broly Berserk", "Bulma Capsule", "Master Roshi Shell",
            "Android Eighteen", "Android Seventeen", "Yamcha Crater", "Tien Three-Eye", "Beerus Destruction", "Whis Angel",
            "Bardock Headband", "Goten Kid", "Nappa Bald", "Ginyu Pose", "Cooler Metal", "Shenron Wish"
        ],
        "traits": [
            ("golden_hair", "spiky glowing golden super aura hair standing up", "dark or normal hair"),
            ("alien_warrior", "extraterrestrial warrior with tail or alien skin tone", "earth martial artist"),
            ("orange_armor", "wearing a bright orange martial arts gi uniform or battle armor", "dark training clothes"),
            ("energy_beam", "charging a glowing blue plasma energy sphere in hands", "fists clenched without beam"),
            ("villain_form", "sleek menacing bio-android or galactic emperor form", "heroic fighter face"),
            ("bald_antenna", "completely bald shiny head with green antennae", "full head of hair"),
            ("scouter_sword", "wearing a glowing green digital power scouter eyepiece over one eye", "no eyepiece scouter")
        ]
    }
]


def get_character_prompt(pack, idx):
    name = pack["names"][idx]
    traits = pack["traits"]
    pos_descriptions = []
    neg_descriptions = []

    for t_idx, (t_key, pos_desc, neg_desc) in enumerate(traits):
        has_trait = (((idx + 1) * (t_idx + 3) + idx) % 3 == 0) or (idx % len(traits) == t_idx)
        if has_trait:
            pos_descriptions.append(pos_desc)
        else:
            neg_descriptions.append(neg_desc)

    traits_str = ", ".join(pos_descriptions)
    avoid_str = ", ".join(neg_descriptions[:3])

    prompt = (
       f"Original 3D stylized collectible toy bust portrait of an original {pack['theme']} archetype, "

        f"{pack['theme']}, {traits_str}, ({avoid_str}), "
        f"vibrant dramatic rim lighting, expressive face, rich dark studio gradient background, "
        f"Octane render, Unreal Engine 5, centered head and shoulders trading card art, no text, no watermark"
    )
    return prompt


def patch_index_html():
    html_path = "index.html"
    if not os.path.exists(html_path):
        print("⚠️ index.html not found in current folder. Skipping auto-patch.")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    old_line = "char.svg = buildCollectiblePortrait(pack.id, char);"
    new_line = (
        "const rawSvg = buildCollectiblePortrait(pack.id, char);\n"
        "        const b64Svg = 'data:image/svg+xml;utf8,' + encodeURIComponent(rawSvg.trim());\n"
        "        char.svg = `<img src=\"assets/${pack.id}/${idx}.webp\" alt=\"${name}\" "
        "onerror=\"this.onerror=null;this.src='${b64Svg}'\" />`;"
    )

    if "assets/${pack.id}/${idx}.webp" in content:
        print("✅ index.html is already wired to load HD portraits from /assets/!")
        return

    if old_line in content:
        content = content.replace(old_line, new_line)
        old_preview = "const previewSvg = buildCollectiblePortrait(pack.id, previewChar);"
        new_preview = (
            "const rawPrev = buildCollectiblePortrait(pack.id, previewChar);\n"
            "        const b64Prev = 'data:image/svg+xml;utf8,' + encodeURIComponent(rawPrev.trim());\n"
            "        const previewSvg = `<img src=\"assets/${pack.id}/0.webp\" style=\"width:100%;height:100%;object-fit:cover;\" "
            "onerror=\"this.onerror=null;this.src='${b64Prev}'\" />`;"
        )
        content = content.replace(old_preview, new_preview)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Successfully patched index.html to auto-load HD portraits from /assets/!")


def download_portrait(pack_id, idx, prompt, seed):
    out_dir = os.path.join("assets", pack_id)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{idx}.webp")

    # Skip if already generated successfully
    if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
        print(f"  [SKIP] {pack_id}/{idx}.webp already exists.")
        return True

    encoded_prompt = urllib.parse.quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?model=flux&width=512&height=512&seed={seed}&nologo=true"
    )

    for attempt in range(1, 5):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                if len(data) > 5000:
                    with open(out_path, "wb") as f:
                        f.write(data)
                    print(f"  [SAVED] {out_path} ({len(data)//1024} KB)")
                    time.sleep(3) # Crucial rate limit pause
                    return True
        except urllib.error.HTTPError as e:
            if e.code == 402:
                wait = attempt * 8
                print(f"  [RATE LIMIT] Server requested pause. Waiting {wait}s...")
                time.sleep(wait)
            else:
                wait = attempt * 4
                print(f"  [RETRY {attempt}/4] Error {e.code}. Waiting {wait}s...")
                time.sleep(wait)
        except Exception as e:
            wait = attempt * 4
            print(f"  [RETRY {attempt}/4] Connection error. Waiting {wait}s...")
            time.sleep(wait)

    print(f"  [FAILED] Could not generate {out_path} after 4 attempts.")
    return False


def main():
    patch_index_html()
    target_pack = sys.argv[1].lower() if len(sys.argv) > 1 else None

    total_generated = 0
    for p_idx, pack in enumerate(PACKS):
        if target_pack and pack["id"] != target_pack:
            continue

        print(f"\n🎨 Generating Pack: {pack['id'].upper()} (24 Characters)...")
        for c_idx in range(24):
            char_name = pack["names"][c_idx]
            prompt = get_character_prompt(pack, c_idx)
            seed = (p_idx + 1) * 1000 + c_idx * 17
            print(f" -> [{c_idx+1}/24] {char_name}...")
            ok = download_portrait(pack["id"], c_idx, prompt, seed)
            if ok:
                total_generated += 1
            time.sleep(2.5)  # Extended pacing to avoid 402 errors

    print(f"\n🎉 Done! {total_generated} character portraits ready in ./assets/")


if __name__ == "__main__":
    main()
