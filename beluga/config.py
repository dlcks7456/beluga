from dataclasses import dataclass, field
from typing import Dict


@dataclass
class BelugaConfig:
    etc_text: str = '기타(직접 입력)'
    default_rotation: bool = False
    dropdown_placeholder: str = '하나 선택...'
    total_text: str = '합계'
    display: bool = True
    change: bool = True  # 문항 추가/수정 시 change 기본값 (None일 때 이 값을 따름)
    text_atleast_error: Dict[str, str] = field(default_factory=lambda: {
        'empty': '첫번째 칸은 반드시 입력해주세요.',
        'outOfOrder': '입력 칸을 순서대로 사용해주세요.',
        'duplicate': '중복된 응답이 있습니다.',
    })

    text_all_error: Dict[str, str] = field(default_factory=lambda: {
        'empty': '빈 칸 없이 응답을 입력해 주세요.',
        'duplicate': '중복된 응답이 있습니다.',
    })

    num_error: Dict[str, str] = field(default_factory=lambda: {
        'empty': '모든 항목을 입력해주세요.',
        'range': '${min}~${max} 사이의 값을 입력해주세요.',
        'total': '총합이 ${total}이 되어야 합니다.',
    })

    dropdown_error: Dict[str, str] = field(default_factory=lambda: {
        'empty': '모든 항목을 응답해주세요.',
        'duplicate': '중복된 항목이 있습니다.',
    })