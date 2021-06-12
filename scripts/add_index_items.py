from idx_search.models  import IndexItem
import re

temp = "મોદી સરકારના સાત વર્ષ:આર્ટિકલ 370 અને રામ મંદિરને લઈને સરકારની વાહવાહ થઈ, જોકે કોરોનાએ સિસ્ટમની પોલ છત્તી કરી; હવે તો પાડોશી પણ આંખો કાઢી રહ્યાં છે"
def run():
    for idx, word in enumerate(temp.split()):

        if len(word) > 4:
            itm = IndexItem()
            itm.index_string = word
            replace_dict = {'ि': 'ी', 'ू': 'ु',
                            'િ': 'ી', 'ૂ': 'ુ'}
            regex = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
            itm.search_string = regex.sub(lambda mo: replace_dict[mo.string[mo.start():mo.end()]], word)

            itm.path = '-'.join(temp.split()[idx:idx+3])
            itm.gatha_num = ''
            itm.page_num = 'page -' + str(idx)
            itm.book_num = 'A-01'+ str(idx)
            itm.last_update_by = 'agam'
            itm.created_by = 'agam'
            itm.save()

