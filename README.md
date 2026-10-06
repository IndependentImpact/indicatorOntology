# Indicator Ontology

An OWL ontology for describing **indicators** — what they measure, how they are computed, where they sit in an impact pathway, and how their reported values are structured and disaggregated. It was developed for the UN Sustainable Development Goal (SDG) indicators but is framework-agnostic and can describe any indicator set.

- **Namespace:** `http://independentimpact.org/indicator-owl/` (prefix `ind:`)
- **Source of truth:** [`indicator.ttl`](indicator.ttl) (Turtle)
- **Documentation:** [independentimpact.github.io/indicatorOntology/indicator.html](https://independentimpact.github.io/indicatorOntology/indicator.html)
- **License:** Apache 2.0

## Ontology dependencies

The indicator ontology extends, and is aligned with, the following ontologies:

| Prefix | Ontology | Role |
|---|---|---|
| `impact:` | [ImpactOnt](http://w3id.org/impactont) | `impact:Indicator` and `impact:IndicatorValue`, which this ontology specialises |
| `aiao:` | [AIAO](http://w3id.org/aiao) — Anthropogenic Impact Accounting Ontology | Agents, activities, environments; DSDs and axes are `aiao:Control`s |
| `claimont:` | [ClaimOnt](http://w3id.org/claimont) | Reports that make claims about indicators |
| `infocomm:` | [InfoComm](http://w3id.org/infocomm) | Information objects and communication events |
| `qudt:` / `unit:` | [QUDT](http://qudt.org) | Units of measure |
| `skos:`, `prov:`, `time:`, `foaf:`, `dct:` | W3C / community vocabularies | Classification schemes, locations, reporting periods, linking, metadata |

External indicator catalogues (for example a SKOS list of SDG indicators) link to an `ind:IndicatorDefinition` via `foaf:focus`.

## What the ontology models

### 1. Indicator definitions

| Term | Kind | Description |
|---|---|---|
| `ind:IndicatorDefinition` | Class | An indicator concept with descriptive metadata, expected units and rationale (subclass of `impact:Indicator`) |
| `ind:IndicatorRationale` | Class | Why the indicator is relevant to the objective or state being monitored |
| `ind:hasRationale` | Object property | Indicator → rationale |
| `ind:hasUnit` | Object property | Indicator or indicator value → `qudt:Unit` |
| `ind:hasDefaultDSD` | Object property | Indicator definition → its recommended data structure definition |

### 2. Formulas and expressions

Indicator computation is described as a structured formula rather than free text alone.

| Term | Kind | Description |
|---|---|---|
| `ind:IndicatorFormula` | Class | Human-readable description of how to compute the indicator |
| `ind:Symbol` | Class | A symbol in a formula; units via `ind:hasUnit`, meaning via `foaf:focus` |
| `ind:MathOperator` | Class | An operator token (`=`, `+`, `-`, `*`, `/`, `^`) |
| `ind:hasFormula` (alias `ind:hasExpression`) | Object property | Indicator → formula |
| `ind:usesSymbol`, `ind:usesOperator` | Object properties | Formula → symbols / operators it contains |
| `ind:expressionText` | Datatype property | The formula as text |
| `ind:mathTextRepresentationType` | Datatype property | Notation of `expressionText`: `LaTeX`, `AsciiMath` or `ContentMathML` |

### 3. Impact pathway stages

A SKOS concept scheme, `ind:IndicatorStageScheme`, classifies indicators by their position in a theory of change, assigned with `ind:hasIndicatorStage`:

`ind:ActivityIndicator` → `ind:OutputIndicator` → `ind:OutcomeIndicator` → `ind:ImpactIndicator`

### 4. Indicator values

| Term | Kind | Description |
|---|---|---|
| `ind:MeasuredIndicatorValue` | Class | Value obtained directly by observation, monitoring, sampling or metering |
| `ind:DerivedIndicatorValue` | Class | Value computed or inferred from other values (disjoint with measured) |
| `ind:usesDSD` | Object property | Value → the DSD it conforms to |
| `ind:refArea` | Object property | Value → `prov:Location` (town, catchment, admin unit, biome …) |
| `ind:reportingPeriod` | Object property | Value → `time:Interval` |
| `ind:obsStatus` | Object property | Value → status concept (reported, estimated, imputed, provisional …) |
| `ind:methodReference` | Datatype property | Value → URI of the method used |
| `ind:reportsIndicator`, `ind:communicatedBy` | Object properties | Link a `claimont:Report` to the indicator it reports and the `infocomm:CommunicationEvent` that transmits it |

### 5. Data structure definitions (DSDs) and disaggregation

DSDs declare how values for an indicator are disaggregated, in the spirit of SDMX / RDF Data Cube:

```
DataStructureDefinition
  └─ hasAxisSpec → AxisSpecification
        ├─ axis        → Axis              (e.g. AxisSex, AxisAgeCategory)
        ├─ axisRole    → Dimension | Measure | Attribute
        ├─ valueScheme → skos:ConceptScheme (allowed values)
        └─ min/maxCardinality
```

An indicator value carries one `ind:SubgroupSlice` per disaggregation (`ind:hasSubgroupSlice`), each pairing an `ind:subgroupAxis` with an `ind:subgroupValue` drawn from that axis's scheme:

```turtle
ex:obs_123 a ind:MeasuredIndicatorValue ;
  ind:usesDSD ind:DSD_BasicSocial_v1 ;
  ind:hasSubgroupSlice [ ind:subgroupAxis ind:AxisSex ; ind:subgroupValue ind:sex_female ] ,
                       [ ind:subgroupAxis ind:AxisAgeCategory ; ind:subgroupValue ind:age_15_19 ] ;
  rdf:value 23.4 .
```

## Repository layout

```
indicator.ttl            Source ontology (edit this)
indicator.owl            OWL/XML serialisation (generated)
indicator.jsonld         JSON-LD serialisation (generated)
convert.py               Converts indicator.ttl to OWL, JSON-LD and HTML (rdflib + Jinja2)
install_requirements.sh  Creates ./venv and installs Python dependencies
docs/
  indicator.html                       Generated HTML reference documentation
  template.html.j2                     Jinja2 template used by convert.py
  TheoryofChange.md                    Background: activities, outputs, outcomes, impacts
  impact-pathway-indicator-guidance.md Modelling guidance for impact pathways and indicator frameworks
IndicatorDSD/
  axis-definitions.ttl     Disaggregation axes (sex, age, location, urban/rural, income, …)
  scheme-definitions.ttl   Versioned SKOS schemes holding the allowed axis values
  dsd-validation.ttl       SHACL shapes for validating DSDs and indicator values
  examples/                Example DSDs, observations and SPARQL queries
  scripts/generators/      Generate axes, schemes and DSDs
  scripts/testing/         Structure validation and integration tests
  README.md                Detailed explanation of the DSD architecture
htdocs/.htaccess         w3id.org content negotiation rules
.github/workflows/release.yml  Builds and publishes release artefacts on version tags
```

## Building

Generate the OWL, JSON-LD and HTML outputs from the Turtle source:

```bash
./install_requirements.sh
source venv/bin/activate
python convert.py indicator.ttl
```

This writes `indicator.owl`, `indicator.jsonld` and `docs/indicator.html`. Edit only `indicator.ttl`; regenerate the rest.

### DSD tests

```bash
cd IndicatorDSD/scripts/testing
./run-dsd-tests.sh --install-deps
```

See [IndicatorDSD/README.md](IndicatorDSD/README.md) for details.

## Releases and persistent identifiers

Pushing a tag matching `v*` triggers the [release workflow](.github/workflows/release.yml), which builds the ontology and attaches `indicator.ttl`, `indicator.owl`, `indicator.jsonld` and `indicator.html` to a GitHub release.

The rules in [`htdocs/.htaccess`](htdocs/.htaccess) are intended for a w3id.org redirect and perform content negotiation:

| `Accept` header | Served |
|---|---|
| `text/html` (or a browser) | HTML documentation on GitHub Pages |
| `text/turtle` | `indicator.ttl` |
| `application/ld+json`, `application/json` | `indicator.jsonld` |
| `application/rdf+xml` (default) | `indicator.owl` |

A version segment in the path (e.g. `/v1.0.0/`) resolves to that tagged release via jsDelivr; requests without one resolve to `main`.

## Usage

Load `indicator.ttl` (or any serialisation) into a triple store or RDF toolkit together with its dependencies and, when reporting disaggregated values, the files in `IndicatorDSD/`. Indicator catalogues reference `ind:IndicatorDefinition` instances, and reported data are expressed as `impact:IndicatorValue` instances using the value and DSD properties above.

## Further reading

- [Theory of Change framework](docs/TheoryofChange.md)
- [Impact pathway indicator guidance](docs/impact-pathway-indicator-guidance.md)
- [DSD architecture](IndicatorDSD/README.md)

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE).
