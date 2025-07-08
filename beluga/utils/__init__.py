import re
from typing import List


def extract_qids(text: str) -> List[str]:
    """
    텍스트에서 #[QID] 패턴을 찾아 QID를 추출합니다.

    Args:
        text (str): QID 패턴을 찾을 텍스트

    Returns:
        List[str]: 발견된 QID들의 리스트

    Examples:
        >>> extract_qids("안녕하세요 #[AQ1] 문항입니다. #[BQ1]도 있습니다.")
        ['AQ1', 'BQ1']
        >>> extract_qids("#[Q1] #[Q2] #[Q3]")
        ['Q1', 'Q2', 'Q3']
    """
    pattern = r'#\[([^\]]+)\]'
    matches = re.findall(pattern, text)
    return matches
