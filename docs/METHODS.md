# Optional method references

These are **ideas and reading references, not a required implementation list**. After direct-answer review and agreement, the notebook first guides zero-shot CoT and then one-shot CoT. Formula grounding and the other methods below are optional extensions. The entries here are optional reading and extensions beyond that scaffold. You do not have to implement MedPrompt, Self-Refine, or any other particular entry.

| Method | Primary reference | Idea to investigate | What to keep clear |
|---|---|---|---|
| Zero-shot CoT / worked reasoning | Kojima et al., [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916) | Ask for a checkable worked calculation before the answer | A visible solution is evidence to inspect, not proof of correct reasoning |
| One-shot CoT / worked reasoning | Wei et al., [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) | Provide one relevant solved example | Use a disjoint example from `examples.json`; a reasoning example differs from an answer-only example |
| Self-Refine | Madaan et al., [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) | Initial solution → self-critique → revised solution, potentially repeated | Choose stopping criteria; preserve earlier attempts; critique must not receive the question's gold answer |
| MedPrompt | Nori et al., [Can Generalist Foundation Models Outcompete Special-Purpose Tuning? Case Study in Medicine](https://arxiv.org/abs/2311.16452) | Retrieve similar worked examples and use them to guide the next solution | Full MedPrompt combines several components; state which ones you actually use |
| Self-consistency | Wang et al., [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) | Sample several solutions and aggregate answers | Define how numerical answers are grouped without accessing their gold values |
| Formula retrieval / RAG | Lewis et al., [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) | Retrieve calculator knowledge before solving | General formula knowledge differs from a worked patient example |
| Program-aided calculation | Gao et al., [PAL: Program-aided Language Models](https://arxiv.org/abs/2211.10435) | Use executable calculation to support language-based problem solving | A reviewed calculator dispatcher is a possible course adaptation; describe it accurately |



## Calculator knowledge and evaluation

`docs/CALCULATOR_REFERENCE.md` gives formulas, scoring tables, units and versions for every calculator in the dataset. The same material is in `data/calculator_references.json`. Use these references to inspect solutions or build your evaluator.

If you supply a calculator card to the solver, that is an explicit formula-grounded/open-book method. Report it separately from a baseline that did not receive the card. Formula retrieval and worked-example retrieval supply different kinds of information.

For additional evaluation inspiration, see Lightman et al., [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050). You choose and validate your own rubric; no particular step-wise evaluator is required.
