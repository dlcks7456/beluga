from IPython.display import display, HTML, Markdown
from .belugaQuestion import BelugaQuestion

def preview_question(question: BelugaQuestion):
    options = question.option_list
    has_options = options is not None and len(options) > 0
    option_buttons = ""
    if has_options:
        for option in options:
            option_buttons += f"""
            <div class='b-option-btn'>
                <span class='b-option-value'>{option.value}</span>
                <span class='b-option-label'>{option.label}</span>
            </div>
            """
    else:
        option_buttons = "<div class='b-no-option'>선택지가 없습니다.</div>"

    # 설정 정보 뱃지
    badges = []
    if question.piping is not None and str(question.piping).strip() != "":
        badges.append(f"<span class='b-badge b-piping'>파이핑: {question.piping}</span>")
    if question.rotation:
        badges.append(f"<span class='b-badge b-rotation'>로테이션</span>")
    if hasattr(question, 'etc') and question.etc:
        badges.append(f"<span class='b-badge b-etc'>기타 포함</span>")
    if hasattr(question, 'na') and question.na:
        badges.append(f"<span class='b-badge b-na'>없음 포함</span>")
    if hasattr(question, 'min') and hasattr(question, 'max'):
        if question.min is not None or question.max is not None:
            minmax = []
            if question.min is not None:
                minmax.append(f"최소 {question.min}")
            if question.max is not None:
                minmax.append(f"최대 {question.max}")
            badges.append(f"<span class='b-badge b-minmax'>{' / '.join(minmax)}</span>")

    # qid, 타입, Logic 버튼 한 행에 배치
    show_logic = question.cond is not None and str(question.cond).strip() != ''

    logic_button = ""
    logic_accordion = ""
    if show_logic:
        logic_button = """
        <button class='b-logic-btn' onclick="var acc=document.getElementById('b-logic-acc'); if(acc.style.display==='block'){acc.style.display='none';}else{acc.style.display='block'; if(window.hljs){hljs.highlightElement(acc.querySelector('code'));}}">Logic</button>
        """
        logic_accordion = f"""<div class='b-logic-accordion' id='b-logic-acc' style='display:none;'><pre class='b-logic-code'><code class='language-javascript'>{question.cond.strip()}</code></pre></div>"""

    # qid 뱃지
    qid_badge = f"<span class='b-qid-badge'>{question.qid}</span>"
    type_badge = f"<span class='b-type-badge'>{question.type}</span>"

    style_id = "beluga-survey-preview-style"
    style_tag = f"""
    <style id='{style_id}'>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    .beluga-survey-preview-wrapper {{
        display: flex;
        flex-direction: row;
        width: 100%;
        min-width: 0;
        height: 557px;
        min-height: 557px;
        max-height: 557px;
        background: none;
        box-sizing: border-box;
        gap: 0;
    }}
    .beluga-survey-preview {{
        background: #fff;
        border-radius: 12px 0 0 12px;
        box-shadow: 0 2px 8px 0 rgba(38,169,223,0.10);
        padding: 14px 10px 10px 10px;
        width: 500px;
        min-width: 500px;
        max-width: 500px;
        height: 557px;
        min-height: 557px;
        max-height: 557px;
        margin: 0 !important;
        float: left;
        text-align: left;
        display: block;
        font-family: 'Noto Sans KR', 'Segoe UI', 'Apple SD Gothic Neo', 'Malgun Gothic', Arial, sans-serif;
        font-size: 13px;
        border: 1.5px solid #26a9df;
        border-right: none;
        box-sizing: border-box;
        overflow: hidden;
    }}
    .beluga-logic-block {{
        background: #f4fbfe;
        border-radius: 0 12px 12px 0;
        border: 1.5px solid #26a9df;
        border-left: none;
        flex: 1 1 0;
        min-width: 0;
        height: 557px;
        min-height: 557px;
        max-height: 557px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: stretch;
        justify-content: flex-start;
        padding: 0;
        overflow: hidden;
    }}
    .beluga-logic-title {{
        font-family: 'Noto Sans KR', 'Segoe UI', Arial, sans-serif;
        font-size: 15px;
        font-weight: 700;
        color: #26a9df;
        background: #eaf7fc;
        padding: 14px 18px 10px 18px;
        border-bottom: 1px solid #b6e6fa;
        border-radius: 0 12px 0 0;
        margin-bottom: 0;
    }}
    .beluga-logic-code-scroll {{
        flex: 1 1 0;
        max-height: 495px;
        min-height: 60px;
        overflow-y: auto;
        padding: 18px 18px 10px 18px;
        box-sizing: border-box;
        scrollbar-color: #26a9df #f4fbfe;
        scrollbar-width: thin;
    }}
    .beluga-logic-code-scroll pre {{
        background: #f4fbfe;
        color: #222;
        font-size: 13px;
        border-radius: 0 0 10px 10px;
        margin: 0;
        padding: 0;
        overflow-x: auto;
        border: none;
        box-shadow: none;
    }}
    .beluga-logic-code-scroll code {{
        background: none;
        font-family: 'Fira Mono', 'Consolas', 'Menlo', 'Monaco', 'monospace';
        font-size: 13px;
        line-height: 1.6;
        white-space: pre;
        word-break: break-all;
        display: block;
        padding: 0;
    }}
    .beluga-logic-code-scroll::-webkit-scrollbar {{
        width: 8px;
        background: #eaf7fc;
        border-radius: 6px;
    }}
    .beluga-logic-code-scroll::-webkit-scrollbar-thumb {{
        background: #26a9df;
        border-radius: 6px;
        border: none;
        min-height: 30px;
        transition: background 0.2s;
    }}
    .beluga-logic-code-scroll:hover::-webkit-scrollbar-thumb {{
        background: #1e7fa6;
    }}
    .beluga-logic-code-scroll::-webkit-scrollbar-track {{
        background: #eaf7fc;
        border-radius: 6px;
    }}
    .beluga-survey-preview .b-header-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 7px;
        min-height: 26px;
        height: 26px;
    }}
    .beluga-survey-preview .b-header-left {{
        display: flex;
        align-items: center;
        gap: 6px;
        height: 26px;
    }}
    .beluga-survey-preview .b-qid-badge {{
        background: #26a9df;
        color: #fff;
        font-weight: bold;
        border-radius: 6px;
        padding: 2px 8px 2px 8px;
        font-size: 11px;
        display: flex;
        align-items: center;
        height: 26px;
        letter-spacing: 0.01em;
        margin-right: 2px;
        box-sizing: border-box;
    }}
    .beluga-survey-preview .b-type-badge {{
        display: flex;
        align-items: center;
        font-size: 11px;
        color: #26a9df;
        background: #eaf7fc;
        border-radius: 6px;
        padding: 2px 8px 2px 8px;
        letter-spacing: 0.01em;
        box-shadow: 0 1.5px 6px 0 rgba(38,169,223,0.10);
        border: 1.2px solid #26a9df;
        height: 26px;
        font-weight: 600;
        box-sizing: border-box;
    }}
    .beluga-survey-preview .b-header-right {{
        flex: 1 1 0;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        min-width: 0;
        height: 26px;
    }}
    .beluga-survey-preview .b-logic-btn {{
        background: #26a9df;
        color: #fff;
        border: none;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        cursor: pointer;
        box-shadow: 0 1.5px 6px 0 rgba(38,169,223,0.10);
        transition: background 0.2s;
        height: 26px;
        display: inline-flex;
        align-items: center;
        justify-content: flex-end;
        box-sizing: border-box;
    }}
    .beluga-survey-preview .b-logic-btn:hover {{
        background: #1e7fa6;
    }}
    .beluga-survey-preview .b-logic-accordion {{
        background: #f4fbfe;
        border-radius: 7px;
        border: 1px solid #eaf7fc;
        margin-top: 7px;
        margin-bottom: 10px;
        padding: 10px 14px 8px 14px;
        font-size: 12px;
        color: #222;
        box-shadow: 0 1.5px 6px 0 rgba(38,169,223,0.07);
        display: block;
        white-space: pre-wrap;
        word-break: break-all;
        max-width: 100%;
        overflow-x: auto;
    }}
    .beluga-survey-preview .question-title {{
        font-size: 14px;
        color: #222;
        margin-bottom: 7px;
        line-height: 1.3;
        word-break: keep-all;
        margin-block: 10px;
    }}
    .beluga-survey-preview .question-badges {{
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 10px;
    }}
    .b-badge {{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 20px;
        min-width: 0;
        padding: 0 8px;
        border-radius: 5px;
        font-size: 10.5px;
        font-weight: 500;
        background: #eaf7fc;
        color: #26a9df;
        border: 1px solid #b6e6fa;
        letter-spacing: 0.01em;
        margin-bottom: 2px;
        box-sizing: border-box;
    }}
    .b-piping {{ color: #1e7fa6; background: #eaf7fc; border-color: #b6e6fa; }}
    .b-rotation {{ color: #e67e22; background: #fff4e6; border-color: #ffd6a0; }}
    .b-etc {{ color: #7c2e8e; background: #f7e6ff; border-color: #e0b6ff; }}
    .b-na {{ color: #5b5b5b; background: #f2f2f2; border-color: #d0d0d0; }}
    .b-minmax {{ color: #005b9f; background: #e6f2ff; border-color: #b6d6ff; }}
    .beluga-survey-preview .option-wrapper {{
        max-height: 350px;
        min-height: 60px;
        width: 100%;
        overflow-y: auto;
        margin-top: 10px;
        padding-right: 2px;
        box-sizing: border-box;
        scrollbar-color: #26a9df #f4fbfe;
        scrollbar-width: thin;
    }}
    .beluga-survey-preview .option-wrapper::-webkit-scrollbar {{
        width: 8px;
        background: #f4fbfe;
        border-radius: 6px;
    }}
    .beluga-survey-preview .option-wrapper::-webkit-scrollbar-thumb {{
        background: #26a9df;
        border-radius: 6px;
        border: none;
        min-height: 30px;
        transition: background 0.2s;
    }}
    .beluga-survey-preview .option-wrapper:hover::-webkit-scrollbar-thumb {{
        background: #1e7fa6;
    }}
    .beluga-survey-preview .option-wrapper::-webkit-scrollbar-track {{
        background: #f4fbfe;
        border-radius: 6px;
    }}
    .beluga-survey-preview .b-option-btn {{
        display: flex;
        align-items: center;
        gap: 10px;
        background: #fff;
        border: 1.5px solid #eaf7fc;
        border-radius: 8px;
        box-shadow: 0 2px 8px 0 rgba(38,169,223,0.13);
        padding: 7px 13px 7px 13px;
        margin-bottom: 7px;
        font-size: 13px;
        cursor: pointer;
        transition: box-shadow 0.18s, border 0.18s;
        min-height: 32px;
        width: 100%;
        box-sizing: border-box;
    }}
    .beluga-survey-preview .b-option-btn:hover {{
        border: 1.5px solid #26a9df;
        box-shadow: 0 4px 16px 0 rgba(38,169,223,0.18);
    }}
    .beluga-survey-preview .b-option-value {{
        color: #26a9df;
        font-weight: 700;
        font-size: 13px;
        min-width: 32px;
        text-align: center;
        margin-right: 8px;
    }}
    .beluga-survey-preview .b-option-label {{
        color: #222;
        font-size: 13px;
        font-weight: 400;
        word-break: break-all;
    }}
    .beluga-survey-preview .b-no-option {{
        color: #aaa;
        text-align: center;
        font-size: 13px;
        padding: 18px 0;
    }}
    </style>
    """

    # JS로 style 태그를 교체
    js_check_style = f"""
    <script>
    var existingStyle = document.getElementById('{style_id}');
    if (existingStyle) {{
        existingStyle.remove();
    }}
    var style = document.createElement('style');
    style.id = '{style_id}';
    style.innerHTML = `{style_tag.split('>',1)[1].rsplit('<',1)[0]}`;
    document.head.appendChild(style);
    </script>
    """

    # highlight.js 동적 로드 및 적용 스크립트 (아코디언 열릴 때마다 적용)
    highlight_js = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    '''

    # Logic code block always visible (right half)
    logic_code = question.cond if question.cond is not None and str(question.cond).strip() != '' else '// 문항에 적용된 Logic(JS)이 없습니다.'
    logic_block = f"""
    <div class='beluga-logic-block'>
        <div class='beluga-logic-title'>Logic (조건/로직)</div>
        <div class='beluga-logic-code-scroll'>
            <pre><code class='language-javascript'>{logic_code}</code></pre>
        </div>
    </div>
    """

    # title
    title = question.title.split('\n')
    title = '<br>'.join(title)

    html = f"""
    {js_check_style}
    {highlight_js}
    <div class='beluga-survey-preview-wrapper'>
        <div class='beluga-survey-preview'>
            <div class='b-header-row'>
                <div class='b-header-left'>
                    {qid_badge}
                    {type_badge}
                </div>
            </div>
            <div class='question-title'>{title}</div>
            <div class='question-badges'>{''.join(badges)}</div>
            <div class='option-wrapper'>
                {option_buttons}
            </div>
        </div>
        {logic_block}
        <script>
        // 코드 블록 하이라이트
        if (window.hljs) {{
            document.querySelectorAll('.beluga-logic-code-scroll code').forEach(function(block) {{ hljs.highlightElement(block); }});
        }}
        </script>
    </div>
    """
    display(HTML(html))