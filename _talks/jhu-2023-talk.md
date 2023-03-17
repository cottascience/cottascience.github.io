---
title: "Causal Lifting and Link Prediction"
collection: talks
type: "Talk"
permalink: /talks/jhu-2023-talk.md
venue: "CISS 2023: Lecture Presentation."
date: 2012-03-22
location: "Baltimore, MD"
---

Current state-of-the-art causal models for link prediction assume an underlying set of inherent node factors -- an innate characteristic defined at the node's birth -- that governs the causal evolution of links in the graph. In some causal tasks, however, link formation is path-dependent, i.e., the outcome of link interventions depends on existing links. For instance, in the customer-product graph of an online retailer, the effect of an 85-inch TV ad (treatment) likely depends on whether the costumer already has an 85-inch TV. Unfortunately, existing causal methods are impractical in these scenarios. The cascading functional dependencies between links (due to path dependence) are either unidentifiable or require an impractical number of control variables. In order to remedy this shortcoming, this work develops the first causal model capable of dealing with path dependencies in link prediction. It introduces the concept of causal lifting, an invariance in causal models that, when satisfied, allows the identification of causal link prediction queries using limited interventional data. On the estimation side, we show how structural pairwise embeddings -- a type of symmetry-based joint representation of node pairs in a graph -- exhibit lower bias and correctly represent the causal structure of the task, as opposed to existing node embedding methods, e.g., GNNs and matrix factorization. Finally, we validate our theoretical findings on four datasets under three different scenarios for causal link prediction tasks: knowledge base completion, covariance matrix estimation and consumer-product recommendations.

