import logging

logger = logging.getLogger(__name__)

class ResponseParser:
    """
    Parses and formats responses from the Gemini API.
    """
    @staticmethod
    def summarize_text(text: str) -> str:

        # provides a human-friendly summary of the Gemini API's text response
        # this function performs basic cleaning for now
        # we can expand it to extract key entities or summarize longer descriptions.

        Args:
        # text (str): the raw text output from the Gemini API

        # str: cleeeaned humannn readable text description

        if not text:
            return "No description was generated."

        # basic cleaning... removing extra whitespace and newlines
        cleaned_text = ' '.join(text.strip().split())
        
        logger.info(f"Parsed Gemini response into: '{cleaned_text}'")
        return cleaned_text
