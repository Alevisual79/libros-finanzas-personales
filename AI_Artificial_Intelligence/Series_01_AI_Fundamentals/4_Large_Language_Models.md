# Large Language Models
## How ChatGPT and Its Cousins Actually Work

**Series 1: AI Fundamentals — Book 4 of 10**

---

*Copyright © 2026 Enrique Padrón. All rights reserved. No part of this publication may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.*

---

> **Disclaimer:** The use of the information in this book is the sole responsibility of the reader.

---

### Prologue
Jordan had been using ChatGPT daily for six months before a colleague asked him a simple question: "How does it actually know what to say?" Jordan paused. He could describe what ChatGPT did — answer questions, write code, summarize documents — but he realized he had no idea how it worked at the level that mattered. He was operating a powerful tool he fundamentally did not understand.

That gap matters. When you understand how a large language model generates text, you understand why it fails when it fails, why certain prompt strategies work, and where its limits are structural rather than temporary. You stop being surprised by hallucinations and start predicting them. You stop wondering why it refuses certain requests and start understanding the design choices involved.

This book is about the mechanism. Not the mathematics — the concepts behind the mechanism. By the end, Jordan's question has a real answer: one that changes how you use these tools.

---

## Chapter 1: What Makes a Language Model "Large"

The word "large" in large language model refers to two things: the number of parameters (the internal numerical values the model adjusts during training) and the amount of training data. GPT-3, released in 2020, had 175 billion parameters. GPT-4 is estimated to have over a trillion. Claude 3 Opus, Gemini Ultra, and their contemporaries operate in similar ranges.

To understand what parameters are, think of them as the knobs in an enormous mixing board. During training, all those knobs are adjusted billions of times until the model produces the right output for each training example. The final position of every knob encodes the patterns the model has learned from text.

Why does size matter? Because language is extraordinarily complex. The patterns that allow a model to understand context, maintain coherence across a long document, translate between languages, and reason about abstract problems require enormous representational capacity. Small models can complete sentences; large models can write coherent essays, debug code, and explain counterarguments. Scale unlocks qualitatively different behaviors — a phenomenon researchers call emergent capabilities.

The "large" in LLM also refers to training data. Models like GPT-4 were trained on hundreds of billions of words: web pages, books, scientific papers, code repositories, forums, news articles. This breadth of data is why they can discuss history, science, law, and programming with apparent fluency. They have, in a real sense, been exposed to the condensed output of human writing.

---

## Chapter 2: The Core Mechanism — Predicting the Next Token

At its core, a large language model does one thing: it predicts the next token given everything that came before it.

A token is not quite a word — it is a chunk of text, roughly three to four characters on average. The word "running" might be one token; "unbelievable" might be two. A model like GPT-4 has a vocabulary of roughly 100,000 tokens.

Given the input "The capital of France is," the model assigns a probability to every token in its vocabulary as the next token. The token "Paris" gets a very high probability. "London" gets a somewhat lower but nonzero probability. "Banana" gets a negligible probability. The model samples from this distribution — usually, but not always, choosing the highest-probability option — and produces "Paris." Then it does the same thing again for the token after that, and again, until it generates a complete response.

This is not retrieval. The model is not looking up "capital of France" in a database. It is computing probabilities based on patterns in its parameters — patterns derived from having seen sentences like "the capital of France is Paris" many times during training, combined with deeper patterns about geography, language structure, and factual relationships.

This mechanism explains both the power and the limits of LLMs. The power: with enough training data and parameters, the model learns extraordinarily sophisticated patterns. The limit: it is always predicting likely text, not verifying facts. It will produce a confident, fluent sentence that sounds like what a knowledgeable person would say — whether or not it is true.

---

## Chapter 3: Transformers and Attention

The architecture that makes modern LLMs possible is the Transformer, introduced in a 2017 paper titled "Attention Is All You Need." Before Transformers, language models used recurrent architectures that processed text sequentially, one token at a time. Transformers process all tokens in parallel, using a mechanism called attention.

Attention allows the model to weigh how relevant each part of the input is to each other part. When processing the word "it" in "The trophy didn't fit in the bag because it was too big," attention allows the model to figure out that "it" refers to "trophy" by weighing the relationships between all words simultaneously.

This might seem technical, but the practical implication is significant: Transformers can handle much longer contexts than older architectures, and they can be trained much more efficiently using modern hardware. These properties allowed researchers to train increasingly large models on increasingly large datasets, producing the LLMs we use today.

The context window is a direct product of the Transformer architecture. Every LLM has a context window — the maximum amount of text it can process at once, measured in tokens. GPT-4's context window is 128,000 tokens (roughly 100,000 words). Claude 3's extends to 200,000 tokens. Within the context window, the model can attend to everything. Beyond it, earlier content is simply gone. This is not a temporary limitation — it is a structural feature of how attention works.

---

## Chapter 4: Pretraining and Fine-Tuning

