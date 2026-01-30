from typing import Union, Optional

multi_text_atleast_js = '''(() => {{
  const errorMessages = {text_atleast_error};

  const question = $(`#survey${{cur}}`);
  const nextBtn = question.find('.next-btn-wrapper');
  question.find('.answer').hide();
  nextBtn.attr('onclick', null);

  const raw = question.find(`.multi input`);
  const rawIndex = [...raw].map((e) => Number(e.id.replace('x', ''))).sort((a, b) => a - b);

  const inputs = question.find(`.multi input`);

  inputs.off('keyup change').on('keyup change', (e) => {{
    const index = inputs.index(e.currentTarget);
    const prevInputs = inputs.slice(0, index);

    const hasEmptyPrev = [...prevInputs].some((input) => input.value.trim() === '');

    if (hasEmptyPrev) {{
      e.currentTarget.value = '';
      if (index > 0) {{
        const emptyInputs = [...prevInputs].findIndex(input => input.value.trim() === '');
        if (emptyInputs !== -1) {{
          inputs.eq(emptyInputs).focus();
        }} else {{
          inputs.eq(index - 1).focus();
        }}
      }}

      alert(errorMessages.outOfOrder);
    }}
  }});

  nextBtn.click(() => {{
    const inputs = question.find(`.multi input`);
    if (inputs.eq(0).val().trim() === '') {{
      alert(errorMessages.empty);
      inputs.eq(0).focus();
      return;
    }}

    const values = [...inputs].filter((e) => e.value.trim() !== '').map((e) => e.value);
    if (new Set(values).size !== values.length) {{
      alert(errorMessages.duplicate);
      return;
    }}

    const answer = rawIndex.map((e) => $(`#survey${{cur}} #x${{e}}`).val()).join('|');
    $(`#answer${{cur}}`).val(answer);
    goNext();
  }});

  return true;
}})()'''




multi_text_all_js = '''(() => {{
  const errorMessages = {text_all_error};

  const question = $(`#survey${{cur}}`);
  const nextBtn = question.find('.next-btn-wrapper');
  question.find('.answer').hide();
  nextBtn.attr('onclick', null);

  const raw = question.find(`.multi input`);
  const rawIndex = [...raw].map((e) => Number(e.id.replace('x', ''))).sort((a, b) => a - b);

  nextBtn.click(() => {{
    const inputs = [...question.find(`.multi input`)].filter((input) => !input.disabled);
    if ([...inputs].some((e) => e.value.trim() === '')) {{
      alert(errorMessages.empty);
      return;
    }}

    const values = [...inputs].map((e) => e.value);
    if (new Set(values).size !== values.length) {{
      alert(errorMessages.duplicate);
      return;
    }}

    const answer = rawIndex.map((e) => $(`#survey${{cur}} #x${{e}}`).val()).join('|');
    $(`#answer${{cur}}`).val(answer);
    goNext();
  }});

  return true;
}})()'''




multi_num_js = '''(() => {{
  let min = {min};
  let max = {max};
  let total = {total};

  const errorMessages = {num_error};

  const question = $(`#survey${{cur}}`);
  const nextBtn = question.find('.next-btn-wrapper');
  question.find('.answer').hide();
  question.find('.question-foot').hide();
  nextBtn.attr('onclick', null);

  const raw = question.find(`.multi input`);
  const rawIndex = [...raw].map((e) => Number(e.id.replace('x', ''))).sort((a, b) => a - b);

  if (total !== null) {{
    question.on('keyup', (e) => {{
      const totalInput = question.find('#xTotal');
      const inputs = question.find(`.multi input`);
      const sum = [...inputs].reduce((acc, cur) => acc + Number(cur.value), 0);
      totalInput.val(sum);
    }});
  }}

  nextBtn.click(() => {{
    const inputs = [...question.find(`.multi input`)].filter((input) => !input.disabled);

    // Empty
    if (inputs.some((e) => $(e).val() === '')) {{
      alert(errorMessages.empty);
      return;
    }}

    // Range
    if (inputs.some((e) => Number(e.value) < min || Number(e.value) > max)) {{
      alert(errorMessages.range);
      return;
    }}

    // Total
    if (total !== null && inputs.reduce((acc, cur) => acc + Number(cur.value), 0) !== total) {{
      alert(errorMessages.total);
      return;
    }}

    const answer = rawIndex.map((e) => $(`#survey${{cur}} #x${{e}}`).val()).join('|');
    $(`#answer${{cur}}`).val(answer);
    goNext();
  }});

  return true;
}})()'''


