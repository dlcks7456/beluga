from typing import Union, Optional
import re
from .errors import BelugaParsingError

class OptionAttribute :
    def __init__(self,
                 label: str,
                 value: int,
                 is_etc: bool = False,
                 is_na: bool = False) :
        self.label: str = label
        self.value: int = value
        self.is_etc: bool = is_etc
        self.is_na: bool = is_na

class BelugaQuestion :
    def __init__(self,
                type: str,
                qid: str,
                qnum: int,
                title: str,
                options: str = None,
                cond: Union[list[str], str] = None,
                min: int = None,
                max: int = None,
                rotation: bool = False,
                fail: bool = False,
                post_logic: Optional[str] = None,
                etc: bool = False,
                etc_text: Optional[str] = None,
                na: Optional[str] = None,
                piping: Union[str, int, 'BelugaQuestion'] = None,
                selected_piping: bool = True,
                post_text: str = ''):
        self.type: str = type
        self.qid: str = qid
        self.qnum: int = qnum
        self.title: str = title
        if options is not None :
            try:
                parsed_options = self.parse_options(options)
            except Exception as e:
                raise BelugaParsingError(f"선택지 파싱 실패: {e}")
            self.option_list: list[OptionAttribute] = list(parsed_options.values())
            self.options = {attr.value: attr.label for attr in self.option_list if not attr.is_etc and not attr.is_na}
        else :
            self.option_list: None
            self.options = {}
        self.cond: Union[list[str], str] = cond
        self.min: int = min
        self.max: int = max
        self.rotation: bool = rotation
        self.fail: bool = fail
        self.post_logic: str = post_logic
        self.etc: bool = etc
        self.etc_text: str = etc_text
        self.na: str = na
        self.piping: Union[str, int, 'BelugaQuestion'] = piping
        self.selected_piping: bool = selected_piping
        self.post_text = post_text

    def parse_options(self, options: str) -> dict:
        options_list = options.split('\n')
        options_list = [option.strip() for option in options_list]
        parsed_options = {}
        for option in options_list:
            match = re.match(r'^(\d+[A-Z]*)\)', option)
            if match:
                number = match.group(1)
                text = option[match.end():].strip()
                if number.isdigit() :
                    attr_name = f'A{number}'
                    setattr(self, attr_name, OptionAttribute(label=text, value=int(number), is_etc=False, is_na=True if int(number) == 0 else False))
                    parsed_options[attr_name] = getattr(self, attr_name)
                else :
                    if 'E' in number :
                        etc_value = number.replace('E', '')
                        attr_name = f'A{etc_value}'
                        setattr(self, attr_name, OptionAttribute(label=text, value=int(etc_value), is_etc=True, is_na=False))
                        parsed_options[attr_name] = getattr(self, attr_name)
        return parsed_options

