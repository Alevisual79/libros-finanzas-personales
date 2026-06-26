# Neural Networks Explained
## The Architecture Behind the Intelligence

**Series 1: AI Fundamentals — Book 3 of 10**

---

*Copyright © 2026 Enrique Padrón. All rights reserved. No part of this publication may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.*

---

> **Disclaimer:** The use of the information in this book is the sole responsibility of the reader.

---

## Prologue

When people ask how AI 'thinks', they often get one of two answers: 'it's just statistics' (dismissive) or 'it's too complex to explain' (evasive). Neither is satisfying or accurate.

Neural networks can be explained clearly. Not the mathematics — the concepts. And the concepts matter because they determine what these systems can and cannot do.

---

## Chapter 1: The Neuron Metaphor

A biological neuron receives signals from many other neurons, combines them, and fires if the combined input exceeds a threshold.

An artificial neuron does something similar in mathematics: it receives numbers from connected neurons, multiplies each by a weight, sums them, applies an activation function, and produces an output.

The metaphor is imperfect — artificial neurons are vastly simpler than biological ones — but it provides a useful mental image.

---

## Chapter 2: Layers and Depth

A neural network organizes neurons into layers:

**Input layer:** Receives the raw data (pixel values of an image, token IDs of text)
**Hidden layers:** Intermediate layers that transform representations
**Output layer:** Produces the final prediction

'Deep learning' simply means the network has many hidden layers (depth). The depth allows the network to learn hierarchical representations: simple features in early layers, complex combinations in later layers.

---

## Chapter 3: Learning by Adjusting Weights

A neural network learns by adjusting the weights on connections between neurons.

The process:
1. Forward pass: input flows through the network, producing an output
2. Compare output to correct answer, calculate error (loss)
3. Backward pass: error propagates backward, indicating how each weight contributed
4. Adjust weights to reduce error (gradient descent)
5. Repeat for millions of examples

After enough training, the weights encode patterns that produce correct outputs for new inputs.

---

## Chapter 4: Convolutional Neural Networks

CNNs are specialized for processing grid-like data: primarily images.

The key innovation: convolutional layers scan the input with a small filter, looking for patterns regardless of where they appear in the image. The network learns to recognize edges, then shapes, then objects.

Applications: image classification, object detection, medical imaging, facial recognition, video analysis.

CNNs are why your phone can recognize your face and why radiologists are being augmented (and in some cases replaced) by AI in medical imaging.

---

## Chapter 5: Recurrent Neural Networks and Sequences

RNNs process sequential data by maintaining a hidden state that carries information across time steps.

Applications: speech recognition, machine translation, text generation, time series prediction.

The key challenge: maintaining relevant information over long sequences. Vanilla RNNs struggle with this. LSTM (Long Short-Term Memory) networks addressed it with gating mechanisms.

Before the Transformer, RNNs were the dominant architecture for language tasks.

---

## Chapter 6: The Transformer — The Architecture That Changed Everything

In 2017, a Google paper titled 'Attention Is All You Need' introduced the Transformer architecture. It changed everything.

The key innovation: the attention mechanism, which allows the model to consider all parts of the input simultaneously, weighting each based on relevance to the current position.

Transformers scale much better than RNNs and can be trained in parallel. This made training on massive datasets practical. GPT, BERT, Claude, Gemini — all are based on the Transformer.

---

## Chapter 7: Attention and Context

The attention mechanism is the heart of the Transformer.

For each position in the input, attention computes a weighted sum of all other positions, where weights reflect how relevant each position is.

Example: in the sentence 'The bank was steep and eroded', the model must determine that 'bank' means a river bank, not a financial institution. Attention allows it to consider 'steep' and 'eroded' when interpreting 'bank', across however many words separate them.

This is why Transformers handle long-range dependencies much better than RNNs.

---

## Chapter 8: Scale and Emergent Abilities

One of the most surprising findings in deep learning: some abilities only emerge in large models.

Small models are incapable of certain tasks. Larger versions of the same architecture suddenly display them. No one fully understands why.

Examples of emergent abilities: multi-step arithmetic, few-shot learning (learning from a few examples in the prompt), chain-of-thought reasoning.

This makes LLMs difficult to predict from smaller experiments — and raises fundamental questions about how intelligence scales.

---

## Chapter 9: Fine-Tuning and Alignment

A pre-trained LLM is trained to predict text. It does not inherently know how to be helpful, honest, or safe.

Fine-tuning adapts a pre-trained model to specific behavior:

**Supervised fine-tuning:** Train on examples of desired behavior (question-answer pairs with good responses)
**RLHF:** Human raters compare model outputs; the model is trained to produce outputs raters prefer

This is how ChatGPT, Claude, and Gemini are shaped into assistants that follow instructions and decline harmful requests, rather than just predicting likely text.

---

## Chapter 10: What the Architecture Reveals

Understanding neural network architecture reveals important truths:

- LLMs are not databases: they interpolate, not retrieve
- Context window is a real limitation, not an implementation detail
- Temperature controls randomness, not creativity in any meaningful sense
- 'Understanding' in LLMs is a contested concept — the architecture does not include explicit knowledge representation
- Emergent capabilities make LLMs difficult to predict, audit, and control

Isabel's takeaway: the HR systems she oversees that use AI for candidate screening are using the same fundamental architecture. Understanding it helps her ask better questions about bias and fairness.

---

## Epilogue

Neural networks are not magic. They are a family of architectures that learn complex transformations from data, guided by the mathematics of optimization.

Understanding the architecture does not tell you everything about AI behavior — emergent properties remain surprising even to researchers. But it tells you enough to be a sophisticated user and a responsible decision-maker.

---

*Book 3 of the AI Applied Intelligence Collection, Book 3 of 10 of Series 1: AI Fundamentals.*

---

*If you found this book valuable, please consider leaving a review on Amazon. It takes less than a minute and makes a real difference for independent authors.*

---

## About the Author

Enrique Padrón was born in the Canary Islands, Spain. Twenty-five years across different companies taught him something few dare to say out loud: people don't fail because they lack information. They fail because nobody gave them the right tools at the right moment. This collection exists to change that. Each book distills what truly works — no filler, no empty theory. Developed with the support of artificial intelligence to carry that knowledge further than any single author could reach alone.