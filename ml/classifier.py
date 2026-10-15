"""
ML classification layer  --  DESIGNED, NOT YET IMPLEMENTED.

The platform is architected so that a resident's free-text description
can be used to SUGGEST the correct category automatically, instead of
asking them to pick from a dropdown every time.

Planned approach (for when this is built out):
  1. Collect labelled data: the (description -> category) pairs that
     accumulate naturally as residents submit reports.
  2. Vectorise the description text (e.g. TF-IDF or a small embedding).
  3. Train a simple multiclass classifier (e.g. logistic regression or
     a linear SVM from scikit-learn) to predict one of models.CATEGORIES.
  4. Load the trained model here and use it to pre-fill / suggest the
     category on the submission form, with the resident able to override.

Keeping this as a clearly-labelled stub is deliberate: the hook exists
in the code, so the ML layer can be dropped in without restructuring,
but nothing claims to classify until a real model is trained.
"""

# Confidence threshold a real model would need to clear before we
# trust its suggestion. Kept here so the design intent is explicit.
CONFIDENCE_THRESHOLD = 0.60


def suggest_category(description: str):
    """
    Return a suggested category for a free-text description.

    STUB: returns None until a trained model is wired in. The caller
    treats None as 'no suggestion -- resident picks manually', so the
    app works end to end today and gains ML suggestions later with no
    change to the calling code.
    """
    # TODO: load trained model and return model.predict(...) when
    # confidence >= CONFIDENCE_THRESHOLD, else None.
    return None
