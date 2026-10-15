"""
Civic waste-reporting platform  --  Flask application entry point.

Routes:
  GET  /            Home: map of all reports + quick stats
  GET  /report      Submission form
  POST /report      Create a new report
  GET  /reports     List + filter reports (by category / status)
  GET  /api/reports JSON feed of reports (consumed by the map)

Run locally:
  pip install -r requirements.txt
  python app.py
  then open http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify

from models import db, Report, CATEGORIES, STATUSES
from ml.classifier import suggest_category


def create_app():
    """Application factory -- builds and configures the Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reports.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()  # create the SQLite tables on first run

    # ---- Routes -------------------------------------------------------

    @app.route("/")
    def index():
        """Home page: the map plus a few headline numbers."""
        total = Report.query.count()
        resolved = Report.query.filter_by(status="Resolved").count()
        return render_template("index.html", total=total, resolved=resolved)

    @app.route("/report", methods=["GET", "POST"])
    def report():
        """Show the submission form (GET) or save a new report (POST)."""
        if request.method == "POST":
            # The map writes the clicked coordinates into these hidden fields.
            new_report = Report(
                category=request.form["category"],
                description=request.form["description"].strip(),
                latitude=float(request.form["latitude"]),
                longitude=float(request.form["longitude"]),
                status="New",
            )
            db.session.add(new_report)
            db.session.commit()
            return redirect(url_for("reports"))

        # GET: ml.suggest_category is called here so the ML hook is live
        # in the flow today (it just returns None until a model exists).
        return render_template(
            "report.html",
            categories=CATEGORIES,
            suggested=suggest_category(""),
        )

    @app.route("/reports")
    def reports():
        """List reports, optionally filtered by category and/or status."""
        category = request.args.get("category", "")
        status = request.args.get("status", "")

        query = Report.query
        if category:
            query = query.filter_by(category=category)
        if status:
            query = query.filter_by(status=status)

        rows = query.order_by(Report.created_at.desc()).all()
        return render_template(
            "list.html",
            reports=rows,
            categories=CATEGORIES,
            statuses=STATUSES,
            active_category=category,
            active_status=status,
        )

    @app.route("/api/reports")
    def api_reports():
        """JSON feed the Leaflet map uses to drop a pin per report."""
        return jsonify([r.to_dict() for r in Report.query.all()])

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
