# 1.Knowledge

- representing knowledge
- drawing conclusions

## 1.1 Knowledge

- Knowledge-Based Agents:

  These are agents that reason by operating on internal representations of knowledge.
- Sentence

  A sentence is an assertion about the world in a knowledge representation language.

## 1.2 Propositional Logic

### 1.2.1 Logical Connectives

**Or:**

- An **inclusive Or** is true if any of P, Q, or P ∧ Q is true.
- **[Exclusive or or exclusive disjunction](https://en.wikipedia.org/wiki/Exclusive_or#Truth_table)** is a logical operation that is true if and only if its arguments differ (one is true, the other is false). **(xor)**

**Implication:**

| P     | Q     | P → Q  |
| ----- | ----- | ------ |
| false | false | true   |
| false | true  | true   |
| true  | false | false  |
| true  | true  | true   |

### 1.2.2 Model

The model is **an assignment of a truth value** to every proposition. 

### 1.2.3 Knowledge Base

The knowledge base is a set of **sentences** known by a knowledge-based agent. This is knowledge that the AI is provided about the world **in the form of propositional logic sentences** that can be used to make additional inferences about the world.

### 1.2.4 Entailment 

If α(KB) ⊨ β (α entails β), then in any world **where α(KB) is true, β is true, too.**

Entailment is different from implication.

Implication is a **logical connective** between two propositions.

Entailment, on the other hand, is a relation that means that if **all the information** in α is true, then **all the information** in β is true.

## 1.3 Inference

### 1.3.1 Model Checking algorithm

To determine if KB ⊨ α (in other words, answering the question: “can we conclude that α is true based on our knowledge base”)

1. Enumerate all possible models.
2. If **in every model** where KB is true, α is true as well, then KB entails α (KB ⊨ α).

If **P in the KB**, then **for a model where P is false**, we can say that in curr model **the KB is false**, too.

We are only interested in the models where KB is true, because we have the information in our KB that **P is true(e.g. Harry played seeker and not beater or others.)**.

To run the Model Checking algorithm, the following information is needed:

- Knowledge Base, which will be used to draw inferences
- A query, or the proposition that we are interested in whether it is entailed by the KB
- Symbols, a list of all the symbols (or atomic propositions) used (in our case, these are rain, hagrid, and dumbledore)
- Model, an assignment of truth and false values to symbols

## 1.4 Knowledge Engineering

Knowledge engineering is the process of figuring out **how to represent propositions and logic** in AI.


For Clue:

- use the Model Checking algorithm
- **start creating our knowledge base** by adding the rules of the game.

For .

For Mastermind game

## 1.5 Inference Rules

Model Checking is **not an efficient algorithm** because it has to consider every possible model before giving the answer (a reminder: a query R is true if **under all the models (truth assignments) where the KB is true, R is true as well**). 

 Inference rules allow us to generate new information based on existing knowledge **without considering every possible model.**

 ### 1.5.1 Knowledge and Search Problems

**Inference can be viewed as a search problem** with the following properties:

- Initial state: starting knowledge base
- Actions: inference rules
- Transition model: new knowledge base after inference
- Goal test: checking whether the statement that we are trying to prove is in the KB
- Path cost function: the number of steps in the proof

## 1.6 Resolution

### 1.6.1 Steps in Conversion of Propositions to Conjunctive Normal Form

### 1.6.2 Algorithm 

facotring: a clause contains the same literal twice: In these cases, a process called **factoring** is used, where the duplicate literal is removed. For example, (P ∨ Q ∨ S) ∧ (¬P ∨ R ∨ S) allow us to infer by resolution that (Q ∨ S ∨ R ∨ S). **The duplicate S can be removed** to give us (Q ∨ R ∨ S).

Resolving a literal and its negation, i.e. ¬P and P, gives the **empty clause ()**. **The empty clause is always false**, and this makes sense because it is impossible that both P and ¬P are true. This fact is used by the resolution algorithm.

To determine if KB ⊨ α:
- Convert (KB ∧ ¬α) to Conjunctive Normal Form. (**Add ¬α to the KB**)
- Keep checking to see if we can use resolution to produce a new clause.
- If we ever **produce the empty clause** (equivalent to False), congratulations! We have arrived at a contradiction, thus proving that KB ⊨ α.
- However, **if contradiction is not achieved and no more clauses can be inferred, there is no entailment.**

## 1.7 First Order Logic

First order logic is another type of logic that allows us to express more complex ideas more succinctly than propositional logic.

There are **other types of logic** as well, and the commonality between them is that they all exist **in pursuit of representing information**. These are the systems we use to represent knowledge in our AI.