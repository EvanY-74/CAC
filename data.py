import json

DATA_PATH = 'data.json'

def get_data():
    try:
        with open(DATA_PATH, 'r') as file:
            return json.load(file)

    except FileNotFoundError:
        print(f'Error: The file "{DATA_PATH}" was not found.')
    except json.JSONDecodeError:
        print(f'Error: Could not decode JSON from "{DATA_PATH}". Check for valid JSON format.')


def get_all_candidates(attributes = None):
    """
    Get specified attributes of the candidates
    [name, party] -> [{name: "candidate 1", party: "party 1"}, {name: "candidate 2", party: "party 2"}]
    if attributes is None, every attribute will be returned
    """
    if attributes is None:
        return get_data()['candidates']

    if type(attributes) is not list:
        attributes = [attributes]

    return [{key: candidate[key] for key in attributes if key in candidate} for candidate in get_data()['candidates']]


def search_candidates(attribute, value, unique=True, case_sensitive=False):
    """Search candidates by attribute (most often id or name)"""

    candidates = get_data()['candidates']

    if not case_sensitive and type(value) is str:
        value = value.lower()

    results = []

    for candidate in candidates:
        fixed_case = candidate[attribute] if case_sensitive or type(candidate[attribute]) is not str else candidate[attribute].lower()
        if fixed_case == value:
            if unique:
                return candidate
            else:
                results.append(candidate)

    return results
