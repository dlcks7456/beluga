import re
from itertools import product
from typing import List, Union
from IPython.display import display, HTML, Markdown

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


def quota_combination(quota_list: str, show: bool = True) -> Union[str, None]:
    def parse_js_object_to_dict(js_obj_str):
        # 각 object 블록을 추출
        obj_pattern = re.compile(r"(\w+)\s*:\s*\{([^}]*)\}", re.DOTALL)
        result = {}
        for obj_match in obj_pattern.finditer(js_obj_str):
            obj_name = obj_match.group(1)
            obj_body = obj_match.group(2)
            # 각 key-value 쌍을 추출
            kv_pattern = re.compile(r"'([^']+)'\s*:\s*([^,]+),?")
            obj_dict = {}
            for kv_match in kv_pattern.finditer(obj_body):
                k = kv_match.group(1)
                v = kv_match.group(2).strip()
                obj_dict[k] = v
            result[obj_name] = obj_dict
        return result

    parse_dict = parse_js_object_to_dict(quota_list)

    quota_logics = list(parse_dict.values())

    # 각 dict의 key, value 쌍을 리스트로 변환
    key_value_lists = [list(d.items()) for d in quota_logics]

    # 모든 조합 생성
    combinations = product(*key_value_lists)

    # 조합을 원하는 형태의 dict로 변환
    quota_combinations = {}
    for combo in combinations:
        # key는 '_'로 join, value는 조건만 리스트로
        keys = [k for k, v in combo]
        values = [v for k, v in combo]
        combo_key = '_'.join(keys)
        quota_combinations[combo_key] = values

    quota_conds = {quota: ' && '.join([f'({c})' for c in cond]) for quota, cond in quota_combinations.items()}

    quota_lines = [f"\t'{quota}': {cond}," for quota, cond in quota_conds.items()]

    export_js = "allCombinationsQuota : {\n%s\n}" % '\n'.join(quota_lines)

    if show:
        # HTML, JS로 UI 구성: 코드블럭 + 복사 버튼
        html_code = f"""
        <style>
        .quota-export-block {{
            position: relative;
            margin: 10px 0 20px 0;
            font-family: 'Noto Sans KR', 'Consolas', 'monospace', monospace;
            color: black;
        }}
        .quota-export-block pre {{
            background: #f4f4f4;
            border-radius: 7px;
            padding: 16px 12px 16px 16px;
            font-size: 13px;
            line-height: 1.5;
            overflow-x: auto;
            margin: 0;
            font-family: 'Consolas', 'monospace', monospace;
        }}
        .quota-export-block .copy-btn {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #26a9df;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
            z-index: 2;
        }}
        .quota-export-block .copy-btn:hover {{
            background: #1e7fa6;
        }}
        </style>
        <div class="quota-export-block">
            <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('quota-export-js').innerText);this.innerText='복사 완료';setTimeout(()=>{{this.innerText='복사하기';}},1200);">복사하기</button>
            <pre id="quota-export-js">{export_js}</pre>
        </div>
        """
        display(HTML(html_code))
    else:
        return export_js