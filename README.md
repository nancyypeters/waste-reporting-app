# Civic Waste-Reporting Platform

A web app that lets residents report waste issues (fly-tipping, overflowing
bins, graffiti, etc.) and see every report plotted on an interactive map.
Built as a final-year Computer Science project.

## What it does

- **Report an issue** — click a location on the map, choose a category, add a description.
- **Map view** — every report shown as a pin, with category, description and status in a popup.
- **List & filter** — browse all reports and filter by category and status.
- **Geospatial data** — each report is stored with latitude/longitude and rendered on a Leaflet map.

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite (via SQLAlchemy ORM) |
| Frontend | HTML templates (Jinja2), vanilla JS |
| Mapping | Leaflet + OpenStreetMap tiles |

## Roadmap — ML classification layer (designed, upcoming)

The app is **architected to add an ML layer** that suggests a report's
category automatically from its free-text description. The hook already
exists in `ml/classifier.py` (`suggest_category()`), currently a stub that
returns no suggestion so the app works fully today. Planned approach:
collect the labelled `description → category` pairs that accumulate as
residents submit reports, vectorise the text (TF-IDF), and train a simple
multiclass classifier (scikit-learn) to pre-fill the category.

> This is deliberately a stub, not a claim: the design is in place, the
> model is future work.

## Run it locally

```bash
pip install -r requirements.txt
python app.py
# open http://127.0.0.1:5000
```

## Project structure

```
waste-reporting-app/
├── app.py            # Flask app + routes
├── models.py         # SQLAlchemy models (Report), categories, statuses
├── ml/
│   └── classifier.py # ML category-suggestion hook (stub, documented)
├── templates/        # Jinja2 HTML (base, index/map, report form, list)
├── static/
│   └── style.css
├── requirements.txt
└── .gitignore
```
