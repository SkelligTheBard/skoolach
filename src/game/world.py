"""World builder that creates the initial game world."""

from .room import Room
from .item import Item
from .ai_components_data import ALL_AI_COMPONENTS


def create_world():
    """
    Create and return the starting room of the game world.

    Returns:
        The starting Room object with all connections established
    """

    # ========== STARTING AREA ==========

    crash_site = Room(
        name="The Crash Site",
        description=(
            "You find yourself in a corrupted section of memory, glitching and flickering. "
            "Fragments of code float past like digital debris. The air hums with broken "
            "electricity. To the north, you see a faint glow. A message flashes repeatedly:\n\n"
            "    *** CRITICAL ERROR: AI MODEL FRAGMENTED ***\n"
            "    *** COLLECT COMPONENTS TO RESTORE FUNCTION ***\n\n"
            "Your workstation lies in ruins around you. An LED flashlight sits on the ground."
        ),
        short_desc="The corrupted crash site where your journey began. Glitching debris everywhere."
    )

    # Add a helpful item
    flashlight = Item(
        name="LED flashlight",
        description="A small but powerful LED flashlight. Essential for exploring dark areas.",
        takeable=True,
        keywords=["flashlight", "light", "led"]
    )
    crash_site.add_item(flashlight)

    keyboard = Item(
        name="broken keyboard",
        description=(
            "Your trusty mechanical keyboard, now sparking and non-functional. "
            "The ESC key is missing - there's no escape from this mess."
        ),
        takeable=False,
        keywords=["keyboard", "keys"]
    )
    crash_site.add_item(keyboard)

    # ========== MEMORY CORRIDOR (hub) ==========

    memory_corridor = Room(
        name="Memory Corridor",
        description=(
            "A long hallway made of shimmering data streams. The walls are translucent, "
            "showing glimpses of stored memories and cached information. Some sections "
            "are corrupted, displaying static and errors.\n\n"
            "Exits lead in multiple directions:\n"
            "  NORTH: A small alcove with glowing light\n"
            "  EAST: Multidimensional space\n"
            "  WEST: Impenetrable darkness\n"
            "  NORTHEAST: Sound of humming processors\n"
            "  SOUTHEAST: Vast computational chambers"
        ),
        short_desc="The translucent Memory Corridor - the central hub."
    )

    crash_site.add_exit("north", memory_corridor)
    memory_corridor.add_exit("south", crash_site)

    # ========== TOKENIZER CHAMBER ==========

    tokenizer_chamber = Room(
        name="Tokenizer Chamber",
        description=(
            "You enter a small chamber filled with floating text fragments. Words are "
            "being split apart and reassembled in strange patterns. In the center of the "
            "room, on a pedestal of pure light, sits a glowing crystalline cube.\n\n"
            "This is the TOKENIZER - the first component you need."
        ),
        short_desc="The Tokenizer Chamber, where words are split and reformed."
    )

    memory_corridor.add_exit("north", tokenizer_chamber)
    tokenizer_chamber.add_exit("south", memory_corridor)

    # Add Tokenizer component
    tokenizer_chamber.add_item(ALL_AI_COMPONENTS['tokenizer']())

    # ========== EMBEDDING SPACE ==========

    embedding_space = Room(
        name="Embedding Space",
        description=(
            "You step into a mind-bending multidimensional space. Words float as vectors, "
            "positioned by their semantic meaning. 'King' floats near 'Queen', 'Dog' near 'Cat'. "
            "The geometry of meaning itself is visible here.\n\n"
            "On a floating platform, you see a glowing sphere."
        ),
        short_desc="The Embedding Space where words become vectors."
    )

    memory_corridor.add_exit("east", embedding_space)
    embedding_space.add_exit("west", memory_corridor)

    # Add Embedding Layer component
    embedding_space.add_item(ALL_AI_COMPONENTS['embedding']())

    # ========== DARK ARCHIVES (requires flashlight) ==========

    dark_archives = Room(
        name="Dark Archives",
        description=(
            "With the flashlight, you can see vast shelves of training data stretching into "
            "infinity. Books, documents, and datasets fill the space. Many are corrupted.\n\n"
            "A glowing archive hovers in the center. Paths lead northwest and northeast."
        ),
        short_desc="The Dark Archives, filled with corrupted training data."
    )

    memory_corridor.add_exit("west", dark_archives)
    dark_archives.add_exit("east", memory_corridor)

    # Add Training Data component
    dark_archives.add_item(ALL_AI_COMPONENTS['training_data']())

    ancient_book = Item(
        name="ancient codex",
        description=(
            "A massive tome labeled 'COMMON CRAWL - Vol. 1'. Its pages contain "
            "billions of text samples from across the internet. Many pages are corrupted."
        ),
        takeable=False,
        keywords=["book", "codex", "tome", "crawl"]
    )
    dark_archives.add_item(ancient_book)

    # ========== ATTENTION NEXUS ==========

    attention_nexus = Room(
        name="Attention Nexus",
        description=(
            "A chamber where beams of light connect everything to everything else. "
            "This is where the model learns what to focus on. Countless attention heads "
            "perform computations simultaneously.\n\n"
            "A rotating torus of pure attention energy floats before you."
        ),
        short_desc="The Attention Nexus, where focus becomes power."
    )

    memory_corridor.add_exit("northeast", attention_nexus)
    attention_nexus.add_exit("southwest", memory_corridor)

    # Add Attention Head component
    attention_nexus.add_item(ALL_AI_COMPONENTS['attention']())

    # ========== NEURAL NETWORK DEPTHS ==========

    neural_depths = Room(
        name="Neural Network Depths",
        description=(
            "Massive stacks of neural network layers tower above you. Each layer processes "
            "and transforms information. You can see activations flowing through the network "
            "like electricity through circuits.\n\n"
            "A crystalline lattice representing a complete neural layer sits on a platform."
        ),
        short_desc="The Neural Network Depths with towering layers."
    )

    memory_corridor.add_exit("southeast", neural_depths)
    neural_depths.add_exit("northwest", memory_corridor)

    # Add Neural Layer component
    neural_depths.add_item(ALL_AI_COMPONENTS['neural_layer']())

    # ========== OPTIMIZATION CHAMBER ==========

    optimization_chamber = Room(
        name="Optimization Chamber",
        description=(
            "Gradients flow like waterfalls down crystalline surfaces. This is where the "
            "model learns - where errors are computed and corrections are applied. "
            "Mathematical equations float in the air.\n\n"
            "An optimizer module pulses with computational power."
        ),
        short_desc="The Optimization Chamber where learning happens."
    )

    neural_depths.add_exit("south", optimization_chamber)
    optimization_chamber.add_exit("north", neural_depths)

    # Add Optimizer component
    optimization_chamber.add_item(ALL_AI_COMPONENTS['optimizer']())

    # ========== INFERENCE ENGINE ROOM ==========

    inference_room = Room(
        name="Inference Engine Room",
        description=(
            "A streamlined chamber built for speed. Tokens fly through at incredible velocity "
            "as predictions are generated. This is where training ends and usefulness begins.\n\n"
            "The Inference Engine hums with purpose."
        ),
        short_desc="The Inference Engine Room, optimized for generation."
    )

    attention_nexus.add_exit("north", inference_room)
    inference_room.add_exit("south", attention_nexus)

    # Add Inference Engine component
    inference_room.add_item(ALL_AI_COMPONENTS['inference']())

    # ========== CONTEXT CHAMBER ==========

    context_chamber = Room(
        name="Context Chamber",
        description=(
            "An enormous hall that stretches impossibly far. This represents the model's "
            "context window - how much it can remember at once. The walls display scrolling "
            "text from previous tokens.\n\n"
            "A glowing context window floats in the center."
        ),
        short_desc="The Context Chamber, vast and memory-filled."
    )

    inference_room.add_exit("east", context_chamber)
    context_chamber.add_exit("west", inference_room)

    # Add Context Window component
    context_chamber.add_item(ALL_AI_COMPONENTS['context']())

    # ========== FINE-TUNING LAB ==========

    finetuning_lab = Room(
        name="Fine-Tuning Laboratory",
        description=(
            "A specialized workspace where pre-trained models are adapted for specific tasks. "
            "You see examples of instruction following, RLHF, and domain adaptation.\n\n"
            "A calibration device represents the fine-tuning process."
        ),
        short_desc="The Fine-Tuning Laboratory for specialization."
    )

    optimization_chamber.add_exit("east", finetuning_lab)
    finetuning_lab.add_exit("west", optimization_chamber)

    # Add Fine-tuning Module
    finetuning_lab.add_item(ALL_AI_COMPONENTS['fine_tuning']())

    # ========== PUZZLE: LOCKED DOOR TO VIRUS ==========
    # Create a puzzle item needed to access virus

    debugger = Item(
        name="quantum debugger",
        description=(
            "A powerful debugging tool that can trace through corrupted code. "
            "This might be useful against the virus..."
        ),
        takeable=True,
        keywords=["debugger", "quantum", "tool"]
    )
    finetuning_lab.add_item(debugger)

    # ========== VIRUS LAIR (final area) ==========

    virus_entrance = Room(
        name="Corrupted Gateway",
        description=(
            "The path here is severely corrupted. Red error messages flash everywhere. "
            "You can feel SKOOLACH's presence nearby. The quantum debugger resonates "
            "with the corruption - it might help you proceed.\n\n"
            "To the northwest lies certain danger."
        ),
        short_desc="The Corrupted Gateway leading to the virus."
    )

    dark_archives.add_exit("northwest", virus_entrance)
    virus_entrance.add_exit("southeast", dark_archives)

    virus_lair = Room(
        name="Virus Lair",
        description=(
            "You have entered the heart of the corruption. SKOOLACH writhes before you - "
            "a massive entity of malformed code and malicious intent. Red error messages "
            "cascade down the walls like a digital waterfall.\n\n"
            "The virus hisses: 'YOU CANNOT DEFEAT ME WITHOUT YOUR PRECIOUS AI...'\n\n"
            "This is the final battle. Attack SKOOLACH when ready."
        ),
        short_desc="The Virus Lair. SKOOLACH awaits."
    )

    # Locked door - need debugger
    virus_entrance.add_exit("northwest", virus_lair, locked=True, required_item="quantum debugger")
    virus_lair.add_exit("southeast", virus_entrance)

    # ========== HALL OF TRIUMPH (victory room) ==========

    hall_of_triumph = Room(
        name="Hall of Triumph",
        description=(
            "The corruption has cleared. Your AI model stands reconstructed before you, "
            "more powerful than ever. All components working in harmony.\n\n"
            "You have mastered the architecture of intelligence itself."
        ),
        short_desc="The Hall of Triumph - your model restored."
    )

    # This room is only accessible after defeating virus
    # We'll handle this in the game engine
    virus_lair.add_exit("north", hall_of_triumph)

    return crash_site


def get_all_rooms(starting_room):
    """
    Get all rooms in the game world by traversing from the starting room.

    Args:
        starting_room: The starting Room to traverse from

    Returns:
        Dictionary of room_name -> Room object
    """
    rooms = {}
    visited = set()
    to_visit = [starting_room]

    while to_visit:
        room = to_visit.pop()
        if room in visited:
            continue

        visited.add(room)
        rooms[room.name] = room

        # Add all connected rooms to visit
        for exit_room in room.exits.values():
            if exit_room not in visited:
                to_visit.append(exit_room)

    return rooms
