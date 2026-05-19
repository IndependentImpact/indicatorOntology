# Data Structure Definition (DSD) Files

This directory contains Data Structure Definition files that define how SDG indicator data should be structured and disaggregated for analysis.

## Understanding DSDs, Axes, Schemes, and Concepts

The DSD infrastructure consists of four interconnected layers that work together to structure and validate SDG indicator values:

### Architectural Overview

```
DSD (Data Structure Definition)
  ↓ defines structure with
AxisSpecifications
  ↓ each axis uses
Axis (e.g., AxisSex)
  ↓ with values from
Scheme (e.g., SexScheme_v1)
  ↓ containing
Concepts (e.g., sex_male, sex_female)
```

### The Four Core Components

1. **Axes** (`axis-definitions.ttl`) - Define dimension types
   - Each axis represents a type of disaggregation dimension (Sex, Age, Geographic Location, etc.)
   - Axes are abstract dimension types that can be reused across multiple DSDs
   - Example: `AxisSex` defines that data can be disaggregated by sex/gender

2. **Schemes** (`scheme-definitions.ttl`) - Provide controlled vocabularies
   - Each scheme is a SKOS ConceptScheme containing allowed values for an axis
   - Schemes are versioned to support evolution over time
   - Example: `SexScheme_v1` contains the concepts: male, female, other, unknown

3. **DSDs** (`../../skos_SDG/ontologies/dsd/dsd-complete.ttl`) - Specify data structures
   - Each DSD defines which axes are used for a particular indicator or set of indicators
   - DSDs reference schemes through AxisSpecifications
   - Example: `DSD_Social_Sex_v1` uses `AxisSex` with values from `SexScheme_v1`

4. **Concepts** (within `scheme-definitions.ttl`) - Individual values
   - Concepts are the actual values used in indicator values
   - Each concept belongs to a scheme and has labels, notations, and definitions
   - Example: `sex_male`, `sex_female` are concepts in `SexScheme_v1`

### Complete Example Flow

Here's how all components work together for an indicator tracking poverty by sex and age:

**1. Axes are defined** (from `axis-definitions.ttl`):
```turtle
ind:AxisSex a ind:Axis ;
  rdfs:label "Sex"@en ;
  skos:definition "Disaggregation by biological sex or gender"@en .

ind:AxisAge a ind:Axis ;
  rdfs:label "Age Category"@en ;
  skos:definition "Disaggregation by age groups"@en .
```

**2. Schemes with concepts are defined** (from `scheme-definitions.ttl`):
```turtle
ind:SexScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Sex scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:sex_male , ind:sex_female , 
                     ind:sex_other , ind:sex_unknown .

ind:sex_male a skos:Concept ;
  skos:prefLabel "Male"@en ;
  skos:inScheme ind:SexScheme_v1 ;
  skos:topConceptOf ind:SexScheme_v1 ;
  skos:notation "M" .

ind:GlobalAgeScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Global age categories v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:age_15_19 , ind:age_20_24 .  # ... more age concepts

ind:age_15_19 a skos:Concept ;
  skos:prefLabel "15-19 years"@en ;
  skos:inScheme ind:GlobalAgeScheme_v1 ;
  skos:notation "AGE_15_19" .
```

**3. A DSD combines them** (from `../../skos_SDG/ontologies/dsd/dsd-complete.ttl`):
```turtle
ind:DSD_Social_SexAge_v1 a ind:DataStructureDefinition ;
  skos:prefLabel "Social indicators with Sex and Age disaggregation v1"@en ;
  ind:definitionVersion "1.0" ;
  ind:hasAxisSpec ind:Spec_DSD_Social_SexAge_v1_Sex ,
                    ind:Spec_DSD_Social_SexAge_v1_Age .

ind:Spec_DSD_Social_SexAge_v1_Sex a ind:AxisSpecification ;
  ind:axis ind:AxisSex ;
  ind:valueScheme ind:SexScheme_v1 ;
  ind:minCardinality 0 ;
  ind:maxCardinality 1 .

ind:Spec_DSD_Social_SexAge_v1_Age a ind:AxisSpecification ;
  ind:axis ind:AxisAge ;
  ind:valueScheme ind:GlobalAgeScheme_v1 ;
  ind:minCardinality 0 ;
  ind:maxCardinality 1 .
```

