# -*- coding: utf-8 -*-
#########################################################################
import http.cookiejar, urllib.request, re
from ckipnlp.container import ParseClause, ParseTree

def parseTree(string):
        if not isinstance(string, str):
                try:
                        string = string.decode('utf-8')
                except:
                        raise UnicodeError('Input encoding should be UTF8 of UNICODE')
        string = string.encode('cp950')

        URL = 'http://parser.iis.sinica.edu.tw/'

        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

        opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'),
        ('referer', 'http://parser.iis.sinica.edu.tw/'),
        ('Host', 'parser.iis.sinica.edu.tw')
        ]

        raw = urllib.request.urlopen(URL).read()
        fid = re.search(rb'name="id" value="(\d+)"', raw).group(1)

        postdata = dict()
        postdata['myTag'] = string
        postdata['id'] = fid

        postdata = urllib.parse.urlencode(postdata)
        postdata = postdata.encode('utf-8')
        resURL = 'http://parser.iis.sinica.edu.tw/svr/webparser.asp'

        res = opener.open(resURL, postdata).read()
        res = res.decode('cp950')
        res = re.findall('<nobr>#\d+:(.*?)</nobr>', res)
        return res


if __name__ == '__main__':
    sent = ""
    while not sent :
        sent = input("請輸入句子:")
    res = parseTree(sent)    ## input your test string e.g 我和食物真的都很不開心
    result = res[0].encode('utf-8').decode('utf8')
    result = result.split()[1].replace("#", "")
    print (result)



    ##### to tree

    clause = ParseClause(result)

    tree = clause.to_tree()

    print('Show Tree')
    tree.show()

    print('Get Heads of {}'.format(tree[5]))
    print('-- Semantic --')
    for head in tree.get_heads(5, semantic=True): print(repr(head))
    print('-- Syntactic --')
    for head in tree.get_heads(5, semantic=False): print(repr(head))
    print()

    print('Get Relations of {}'.format(tree[0]))
    print('-- Semantic --')
    for rel in tree.get_relations(0, semantic=True): print(repr(rel))
    print('-- Syntactic --')
    for rel in tree.get_relations(0, semantic=False): print(repr(rel))
    print()
    print('Get get_subjects of {}'.format(tree[0]))
    print('-- Semantic --')
    for subject in tree.get_subjects(0, semantic=True): print(repr(subject))
    print('-- Syntactic --')
    for subject in tree.get_subjects(0, semantic=False): print(repr(subject))
    print()




