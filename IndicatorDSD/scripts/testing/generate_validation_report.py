#!/usr/bin/env python3
"""
Thin wrapper to run the canonical DSD validation report generator
from indicatorOntology/IndicatorDSD.
"""

from pathlib import Path
import runpy
import sys

canonical = (Path(__file__).resolve().parents[3] /
             'indicatorOntology' / 'IndicatorDSD' / 'scripts' / 'testing' /
             'generate_validation_report.py')

if not canonical.exists():
    print(f"Error: canonical script not found at {canonical}", file=sys.stderr)
    sys.exit(1)

runpy.run_path(str(canonical), run_name='__main__')
