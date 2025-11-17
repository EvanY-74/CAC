# MyNCRep

MyNCRep is a civic-information tool built to help North Carolina voters cut through noise and get the facts that matter. It shows where to vote, what you need, and what each candidate actually stands for. No spins. No party narratives. Just information you can use.

This project began as an entry for the **Congressional App Challenge**, created by students who realized most new voters don’t lack opinions; they lack context. MyNCRep was our answer to that gap.

## What It Does

- Shows nearby polling places using optional location access  
- Explains how to register and vote, with reminders for key deadlines  
- Displays candidate profiles with issue positions, biographies, and voting histories  
- Pulls data from trusted sources like Vote Smart and NCSBE  
- Provides short guides on government processes for new voters  
- Tailors information based on a simple onboarding quiz  

The goal is simple: help people understand who represents them and what those people stand for.

## Technical Overview

- Google Civics API for polling and representative data  
- Leaflet + OpenStreetMap for interactive mapping  
- Python backend managed with Poetry  
- Modular architecture so contributors can easily extend functionality  

## Known Challenges

During development, we ran into several issues that shaped how the app works:

- Missing NC polling data in VIP, requiring fallback logic  
- Choosing between API-driven data flow and local storage  
- Designing location features without compromising user safety  
- Ensuring civic data is presented in a neutral, verifiable way  

## Roadmap: Version 2.0

- Expand beyond North Carolina  
- Real-time updates when bills are introduced or candidates release statements  
- Gamified civics learning modules  
- AI-powered summaries of bills and issue positions  
- Partnerships with election boards for verified polling data  
- Cleaner UI and broader device support  

## Setup

### 1. Clone the Repository
Clone the repo using your preferred method.

### 2. Install Poetry
```
powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
Add this directory to your PATH:
```
shell
```
Copy code
```
%USERPROFILE%\AppData\Roaming\Python\Scripts
```
Verify installation:
```
powershell
Copy code
poetry --version
```
3. Create a Virtual Environment
```
powershell
```
Copy code
```
python -m venv venv
```
Activate it:
```
powershell
```
Copy code
```
venv\Scripts\activate
```
If script execution is blocked:
```
powershell
```
Copy code
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```
4. Install Dependencies
```
powershell
```
Copy code
```
poetry install
```
6. Run the App
```
powershell
```
Copy code
```
python main.py
```
The server will automatically restart when changes are made.

Development Notes
To add new packages:
```
powershell
poetry add package_name
```
Other contributors should run:
```
powershell
poetry install
```
to stay synced with the environment.

Authors
Built by Aryan Vyahalkar, Evan Yango, Heerah Shah, & Arav Vyahalkar
Students committed to making civic participation clearer, simpler, and easier to start.
If you want to contribute, feel free to open an issue or pull request.
