from typing import Optional, Union, List

multi_container = '''<div class="multi-container" style="width: 100%;display: flex;flex-direction: column;gap: 10px;padding: 5px;">{html}{total}</div>'''

multi_input = '''<div class="multi multi-{code}"> <div style="display: flex; gap:5px; align-items: center;"> <input type="text" id="x{code}" style="border: 1px solid #ccc; border-radius: 7px; height: 25px; width: 100%; max-width: {width};"/>{post_text} </div> </div>'''

multi_input_with_label = '''<div class="multi multi-{code}" style="display: flex;flex-direction: column;gap: 5px;margin-bottom: 7px;"> <label for="x{code}">{label}</label> <div style="display: flex; gap:5px; align-items: center;"> <input type="text" id="x{code}" style="border: 1px solid #ccc; border-radius: 7px; height: 25px; width: 100%; max-width: {width};"/>{post_text} </div> </div> '''

multi_total = '''<div class="multi-total" style="display: flex;flex-direction: column;gap: 5px;border-top: 1px solid #ccc;padding-top: 7px;margin-bottom: 7px;"> <label for="xTotal">{total_label}</label> <div style="display: flex; gap:5px; align-items: center;"> <input type="number" id="xTotal" style="border: 1px solid #ccc; border-radius: 7px; height: 25px; width: 100%; max-width: {width};background-color: #ececec; color: rgb(245, 94, 94);font-weight: bold;" readonly/>{post_text} </div> </div>'''

dropdown_container = '''<div class="multi-container" style="display:flex; flex-direction: column; gap: 20px; width: 100%;">{html}</div>'''
dropdown_html = '''<div class="multi multi-{code}" style="display:flex; flex-direction: column; gap: 5px;"> <label for="x{code}">{label}</label> <div style="display: flex; gap: 10px; align-items: center;"> <select id="x1" style="width: 100%;min-height: 30px;border: 1px solid #ccc;border-radius: 7px;"> <option value="">{placeholder}</option>{options} </select> </div> </div> '''



def set_multi_input(
        n: Union[int, list[str], dict] = 1,
        type: str = 'text',
        width: str = '200px',
        post_text: Optional[str] = None,
        total: bool = False,
        total_label: str = '합계',
        ) -> str:

    multi_html = []
    post = '' if post_text == None else f' {post_text}'
    if isinstance(n, int) :
        for i in range(1, n+1) :
            multi_html.append(multi_input.format(code=i, type=type, width=width, post_text=post))

    elif isinstance(n, list) :
        for i, label in enumerate(n, 1) :
            multi_html.append(multi_input_with_label.format(code=i, label=label, width=width, post_text=post))
    elif isinstance(n, dict) :
        for i, label in n.items() :
            multi_html.append(multi_input_with_label.format(code=i, label=label, width=width, post_text=post))

    total_html = ''
    if total :
        total_html = multi_total.format(total_label=total_label, width=width, post_text=post)

    return multi_container.format(html=''.join(multi_html), total=total_html)


def set_dropdown(
        options: Union[List[str], str] = [],
        rows: Union[List[str]] = [],
        placeholder: str = '하나 선택...',
    ) -> str:
        if isinstance(options, list) :
            option_tags = [f'<option value="{value}">{option}</option>' for value, option in enumerate(options, 1)]
            option_tags = ''.join(option_tags)

        if isinstance(rows, dict) :
            option_tags = [f'<option value="{value}">{option}</option>' for value, option in options.items()]
            option_tags = ''.join(option_tags)

        if isinstance(rows, list) :
            row_tags = [dropdown_html.format(code=code, label=row, placeholder=placeholder, options=option_tags) for code, row in enumerate(rows, 1)]

        if isinstance(rows, dict) :
            row_tags = [dropdown_html.format(code=code, label=row, placeholder=placeholder, options=option_tags) for code, row in rows.items()]

        return dropdown_container.format(html=''.join(row_tags))


def table(text: str, border: str = 'dashed', bg: bool = False, bg_color: str = 'rgba(215, 215, 215, 0.4)') -> str :
    # 배경색 스타일 설정
    bg_style = f' background-color: {bg_color};' if bg else ''

    # 테이블 스타일과 데이터 스타일에 배경색 추가
    table_style = f'width: 100%; font-size: 16px;{bg_style}'

    html = f'''<table class="fr-tag mce-item-table" style="{table_style}"><tbody><tr><td style="padding: 10px; text-align: center; border: 1px {border} #979797;"><p class="fr-tag">{text}</p></td></tr></tbody></table>'''

    return html