**4. Observations use the concepts** (example from observation data):
```turtle
ind:obs_123 a impact:IndicatorValue ;
  ind:hasSubgroupSlice [ a ind:SubgroupSlice ; ind:subgroupAxis ind:AxisSex ; ind:subgroupValue ind:sex_female ] ;
    ind:hasSubgroupSlice [ a ind:SubgroupSlice ; ind:subgroupAxis ind:AxisAge ; ind:subgroupValue ind:age_15_19 ] ;
  
    ind:usesDSD ind:DSD_Social_SexAge_v1 ;
  rdf:value 23.4 .
```

### Why This Architecture Matters

**Data Quality Control:** Schemes enable SHACL validation to ensure indicator values use correct values. Invalid values are rejected before they enter the system.

**Semantic Interoperability:** Standardized schemes allow data aggregation across sources, enable SPARQL queries across datasets, and support linked data integration.

**Version Management:** Schemes are versioned (e.g., `_v1`, `_v2`), allowing controlled evolution while maintaining backward compatibility for existing indicator values.

**Reusability:** A single axis and scheme (e.g., `AxisSex` with `SexScheme_v1`) can be used by multiple DSDs, ensuring consistency across indicators.

### Integration with the DSD Ecosystem

The four DSD files work as an integrated system:

| File | Purpose | Depends On |
|------|---------|------------|
| `axis-definitions.ttl` | Defines dimension types (Sex, Age, etc.) | - |
| `scheme-definitions.ttl` | Provides controlled vocabularies | - |
| `../../skos_SDG/ontologies/dsd/dsd-complete.ttl` | Defines 23 DSD structures | Both above |
| `dsd-validation.ttl` | SHACL shapes for validation | All above |

**Dependency Chain:**
```
axis-definitions.ttl ────┐
                         ├──> dsd-complete.ttl ──> indicator values
scheme-definitions.ttl ──┘
```

All indicator values must reference a DSD, which in turn references axes and schemes to ensure data conforms to the expected structure.

## Files

### axis-definitions.ttl
Definitions of disaggregation axes (dimensions) for indicator data. Axes are abstract dimension types that can be reused across multiple DSDs.

**Purpose:**
- Define the types of dimensions available for disaggregation
- Provide semantic definitions for each axis
- Establish a standardized vocabulary for data structure specifications

**Common Axes Include:**
- `AxisSex` - Sex/Gender disaggregation
- `AxisAge` - Age category disaggregation  
- `AxisGeographicLocation` - Geographic/spatial disaggregation
- `AxisUrbanRural` - Urban/Rural classification
- `AxisIncomeQuintile` - Income level disaggregation
- `AxisEmploymentStatus` - Employment status categories
- `AxisEducationLevel` - Education level categories
- Plus additional axes for comprehensive coverage

**Key Characteristics:**
- Axes are dimension types, not the actual values
- Each axis can be used by multiple DSDs
- Axes reference schemes for their allowed values through AxisSpecifications

### scheme-definitions.ttl
SKOS concept schemes for axis value vocabularies. This file provides controlled vocabularies that populate the dimensions (axes) of Data Structure Definitions.

**Current Content:**
- **17 SKOS ConceptSchemes** with 100+ individual concepts
- Versioned collections (e.g., `SexScheme_v1`, `GlobalAgeScheme_v1`)
- Labels and notations for each concept
- Semantic relationships between concepts

**Key Schemes Include:**
- `SexScheme_v1` - Sex/gender classification (Male, Female, Other, Unknown)
- `GlobalAgeScheme_v1` - International age groups (5-year bands)
- `UrbanRuralScheme_v1` - Urban vs Rural location
- `IncomeQuintileScheme_v1` - Household income quintiles (Q1-Q5)
- `EducationLevelScheme_v1` - Education levels (none to tertiary)
- Plus 12 additional schemes for comprehensive disaggregation coverage

**File Structure Pattern:**
```turtle
ind:SexScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Sex scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:sex_male , ind:sex_female .

ind:sex_male a skos:Concept ;
  skos:prefLabel "Male"@en ;
  skos:inScheme ind:SexScheme_v1 ;
  skos:topConceptOf ind:SexScheme_v1 ;
  skos:notation "M" .
```

**Naming Conventions:**
- Schemes: `{Domain}{Purpose}Scheme_v{Version}` (e.g., `SexScheme_v1`)
- Concepts: `{prefix}_{name}` (e.g., `sex_male`, `age_15_19`)
- Notations: Short uppercase codes (e.g., "M", "F", "AGE_15_19")