Building a capable LLM happens in stages. The first and most expensive stage is pretraining: the model is trained on an enormous corpus of text to predict the next token, adjusting hundreds of billions of parameters over weeks or months on thousands of specialized chips. The cost of pretraining frontier models is estimated in the hundreds of millions of dollars.

After pretraining, the model has absorbed vast knowledge about language and the world — but it produces raw text continuations, not helpful responses. If you ask a pretrained model "What is the capital of France?" it might respond by generating more text that looks like a quiz: "What is the capital of Germany? What is the capital of Italy?" — because that is the pattern it has seen in similar contexts.

Fine-tuning transforms the pretrained model into an assistant. The most important technique is Reinforcement Learning from Human Feedback (RLHF). Human raters evaluate model outputs and indicate which responses are better. A separate "reward model" learns to predict human preferences. The LLM is then trained to produce responses the reward model rates highly.

This is why ChatGPT and Claude answer your questions helpfully instead of completing your sentences randomly. The pretraining gives them knowledge and language ability; the fine-tuning shapes how they use that ability. It also explains why different models have different "personalities" — the fine-tuning choices reflect the values and priorities of the company that built the model.

---

## Chapter 5: The Temperature and Sampling

When a language model generates text, it does not simply always choose the highest-probability next token. If it did, responses would be deterministic and often repetitive. Instead, models sample from the probability distribution, with settings that control how much randomness to introduce.

Temperature is the most commonly discussed setting. At temperature 0, the model always picks the highest-probability token — maximum consistency, minimum variation. At higher temperatures (up to 2.0 in many systems), lower-probability tokens get selected more often, producing more varied and sometimes more creative outputs.

The practical implications: for tasks requiring consistency (extracting data, answering factual questions), lower temperatures work better. For creative tasks (brainstorming, writing fiction, generating marketing variations), higher temperatures are more useful. Most systems set temperature at 0.7-1.0 by default, balancing consistency and variety.

Other sampling strategies — top-p (nucleus sampling) and top-k — further control which tokens are eligible for selection. These technical details matter less than understanding the underlying principle: LLM output is probabilistic, not deterministic. The same prompt will produce somewhat different responses on different runs. This is not a bug; it is a design choice that reflects the nature of text generation.

---

## Chapter 6: Why LLMs Hallucinate

Hallucination — the confident generation of false information — is not a flaw that will be patched out of LLMs. It is a predictable consequence of how they work.

LLMs predict likely text. They do not have a separate "fact-checking" module. When they generate a claim, they are producing the text that seems most probable given their training data and the current context — not the text that is factually correct. If the training data contained inaccuracies (and it did), the model may reproduce them. If a plausible-sounding but false claim fits the pattern of the text the model is generating, it will produce that claim.

The specific failure modes are predictable. LLMs hallucinate most when asked about: recent events (after their training cutoff), obscure facts (where training data is sparse), specific numerical data (prices, statistics, dates), proper nouns and citations (fictional sources sound plausible), and complex multi-step reasoning (errors compound across steps).

Understanding hallucination changes how you use LLMs. For tasks where accuracy is critical — legal research, medical information, financial data — you always verify. For tasks where fluency and structure matter more than specific facts — drafting communications, brainstorming ideas, explaining concepts you already understand — hallucination risk is lower and less consequential. The tool is not broken; you just need to know when to deploy it and when to double-check.

---

## Chapter 7: Context Windows and Memory

One of the most practically important aspects of LLMs is the context window: the amount of text the model can process in a single interaction. Everything within the context window is available to the model as it generates its response. Everything outside it is not.

Modern context windows are large: 100,000 to 200,000 tokens for frontier models, meaning you can paste in entire books and have a meaningful conversation about them. But context windows have two important properties that users often misunderstand.

First, LLMs do not retain memory between conversations. When you start a new chat, the model has no recollection of previous sessions. The conversation history within a session is maintained by sending the full prior context to the model on each turn — which is why long conversations can eventually hit context limits.

Second, the model's ability to use context is not uniform. Research shows that information at the very beginning and very end of a long context is used most reliably; information buried in the middle is less reliably attended to. This matters when you are pasting a large document and asking questions about specific parts of it.

Memory systems (where important information from past conversations is summarized and injected into future contexts) are increasingly common in AI products. These are engineering solutions built on top of LLMs, not capabilities of the models themselves. Understanding the distinction helps you understand why some AI systems seem to "remember" things and others do not.

---

## Chapter 8: The Major Models — GPT, Claude, Gemini, and Others

The LLM landscape as of 2024-2025 is competitive, with several frontier models operating at comparable capability levels.

**GPT-4 and GPT-4o (OpenAI):** The models behind ChatGPT and the OpenAI API. GPT-4o ("omni") integrates text, vision, and audio natively in a single model, enabling real-time voice conversation and image understanding. GPT-4 established many benchmarks that competing models now target.

