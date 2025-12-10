"""
PART 1: Understanding the ClinicalTrials.gov API
Run this on your local machine to see the actual data structure
"""

import requests
import json

print("="*80)
print("PART 1: EXPLORING THE API")
print("="*80)

# Test 1: Basic query from lab instructions
print("\n1. BASIC QUERY: Diabetes trials in France")
print("-" * 80)

response = requests.get(
    "https://clinicaltrials.gov/api/v2/studies",
    params={
        "format": "json",
        "pageSize": 2,
        "query.cond": "diabetes",
        "filter.overallStatus": "RECRUITING",
        "query.term": "PHASE2",
        "query.locn": "France",
        "fields": "NCTId,BriefTitle,Condition,Phase,BriefSummary,LocationFacility,LocationCity,LocationCountry,EligibilityCriteria"
    }
)

data = response.json()
print(f"Status: {response.status_code}")
print(f"Number of studies: {len(data.get('studies', []))}")

if data.get('studies'):
    print("\nFIRST STUDY:")
    print(json.dumps(data['studies'][0], indent=2)[:2000])  # First 2000 chars

# Test 2: Count trials
print("\n\n2. COUNTING: How many diabetes trials are recruiting?")
print("-" * 80)

response = requests.get(
    "https://clinicaltrials.gov/api/v2/studies",
    params={
        "format": "json",
        "pageSize": 1000,
        "query.cond": "diabetes",
        "filter.overallStatus": "RECRUITING",
        "fields": "NCTId"
    }
)

data = response.json()
print(f"Count: {len(data.get('studies', []))} trials")

# Test 3: Eligibility criteria
print("\n\n3. ELIGIBILITY: Ulcerative Colitis criteria")
print("-" * 80)

response = requests.get(
    "https://clinicaltrials.gov/api/v2/studies",
    params={
        "format": "json",
        "pageSize": 3,
        "query.cond": "ulcerative colitis",
        "filter.overallStatus": "RECRUITING",
        "fields": "NCTId,BriefTitle,EligibilityCriteria"
    }
)

data = response.json()
if data.get('studies'):
    study = data['studies'][0]
    protocol = study['protocolSection']
    title = protocol['identificationModule']['briefTitle']
    criteria = protocol['eligibilityModule']['eligibilityCriteria']
    
    print(f"Title: {title}")
    print(f"Criteria: {criteria[:500]}...")

# Test 4: Locations
print("\n\n4. LOCATIONS: Depression trials in Spain")
print("-" * 80)

response = requests.get(
    "https://clinicaltrials.gov/api/v2/studies",
    params={
        "format": "json",
        "pageSize": 10,
        "query.cond": "depression",
        "query.locn": "Spain",
        "fields": "NCTId,LocationFacility,LocationCity,LocationCountry"
    }
)

data = response.json()
print(f"Found: {len(data.get('studies', []))} trials")

if data.get('studies'):
    # Extract locations
    for study in data['studies'][:3]:
        protocol = study['protocolSection']
        if 'contactsLocationsModule' in protocol:
            locations = protocol['contactsLocationsModule'].get('locations', [])
            for loc in locations[:2]:
                print(f"  - {loc.get('facility', 'N/A')} in {loc.get('city', 'N/A')}")

