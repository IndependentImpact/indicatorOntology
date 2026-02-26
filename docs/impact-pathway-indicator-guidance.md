# Modelling Impact Pathways and Indicator Frameworks

This document describes **how to extend your existing indicator ontology** so that it can express:

- A **theory of change / impact pathway** (activities → outputs → outcomes → impacts)
- A **categorisation of indicators** by their position in that pathway
- **Indicator frameworks** that bundle indicators across the pathway to strengthen causal confidence

The guidance is grounded in the following ontologies:

- **AIAO** – https://w3id.org/aiao  
- **ImpactOnt** – https://w3id.org/impactont  
- **ClaimOnt** – https://w3id.org/claimont  
- **InfoComm** – https://w3id.org/infocomm  

You have chosen **Option 1** under section 6(A):  
➡ *Indicator definitions are instances that are also `impactont:Indicator`.*

---

## 1. Core Design Principle

**Do not hard-code causality.**  
Model *measurement facts* as states and *causal assertions* as claims.

- Indicators measure **states**
- Activities are **events**
- Changes in states are **events**
- Claims assert that an activity contributed to a change

This keeps the ontology honest, evidence-aware, and extensible.

---

## 2. Backbone Concepts from Existing Ontologies

### 2.1 ImpactOnt (What changed?)

Use these as-is:

- `impactont:Indicator`  
  A convention for measuring a state (unit, description, etc.)

- `impactont:State`  
  A condition of a thing, expressed using indicator–value pairs

- `impactont:Event`  
  A change between two states

Key properties:
- `impactont:isDefinedByIndicator`
- `impactont:hasIndicatorValue`
- `impactont:hasStateA` / `impactont:hasStateB`

---

### 2.2 AIAO (Who did what?)

- `aiao:Activity` ⊆ `impactont:Event`
- `aiao:Project` ⊆ `impactont:Process`
- `aiao:AgentActivityRelation` for accountable participation

Activities are therefore already compatible with state change modelling.

---

### 2.3 ClaimOnt (Why do we think it changed?)

- `aiao:ImpactClaim` ⊆ `claimont:Claim`

Use claims to assert:
> “This activity contributed to this observed change”

Claims can be supported, challenged, revised, or withdrawn.

---

## 3. Indicator Categorisation by Impact Pathway Stage (SKOS)

This is **classification**, not logic → use SKOS.

### 3.1 Indicator Stage Scheme

```turtle
ii:IndicatorStageScheme a skos:ConceptScheme ;
  skos:prefLabel "Indicator stages in an impact pathway"@en .
```

### 3.2 Stage Concepts

```turtle
ii:ActivityIndicator a skos:Concept ;
  skos:prefLabel "Activity indicator"@en ;
  skos:inScheme ii:IndicatorStageScheme .

ii:OutputIndicator a skos:Concept ;
  skos:prefLabel "Output indicator"@en ;
  skos:inScheme ii:IndicatorStageScheme .

ii:OutcomeIndicator a skos:Concept ;
  skos:prefLabel "Outcome indicator"@en ;
  skos:inScheme ii:IndicatorStageScheme .

ii:ImpactIndicator a skos:Concept ;
  skos:prefLabel "Impact indicator"@en ;
  skos:inScheme ii:IndicatorStageScheme .
```

### 3.3 Linking Indicators to Stages

```turtle
ii:hasIndicatorStage a owl:ObjectProperty ;
  rdfs:label "has indicator stage"@en ;
  rdfs:domain impactont:Indicator ;
  rdfs:range  skos:Concept .
```

---

## 4. Indicator Frameworks (SKOS Collections)

An **indicator framework** is a curated bundle across stages.

```turtle
ii:Poverty_ToC_Framework a skos:Collection ;
  skos:prefLabel "Poverty theory-of-change indicator framework"@en ;
  skos:member sdg:1.1.1 ;
  skos:member ii:SomeActivityIndicator ;
  skos:member ii:SomeOutputIndicator ;
  skos:member ii:SomeImpactIndicator .
```

Use `skos:OrderedCollection` if sequence matters.

---

## 5. Measurement Pattern (Baseline / Endline)

```turtle
ii:HouseholdGroupX a impactont:Thing ;
  rdfs:label "Households in area X"@en ;
  impactont:hasState ii:State_baseline, ii:State_endline .

ii:State_baseline a impactont:State ;
  impactont:isDefinedByIndicator sdg:1.1.1 ;
  impactont:hasIndicatorValue "0.42"^^xsd:decimal .

ii:State_endline a impactont:State ;
  impactont:isDefinedByIndicator sdg:1.1.1 ;
  impactont:hasIndicatorValue "0.35"^^xsd:decimal .
```

Time should be added using `impactont:hasTemporalLocation`.

---

## 6. Changes Required to Your Current Indicator Ontology

### A. Indicator Alignment (Chosen Option)

**Option 1 (selected):**  
➡ *Make each indicator definition instance also an `impactont:Indicator`.*

Example:

```turtle
sdg:1.1.1 a impactont:Indicator ;
  rdfs:label "Proportion of the population below the international poverty line"@en ;
  ii:hasIndicatorStage ii:OutcomeIndicator .
```

You keep your existing unit, formula, metadata, etc.

---

### B. Add State-Based Measurement (if not already present)

Ensure you can express:
- baseline state
- endline state
- indicator–value pairs

---

### C. Model Theory of Change as Claims (not facts)

```turtle
ii:Claim_ActivityA_reduced_poverty a aiao:ImpactClaim ;
  rdfs:label "Cash transfer activity reduced poverty"@en ;
  claimont:hasSubject ii:ActivityA ;
  claimont:hasObject  ii:State_endline .
```

Evidence can be attached using ClaimOnt support properties.

---

## 7. End-to-End Sample (Condensed)

```turtle
ii:ActivityA a aiao:Activity ;
  rdfs:label "Cash transfer disbursement"@en .

sdg:1.1.1 a impactont:Indicator ;
  rdfs:label "Proportion below poverty line"@en ;
  ii:hasIndicatorStage ii:OutcomeIndicator .

ii:State_endline a impactont:State ;
  impactont:isDefinedByIndicator sdg:1.1.1 ;
  impactont:hasIndicatorValue "0.35"^^xsd:decimal .

ii:Claim_ActivityA_reduced_poverty a aiao:ImpactClaim ;
  claimont:hasSubject ii:ActivityA ;
  claimont:hasObject ii:State_endline .
```

---

## 8. Final Checklist

- [ ] Indicators are instances of `impactont:Indicator`
- [ ] Measurements use `impactont:State`
- [ ] Activities are `aiao:Activity`
- [ ] Causality expressed via `aiao:ImpactClaim`
- [ ] Indicator stages use SKOS concepts
- [ ] Frameworks use `skos:Collection`

---

**Result:**  
You can now express projects, measurements, pathways, and causal reasoning **without overcommitting semantics**, while remaining compatible with SDGs and client-specific frameworks.
