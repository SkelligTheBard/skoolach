# SKOOLACH - Quick Start Guide

## Installation & Running

### Option 1: Text-Only (No Installation Required)

```bash
cd skoolach
python src/main.py
# Choose option 2 when prompted
```

### Option 2: Full Graphics Experience (Recommended)

```bash
cd skoolach
pip install -r requirements.txt
python src/main.py
# Choose option 1 when prompted
```

## Your First 10 Minutes

### 1. Start the Game
```
> python src/main.py
```

You'll see the intro story and wake up at the Crash Site.

### 2. Get Your Bearings
```
> LOOK
```

Examines the current room. Shows items and exits.

### 3. Pick Up the Flashlight
```
> TAKE FLASHLIGHT
```

You'll need this for the Dark Archives later!

### 4. Check Your Inventory
```
> INVENTORY
```

Or just `I` for short. Shows what you're carrying.

### 5. Move North
```
> GO NORTH
```

Or just `N`. You'll reach the Memory Corridor (central hub).

### 6. Explore and Collect
```
> NORTH      # Tokenizer Chamber
> TAKE TOKENIZER CORE
```

**Notice**: Your parser upgrades! You can now use articles like "the" and "a".

### 7. Continue Exploring
```
> SOUTH      # Back to Memory Corridor
> EAST       # Embedding Space
> TAKE EMBEDDING LAYER
```

Each AI component you collect makes your parser smarter!

### 8. Use Your Map

From Memory Corridor:
- **NORTH**: Tokenizer Chamber
- **EAST**: Embedding Space
- **WEST**: Dark Archives (need flashlight!)
- **NORTHEAST**: Attention Nexus
- **SOUTHEAST**: Neural Network Depths

### 9. Collect More Components

Explore all rooms and collect all 9 AI components:
- Tokenizer Core
- Embedding Layer
- Training Data Archive
- Attention Head
- Neural Network Layer
- Optimizer Module
- Inference Engine
- Context Window
- Fine-tuning Module

### 10. Get Ready for Battle

Before fighting SKOOLACH:
1. Collect **at least 3-4 AI components** (more is better!)
2. Find the **quantum debugger** in Fine-Tuning Laboratory
3. Navigate to Dark Archives → Northwest → Northwest
4. Type `ATTACK SKOOLACH` to begin combat

## Combat Quick Guide

### Starting Combat
```
> ATTACK SKOOLACH
```

### Combat Commands
You'll see a numbered list of actions:
```
Choose your action:
  1. Debug Attack [DMG: 10]
     A basic debugging attempt. Weak but reliable.
  2. Token Blast [DMG: 20]
     Break down the virus into manageable tokens...
```

Just type the number:
```
> 1
```

### Combat Tips
- **More components = more attacks**: Each AI component unlocks a unique attack
- **Damage varies**: Higher DMG numbers are better
- **Watch boss phases**: SKOOLACH gets more aggressive as health drops
- **Heal if available**: Optimizer unlocks healing ability

## Essential Commands Reference

### Movement
- `NORTH` / `N`
- `SOUTH` / `S`
- `EAST` / `E`
- `WEST` / `W`
- `NORTHEAST` / `NE`
- `NORTHWEST` / `NW`
- `SOUTHEAST` / `SE`
- `SOUTHWEST` / `SW`
- `UP` / `U`
- `DOWN` / `D`

### Interaction
- `TAKE <item>` - Pick up item
- `DROP <item>` - Drop item
- `LOOK` - Examine room
- `LOOK <item>` - Examine specific item
- `INVENTORY` / `I` - Check inventory
- `USE <item>` - Use an item

### Combat
- `ATTACK <target>` - Start fight
- `<number>` - Choose combat action
- `HELP` - Show available actions

### System
- `HELP` - Show help text
- `QUIT` - Exit game

## Win Conditions

To beat SKOOLACH:

1. ✅ Collect AI components (3 minimum, 9 recommended)
2. ✅ Get quantum debugger from Fine-Tuning Lab
3. ✅ Navigate to Virus Lair
4. ✅ Defeat SKOOLACH in combat
5. ✅ Learn about AI architecture!

## Parser Evolution

As you collect components, your parser gets smarter:

**Level 0** (Start):
```
> GO NORTH        ✓
> GO TO NORTH     ✗ (too complex)
```

**Level 1** (1+ components):
```
> GO TO THE NORTH     ✓
> TAKE THE KEY        ✓
```

**Level 2+** (More components):
```
> EXAMINE THE ANCIENT CODEX    ✓
> GET DEBUGGER                 ✓ (synonyms work)
```

## Troubleshooting

### "I can't go that way"
- Use `LOOK` to see available exits
- Some paths require items (flashlight, debugger)

### "I don't understand that command"
- Your parser level might be too low
- Try simpler commands: `TAKE KEY` instead of `TAKE THE GOLDEN KEY`
- Type `HELP` to see available commands

### "You're too weak to fight SKOOLACH"
- Collect more AI components (minimum 3)
- Explore more rooms to find components

### Graphics not working
- Install pygame: `pip install pygame`
- Or use text-only mode (option 2)

## Tips for Success

1. **Read everything**: Every item description has real educational content
2. **Explore systematically**: Memory Corridor is the hub, explore all branches
3. **Collect before fighting**: Get 6-9 components for easier combat
4. **Watch your health**: Combat can be tough with few components
5. **Enjoy learning**: This game teaches real AI architecture!

## Map Overview

```
                    Fine-Tuning Lab
                           |
    Tokenizer    Optimization Chamber      Context Chamber
        |               |                       |
    Memory ---- Neural Depths ------- Inference Room
    Corridor            |                       |
        |          (unexplored)         Attention Nexus
    Crash Site
        |
    (start)

    Memory Corridor also connects:
    - EAST: Embedding Space
    - WEST: Dark Archives → Corrupted Gateway → Virus Lair
```

## Next Steps

Once you beat SKOOLACH:
- Try speedrunning (how fast can you win?)
- Can you beat it with only 3 components?
- Read all the educational content for each component
- Share your experience!

---

**Now go forth and rebuild your AI!** 🎮🤖

For the complete guide: See `GAME_GUIDE.md`
