#!/usr/bin/env python3
"""
Generate additional axes and schemes needed for DSD coverage.
Extends existing axis-definitions.ttl and scheme-definitions.ttl.

Part of Phase 3: DSD Design and Creation
"""

import sys
from datetime import date

def generate_additional_axes():
    """Generate Turtle for additional axes needed."""
    
    axes = """
# Additional axes for comprehensive DSD coverage

# Economic Sector Axis
ind:AxisEconomicSector a ind:Axis ;
  rdfs:label "Economic sector"@en ;
  skos:definition "Classification by primary economic sector (agriculture, industry, services)."@en .

# Health Condition Axis
ind:AxisHealthCondition a ind:Axis ;
  rdfs:label "Health condition"@en ;
  skos:definition "Classification by disease type, cause of death, or health category."@en .

# Tenure Type Axis
ind:AxisTenureType a ind:Axis ;
  rdfs:label "Tenure type"@en ;
  skos:definition "Classification by type of land or property tenure rights."@en .

# Household Type Axis
ind:AxisHouseholdType a ind:Axis ;
  rdfs:label "Household type"@en ;
  skos:definition "Classification by household characteristics or composition."@en .

# Pregnancy Status Axis
ind:AxisPregnancyStatus a ind:Axis ;
  rdfs:label "Pregnancy status"@en ;
  skos:definition "Classification by pregnancy and maternal health status."@en .

# Vulnerability Category Axis
ind:AxisVulnerabilityCategory a ind:Axis ;
  rdfs:label "Vulnerability category"@en ;
  skos:definition "Classification by vulnerability or poverty status."@en .

# Ethnicity Axis
ind:AxisEthnicity a ind:Axis ;
  rdfs:label "Ethnicity"@en ;
  skos:definition "Classification by ethnic group or indigenous status."@en .

# Marital Status Axis
ind:AxisMaritalStatus a ind:Axis ;
  rdfs:label "Marital status"@en ;
  skos:definition "Classification by marital or partnership status."@en .
"""
    return axes

