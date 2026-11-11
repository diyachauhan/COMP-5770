# Data credit and license

Patient vignettes, questions and original answer annotations originate from **MedCalc-Bench**, by Khandekar and collaborators, and its Open-Patients sources.

- Original dataset and attribution: https://github.com/ncbi-nlp/MedCalc-Bench
- Dataset landing page: https://huggingface.co/datasets/ncbi/MedCalc-Bench
- Dataset license: **Creative Commons Attribution-ShareAlike 4.0 International**, https://creativecommons.org/licenses/by-sa/4.0/

The course subset and example bank retain that dataset license. Changes for this package: selected 16 calculators; deterministic random selection of 10 questions per calculator; assigned dev/test partitions; renamed columns and converted entity strings into JSON; added stable IDs, note hashes and metadata; normalized numerical reference explanations to explicit formula/input/answer summaries. Numerical answer values and supplied tolerance bounds are retained. Rule-based reference annotations are retained and may contain interpretation assumptions. Credit the original dataset if redistributing the subset; retain this file and the share-alike terms.

The assignment text and Python helpers were written specifically for this course package. No inference/evaluator code from an external research repository is redistributed. Dataset provenance does not prescribe a solution method for this assignment.
