"""
Counter API Implementation
"""
from flask import Flask, jsonify
from . import status    

app = Flask(__name__)

COUNTERS = {}

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if name == "reset":
        return jsonify({"error": "Counter name 'reset' is reserved"}), status.HTTP_400_BAD_REQUEST
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

def counter_exists(name):
  """Check if counter exists"""
  return name in COUNTERS

@app.route('/counters', methods=['GET'])
def list_all_counters():
    #lists all the counters
    return jsonify(COUNTERS), status.HTTP_200_OK

# Write code to make test pass - Brian
@app.route('/counters/<name>', methods=['GET'])
def read_counter(name):
    """Read a counter"""
    # Check if the counter exists in our dictionary
    if name in COUNTERS:
        return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK
    
    # If not found, return 404
    return counter_not_found(name)


# RETURN 404 for non-exixtent counter - Ernesto
@app.route('/counters/<name>', methods=['GET'])
def counter_not_found(name):
    # Counter doesnt exists, so generate a 404 error
    return jsonify({"error": f"Counter {name} doesn't exist"}), status.HTTP_404_NOT_FOUND

# Increment a counter - Donald Hunter
@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
    """Update/Increment a counter"""
    # Check if the counter exists
    # refactor: use existing helper function
    if not counter_exists(name):
        return counter_not_found(name)
    
    # Increment the counter
    COUNTERS[name] += 1

    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

# Reset all counters - Alvaro Avalos-Morales
@app.route('/counters/reset', methods=['POST'])
def reset_counters():
    """Reset all counters"""
    for key in COUNTERS:
        COUNTERS[key] = 0
    return jsonify({"message": "All counters have been reset"}), status.HTTP_200_OK