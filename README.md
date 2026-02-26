# Indicator Ontology 

This repository contains the core ontology definitions for the indicator ontology project.

## Files

### indicator.ttl
OWL ontology for indicator semantics. This file provides:
- Semantic definitions for SDG indicators
- Alignment with established ontologies (AIAO, ClaimOnt, ImpactOnt, InfoComm)
- Impact pathway classifications (activities → outputs → outcomes → impacts)
- Properties for indicator formulas, units, rationales, and operational semantics
- Integration with QUDT for measurement units

## Purpose

The core ontology files provide the foundational semantic framework that the other vocabularies build upon. They define the essential concepts, properties, and relationships needed to represent SDG indicators and their measurements in a machine-readable format.

## Usage

These files should be loaded into a triple store or RDF processing system along with the vocabulary and DSD files. The core definitions are referenced by all other ontology files in this repository.

## Related Documentation

- [Theory of Change Framework](../../docs/theory/TheoryofChange.md)
- [Impact Pathway Guidance](../../docs/theory/impact-pathway-indicator-guidance.md)
