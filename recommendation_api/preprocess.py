"""preparations for slack text messages
    ref: https://github.com/sota0121/nlpslack/blob/master/nlpslack/preprocessing.py
"""

import re
import urllib.request
from pathlib import Path


# -------------------------------------------------
# cleaning
# - Return and Space : regex >> "\s"
# - url link (<https://...>): regex >> "(<)http.+(>)"
# - reaction (:grin:) : regex >> "(:).+\w(:)"
# - html kw (&lt;, 	&gt;, &amp;, &nbsp;, &ensp;, &emsp;, &ndash;, &mdash;) : regex >> "(&).+?\w(;)"
# - mention (<@XXXXXX>) : regex >> "(<)@.+\w(>)"
# - inline code block : regex >> "(`).+(`)"
# - multi lines code block : regex >> "(```).+(```)"
# -------------------------------------------------
def clean_msg(msg: str) -> str:
    if 'チャンネルに参加しました' in msg:
        return ''
    # sub 'Return and Space'
    result = re.sub(r'\s', '', msg)
    # sub 'url link'
    result = re.sub(r'(<)http.+(>)', '', result)
    # sub 'mention'
    result = re.sub(r'(<)@.+\w(>)', '', result)
    # sub 'reaction'
    result = re.sub(r'(:).+\w(:)', '', result)
    # sub 'html key words'
    result = re.sub(r'(&).+?\w(;)', '', result)
    # sub 'multi lines code block'
    result = re.sub(r'(```).+(```)', '', result)
    # sub 'inline code block'
    result = re.sub(r'(`).+(`)', '', result)
    return result


# -------------------------------------------------
# normalization
# -------------------------------------------------
def normarize_text(text: str):
    normalized_text = normalize_number(text)
    normalized_text = lower_text(normalized_text)
    return normalized_text


def normalize_number(text: str) -> str:
    """
    pattern = r'\d+'
    replacer = re.compile(pattern)
    result = replacer.sub('0', text)
    """
    # 連続した数字を0で置換
    replaced_text = re.sub(r'\d+', '0', text)
    return replaced_text


def lower_text(text: str) -> str:
    return text.lower()


# -------------------------------------------------
# stopword removal
# -------------------------------------------------
def maybe_download(path: str):
    stopword_def_page_url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    p = Path(path)
    if p.exists():
        print('File already exists.')
    else:
        print('downloading stop words definition ...')
        # Download the file from `url` and save it locally under `file_name`:
        urllib.request.urlretrieve(stopword_def_page_url, path)
    # stop word 追加分
    sw_added_list = ['-', 'ー', 'w', 'm', '笑', 'nan']
    sw_added_str = '\n'.join(sw_added_list)
    with open(path, 'a') as f:
        print(sw_added_str, file=f)


def load_sw_definition(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read()
        line_list = lines.split('\n')
        line_list = [x for x in line_list if x != '']
    return line_list


def remove_sw_from_text(wktstr: str, stopwords: list) -> str:
    words_list = wktstr.split(' ')
    words_list_swrm = [x for x in words_list if x not in stopwords]
    swremoved_str = ' '.join(words_list_swrm)
    return swremoved_str
