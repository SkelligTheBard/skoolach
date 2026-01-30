# Contributing to SKOOLACH

**SKOOLACH is designed to evolve!** This game is meant to be played, enhanced, and shared. Each player can add their own improvements using AI assistance before passing it on.

---

## The Philosophy

SKOOLACH represents a new model of collaborative game development:

1. **Play** - Experience the game and learn about AI concepts
2. **Enhance** - Use AI tools to add features you'd like to see
3. **Share** - Pass your improved version to others
4. **Repeat** - Others build on your work

This creates a **living educational artifact** that grows with its community.

---

## Using AI to Extend SKOOLACH

### Recommended AI Assistants

- **Claude** (claude.ai or Claude Code CLI)
- **ChatGPT** (with code interpreter)
- **GitHub Copilot**
- **Cursor**
- Any other coding assistant you prefer

### How to Work with AI

1. **Start a conversation** about what you want to add
2. **Share relevant code files** with the AI
3. **Describe your vision** for the feature
4. **Iterate on the design** together
5. **Test incrementally** as you build
6. **Ask for explanations** to learn as you go

### Example AI Prompt

```
I'm working on SKOOLACH, an educational text adventure game that teaches
AI concepts. I want to add [FEATURE]. Here's the relevant code:

[paste code files]

Can you help me implement this? Please explain your approach so I can
learn from it.
```

---

## Enhancement Ideas by Difficulty

### 🟢 Beginner-Friendly

- Add new room descriptions
- Create new flavor items (non-functional decorations)
- Write new dialogue for existing NPCs
- Add more keywords to existing items
- Create alternative room descriptions for different parser levels
- Add easter eggs or hidden messages

### 🟡 Intermediate

- Design new puzzle mechanics
- Add new AI components with educational content
- Create side quests or optional objectives
- Implement new enemy types
- Add status effects (buffs/debuffs)
- Create an inventory management system
- Add achievements/unlockables

### 🔴 Advanced

- Implement save/load functionality
- Add networking for multiplayer
- Create a procedural generation system
- Build a level editor
- Add voice acting or TTS
- Implement an AI opponent that learns from player behavior
- Create a modding API

---

## Code Structure Guide

### Key Files

```
src/
├── game/
│   ├── engine.py          # Main game loop and command processing
│   ├── player.py          # Player state and inventory
│   ├── room.py            # Room definitions and connections
│   ├── item.py            # Items and AI components
│   ├── parser.py          # Command parsing (evolves with gameplay)
│   ├── combat.py          # Combat system
│   ├── world.py           # World creation and layout
│   └── ai_components_data.py  # Educational content for AI components
├── graphics/
│   ├── graphics_engine.py # Graphics integration
│   ├── renderer.py        # Wireframe rendering
│   └── scene.py           # 3D scene management
└── main.py                # Entry points

tests/                     # Test suites
```

### Adding New Features

**New AI Component:**
1. Define in `ai_components_data.py`
2. Add to `world.py` in appropriate room
3. Update `ALL_AI_COMPONENTS` dict

**New Room:**
1. Create Room object in `world.py`
2. Connect with `add_exit()` to existing rooms
3. Add items/enemies as needed

**New Command:**
1. Add verb to `parser.py` verb mappings
2. Create handler method in `engine.py`
3. Update help text in `parser.py`

**New Game Mechanic:**
1. Add state tracking to appropriate class
2. Update game loop in `engine.py`
3. Modify command handlers as needed
4. Test thoroughly!

---

## Testing Your Changes

Before sharing your enhanced version:

1. **Run existing tests**
   ```bash
   python tests/run_all_tests.py
   python test_dry_run.py
   python test_world_integrity.py
   ```

2. **Playtest manually**
   - Start new game
   - Test your new feature
   - Try edge cases
   - Verify nothing broke

3. **Test with AI components**
   - Verify parser evolution still works
   - Check that components unlock features properly

4. **Graphics mode testing** (if applicable)
   - Test both text-only and graphics modes
   - Verify UI updates correctly

---

## Documentation Standards

When adding features, please document:

### In Code
- Clear docstrings for new functions/classes
- Comments explaining complex logic
- Type hints where applicable

### In README
- Add to "Development Status" section
- Update controls if you add new keybindings
- Note any new dependencies

### In Changelog
Create an entry like:
```markdown
## [Your Version] - YYYY-MM-DD
### Added
- [Feature name and description]
- [Another feature]

### Changed
- [What you modified]

### Enhanced by
- Your Name (@yourhandle)
```

---

## Sharing Your Version

### Option 1: GitHub
1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with clear messages
4. Push and create a pull request
5. Or share your fork directly!

### Option 2: Direct Sharing
1. Zip your modified version
2. Include a CHANGES.md file describing your additions
3. Share via email, Discord, forums, etc.

### Option 3: Community Hub
- Post to relevant forums (gamedev, AI/ML communities)
- Share on social media with #SKOOLACH
- Create YouTube videos showing your additions
- Write blog posts about what you learned

---

## Educational Focus

Remember: SKOOLACH is primarily an **educational tool**. When adding features:

✅ **Good Additions:**
- Features that teach new concepts
- Mechanics that make learning more engaging
- Content that explains "why" not just "what"
- Improvements to accessibility
- Better visualization of concepts

❌ **Less Aligned:**
- Features that obscure the educational content
- Overly complex mechanics that distract from learning
- Changes that remove educational components
- Additions that make the game feel like grinding

---

## Community Guidelines

- Be respectful of others' additions
- Give credit to previous contributors
- Keep the educational focus
- Make the game better, not just different
- Share your learnings along with your code
- Help others understand your additions
- Accept that your version may be modified by others

---

## Questions?

The beauty of this model is that **there's no central authority**. If you're unsure:
1. Try it and see!
2. Ask your AI assistant
3. Share early versions for feedback
4. Learn from what works and what doesn't

The worst that can happen is someone creates a different branch. The best that can happen is you create something amazing that inspires dozens of other creators!

---

## Example: Adding Your First Feature

Let's walk through adding a simple feature using AI:

### Goal: Add a "hint" command

**Step 1: Talk to your AI**
```
I want to add a HINT command to SKOOLACH that gives players context-aware
hints based on their current location and what they've collected. Here's
the parser.py and engine.py files...
```

**Step 2: Implement with AI guidance**
- AI suggests adding 'hint' to parser verb mappings
- AI helps create `_handle_hint()` method
- AI recommends storing hint text in Room objects

**Step 3: Test**
- Play through the game using hints
- Ask AI to help write tests
- Verify hints are helpful but not too revealing

**Step 4: Document**
- Update README with HINT command
- Add docstrings to your code
- Create a changelog entry

**Step 5: Share**
- Post to community: "Added context-aware hints!"
- Explain why hints improve the learning experience
- Share what you learned about game design

---

## The Long Game

Imagine SKOOLACH in one year, having passed through 100 developers:
- 50 new rooms exploring advanced AI concepts
- Multiple storylines and endings
- Beautiful 3D graphics
- Multiplayer co-op mode
- Available in 10 languages
- Dozens of educational mini-games
- A thriving modding community

**Every contribution, no matter how small, moves toward this vision.**

Your enhancement today might inspire someone else's breakthrough tomorrow.

---

*"The best way to learn is to build. The best way to build is together."*

**Now go forth and create! 🚀**
