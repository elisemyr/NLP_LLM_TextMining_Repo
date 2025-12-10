"""
PART 2: Clinical Trials Agent with Groq
=========================================

This agent uses:
- Groq API for LLM (fast and free)
- Function calling to query ClinicalTrials.gov
- Tool definitions for different query types

"""

import os
import json
import requests
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

#API queries

def count_trials(condition: str, status: str = "RECRUITING") -> dict:
    """
    Count clinical trials for a specific condition and status.
    
    Args:
        condition: Medical condition (e.g., "diabetes", "asthma")
        status: Trial status (RECRUITING, COMPLETED, TERMINATED, etc.)
    
    Returns:
        Dictionary with count and details
    """
    response = requests.get(
        "https://clinicaltrials.gov/api/v2/studies",
        params={
            "format": "json",
            "pageSize": 1000,
            "query.cond": condition,
            "filter.overallStatus": status,
            "fields": "NCTId,BriefTitle"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        studies = data.get('studies', [])
        
        return {
            "count": len(studies),
            "condition": condition,
            "status": status,
            "sample_titles": [
                s['protocolSection']['identificationModule']['briefTitle'] 
                for s in studies[:3]
            ]
        }
    else:
        return {"error": f"API error: {response.status_code}"}


def get_eligibility_criteria(condition: str, max_trials: int = 5) -> dict:
    """
    Get eligibility criteria for trials of a specific condition.
    
    Args:
        condition: Medical condition
        max_trials: Maximum number of trials to analyze
    
    Returns:
        Dictionary with eligibility criteria from multiple trials
    """
    response = requests.get(
        "https://clinicaltrials.gov/api/v2/studies",
        params={
            "format": "json",
            "pageSize": max_trials,
            "query.cond": condition,
            "filter.overallStatus": "RECRUITING",
            "fields": "NCTId,BriefTitle,EligibilityCriteria,Sex,MinimumAge,MaximumAge"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        studies = data.get('studies', [])
        
        criteria_list = []
        for study in studies:
            protocol = study['protocolSection']
            eligibility = protocol.get('eligibilityModule', {})
            
            criteria_list.append({
                "nct_id": protocol['identificationModule']['nctId'],
                "title": protocol['identificationModule']['briefTitle'],
                "criteria": eligibility.get('eligibilityCriteria', 'N/A'),
                "sex": eligibility.get('sex', 'N/A'),
                "age_range": f"{eligibility.get('minimumAge', 'N/A')} - {eligibility.get('maximumAge', 'N/A')}"
            })
        
        return {
            "condition": condition,
            "number_of_trials": len(criteria_list),
            "criteria": criteria_list
        }
    else:
        return {"error": f"API error: {response.status_code}"}


def get_trial_locations(condition: str, country: str = None) -> dict:
    """
    Get clinical trial locations for a condition, optionally filtered by country.
    
    Args:
        condition: Medical condition
        country: Country name (optional, e.g., "Spain", "France")
    
    Returns:
        Dictionary with unique facilities and their locations
    """
    params = {
        "format": "json",
        "pageSize": 50,
        "query.cond": condition,
        "fields": "NCTId,BriefTitle,LocationFacility,LocationCity,LocationCountry"
    }
    
    if country:
        params["query.locn"] = country
    
    response = requests.get(
        "https://clinicaltrials.gov/api/v2/studies",
        params=params
    )
    
    if response.status_code == 200:
        data = response.json()
        studies = data.get('studies', [])
        
        # Collect all unique facilities
        facilities = []
        for study in studies:
            protocol = study['protocolSection']
            if 'contactsLocationsModule' in protocol:
                locations = protocol['contactsLocationsModule'].get('locations', [])
                
                for loc in locations:
                    # Filter by country if specified
                    if country and loc.get('country', '').lower() != country.lower():
                        continue
                    
                    facility_info = {
                        "facility": loc.get('facility', 'N/A'),
                        "city": loc.get('city', 'N/A'),
                        "country": loc.get('country', 'N/A')
                    }
                    
                    # Avoid duplicates
                    if facility_info not in facilities:
                        facilities.append(facility_info)
        
        return {
            "condition": condition,
            "country": country or "all",
            "number_of_facilities": len(facilities),
            "facilities": facilities[:20]  # Return first 20
        }
    else:
        return {"error": f"API error: {response.status_code}"}


def get_trial_phases(condition: str, phase: str) -> dict:
    """
    Get trials for a specific condition and phase.
    
    Args:
        condition: Medical condition
        phase: Trial phase (e.g., "PHASE1", "PHASE2", "PHASE3", "PHASE4")
    
    Returns:
        Dictionary with trials in that phase
    """
    response = requests.get(
        "https://clinicaltrials.gov/api/v2/studies",
        params={
            "format": "json",
            "pageSize": 100,
            "query.cond": condition,
            "query.term": phase,
            "fields": "NCTId,BriefTitle,Phase,StartDate,CompletionDate"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        studies = data.get('studies', [])
        
        trials = []
        for study in studies:
            protocol = study['protocolSection']
            status_module = protocol.get('statusModule', {})
            
            trials.append({
                "nct_id": protocol['identificationModule']['nctId'],
                "title": protocol['identificationModule']['briefTitle'],
                "phase": protocol.get('designModule', {}).get('phases', ['N/A']),
                "start_date": status_module.get('startDateStruct', {}).get('date', 'N/A'),
                "completion_date": status_module.get('completionDateStruct', {}).get('date', 'N/A')
            })
        
        return {
            "condition": condition,
            "phase": phase,
            "count": len(trials),
            "trials": trials
        }
    else:
        return {"error": f"API error: {response.status_code}"}

#tool schema for groq

tools = [
    {
        "type": "function",
        "function": {
            "name": "count_trials",
            "description": "Count the number of clinical trials for a specific medical condition and status. Use this when users ask 'how many trials' or want to know trial counts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "condition": {
                        "type": "string",
                        "description": "The medical condition or disease (e.g., 'diabetes', 'asthma', 'ulcerative colitis')"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["RECRUITING", "COMPLETED", "TERMINATED", "ACTIVE_NOT_RECRUITING"],
                        "description": "The trial status",
                        "default": "RECRUITING"
                    }
                },
                "required": ["condition"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_eligibility_criteria",
            "description": "Get eligibility criteria for clinical trials of a specific condition. Use this when users ask about eligibility, inclusion/exclusion criteria, or who can participate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "condition": {
                        "type": "string",
                        "description": "The medical condition"
                    },
                    "max_trials": {
                        "type": "integer",
                        "description": "Maximum number of trials to analyze",
                        "default": 5
                    }
                },
                "required": ["condition"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_trial_locations",
            "description": "Get locations and facilities running clinical trials for a condition. Use this when users ask about trial sites, locations, or which hospitals/centers are conducting trials.",
            "parameters": {
                "type": "object",
                "properties": {
                    "condition": {
                        "type": "string",
                        "description": "The medical condition"
                    },
                    "country": {
                        "type": "string",
                        "description": "Optional country name to filter by (e.g., 'Spain', 'France', 'Germany')"
                    }
                },
                "required": ["condition"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_trial_phases",
            "description": "Get trials for a specific phase. Use this when users ask about Phase 1, 2, 3, or 4 trials, or trial duration by phase.",
            "parameters": {
                "type": "object",
                "properties": {
                    "condition": {
                        "type": "string",
                        "description": "The medical condition"
                    },
                    "phase": {
                        "type": "string",
                        "enum": ["PHASE1", "PHASE2", "PHASE3", "PHASE4"],
                        "description": "The trial phase"
                    }
                },
                "required": ["condition", "phase"]
            }
        }
    }
]

# Map function names to actual functions
available_functions = {
    "count_trials": count_trials,
    "get_eligibility_criteria": get_eligibility_criteria,
    "get_trial_locations": get_trial_locations,
    "get_trial_phases": get_trial_phases
}


#main agent function

def run_agent(user_question: str, model: str = "llama-3.3-70b-versatile") -> str:
    """
    Run the clinical trials agent with a user question.
    
    Args:
        user_question: Natural language question from user
        model: Groq model to use
    
    Returns:
        Agent's response
    """
    messages = [
        {
            "role": "system",
            "content": "You are a clinical trials research assistant. You help pharmaceutical researchers find information about clinical trials using the ClinicalTrials.gov database. Answer questions clearly and cite specific data when available."
        },
        {
            "role": "user",
            "content": user_question
        }
    ]
    
    # First call: Let the model decide which tools to use
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # If no tool calls, return the direct response
    if not tool_calls:
        return response_message.content
    
    # Execute the tool calls
    messages.append(response_message)
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"\n🔧 Calling tool: {function_name}")
        print(f"   Args: {function_args}")
        
        # Call the actual function
        function_response = available_functions[function_name](**function_args)
        
        # Add function response to messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": json.dumps(function_response)
        })
    
    # Second call: Let the model generate a final response using the tool results
    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=4096
    )
    
    return final_response.choices[0].message.content


#test the agent

if __name__ == "__main__":
    print("="*80)
    print("CLINICAL TRIALS AGENT")
    print("="*80)
    
    # Test questions from the lab
    test_questions = [
        "How many trials are currently recruiting for diabetes?",
        "What are typical eligibility criteria for Ulcerative Colitis trials?",
        "Which clinical sites in Spain have been used for depression trials?",
        "Show me Phase 3 Asthma trials",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"QUESTION {i}: {question}")
        print('='*80)
        
        try:
            answer = run_agent(question)
            print(f"\nANSWER:\n{answer}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n")
    
    # Interactive mode
    print("\n" + "="*80)
    print("INTERACTIVE MODE")
    print("="*80)
    
    while True:
        question = input("\nYour question: ")
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        try:
            answer = run_agent(question)
            print(f" Answer:\n{answer}\n")
        except Exception as e:
            print(f"❌ Error: {e}")