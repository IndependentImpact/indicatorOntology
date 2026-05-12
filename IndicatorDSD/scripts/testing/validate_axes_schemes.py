#!/usr/bin/env python3
"""
Validate axes and schemes definitions.
Checks that all axes and schemes are properly structured.
"""

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, DCTERMS
import sys
from pathlib import Path

IND = Namespace("http://independentimpact.org/indicator-owl/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

def validate_axes(graph):
    """Validate axis definitions."""
    errors = []
    warnings = []
    
    # Try both possible type names
    axes = list(graph.subjects(RDF.type, IND.DisaggregationAxis))
    if not axes:
        axes = list(graph.subjects(RDF.type, IND.Axis))
    
    print(f"   Found {len(axes)} axes")
    
    for axis in axes:
        axis_name = str(axis).split('/')[-1]
        
        # Check has label (either rdfs:label or skos:prefLabel)
        label = graph.value(axis, RDFS.label)
        if not label:
            label = graph.value(axis, SKOS.prefLabel)
        if not label:
            warnings.append(f"Axis {axis_name} missing label (rdfs:label or skos:prefLabel)")
        
        # Check has description (optional but recommended)
        desc = graph.value(axis, RDFS.comment)
        if not desc:
            # Don't warn if it's a simple axis
            pass
    
    return axes, errors, warnings

def validate_schemes(graph):
    """Validate scheme definitions."""
    errors = []
    warnings = []
    
    schemes = list(graph.subjects(RDF.type, SKOS.ConceptScheme))
    print(f"   Found {len(schemes)} schemes")
    
    for scheme in schemes:
        scheme_name = str(scheme).split('/')[-1]
        
        # Check has label (prefer skos:prefLabel, fallback to rdfs:label)
        label = graph.value(scheme, SKOS.prefLabel)
        if not label:
            label = graph.value(scheme, RDFS.label)
        if not label:
            errors.append(f"Scheme {scheme_name} missing label (skos:prefLabel or rdfs:label)")
        
        # Check has concepts
        concepts = list(graph.objects(scheme, SKOS.hasTopConcept))
        if not concepts:
            # Try finding concepts that reference this scheme
            concepts = list(graph.subjects(SKOS.inScheme, scheme))
            if not concepts:
                warnings.append(f"Scheme {scheme_name} has no concepts")
        
        # Check each concept
        for concept in concepts:
            concept_name = str(concept).split('/')[-1]
            
            # Check concept has label (prefer skos:prefLabel)
            concept_label = graph.value(concept, SKOS.prefLabel)
            if not concept_label:
                concept_label = graph.value(concept, RDFS.label)
                if not concept_label:
                    errors.append(f"Concept {concept_name} in {scheme_name} missing label")
    
    return schemes, errors, warnings

def main():
    """Validate axes and schemes."""
    
    print("📖 Loading definitions...")
    g = Graph()
    g.bind('ind', IND)
    g.bind('skos', SKOS)
    
    axis_file = Path('../../axis-definitions.ttl')
    scheme_file = Path('../../scheme-definitions.ttl')
    
    if not axis_file.exists():
        print(f"❌ Error: {axis_file} not found", file=sys.stderr)
        sys.exit(1)
    
    if not scheme_file.exists():
        print(f"❌ Error: {scheme_file} not found", file=sys.stderr)
        sys.exit(1)
    
    g.parse(axis_file, format='turtle')
    g.parse(scheme_file, format='turtle')
    
    # Validate axes
    print("\n🔍 Validating axes...")
    axes, axis_errors, axis_warnings = validate_axes(g)
    
    # Validate schemes
    print("\n🔍 Validating schemes...")
    schemes, scheme_errors, scheme_warnings = validate_schemes(g)
    
    # Print results
    print(f"\n{'='*60}")
    print(f"AXES AND SCHEMES VALIDATION RESULTS")
    print(f"{'='*60}")
    print(f"Axes:    {len(axes)}")
    print(f"Schemes: {len(schemes)}")
    print(f"Errors:   {len(axis_errors) + len(scheme_errors)}")
    print(f"Warnings: {len(axis_warnings) + len(scheme_warnings)}")
    print(f"{'='*60}")
    
    # Show errors
    all_errors = axis_errors + scheme_errors
    if all_errors:
        print("\n❌ Errors:")
        for error in all_errors:
            print(f"   - {error}")
    
    # Show warnings
    all_warnings = axis_warnings + scheme_warnings
    if all_warnings:
        print("\n⚠️  Warnings:")
        for warning in all_warnings[:10]:  # Show first 10
            print(f"   - {warning}")
        if len(all_warnings) > 10:
            print(f"   ... and {len(all_warnings) - 10} more")
    
    # Success criteria
    if all_errors:
        print("\n❌ VALIDATION FAILED")
        sys.exit(1)
    else:
        print("\n✅ VALIDATION PASSED")
        if all_warnings:
            print(f"   (with {len(all_warnings)} warnings)")
        sys.exit(0)

if __name__ == "__main__":
    main()

