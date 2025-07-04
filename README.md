# Beluga 클래스 메서드 사용 가이드

## 목차

1. [설치 및 기본 사용법](#설치-및-기본-사용법)
2. [기본 설정](#기본-설정)
3. [문항 유형별 메서드](#문항-유형별-메서드)
4. [데이터 관리 메서드](#데이터-관리-메서드)
5. [공통 파라미터](#공통-파라미터)
6. [고급 기능](#고급-기능)

## 설치 및 기본 사용법

### 설치

```bash
pip install git+https://github.com/dlcks7456/beluga
```

### 기본 사용법

```python
from beluga import Beluga, BelugaConfig

# 기본 인스턴스 생성
beluga = Beluga()

# 설정과 함께 인스턴스 생성
config = BelugaConfig(etc_text="기타", default_rotation=True)
beluga = Beluga(config)
```

## 기본 설정

### BelugaConfig 클래스

```python
config = BelugaConfig(
    etc_text='기타(직접 입력)',        # 기타 선택지 텍스트
    default_rotation=False,           # 기본 로테이션 설정
    dropdown_placeholder='하나 선택...', # 드롭다운 플레이스홀더
    total_text='합계',                # 합계 텍스트
    display=True,                     # 표시 여부
    change=True                       # 기본 변경 허용 여부
)
```

### 기타 텍스트 변경

```python
beluga.set_etc_text("사용자 정의 기타 텍스트")
```

## 문항 유형별 메서드

### 1. sa() - 단일 선택 객관식

단일 선택 객관식 문항을 생성합니다.

**파라미터:**

- `title` (str, 필수): 질문 제목
- `qid` (str, 선택): 질문 ID (None시 자동 생성)
- `options` (dict|list, 선택): 선택지 목록
- `scale` (bool, 선택): 척도형 문항 여부 (기본: False)
- `etc` (bool, 선택): 기타 선택지 포함 여부 (기본: False)
- `etc_text` (str, 선택): 기타 선택지 텍스트
- `na` (str, 선택): 무응답 옵션
- `cond` (str|list, 선택): 조건문
- `piping` (str|int|BelugaQuestion, 선택): 파이핑 설정
- `selected_piping` (bool, 선택): 선택된 파이핑 (기본: True)
- `rotation` (bool, 선택): 보기 순서 로테이션 여부
- `fail` (str, 선택): 조건 실패시 이동할 위치
- `post_logic` (str, 선택): 응답 후 로직
- `change` (bool, 선택): 기존 QID 변경 여부
- `inplace` (bool, 선택): 현재 인스턴스에 추가할지 여부 (기본: True)

**사용 예시:**

```python
# 기본 단일 선택
beluga.sa(
    title="성별을 선택해주세요",
    options=["남성", "여성"],
    qid="Q1"
)

# 기타 선택지 포함
beluga.sa(
    title="선호하는 색상을 선택해주세요",
    options=["빨강", "파랑", "노랑"],
    etc=True,
    qid="Q2"
)

# 딕셔너리 형태 선택지
beluga.sa(
    title="연령대를 선택해주세요",
    options={1: "10대", 2: "20대", 3: "30대", 4: "40대 이상"},
    qid="Q3"
)

# 척도형 문항
beluga.sa(
    title="만족도를 평가해주세요",
    options=["매우 불만족", "불만족", "보통", "만족", "매우 만족"],
    scale=True,
    qid="Q4"
)

# 조건부 문항
beluga.sa(
    title="추가 질문입니다",
    options=["예", "아니오"],
    cond="Q1A1",  # Q1이 1번 선택시에만 표시
    qid="Q5"
)
```

### 2. ma() - 다중 선택 객관식

다중 선택 객관식 문항을 생성합니다.

**파라미터:**

- `title` (str, 필수): 질문 제목
- `qid` (str, 선택): 질문 ID
- `options` (dict|list, 선택): 선택지 목록
- `etc` (bool, 선택): 기타 선택지 포함 여부
- `etc_text` (str, 선택): 기타 선택지 텍스트
- `na` (str, 선택): 무응답 옵션
- `cond` (str|list, 선택): 조건문
- `min` (int, 선택): 최소 선택 개수 (기본: 1)
- `max` (int, 선택): 최대 선택 개수 (기본: 선택지 개수)
- `piping` (str|int|BelugaQuestion, 선택): 파이핑 설정
- `selected_piping` (bool, 선택): 선택된 파이핑
- `rotation` (bool, 선택): 보기 순서 로테이션 여부
- `fail` (str, 선택): 조건 실패시 이동할 위치
- `post_logic` (str, 선택): 응답 후 로직
- `change` (bool, 선택): 기존 QID 변경 여부
- `inplace` (bool, 선택): 현재 인스턴스에 추가할지 여부

**사용 예시:**

```python
# 기본 다중 선택
beluga.ma(
    title="관심 있는 분야를 선택해주세요 (복수 선택 가능)",
    options=["프로그래밍", "데이터 분석", "머신러닝", "웹 개발"],
    min=1,
    max=3,
    qid="Q6"
)

# 기타 선택지 포함
beluga.ma(
    title="사용하는 프로그래밍 언어를 모두 선택해주세요",
    options=["Python", "Java", "JavaScript", "C++"],
    etc=True,
    qid="Q7"
)

# 로테이션 적용
beluga.ma(
    title="선호하는 브랜드를 선택해주세요",
    options=["브랜드A", "브랜드B", "브랜드C", "브랜드D"],
    rotation=True,
    qid="Q8"
)
```

### 3. rank() - 순위 선택

순위 선택 문항을 생성합니다.

**파라미터:** (ma()와 동일)

**사용 예시:**

```python
# 순위 선택
beluga.rank(
    title="다음 중 중요한 순서대로 최대 3개를 선택해주세요",
    options=["가격", "품질", "디자인", "브랜드", "기능"],
    min=1,
    max=3,
    qid="Q9"
)
```

### 4. scale() - 척도형 문항

평가형(척도형) 문항을 생성합니다.

**파라미터:**

- `title` (str, 필수): 질문 제목
- `qid` (str, 선택): 질문 ID
- `left` (str, 선택): 왼쪽 라벨 (최저점)
- `center` (str, 선택): 중간 라벨
- `right` (str, 선택): 오른쪽 라벨 (최고점)
- `score` (int, 선택): 척도 점수 (3,4,5,6,7,9,10,11 중 선택, 기본: 5)
- `cond` (str|list, 선택): 조건문
- `fail` (str, 선택): 조건 실패시 이동할 위치
- `post_logic` (str, 선택): 응답 후 로직
- `change` (bool, 선택): 기존 QID 변경 여부
- `inplace` (bool, 선택): 현재 인스턴스에 추가할지 여부

**사용 예시:**

```python
# 5점 척도
beluga.scale(
    title="이 제품에 대한 만족도를 평가해주세요",
    left="매우 불만족",
    right="매우 만족",
    score=5,
    qid="Q10"
)

# 7점 척도 (중간 라벨 포함)
beluga.scale(
    title="서비스 품질을 평가해주세요",
    left="매우 나쁨",
    center="보통",
    right="매우 좋음",
    score=7,
    qid="Q11"
)

# 10점 척도
beluga.scale(
    title="추천 의향을 평가해주세요",
    left="전혀 추천하지 않음",
    right="매우 추천함",
    score=10,
    qid="Q12"
)
```

### 5. text() - 텍스트 입력

주관식 문자 입력 문항을 생성합니다.

**파라미터:**

- `title` (str, 필수): 질문 제목
- `qid` (str, 선택): 질문 ID
- `cond` (str|list, 선택): 조건문
- `fail` (str, 선택): 조건 실패시 이동할 위치
- `post_logic` (str, 선택): 응답 후 로직
- `change` (bool, 선택): 기존 QID 변경 여부
- `multi` (int|list|dict, 선택): 다중 입력 설정
- `multi_atleast` (bool, 선택): 다중 입력시 최소 하나 이상 입력 필수 (기본: False)
- `multi_post` (str, 선택): 다중 입력 후 텍스트
- `multi_width` (str, 선택): 입력 필드 너비 (기본: '200px')
- `inplace` (bool, 선택): 현재 인스턴스에 추가할지 여부

**사용 예시:**

```python
# 단일 텍스트 입력
beluga.text(
    title="추가 의견을 자유롭게 작성해주세요",
    qid="Q13"
)

# 다중 텍스트 입력 (개수 지정)
beluga.text(
    title="좋아하는 음식 3가지를 작성해주세요",
    multi=3,
    multi_atleast=True,
    qid="Q14"
)

# 다중 텍스트 입력 (라벨 지정)
beluga.text(
    title="개인 정보를 입력해주세요",
    multi=["이름", "나이", "직업"],
    qid="Q15"
)

# 다중 텍스트 입력 (딕셔너리 형태)
beluga.text(
    title="연락처 정보를 입력해주세요",
    multi={1: "이메일", 2: "전화번호", 3: "주소"},
    multi_width="300px",
    qid="Q16"
)
```

### 6. number() - 숫자 입력

숫자 입력 문항을 생성합니다.

**파라미터:**

- `title` (str, 필수): 질문 제목
- `qid` (str, 선택): 질문 ID
- `cond` (str|list, 선택): 조건문
- `min` (int, 선택): 최소값
- `max` (int, 선택): 최대값
- `total` (int, 선택): 총합 제한
- `fail` (str, 선택): 조건 실패시 이동할 위치
- `post_logic` (str, 선택): 응답 후 로직
- `post_text` (str, 선택): 입력 후 텍스트
- `change` (bool, 선택): 기존 QID 변경 여부
- `multi` (int|list|dict, 선택): 다중 입력 설정
- `multi_post` (str, 선택): 다중 입력 후 텍스트
- `multi_width` (str, 선택): 입력 필드 너비 (기본: '70px')
- `inplace` (bool, 선택): 현재 인스턴스에 추가할지 여부

**사용 예시:**

```python
# 단일 숫자 입력
beluga.number(
    title="나이를 입력해주세요",
    min=0,
    max=100,
    post_text="세",
    qid="Q17"
)

# 다중 숫자 입력 (총합 제한)
beluga.number(
    title="각 항목의 중요도를 100점 만점으로 배분해주세요",
    multi=["가격", "품질", "디자인"],
    total=100,
    min=0,
    max=100,
    multi_post="점",
    qid="Q18"
)
```

### 7. date() - 날짜 입력

날짜 입력 문항을 생성합니다.

**파라미터:**

- `title` (str, 필수): 질문 제목
- `qid` (str, 선택): 질문 ID
- `cond` (str|list, 선택): 조건문
- `fail` (str, 선택): 조건 실패시 이동할 위치
- `post_logic` (str, 선택): 응답 후 로직
- `change` (bool, 선택): 기존 QID 변경 여부
- `inplace` (bool, 선택): 현재 인스턴스에 추가할지 여부

**사용 예시:**

```python
beluga.date(
    title="생년월일을 입력해주세요",
    qid="Q20"
)
```

### 8. phone() - 전화번호 입력

전화번호 입력 문항을 생성합니다.

**파라미터:** (date()와 동일)

**사용 예시:**

```python
beluga.phone(
    title="연락처를 입력해주세요",
    qid="Q21"
)
```

### 9. address() - 주소 입력

주소 입력 문항을 생성합니다.

**파라미터:** (date()와 동일)

**사용 예시:**

```python
beluga.address(
    title="주소를 입력해주세요",
    qid="Q22"
)
```

### 10. image() - 이미지 업로드

이미지 업로드 문항을 생성합니다.

**파라미터:** (date()와 동일)

**사용 예시:**

```python
beluga.image(
    title="증빙 서류를 업로드해주세요",
    qid="Q23"
)
```

### 11. dropdown() - 드롭다운 선택

드롭다운 선택 문항을 생성합니다.

**파라미터:**

- `title` (str, 필수): 질문 제목
- `qid` (str, 선택): 질문 ID
- `cond` (str|list, 선택): 조건문
- `options` (dict|list, 필수): 드롭다운 선택지
- `rows` (dict|list, 필수): 행 목록
- `row_cond` (str|int, 선택): 행 조건
- `duplicate` (bool, 선택): 중복 응답 제한 여부 (기본: False)
- `fail` (str, 선택): 조건 실패시 이동할 위치
- `post_logic` (str, 선택): 응답 후 로직
- `change` (bool, 선택): 기존 QID 변경 여부
- `inplace` (bool, 선택): 현재 인스턴스에 추가할지 여부

**사용 예시:**

```python
# 기본 드롭다운
beluga.dropdown(
    title="각 항목에 대한 만족도를 선택해주세요",
    options=["매우 불만족", "불만족", "보통", "만족", "매우 만족"],
    rows=["가격", "품질", "서비스"],
    qid="Q24"
)

# 중복 응답 제한
beluga.dropdown(
    title="선호도 순위를 선택해주세요",
    options=["1순위", "2순위", "3순위"],
    rows=["상품A", "상품B", "상품C"],
    duplicate=True,
    qid="Q25"
)
```

## 데이터 관리 메서드

### show_df() - DataFrame 조회

생성된 문항 DataFrame을 조회합니다.

**파라미터:**

- `qid` (str, 선택): 특정 QID 조회 (None시 전체 조회)

**사용 예시:**

```python
# 전체 문항 조회
df = beluga.show_df()
print(df)

# 특정 문항 조회
df_q1 = beluga.show_df("Q1")
print(df_q1)
```

### show_options() - 선택지 출력

특정 문항의 선택지를 출력합니다.

**파라미터:**

- `qid` (str, 필수): 질문 ID

**사용 예시:**

```python
beluga.show_options("Q1")
```

### to_excel() - Excel 파일 저장

생성된 문항을 Excel 파일로 저장합니다.

**파라미터:**

- `path` (str, 필수): 저장할 파일 경로

**사용 예시:**

```python
beluga.to_excel("survey_questions.xlsx")
```

## 공통 파라미터

### 조건문 (cond)

문항 표시 조건을 설정합니다.

```python
# 단일 조건
cond="Q1A1"

# 복수 조건
cond="Q1A1 && Q2CNT > 3"

# 리스트 형태
cond=["Q1A1", "Q2CNT > 3"]
```

### 파이핑 (piping)

이전 문항의 응답을 현재 문항에 반영합니다.

```python
# QID로 파이핑
piping="Q1"

# 문항 번호로 파이핑
piping=1

# BelugaQuestion 객체로 파이핑
piping=beluga_question_obj
```

### 로테이션 (rotation)

선택지 순서를 무작위로 섞습니다.

```python
rotation=True   # 로테이션 적용
rotation=False  # 로테이션 미적용
```

## 고급 기능

### 체인 메서드 사용

```python
# 메서드 체이닝
beluga.sa(
    title="성별을 선택해주세요",
    options=["남성", "여성"],
    qid="Q1"
).ma(
    title="관심 분야를 선택해주세요",
    options=["프로그래밍", "데이터", "AI"],
    qid="Q2"
).scale(
    title="만족도를 평가해주세요",
    left="불만족",
    right="만족",
    score=5,
    qid="Q3"
)
```

### 문항 수정

```python
# 기존 문항 수정 (change=True)
beluga.sa(
    title="수정된 성별 질문",
    options=["남성", "여성", "기타"],
    qid="Q1",
    change=True
)
```

### 조건부 로직

```python
# 복잡한 조건부 로직
beluga.sa(
    title="추가 질문",
    options=["예", "아니오"],
    cond="(Q1A1 || Q1A2) && Q2CNT > 3",
    qid="Q_EXTRA"
)
```

### 다중 입력 고급 사용

```python
# 복잡한 다중 입력
beluga.number(
    title="월별 매출을 입력해주세요",
    multi={
        1: "1월", 2: "2월", 3: "3월",
        4: "4월", 5: "5월", 6: "6월"
    },
    min=0,
    post_text="만원",
    multi_width="100px",
    qid="SALES"
)
```

## 주의사항

1. **QID 중복**: 같은 QID를 사용할 때는 `change=True`로 설정해야 합니다.
2. **척도 점수**: `scale()` 메서드의 `score` 파라미터는 [3,4,5,6,7,9,10,11] 중 하나여야 합니다.
3. **필수 파라미터**: `title`은 모든 메서드에서 필수 파라미터입니다.
4. **옵션 형태**: `options`는 리스트 또는 딕셔너리 형태로 제공해야 합니다.
5. **조건문 문법**: 조건문은 JavaScript 문법을 따릅니다.

## 예시: 완전한 설문 작성

```python
from beluga import Beluga

# 인스턴스 생성
beluga = Beluga()

# 기본 정보 수집
beluga.sa(
    title="성별을 선택해주세요",
    options=["남성", "여성"],
    qid="GENDER"
)

beluga.number(
    title="나이를 입력해주세요",
    min=0,
    max=120,
    post_text="세",
    qid="AGE"
)

# 만족도 조사
beluga.scale(
    title="전반적인 만족도를 평가해주세요",
    left="매우 불만족",
    right="매우 만족",
    score=5,
    qid="SATISFACTION"
)

# 조건부 문항
beluga.text(
    title="불만족 사유를 작성해주세요",
    cond="Q#[SATISFACTION] <= 2",
    qid="DISSATISFACTION_REASON"
)

# 다중 선택
beluga.ma(
    title="개선이 필요한 부분을 선택해주세요 (복수 선택)",
    options=["가격", "품질", "서비스", "배송"],
    etc=True,
    min=1,
    max=3,
    qid="IMPROVEMENT_AREAS"
)

# 최종 의견
beluga.text(
    title="추가 의견이 있으시면 자유롭게 작성해주세요",
    qid="ADDITIONAL_COMMENTS"
)

# Excel 파일로 저장
beluga.to_excel("complete_survey.xlsx")

# 생성된 문항 확인
print(beluga.show_df())
```

## QID 참조 기능 (extract_qids)

### 개요

Beluga 라이브러리는 `title`과 `cond` 파라미터에서 `#[QID]` 패턴을 사용하여 다른 문항의 번호를 동적으로 참조할 수 있는 기능을 제공합니다. 이는 매우 중요한 기능으로, 문항 간의 연관성을 표현할 때 사용됩니다.

### 사용 방법

`#[QID]` 패턴을 사용하면 해당 QID의 문항번호로 자동 치환됩니다.

### 사용 예시

#### 1. 조건문에서 QID 참조

```python
# 기본 문항들 생성
beluga.sa(
    title="성별을 선택해주세요",
    options=["남성", "여성"],
    qid="GENDER"
)

beluga.scale(
    title="만족도를 평가해주세요",
    left="매우 불만족",
    right="매우 만족",
    score=5,
    qid="SATISFACTION"
)

# QID 참조를 사용한 조건부 문항
beluga.text(
    title="불만족 사유를 작성해주세요",
    cond="Q#[SATISFACTION] <= 2",  # SATISFACTION 문항의 번호로 자동 치환
    qid="DISSATISFACTION_REASON"
)
```

#### 2. 제목에서 QID 참조

```python
# 이전 응답을 참조하는 문항
beluga.sa(
    title="앞서 #[GENDER] 번 문항에서 선택하신 성별에 따른 추가 질문입니다",
    options=["예", "아니오"],
    qid="GENDER_FOLLOW_UP"
)
```

#### 3. 복합 조건에서 QID 참조

```python
beluga.ma(
    title="개선 사항을 선택해주세요",
    options=["가격", "품질", "서비스", "배송"],
    cond="Q#[SATISFACTION] <= 3 && Q#[GENDER] == 1",  # 만족도 3점 이하이고 성별이 남성인 경우
    qid="IMPROVEMENT_SUGGESTIONS"
)
```

#### 4. 다중 QID 참조

```python
beluga.text(
    title="#[GENDER] 번과 #[SATISFACTION] 번 문항을 참고하여 의견을 작성해주세요",
    cond="Q#[GENDER] == 1 || Q#[SATISFACTION] >= 4",
    qid="DETAILED_FEEDBACK"
)
```

### 실제 변환 예시

문항이 다음과 같이 생성되었다고 가정:

- GENDER (문항번호: 1)
- SATISFACTION (문항번호: 3)
- AGE (문항번호: 2)

```python
# 작성한 코드
beluga.text(
    title="앞서 #[GENDER] 번 문항에서 응답하신 내용을 바탕으로 답변해주세요",
    cond="Q#[SATISFACTION] <= 2 && Q#[AGE] >= 30",
    qid="FOLLOW_UP"
)

# 실제 변환된 결과
# title: "앞서 1 번 문항에서 응답하신 내용을 바탕으로 답변해주세요"
# cond: "Q3 <= 2 && Q2 >= 30"
```

### 주요 특징

1. **동적 참조**: 문항 순서가 바뀌어도 자동으로 올바른 문항번호로 치환됩니다.
2. **제목과 조건문 모두 지원**: `title`과 `cond` 파라미터에서 모두 사용 가능합니다.
3. **복수 참조 가능**: 하나의 문자열에서 여러 개의 QID를 참조할 수 있습니다.
4. **정규식 기반**: `#[QID명]` 패턴을 정확히 매칭합니다.

### 실용적인 활용 예시

```python
from beluga import Beluga

beluga = Beluga()

# 기본 정보 수집
beluga.sa(
    title="성별을 선택해주세요",
    options=["남성", "여성"],
    qid="GENDER"
)

beluga.number(
    title="나이를 입력해주세요",
    min=0,
    max=100,
    post_text="세",
    qid="AGE"
)

beluga.scale(
    title="서비스 만족도를 평가해주세요",
    left="매우 불만족",
    right="매우 만족",
    score=5,
    qid="SERVICE_SATISFACTION"
)

# QID 참조를 활용한 조건부 문항들
beluga.text(
    title="#[GENDER] 번 문항에서 선택하신 성별을 고려한 추가 의견을 작성해주세요",
    cond="Q#[AGE] >= 20",  # 20세 이상만 표시
    qid="GENDER_SPECIFIC_FEEDBACK"
)

beluga.ma(
    title="만족도가 낮은 이유를 선택해주세요 (복수 선택)",
    options=["가격", "품질", "서비스", "접근성"],
    cond="Q#[SERVICE_SATISFACTION] <= 2",  # 만족도 2점 이하만 표시
    min=1,
    max=3,
    qid="DISSATISFACTION_REASONS"
)

beluga.text(
    title="#[SERVICE_SATISFACTION] 번 문항에서 평가하신 점수에 대한 구체적인 이유를 작성해주세요",
    cond="Q#[SERVICE_SATISFACTION] <= 2 || Q#[SERVICE_SATISFACTION] >= 4",  # 극값인 경우만 표시
    qid="DETAILED_SATISFACTION_REASON"
)

# 연령대별 맞춤 문항
beluga.sa(
    title="#[AGE] 번 문항에서 입력하신 연령대에 적합한 서비스 개선 방향을 선택해주세요",
    options=["모바일 최적화", "사용성 개선", "고객 지원 강화", "가격 정책 개선"],
    cond="Q#[AGE] >= 18",  # 성인만 표시
    qid="AGE_SPECIFIC_IMPROVEMENT"
)

beluga.to_excel("survey_with_qid_references.xlsx")
```

### 주의사항

1. **QID 존재 확인**: 참조하는 QID가 실제로 존재하는지 확인해야 합니다.
2. **순서 의존성**: 참조되는 문항이 참조하는 문항보다 먼저 생성되어야 합니다.
3. **정확한 패턴**: `#[QID]` 형태를 정확히 지켜야 합니다. 대괄호나 샵 기호가 누락되면 치환되지 않습니다.
4. **대소문자 구분**: QID는 대소문자를 구분합니다.

이 QID 참조 기능을 활용하면 문항 간의 연관성을 효과적으로 표현하고, 동적이고 지능적인 설문을 구성할 수 있습니다.
