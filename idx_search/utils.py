import re


def gen_sql_search_q(search_string):
    """generate sql search query based on the search string"""
    search_q = 'select * from idx_search_indexitem where '
    search_params = list()
    split_by = '|'
    if ',' in search_string:
        split_by = ','
    search_items = search_string.split(split_by)
    for item in search_items:
        search_params.append(" search_string like '%{}%'".format(item))
    split_join = split_by.replace(',', ' and ').replace('|', ' or ')
    search_q += split_join.join(search_params)
    return search_q

def gen_search_string(index_string):
    """generate  search_string for IndexItem model"""
    replace_dict = {'ि': 'ी', 'ू': 'ु',
                    'િ': 'ી', 'ૂ': 'ુ'}
    regex = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
    return regex.sub(lambda mo: replace_dict[mo.string[mo.start():mo.end()]], index_string)