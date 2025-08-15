
# !important: This file is left over from replit and is not currently used.

from app import db
from datetime import datetime

class GovTerm(db.Model):
    """Model for storing government terminology definitions"""
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100), nullable=False, unique=True)
    definition = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Candidate(db.Model):
    """Model for storing candidate information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    office = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(50))
    district = db.Column(db.String(50))
    bio = db.Column(db.Text)
    website = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CandidateStance(db.Model):
    """Model for storing candidate stances on issues"""
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    issue = db.Column(db.String(100), nullable=False)
    stance = db.Column(db.Text, nullable=False)
    source_url = db.Column(db.String(200))
    
    candidate = db.relationship('Candidate', backref=db.backref('stances', lazy=True))

class Election(db.Model):
    """Model for storing election information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    election_date = db.Column(db.Date, nullable=False)
    election_type = db.Column(db.String(50), nullable=False)  # 'local', 'district', 'state'
    registration_deadline = db.Column(db.Date)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
