# SKOOLACH

A retro text adventure game with vector graphics that teaches the fundamentals of AI model architecture through interactive storytelling.

## Concept

You are a coder whose AI model has been infected by the SKOOLACH virus. The virus has broken down your model into its fundamental components and scattered them throughout a mysterious digital cave system. To defeat the virus and restore your AI, you must explore, solve puzzles, and collect the pieces that make up a modern language model.

## Educational Goals

Players will learn about:
- **Tokenization** - How text is broken down into processable units
- **Embeddings** - How words are represented as vectors
- **Attention Mechanisms** - How models focus on relevant information
- **Neural Network Layers** - The building blocks of the model
- **Training Data** - The knowledge that powers the AI
- **Inference Pipeline** - How queries are processed
- And more...

## Unique Gameplay Mechanic

The game's text parser evolves as you play:
- **Early game**: Simple two-word commands (VERB NOUN - "GO NORTH", "TAKE KEY")
- **Mid game**: More sophisticated parsing as you collect AI components
- **Late game**: Natural language understanding with context awareness
- **End game**: Full AI-assisted parser to defeat the SKOOLACH virus

## Inspirations

- **Zork** - Deep exploration and clever puzzles
- **Colossal Cave Adventure** - The original text adventure aesthetic
- **Mystery House** - Early graphics integration
- **Hitchhiker's Guide to the Galaxy** - Humor and creative problem-solving
- **Oregon Trail** - Educational gaming with memorable challenges

## Technical Stack

- **Language**: Python 3.10+
- **Graphics**: Vector-style rendering (wireframe aesthetic)
- **Architecture**: Modular game engine with plugin system for AI components

## Project Structure

```
skoolach/
├── src/
│   ├── game/          # Core game engine and loop
│   ├── graphics/      # Vector graphics rendering
│   └── ai_components/ # Collectible AI pieces and their effects
├── assets/
│   └── maps/          # Room definitions and world data
├── tests/             # Unit tests
└── README.md
```

## Getting Started

### Quick Start (Text-Only)

```bash
# Run without graphics (no installation needed)
python src/main.py
# Select option 2 for text-only mode
```

### Full Experience (With Graphics)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game with retro vector graphics
python src/main.py
# Select option 1 for graphics mode
```

### Alternative Text-Only Version

```bash
# Direct text-only mode
python src/main_text.py
```

## Game Controls

### Text Commands
- `GO <direction>` or `N/S/E/W/NE/NW/SE/SW/U/D`
- `TAKE <item>` - Pick up items
- `DROP <item>` - Drop items
- `LOOK [item]` - Examine room or item
- `INVENTORY` or `I` - Check your inventory
- `ATTACK <target>` - Start combat
- `HELP` - Show available commands
- `QUIT` - Exit game

### Graphics Mode Controls
- `TAB` - Toggle auto-rotate camera
- `LEFT/RIGHT ARROWS` - Manually rotate camera
- `ESC` - Quit game
- Type commands in the input area at bottom

## Development Status

✅ **Complete** - Full game with combat, 9 AI components, and graphics!

---

*"In the depths of the digital cave, your model awaits reconstruction..."*
