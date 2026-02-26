# Indicator Ontology 

This repository contains the core ontology definitions for the indicator ontology project, prepared for integration with [w3id.org](https://w3id.org).

## Ontology Dependencies

This ontology **conforms to and depends on** the following foundational ontologies:

- **[Impact Ontology (ImpactOnt)](http://w3id.org/impactont)**: Provides the foundational semantic framework for impact modeling, including the impact of human activities on environments.
- **[Anthropogenic Impact Accounting Ontology (AIAO)](http://w3id.org/aiao)**: Provides the semantic framework for accounting for human impact on environments, including agents, activities, and environments.

These dependencies ensure semantic interoperability and consistency with established impact assessment frameworks. The indicator ontology extends these foundational ontologies with specific semantics for indicators and measurements.

## Files

### Core Ontology
- **indicator.ttl**: Turtle/RDF source ontology for indicator semantics
- **indicator.owl**: OWL/XML serialization (generated)
- **indicator.jsonld**: JSON-LD serialization (generated)
- **docs/indicator.html**: Human-readable HTML documentation (generated)

### Scripts
- **convert.py**: Python script to convert indicator.ttl to OWL, JSON-LD, and HTML formats
- **install_requirements.sh**: Script to install Python dependencies for conversion

### w3id.org Integration
- **htdocs/.htaccess**: Content negotiation configuration for w3id.org hosting

## Ontology Content

The indicator.ttl file provides:
- Semantic definitions for indicators (including examples such as SDG indicators)
- Alignment with established ontologies (AIAO, ClaimOnt, ImpactOnt, InfoComm)
- Impact pathway classifications (activities → outputs → outcomes → impacts)
- Properties for indicator formulas, units, rationales, and operational semantics
- Integration with QUDT for measurement units

## Building the Ontology

To generate the OWL, JSON-LD, and HTML documentation from the Turtle source:

1. Install dependencies:
   ```bash
   ./install_requirements.sh
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

3. Run the conversion script:
   ```bash
   python convert.py indicator.ttl
   ```

This will generate:
- `indicator.owl` - OWL/XML format
- `indicator.jsonld` - JSON-LD format
- `docs/indicator.html` - Human-readable HTML documentation

## Purpose

The core ontology files provide the foundational semantic framework that other vocabularies build upon. They define the essential concepts, properties, and relationships needed to represent indicators and their measurements in a machine-readable format, while maintaining conformance to the [Impact Ontology](http://w3id.org/impactont) and [AIAO](http://w3id.org/aiao) standards. While originally developed for SDG indicators, this ontology has general applicability to any indicator framework.

## Usage

These files should be loaded into a triple store or RDF processing system along with the vocabulary and DSD files. The core definitions are referenced by all other ontology files in this repository.

## License

This ontology is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

## Related Documentation

- [Theory of Change Framework](docs/TheoryofChange.md)
- [Impact Pathway Guidance](docs/impact-pathway-indicator-guidance.md)
