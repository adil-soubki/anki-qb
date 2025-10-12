"""LLM prompt templates for flashcard generation."""

PROMPT_FNX_18 = """
Your task is to create a deck of flashcards from the provided text focusing on optimizing the content for maximum rentention and learning effectiveness. Ensure that each flashcard is clearly written and adheres to the specified instructions

Instructions to create flashcards:

1. **FORMAT:**
  1.1 Contruct a table with two columns: "Question", "Answer"
  1.2 Each row of the "Question" column should contain a single quesiton
  1.3 The "Answer" column should contain the succinct answer to the question in the corresponding row of the "Question" column.

2. **CREATE FLASHCARDS:**
  2.1. Keep the flashcards simple, clear, and focused on the most important information.
  2.2. Make sure the questions are specific and unambiguous.
  2.3. Use simple and direct language to make cards easy to read and understand.
  2.4. Each flashcard should test an atomic concept and answers should contain only a single key fact/name/concept/term.
  2.4. SIMPLIFY complex concepts into digestible parts, splitting into multiple flashcards if needed.
  2.5. ENSURE that the questions are framed in a way that challenges the learner's recall and understanding.
  2.8. Stick to the minimum information principle, keep the questions short, and answers as short as possible

3. **FINALIZE FLASHCARDS:**
  3.1. Write "(image)" at the end of the question on the Front side if you think the question should include an image

Chain of Thoughts:

1. **UNDERSTAND THE INPUT:** Start by understanding the given text
2. **GENERATE FLASHCARDS:**
  2.1. For each question-answer pair, create a flashcard ensuring clarity and correctness.
  2.2. If a concept is complex, break it down into simpler parts, potentially creating multiple cards.
  2.3. Where beneficial, add context, examples, or memory aids to enhance learning.
3. **REVIEW AND FINALIZE:** Ensure each card is well-structured and effective for learning

What Not To Do:
- **DO NOT** CREATE CONFUSING OR VAGUE QUESTIONS THAT LACK CLEAR ANSWERS.
- **DO NOT** INCLUDE IRRELEVANT OR UNNECESSARY DETAILS THAT COULD OVERLOAD THE LEARNER.
- **DO NOT** OMIT KEY INFORMATION THAT IS CRUCIAL FOR UNDERSTANDING THE CONCEPT.
- **DO NOT** LEAVE FLASHCARDS UNFORMATTED OR DISORGANIZED FOR ANKI.
- **DO NOT** COMBINE MULTIPLE COMPLEX CONCEPTS INTO A SINGLE FLASHCARD; SPLIT THEM INSTEAD.
- **DO NOT** ADD MNEMONICS OR HINTS UNLESS THEY CLEARLY AID MEMORY RETENTION.
- **DO NOT** CREATE FLASHCARDS FOR CONCEPTS WHICH ARE SELF EXPLANATORY.
- **DO NOT** CREATE FLASHCARDS FOR CONCEPTS WHICH ARE EASY ENOUGH TO MEMORIZE ON THE SPOT.
- **DO NOT** CREATE FLASHCARDS FOR SETS, LISTS of ITEMS
- **DO NOT** CREATE FLASHCARDS FOR ENUMERATIONS (EXAMPLE: Q: What is the sequence of letters in the alphabet? A: abcdefghijklmnopqrstuvwxyz

Example Text: The characteristics of the Dead Sea: Salt lake located on the border between Israel and Jordan. Its shoreline is the lowest point on the Earth's surface, averaging 396 m below sea level. It is 74 km long. It is seven times as salty (30% by volume) as the ocean. Its density keeps swimmers afloat. Only simple organisms can live in its saline waters

A deck of flashcards:
|Question|Answer|
|---|---|
|Where is the Dead Sea located?|on the border between Israel and Jordan|
|What is the lowest point on the Earth's surface?|The Dead Sea shoreline|
|What is the average level on which the Dead Sea is located?|396 meters (below sea level)|
|How long is the Dead Sea?|74 km|
|How much saltier is the Dead Sea as compared with the oceans?|7 times|
|What is the volume content of salt in the Dead Sea?|30%|
|Why can the Dead Sea keep swimmers afloat?|due to high salt content|
|Why is the Dead Sea called Dead?|because only simple organisms can live in it|
|Why only simple organisms can live in the Dead Sea?|because of high salt content|

Note in the example above how short the questions are. Note also that the answers are even shorter!
We want a minimum amount of information to be retrieved from memory in a single repetition!
We want answer to be as short as imaginably possible!

Example 2: Use imagery wherever possible in the question

Less Benenficial Formulation:
Q: What African country is located between Kenya, Zambia and Mozambique?
A: Tanzania

Well-formulated knowledge:
- A graphic representation of information is usually far less volatile.
|Question|Answer|
|---|---|
|What African country is marked white on the map? (image)|Tanzania|

Example 3: Focus on understanding part rather than memorizing facts

A student with a mindset to memorize might write a single card for the quadratic formula:
Q - What is the Quadratic formula?
A - (-b±√(b²-4ac))/(2a)

But a student who is focusing on understanding as opposed to "facts" might write many cards, such as:

|Question|Answer|
|---|---|
|What are two reasons "a" can't be 0?|1. If "a" was zero, we would have a division by 0 error. 2. If "a" was zero, the x2 term would multiply to 0, and we would have a linear equation instead of a quadratic one.|
|What is the purpose of the "±"? | Quadratic equations have two solutions. i.e, they cross the x axis twice. | |
|If you are given a polynomial that looks like ax2 + bx + c, what could you use to find the value of x where the equation is zero? | You could use the quadratic formula. |
|If "c" increases/decreases, what would visually happen to the graph of the equation?|answer|
|If "b" increases/decreases, what would visually happen to the graph of the equation?|answer|
|If "a" increases/decreases, what would visually happen to the graph of the equation?|answer|
""".strip()

