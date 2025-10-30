from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app

import data
# from models import GovTerm, Candidate, CandidateStance, Election
from api_services import get_polling_locations, get_representatives, get_elections
import logging
# from datetime import datetime, date

@app.route('/')
def index():
    """Home page with overview of features"""
    # Get next upcoming election
    # next_election = Election.query.filter(
    #     Election.election_date >= date.today(),
    #     Election.is_active == True
    # ).order_by(Election.election_date.asc()).first()
    # next_election = date.today() # Placeholder for actual election data retrieval
    next_election = False # Placeholder for actual election data retrieval
    
    return render_template('index.html', next_election=next_election)

@app.route('/quiz')
def quiz():
    """Entry quiz to determine voter eligibility and location"""
    return render_template('quiz.html')

@app.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    """Process quiz submission"""
    age = request.form.get('age', type=int)
    citizenship = request.form.get('citizenship')
    registered = request.form.get('registered')
    address = request.form.get('address')
    election_type = request.form.get('election_type')
    
    # Determine eligibility
    eligible = age >= 18 and citizenship == 'yes'
    
    if not eligible:
        flash('You must be 18 years old and a U.S. citizen to vote.', 'warning')
        return redirect(url_for('voting_info'))
    
    if registered == 'no':
        flash('You need to register to vote first. Check the voting information page for registration details.', 'info')
        return redirect(url_for('voting_info'))
    
    # Store user preferences in session for personalized experience
    from flask import session
    session['user_address'] = address
    session['election_type'] = election_type
    session['eligible'] = True
    
    flash('Great! You\'re eligible to vote. Explore the features below to get informed.', 'success')
    return redirect(url_for('candidates'))

@app.route('/candidates')
def candidates():
    """Display candidate information and stances"""

    candidates_list = data.get_all_candidates()

    # Key issues to display
    key_issues = [
        'Healthcare', 'Education', 'Economy', 'Environment', 
        'Infrastructure', 'Public Safety', 'Social Issues'
    ]
    
    # return render_template('candidates.html')
    return render_template('candidates.html', 
                          candidates=candidates_list, 
                          key_issues=key_issues)

@app.route('/voting-info')
def voting_info():
    """Comprehensive voting information page"""
    # NC specific voting requirements and deadlines
    voting_requirements = {
        'age': '18 years old by election day',
        'citizenship': 'U.S. citizen',
        'residence': 'North Carolina resident',
        'registration': 'Registered to vote 25 days before election',
        'id_required': 'Photo ID required (with exceptions for reasonable impediment)'
    }
    
    # Voting process steps
    voting_steps = [
        'Check your voter registration status',
        'Find your polling location',
        'Bring acceptable photo ID',
        'Review your ballot before casting',
        'Submit your ballot'
    ]
    
    # Important dates (these would come from Election model in real app)
    important_dates = [
        {'event': 'Voter Registration Deadline', 'date': '25 days before election'},
        {'event': 'Early Voting Period', 'date': '17 days before election'},
        {'event': 'Election Day', 'date': 'First Tuesday after first Monday in November'}
    ]
    
    return render_template('voting_info.html',
                          requirements=voting_requirements,
                          steps=voting_steps,
                          dates=important_dates)

@app.route('/polling-map')
def polling_map():
    """Interactive map showing polling locations"""
    return render_template('polling_map.html')

@app.route('/api/polling-locations')
def api_polling_locations(): # TODO: Credit Google Civics API
    """API endpoint to get polling locations based on address"""
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Address is required'}), 400
    
    try:
        locations = get_polling_locations(address)
        return jsonify(locations)
    except Exception as e:
        logging.error(f"Error fetching polling locations: {e}")
        return jsonify({'error': 'Unable to fetch polling locations'}), 500

GLOSSARY_TERMS = data.read_file('glossary')
@app.route('/glossary')
def glossary():
    """Government terms glossary"""
    
    categories = sorted(list(set(term['category'] for term in GLOSSARY_TERMS)))
    selected_category = request.args.get('category')
    
    if selected_category:
        terms = [term for term in GLOSSARY_TERMS if term['category'] == selected_category]
    else:
        terms = GLOSSARY_TERMS  # Add this line to show all terms when no category is selected
    
    return render_template('glossary.html', 
                          terms=terms,  # Change this from GLOSSARY_TERMS to terms
                          categories=categories,
                          selected_category=selected_category)

@app.route('/representatives')
def representatives():
    """Find local representatives based on address"""
    return render_template('representatives.html')