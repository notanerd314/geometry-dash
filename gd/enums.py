"""
# .entities.enums

A module containing all enumerations of various things.
"""

from enum import IntEnum, Enum, StrEnum, auto
from typing import Literal, Union

# Literals
SpecialLevel = Literal["DAILY", "WEEKLY", "EVENT"]
ChestType = Literal["SMALL", "LARGE"]
Folders = Literal[
    "Aquatic Sounds",
    "Underwater",
    "Construction and Demolition",
    "Creatures",
    "Alien Insect",
    "Animals",
    "Beasts",
    "Feral Beast",
    "Savage Beast",
    "Big Monster",
    "Earth Elemental",
    "Effects",
    "Fantasy Giant",
    "Fire Elemental",
    "Ghost",
    "Giant Ogre",
    "Goblin",
    "Goblin Demon",
    "Humanoids",
    "Ice Elemental",
    "Monsters",
    "Orc",
    "Robotic",
    "Robotic Creature 01",
    "Small Creatures",
    "Small Monster",
    "Undead",
    "Various",
    "Zombie",
    "Environmental",
    "Ice",
    "Events and Fanfares",
    "Retro",
    "Scary",
    "Explosions and Destruction",
    "Sci-Fi",
    "Underwater",
    "Fire and Flames",
    "Footsteps",
    "Impacts and Hits",
    "Cinematic",
    "Dark",
    "Metal",
    "Organic Impacts",
    "Interface",
    "Alerts and Notifications",
    "Alarms",
    "Errors",
    "Hi-Tech",
    "Simple",
    "Bells and Chimes",
    "Buttons and Clicks",
    "Drums and Percussion",
    "Geometry Dash",
    "Humorous",
    "Other",
    "Retro",
    "Swipes and Wind",
    "UI Actions",
    "Locations",
    "Pirate Ship",
    "Spaceship",
    "Ambiance",
    "Engine and Drones",
    "Witches Hut",
    "Machines and Robotics",
    "Robots",
    "Melodic Stingers",
    "Casual",
    "Music Kits",
    "Cybernetic Rave",
    "Loops",
    "Atmosphere",
    "Bass",
    "Drum Perc",
    "Melodic Reese Pad",
    "Melodic Synth",
    "One Shots",
    "Bass",
    "Drum Perc",
    "Claps",
    "Crashes",
    "HiHats",
    "Kicks",
    "Percussion",
    "Rides",
    "Snares",
    "Synth",
    "Vocal",
    "Fire Dubstep",
    "Loops",
    "Bass",
    "Drum Perc",
    "FX",
    "Melodic",
    "One Shots",
    "Bass",
    "Drum Perc",
    "Claps",
    "HiHats",
    "Kicks",
    "Percussion",
    "Rides",
    "Snares",
    "FX",
    "Melodic",
    "Vocal",
    "Sharks",
    "Atmosphere",
    "Loops",
    "Drum Loops",
    "Guitar Loops",
    "Song Loops",
    "Break Eb minor 128 bpm",
    "Breakcore Eb minor 180bpm",
    "DnB E minor 174 bpm",
    "DnB Gb minor 172 bpm",
    "Dubstep Eb minor 140 bpm",
    "Funk D minor 100 bpm",
    "House Eb minor 128 bpm",
    "Melodic Drumstep E minor 174 bpm",
    "Phonk Db minor 174 bpm",
    "Tonal Loops",
    "One Shots",
    "Bass",
    "Drums",
    "Fills",
    "Sfx",
    "Synths",
    "Vocals",
    "Various",
    "Drum Loops",
    "Hits",
    "Objects",
    "Cards and Dice",
    "Coins and Money",
    "Crafting",
    "Doors and Chests",
    "Futuristic",
    "Food and Drink",
    "Items and Equipment",
    "Gems",
    "Medieval Inventory",
    "Locks and Levers",
    "Mechanisms",
    "Metal and Gears",
    "Object Interactions",
    "Pick Ups",
    "Potions and Brewing",
    "Power Up Down",
    "Tools and Crafting",
    "Wood and Stone",
    "Retro Sounds",
    "Actions",
    "Damage and Health",
    "Enemy",
    "Events",
    "Explosions",
    "Impacts and Weapons",
    "Melodic Events",
    "Miscellaneous",
    "Movement",
    "Pick Ups",
    "Power Up Down",
    "UI",
    "Access Denied",
    "Buttons",
    "Dialog",
    "Negative",
    "Points Counter",
    "Positive",
    "Weapons",
    "Laser Gun",
    "Spells and Magic",
    "Buffs",
    "Casting",
    "Effects",
    "Explosion",
    "Impacts",
    "Shoot",
    "Various",
    "Ambience",
    "Spooky and Scary",
    "Sports and Athletics",
    "Vehicles and Transport",
    "Voice",
    "AI Voice",
    "Announcers",
    "Army Sergeant",
    "Cute",
    "Generic Female",
    "Generic Male",
    "Luchador",
    "Monster",
    "Nerdy",
    "Robot",
    "Blacksmith 01",
    "Cartoon Dwarf",
    "Cartoon Emotes",
    "Cartoon Pirate",
    "Cartoon Small",
    "Cartoon Voices",
    "Crowd Reactions",
    "Demon",
    "Battle Cries",
    "Common",
    "Custom",
    "Laughing",
    "Vocalizations",
    "Demon 02",
    "Common",
    "Custom",
    "Vocalizations",
    "Dont",
    "Enemy NPCs",
    "Enemy 01",
    "Laughing",
    "Vocalization",
    "Voicelines",
    "Enemy 02",
    "Laughing",
    "Vocalization",
    "Voicelines",
    "Enemy 03",
    "Laughing",
    "Vocalization",
    "Voicelines",
    "Enemy 04",
    "Laughing",
    "Vocalization",
    "Voicelines",
    "Enemy 05",
    "Laughing",
    "Vocalization",
    "Voicelines",
    "FPS Announcer",
    "GLaDAI",
    "Knight",
    "Battle Cries",
    "Common",
    "Coughing",
    "Crying",
    "Custom",
    "Laughing",
    "Vocalization",
    "Merchant 01",
    "Merchant 02",
    "Greetings",
    "Merchant",
    "Partings",
    "Quest Begin",
    "Quest End",
    "Military",
    "US Cartoon",
    "US Marine",
    "US Monster",
    "Military Radio",
    "Codes",
    "Alphabet",
    "Letters",
    "Numbers",
    "Communication",
    "Objectives",
    "Orders",
    "Support",
    "Necromancer",
    "Common",
    "Custom",
    "Vocalizations",
    "Necromancer Lord",
    "Common",
    "Custom",
    "Vocalizations",
    "Random Guy 01",
    "Trailer Voice",
    "Ultimate Announcer",
    "Vocalizations",
    "Human Male 01",
    "Humanoid",
    "Laughing",
    "Female Type 01",
    "Female Type 02",
    "Female Type 03",
    "Female Type 04",
    "Male Type 01",
    "Male Type 02",
    "Small Humanoid",
    "Wizard",
    "Wraith",
    "Common",
    "Custom",
    "Vocalizations",
    "Weapons",
    "Effects",
    "Whoosh",
    "Futuristic",
    "Blaster",
    "Boosted Shotgun",
    "Chain Gun",
    "Cyber Crossbow",
    "Electric Blaster",
    "Energy Shield",
    "Fire Thrower",
    "Handling",
    "Reload",
    "High Tech",
    "Interface",
    "Laser Sword",
    "Laser Weapon",
    "Night Vision",
    "Plasma Weapon",
    "Spaceship",
    "Various",
    "Handling Noises",
    "Historical",
    "Cannon",
    "Firearms",
    "Medieval",
    "Blade 01",
    "Blade Large",
    "Blade Normal",
    "Blade Sharp",
    "Blade Small",
    "Bow and Arrow",
    "Effects",
    "Impact",
    "Impact Flesh",
    "Maul Hammer",
    "Sharp Dagger",
    "Siege Weapon",
    "Various",
    "Modern",
    "AK47",
    "Grenade",
    "Handgun",
    "Machine Gun",
    "Machine Gun 2",
    "Rocket Launcher",
    "Sniper Rifle",
]
Tags = Literal[
    "8bit",
    "action",
    "ambiance",
    "ambient",
    "battle",
    "boss",
    "calm",
    "casual",
    "dark",
    "epic",
    "ethnic",
    "fantasy",
    "happy",
    "horror",
    "hybrid",
    "nordic",
    "orchestral",
    "scifi",
    "tavern",
    "western",
    "16bit",
    "8bit",
    "Acion",
    "Action",
    "Adventure",
    "African",
    "Aggressive",
    "Alert",
    "Alternative dance",
    "Alternative hip-hop",
    "Alternative pop",
    "Ambiance",
    "Ambience",
    "Ambient",
    "Angry",
    "Anti-pop",
    "Asian",
    "Atmosphere",
    "Atmospheric",
    "Bass house",
    "Bass music",
    "Battle",
    "Big room house",
    "Blues",
    "Boss",
    "Bouncy",
    "Brazilian phonk",
    "Breakbeat",
    "Bright",
    "Calm",
    "Calming",
    "Cartoon",
    "Casual",
    "Celtic",
    "Chasing",
    "Chill",
    "Chill bass",
    "Chill house",
    "Chill pop",
    "Chiptune",
    "Christmas",
    "Cinematic",
    "Classical",
    "Color bass",
    "Combat",
    "Comedy",
    "Complextro",
    "Contemporary",
    "Creepy",
    "Cute",
    "Cyberpunk",
    "Dance",
    "Dance-pop",
    "Dance-punk",
    "Dance-rock",
    "Dark",
    "Deep house",
    "Desert",
    "Disco",
    "Disco house",
    "Doom",
    "Downtempo",
    "Dreamy",
    "Driving",
    "Drone",
    "Drum & bass",
    "Drums",
    "Drumstep",
    "Dubstep",
    "Dungeon",
    "Dystopian",
    "Eccentric",
    "Edm",
    "Eerie",
    "Electro",
    "Electro house",
    "Electronic",
    "Electronic pop",
    "Electronic rock",
    "Electronica",
    "Elegant",
    "Energetic",
    "Environment",
    "Epic",
    "Ethnic",
    "Euphoric",
    "Event",
    "Experimental",
    "Fantasy",
    "Fear",
    "Field",
    "Fire",
    "Floating",
    "Forest",
    "Funk",
    "Funny",
    "Future bass",
    "Future bounce",
    "Future funk",
    "Future house",
    "Future rave",
    "Future trap",
    "Futurepop",
    "Futuristic",
    "Garage",
    "Glamorous",
    "Glitch hop",
    "Gothic",
    "Grooving",
    "Guitar",
    "Happy",
    "Hardcore",
    "Hardstyle",
    "Harp",
    "Heavy",
    "Hip-hop",
    "Holiday",
    "Hopeful",
    "Horror",
    "House",
    "Humor",
    "Humorous",
    "Hybrid",
    "Hyperpop",
    "Indie",
    "Indie dance",
    "Instrumental",
    "Intense",
    "Jazz",
    "Jersey club",
    "Jrpg",
    "Jump-up",
    "Laid back",
    "Latin",
    "Latin-dance",
    "Light",
    "Liquid",
    "Lofi",
    "Lofi hip-hop",
    "Loop",
    "Low-fi",
    "Medieval",
    "Melbourne bounce",
    "Melodic dubstep",
    "Melodic house",
    "Metal",
    "Midtempo bass",
    "Military",
    "Minimal",
    "Modern",
    "Moodshappy",
    "Musical",
    "Mysterious",
    "Mystery",
    "Mystical",
    "Nature",
    "Neurofunk",
    "Nordic",
    "Ocean",
    "Orchestral",
    "Peaceful",
    "Percussion",
    "Phonk",
    "Piano",
    "Pirate",
    "Platformer",
    "Polka",
    "Pop",
    "Progressive electro",
    "Progressive electron",
    "Progressive house",
    "Puzzle",
    "Quirky",
    "Reggae",
    "Relaxed",
    "Relaxing",
    "Restless",
    "Retro",
    "Retrowave",
    "Riddim",
    "Rock",
    "Romantic",
    "Rpg",
    "Running",
    "Sad",
    "Scary",
    "Sci-fi",
    "Scifi",
    "Sentimental",
    "Sexy",
    "Sfx",
    "Short",
    "Silentfilmscore",
    "Ska",
    "Slap house",
    "Slavic",
    "Smooth",
    "Sneaking",
    "Sneaky",
    "Somber",
    "Soundscape",
    "Soundtrack",
    "Spooky",
    "Stings",
    "Suspense",
    "Suspenseful",
    "Synth",
    "Synth-pop",
    "Synthwave",
    "Tavern",
    "Tech house",
    "Techno",
    "Texture",
    "Theme",
    "Tonal",
    "Town",
    "Trance",
    "Tranquil",
    "Trap",
    "Tropical house",
    "Unclassifiable",
    "Underscore",
    "Unnerving",
    "Upbeat",
    "Uplifting",
    "Urban",
    "Weird",
    "Western",
    "World",
]


