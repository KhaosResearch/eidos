import transformers

from eidos.logs import get_logger

logger = get_logger()

INTENT_CLASSIFICATION_MODEL = None


def load_model() -> transformers.Pipeline:
    """Load the zero-shot classification model from HuggingFace if it is not loaded."""
    global INTENT_CLASSIFICATION_MODEL
    if INTENT_CLASSIFICATION_MODEL is None:
        INTENT_CLASSIFICATION_MODEL = transformers.pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )

    return INTENT_CLASSIFICATION_MODEL


def predict_intent(
    text: str,
    candidate_labels: list[str] = [
        "QuestionRequiresAnswer",
        "ConversationalInformation",
    ],
) -> tuple[str, float]:
    """Predict the intent of the user input.

    Args:
        text (str): User input.
        candidate_labels (list[str], optional): Candidate labels for the intent.
            Defaults to ["QuestionRequiresAnswer", "ConversationalInformation"].

    Returns:
        str, float: Predicted intent from candidate_labels and the associated score.
    """
    # Classify user input
    classifier = load_model()
    intent_scores = classifier(text, candidate_labels)

    # Get the index of the label with the highest score
    max_score = max(intent_scores["scores"])
    max_score_index = intent_scores["scores"].index(max_score)
    label = intent_scores["labels"][max_score_index]

    logger.info(f"User intent is {label} with a score of {max_score}")

    return label, max_score
