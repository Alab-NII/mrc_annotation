# mrc_annotation
Annotation and parsers for ["Evaluation Metrics for Machine Reading Comprehension: Prerequisite Skills and Readability"](https://aclanthology.info/papers/P17-1075/p17-1075) (Sugawara et al., ACL 2017)

## Annotation data

In the `annotation` directory.

* `skills` indicate skill numbers (multiple labeling).
  - 0: Object tracking
  - 1: Mathematical reasoning
  - 2: Coreference resolution
  - 3: Logical reasoning
  - 4: Analogy
  - 5: Causal relation
  - 6: Spatiotemporal relation
  - 7: Ellipsis
  - 8: Bridging
  - 9: Elaboration
  - 10: Meta knowledge
  - 11: Schematic clause relation
  - 12: Punctuation
  - 13: no skill
* `skill_count`
  - Number of required skills.
* `sents_indices`
  - Indices of sentences that are required for answering a question.
  - Each value indicates an index of list of string(context).split() in python.
* `id`
  - Numbering in annotation.
* `original_id`
  - Identifier in the dataset. See each parsing script in the `parse` directory for naming.

## Annotation guildline

Please refer to the following spredsheets for the annotation procedure, the skill definitions, and toy examples.

https://docs.google.com/spreadsheets/d/1B-t0309obrbNuwhWeDAYDcTdJv8owobUHLY07KXez54/edit?usp=sharing
