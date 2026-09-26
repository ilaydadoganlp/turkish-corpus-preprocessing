# Adaptive Turkish Corpus Preprocessing & Quality Pipeline

A Turkish NLP project exploring how preprocessing decisions should adapt to
different corpus characteristics and downstream tasks.

The project builds a heterogeneous Turkish corpus consisting of different text
types and uses it as an experimental testbed for comparing preprocessing
strategies, evaluating their outputs and analysing task-dependent pipeline
decisions.

The corpus is designed as a reusable experimental resource rather than an
attempt to represent the entirety of Turkish.

## Research Motivation

A single preprocessing pipeline may not be equally appropriate for different
types of linguistic data. Legal, news, academic and user generated texts
differ in their linguistic, structural and surface level characteristics.

In this project, I aim to investigate these differences experimentally by applying and comparing preprocessing decisions across subcorpora instead of treating preprocessing as a fixed sequence of steps.

## Corpus

The experimental corpus currently consists of four subcorpora:

- News
- Legal
- Academic
- User generated entries

The corpus is intentionally heterogeneous and will be used to examine how
different preprocessing choices affect corpus-level and subcorpus-level
outputs.

## Project Status

🚧 Work in progress