# Core Ontology Definitions

This directory contains the core ontology definitions for the SDG SKOS vocabulary project.

## Files

### sdg-vocab-metadata.ttl
Core metadata and namespace definitions for the SDG ontology. This file establishes:
- The base namespace for SDG concepts (`http://independentimpact.org/sdg/`)
- Core properties and relationships used across all SDG vocabularies
- Provenance and metadata about the ontology itself

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

- [Main Ontologies README](../README.md)
- [Theory of Change Framework](../../docs/theory/TheoryofChange.md)
- [Impact Pathway Guidance](../../docs/theory/impact-pathway-indicator-guidance.md)