# Enum
class OfficialSong(Enum):
    """
    Represents official songs in the game.
    """

    STEREO_MADNESS = 0
    BACK_ON_TRACK = 1
    POLAR_GEIST = 2
    DRY_OUT = 3
    BASE_AFTER_BASE = 4
    CANT_LET_GO = 5
    JUMPER = 6
    TIME_MACHINE = 7
    CYCLES = 8
    XSTEP = 9
    CLUTTERFUNK = 10
    THEORY_OF_EVERYTHING = 11
    ELECTROMAN_ADVENTURES = 12
    CLUBSTEP = 13
    ELECTRODYNAMIX = 14
    HEXAGON_FORCE = 15
    BLAST_PROCESSING = 16
    THEORY_OF_EVERYTHING_2 = 17
    GEOMETRICAL_DOMINATOR = 18
    DEADLOCKED = 19
    FINGERDASH = 20
    DASH = 21
    # Add more official songs here


class Difficulty(Enum):
    """
    Represents the non-demon difficulty levels.
    """

    NA = 0
    """No difficulty."""
    EASY = 1
    """Easy difficulty."""
    NORMAL = 2
    """Normal difficulty."""
    HARD = 3
    """Hard difficulty."""
    HARDER = 4
    """Harder difficulty."""
    INSANE = 5
    """Insane difficulty."""
    DEMON = 6
    """Demon difficulty."""
    AUTO = 7
    """Auto difficulty."""


