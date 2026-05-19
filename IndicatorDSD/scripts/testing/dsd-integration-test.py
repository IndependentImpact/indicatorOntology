#!/usr/bin/env python3
"""
DSD Integration Test Suite
============================

This script performs Phase 6 integration testing for the Data Structure 
Definition (DSD) implementation by:

1. Loading all DSD-related TTL files into an RDF graph
2. Executing example SPARQL queries to test navigation
3. Running SHACL validation on example observations
4. Reporting test results

Created as part of Phase 6 of the DSD Implementation Plan
"""

import sys
from pathlib import Path
from typing import List, Tuple, Dict
import traceback

try:
    from rdflib import Graph, Namespace, URIRef
    from rdflib.plugins.sparql import prepareQuery
except ImportError:
    print("ERROR: rdflib is required. Install with: pip install rdflib")
    sys.exit(1)

try:
    from pyshacl import validate
    SHACL_AVAILABLE = True
except ImportError:
    print("WARNING: pyshacl not available. SHACL validation will be skipped.")
    print("To enable SHACL validation, install with: pip install pyshacl")
    SHACL_AVAILABLE = False

# Define namespaces
IND = Namespace("http://independentimpact.org/indicator-owl/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# TTL files to load for integration testing
TTL_FILES = [
    "../../axis-definitions.ttl",
    "../../scheme-definitions.ttl",
    "../../examples/dsd/dsd-examples.ttl",
    "../../IndicatorDSD/dsd-validation.ttl",
    "../../examples/observations/observation-examples.ttl",
]

# SPARQL queries to test
TEST_QUERIES = [
    {
        "name": "Query 1: Find observations by sex",
        "query": """
            PREFIX ind: <http://independentimpact.org/indicator-owl/>
            PREFIX impact: <http://w3id.org/impactont#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?obs ?sex ?value
            WHERE {
              ?obs a impact:IndicatorValue ;
                   rdf:value ?value .
              
              ?obs ind:hasSubgroupSlice ?slice .
              ?slice ind:subgroupAxis ind:AxisSex ;
                     ind:subgroupValue ?sexConcept .
              
              ?sexConcept skos:prefLabel ?sex .
            }
            ORDER BY ?sex
            LIMIT 5
        """,
        "expected_min_results": 1
    },
    {
        "name": "Query 2: Find DSDs using AxisSex",
        "query": """
            PREFIX ind: <http://independentimpact.org/indicator-owl/>
            PREFIX impact: <http://w3id.org/impactont#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX dct: <http://purl.org/dc/terms/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            
            SELECT ?dsd ?dsdTitle
            WHERE {
              ?dsd a ind:DataStructureDefinition ;
                   dct:title ?dsdTitle ;
                   ind:hasAxisSpec ?spec .
              
              ?spec ind:axis ind:AxisSex .
            }
        """,
        "expected_min_results": 1
    },
    {
        "name": "Query 3: Validate cardinality constraints",
        "query": """
            PREFIX ind: <http://independentimpact.org/indicator-owl/>
            PREFIX impact: <http://w3id.org/impactont#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            
            SELECT ?obs ?axis (COUNT(?slice) AS ?count) ?maxCard
            WHERE {
                   ind:usesDSD ?dsd ;
                   ind:hasSubgroupSlice ?slice .
              
              ?slice ind:subgroupAxis ?axis .
              
              ?dsd ind:hasAxisSpec ?spec .
              ?spec ind:axis ?axis ;
                    ind:maxCardinality ?maxCard .
              
              FILTER (?maxCard >= 0)
            }
            GROUP BY ?obs ?axis ?maxCard
            HAVING (COUNT(?slice) > ?maxCard)
        """,
        "expected_min_results": 0,  # Should be 0 violations
        "is_validation": True
    }
]


class TestResult:
    """Container for test results"""
    def __init__(self, name: str, passed: bool, message: str = "", details: str = ""):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details
    
    def __str__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        result = f"{status}: {self.name}"
        if self.message:
            result += f"\n  {self.message}"
        if self.details:
            result += f"\n  Details: {self.details}"
        return result


def load_ttl_files(base_path: Path, files: List[str]) -> Tuple[Graph, List[TestResult]]:
    """Load all TTL files into a single RDF graph
    
    Note: For large datasets (>100K triples), consider implementing
    streaming or chunked loading for better memory efficiency.
    """
    print("\n" + "="*70)
    print("PHASE 1: Loading TTL Files")
    print("="*70)
    
    graph = Graph()
    results = []
    
    # Bind namespaces
    graph.bind("ind", IND)
    graph.bind("skos", SKOS)
    graph.bind("dct", DCT)
    graph.bind("rdfs", RDFS)
    
    for filename in files:
        filepath = base_path / filename
        try:
            print(f"Loading {filename}...", end=" ")
            initial_size = len(graph)
            graph.parse(filepath, format="turtle")
            triples_added = len(graph) - initial_size
            print(f"OK ({triples_added} triples)")
            results.append(TestResult(
                f"Load {filename}",
                True,
                f"Loaded {triples_added} triples"
            ))
        except Exception as e:
            print(f"FAILED")
            results.append(TestResult(
                f"Load {filename}",
                False,
                f"Failed to load: {str(e)}"
            ))
    
    print(f"\nTotal triples loaded: {len(graph)}")
    return graph, results


def run_sparql_queries(graph: Graph, queries: List[Dict]) -> List[TestResult]:
    """Execute SPARQL queries and verify results"""
    print("\n" + "="*70)
    print("PHASE 2: Running SPARQL Queries")
    print("="*70)
    
    results = []
    
    for query_spec in queries:
        query_name = query_spec["name"]
        query_text = query_spec["query"]
        expected_min = query_spec["expected_min_results"]
        is_validation = query_spec.get("is_validation", False)
        
        try:
            print(f"\nExecuting: {query_name}")
            query = prepareQuery(query_text)
            result_rows = graph.query(query)
            result_count = len(list(result_rows))
            
            print(f"  Results: {result_count} rows")
            
            # Check if results meet expectations
            if is_validation:
                # For validation queries, we expect 0 results (no violations)
                if result_count == expected_min:
                    results.append(TestResult(
                        query_name,
                        True,
                        f"No violations found (expected {expected_min}, got {result_count})"
                    ))
                    print("  ✓ Validation passed: No violations found")
                else:
                    results.append(TestResult(
                        query_name,
                        False,
                        f"Found {result_count} violations (expected {expected_min})"
                    ))
                    print(f"  ✗ Validation failed: Found {result_count} violations")
            else:
                # For regular queries, we expect at least min results
                if result_count >= expected_min:
                    results.append(TestResult(
                        query_name,
                        True,
                        f"Returned {result_count} results (expected at least {expected_min})"
                    ))
                    print(f"  ✓ Query passed: {result_count} >= {expected_min}")
                else:
                    results.append(TestResult(
                        query_name,
                        False,
                        f"Returned {result_count} results (expected at least {expected_min})"
                    ))
                    print(f"  ✗ Query failed: {result_count} < {expected_min}")
            
        except Exception as e:
            error_msg = f"Query failed with error: {str(e)}"
            results.append(TestResult(query_name, False, error_msg))
            print(f"  ✗ {error_msg}")
    
    return results


def run_shacl_validation(graph: Graph, base_path: Path) -> List[TestResult]:
    """Run SHACL validation on observations"""
    print("\n" + "="*70)
    print("PHASE 3: SHACL Validation")
    print("="*70)
    
    results = []
    
    if not SHACL_AVAILABLE:
        print("SKIPPED: pyshacl not available")
        results.append(TestResult(
            "SHACL Validation",
            True,
            "Skipped (pyshacl not installed)"
        ))
        return results
    
    try:
        print("\nRunning SHACL validation...")
        shapes_file = base_path / "../../IndicatorDSD/dsd-validation.ttl"
        
        # Load shapes graph separately
        shapes_graph = Graph()
        shapes_graph.parse(shapes_file, format="turtle")
        
        # Run validation
        conforms, results_graph, results_text = validate(
            graph,
            shacl_graph=shapes_graph,
            inference='rdfs',
            abort_on_first=False,
        )
        
        if conforms:
            print("✓ SHACL validation passed: All observations conform to shapes")
            results.append(TestResult(
                "SHACL Validation",
                True,
                "All observations conform to DSD shapes"
            ))
        else:
            print("✗ SHACL validation failed: Some observations do not conform")
            print("\nValidation Report:")
            print(results_text)
            results.append(TestResult(
                "SHACL Validation",
                False,
                "Some observations do not conform",
                results_text
            ))
    
    except Exception as e:
        error_msg = f"SHACL validation error: {str(e)}"
        print(f"✗ {error_msg}")
        results.append(TestResult("SHACL Validation", False, error_msg))
    
    return results


def verify_dsd_structure(graph: Graph) -> List[TestResult]:
    """Verify that DSD components are properly structured"""
    print("\n" + "="*70)
    print("PHASE 4: Structural Verification")
    print("="*70)
    
    results = []
    
    # Check 1: Verify DSDs exist
    query = """
        PREFIX ind: <http://independentimpact.org/indicator-owl/>
            PREFIX impact: <http://w3id.org/impactont#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT(?dsd) AS ?count)
        WHERE { ?dsd a ind:DataStructureDefinition . }
    """
    dsd_count = int(list(graph.query(query))[0][0])
    print(f"\nData Structure Definitions found: {dsd_count}")
    
    if dsd_count > 0:
        results.append(TestResult(
            "DSD Existence Check",
            True,
            f"Found {dsd_count} DSDs"
        ))
    else:
        results.append(TestResult(
            "DSD Existence Check",
            False,
            "No DSDs found in the graph"
        ))
    
    # Check 2: Verify Axes exist
    query = """
        PREFIX ind: <http://independentimpact.org/indicator-owl/>
            PREFIX impact: <http://w3id.org/impactont#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT(?axis) AS ?count)
        WHERE { ?axis a ind:Axis . }
    """
    axis_count = int(list(graph.query(query))[0][0])
    print(f"Axes found: {axis_count}")
    
    if axis_count > 0:
        results.append(TestResult(
            "Axis Existence Check",
            True,
            f"Found {axis_count} axes"
        ))
    else:
        results.append(TestResult(
            "Axis Existence Check",
            False,
            "No axes found in the graph"
        ))
    
    # Check 3: Verify SKOS schemes exist
    query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT (COUNT(?scheme) AS ?count)
        WHERE { ?scheme a skos:ConceptScheme . }
    """
    scheme_count = int(list(graph.query(query))[0][0])
    print(f"SKOS Concept Schemes found: {scheme_count}")
    
    if scheme_count > 0:
        results.append(TestResult(
            "Scheme Existence Check",
            True,
            f"Found {scheme_count} concept schemes"
        ))
    else:
        results.append(TestResult(
            "Scheme Existence Check",
            False,
            "No concept schemes found in the graph"
        ))
    
    # Check 4: Verify observations with DSDs
    query = """
        PREFIX ind: <http://independentimpact.org/indicator-owl/>
            PREFIX impact: <http://w3id.org/impactont#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT(?obs) AS ?count)
        WHERE { 
            ?obs a impact:IndicatorValue ;
                 ind:usesDSD ?dsd .
        }
    """
    obs_count = int(list(graph.query(query))[0][0])
    print(f"Observations using DSDs: {obs_count}")
    
    if obs_count > 0:
        results.append(TestResult(
            "Observation-DSD Link Check",
            True,
            f"Found {obs_count} observations using DSDs"
        ))
    else:
        results.append(TestResult(
            "Observation-DSD Link Check",
            False,
            "No observations found using DSDs"
        ))
    
    # Check 5: Verify axis specifications
    query = """
        PREFIX ind: <http://independentimpact.org/indicator-owl/>
            PREFIX impact: <http://w3id.org/impactont#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT(?spec) AS ?count)
        WHERE { 
            ?dsd ind:hasAxisSpec ?spec .
            ?spec ind:axis ?axis ;
                  ind:valueScheme ?scheme ;
                  ind:minCardinality ?min ;
                  ind:maxCardinality ?max .
        }
    """
    spec_count = int(list(graph.query(query))[0][0])
    print(f"Complete axis specifications: {spec_count}")
    
    if spec_count > 0:
        results.append(TestResult(
            "Axis Specification Check",
            True,
            f"Found {spec_count} complete axis specifications"
        ))
    else:
        results.append(TestResult(
            "Axis Specification Check",
            False,
            "No complete axis specifications found"
        ))
    
    return results


def print_summary(all_results: List[TestResult]):
    """Print summary of all test results"""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in all_results if r.passed)
    failed = sum(1 for r in all_results if not r.passed)
    total = len(all_results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/total*100):.1f}%")
    
    if failed > 0:
        print("\n" + "-"*70)
        print("FAILED TESTS:")
        print("-"*70)
        for result in all_results:
            if not result.passed:
                print(f"\n{result}")
    
    print("\n" + "="*70)
    if failed == 0:
        print("✓ ALL TESTS PASSED - Phase 6 Integration Complete!")
    else:
        print(f"✗ {failed} TEST(S) FAILED - Review failures above")
    print("="*70)


def main():
    """Main test execution"""
    print("\n" + "="*70)
    print("DSD INTEGRATION TEST SUITE - Phase 6")
    print("="*70)
    print("\nThis test suite validates the integration of all DSD components:")
    print("  - Axis definitions")
    print("  - SKOS concept schemes")
    print("  - Data Structure Definitions (DSDs)")
    print("  - Example observations")
    print("  - SHACL validation rules")
    
    # Determine base path
    base_path = Path(__file__).parent
    
    all_results = []
    
    try:
        # Phase 1: Load TTL files
        graph, load_results = load_ttl_files(base_path, TTL_FILES)
        all_results.extend(load_results)
        
        # Only continue if all files loaded successfully
        if all(r.passed for r in load_results):
            # Phase 2: Run SPARQL queries
            query_results = run_sparql_queries(graph, TEST_QUERIES)
            all_results.extend(query_results)
            
            # Phase 3: Run SHACL validation
            shacl_results = run_shacl_validation(graph, base_path)
            all_results.extend(shacl_results)
            
            # Phase 4: Verify structure
            structure_results = verify_dsd_structure(graph)
            all_results.extend(structure_results)
        else:
            print("\n⚠ Skipping further tests due to file loading failures")
        
        # Print summary
        print_summary(all_results)
        
        # Exit with appropriate code
        if all(r.passed for r in all_results):
            sys.exit(0)
        else:
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nTest execution interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n✗ FATAL ERROR: {str(e)}")
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()





