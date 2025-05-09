from website import run_app

app = run_app()
# This is the main entry point for the Flask application.

if __name__ == '__main__':
    app.run(debug=True)