class DemonDifficulty(Enum):
    """
    Represents the demon difficulty levels.
    """

    HARD_DEMON = 0
    """Hard demon."""
    EASY_DEMON = 3
    """Easy demon."""
    MEDIUM_DEMON = 4
    """Medium demon."""
    INSANE_DEMON = 5
    """Insane demon."""
    EXTREME_DEMON = 6
    """Extreme demon."""

    DEFAULT = HARD_DEMON


class Length(IntEnum):
    """
    Represents the length of a level.
    """

    TINY = 0
    """Tiny length."""
    SHORT = 1
    """Short length."""
    MEDIUM = 2
    """Medium length."""
    LONG = 3
    """Long length."""
    XL = 4
    """Extra long length."""
    PLATFORMER = 5
    """Platformer level type."""


class LevelRating(Enum):
    """
    Represents the rating of a level.
    """

    NO_RATE = -2
    """No rating specified."""
    RATED = -1
    """Rated but not featured."""
    FEATURED = 0
    """Featured level."""
    EPIC = 1
    """Epic level."""
    MYTHIC = 3
    """Mythic level."""
    LEGENDARY = 2
    """Legendary level."""


class ModRank(IntEnum):
    """
    Represents the moderator status of a level.
    """

    NONE = 0
    """Not a moderator."""
    MOD = 1
    """Moderator."""
    ELDER_MOD = 2
    """Elder moderator."""
    DEFAULT = NONE


