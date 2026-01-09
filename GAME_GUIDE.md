# SKOOLACH - Complete Game Guide

## Overview

SKOOLACH is an educational text adventure game with retro vector graphics that teaches players about AI model architecture, specifically large language models like Claude. Players collect AI components scattered throughout a digital cave system to rebuild their broken model and defeat the SKOOLACH virus.

## Game Features

### Educational Content
- **9 AI Components** with detailed explanations:
  1. Tokenizer - Text to tokens conversion
  2. Embedding Layer - Words to vectors
  3. Attention Head - Focus mechanism
  4. Neural Network Layer - Transformation layers
  5. Training Data - Knowledge source
  6. Optimizer - Learning process
  7. Inference Engine - Generation system
  8. Context Window - Memory capacity
  9. Fine-tuning Module - Specialization

### Progressive Parser Evolution
- **Level 0**: Basic VERB NOUN commands (virus-degraded)
- **Level 1+**: Articles, prepositions, synonyms
- **Level 2+**: Natural language understanding
- Higher levels unlock as you collect AI components

### Combat System
- Turn-based combat against SKOOLACH virus
- Actions unlock based on collected AI components
- Boss has 3 phases with increasing difficulty
- Strategic depth: more components = more powerful attacks

### Game World
**13 Unique Locations:**
1. **The Crash Site** - Starting area
2. **Memory Corridor** - Central hub
3. **Tokenizer Chamber** - First component
4. **Embedding Space** - Multidimensional vectors
5. **Dark Archives** - Training data storage
6. **Attention Nexus** - Focus computations
7. **Neural Network Depths** - Layer stacks
8. **Optimization Chamber** - Learning mechanics
9. **Inference Engine Room** - Generation speed
10. **Context Chamber** - Memory capacity
11. **Fine-Tuning Laboratory** - Specialization
12. **Corrupted Gateway** - Path to boss
13. **Virus Lair** - Final battle

### Puzzles & Progression
- **Flashlight puzzle**: Required for Dark Archives
- **Quantum Debugger**: Required to reach virus
- **Component gates**: Need minimum components for boss fight

## How to Play

### Text-Only Version
```bash
python src/main_text.py
```

### With Graphics (requires pygame)
```bash
pip install -r requirements.txt
python src/main.py  # (once created)
```

### Basic Commands

**Level 0 (Start):**
- `GO <direction>` or just `NORTH`, `N`, etc.
- `TAKE <item>`
- `DROP <item>`
- `LOOK` or `LOOK <item>`
- `INVENTORY` or `I`
- `HELP`
- `QUIT`

**Higher Levels:**
- `TAKE THE KEY` (articles work)
- `GO TO THE NORTH` (prepositions work)
- `EXAMINE` (synonyms work)

**Combat Commands:**
- `ATTACK SKOOLACH` - Initiate combat
- `1`, `2`, `3`, etc. - Choose numbered action
- Combat is turn-based

## Gameplay Tips

1. **Explore thoroughly** - All AI components are essential for understanding
2. **Read descriptions carefully** - They contain real educational content
3. **Collect the flashlight** first - Needed for Dark Archives
4. **Get the quantum debugger** - Required to reach the virus
5. **Collect at least 3-4 components** before fighting SKOOLACH
6. **All 9 components** make the fight much easier

## Victory Conditions

To win the game:
1. Collect AI components (minimum 3, ideally all 9)
2. Find the quantum debugger in Fine-Tuning Lab
3. Navigate to the Virus Lair
4. Defeat SKOOLACH in combat
5. Learn about AI architecture!

## Educational Goals

By completing SKOOLACH, players learn:
- How tokenization works
- What embeddings are and why they matter
- The attention mechanism breakthrough
- How neural networks process information
- The role of training data
- How optimization/learning works
- The inference generation process
- Context window limitations
- Fine-tuning vs base models

## Technical Architecture

### Core Systems
- **Parser**: Evolving command interpreter
- **Player**: Inventory, health, component tracking
- **Room**: Navigation, items, locked exits
- **Combat**: Turn-based battle system
- **Items**: Regular items and AI components

### Graphics System (Optional)
- **Vector3D**: 3D math and wireframe rendering
- **Renderer**: Retro CRT-style graphics
- **Scene**: 3D visualization of rooms and items
- **Camera**: Perspective projection

### File Structure
```
skoolach/
├── src/
│   ├── game/
│   │   ├── engine.py              # Main game loop
│   │   ├── parser.py              # Command parsing
│   │   ├── player.py              # Player state
│   │   ├── room.py                # Room system
│   │   ├── item.py                # Items & components
│   │   ├── combat.py              # Combat system
│   │   ├── world.py               # World creation
│   │   └── ai_components_data.py  # Component definitions
│   └── graphics/
│       ├── vector3d.py            # 3D math
│       ├── renderer.py            # Rendering engine
│       ├── scene.py               # Scene management
│       └── graphics_engine.py     # Graphics integration
├── tests/
│   ├── test_parser.py             # Parser tests
│   ├── test_player.py             # Player tests
│   ├── test_room.py               # Room tests
│   ├── test_graphics.py           # Graphics tests
│   └── test_combat.py             # Combat tests
└── assets/
    └── maps/                       # Future: saved games
```

## Testing

Run all tests:
```bash
cd tests
python test_parser.py
python test_player.py
python test_room.py
python test_combat.py
# test_graphics.py requires pygame
```

All core tests pass successfully!

## Easter Eggs & Inspirations

The game includes references to:
- **Zork** - Parser style and exploration
- **Colossal Cave Adventure** - Original text adventure
- **Mystery House** - Early graphics integration
- **Hitchhiker's Guide** - Humor and puzzles
- **Oregon Trail** - Educational gaming

## Future Enhancements

Potential additions:
- Save/load system
- More puzzles and obstacles
- Additional boss fights (overfitting, hallucination, etc.)
- Sound effects
- Multiple difficulty levels
- Speedrun mode
- More AI components (RLHF, Constitutional AI, etc.)

## Credits

Inspired by classic text adventures and modern AI education needs.
Built to make AI architecture fun and accessible!

---

**Have fun learning about AI architecture!**

For questions or feedback: https://github.com/SkelligTheBard/skoolach