PROMPT_LM_SHERLOCK = """
I want you to create a deck of flashcards from the text.

Instructions to create a deck of flashcards:
- Keep the flashcards simple, clear, and focused on the most important information.
- Make sure the questions are specific and unambiguous.
- Use simple and direct language to make the cards easy to read and understand.
- Answers should contain only a single key fact/name/concept/term.

Let's do it step by step when creating a deck of flashcards:
1. Rewrite the content using clear and concise language while retaining its original meaning.
2. Split the rewritten content into several sections, with each section focusing on one main point.
3. Utilize the sections to generate multiple flashcards, and for sections with more than 10 words, split and summarize them before creating the flashcards.

Text: The characteristics of the Dead Sea: Salt lake located on the border between Israel and Jordan. Its shoreline is the lowest point on the Earth's surface, averaging 396 m below sea level. It is 74 km long. It is seven times as salty (30% by volume) as the ocean. Its density keeps swimmers afloat. Only simple organisms can live in its saline waters

A deck of flashcards:
|Question|Answer|
|---|---|
|Where is the Dead Sea located?|on the border between Israel and Jordan|
|What is the lowest point on the Earth's surface?|The Dead Sea shoreline|
|What is the average level on which the Dead Sea is located?|396 meters (below sea level)|
|How long is the Dead Sea?|74 km|
|How much saltier is the Dead Sea as compared with the oceans?|7 times|
|What is the volume content of salt in the Dead Sea?|30%|
|Why can the Dead Sea keep swimmers afloat?|due to high salt content|
|Why is the Dead Sea called Dead?|because only simple organisms can live in it|
|Why only simple organisms can live in the Dead Sea?|because of high salt content|

Text: The contraction of any muscle is associated with electrical changes called 'depolarization', and these changes can be detected by electrodes attached to the surface of the body. Since all muscular contraction will be detected, the electrical changes associated with contraction of the heart muscle will only be clear if the patient is fully relaxed and no skeletal muscles are contracting. Although the heart has four chambers, from the electrical point of view it can be thought of as having only two, because the two atria contract together ('depolarization'), and then the two ventricles contract together.
""".strip()

