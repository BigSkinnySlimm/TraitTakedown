using System;
using System.Collections.Generic;
using UnityEngine;

namespace TraitTakedown.Core
{
    [Serializable]
    public class OperativeData
    {
        public string id;
        public string name;
        public string faction;
        public string species;
        public string armor;
        public string weapon;
        public string element;

        public OperativeData(string id, string name, string faction, string species, string armor, string weapon, string element)
        {
            this.id = id;
            this.name = name;
            this.faction = faction;
            this.species = species;
            this.armor = armor;
            this.weapon = weapon;
            this.element = element;
        }

        public string GetTraitValue(string category)
        {
            switch (category.ToLowerInvariant())
            {
                case "faction": return faction;
                case "species": return species;
                case "armor": return armor;
                case "weapon": return weapon;
                case "element": return element;
                default: return faction;
            }
        }
    }

    [Serializable]
    public class FactionAbilitySpec
    {
        public string faction;
        public string title;
        public string description;
    }

    public static class RosterDatabase
    {
        public static readonly List<OperativeData> Operatives = new List<OperativeData>
        {
            new OperativeData("u01", "Spiked Tortoise",   "Ironclad",   "Reptilian",  "Spiked Shell",    "Plasma Cannon", "Terra"),
            new OperativeData("u02", "Vortex Stalker",    "Cybernetic", "Android",    "Stealth Weave",   "Rail Rifle",    "Volt"),
            new OperativeData("u03", "Pyre Seraph",       "Solaris",    "Avian",      "Aegis Plate",     "Solar Lance",   "Solar"),
            new OperativeData("u04", "Abyssal Leviathan", "Abyssal",    "Cephalopod", "Chitin Carapace", "Void Tendril",  "Void"),
            new OperativeData("u05", "Chrome Basilisk",   "Cybernetic", "Reptilian",  "Aegis Plate",     "Plasma Cannon", "Volt"),
            new OperativeData("u06", "Dread Carapace",    "Abyssal",    "Arachnid",   "Spiked Shell",    "Venom Blade",   "Void"),
            new OperativeData("u07", "Helios Warden",     "Solaris",    "Android",    "Aegis Plate",     "Solar Lance",   "Solar"),
            new OperativeData("u08", "Rust Juggernaut",   "Ironclad",   "Construct",  "Spiked Shell",    "Siege Hammer",  "Terra"),
            new OperativeData("u09", "Neon Mantis",       "Cybernetic", "Arachnid",   "Stealth Weave",   "Venom Blade",   "Volt"),
            new OperativeData("u10", "Trench Kraken",     "Abyssal",    "Cephalopod", "Chitin Carapace", "Plasma Cannon", "Cryo"),
            new OperativeData("u11", "Dawn Valkyrie",     "Solaris",    "Avian",      "Stealth Weave",   "Rail Rifle",    "Solar"),
            new OperativeData("u12", "Magma Golem",       "Ironclad",   "Construct",  "Aegis Plate",     "Siege Hammer",  "Solar"),
            new OperativeData("u13", "Glacier Wyrm",      "Abyssal",    "Reptilian",  "Chitin Carapace", "Void Tendril",  "Cryo"),
            new OperativeData("u14", "Aether Hawk",       "Solaris",    "Avian",      "Chitin Carapace", "Rail Rifle",    "Volt"),
            new OperativeData("u15", "Cobalt Widow",      "Cybernetic", "Arachnid",   "Chitin Carapace", "Rail Rifle",    "Cryo"),
            new OperativeData("u16", "Bastion Drake",     "Ironclad",   "Reptilian",  "Aegis Plate",     "Siege Hammer",  "Terra"),
            new OperativeData("u17", "Null Specter",      "Abyssal",    "Android",    "Stealth Weave",   "Void Tendril",  "Void"),
            new OperativeData("u18", "Volt Centurion",    "Cybernetic", "Construct",  "Aegis Plate",     "Solar Lance",   "Volt"),
            new OperativeData("u19", "Frost Talon",       "Solaris",    "Avian",      "Spiked Shell",    "Venom Blade",   "Cryo"),
            new OperativeData("u20", "Slag Octopod",      "Ironclad",   "Cephalopod", "Spiked Shell",    "Plasma Cannon", "Terra"),
            new OperativeData("u21", "Prism Weaver",      "Solaris",    "Arachnid",   "Stealth Weave",   "Solar Lance",   "Solar"),
            new OperativeData("u22", "Cryo Automaton",    "Cybernetic", "Construct",  "Spiked Shell",    "Siege Hammer",  "Cryo"),
            new OperativeData("u23", "Rift Nautilus",     "Abyssal",    "Cephalopod", "Aegis Plate",     "Void Tendril",  "Void"),
            new OperativeData("u24", "Titan Anvil",       "Ironclad",   "Android",    "Chitin Carapace", "Plasma Cannon", "Terra")
        };

        public static readonly Dictionary<string, FactionAbilitySpec> FactionAbilities = new Dictionary<string, FactionAbilitySpec>
        {
            {
                "Ironclad", new FactionAbilitySpec
                {
                    faction = "Ironclad",
                    title = "AEGIS BASTION PROTOCOL",
                    description = "Executes a free Armor interrogation scan AND cloaks your remaining unit telemetry for 1 turn."
                }
            },
            {
                "Cybernetic", new FactionAbilitySpec
                {
                    faction = "Cybernetic",
                    title = "NEURAL OVERCLOCK",
                    description = "Dual-vector scan: reveals whether enemy Element is High-Voltage (Volt/Solar) without ending your turn."
                }
            },
            {
                "Solaris", new FactionAbilitySpec
                {
                    faction = "Solaris",
                    title = "HELIOS ORBITAL SWEEP",
                    description = "Precision orbital flare eliminates 3 confirmed non-target decoys on the 3D board immediately."
                }
            },
            {
                "Abyssal", new FactionAbilitySpec
                {
                    faction = "Abyssal",
                    title = "VOID TEMPORAL JAMMER",
                    description = "Reveals whether enemy Biotype is Synthetic or Organic AND drains 8 seconds from their next turn clock."
                }
            }
        };

        public static Color GetElementPrimaryColor(string element)
        {
            switch (element)
            {
                case "Terra": return new Color(0.90f, 0.49f, 0.13f);
                case "Volt":  return new Color(0.00f, 0.90f, 1.00f);
                case "Solar": return new Color(1.00f, 0.76f, 0.05f);
                case "Void":  return new Color(0.65f, 0.35f, 0.95f);
                case "Cryo":  return new Color(0.30f, 0.86f, 0.98f);
                default:      return new Color(0.00f, 0.90f, 1.00f);
            }
        }
    }
}
