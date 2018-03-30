#!/usr/bin/env python

from ramsim import create_app, db

if __name__ == "__main__":
    app = create_app("development")

    with app.app_context():
        # Initialize Database
        db.create_all()
    
    app.run(host="0.0.0.0")