### dsd-validation.ttl
SHACL (Shapes Constraint Language) shapes for validating Data Structure Definitions. This file contains:
- Validation rules for DSD structure
- Constraints on axis definitions
- Required properties and relationships
- Data quality checks

### examples/dsd/dsd-examples.ttl
Example Data Structure Definitions demonstrating best practices. This file shows:
- Sample DSDs for common indicator types
- Complete examples of disaggregation specifications
- How to combine multiple axes
- Practical patterns for real-world usage

### SDG-side DSD bundle (external)
Comprehensive collection of production-ready Data Structure Definitions is maintained in `../../skos_SDG/ontologies/dsd/dsd-complete.ttl`. It includes:
- Complete DSD specifications for SDG indicators
- AxisSpecifications that link axes to their value schemes
- Cardinality constraints for each dimension
- Support for 251 SDG indicators across all 17 goals

**What DSDs Define:**
Each DSD specifies:
- Which axes (dimensions) are used for disaggregation
- Which schemes provide the allowed values for each axis
- Whether each dimension is required or optional (cardinality)
- Semantic relationships with indicator definitions

**Example DSDs:**
- `DSD_Social_Sex_v1` - Single dimension: Sex
- `DSD_Social_SexAge_v1` - Two dimensions: Sex and Age
- `DSD_Geographic_Admin_v1` - Geographic disaggregation
- Plus 20 additional DSDs for various indicator types

## Purpose

The DSD files enable:
- Standardized data disaggregation across SDG monitoring systems
- Validation of indicator data submissions
- Interoperability between different data collection platforms
- Machine-readable specifications for data structure requirements

## Usage

DSDs are used in conjunction with the indicator vocabularies to define how data should be collected and structured. They are particularly important for:
- Data validation pipelines
- Data submission templates
- API specifications for data exchange
- Statistical database schemas

Example: Loading and validating a DSD using SHACL:
```python
from rdflib import Graph
from pyshacl import validate

# Load the DSD
dsd_graph = Graph()
dsd_graph.parse("examples/dsd/dsd-examples.ttl", format="turtle")

# Load validation shapes
shapes_graph = Graph()
shapes_graph.parse("dsd-validation.ttl", format="turtle")

# Validate
conforms, results_graph, results_text = validate(
    dsd_graph,
    shacl_graph=shapes_graph,
    inference='rdfs'
)

print(f"Validation result: {conforms}")
```

## Related Documentation

- [Main Ontologies README](../README.md)
- SDG-specific DSD implementation guides are maintained in the `skos_SDG` repository.

## Extending the DSD System

### Adding New Schemes

To add a new controlled vocabulary:

1. **Identify need** - Determine if a new scheme is necessary or if an existing scheme should be extended

2. **Define scope** - List all concepts required for the new dimension

3. **Add to scheme-definitions.ttl:**
```turtle
ind:NewDimensionScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "New Dimension scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:newdim_value1 , ind:newdim_value2 .

ind:newdim_value1 a skos:Concept ;
  skos:prefLabel "Value 1"@en ;
  skos:inScheme ind:NewDimensionScheme_v1 ;
  skos:topConceptOf ind:NewDimensionScheme_v1 ;
  skos:notation "V1" .
```

4. **Add corresponding axis** to `axis-definitions.ttl`:
```turtle
ind:AxisNewDimension a ind:Axis ;
  rdfs:label "New dimension"@en ;
  skos:definition "Definition of the dimension."@en .
```

5. **Create or update DSD** in `../../skos_SDG/ontologies/dsd/dsd-complete.ttl`:
```turtle
ind:Spec_DSD_Example_NewDim a ind:AxisSpecification ;
  ind:axis ind:AxisNewDimension ;
  ind:valueScheme ind:NewDimensionScheme_v1 ;
  ind:minCardinality 0 ;
  ind:maxCardinality 1 .
```

6. **Validate** using the repository's validation scripts

### Version Management

**Important:** Keep all schemes at their current version unless breaking changes are required.
- 251 indicators depend on current scheme versions
- Breaking changes require updating all indicator values
- Version stability enables production deployment

**For changes:**
1. Create new version (e.g., `SexScheme_v2`)
2. Keep v1 for backward compatibility
3. Provide migration guidance
4. Update DSDs to reference new version as appropriate






