# How AI Actually Works

**Series 1: AI Fundamentals — Book 1 of 10**

*Copyright © 2026 Enrique Padrón. All rights reserved. No part of this publication may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.*

> **Disclaimer:** The use of the information in this book is the sole responsibility of the reader.

## A Clear Guide for Non-Technical People

### Prologue
Elena opened her laptop and typed 'explain machine learning' into ChatGPT. The response was clear, well-written, and felt helpful. But when her colleague asked her to explain, in her own words, what machine learning actually was, she found she could not.

This is the gap this book closes. Not a technical deep-dive — a clear understanding of the mechanisms behind the AI you already use.

---

## Chapter 1: The Old Way of Programming

Traditional software follows rules written by humans. A spam filter built the old way contains hundreds of hand-written rules: if the email contains 'lottery' and 'winner' and 'click here', mark as spam.

The problem: reality is more complex than any set of hand-written rules. New types of spam emerge faster than engineers can write rules to catch them.

AI takes a different approach: instead of writing rules, it learns patterns from examples.

---

## Chapter 2: Learning from Examples

A machine learning system learns by studying thousands of examples. To build a spam filter with ML, you show the system millions of emails labeled 'spam' or 'not spam'. The system finds patterns in the data — combinations of words, sender characteristics, formatting — that correlate with spam.

No engineer writes the rules. The system discovers them from the data.

The result often performs better than hand-crafted rules because it finds patterns humans would never think to look for.

---

## Chapter 3: Training, Testing, Deploying

Building an AI system has three phases:

**Training:** The system studies labeled examples and adjusts its internal parameters to minimize errors. This is the computationally expensive phase that requires powerful hardware.

**Testing:** The system is evaluated on examples it has never seen, to verify it has learned general patterns rather than memorizing the training data.

**Deployment:** The trained system is released for real-world use, making predictions on new inputs.

The quality of the training data largely determines the quality of the resulting system.

---

## Chapter 4: What Neural Networks Are

Neural networks are the architecture behind most modern AI. They are loosely inspired by the brain: layers of mathematical nodes, each performing a simple computation, connected in ways that allow the network to represent very complex functions.

A deep neural network has many layers — hence 'deep learning'. The early layers learn simple patterns (edges in images, common word combinations in text). Later layers combine those patterns into more complex representations.

The network learns by adjusting the strength of connections between nodes during training, guided by feedback on whether its output is correct.

---

## Chapter 5: Large Language Models

An LLM is a neural network trained on massive amounts of text to predict the next word (or token) in a sequence. During training, the model processes text, makes a prediction, receives feedback on whether the prediction was correct, and adjusts accordingly — billions of times.

The result is a model that has, in some sense, absorbed patterns from nearly all text available on the internet, in books, and in other sources.

When you type a message to ChatGPT or Claude, the model predicts, token by token, the most probable continuation given your input and everything it learned during training.

---

## Chapter 6: Why LLMs Sometimes Get Things Wrong

LLMs generate text by predicting likely continuations. They do not verify facts. They do not know when they are uncertain. They produce fluent, confident text regardless of whether the content is accurate.

This explains 'hallucination' — when an AI states false information with the same confidence as true information.

The mechanism — predicting likely text — does not include a truth-checking step. A model that has seen many texts claiming X will reproduce X confidently, even if X is wrong.

Understanding this makes you a better user: you know when to verify and when the output can be trusted without verification.

---

## Chapter 7: The Difference Between Generative and Predictive AI

Not all AI is the same type.

**Predictive AI** takes inputs and produces a classification or a number: spam or not spam, probability of loan default, likely medical diagnosis. This type of AI has been deployed in business for decades.

**Generative AI** produces new content: text, images, audio, video, code. LLMs are the most visible example. This type of AI has scaled dramatically since 2020 and is responsible for most of the current public attention to AI.

Most conversations about 'AI' today are really conversations about generative AI, specifically LLMs.

---

## Chapter 8: What AI Cannot Do

Knowing the limits is as important as knowing the capabilities.

AI cannot:
- Verify its own outputs for factual accuracy
- Access information not in its training data (unless connected to external tools)
- Learn from a conversation (by default, the model does not update from your chat)
- Understand intent beyond the words you use
- Make ethical judgments
- Guarantee consistent outputs (the same prompt can produce different responses)

These are not temporary limitations to be solved next year. They are structural features of how current AI systems work.

---

## Chapter 9: The Role of Human Judgment

The right mental model: AI is a powerful first-draft generator and pattern recognizer. Human judgment provides what AI cannot: domain expertise, ethical evaluation, verification of facts, and accountability for outcomes.

Elena's code generation workflow: she uses AI to generate first drafts of code, then applies her expertise to evaluate correctness, security, and architecture. The AI speeds up her production; her judgment determines what is actually shipped.

This collaboration model — AI for production, human for judgment — applies across virtually every professional domain.

---

## Chapter 10: Building Your AI Mental Model

A useful mental model for AI:

1. AI learns patterns from data, not rules from programmers
2. The quality of outputs depends heavily on the quality of training data
3. LLMs predict likely text, they do not reason or verify facts
4. AI is excellent at well-defined, text-based production tasks
5. Human judgment is essential for evaluation, ethics, and accountability

With this model, you can make sensible predictions about when AI will be helpful and when it will be unreliable — without needing to understand the mathematics.

---

## Epilogue

The goal of this book was not to make you a machine learning engineer. It was to give you a mental model that holds up: one that explains why AI is impressive in the ways it is impressive, and limited in the ways it is limited.

Elena can now explain machine learning to her colleague. And more importantly, she knows why the spam filter works better than the rule-based system, why ChatGPT occasionally makes up citations, and why the data quality matters as much as the algorithm.

That understanding is the foundation for everything else in this collection.

---

*Book 1 of the AI Applied Intelligence Collection, Book 1 of 10 of Series 1: AI Fundamentals.*

---

*If you found this book valuable, please consider leaving a review on Amazon. It takes less than a minute and makes a real difference for independent authors.*

---

## About the Author

Enrique Padrón was born in the Canary Islands, Spain. Twenty-five years across different companies taught him something few dare to say: people don't fail because they lack information, they fail because nobody gave them the right tools at the right moment. This collection exists to change that. Each book distills what truly works, no filler, no empty theory. Developed with the support of artificial intelligence to carry that knowledge further than any author could reach alone.