def generate_additional_schemes():
    """Generate Turtle for additional schemes needed."""
    
    schemes = """
#################################################################
# Economic Sector Scheme
#################################################################

ind:EconomicSectorScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Economic sector scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:sector_agriculture , ind:sector_industry , 
                     ind:sector_services .

ind:sector_agriculture a skos:Concept ;
  skos:prefLabel "Agriculture"@en ;
  skos:inScheme ind:EconomicSectorScheme_v1 ;
  skos:topConceptOf ind:EconomicSectorScheme_v1 ;
  skos:notation "AGR" .

ind:sector_industry a skos:Concept ;
  skos:prefLabel "Industry"@en ;
  skos:inScheme ind:EconomicSectorScheme_v1 ;
  skos:topConceptOf ind:EconomicSectorScheme_v1 ;
  skos:notation "IND" .

ind:sector_services a skos:Concept ;
  skos:prefLabel "Services"@en ;
  skos:inScheme ind:EconomicSectorScheme_v1 ;
  skos:topConceptOf ind:EconomicSectorScheme_v1 ;
  skos:notation "SRV" .

#################################################################
# Employment Status Scheme
#################################################################

ind:EmploymentStatusScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Employment status scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:employment_employed , ind:employment_unemployed ,
                     ind:employment_not_in_labor_force .

ind:employment_employed a skos:Concept ;
  skos:prefLabel "Employed"@en ;
  skos:inScheme ind:EmploymentStatusScheme_v1 ;
  skos:topConceptOf ind:EmploymentStatusScheme_v1 ;
  skos:notation "EMP" .

ind:employment_unemployed a skos:Concept ;
  skos:prefLabel "Unemployed"@en ;
  skos:inScheme ind:EmploymentStatusScheme_v1 ;
  skos:topConceptOf ind:EmploymentStatusScheme_v1 ;
  skos:notation "UNE" .

ind:employment_not_in_labor_force a skos:Concept ;
  skos:prefLabel "Not in labor force"@en ;
  skos:inScheme ind:EmploymentStatusScheme_v1 ;
  skos:topConceptOf ind:EmploymentStatusScheme_v1 ;
  skos:notation "NLF" .

#################################################################
# Disability Status Scheme
#################################################################

ind:DisabilityStatusScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Disability status scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:disability_with_disability , 
                     ind:disability_without_disability .

ind:disability_with_disability a skos:Concept ;
  skos:prefLabel "Persons with disabilities"@en ;
  skos:inScheme ind:DisabilityStatusScheme_v1 ;
  skos:topConceptOf ind:DisabilityStatusScheme_v1 ;
  skos:notation "PWD" .

ind:disability_without_disability a skos:Concept ;
  skos:prefLabel "Persons without disabilities"@en ;
  skos:inScheme ind:DisabilityStatusScheme_v1 ;
  skos:topConceptOf ind:DisabilityStatusScheme_v1 ;
  skos:notation "WOD" .

#################################################################
# Migration Status Scheme
#################################################################

ind:MigrationStatusScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Migration status scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:migration_citizen , ind:migration_migrant ,
                     ind:migration_refugee .

ind:migration_citizen a skos:Concept ;
  skos:prefLabel "Citizen"@en ;
  skos:inScheme ind:MigrationStatusScheme_v1 ;
  skos:topConceptOf ind:MigrationStatusScheme_v1 ;
  skos:notation "CTZ" .

ind:migration_migrant a skos:Concept ;
  skos:prefLabel "Migrant"@en ;
  skos:inScheme ind:MigrationStatusScheme_v1 ;
  skos:topConceptOf ind:MigrationStatusScheme_v1 ;
  skos:notation "MIG" .

ind:migration_refugee a skos:Concept ;
  skos:prefLabel "Refugee"@en ;
  skos:inScheme ind:MigrationStatusScheme_v1 ;
  skos:topConceptOf ind:MigrationStatusScheme_v1 ;
  skos:notation "REF" .

#################################################################
# Education Level Scheme
#################################################################

ind:EducationLevelScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Education level scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:education_no_education , ind:education_primary ,
                     ind:education_secondary , ind:education_tertiary .

ind:education_no_education a skos:Concept ;
  skos:prefLabel "No formal education"@en ;
  skos:inScheme ind:EducationLevelScheme_v1 ;
  skos:topConceptOf ind:EducationLevelScheme_v1 ;
  skos:notation "EDU0" .

ind:education_primary a skos:Concept ;
  skos:prefLabel "Primary education"@en ;
  skos:inScheme ind:EducationLevelScheme_v1 ;
  skos:topConceptOf ind:EducationLevelScheme_v1 ;
  skos:notation "EDU1" .

ind:education_secondary a skos:Concept ;
  skos:prefLabel "Secondary education"@en ;
  skos:inScheme ind:EducationLevelScheme_v1 ;
  skos:topConceptOf ind:EducationLevelScheme_v1 ;
  skos:notation "EDU2" .

ind:education_tertiary a skos:Concept ;
  skos:prefLabel "Tertiary education"@en ;
  skos:inScheme ind:EducationLevelScheme_v1 ;
  skos:topConceptOf ind:EducationLevelScheme_v1 ;
  skos:notation "EDU3" .

#################################################################
# Health Condition Scheme (Generic)
#################################################################

ind:HealthConditionScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Health condition scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:definition "Generic health condition categories for SDG indicators."@en ;
  skos:hasTopConcept ind:health_communicable , ind:health_noncommunicable ,
                     ind:health_maternal , ind:health_child ,
                     ind:health_injury .

ind:health_communicable a skos:Concept ;
  skos:prefLabel "Communicable diseases"@en ;
  skos:inScheme ind:HealthConditionScheme_v1 ;
  skos:topConceptOf ind:HealthConditionScheme_v1 ;
  skos:notation "COM" .

ind:health_noncommunicable a skos:Concept ;
  skos:prefLabel "Non-communicable diseases"@en ;
  skos:inScheme ind:HealthConditionScheme_v1 ;
  skos:topConceptOf ind:HealthConditionScheme_v1 ;
  skos:notation "NCD" .

ind:health_maternal a skos:Concept ;
  skos:prefLabel "Maternal health"@en ;
  skos:inScheme ind:HealthConditionScheme_v1 ;
  skos:topConceptOf ind:HealthConditionScheme_v1 ;
  skos:notation "MAT" .

ind:health_child a skos:Concept ;
  skos:prefLabel "Child health"@en ;
  skos:inScheme ind:HealthConditionScheme_v1 ;
  skos:topConceptOf ind:HealthConditionScheme_v1 ;
  skos:notation "CHD" .

ind:health_injury a skos:Concept ;
  skos:prefLabel "Injuries"@en ;
  skos:inScheme ind:HealthConditionScheme_v1 ;
  skos:topConceptOf ind:HealthConditionScheme_v1 ;
  skos:notation "INJ" .

#################################################################
# Tenure Type Scheme
#################################################################

ind:TenureTypeScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Tenure type scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:tenure_owned , ind:tenure_rented ,
                     ind:tenure_customary , ind:tenure_informal .

ind:tenure_owned a skos:Concept ;
  skos:prefLabel "Owned with title"@en ;
  skos:inScheme ind:TenureTypeScheme_v1 ;
  skos:topConceptOf ind:TenureTypeScheme_v1 ;
  skos:notation "OWN" .

ind:tenure_rented a skos:Concept ;
  skos:prefLabel "Rented"@en ;
  skos:inScheme ind:TenureTypeScheme_v1 ;
  skos:topConceptOf ind:TenureTypeScheme_v1 ;
  skos:notation "RNT" .

ind:tenure_customary a skos:Concept ;
  skos:prefLabel "Customary rights"@en ;
  skos:inScheme ind:TenureTypeScheme_v1 ;
  skos:topConceptOf ind:TenureTypeScheme_v1 ;
  skos:notation "CST" .

ind:tenure_informal a skos:Concept ;
  skos:prefLabel "Informal/no documentation"@en ;
  skos:inScheme ind:TenureTypeScheme_v1 ;
  skos:topConceptOf ind:TenureTypeScheme_v1 ;
  skos:notation "INF" .

#################################################################
# Household Type Scheme
#################################################################

ind:HouseholdTypeScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Household type scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:household_single , ind:household_couple ,
                     ind:household_nuclear , ind:household_extended .

ind:household_single a skos:Concept ;
  skos:prefLabel "Single person"@en ;
  skos:inScheme ind:HouseholdTypeScheme_v1 ;
  skos:topConceptOf ind:HouseholdTypeScheme_v1 ;
  skos:notation "SIN" .

ind:household_couple a skos:Concept ;
  skos:prefLabel "Couple without children"@en ;
  skos:inScheme ind:HouseholdTypeScheme_v1 ;
  skos:topConceptOf ind:HouseholdTypeScheme_v1 ;
  skos:notation "CPL" .

ind:household_nuclear a skos:Concept ;
  skos:prefLabel "Nuclear family"@en ;
  skos:inScheme ind:HouseholdTypeScheme_v1 ;
  skos:topConceptOf ind:HouseholdTypeScheme_v1 ;
  skos:notation "NUC" .

ind:household_extended a skos:Concept ;
  skos:prefLabel "Extended family"@en ;
  skos:inScheme ind:HouseholdTypeScheme_v1 ;
  skos:topConceptOf ind:HouseholdTypeScheme_v1 ;
  skos:notation "EXT" .

#################################################################
# Pregnancy Status Scheme
#################################################################

ind:PregnancyStatusScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Pregnancy status scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:pregnancy_pregnant , ind:pregnancy_not_pregnant ,
                     ind:pregnancy_postpartum .

ind:pregnancy_pregnant a skos:Concept ;
  skos:prefLabel "Pregnant"@en ;
  skos:inScheme ind:PregnancyStatusScheme_v1 ;
  skos:topConceptOf ind:PregnancyStatusScheme_v1 ;
  skos:notation "PRG" .

ind:pregnancy_not_pregnant a skos:Concept ;
  skos:prefLabel "Not pregnant"@en ;
  skos:inScheme ind:PregnancyStatusScheme_v1 ;
  skos:topConceptOf ind:PregnancyStatusScheme_v1 ;
  skos:notation "NPR" .

ind:pregnancy_postpartum a skos:Concept ;
  skos:prefLabel "Postpartum"@en ;
  skos:inScheme ind:PregnancyStatusScheme_v1 ;
  skos:topConceptOf ind:PregnancyStatusScheme_v1 ;
  skos:notation "PPT" .

#################################################################
# Vulnerability Category Scheme
#################################################################

ind:VulnerabilityCategoryScheme_v1 a skos:ConceptScheme ;
  skos:prefLabel "Vulnerability category scheme v1"@en ;
  ind:definitionVersion "1.0" ;
  skos:hasTopConcept ind:vulnerability_poor , ind:vulnerability_vulnerable ,
                     ind:vulnerability_not_vulnerable .

ind:vulnerability_poor a skos:Concept ;
  skos:prefLabel "Poor"@en ;
  skos:inScheme ind:VulnerabilityCategoryScheme_v1 ;
  skos:topConceptOf ind:VulnerabilityCategoryScheme_v1 ;
  skos:notation "POOR" .

ind:vulnerability_vulnerable a skos:Concept ;
  skos:prefLabel "Vulnerable"@en ;
  skos:inScheme ind:VulnerabilityCategoryScheme_v1 ;
  skos:topConceptOf ind:VulnerabilityCategoryScheme_v1 ;
  skos:notation "VUL" .

ind:vulnerability_not_vulnerable a skos:Concept ;
  skos:prefLabel "Not vulnerable"@en ;
  skos:inScheme ind:VulnerabilityCategoryScheme_v1 ;
  skos:topConceptOf ind:VulnerabilityCategoryScheme_v1 ;
  skos:notation "NVUL" .
"""
    return schemes

def main():
    print("Generating additional axes and schemes...")
    print()
    
    # Generate axes
    print("=" * 70)
    print("ADDITIONAL AXES")
    print("=" * 70)
    print()
    print("Append this to: ../indicatorOntology/IndicatorDSD/axis-definitions.ttl")
    print()
    print(generate_additional_axes())
    
    # Generate schemes
    print()
    print("=" * 70)
    print("ADDITIONAL SCHEMES")
    print("=" * 70)
    print()
    print("Append this to: ../indicatorOntology/IndicatorDSD/scheme-definitions.ttl")
    print()
    print(generate_additional_schemes())
    
    print()
    print("✅ Generation complete!")
    print()
    print("To apply:")
    print("1. Review the generated definitions above")
    print("2. Append axes to ../indicatorOntology/IndicatorDSD/axis-definitions.ttl")
    print("3. Append schemes to ../indicatorOntology/IndicatorDSD/scheme-definitions.ttl")

if __name__ == "__main__":
    main()

