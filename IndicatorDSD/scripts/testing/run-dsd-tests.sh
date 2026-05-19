#!/bin/bash
#
# DSD Integration Test Runner
# ============================
# 
# A user-friendly wrapper script for running the DSD integration tests
# with helpful output and error handling.
#
# Usage:
#   ./run-dsd-tests.sh [--install-deps] [--verbose] [--help]
#
# Options:
#   --install-deps    Install required Python dependencies before running
#   --verbose         Show detailed test output
#   --help            Show this help message
#

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Parse command line arguments
INSTALL_DEPS=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "DSD Integration Test Runner"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --install-deps    Install required Python dependencies"
            echo "  --verbose         Show detailed test output"
            echo "  --help            Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                       # Run tests with existing dependencies"
            echo "  $0 --install-deps        # Install deps and run tests"
            echo "  $0 --verbose             # Run tests with detailed output"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Print header
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  DSD Integration Test Suite - Phase 6${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
echo ""

# Install dependencies if requested
if [ "$INSTALL_DEPS" = true ]; then
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    if python3 -m pip install rdflib pyshacl --quiet; then
        echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        echo "Try running manually: pip install rdflib pyshacl"
        exit 1
    fi
    echo ""
fi

# Check if dependencies are available
echo -e "${YELLOW}Checking dependencies...${NC}"

DEPS_OK=true

if python3 -c "import rdflib" 2>/dev/null; then
    echo -e "${GREEN}✓ rdflib is installed${NC}"
else
    echo -e "${RED}✗ rdflib is not installed${NC}"
    DEPS_OK=false
fi

if python3 -c "import pyshacl" 2>/dev/null; then
    echo -e "${GREEN}✓ pyshacl is installed${NC}"
else
    echo -e "${YELLOW}⚠ pyshacl is not installed (SHACL validation will be skipped)${NC}"
fi

echo ""

if [ "$DEPS_OK" = false ]; then
    echo -e "${YELLOW}Some dependencies are missing. Install them with:${NC}"
    echo "  $0 --install-deps"
    echo "or manually:"
    echo "  pip install rdflib pyshacl"
    exit 1
fi

# Check if test script exists
if [ ! -f "$SCRIPT_DIR/dsd-integration-test.py" ]; then
    echo -e "${RED}Error: dsd-integration-test.py not found${NC}"
    exit 1
fi

# Check if TTL files exist
echo -e "${YELLOW}Checking for required data files...${NC}"
REQUIRED_FILES=(
    "../../axis-definitions.ttl"
    "../../scheme-definitions.ttl"
    "../../examples/dsd/dsd-examples.ttl"
    "../../IndicatorDSD/dsd-validation.ttl"
    "../../examples/observations/observation-examples.ttl"
)

FILES_OK=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo -e "${GREEN}✓ Found $(basename $file)${NC}"
    else
        echo -e "${RED}✗ Missing $file${NC}"
        FILES_OK=false
    fi
done

echo ""

if [ "$FILES_OK" = false ]; then
    echo -e "${RED}Some required files are missing${NC}"
    exit 1
fi

# Run the tests
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Running Integration Tests${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Change to script directory
cd "$SCRIPT_DIR"

# Run tests and capture output
if [ "$VERBOSE" = true ]; then
    python3 dsd-integration-test.py
    TEST_EXIT_CODE=$?
else
    # Run tests and capture output
    TEST_OUTPUT=$(python3 dsd-integration-test.py 2>&1)
    TEST_EXIT_CODE=$?
    
    # Print summary only (last part of output)
    echo "$TEST_OUTPUT" | tail -n 25
fi

echo ""

# Print final result
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✓ ALL TESTS PASSED${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${GREEN}Phase 6 integration testing completed successfully!${NC}"
    echo "All DSD components are working correctly together."
    echo ""
    echo "Next steps:"
    echo "  - Review ../../examples/queries/dsd-example-queries.sparql for query examples"
    echo "  - SDG-specific integration docs are maintained in skos_SDG"
    echo "  - Start using DSDs in your indicator observations"
else
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  ✗ SOME TESTS FAILED${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW}For detailed output, run:${NC}"
    echo "  $0 --verbose"
    echo ""
    echo -e "${YELLOW}For help, see:${NC}"
    echo "  - SDG-specific integration docs are maintained in skos_SDG"
    echo "  - dsd-integration-test.py output above for specific errors"
fi

echo ""
exit $TEST_EXIT_CODE


