import re
from app.constants import CODES
def clean_llm_response(raw_response: str) -> dict:

    # ==========================================
    # REMOVE <think> BLOCK
    # ==========================================
    think_match = re.search(
    r"<think>(.*?)</think>",
    raw_response,
    re.DOTALL
    )

    thinking = think_match.group(1).strip() \
        if think_match else ""

    cleaned = re.sub(
        r"<think>.*?</think>",
        "",
        raw_response,
        flags=re.DOTALL
    ).strip()

    # ==========================================
    # EXTRACT CODE
    # ==========================================

    code_match = re.search(
        r"\[CODE:(\d+)\]",
        cleaned
    )

    code = int(code_match.group(1)) \
        if code_match else 0

    # ==========================================
    # REMOVE CODE LINE
    # ==========================================

    cleaned = re.sub(
        r"\[CODE:\d+\]",
        "",
        cleaned
    ).strip()

    # ==========================================
    # EXTRACT TITLE + SOURCE
    # ==========================================

    title_match = re.search(
        r"\[title:\s*(.*?)\]&\[source:\s*(.*?)\]",
        cleaned,
        flags=re.IGNORECASE
    )

    title = title_match.group(1).strip() \
        if title_match else None

    section = title_match.group(2).strip() \
        if title_match else "General"

    # ==========================================
    # REMOVE TITLE LINE
    # ==========================================

    cleaned = re.sub(
        r"\[title:.*?\]&\[source:.*?\]",
        "",
        cleaned,
        flags=re.IGNORECASE
    ).strip()

    # ==========================================
    # EXTRACT SOURCE
    # ==========================================

    source_match_en = re.search(
        r"\[Source:\s*(.*?)\]",
        cleaned
    )

    source_match_ar = re.search(
        r"\[المصدر:\s*(.*?)\]",
        cleaned
    )

    source = None

    if source_match_en:
        source = source_match_en.group(1).strip()

    elif source_match_ar:
        source = source_match_ar.group(1).strip()

    # ==========================================
    # REMOVE SOURCE LINE
    # ==========================================

    cleaned = re.sub(
        r"\[Source:.*?\]",
        "",
        cleaned
    )

    cleaned = re.sub(
        r"\[المصدر:.*?\]",
        "",
        cleaned
    ).strip()

    # ==========================================
    # FINAL RESPONSE BODY
    # ==========================================

    response = cleaned.strip()

    return {

        "title":
        title,

        "section":
        section,

        "code":
        code,

        "code_title":
        CODES.get(
            code,
            "Unknown"
        ),

        "response":
        response,

        "source":
        source,

        "needs_support":
        code in [2000, 4000],
        "thinking":
         thinking
        
    }   
    