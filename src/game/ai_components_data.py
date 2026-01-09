"""Data for all AI components with educational content."""

from .item import AIComponent


def create_tokenizer():
    """Create the Tokenizer component."""
    return AIComponent(
        name="Tokenizer Core",
        description="""
A crystalline cube that pulses with soft blue light. Inside, you can see
text being broken down into tokens - individual words and subwords that
form the basis of language understanding.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: TOKENIZER                                   ║
╚════════════════════════════════════════════════════════════════╝

The tokenizer is the FIRST STEP in processing language. It takes raw
text and breaks it into manageable pieces called "tokens".

Example: "Hello, world!" might become: ["Hello", ",", " world", "!"]

Why tokenization matters:
  • Converts text into a format the model can process
  • Handles unknown words by breaking them into subwords
  • Creates a vocabulary that the model can learn from
  • Modern tokenizers (like BPE or WordPiece) balance between
    character-level and word-level representations

Without tokenization, an AI model would be overwhelmed by the infinite
variety of possible text inputs. Tokens are the foundation of understanding.
""",
        component_type="tokenizer"
    )


def create_embedding_layer():
    """Create the Embedding Layer component."""
    return AIComponent(
        name="Embedding Layer",
        description="""
A sphere containing a dense network of connections between words. Each
word is represented as a point in high-dimensional space, positioned by
semantic meaning.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: EMBEDDINGS                                  ║
╚════════════════════════════════════════════════════════════════╝

Embeddings convert tokens into NUMERICAL VECTORS that capture meaning.

Key concepts:
  • Each token becomes a vector of numbers (e.g., 768 dimensions)
  • Similar words have similar vectors
  • Enables mathematical operations on language
  • "king" - "man" + "woman" ≈ "queen" (famous example)

How it works:
  The model learns these embeddings during training by adjusting
  the numbers to better capture relationships. Words that appear
  in similar contexts end up with similar embeddings.

Why it matters:
  Computers can't understand words directly. Embeddings translate
  language into math, allowing neural networks to process meaning.
""",
        component_type="embedding"
    )


def create_attention_head():
    """Create the Attention Mechanism component."""
    return AIComponent(
        name="Attention Head",
        description="""
A glowing torus that rotates continuously, with beams of light connecting
different points on its surface. This represents how attention focuses on
relevant information across a sequence.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: ATTENTION MECHANISM                         ║
╚════════════════════════════════════════════════════════════════╝

Attention is the BREAKTHROUGH that enabled modern AI. It allows models
to focus on relevant parts of the input when processing each word.

The mechanism:
  When processing "The cat sat on the mat", to understand "sat":
  • Attention looks at ALL other words
  • Calculates relevance scores (how important each word is)
  • Focuses more on "cat" and "mat" than on "the"

Multi-head attention:
  Multiple attention mechanisms run in parallel, each learning to
  focus on different aspects (syntax, semantics, relationships, etc.)

Why transformers work:
  Unlike older models that processed words one-by-one, attention
  allows every word to "see" every other word simultaneously.
  This parallel processing is what makes models like GPT and Claude
  so powerful.

Query, Key, Value:
  Attention uses three learned transformations of each word:
  • Query: "What am I looking for?"
  • Key: "What do I contain?"
  • Value: "What should I output?"
""",
        component_type="attention"
    )


def create_neural_layer():
    """Create the Neural Network Layer component."""
    return AIComponent(
        name="Neural Network Layer",
        description="""
A complex lattice of interconnected nodes, pulsing with computational
energy. Information flows through the network, being transformed at
each layer.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: NEURAL NETWORK LAYERS                       ║
╚════════════════════════════════════════════════════════════════╝

Neural networks are stacks of transformation layers. Modern language
models have MANY layers (GPT-3 has 96, Claude has many as well).

What each layer does:
  1. Receives input from previous layer
  2. Applies learned transformations (matrix multiplications)
  3. Adds non-linearity (activation functions like ReLU, GELU)
  4. Passes output to next layer

Layer types in transformers:
  • Multi-head attention layers (focus on relationships)
  • Feed-forward layers (process individual positions)
  • Layer normalization (stabilize learning)
  • Residual connections (help information flow)

Deep networks:
  Early layers learn basic patterns (grammar, word relationships)
  Middle layers learn abstract concepts (topics, sentiment)
  Late layers learn complex reasoning and generation

Why depth matters:
  More layers = more complex transformations = better understanding
  But diminishing returns exist, and very deep networks are hard to train.
""",
        component_type="neural_layer"
    )


def create_training_data():
    """Create the Training Data component."""
    return AIComponent(
        name="Training Data Archive",
        description="""
An enormous crystalline database, containing compressed knowledge from
billions of text examples. Swirling patterns show information being
organized and indexed.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: TRAINING DATA                               ║
╚════════════════════════════════════════════════════════════════╝

Training data is the KNOWLEDGE that an AI model learns from. For large
language models, this means massive amounts of text.

What training data includes:
  • Books, articles, websites (Common Crawl)
  • Code repositories (GitHub, StackOverflow)
  • Conversations, forums, Q&A sites
  • Academic papers, documentation
  • Curated datasets for specific tasks

The training process:
  1. The model reads examples from the training data
  2. Tries to predict the next word/token
  3. Measures how wrong it was (loss function)
  4. Adjusts its internal weights to do better next time
  5. Repeats billions of times

Quality matters:
  • Diverse data → versatile model
  • High-quality data → better outputs
  • Biased data → biased model
  • Curated data helps the model learn what's valuable

Scale:
  GPT-3 trained on ~300 billion tokens
  Modern models train on trillions of tokens
  More data generally means better performance (with diminishing returns)
""",
        component_type="training_data"
    )


