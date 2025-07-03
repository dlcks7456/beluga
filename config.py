from dataclasses import dataclass

@dataclass
class BelugaConfig:
    etc_text: str = '기타(직접 입력)'
    default_rotation: bool = False
    dropdown_placeholder: str = '하나 선택...'
    total_text: str = '합계'
    display: bool = True