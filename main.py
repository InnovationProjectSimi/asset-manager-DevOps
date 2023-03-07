# Imports
from webApp import create_app
from flask import render_template, current_app

# Create the app
app = create_app()

# Create custom error handling pages
@app.errorhandler(404)
def page_not_found(e):
    current_app.logger.error("Error 404 not found")
    return render_template('404.html'), 404

@app.errorhandler(500)
def unexpected_error(e):
    current_app.logger.error("Error 500 unexpected error")
    return render_template('500.html'), 500

# App will only run if run from this file
if __name__ == "__main__":
    app.run(debug=True)