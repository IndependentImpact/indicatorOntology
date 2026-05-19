#!/usr/bin/env python3
"""
Generate comprehensive DSD definitions based on pattern analysis.
Creates DSDs for all common disaggregation patterns.

Part of Phase 3: DSD Design and Creation
"""

import sys
from datetime import date

TODAY = date.today().isoformat()

# Prefix declarations
PREFIXES = """@prefix ind: <http://independentimpact.org/indicator-owl/> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

"""

def generate_axis_spec(dsd_id, axis_name, scheme_name, min_card=0, max_card=1):
    """Generate an axis specification."""
    spec_id = f"Spec_{dsd_id}_{axis_name}"
    return f"""
ind:{spec_id} a ind:AxisSpecification ;
  ind:axis ind:Axis{axis_name} ;
  ind:axisRole ind:DimensionRole ;
  ind:valueScheme ind:{scheme_name} ;
  ind:minCardinality {min_card} ;
  ind:maxCardinality {max_card} ;
  rdfs:comment "Disaggregation by {axis_name.lower()}"@en ."""

def generate_dsd(dsd_id, title, description, axes):
    """
    Generate a complete DSD definition.
    axes: list of tuples (axis_name, scheme_name, min_card, max_card)
    """
    output = f"""
#################################################################
# {dsd_id}
#################################################################

ind:{dsd_id} a ind:DataStructureDefinition ;
  dct:title "{title}"@en ;
  dct:description "{description}"@en ;
  dct:created "{TODAY}"^^xsd:date ;
  dct:creator "Independent Impact SDG Ontology Project"@en"""
    
    # Add axis specs if present
    if axes:
        spec_refs = [f"ind:Spec_{dsd_id}_{axis[0]}" for axis in axes]
        spec_list = " ,\n                    ".join(spec_refs)
        output += f" ;\n  ind:hasAxisSpec {spec_list}"
    
    output += " .\n"
    
    # Generate each axis specification
    for axis_name, scheme_name, min_card, max_card in axes:
        output += generate_axis_spec(dsd_id, axis_name, scheme_name, min_card, max_card)
        output += "\n"
    
    return output