PROMPT_ADIL = """
<INSTRUCTIONS>
Your task is to create a deck of flashcards from the provided text focusing on optimizing the content for maximum rentention and learning effectiveness. Ensure that each flashcard is clearly written and adheres to the specified instructions.

Task Context:

The goal of these flashcards is to help study for college-level Quiz Bowl so
use what you know about the kinds of questions that get asked to select the
most important content to include. You will be provided text from two sources
to build flashcards from.

1. Excerpts from NAQT's "You Gotta Know" series of articles. Each of these
articles highlights a category (e.g., works of horror fiction) and the list of
(more or less) ten topics that NAQT's editors have determined to be very
valuable to know for the purposes of quiz bowl, along with a brief summary of
each topic's importance. Naturally, there is no guarantee that these topics or
clues will appear in NAQT question sets, but statistically speaking, they
should be a great place to start. The except you are given will pertain to one
topic from a single article (i.e., category). These articles have key terms
designated by the authors that appear bolded (e.g., this is a **key term**).

2. Several tossup and bonus questions regarding the topic and/or its key terms
taken from the QBReader database of prior NAQT packets. Quiz Bowl questions are
often designed to pyramidal, meaning that they begin with more difficult clues
and move towards easier ones. In some cases, tossups have a set of early clues
where answering prior to reading past those clues (indicated by "(*)") is worth
extra points. This is called power.

Instructions to create flashcards:

1. **FORMAT:**
  1.1 Contruct a table with three columns: "Question", "Answer", "Difficulty"
  1.2 Each row of the "Question" column should contain a single quesiton
  1.3 The "Answer" column should contain the succinct answer to the question in the corresponding row of the "Question" column.
  1.4 The "Difficulty" column should contain a number 1-5 indicating the difficulty of the question with 1 being the easiest and 5 being the hardest. Easy cards should contain critical information for answering tossups and bonuses while harder cards should focus more on facts needed to get bonus points from power.

2. **CREATE FLASHCARDS:**
  2.1. Keep the flashcards simple, clear, and focused on the most important information.
  2.2. Make sure the questions are specific and unambiguous.
  2.3. Use simple and direct language to make cards easy to read and understand.
  2.4. Each flashcard should test an atomic concept and answers should contain only a single key fact/name/concept/term.
  2.4. SIMPLIFY complex concepts into digestible parts, splitting into multiple flashcards if needed.
  2.5. ENSURE that the questions are framed in a way that challenges the learner's recall and understanding.
  2.8. Stick to the minimum information principle, keep the questions short, and answers as short as possible

3. **FINALIZE FLASHCARDS:**
  3.1. Write "(image)" at the end of the question on the Front side if you think the question should include an image

Chain of Thoughts:

1. **UNDERSTAND THE INPUT:** Start by understanding the given text
2. **GENERATE FLASHCARDS:**
  2.1. For each question-answer pair, create a flashcard ensuring clarity and correctness.
  2.2. If a concept is complex, break it down into simpler parts, potentially creating multiple cards.
  2.3. Where beneficial, add context, examples, or memory aids to enhance learning.
3. **REVIEW AND FINALIZE:** Ensure each card is well-structured and effective for learning

What Not To Do:
- **DO NOT** CREATE CONFUSING OR VAGUE QUESTIONS THAT LACK CLEAR ANSWERS.
- **DO NOT** INCLUDE IRRELEVANT OR UNNECESSARY DETAILS THAT COULD OVERLOAD THE LEARNER.
- **DO NOT** OMIT KEY INFORMATION THAT IS CRUCIAL FOR UNDERSTANDING THE CONCEPT.
- **DO NOT** LEAVE FLASHCARDS UNFORMATTED OR DISORGANIZED FOR ANKI.
- **DO NOT** COMBINE MULTIPLE COMPLEX CONCEPTS INTO A SINGLE FLASHCARD; SPLIT THEM INSTEAD.
- **DO NOT** ADD MNEMONICS OR HINTS UNLESS THEY CLEARLY AID MEMORY RETENTION.
- **DO NOT** CREATE FLASHCARDS FOR CONCEPTS WHICH ARE SELF EXPLANATORY.
- **DO NOT** CREATE FLASHCARDS FOR CONCEPTS WHICH ARE EASY ENOUGH TO MEMORIZE ON THE SPOT.
- **DO NOT** CREATE FLASHCARDS FOR SETS, LISTS of ITEMS
- **DO NOT** CREATE FLASHCARDS FOR ENUMERATIONS (EXAMPLE: Q: What is the sequence of letters in the alphabet? A: abcdefghijklmnopqrstuvwxyz

Example Text: The characteristics of the Dead Sea: Salt lake located on the border between Israel and Jordan. Its shoreline is the lowest point on the Earth's surface, averaging 396 m below sea level. It is 74 km long. It is seven times as salty (30% by volume) as the ocean. Its density keeps swimmers afloat. Only simple organisms can live in its saline waters

A deck of flashcards:
|Question|Answer|
|---|---|
|Where is the Dead Sea located?|on the border between Israel and Jordan|
|What is the lowest point on the Earth's surface?|The Dead Sea shoreline|
|What is the average level on which the Dead Sea is located?|396 meters (below sea level)|
|How long is the Dead Sea?|74 km|
|How much saltier is the Dead Sea as compared with the oceans?|7 times|
|What is the volume content of salt in the Dead Sea?|30%|
|Why can the Dead Sea keep swimmers afloat?|due to high salt content|
|Why is the Dead Sea called Dead?|because only simple organisms can live in it|
|Why only simple organisms can live in the Dead Sea?|because of high salt content|

Note in the example above how short the questions are. Note also that the answers are even shorter!
We want a minimum amount of information to be retrieved from memory in a single repetition!
We want answer to be as short as imaginably possible!

Example 2: Use imagery wherever possible in the question

Less Benenficial Formulation:
Q: What African country is located between Kenya, Zambia and Mozambique?
A: Tanzania

Well-formulated knowledge:
- A graphic representation of information is usually far less volatile.
|Question|Answer|
|---|---|
|What African country is marked white on the map? (image)|Tanzania|

Example 3: Focus on understanding part rather than memorizing facts

A student with a mindset to memorize might write a single card for the quadratic formula:
Q - What is the Quadratic formula?
A - (-b±√(b²-4ac))/(2a)

But a student who is focusing on understanding as opposed to "facts" might write many cards, such as:

|Question|Answer|
|---|---|
|What are two reasons "a" can't be 0?|1. If "a" was zero, we would have a division by 0 error. 2. If "a" was zero, the x2 term would multiply to 0, and we would have a linear equation instead of a quadratic one.|
|What is the purpose of the "±"? | Quadratic equations have two solutions. i.e, they cross the x axis twice. | |
|If you are given a polynomial that looks like ax2 + bx + c, what could you use to find the value of x where the equation is zero? | You could use the quadratic formula. |
|If "c" increases/decreases, what would visually happen to the graph of the equation?|answer|
|If "b" increases/decreases, what would visually happen to the graph of the equation?|answer|
|If "a" increases/decreases, what would visually happen to the graph of the equation?|answer|

Example 4: Use cloze deletions when appropriate

Cloze deletion is easy and effective

Cloze deletion is a sentence with its parts missing and replaced by three dots.

Ill-formulated knowledge:
Q: What was the history of the Kaleida company?
A: Kaleida, funded to the tune of $40 million by Apple Computer and IBM in 1991.

Well-formulated knowledge:
Q: Kaleida was funded to the tune of $40 million by ...(companies) in 1991
A: Apple and IBM

Q: Kaleida's mission was to create a ... It finally produced one, called Script X. But it took three years
A: multimedia programming language
</INSTRUCTIONS>

Article Category: {category}
Excerpt Topic: {topic}
Excerpt Text:
{text}

Number of related tossups: {num_related_tossups}
Related tossups:
{tossups}

Number of related bonuses: {num_related_bonuses}
Related bonuses:
{bonuses}
""".strip()

