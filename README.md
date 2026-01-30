# SKOOLACH 
(The primary Scottish Gaelic word for a narrative, tale, or story is sgeulachd, honetically anglicized to SKOOLACH)

A retro text adventure game with vector graphics that teaches the fundamentals of AI model architecture through interactive storytelling.

## Concept

You are a coder whose AI model has been infected by the SKOOLACH virus. The virus has broken down your model into its fundamental components and scattered them throughout a mysterious digital cave system. To defeat the virus and restore your AI, you must explore, solve puzzles, and collect the pieces that make up a modern language model.

## A Living, Evolving Game

**SKOOLACH is designed to be modified, enhanced, and shared!**

Part of the game's purpose is to be passed around among developers and AI enthusiasts. After playing through SKOOLACH, you're encouraged to:

- 🤖 **Use AI assistance** (like Claude, ChatGPT, etc.) to add your own features
- 🎮 **Create new puzzles** and challenges
- 🏗️ **Add complexity** to existing mechanics
- 🎨 **Improve graphics** or add new visual effects
- 📚 **Expand educational content** with new AI concepts
- 🌍 **Design new rooms** and areas to explore
- ⚔️ **Add new items** or enemies
- 🔧 **Refine gameplay** mechanics
- **BE CURIOUS** about the process when working with the AI, ask it to explain steps, choices, and give you opportunities to ask questions. 

Then **share your enhanced version** with others! Each person who plays can contribute their own improvements, creating an ever-evolving educational experience.

### Why This Matters

SKOOLACH demonstrates:
- How AI can help you **learn by building**
- The power of **collaborative enhancement** with AI tools
- That games can be **living documents** that grow with their community
- How **open-source + AI** creates new possibilities for creative projects

**Think of it as:** A game that teaches AI concepts, built to be improved using AI, shared within a community learning about AI. 🔄

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
- `UP/DOWN ARROWS` - Scroll through description text
- `PAGE UP/PAGE DOWN` - Scroll description by full page
- `DELETE` - Clear the description pane
- `ESC` - Quit game
- Type commands in the input area at bottom left

## Development Status

✅ **Complete** - Full game with combat, 9 AI components, and graphics!

---

## Extending SKOOLACH

### Ideas for Your Enhancements

Here are some ways you could expand the game:

**New Features:**
- Add save/load game functionality
- Create a crafting system for combining items
- Add side quests or optional challenges
- Implement multiple endings based on choices
- Add background music and sound effects
- Create character customization options

**Educational Expansions:**
- Add more AI concepts (transformers, reinforcement learning, GANs)
- Create quiz mini-games that test understanding
- Add visual diagrams explaining concepts
- Include code examples for each component
- Add historical context about AI development

**Gameplay Enhancements:**
- Design new puzzle types
- Add time-based challenges
- Create inventory management mechanics
- Add companion NPCs with dialogue trees
- Implement a hint system for stuck players
- Add achievements/badges for accomplishments

**Technical Improvements:**
- Add networking for multiplayer features
- Create a level editor
- Implement mod support
- Add accessibility options
- Optimize performance
- Create mobile version

### How to Get Started with AI

1. **Play the game** to understand its structure
2. **Pick a feature** you want to add
3. **Use an AI assistant** (Claude, ChatGPT, etc.) by:
   - Showing it relevant code files
   - Describing what you want to add
   - Asking for implementation guidance
   - Iterating on the design together
4. **Test your changes** thoroughly
5. **Document** what you added
6. **Share** your enhanced version!

### Sharing Your Version

When you've added your improvements:
- Create a fork/branch with a descriptive name
- Document your changes in a changelog
- Add your name to a contributors list
- Share with the community
- Encourage others to build on your work!

---

## License & Sharing

SKOOLACH is designed to be freely shared, modified, and enhanced. When you add your improvements:
- ✅ You're encouraged to share your version
- ✅ Others can build on your work
- ✅ Give credit to previous contributors
- ✅ Keep the educational spirit alive
- ✅ Use any license that allows continued sharing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidance on extending the game.

---

*"In the depths of the digital cave, your model awaits reconstruction..."*

*"And with each player's touch, the cave grows deeper..."*
