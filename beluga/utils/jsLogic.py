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


def group_rot(options: Union[list, dict], config: dict = {}) -> Optional[str]:
    if isinstance(options, list) :
      group_set = list_group_set(options)

    if isinstance(options, dict) :
      group_set = dict_group_set(options)

    if group_set is None or len(group_set) == 0:
      return None

    between_js = map(lambda x: f'\tbetween({x[0]}, {x[1]})', group_set)
    between_js = ',\n'.join(between_js)

    config_arg = {}
    bool_list = ['group', 'option', 'topShuffle', 'botShuffle']
    for key in bool_list :
      if key in config :
        config_arg[key] =  'true' if config[key] else 'false'

    if 'top' in config :
      config_arg['top'] = config['top']

    if 'bot' in config :
      config_arg['bot'] = config['bot']

    if len(config_arg) > 0 :
      config_arg = ',\n'.join(map(lambda x: f'\t{x[0]}: {x[1]}', config_arg.items()))
      return f'''groupRotation([
{between_js}
],
{{
{config_arg}
}})'''

    return f'''groupRotation([
{between_js}
])'''


pre_logic_dict = {
  # Between
  'between': '''window.between = (start, end) => {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
};''',

  # Group Rotation
  'groupRotation': '''window.groupRotation = (optionGroups = [], config = {}, qnum = null) => {
  config.group = config.group !== undefined ? config.group : true;
  config.option = config.option !== undefined ? config.option : true;
  try {
    if (qnum === null) {
      qnum = cur;
    }

    if (optionGroups.length === 0) return true;
    if (optionGroups.some((group) => !Array.isArray(group))) {
      throw new Error('optionGroups must be an array of arrays');
    }

    const { group: groupRandom, option: optionRandom } = config;
    const question = document.querySelector(`#survey${qnum}`);
    const originOrder = [...question.querySelectorAll('.answer-choice-wrapper')];
    let options = [];
    let fixed = [];

    originOrder.forEach((e) => {
      const rank = Number(e.querySelector('#rank').value);
      if (e.classList.contains('answer-etc') || rank === -1) {
        fixed.push(rank);
      } else {
        options.push(rank);
      }
    });

    options = options.sort((a, b) => a - b);

    let newOrders = [];

    for (const groups of optionGroups) {
      const setGroup = options.filter((e) => groups.includes(e));
      if (optionRandom) {
        setGroup.sort(() => Math.random() - 0.5);
      }
      options = options.filter((e) => !groups.includes(e));
      newOrders.push(setGroup);
    }

    if (options.length > 0) {
      options.forEach((code) => {
        newOrders.push([code]);
      });
    }

    if (groupRandom) {
      newOrders.sort(() => Math.random() - 0.5);
    }

    const answerWrapper = question.querySelector('.answer-wrapper');
    newOrders.forEach((order) => {
      order.forEach((code) => {
        const optionNode = originOrder.find((e) => e.querySelector('#rank').value === String(code));
        if (optionNode) {
          answerWrapper.appendChild(optionNode);
        } else {
          console.warn(`Option with rank ${code} not found`);
        }
      });
    });

    if ('top' in config) {
      const top = config.top;
      if (!Array.isArray(top)) throw new Error('top must be an array');

      const topShuffle = config.topShuffle ?? true;
      if (topShuffle) top.sort(() => Math.random() - 0.5);

      [...top].reverse().forEach((code) => {
        const optionNode = originOrder.find((e) => e.querySelector('#rank').value === String(code));
        optionNode
          ? answerWrapper.insertBefore(optionNode, answerWrapper.firstChild)
          : console.warn(`Top : Option with rank ${code} not found`);
      });
    }

    if ('bot' in config) {
      const bot = config.bot;
      if (!Array.isArray(bot)) throw new Error('bottom must be an array');

      const botShuffle = config.botShuffle ?? true;
      if (botShuffle) bot.sort(() => Math.random() - 0.5);

      bot.forEach((code) => {
        const optionNode = originOrder.find((e) => e.querySelector('#rank').value === String(code));
        optionNode ? answerWrapper.appendChild(optionNode) : console.warn(`Bot : Option with rank ${code} not found`);
      });
    }

    fixed.forEach((code) => {
      const optionNode = originOrder.find((e) => e.querySelector('#rank').value === String(code));
      if (optionNode) {
        answerWrapper.appendChild(optionNode);
      }
    });
  } catch (e) {
    console.error(e);
  } finally {
    return true;
  }
};''',

  # ShuffleBy
  'shuffleBy': '''window.shuffleBy = (baseQid, qnum = null) => {
  const params = { baseQid, qnum };
  for (const [key, value] of Object.entries(params)) {
    if (value === null && key === 'qnum') continue;
    if (typeof value !== 'number') {
      throw new Error(`Please set '${key}' as a number`);
    }
  }

  if (qnum === null) {
    qnum = cur;
  }

  try {
    const answerWrappers = '.answer-wrapper .answer-choice-wrapper';
    const baseQuestion = `#survey${baseQid} ${answerWrappers}`;
    const targetQuestion = `#survey${qnum} ${answerWrappers}`;

    const answerWrapper = document.querySelector(`#survey${qnum} .answer-wrapper`);

    const baseQuestionAnswers = document.querySelectorAll(baseQuestion);
    const answerOrderValues = [...baseQuestionAnswers].map((ans) => ans.querySelector(`input[id^='rank']`).value);

    const targetQuestionAnswers = document.querySelectorAll(targetQuestion);
    const targetAnswers = [...targetQuestionAnswers];
    const targetAnswerValues = targetAnswers.map((ans) => ans.querySelector(`input[id^='rank']`).value);

    const remainAnswers = targetAnswerValues.filter((value) => !answerOrderValues.includes(value) && value !== '-1');
    if (remainAnswers.length > 0) {
      throw new Error(`There are mismatched answers. : ${remainAnswers}`);
    }

    try {
      const tempContainer = document.createDocumentFragment();

      while (answerWrapper.firstChild) {
        tempContainer.appendChild(answerWrapper.firstChild);
      }

      answerOrderValues.forEach((rank) => {
        try {
          const matchingAnswer = targetAnswers.find(
            (wrapper) => wrapper.querySelector(`input[id^='rank']`).value === rank
          );
          if (matchingAnswer) {
            answerWrapper.appendChild(matchingAnswer);
          }
        } catch (error) {
          console.error('Error reordering answers:', error);
          throw error;
        }
      });

      while (tempContainer.firstChild) {
        answerWrapper.appendChild(tempContainer.firstChild);
      }

      if (typeof updateQASummary === 'function') {
        updateQASummary(qnum, `shb: Q${baseQid}`);
      }
    } catch (error) {
      console.error('Error relocating answers:', error);
      throw error;
    }
  } catch (error) {
    console.error('shuffleBy Function Errors:', error);
    throw error;
  } finally {
    return true;
  }
};''',

  # Rating Handler
  'rating': '''// ratingHandler({ reverse: true, showValue: true});
window.rating = (obj) => {
  return ratingHandler({ ...obj, qNum: cur });
};

function ratingHandler({
  reverse = false,
  showValue = false,
  qNum = null,
  balance = false,
  format = null,
  colSpan = false,
  colSize = '45%',
}) {
  try {
    const surveyForm = document.querySelector('#survey_form');
    let ratings = [];
    if (qNum === null) {
      const allQuestions = surveyForm.querySelectorAll('.survey');
      ratings = [...allQuestions].filter((question) => [5, 9].includes(Number(question.querySelector('#type').value)));
    } else {
      if (Array.isArray(qNum)) {
        ratings = qNum.map((q) => surveyForm.querySelectorAll(`#survey${q}`));
      } else {
        ratings = [surveyForm.querySelector(`#survey${qNum}`)];
      }
    }

    ratings.forEach((rating) => {
      const cells = rating.querySelectorAll('.answer-eval-wrapper tbody tr:first-child td');
      const score = cells.length;
      const ratingType = Number(rating.querySelector('#type').value);
      const tableFlag = score > 7;

      let ratingCSS = '';
      let tableCellCSS = '';

      const maxScore = cells.length;
      const halfScore = maxScore % 2 === 0 ? Math.floor(maxScore / 2) : Math.floor(maxScore / 2) + 1;

      if (ratingType === 5) {
        tableCellCSS += `
              td {
                  width: 100%;
              }`;

        if (reverse) {
          ratingCSS += `
              #${rating.id} .answer-eval-wrapper {
                  tbody tr {
                      ${tableFlag ? 'display: flex;' : ''}
                      flex-direction: row-reverse;

                      ${tableFlag ? tableCellCSS : ''}

                      &:last-child {
                        td:first-child {
                          text-align: right!important;
                        }
                        td:last-child {
                          text-align: left!important;
                        }
                      }
                  }
              }
              `;
        }

        if ((showValue || balance) && !tableFlag) {
          ratingCSS += `
                  #${rating.id} table tbody tr:first-child td {
                      position: relative;
                  }

                  #${rating.id} .cell-value {
                      position: absolute;
                      bottom: -60%;
                      left: 50%;
                      transform: translate(-50%, -50%);
                      font-size: 0.7rem;
                      z-index: 999;
                      color: #2b2a2a;
                      pointer-events: none;
                      font-weight: bold;
                      width: 100%;
                      text-align: center;
                  }`;

          cells.forEach((cell) => {
            let cellValue = Number(cell.querySelector('input').value);
            if (balance) {
              cellValue = Math.abs(cellValue - halfScore) + (cellValue <= halfScore && maxScore % 2 === 0 ? 1 : 0);
            }
            const valueLabel = document.createElement('div');
            valueLabel.classList.add('cell-value');
            valueLabel.textContent = `[${cellValue}점]`;
            if (format !== null) {
              valueLabel.textContent = format.replace('%d', cellValue);
            }
            cell.appendChild(valueLabel);
          });
        }
      }

      if (ratingType === 9) {
        ratingCSS += `
        #${rating.id} .answer .answer-wrapper {
          display: flex;
          flex-direction: column-reverse;
        }
        `;
      }

      const styleTag = document.createElement('style');
      styleTag.textContent = ratingCSS;
      rating.insertBefore(styleTag, rating.firstChild);

      if (colSpan) {
        const centerWrapper = rating.querySelector(`td.eval-text-wrapper[align='center']`);
        const leftWrapper = rating.querySelector(`td.eval-text-wrapper[align='left']`);
        const rightWrapper = rating.querySelector(`td.eval-text-wrapper[align='right']`);
        const allWrappers = rating.querySelectorAll('td.eval-text-wrapper');

        if (maxScore % 2 === 0) {
          centerWrapper.style.display = 'none';
          centerWrapper.setAttribute('colspan', 0);
        } else {
          centerWrapper.setAttribute('colspan', 1);
        }

        const spanCount = maxScore % 2 === 0 ? halfScore : halfScore - 1;

        leftWrapper.setAttribute('colspan', spanCount);
        rightWrapper.setAttribute('colspan', spanCount);
        [...allWrappers].forEach((wrapper) => {
          wrapper.style.flexBasis = colSize;
          wrapper.style.wordBreak = 'keep-all';
        });
      }
    });
  } catch (error) {
    console.error('ratingHandler error:', error);
  } finally {
    return true;
  }
};''',

  # this or that
  'thisOrThat': '''window.thisOrThat = (groups = {}, qnum = null) => {
  try {
    if (qnum === null) qnum = cur;
    if (Object.keys(groups).length === 0) return true;

    const questionId = `#survey${qnum}`;
    const question = document.querySelector(questionId);

    if (!question.querySelector('style[data-this-that-style]')) {
      const thisThatCSS = `
  <style data-this-that-style>
  ${questionId} .answer-choice-wrapper {
      transition: opacity 0.5s ease;
  }
  </style>`;
      question.insertAdjacentHTML('beforeend', thisThatCSS);
    }

    const optionMap = {};
    const groupInfo = {};

    Object.entries(groups).forEach(([group, arr]) => {
      if (!Array.isArray(arr)) return;

      if (arr.every((v) => typeof v === 'number')) {
        groupInfo[group] = { type: 'exclusive', sets: [arr] };
        mapOptionsToGroup(arr, group, 0);
      } else if (arr.length === 2) {
        const agroup = arr[0];
        const bgroup = arr[1];
        const sets = [Array.isArray(agroup) ? agroup : [agroup], Array.isArray(bgroup) ? bgroup : [bgroup]];
        groupInfo[group] = { type: 'pair', sets };
        sets.forEach((set, idx) => mapOptionsToGroup(set, group, idx));
      } else {
        const flatArr = arr.flat();
        groupInfo[group] = { type: 'exclusive', sets: [flatArr] };
        mapOptionsToGroup(flatArr, group, 0);
      }
    });

    function mapOptionsToGroup(options, group, role) {
      options.forEach((code) => {
        if (!optionMap[code]) optionMap[code] = [];
        optionMap[code].push({ group, role });
      });
    }

    question.addEventListener('change', updateDisabled);

    function updateDisabled() {
      const checked = Object.keys(optionMap).filter((code) => {
        const input = document.querySelector(`#answer${qnum}-${code}`);
        return input && input.checked;
      });

      let hasConflict = false;
      const conflictGroups = new Set();

      checked.forEach((checkedCode) => {
        optionMap[checkedCode].forEach(({ group, role }) => {
          const info = groupInfo[group];

          if (info.type === 'exclusive') {
            const sameGroupChecked = checked.filter(
              (code) => code !== checkedCode && optionMap[code].some((x) => x.group === group)
            );
            if (sameGroupChecked.length > 0) {
              hasConflict = true;
              conflictGroups.add(group);
            }
          } else if (info.type === 'pair') {
            const agroupChecked = checked.filter((code) =>
              optionMap[code].some((x) => x.group === group && x.role === 0)
            );
            const bgroupChecked = checked.filter((code) =>
              optionMap[code].some((x) => x.group === group && x.role === 1)
            );

            if (agroupChecked.length > 0 && bgroupChecked.length > 0) {
              hasConflict = true;
              conflictGroups.add(group);
            }
          }
        });
      });

      if (hasConflict) {
        console.warn('중복 선택이 감지되어 해당 그룹의 응답을 초기화합니다.');
        resetConflictGroups(conflictGroups);
        return;
      }

      Object.keys(optionMap).forEach((code) => {
        let shouldDisable = false;

        optionMap[code].forEach(({ group, role }) => {
          const info = groupInfo[group];

          if (info.type === 'exclusive') {
            checked.forEach((checkedCode) => {
              if (checkedCode !== code && optionMap[checkedCode].some((x) => x.group === group)) {
                shouldDisable = true;
              }
            });
          } else if (info.type === 'pair') {
            checked.forEach((checkedCode) => {
              optionMap[checkedCode].forEach(({ group: checkedGroup, role: checkedRole }) => {
                if (group === checkedGroup && role !== checkedRole) {
                  shouldDisable = true;
                }
              });
            });
          }
        });

        const input = document.querySelector(`#answer${qnum}-${code}`);
        const option = input?.parentNode;
        if (input && option) {
          input.readOnly = shouldDisable;
          option.style.opacity = shouldDisable ? '0.5' : '1';
          option.style.pointerEvents = shouldDisable ? 'none' : '';
        }
      });
    }

    function resetConflictGroups(conflictGroups) {
      Object.keys(optionMap).forEach((code) => {
        const belongsToConflictGroup = optionMap[code].some(({ group }) => conflictGroups.has(group));

        if (belongsToConflictGroup) {
          const input = document.querySelector(`#answer${qnum}-${code}`);
          const option = input?.parentNode;

          if (input && option) {
            turn_off_checkbox($(option));

            input.readOnly = false;

            option.style.opacity = '1';
            option.style.pointerEvents = '';
          }
        }
      });
    }

    updateDisabled();
  } catch (e) {
    console.error('Error in thisOrThat function:', e);
  } finally {
    return true;
  }
};''',

  # validate ★
  'validate':  '''window.exec = (fn) => {
  try {
    fn();
  } catch (error) {
    console.error(error);
  } finally {
    return true;
  }
};

window.cond = (fn) => {
  try {
    return fn();
  } catch (error) {
    console.error(error);
    return true;
  }
};

window.err = (msg) => {
  alert(msg);
  return true;
};

window.softFlag = true;
window.softErr = (msg) => {
  if (window.softFlag) {
    alert(msg);
    window.softFlag = false;
    return true;
  } else {
    window.softFlag = true;
    return false;
  }
};

window.validate = (fn, target = null) => {
  const wrappedFn = () => {
    try {
      const result = fn();
      return result;
    } catch (error) {
      return false;
    }
  };

  return exec(() => {
    if (target !== null && typeof target !== 'number') {
      throw new Error('target must be a number');
    }

    let qNumber = target;
    if (qNumber === null) {
      qNumber = cur;
    }

    if (typeof fn !== 'function') {
      throw new Error('fn must be a function');
    }

    const targetQuestion = document.querySelector(`#survey${qNumber}`);
    const targetBtn = targetQuestion.querySelector('.next-btn-wrapper');
    targetBtn.removeAttribute('onclick');
    targetBtn.onclick = null;

    targetBtn.addEventListener('click', () => {
      const validateResult = wrappedFn();

      if (validateResult === true) {
        return;
      } else {
        goNext();
      }
    });
  });
};

window.hangle = (qnum = null) => {
  if (qnum === null) {
    qnum = cur;
  }

  validate(() => {
    const textAnswers = document.querySelectorAll(`#survey${qnum} input[type='text'], #survey${qnum} textarea`);
    const badAnswer = [...textAnswers].some((answer) => {
      return answer.value.match(/[ㄱ-ㅎㅏ-ㅣ]/);
    });
    if (badAnswer) {
      return err('자/모음이 입력된 답변이 있습니다.');
    }
  });

  return true;
};''',

  # replaceText
  'replaceText': '''window.replaceText = (replacements, qnum = null) => {
  try {
    if (qnum === null) {
      qnum = cur;
    }
    const question = document.querySelector(`#survey${qnum}`);
    if (!question) {
      throw new Error(`Q${qnum} is not found`);
    }

    const mainFnc = () => {
      if (typeof replacements !== 'object' || replacements === null) {
        throw new Error('replacements must be an object');
      }

      const answerEvalText = question.querySelectorAll('.answer-eval-text');
      const answerLabel = question.querySelectorAll('.answer-label');
      const description = question.querySelectorAll('.question-description');
      const allElements = [...description, ...answerEvalText, ...answerLabel];

      for (const [key, conditions] of Object.entries(replacements)) {
        const pattern = new RegExp(`{{${key}}}`, 'g');
        const baseClass = `replace-${key.toLowerCase()}`;
        let changeText = conditions;
        if (typeof conditions === 'object' && conditions !== null) {
          const pipe = Object.entries(conditions).find(([key, value]) => value === true);
          if (!pipe || pipe.length === 0) {
            changeText = 'UNDEFINED';
          } else {
            changeText = pipe[0];
          }
        } else {
          changeText = conditions;
        }

        allElements.forEach((element) => {
          const replaceBase = element.querySelectorAll(`.${baseClass}`);
          if (replaceBase.length >= 1) {
            replaceBase.forEach((base) => {
              base.innerHTML = changeText;
            });
          } else {
            const replaceSpan = document.createElement('span');
            replaceSpan.classList.add(baseClass);
            replaceSpan.innerHTML = changeText;

            element.innerHTML = element.innerHTML.replace(pattern, function () {
              return replaceSpan.outerHTML;
            });
          }
        });
      }
    };

    const originReferAnswers = window.referAnswers;
    function referAnswersWrapper(fn) {
      return function (...args) {
        const result = fn.apply(this, args);
        mainFnc();
        return result;
      };
    }

    window.referAnswers = referAnswersWrapper(window.referAnswers);
    referAnswers(qnum);
    common_align(qnum);

    const nxtBtn = document.querySelector(`#survey${qnum} .next-btn-wrapper`);
    nxtBtn.addEventListener('click', () => {
      window.referAnswers = originReferAnswers;
    });
  } catch (error) {
    console.error(error);
  } finally {
    return true;
  }
};''',

  # timer
  'holdNext': '''window.holdNext = ({ seconds = 5, qnum = null, mode = 'count' } = {}) => {
  try {
    if (qnum === null) {
      qnum = cur;
    }
    const question = document.querySelector(`#survey${qnum}`);
    if (!question) {
      throw new Error(`Q${qnum} is not found`);
    }

    const wrapper = question.querySelector('.next-btn-wrapper');
    const target = wrapper.querySelector('.next');

    if (mode === 'count') {
      const originNextText = target.textContent;
      wrapper.style.pointerEvents = 'none';
      let remainingSeconds = seconds;
      target.textContent = remainingSeconds;

      const countdownInterval = setInterval(() => {
        remainingSeconds--;
        if (remainingSeconds > 0) {
          target.textContent = remainingSeconds;
        } else {
          clearInterval(countdownInterval);
          target.textContent = originNextText;
          wrapper.style.pointerEvents = 'auto';
        }
      }, 1000);
    } else if (mode === 'alert') {
      const message = '더 자세히 확인하고 응답해 주세요.';
      wrapper.setAttribute('onclick', `alert('${message}')`);
      setTimeout(() => {
        wrapper.setAttribute('onclick', 'goNext()');
      }, seconds * 1000);
    } else if (mode === 'blur') {
      wrapper.style.pointerEvents = 'none';
      wrapper.style.opacity = '0.5';
      setTimeout(() => {
        wrapper.style.pointerEvents = 'auto';
        wrapper.style.opacity = '1';
      }, seconds * 1000);
    }
  } catch (error) {
    console.error(error);
  } finally {
    return true;
  }
};''',

  # optionPosition ★
  'optionPosition': '''const optionPosition = (baseCode, appendCodes, qnum, isNext) => {
  try {
    if (qnum === null) {
      qnum = cur;
    }
    if (baseCode === null) {
      throw new Error('baseCode is required');
    }

    if (!Array.isArray(appendCodes)) {
      appendCodes = [appendCodes];
    }

    if (isNext) {
      appendCodes = appendCodes.reverse();
    }

    appendCodes.forEach((code) => {
      const base = document.querySelector(`#answer${qnum}-${baseCode}`).parentNode;
      const target = document.querySelector(`#answer${qnum}-${code}`).parentNode;
      base.parentNode.insertBefore(target, isNext ? base.nextSibling : base);
    });
  } catch (e) {
    console.error(e);
  } finally {
    return true;
  }
};

window.nextTo = (baseCode = null, appendCodes = [], qnum = null) => {
  return optionPosition(baseCode, appendCodes, qnum, true);
};

window.beforeTo = (baseCode = null, appendCodes = [], qnum = null) => {
  return optionPosition(baseCode, appendCodes, qnum, false);
};

window.topPosition = (appendCodes = [], qnum = null) => {
  try {
    if (qnum === null) {
      qnum = cur;
    }

    if (!Array.isArray(appendCodes)) {
      appendCodes = [appendCodes];
    }

    appendCodes = appendCodes.reverse();

    const base = document.querySelector(`#survey${qnum} .answer-wrapper`);
    appendCodes.forEach((code) => {
      const target = document.querySelector(`#answer${qnum}-${code}`).parentNode;
      if (target) {
        base.insertBefore(target, base.firstChild);
      }
    });
  } catch (e) {
    console.error(e);
  } finally {
    return true;
  }
};'''
}


piping_js = '''(()=>{{
    hideOption(cur);
    showOption(cur, getAnswerSet({base}).answers.map(ans => ans.value.order));
    {extra}
    return true;
}})()'''


rv_piping_js = '''(()=>{{
    showOption(cur);
    hideOption(cur, getAnswerSet({base}).answers.map(ans => ans.value.order));
    {extra}
    return true;
}})()'''