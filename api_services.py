import os
import requests
import logging
from typing import Dict, List, Any

# API Keys from environment variables
GOOGLE_CIVICS_API_KEY = os.getenv('CIVICS_API_KEY', 'your_google_civics_api_key')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'your_google_maps_api_key')

def get_polling_locations(address: str) -> Dict[str, Any]:
    """
    Get polling locations using Google Civics Information API
    """
    try:
        url = "https://www.googleapis.com/civicinfo/v2/voterinfo"
        params = {
            'key': GOOGLE_CIVICS_API_KEY,
            'address': address,
            'electionId': '2000'  # Use latest election ID
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract polling location information
        polling_locations = []
        
        if 'pollingLocations' in data:
            for location in data['pollingLocations']:
                location_info = {
                    'name': location.get('address', {}).get('locationName', 'Polling Location'),
                    'address': format_address(location.get('address', {})),
                    'hours': location.get('pollingHours', 'Check local listings'),
                    'notes': location.get('notes', '')
                }
                polling_locations.append(location_info)
        
        # Also check for early vote sites
        early_vote_sites = []
        if 'earlyVoteSites' in data:
            for site in data['earlyVoteSites']:
                site_info = {
                    'name': site.get('address', {}).get('locationName', 'Early Voting Site'),
                    'address': format_address(site.get('address', {})),
                    'hours': site.get('pollingHours', 'Check local listings'),
                    'notes': site.get('notes', ''),
                    'type': 'early_voting'
                }
                early_vote_sites.append(site_info)
        
        return {
            'polling_locations': polling_locations,
            'early_vote_sites': early_vote_sites,
            'election': data.get('election', {}),
            'success': True
        }
        
    except requests.RequestException as e:
        logging.error(f"Error fetching polling locations: {e}")
        return {
            'error': 'Unable to fetch polling locations. Please try again later.',
            'success': False
        }
    except Exception as e:
        logging.error(f"Unexpected error in get_polling_locations: {e}")
        return {
            'error': 'An unexpected error occurred.',
            'success': False
        }

def get_representatives(address: str) -> Dict[str, Any]:
    """
    Get representatives information using Google Civics Information API
    """
    try:
        url = "https://www.googleapis.com/civicinfo/v2/representatives"
        params = {
            'key': GOOGLE_CIVICS_API_KEY,
            'address': address,
            'levels': 'country,administrativeArea1,administrativeArea2,locality',
            'roles': 'legislatorUpperBody,legislatorLowerBody,executiveHead'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        representatives = []
        
        if 'officials' in data and 'offices' in data:
            offices = data['offices']
            officials = data['officials']
            
            for office in offices:
                office_name = office.get('name', '')
                official_indices = office.get('officialIndices', [])
                
                for index in official_indices:
                    if index < len(officials):
                        official = officials[index]
                        
                        rep_info = {
                            'name': official.get('name', ''),
                            'office': office_name,
                            'party': official.get('party', ''),
                            'phones': official.get('phones', []),
                            'emails': official.get('emails', []),
                            'urls': official.get('urls', []),
                            'photo_url': official.get('photoUrl', ''),
                            'address': format_address(official.get('address', [{}])[0] if official.get('address') else {})
                        }
                        representatives.append(rep_info)
        
        return {
            'representatives': representatives,
            'success': True
        }
        
    except requests.RequestException as e:
        logging.error(f"Error fetching representatives: {e}")
        return {
            'error': 'Unable to fetch representatives. Please try again later.',
            'success': False
        }
    except Exception as e:
        logging.error(f"Unexpected error in get_representatives: {e}")
        return {
            'error': 'An unexpected error occurred.',
            'success': False
        }

def get_elections() -> Dict[str, Any]:
    """
    Get upcoming elections using Google Civics Information API
    """
    try:
        url = "https://www.googleapis.com/civicinfo/v2/elections"
        params = {
            'key': GOOGLE_CIVICS_API_KEY
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        elections = []
        if 'elections' in data:
            for election in data['elections']:
                election_info = {
                    'id': election.get('id'),
                    'name': election.get('name', ''),
                    'election_day': election.get('electionDay', ''),
                    'description': election.get('description', '')
                }
                elections.append(election_info)
        
        return {
            'elections': elections,
            'success': True
        }
        
    except requests.RequestException as e:
        logging.error(f"Error fetching elections: {e}")
        return {
            'error': 'Unable to fetch elections. Please try again later.',
            'success': False
        }
    except Exception as e:
        logging.error(f"Unexpected error in get_elections: {e}")
        return {
            'error': 'An unexpected error occurred.',
            'success': False
        }

def format_address(address_obj: Dict[str, str]) -> str:
    """
    Format address object into a readable string
    """
    if not address_obj:
        return ''
    
    parts = []
    
    if 'line1' in address_obj:
        parts.append(address_obj['line1'])
    if 'line2' in address_obj:
        parts.append(address_obj['line2'])
    if 'line3' in address_obj:
        parts.append(address_obj['line3'])
    
    city_state_zip = []
    if 'city' in address_obj:
        city_state_zip.append(address_obj['city'])
    if 'state' in address_obj:
        city_state_zip.append(address_obj['state'])
    if 'zip' in address_obj:
        city_state_zip.append(address_obj['zip'])
    
    if city_state_zip:
        parts.append(', '.join(city_state_zip))
    
    return ', '.join(parts)
