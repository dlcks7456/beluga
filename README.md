# Beluga

벨루가 에디터를 위한 설문 문항을 생성하고 관리하는 Python 라이브러리입니다.

## 설치

```bash
pip install beluga
```

## 사용법

```python
from beluga import Beluga

# Beluga 인스턴스 생성
beluga = Beluga()

# 단일 선택 객관식 문항 추가
beluga.sa(
    title="성별을 선택해주세요",
    options=["남성", "여성"],
    qid="Q1"
)

# 다중 선택 객관식 문항 추가
beluga.ma(
    title="관심 있는 분야를 선택해주세요 (복수 선택 가능)",
    options=["프로그래밍", "데이터 분석", "머신러닝", "웹 개발"],
    min=1,
    max=3,
    qid="Q2"
)

# 척도형 문항 추가
beluga.scale(
    title="이 제품에 대한 만족도를 평가해주세요",
    left="매우 불만족",
    right="매우 만족",
    score=5,
    qid="Q3"
)

# 텍스트 입력 문항 추가
beluga.text(
    title="추가 의견을 자유롭게 작성해주세요",
    qid="Q4"
)

# Excel 파일로 저장
beluga.to_excel("survey_questions.xlsx")
```

## 주요 기능

- **다양한 문항 유형 지원**: 단일 선택, 다중 선택, 척도형, 텍스트 입력, 숫자 입력 등
- **조건부 문항**: 특정 조건에 따라 문항 표시/숨김
- **파이핑**: 이전 응답을 다음 문항에 반영
- **Excel 내보내기**: 생성된 문항을 Excel 파일로 저장
- **Jupyter 노트북 지원**: IPython 환경에서 미리보기 기능

## 메서드

- `sa()`: 단일 선택 객관식
- `ma()`: 다중 선택 객관식
- `rank()`: 순위 선택
- `scale()`: 척도형
- `text()`: 텍스트 입력
- `number()`: 숫자 입력
- `date()`: 날짜 입력
- `phone()`: 전화번호 입력
- `address()`: 주소 입력
- `image()`: 이미지 업로드
- `dropdown()`: 드롭다운 선택
