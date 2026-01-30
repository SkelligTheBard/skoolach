"""Test the quantum debugger spawn mechanic."""

import sys
sys.path.insert(0, 'src')

from game import GameEngine, create_world

def test_debugger_spawn():
    """Test that debugger spawns after collecting all 9 AI components."""
    print("=" * 70)
    print("QUANTUM DEBUGGER SPAWN TEST")
    print("=" * 70)

    engine = GameEngine()
    starting_room = create_world()
    engine.setup(starting_room, player_name="Tester")

    print(f"\n1. Memory Corridor reference: {engine.memory_corridor is not None}")
    print(f"   Quantum Debugger reference: {engine.quantum_debugger is not None}")
    print(f"   Debugger spawned: {engine.debugger_spawned}")

    # Check Memory Corridor items before
    if engine.memory_corridor:
        items_before = [item.name for item in engine.memory_corridor.items]
        print(f"\n2. Items in Memory Corridor before: {items_before}")
        print(f"   Has debugger: {'quantum debugger' in [i.lower() for i in items_before]}")

    # Simulate collecting 9 AI components
    print(f"\n3. Simulating collection of 9 AI components...")

    # Navigate and collect components
    components_to_collect = [
        ("go north", "go north", "take tokenizer"),  # Tokenizer
        ("go south", "go west", "take embeddings"),  # Embeddings
        ("go south", "use flashlight", "take training"),  # Training Data
        ("go north", "go northeast", "take attention"),  # Attention
        ("go southwest", "go northeast", "take neural"),  # Neural Network
        ("go south", "go south", "take inference"),  # Inference
        ("go north", "go east", "take optimizer"),  # Optimizer
        ("go west", "go east", "take context"),  # Context
        ("go east", "take fine"),  # Fine-tuning
    ]

    engine.process_command("take flashlight")

    for commands in components_to_collect:
        for cmd in commands:
            response = engine.process_command(cmd)
            if "AI COMPONENT ACQUIRED" in response or "FINAL KEY UNLOCKED" in response:
                print(f"   Component collected! Total: {len(engine.player.ai_components_collected)}")
                if "FINAL KEY" in response:
                    print(f"\n   *** DEBUGGER SPAWN MESSAGE: ***")
                    # Extract just the notification part
                    if "SYSTEM NOTIFICATION" in response:
                        lines = response.split('\n')
                        for line in lines:
                            if '═' in line or '⚡' in line or 'FINAL KEY' in line or 'QUANTUM DEBUGGER' in line:
                                print(f"   {line}")

    print(f"\n4. After collecting all components:")
    print(f"   Total AI components: {len(engine.player.ai_components_collected)}")
    print(f"   Debugger spawned flag: {engine.debugger_spawned}")

    # Check Memory Corridor items after
    if engine.memory_corridor:
        items_after = [item.name for item in engine.memory_corridor.items]
        print(f"\n5. Items in Memory Corridor after: {items_after}")
        has_debugger = any('debugger' in item.lower() for item in items_after)
        print(f"   Has debugger: {has_debugger}")

    print("\n" + "=" * 70)
    print("TEST COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_debugger_spawn()
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