**Claude 3 family (Anthropic):** Claude 3 Haiku (fast and cheap), Claude 3 Sonnet (balanced), and Claude 3 Opus (most capable) represent a tiered approach. Anthropic has placed particular emphasis on safety research and on Constitutional AI — a technique for training models to follow ethical principles more reliably than RLHF alone.

**Gemini (Google DeepMind):** Google's frontier model, available in Ultra, Pro, and Nano sizes. Gemini was designed from the ground up to be multimodal — processing text, images, audio, and video natively. It is deeply integrated with Google's search and productivity products.

**Llama (Meta):** Unlike the above, Llama models are open-weights — Meta releases the model weights publicly, allowing anyone to download and run them. This has enabled a large ecosystem of fine-tuned variants and local deployment options.

Understanding the competitive landscape helps you choose the right tool. Each model has different strengths, pricing, context windows, and policies. No single model dominates on every task.

---

## Chapter 9: Using LLMs Effectively — The Practical Layer

Understanding how LLMs work translates directly into better usage strategies.

**Be specific in prompts.** The model generates text based on patterns in your input. Vague prompts produce vague outputs. "Write an email" versus "Write a professional email to a client explaining a one-week delay in their project delivery, apologetic but confident in resolution" produces dramatically different results.

**Provide context.** The model has no knowledge of your specific situation, company, or preferences beyond what you tell it. Adding context — role, audience, constraints, examples — improves output quality substantially.

**Use structured prompts for complex tasks.** Breaking a complex task into steps ("First, identify the key issues. Then, for each issue, suggest a solution. Finally, rank solutions by feasibility") guides the model through a better reasoning process.

**Verify outputs.** Treat LLM outputs as drafts that may need fact-checking. This is most important for specific claims, citations, statistics, and technical details.

**Iterate.** Unlike a search engine, LLMs benefit from follow-up. "Make the tone more formal," "Shorten this by 30%," "Add a section on the budget implications" — iterative refinement almost always produces better results than trying to get the perfect output in a single prompt.

Jordan adopted these practices and found that his productivity with AI tools roughly doubled — not because the model changed, but because his understanding of how it worked let him communicate with it more effectively.

---

## Chapter 10: The Future of Large Language Models

The LLM landscape is evolving rapidly, but several directions are clear enough to describe.

**Multimodality is becoming standard.** Models increasingly handle text, images, audio, and video in a unified architecture. GPT-4o and Gemini Ultra both demonstrate this. The capability gap between text-only and multimodal models is closing quickly.

**Context windows will keep growing.** Longer contexts enable more complex tasks — processing entire codebases, analyzing book-length documents, maintaining longer conversation histories. The limiting factor is now more about cost and speed than architectural capability.

**Reasoning is improving.** Models like GPT-4 with chain-of-thought prompting and specialized reasoning models (OpenAI o1) show dramatically better performance on multi-step problems. Separating "fast generation" from "slow reasoning" is a productive research direction.

**Local models are becoming viable.** Models that run on consumer hardware — Meta's Llama 3, Microsoft's Phi-3, Google's Gemma — are closing the capability gap with frontier models for many tasks. This matters for privacy, cost, and offline use.

**The gap between models is narrowing.** The extraordinary advantage of the frontier models in 2022 has shrunk as competition intensified. For many everyday tasks, GPT-4, Claude 3 Sonnet, and Gemini Pro are comparable. The choice increasingly depends on specific strengths, pricing, and integration.

What will not change: the core mechanism. LLMs will continue to predict tokens, generate probabilistic outputs, and fail in the specific ways described in this book. Understanding the fundamentals stays useful regardless of which model becomes state-of-the-art next quarter.

---

## Epilogue

Jordan now has an answer for his colleague: the model has absorbed patterns from an enormous corpus of human text, encoded those patterns in hundreds of billions of numerical parameters, and generates responses by predicting the most probable next token given your input. It is not looking things up. It is not reasoning in the way humans reason. It is predicting, fluently and at scale, what text should come next.

That understanding changed how Jordan uses AI. He stopped being surprised when the model invented a source — of course it did; it was predicting what a knowledgeable citation would look like. He started writing better prompts — of course context helps; the model can only work with what you give it. He became a more effective user not by learning more about AI in the abstract but by understanding the specific mechanism that produces its outputs.

The LLM landscape will look different in twelve months. The concepts in this book will not. Build the mental model; the specific knowledge will update itself.

---

*Book 4 of the AI & Artificial Intelligence Collection, Book 4 of 10 of Series 1: AI Fundamentals.*

---

*If you found this book valuable, please consider leaving a review on Amazon. It takes less than a minute and makes a real difference for independent authors.*

---

## About the Author

Enrique Padrón was born in the Canary Islands, Spain. Twenty-five years across different companies taught him something few dare to say: people don't fail because they lack information, they fail because nobody gave them the right tools at the right moment. This collection exists to change that. Each book distills what truly works, no filler, no empty theory. Developed with the support of artificial intelligence to carry that knowledge further than any author could reach alone.