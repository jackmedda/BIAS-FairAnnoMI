import os
import re
import json


_PROPERTIES_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir, 'properties'
)
_CONTRACTION_MAP_FILEPATH = os.path.join(_PROPERTIES_PATH, 'contraction_map.json')
_MANUAL_CONTRACTION_MAP_FILEPATH = os.path.join(_PROPERTIES_PATH, 'contraction_map.json')

with open(_CONTRACTION_MAP_FILEPATH, 'r') as contr_map_file:
    CONTRACTION_MAP = json.load(contr_map_file)
with open(_MANUAL_CONTRACTION_MAP_FILEPATH, 'r') as manual_contr_map_file:
    MANUAL_CONTRACTION_MAP = json.load(manual_contr_map_file)


def __replace__substr(string, dict_items_iter):
    try:
        key_value = next(dict_items_iter)
        return __replace__substr(string.replace(*key_value), dict_items_iter)
    except StopIteration:
        return string


def replace_substr(string, dict_items_iter):
    return __replace__substr(string, dict_items_iter.items().__iter__())


def replace_substr_column_dataframe(df, col, mapping=None, inplace=False):
    mapping = {**CONTRACTION_MAP, **MANUAL_CONTRACTION_MAP} if mapping is None else mapping
    if isinstance(mapping, dict):
        df = df if inplace else df.copy()
        df[col] = df[col].apply(lambda x: replace_substr(x, mapping))
    else:
        raise NotImplementedError("`mapping` should be a dictionary in the form {to_replace_value: new_value}")

    if not inplace:
        return df


def clean_utterance_text(df, col, inplace=False):
    df = df if inplace else df.copy()
    df[col] = df[col].str.replace('-', ' ').str.strip()

    # removes the pattern `[unintelligible HH:MM:SS]` from the utterance text
    def unintelligible_check(string):
        start_sentence_pattern = r'\[unintelligible.*\] +'
        mid_end_sentence_pattern = r' +\[unintelligible.*\]'
        if re.search(mid_end_sentence_pattern, string):
            return re.sub(mid_end_sentence_pattern, '', string)
        elif re.search(start_sentence_pattern, string):
            return re.sub(start_sentence_pattern, '', string)

        return string

    def remove_multiple_spaces(string):
        return re.sub(r'\s{2,}', ' ', string)

    df[col] = df[col].map(unintelligible_check).map(remove_multiple_spaces)

    if not inplace:
        return df
