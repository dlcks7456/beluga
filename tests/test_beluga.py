import pytest
import pandas as pd
from beluga import Beluga, BelugaConfig


class TestBeluga:
    def test_beluga_initialization(self):
        """Beluga 인스턴스가 올바르게 초기화되는지 테스트"""
        beluga = Beluga()
        assert isinstance(beluga.df, pd.DataFrame)
        assert beluga.config is not None
        assert beluga.etc_text == '기타(직접 입력)'

    def test_beluga_with_config(self):
        """설정과 함께 Beluga 인스턴스가 초기화되는지 테스트"""
        config = BelugaConfig(etc_text="기타", default_rotation=True)
        beluga = Beluga(config)
        assert beluga.etc_text == "기타"
        assert beluga.config.default_rotation is True

    def test_sa_method(self):
        """단일 선택 문항 추가 테스트"""
        beluga = Beluga()
        result = beluga.sa(
            title="성별을 선택해주세요",
            options=["남성", "여성"],
            qid="Q1"
        )

        assert len(beluga.df) == 1
        assert beluga.df.iloc[0]['QID'] == "Q1"
        assert beluga.df.iloc[0]['질문'] == "성별을 선택해주세요"
        assert beluga.df.iloc[0]['문항유형'] == "SA"

    def test_ma_method(self):
        """다중 선택 문항 추가 테스트"""
        beluga = Beluga()
        result = beluga.ma(
            title="관심 분야를 선택해주세요",
            options=["프로그래밍", "데이터 분석", "머신러닝"],
            min=1,
            max=2,
            qid="Q2"
        )

        assert len(beluga.df) == 1
        assert beluga.df.iloc[0]['QID'] == "Q2"
        assert beluga.df.iloc[0]['질문'] == "관심 분야를 선택해주세요"
        assert beluga.df.iloc[0]['문항유형'] == "MA"
        assert beluga.df.iloc[0]['최소'] == 1
        assert beluga.df.iloc[0]['최대'] == 2

    def test_scale_method(self):
        """척도형 문항 추가 테스트"""
        beluga = Beluga()
        result = beluga.scale(
            title="만족도를 평가해주세요",
            left="매우 불만족",
            right="매우 만족",
            score=5,
            qid="Q3"
        )

        assert len(beluga.df) == 1
        assert beluga.df.iloc[0]['QID'] == "Q3"
        assert beluga.df.iloc[0]['질문'] == "만족도를 평가해주세요"
        assert beluga.df.iloc[0]['문항유형'] == "SCALE"

    def test_text_method(self):
        """텍스트 입력 문항 추가 테스트"""
        beluga = Beluga()
        result = beluga.text(
            title="의견을 작성해주세요",
            qid="Q4"
        )

        assert len(beluga.df) == 1
        assert beluga.df.iloc[0]['QID'] == "Q4"
        assert beluga.df.iloc[0]['질문'] == "의견을 작성해주세요"
        assert beluga.df.iloc[0]['문항유형'] == "TEXT"

    def test_show_df_method(self):
        """DataFrame 조회 메서드 테스트"""
        beluga = Beluga()
        beluga.sa(title="질문1", options=["옵션1"], qid="Q1")
        beluga.sa(title="질문2", options=["옵션2"], qid="Q2")

        # 전체 조회
        df = beluga.show_df()
        assert len(df) == 2

        # 특정 QID 조회
        df_q1 = beluga.show_df("Q1")
        assert len(df_q1) == 1
        assert df_q1.iloc[0]['QID'] == "Q1"

    def test_duplicate_qid_validation(self):
        """중복 QID 검증 테스트"""
        beluga = Beluga()
        beluga.sa(title="질문1", options=["옵션1"], qid="Q1")

        # 중복 QID로 추가 시도 (change=False)
        with pytest.raises(Exception):
            beluga.sa(title="질문2", options=["옵션2"], qid="Q1", change=False)

        # change=True로 변경
        beluga.sa(title="질문2", options=["옵션2"], qid="Q1", change=True)
        assert len(beluga.df) == 1
        assert beluga.df.iloc[0]['질문'] == "질문2"


if __name__ == "__main__":
    pytest.main([__file__])