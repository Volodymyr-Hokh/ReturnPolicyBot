import re

from bs4 import BeautifulSoup
import markdown2


def normalize_text(text: str) -> str:
    html_text = markdown2.markdown(text)
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text()
    cleaned_text = re.sub(r"【\d+:\d+†\w+】", "", text)
    return cleaned_text
