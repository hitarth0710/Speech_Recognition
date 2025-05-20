import os
import sys
from app import create_app

try:
    # Get configuration from environment variable or use default
    config_name = os.environ.get('FLASK_CONFIG') or 'default'
    app = create_app(config_name)

    if __name__ == '__main__':
        app.run(debug=True)
except Exception as e:
    print(f"Error starting application: {str(e)}", file=sys.stderr)
    # Add more detailed error information for debugging
    import traceback
    traceback.print_exc()
    sys.exit(1)