dropdown_js = '''(() => {{
  const duplicateCheck = {duplicate};
  const errorMessages = {dropdown_error};
  const question = $(`#survey${{cur}}`);
  const nextBtn = question.find('.next-btn-wrapper');
  question.find('.answer').hide();
  question.find('.question-foot').hide();
  nextBtn.attr('onclick', null);

  const raw = question.find(`.multi select`);
  const rawIndex = [...raw].map((e) => Number(e.id.replace('x', ''))).sort((a, b) => a - b);

  nextBtn.click(() => {{
    // Empty
    const selects = [...question.find(`.multi select`)].filter((select) => !select.disabled);
    if (selects.some((select) => select.value === '')) {{
      alert(errorMessages.empty);
      return;
    }}

    // Duplicate
    const values = [...selects].map((select) => select.value);
    if (duplicateCheck && values.some((value, index) => values.indexOf(value) !== index)) {{
      alert(errorMessages.duplicate);
      return;
    }}

    const answer = rawIndex.map((e) => $(`#survey${{cur}} #x${{e}}`).val()).join('|');
    $(`#answer${{cur}}`).val(answer);
    goNext();
  }});

  return true;
}})()'''

dropdown_row_cond = '''(() => {{
  const question = $(`#survey${{cur}}`);
  const multis = question.find('.multi');
  const base = getAnswerSet({base});
  multis.hide();
  multis.find('input, select').prop('disabled', true);
  base.answers.forEach((answer) => {{
    const code = answer.value.order;
    const target = question.find(`.multi-${{code}}`);
    target.show();
    target.find('input, select').prop('disabled', false);
  }});
  return true;
}})()'''


def any_list(options: list) -> bool :
    return any(isinstance(option, list) for option in options)

def any_dict(options: dict) -> bool :
    return any(isinstance(option, dict) for option in options.values())

def list_group_set(options: list) -> Optional[list] :
  if isinstance(options, list) :
      if not any_list(options) :
        return None

  code = 0
  groups = []
  for option in options :
    if isinstance(option, list) :
      group = []
      for sub in option :
        code += 1
        group.append(code)

      groups.append([group[0], group[-1]])
    else :
       code += 1

  return groups

def dict_group_set(options: dict) -> Optional[dict] :
  if isinstance(options, dict) :
    if not any_dict(options) :
      return None

  groups = {}
  for key, value in options.items() :
    if isinstance(value, dict) :
      group = []
      for sub_key in value.keys() :
        group.append(sub_key)

      if group :
        groups[key] = [min(group), max(group)]

  return list(groups.values())


def group_rot(options: Union[list, dict], group_config: Optional[dict] = None) -> Optional[str]:
    if isinstance(options, list) :
      group_set = list_group_set(options)

    if isinstance(options, dict) :
      group_set = dict_group_set(options)

    if group_set is None or len(group_set) == 0:
      return None

    between_js = map(lambda x: f'\toBetween({x[0]}, {x[1]})', group_set)
    between_js = ',\n'.join(between_js)

    config_arg = {}
    if group_config is not None :
      bool_list = ['group', 'option', 'topShuffle', 'botShuffle']
      for key in bool_list :
        if key in group_config :
          config_arg[key] =  'true' if group_config[key] else 'false'

      if 'top' in group_config :
        config_arg['top'] = group_config['top']

      if 'bot' in group_config :
        config_arg['bot'] = group_config['bot']

    if len(config_arg) > 0 :
      config_arg = ',\n'.join(map(lambda x: f'\t{x[0]}: {x[1]}', config_arg.items()))
      return f'''oGroupRotation([
{between_js}
],
{{
{config_arg}
}})'''

    return f'''oGroupRotation([
{between_js}
])'''


piping_js = '''oShowByAnswer({{base: {base}, must: []}}) && (()=>{{
    {extra}
    return true;
}})()'''


rv_piping_js = '''oHideByAnswer({{base: {base}}}) && (()=>{{
    {extra}
    return true;
}})()'''