class Gamemode(Enum):
    """
    Represents the different gamemodes.
    """

    CUBE = 0
    SHIP = 1
    BALL = 2
    UFO = 3
    WAVE = 4
    ROBOT = 5
    SPIDER = 6
    SWING = 7
    JETPACK = 8


class SearchFilter(IntEnum):
    """
    Represents search options.
    """

    MOST_DOWNLOADED = 1
    """Sort to most downloaded."""
    MOST_LIKED = 2
    """Sort to most liked. (default)"""
    TRENDING = 3
    """Sort to trending."""
    RECENT = 4
    """Sort to recent."""
    FEATURED = 6
    """Sort to featured tab."""
    TOP_LISTS = 6
    """Sort top lists."""
    MAGIC = 7
    """Sort to magic."""
    LIST_OF_LEVELS = 10
    """Get the display information for levels. (Seperated by a comma)"""
    AWARDED = 11
    """Sort to recently rated."""
    HALL_OF_FAME = 16
    """Hall of Fame."""
    GD_WORLD = 17
    """GD World."""
    DAILY = 21
    """Filter daily levels."""
    WEEKLY = 22
    """Filter weekly levels."""
    EVENT = 23
    """Filter event levels."""
    LIST_SENT = 27
    """Filter lists sent by moderators."""
    FRIENDS = 13
    """Filter levels made by friends. (Login required)"""

    DEFAULT = MOST_DOWNLOADED


class Leaderboard(StrEnum):
    """
    Represents the leaderboard types.
    """

    TOP = auto()
    """Gets the top 100 in the global leaderboard."""
    RELATIVE = auto()
    """Gets the surrounding leaderboard of your rank."""
    FRIENDS = auto()
    """Gets the leaderboard of your friends."""
    CREATORS = auto()
    """Gets the leaderboard of creators."""

    DEFAULT = TOP


class Item(Enum):
    """
    Represents items/collectables.
    """

    DIAMOND = 1
    ORBS = 2
    STARS = 3
    MOONS = 4
    USERCOIN = 5
    SHARDS = 6
    DEMON_KEY = 7

    @staticmethod
    def from_chest_item_id(item_id: int) -> Union["Item.DEMON_KEY", "Shard", None]:
        """
        Returns the corresponding `Item` or `Shard` from the given `item_id` in the chest response.

        :param item_id: The `item_id` returned from the chest response.
        :type item_id: int
        :return: The corresponding `Item` or `Shard`.
        :rtype: Union["Item.DEMON_KEY", "Shard", None]
        """
        if item_id == 0:
            return None
        if item_id == 5:
            return Item.DEMON_KEY

        return Shard(item_id)


class Shard(Enum):
    """
    Represents shard types.
    """

    FIRE = 1
    ICE = 2
    POISON = 3
    SHADOW = 4
    LAVA = 5
    EARTH = 10
    BLOOD = 11
    METAL = 12
    LIGHT = 13
    SOUL = 14
