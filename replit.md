# MyNCRep - North Carolina Voter Guide

## Overview

MyNCRep is a comprehensive web application designed to help North Carolina residents engage with the democratic process. The application provides voter eligibility assessment, candidate information, polling location finding, representative lookup, and educational resources about government terminology. It serves as a one-stop platform for civic engagement and voting preparation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses a server-side rendered Flask web application with Bootstrap for responsive UI design. The frontend follows a traditional MVC pattern with Jinja2 templates for dynamic content rendering. JavaScript is used for interactive features like maps integration and form validation.

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM for database operations
- **Database**: SQL-based storage using SQLAlchemy with environment-configurable database URL
- **API Integration**: External service integration for Google Civics Information API and Google Maps API
- **Session Management**: Flask sessions for user state management

### Data Storage Solutions
The application uses SQLAlchemy ORM with a relational database approach. Key models include:
- Government terminology definitions
- Candidate information and stances
- Election data
- Relationships between candidates and their issue positions

## Key Components

### 1. Voter Eligibility System
- Interactive quiz to assess voting eligibility
- Session-based user state management
- Personalized experience based on user location and preferences

### 2. Candidate Information System
- Comprehensive candidate database with filtering capabilities
- Issue stance tracking with source attribution
- Office and district-based organization

### 3. Polling Location Finder
- Google Maps integration for visual location display
- Address-based polling location lookup
- Early voting site information

### 4. Representative Lookup
- Address-based representative identification
- Integration with Google Civics Information API
- Multi-level government representation (local, state, federal)

### 5. Educational Resources
- Government terminology glossary
- Searchable and categorized definitions
- Voting process information and requirements

## Data Flow

1. **User Entry**: Users begin with an eligibility quiz that determines their voting status
2. **Personalization**: User preferences and location are stored in Flask sessions
3. **Information Retrieval**: Based on user location, relevant candidates, representatives, and polling locations are fetched
4. **External API Integration**: Google APIs provide real-time polling locations and representative data
5. **Database Queries**: Local database provides candidate stances, election information, and terminology definitions

## External Dependencies

### APIs
- **Google Civics Information API**: For polling locations, election data, and representative information
- **Google Maps API**: For interactive map display and geocoding services

### Frontend Libraries
- **Bootstrap**: Responsive UI framework with dark theme support
- **Font Awesome**: Icon library for consistent visual elements
- **Google Maps JavaScript API**: Interactive map functionality

### Backend Dependencies
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Requests**: HTTP client for API integration
- **ProxyFix**: WSGI middleware for deployment

## Deployment Strategy

The application is configured for cloud deployment with:
- Environment variable configuration for database URLs and API keys
- WSGI proxy support for reverse proxy deployments
- Session secret management through environment variables
- Database connection pooling with automatic reconnection
- Logging configuration for debugging and monitoring

The application structure suggests deployment on platforms like Replit, Heroku, or similar PaaS providers, with PostgreSQL as the likely production database choice despite using SQLAlchemy's database-agnostic approach.

### Configuration Management
- Database URL configured via `DATABASE_URL` environment variable
- API keys managed through environment variables
- Session secrets externalized for security
- Debug mode controllable for different environments