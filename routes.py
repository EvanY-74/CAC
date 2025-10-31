from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import app

import data
from api_services import get_polling_locations, get_representatives, get_elections
import logging

@app.route('/')
def index():
    """Home page with overview of features"""
    
    return render_template('index.html')

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
    # Store user quiz answers in session and mark quiz as completed.
    # NOTE: allow submission regardless of answers (user requested this behavior).
    session['quiz_answers'] = {
        'age': age,
        'citizenship': citizenship,
        'registered': registered,
        'address': address,
        'election_type': election_type,
    }
    session['quiz_completed'] = True

    # Provide friendly messaging but don't block navigation.
    flash('Thanks — your quiz responses have been saved. You can now view voting information.', 'success')
    return redirect(url_for('voting_info'))

@app.route('/candidates')
def candidates():
    """Display candidate information and stances"""

    candidates_list = data.get_all_candidates()

    # Key issues to display
    key_issues = [
        'Healthcare', 'Education', 'Economy', 'Environment', 
        'Infrastructure', 'Public Safety', 'Social Issues'
    ]
    
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
    
    # If user hasn't completed the quiz yet, redirect them to the quiz first.
    if not session.get('quiz_completed'):
        # Preserve original target so after quiz we land here.
        session['post_quiz_target'] = url_for('voting_info')
        return redirect(url_for('quiz'))

    # Build a dict of whether each requirement is met based on quiz answers.
    answers = session.get('quiz_answers', {})
    requirement_status = {
        'age': (answers.get('age') is not None and answers.get('age') >= 18),
        'citizenship': (answers.get('citizenship') == 'yes'),
        'residence': bool(answers.get('address')),
        'registration': (answers.get('registered') == 'yes'),
        # 'id_required' isn't asked on the quiz; assume requirement is met (or keep True)
        'id_required': True,
    }

    return render_template('voting_info.html',
                          requirements=voting_requirements,
                          requirement_status=requirement_status,
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