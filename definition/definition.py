#!/usr/bin/env python
# coding=utf-8
#
#  vocab_definition.py - find definitions online from more than 5 dictionaries
#  and print them in your terminal, use --help for details
#
#  Copyright (c) 2014 Shubham Chaudhary <me@shubhamchaudhary.in>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function

import sys
from optparse import OptionParser

import requests
from wordnik import WordApi
from wordnik import WordsApi
from wordnik import swagger

apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'
apiKey = '9c20e2ed369b002e580010499c40f84816050d822330fadbd'  # Get your own freaking key ! ! !

client = swagger.ApiClient(apiKey, apiUrl)


# wordapi = WordApi.WordApi(client)

def get_word_of_the_day():
    wordsapi = WordsApi.WordsApi(client)
    ret = wordsapi.getWordOfTheDay()
    out = 'Word of the day: ' + ret.word
    return out


def random_words(count=10):
    wordsapi = WordsApi.WordsApi(client)
    rns = wordsapi.getRandomWords()
    for i in range(min(len(rns), count)):
        print('%d:' % (i + 1), rns[i].word)

    return


def get_hyphenation(query):
    wordapi = WordApi.WordApi(client)
    hyphenation = wordapi.getHyphenation(query)
    if not hyphenation:
        return ''
    out = ''
    for hyphen in hyphenation:
        out += hyphen.text
        if hyphen.type:
            out += '(' + hyphen.type + ')'
        out += ' - '
    return out[:-3]


def get_pronunciation(query, send_one=0):
    wordapi = WordApi.WordApi(client)
    pro = wordapi.getTextPronunciations(query)
    if not pro:
        pro = wordapi.getTextPronunciations(query, useCanonical='true')
        if not pro:
            return ''
    if send_one:
        return pro[0].raw
    else:
        print(get_hyphenation(query))
        for p in pro:
            print(p.raw)
    return


def reverse_dictionary_search(query):
    return NotImplemented


def search_from_part_of_word(query):
    return NotImplemented


def related_words(query):
    return NotImplemented


def get_audio(query):
    return NotImplemented


def get_examples(query, limit=5):
    wordapi = WordApi.WordApi(client)
    examples = wordapi.getExamples(query, limit=limit)
    if not examples:
        examples = wordapi.getExamples(query, limit=limit, useCanonical='true')
        if not examples:
            examples = wordapi.getExamples(query, limit=limit, useCanonical='true', includeDuplicates='true')
            if not examples:
                return ''
    out = ''
    examples_list = examples.examples
    if examples_list:
        for i in range(len(examples_list)):
            out += '%d: ' % (i + 1) + examples_list[i].text + '\n'

    # XXX: Experimental
    facets_list = examples.facets
    if facets_list:
        for i in range(len(facets_list)):
            print('\n%d: ' % (i + 1) + facets_list[i].text)

    return out


def get_top_example(query):
    wordapi = WordApi.WordApi(client)
    top = wordapi.getTopExample(query)
    if not top:
        top = wordapi.getTopExample(query, useCanonical='true')
        if not top:
            return ''
    out = 'Top Example: ' + top.text
    return out


def get_definition_api(query):
    wordapi = WordApi.WordApi(client)
    print('Searching on the Internet for %s:' % query)
    definitions = wordapi.getDefinitions(query, sourceDictionaries='all', includeRelated='true', useCanonical='false',
                                         includeTags='false')
    if not definitions:
        definitions = wordapi.getDefinitions(query, sourceDictionaries='all', includeRelated='true',
                                             useCanonical='true', includeTags='false')
        if not definitions:
            print('Sorry, nothing found')
            return ''
    print(definitions[0].word, get_pronunciation(query, 1), ':')

    #     else:
    #         print 'Note: Using Canonical form of',query
    # else:
    #     print query, get_pronunciation(query,1), ':'
    previous = ''
    dic_count = 0
    for defs in definitions:
        source = defs.sourceDictionary
        if source != previous:
            source_name = source
            if source == 'gcide':
                source_name = 'GNU CIDE'  # 'GNU Collaborative International Dictionary of English'
            elif source == 'ahd-legacy':
                source_name = 'American Heritage'  # 'American Heritage Dictionary'
            elif source == 'wiktionary':
                source_name = 'Wiktionary'  # 'Wiktionary CCommons'
            elif source == 'century':
                source_name = 'Century'  # 'Century Dictionary and Cyclopedia'
            elif source == 'wordnet':
                source_name = 'WordNet'  # 'WordNet, Princeton University'
            # print '\n---->',source_name,'<----'
            dic_count += 1
            print('%d: %s -->' % (dic_count, source_name))
            previous = source
        if defs.partOfSpeech:
            print('(%s)' % defs.partOfSpeech[0], end='')
        else:
            print('( )', end='')
        print(defs.text)
        # print '(%s)'%defs.partOfSpeech[0],defs.text
        # print defs.sourceDictionary,':',defs.text
    print('\n', get_top_example(query))
    return ''


def get_definition(query):
    """Returns dictionary of id, first names of people who posted on my wall
    between start and end time"""
    try:
        return get_definition_api(query)
    except:
        raise

    # http://api.wordnik.com:80/v4/word.json/discrimination/definitions?limit=200&includeRelated=true&sourceDictionaries=all&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5
    import json
    payload = {'q': query, 'limit': 200, 'includeRelated': 'true', 'sourceDictionaries': 'all',
               'useCanonical': 'false', 'includeTags': 'false',
               'api_key': 'a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'}
    url = 'http://api.wordnik.com:80/v4/word.json/%s/definitions' % query
    r = requests.get(url, params=payload)
    result = json.loads(r.text)
    return result


def print_usage():
    print('Usage: -w -a -r -p -e')


def main(argv=sys.argv):
    usage = "%prog [-p] [-r [INT]] [-e [INT]] query"  # %sys.argv[0]
    parser = OptionParser(usage=usage, version="%prog 1.0")
    parser.add_option("-w", "--word", action="store_true", dest="wordOfDay", default=False,
                      help='Show the word of the day')
    parser.add_option("-x", "--xamples", action='store_true', dest="xamples", default=False, help="Show 30 examples")
    parser.add_option("-e", "--example", type='int', dest="example", help="Show specified number of examples")
    parser.add_option("-r", "--random", action='store_true', dest="random", help="Show random words")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")
    parser.add_option("-p", "--pronunciation", action="store_true", dest="pronunciation", default=False,
                      help='Show detailed pronunciation')

    (options, args) = parser.parse_args()

    query = ''
    if args:
        query = args[0]

    if options.wordOfDay:
        print(get_word_of_the_day())
        return

    if options.random:
        return random_words(count=10)

    if options.pronunciation:
        if not query:
            print('No query specified for pronunciation')
            query = input('Enter query: ').strip()
            if not query:
                return
        return get_pronunciation(query)

    if options.example:
        print(get_examples(query, options.example), end='')
        return

    if options.xamples:
        if not query:
            print('No query specified for examples')
            query = input('Enter query: ').strip()
            if not query:
                return
        print(get_examples(query), end='')
        return

    if query:
        return get_definition_api(query)

    parser.print_help()

    return


#     return random_words()
#     print 'Please specify the search word after %s option'%argv[1]
#     return random_words(int(argv[2]))
#     print get_examples(argv[2],int(argv[3])),
#     print_usage()

if __name__ == '__main__':
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print('\nExiting gracefully')
# except:
#         print '\nOops, Unknown Error:', sys.exc_info()[1]
#         raise
