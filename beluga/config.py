from dataclasses import dataclass

@dataclass
class BelugaConfig:
    etc_text: str = '기타(직접 입력)'
    default_rotation: bool = False
    dropdown_placeholder: str = '하나 선택...'
    total_text: str = '합계'
    display: bool = True
    change: bool = True  # 문항 추가/수정 시 change 기본값 (None일 때 이 값을 따름)