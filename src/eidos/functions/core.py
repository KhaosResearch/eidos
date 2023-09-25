from eidos.logs import get_logger

logger = get_logger("eidos.functions")


def salute(who: str) -> str:
    """Salute someone.

    Args:
        who (str): The name of whom to salute. o7

    Returns:
        msg (str): The salutation message.
    """
    return f"Hello, {who}! o7"
