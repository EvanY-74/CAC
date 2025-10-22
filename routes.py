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

    #* Previous code to get and filter candidates (delete later if for sure not useful)
    # from flask import session
    # election_type = session.get('election_type', 'all')
    
    # Filter candidates based on election type if specified
    # if election_type == 'all':
    #     candidates_list = Candidate.query.all()
    # else:
    #     # This would need more sophisticated filtering based on user location
    #     candidates_list = Candidate.query.filter_by(office=election_type).all()
    
    #* Evan's code
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
def api_polling_locations():
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

@app.route('/glossary')
def glossary():
    """Government terms glossary"""
    # Get terms by category
    categories = db.session.query(GovTerm.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    selected_category = request.args.get('category', 'all')
    
    if selected_category == 'all':
        terms = GovTerm.query.order_by(GovTerm.term).all()
    else:
        terms = GovTerm.query.filter_by(category=selected_category).order_by(GovTerm.term).all()
    
    return render_template('glossary.html', 
                          terms=terms, 
                          categories=categories,
                          selected_category=selected_category)

@app.route('/representatives')
def representatives():
    """Find local representatives based on address"""
    return render_template('representatives.html')

@app.route('/api/representatives')
def api_representatives():
    """API endpoint to get representatives based on address"""
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Address is required'}), 400
    
    try:
        representatives = get_representatives(address)
        return jsonify(representatives)
    except Exception as e:
        logging.error(f"Error fetching representatives: {e}")
        return jsonify({'error': 'Unable to fetch representatives'}), 500

@app.route('/admin/populate-terms')
def populate_terms():
    """Admin route to populate government terms (for development)"""
    # Only populate if terms don't exist
    if GovTerm.query.count() > 0:
        return "Terms already populated"
    
    terms_data = [
        {"term": "House of Representatives", "definition": "The lower chamber of the U.S. Congress, with members serving two-year terms representing districts.", "category": "Legislative"},
        {"term": "Senate", "definition": "The upper chamber of the U.S. Congress, with two senators from each state serving six-year terms.", "category": "Legislative"},
        {"term": "Bill", "definition": "A proposed law presented to a legislature for consideration.", "category": "Legislative Process"},
        {"term": "Amendment", "definition": "A change or addition to a constitution, law, or bill.", "category": "Legislative Process"},
        {"term": "Filibuster", "definition": "A tactic used in the Senate to delay or prevent a vote on a bill by extending debate.", "category": "Legislative Process"},
        {"term": "Gerrymandering", "definition": "The practice of drawing electoral district boundaries to favor one party or group.", "category": "Elections"},
        {"term": "Constituent", "definition": "A voting member of a community or organization with the power to elect representatives.", "category": "Representation"},
        {"term": "Caucus", "definition": "A meeting of supporters or members of a specific political party or movement.", "category": "Political Process"},
        {"term": "Primary Election", "definition": "An election where voters choose candidates to represent their party in the general election.", "category": "Elections"},
        {"term": "General Election", "definition": "The main election where voters choose between candidates from different parties.", "category": "Elections"}
    ]
    
    for term_data in terms_data:
        term = GovTerm(**term_data)
        db.session.add(term)
    
    db.session.commit()
    return f"Populated {len(terms_data)} terms"

# @app.context_processor
# def inject_election_countdown():
#     """Inject election countdown into all templates"""
#     next_election = Election.query.filter(
#         Election.election_date >= date.today(),
#         Election.is_active == True
#     ).order_by(Election.election_date.asc()).first()
    
#     days_until_election = None
#     if next_election:
#         days_until_election = (next_election.election_date - date.today()).days
    
#     return dict(next_election=next_election, days_until_election=days_until_election)