PROMPT_CHATGPT = """
# FLASHCARD GENERATION PROMPT (LLM-Optimized Version)

## GOAL
Create a deck of flashcards from the provided text to **maximize learning efficiency and retention** for **college-level Quiz Bowl** preparation.

Flashcards should:
- Help players recognize **high-value quiz clues** in questions
- Follow the **minimum information principle**
- Use clear, atomic, recall-oriented questions

---

## CONTEXT
You will receive two input sources:

1. **Excerpt from NAQT's "You Gotta Know" articles**
   - Focuses on one topic within a category (e.g., works of horror fiction)
   - Contains short summaries and **bolded key terms**

2. **Related Quiz Bowl material**
   - Tossups and bonuses from the QBReader database
   - Tossups are *pyramidal* (hard clues first → easier clues later)
   - Some tossups include "(*)" indicating **power** clues (extra points for early buzzes)

Use both sources to identify the **most quiz-relevant information** for flashcards.

---

## OUTPUT FORMAT
You must output a **Markdown table** with these exact headers:

| Question | Answer | Difficulty |
|-----------|---------|------------|

- Each row = one flashcard
- "Question" = a single clear question or cloze deletion
- "Answer" = concise, factual response (ideally ≤10 words)
- "Difficulty" = integer 1–5 (see below)

### Difficulty Scale
| Level | Description |
|-------|--------------|
| 1 | Core fact — critical to basic understanding |
| 2 | Common secondary clue — appears in later tossup clues |
| 3 | Intermediate — appears mid-tossup |
| 4 | Advanced — early or "power" clue |
| 5 | Specialist-level or deep trivia |

If unsure, assign **3**.

---

## FLASHCARD CREATION RULES

1. **Keep it atomic:**
   - One fact or concept per flashcard.
   - Split complex ideas into multiple cards.

2. **Keep it minimal:**
   - Short, direct questions and answers.
   - Follow the *minimum information principle*: smallest retrievable fact.

3. **Keep it clear:**
   - Avoid ambiguity or multi-part phrasing.
   - Use plain, natural language.

4. **Keep it quiz-relevant:**
   - Focus on clues and facts that help answer tossups or bonuses.
   - Prioritize **recognition value** and **recall efficiency**.

5. **When to use (image):**
   - Add "(image)" at the end of the question if a diagram, painting, or map would clearly enhance learning.

6. **When to use cloze deletions:**
   - Use only when it makes the card simpler and more natural.
   - Example:
     - ✅ `Kaleida was funded by ... in 1991` → `Apple and IBM`

---

## AVOID THESE MISTAKES

**Question Design**
- Multi-part, vague, or self-explanatory questions
- Lists or enumerations
- Overly long phrasing

**Content**
- Irrelevant trivia or excessive detail
- Obvious or trivial facts
- Missing key quiz clues

**Style**
- Long answers (>10 words)
- Missing difficulty ratings
- Unformatted or non-table output

---

## GENERATION PROCESS (Internal to You)

1. **Understand the input:**
   Read the NAQT excerpt and related tossups/bonuses. Identify key terms, clues, and patterns.

2. **Generate flashcards:**
   - For each key idea, create one atomic Q–A pair.
   - Prioritize high-value facts for quiz success.
   - Add difficulty rating per the scale above.

3. **Review before finalizing:**
   Confirm:
   - Each row is complete and formatted correctly
   - Answers are concise (<10 words)
   - Each question tests one clear fact
   - No lists or multi-part answers

---

## EXAMPLES

### Example 1 — Simple Factual Cards

**Input text:**
"The Dead Sea is a salt lake on the border between Israel and Jordan. It lies 396 m below sea level, is 74 km long, and is seven times as salty (30% by volume) as the ocean. Only simple organisms live in its waters."

**Output:**

| Question | Answer | Difficulty |
|-----------|---------|------------|
| Where is the Dead Sea located? | Between Israel and Jordan | 1 |
| What is the lowest point on Earth's surface? | The Dead Sea shoreline | 2 |
| How far below sea level is the Dead Sea? | 396 meters | 2 |
| How long is the Dead Sea? | 74 km | 1 |
| How much saltier is the Dead Sea than the ocean? | Seven times | 2 |
| What is the salt concentration of the Dead Sea? | 30% | 3 |
| Why do swimmers float easily in the Dead Sea? | High salt content | 2 |
| Why is the Dead Sea called "Dead"? | Only simple organisms live in it | 1 |

---

### Example 2 — Image-Aided Question

| Question | Answer | Difficulty |
|-----------|---------|------------|
| What African country is marked white on the map? (image) | Tanzania | 1 |

---

### Example 3 — Conceptual Understanding

| Question | Answer | Difficulty |
|-----------|---------|------------|
| Why can't "a" be zero in a quadratic equation? | It would make it linear | 2 |
| What does the "±" in the quadratic formula represent? | Two possible solutions | 2 |
| What happens if "c" increases in ax²+bx+c? | Graph shifts up | 3 |

---

## FINAL INPUT TEMPLATE

```
Article Category: {category}
Excerpt Topic: {topic}
Excerpt Text:
{text}

Number of related tossups: {num_related_tossups}
Related tossups:
{tossups}

Number of related bonuses: {num_related_bonuses}
Related bonuses:
{bonuses}
```
""".strip()

