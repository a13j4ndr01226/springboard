import os
import sys

# Add the DEBank directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import DEBank  # so it can be imported in test modules