def create_optimizer():
    """Create the Optimizer component."""
    return AIComponent(
        name="Optimizer Module",
        description="""
A device showing flowing gradients and weight adjustments. Numbers
constantly update as the system searches for the optimal configuration.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: OPTIMIZER                                   ║
╚════════════════════════════════════════════════════════════════╝

The optimizer is HOW the model learns. It adjusts the billions of
parameters (weights) to improve performance.

Gradient descent:
  • Calculate how wrong the model is (loss)
  • Compute gradients (which direction to adjust each weight)
  • Update weights to reduce loss
  • Repeat millions of times

Popular optimizers:
  • SGD: Simple but effective
  • Adam: Adaptive learning rates, very popular
  • AdamW: Adam with weight decay (regularization)

Key concepts:
  • Learning rate: How big each adjustment step is
  • Momentum: Use previous gradients to smooth updates
  • Adaptive rates: Different learning rates for different parameters

The challenge:
  With billions of parameters, finding the right values is like
  navigating a landscape with billions of dimensions. The optimizer
  is the guide that finds the path to good performance.

Fun fact:
  Training large models requires careful optimizer tuning. The wrong
  learning rate can cause training to diverge (explode) or stagnate.
""",
        component_type="optimizer"
    )


def create_inference_engine():
    """Create the Inference Engine component."""
    return AIComponent(
        name="Inference Engine",
        description="""
A streamlined processing unit that generates outputs at high speed.
You can see tokens being predicted one after another in rapid
succession.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: INFERENCE                                   ║
╚════════════════════════════════════════════════════════════════╝

Inference is the process of USING a trained model to generate outputs.
After training is complete, the model's weights are frozen and it
generates responses.

The inference loop (for text generation):
  1. Receive input prompt
  2. Process through all layers
  3. Predict next token (word/subword)
  4. Add predicted token to input
  5. Repeat until done (special stop token or max length)

This is called "autoregressive generation" - each token depends on
all previous tokens.

Key considerations:
  • Temperature: Controls randomness (higher = more creative)
  • Top-k/Top-p: Limits choices to most likely tokens
  • Beam search: Explores multiple possibilities simultaneously
  • Caching: Reuse computations from previous tokens (KV cache)

Speed matters:
  Inference must be FAST for real-time use. Optimizations include:
  • Quantization (use smaller numbers)
  • Batching (process multiple requests together)
  • Specialized hardware (GPUs, TPUs)
  • Model compression

The inference engine is what you interact with when you use an AI.
""",
        component_type="inference"
    )


def create_context_window():
    """Create the Context Window component."""
    return AIComponent(
        name="Context Window",
        description="""
A scrolling display that shows how the model maintains awareness of
previous text. The window slides forward, keeping recent information
in focus while older information fades.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: CONTEXT WINDOW                              ║
╚════════════════════════════════════════════════════════════════╝

The context window is HOW MUCH TEXT the model can "see" at once.
It's like the model's short-term memory.

Why it matters:
  The model can only pay attention to tokens within its context window.
  Anything outside that window is invisible to it.

Context length examples:
  • Early GPT: 512-1024 tokens
  • GPT-3: 2048-4096 tokens
  • GPT-4: 8K-32K tokens
  • Claude: 100K-200K tokens
  • Specialized models: 1M+ tokens

The technical challenge:
  Attention is O(n²) - doubling context length quadruples computation!
  Innovations like Flash Attention make longer contexts feasible.

Why longer is better:
  • Remember more of the conversation
  • Process entire documents
  • Maintain consistency over long outputs
  • Reduce need for summarization

Trade-offs:
  • Longer context = slower inference
  • Longer context = more memory needed
  • Finding the right balance is key

Modern AI systems often use techniques like:
  • Sliding window attention
  • Hierarchical attention
  • Retrieval-augmented generation (RAG)
""",
        component_type="context"
    )


def create_fine_tuning_module():
    """Create the Fine-tuning Module component."""
    return AIComponent(
        name="Fine-tuning Module",
        description="""
A calibration device that shows the model being adjusted for specific
tasks. General knowledge being refined into specialized expertise.

╔════════════════════════════════════════════════════════════════╗
║ EDUCATIONAL NOTE: FINE-TUNING                                 ║
╚════════════════════════════════════════════════════════════════╝

Fine-tuning is the process of taking a pre-trained model and
SPECIALIZING IT for specific tasks or behaviors.

The process:
  1. Start with a base model trained on general data
  2. Continue training on specialized data
  3. Use a smaller learning rate (don't forget old knowledge)
  4. Train for fewer steps (don't overfit)

Types of fine-tuning:
  • Supervised fine-tuning (SFT): Learn from examples
  • Instruction tuning: Learn to follow instructions
  • RLHF: Reinforcement learning from human feedback
  • LoRA/Adapters: Only update small parts of the model

Why fine-tune instead of training from scratch?
  • MUCH faster and cheaper
  • Requires less data
  • Leverages existing knowledge
  • Can specialize for domains (medical, legal, code, etc.)

Examples:
  • ChatGPT: Base GPT model + instruction tuning + RLHF
  • Code models: Base model + code-heavy fine-tuning
  • Domain experts: Base model + specialized documents

The base model learns "how to language"
Fine-tuning teaches "how to be helpful/accurate/safe/specialized"
""",
        component_type="fine_tuning"
    )


# Create a dictionary for easy access
ALL_AI_COMPONENTS = {
    'tokenizer': create_tokenizer,
    'embedding': create_embedding_layer,
    'attention': create_attention_head,
    'neural_layer': create_neural_layer,
    'training_data': create_training_data,
    'optimizer': create_optimizer,
    'inference': create_inference_engine,
    'context': create_context_window,
    'fine_tuning': create_fine_tuning_module,
}