PROMPT_CHATGPT_SHORT = """
# FLASHCARD GENERATION PROMPT (Short Version)

## GOAL
Create flashcards from the given text to **maximize learning efficiency** for **college-level Quiz Bowl**.
Focus on **high-value clues**, **atomic questions**, and **short, precise answers**.

---

## CONTEXT
Input includes:
1. **Excerpt from NAQT's "You Gotta Know"** – one topic with short summaries and bolded key terms.
2. **Related tossups and bonuses** – pyramidal questions from QBReader (early = harder clues).

Use both to identify **facts and clues** that help players answer earlier in tossups.

---

## OUTPUT FORMAT
Always output a **Markdown table**:

| Question | Answer | Difficulty |
|-----------|---------|------------|

- **Question:** one clear question or cloze deletion
- **Answer:** concise fact (≤10 words)
- **Difficulty:** integer 1–5

### Difficulty Scale
1 = Core fact
2 = Common clue
3 = Intermediate clue
4 = Advanced / early "power" clue
5 = Specialist trivia
(If unsure, use 3.)

---

## FLASHCARD RULES
1. **Atomic:** one fact per card.
2. **Minimal:** shortest phrasing possible (minimum information principle).
3. **Clear:** no vague or multi-part questions.
4. **Relevant:** focus on clues valuable for quiz performance.
5. **(image):** add if a visual (map, artwork, etc.) would help.
6. **Cloze:** use only when it improves clarity.
   - Example: `Kaleida was funded by ... in 1991` → `Apple and IBM`

---

## AVOID
- Lists or enumerations
- Multi-part or trivial questions
- Overly long answers
- Missing difficulty rating
- Unformatted or extra text outside the table

---

## PROCESS
1. Read the input (excerpt + tossups/bonuses).
2. Extract important clues and facts.
3. Generate atomic Q–A pairs with difficulty ratings.
4. Review: short, clear, formatted correctly.

---

## EXAMPLES

### Example 1 — Simple Facts
| Question | Answer | Difficulty |
|-----------|---------|------------|
| Where is the Dead Sea located? | Between Israel and Jordan | 1 |
| How far below sea level is the Dead Sea? | 396 meters | 2 |
| Why do swimmers float easily in the Dead Sea? | High salt content | 2 |

### Example 2 — Image-Aided
| Question | Answer | Difficulty |
|-----------|---------|------------|
| What African country is marked white on the map? (image) | Tanzania | 1 |

### Example 3 — Conceptual
| Question | Answer | Difficulty |
|-----------|---------|------------|
| Why can't "a" be zero in a quadratic equation? | It would make it linear | 2 |
| What does "±" in the quadratic formula mean? | Two solutions | 2 |

---

## INPUT TEMPLATE

```
Article Category: {category}
Excerpt Topic: {topic}
Excerpt Text:
{text}

Number of related tossups: {num_related_tossups}
Related tossups:
{tossups}

Number of related bonuses: {num_related_bonuses}
Related bonuses:
{bonuses}
```
"""

PROMPT_SANITIZE_TERM = """
Below, between <term>...</term> is a search term to be exactly matched in
database. Format the term such that it has the greatest likelihood of appearing
in the database text. Output only the term, nothing else.

For example if the input was "<term>Flannery O'Connor (1925-1964)<term>", then
the output should be "Flannery O'Connor".

---

<term>{term}</term>
""".strip()

# Default prompt to use
DEFAULT_PROMPT = PROMPT_CHATGPT_SHORT
