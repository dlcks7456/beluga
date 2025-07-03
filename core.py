from .config import BelugaConfig
from .errors import BelugaValidationError
import pandas as pd
from typing import Optional, Union
from .utils.html import *
from .utils.jsLogic import *
from .utils import *
from .belugaQuestion import *
from .previewQuestion import *


def create_question_df() :
    """설문 문항을 저장할 DataFrame을 생성합니다."""
    return pd.DataFrame(columns=[
            'QID',
            '문항번호',
            '문항유형',
            '최소',
            '최대',
            '보기 순서 로테이션',
            '보기 파이핑 적용',
            '질문',
            '보기',
            '조건',
            '실패시 이동',
            '응답후 로직',
            '단위',
        ])

class Beluga:
    """
    설문 문항을 생성하고 관리하는 클래스입니다.
    다양한 유형의 문항을 DataFrame 형태로 관리할 수 있습니다.
    """
    ALLOWED_RATING_SCORES = [3, 4, 5, 6, 7, 9, 10, 11]
    DEFAULT_ETC_TEXT = '기타(직접 입력)'

    def __init__(self, config: Optional[BelugaConfig] = None) -> None:
        self.config = config or BelugaConfig()
        self.df = create_question_df()
        self.etc_text = self.config.etc_text
        self.dropdown_placeholder = self.config.dropdown_placeholder
        self.total_text = self.config.total_text
        self._qid_cache = set()

    def set_etc_text(self, new_etc_text: str) -> None:
        self.etc_text = new_etc_text
        self.config.etc_text = new_etc_text

    def _validate_question(self, qid: Optional[str], title: str, min_val: Optional[int], max_val: Optional[int], change: bool = True) -> None:
        if not title:
            raise BelugaValidationError("제목은 필수입니다.")
        if min_val is not None and max_val is not None:
            if min_val > max_val:
                raise BelugaValidationError("최소 선택 개수는 최대 선택 개수보다 작아야 합니다.")
            if min_val < 0:
                raise BelugaValidationError("최소 선택 개수는 0 이상이어야 합니다.")
        if qid is not None and qid in self._qid_cache and not change:
            raise BelugaValidationError("QID가 중복됩니다. 내용을 변경하는 것이라면 change=True로 설정하세요.")

    # ... 이하 기존 Beluga 클래스의 나머지 메서드 ...