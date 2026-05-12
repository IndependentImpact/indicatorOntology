#!/usr/bin/env python3
"""
Validate DSD structural integrity.
Checks that DSDs, axes, and schemes are properly defined.

Part of Phase 3 validation
"""

import sys
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, SKOS

IND = Namespace("http://independentimpact.org/indicator-owl/")

def validate_dsds(graph):
    """Validate DSD definitions."""
    errors = []
    warnings = []
    
    # Check all DSDs
    dsds = list(graph.subjects(RDF.type, IND.DataStructureDefinition))
    print(f"✓ Found {len(dsds)} DSDs")
    
    for dsd in dsds:
        dsd_name = str(dsd).split('/')[-1]
        
        # Check has axis specs (optional - some DSDs have no disaggregation)
        specs = list(graph.objects(dsd, IND.hasAxisSpec))
        if not specs:
            # This is OK for NoDisaggregation DSD
            if 'NoDisaggregation' not in dsd_name:
                warnings.append(f"DSD {dsd_name} has no axis specifications")
        
        # Check each spec
        for spec in specs:
            axis = graph.value(spec, IND.axis)
            scheme = graph.value(spec, IND.valueScheme)
            
            if not axis:
                errors.append(f"Spec {spec} missing axis reference")
            if not scheme:
                errors.append(f"Spec {spec} missing scheme reference")
    
    return errors, warnings

def validate_axes(graph):
    """Validate axis definitions."""
    errors = []
    
    axes = list(graph.subjects(RDF.type, IND.Axis))
    print(f"✓ Found {len(axes)} axes")
    
    for axis in axes:
        label = graph.value(axis, RDFS.label)
        definition = graph.value(axis, SKOS.definition)
        
        if not label:
            errors.append(f"Axis {axis} missing rdfs:label")
        if not definition:
            errors.append(f"Axis {axis} missing skos:definition")
    
    return errors

def validate_schemes(graph):
    """Validate scheme definitions."""
    errors = []
    
    schemes = list(graph.subjects(RDF.type, SKOS.ConceptScheme))
    print(f"✓ Found {len(schemes)} schemes")
    
    for scheme in schemes:
        label = graph.value(scheme, SKOS.prefLabel)
        concepts = list(graph.objects(scheme, SKOS.hasTopConcept))
        
        if not label:
            errors.append(f"Scheme {scheme} missing skos:prefLabel")
        if not concepts:
            errors.append(f"Scheme {scheme} has no top concepts")
    
    return errors

def main():
    print("=" * 70)
    print("DSD STRUCTURAL VALIDATION")
    print("=" * 70)
    print()
    
    # Load all DSD-related files
    g = Graph()
    
    files_to_load = [
        ("../../../../skos_SDG/ontologies/dsd/dsd-complete.ttl", "DSDs"),
        ("../../axis-definitions.ttl", "Axes"),
        ("../../scheme-definitions.ttl", "Schemes")
    ]
    
    for filepath, name in files_to_load:
        try:
            g.parse(filepath, format="turtle")
            print(f"✓ Loaded {name}: {filepath}")
        except Exception as e:
            print(f"✗ Error loading {name}: {e}")
            sys.exit(1)
    
    print()
    
    # Validate DSDs
    print("Validating DSDs...")
    dsd_errors, dsd_warnings = validate_dsds(g)
    
    # Validate Axes
    print("Validating Axes...")
    axis_errors = validate_axes(g)
    
    # Validate Schemes
    print("Validating Schemes...")
    scheme_errors = validate_schemes(g)
    
    print()
    print("=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)
    print()
    
    all_errors = dsd_errors + axis_errors + scheme_errors
    
    if dsd_warnings:
        print(f"⚠ Warnings ({len(dsd_warnings)}):")
        for warning in dsd_warnings:
            print(f"  - {warning}")
        print()
    
    if all_errors:
        print(f"✗ Errors ({len(all_errors)}):")
        for error in all_errors:
            print(f"  - {error}")
        print()
        print("❌ Validation FAILED")
        sys.exit(1)
    else:
        print("✅ All validations PASSED")
        print()
        print("Summary:")
        print(f"  - {len(list(g.subjects(RDF.type, IND.DataStructureDefinition)))} DSDs validated")
        print(f"  - {len(list(g.subjects(RDF.type, IND.Axis)))} axes validated")
        print(f"  - {len(list(g.subjects(RDF.type, SKOS.ConceptScheme)))} schemes validated")
        if dsd_warnings:
            print(f"  - {len(dsd_warnings)} warnings (non-critical)")

if __name__ == "__main__":
    main()