def main():
    print(PREFIXES)
    
    print("""#################################################################
# DATA STRUCTURE DEFINITIONS - COMPREHENSIVE COVERAGE
# Generated for Phase 3 of DSD Completion Plan
# Date: """ + TODAY + """
#################################################################

""")
    
    # Pattern 1: No disaggregation (106 indicators - 42%)
    print(generate_dsd(
        "DSD_Simple_NoDisaggregation_v1",
        "Simple indicator with no disaggregation",
        "For aggregate counts, percentages, and indicators without demographic or geographic disaggregation.",
        []
    ))
    
    # Pattern 2: Sex only (52 indicators - 21%)
    print(generate_dsd(
        "DSD_Social_Sex_v1",
        "Social indicator with sex disaggregation",
        "For indicators requiring only sex/gender disaggregation.",
        [("Sex", "SexScheme_v1", 0, 1)]
    ))
    
    # Pattern 3: Age + Sex (18 indicators - 7%)
    print(generate_dsd(
        "DSD_Social_SexAge_v1",
        "Social indicator with sex and age disaggregation",
        "For indicators requiring disaggregation by sex and age groups.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("AgeCategory", "GlobalAgeScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 4: Sector only (10 indicators - 4%)
    print(generate_dsd(
        "DSD_Economic_Sector_v1",
        "Economic indicator with sector disaggregation",
        "For indicators requiring disaggregation by economic sector (agriculture, industry, services).",
        [("EconomicSector", "EconomicSectorScheme_v1", 0, 1)]
    ))
    
    # Pattern 5: Age + Disability + Sex (7 indicators - 3%)
    print(generate_dsd(
        "DSD_Social_SexAgeDisability_v1",
        "Social indicator with sex, age, and disability disaggregation",
        "For indicators requiring disaggregation by sex, age, and disability status.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("AgeCategory", "GlobalAgeScheme_v1", 0, 1),
            ("DisabilityStatus", "DisabilityStatusScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 6: Age only (7 indicators - 3%)
    print(generate_dsd(
        "DSD_Social_Age_v1",
        "Social indicator with age disaggregation",
        "For indicators requiring only age group disaggregation.",
        [("AgeCategory", "GlobalAgeScheme_v1", 0, 1)]
    ))
    
    # Pattern 7: Health condition (7 indicators - 3%)
    print(generate_dsd(
        "DSD_Health_Condition_v1",
        "Health indicator with condition disaggregation",
        "For health indicators requiring disaggregation by disease type or health category.",
        [("HealthCondition", "HealthConditionScheme_v1", 0, 1)]
    ))
    
    # Pattern 8: Migration + Sex (5 indicators - 2%)
    print(generate_dsd(
        "DSD_Social_SexMigration_v1",
        "Social indicator with sex and migration status disaggregation",
        "For indicators related to migrants, refugees, and citizenship.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("MigrationStatus", "MigrationStatusScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 9: Sector + Sex (4 indicators - 2%)
    print(generate_dsd(
        "DSD_Economic_SexSector_v1",
        "Economic indicator with sex and sector disaggregation",
        "For economic indicators requiring disaggregation by sex and economic sector.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("EconomicSector", "EconomicSectorScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 10: Location + Sex (4 indicators - 2%)
    print(generate_dsd(
        "DSD_Social_SexLocation_v1",
        "Social indicator with sex and location disaggregation",
        "For indicators requiring disaggregation by sex and urban/rural location.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("UrbanRural", "UrbanRuralScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 11: Education only (4 indicators - 2%)
    print(generate_dsd(
        "DSD_Education_Level_v1",
        "Education indicator with education level disaggregation",
        "For indicators requiring disaggregation by education level or attainment.",
        [("EducationLevel", "EducationLevelScheme_v1", 0, 1)]
    ))
    
    # Pattern 12: Income + Sex (3 indicators - 1%)
    print(generate_dsd(
        "DSD_Economic_SexIncome_v1",
        "Economic indicator with sex and income disaggregation",
        "For indicators requiring disaggregation by sex and income quintile or wealth.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("IncomeQuintile", "IncomeQuintileScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 13: Sex + Tenure (2 indicators)
    print(generate_dsd(
        "DSD_Social_SexTenure_v1",
        "Social indicator with sex and tenure type disaggregation",
        "For indicators related to land rights and tenure security.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("TenureType", "TenureTypeScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 14: Household + Income (2 indicators)
    print(generate_dsd(
        "DSD_Economic_HouseholdIncome_v1",
        "Economic indicator with household and income disaggregation",
        "For household-level economic indicators with income classification.",
        [
            ("HouseholdType", "HouseholdTypeScheme_v1", 0, 1),
            ("IncomeQuintile", "IncomeQuintileScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 15: Education + Sex (2 indicators)
    print(generate_dsd(
        "DSD_Education_SexLevel_v1",
        "Education indicator with sex and education level disaggregation",
        "For education indicators requiring disaggregation by sex and education level.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("EducationLevel", "EducationLevelScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 16: Employment only (2 indicators)
    print(generate_dsd(
        "DSD_Economic_Employment_v1",
        "Economic indicator with employment status disaggregation",
        "For labor market indicators requiring employment status disaggregation.",
        [("EmploymentStatus", "EmploymentStatusScheme_v1", 0, 1)]
    ))
    
    # Pattern 17: Age + Employment + Location + Sex (1 indicator - 1.1.1)
    print(generate_dsd(
        "DSD_Social_Extended_v1",
        "Extended social indicator with multiple disaggregations",
        "For comprehensive social indicators requiring sex, age, employment, and location disaggregation.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("AgeCategory", "GlobalAgeScheme_v1", 0, 1),
            ("EmploymentStatus", "EmploymentStatusScheme_v1", 0, 1),
            ("UrbanRural", "UrbanRuralScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 18: Complex vulnerability (1 indicator - 1.3.1)
    print(generate_dsd(
        "DSD_Social_Comprehensive_v1",
        "Comprehensive social protection indicator",
        "For social protection indicators with multiple vulnerability dimensions.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("AgeCategory", "GlobalAgeScheme_v1", 0, 1),
            ("DisabilityStatus", "DisabilityStatusScheme_v1", 0, 1),
            ("EmploymentStatus", "EmploymentStatusScheme_v1", 0, 1),
            ("PregnancyStatus", "PregnancyStatusScheme_v1", 0, 1),
            ("VulnerabilityCategory", "VulnerabilityCategoryScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 19: Household + Sector (1 indicator)
    print(generate_dsd(
        "DSD_Economic_HouseholdSector_v1",
        "Economic indicator with household and sector disaggregation",
        "For household-level economic indicators with sector classification.",
        [
            ("HouseholdType", "HouseholdTypeScheme_v1", 0, 1),
            ("EconomicSector", "EconomicSectorScheme_v1", 0, 1)
        ]
    ))
    
    # Pattern 20: Vulnerability only (1 indicator)
    print(generate_dsd(
        "DSD_Social_Vulnerability_v1",
        "Social indicator with vulnerability disaggregation",
        "For indicators focused on vulnerable populations.",
        [("VulnerabilityCategory", "VulnerabilityCategoryScheme_v1", 0, 1)]
    ))
    
    # Additional commonly needed patterns not in top 20
    
    # Sex + Age + Location (common SDG pattern)
    print(generate_dsd(
        "DSD_Social_SexAgeLocation_v1",
        "Social indicator with sex, age, and location disaggregation",
        "For social indicators requiring comprehensive demographic and geographic disaggregation.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("AgeCategory", "GlobalAgeScheme_v1", 0, 1),
            ("UrbanRural", "UrbanRuralScheme_v1", 0, 1)
        ]
    ))
    
    # Health with Sex and Age
    print(generate_dsd(
        "DSD_Health_SexAge_v1",
        "Health indicator with sex and age disaggregation",
        "For health indicators requiring demographic disaggregation.",
        [
            ("Sex", "SexScheme_v1", 0, 1),
            ("AgeCategory", "GlobalAgeScheme_v1", 0, 1)
        ]
    ))
    
    # Health comprehensive
    print(generate_dsd(
        "DSD_Health_Comprehensive_v1",
        "Comprehensive health indicator with condition, sex, and age",
        "For detailed health indicators requiring condition type with demographic disaggregation.",
        [
            ("HealthCondition", "HealthConditionScheme_v1", 0, 1),
            ("Sex", "SexScheme_v1", 0, 1),
            ("AgeCategory", "GlobalAgeScheme_v1", 0, 1)
        ]
    ))
    
    print("\n# End of DSD definitions")

if __name__ == "__main__":
    main()
