import wikipedia
import urllib.parse  # to decode escaped chars from links


def assign_values(page_object):
    wiki_info = {}
    wiki_info['wiki_id'] = page_object.pageid

    # Some album titles have additional description, i.e. Ten (Pearl Jam album). Remove chars after '('
    wiki_title = page_object.title
    if '(' in wiki_title:
        cut_from = wiki_title.index('(')
        wiki_title = wiki_title[:cut_from]
    wiki_info['wiki_title'] = wiki_title

    wiki_info['wiki_url'] = page_object.url
    wiki_info['wiki_summary'] = page_object.summary
    # Cut only first sentence, i.e. to first full stop (including)
    wiki_info['wiki_resume'] = wiki_info['wiki_summary'][:wiki_info['wiki_summary'].index('.') + 1]
    wiki_info['wiki_image'] = [img for img in page_object.images
                               if ('jpg' in img or 'png' in img or 'gif' in img or 'jpeg' in img)
                               and 'en' in img and 'commons' not in img][0]

    '''
    get artist name from raw html and return it if found
    1. find relevant element
    2. perform some quite ridiculous slicing based on wikipedia's html
    3. it works though (for the time being)...
    '''
    artist = None
    raw_html = page_object.html()
    if 'album</a>&#32;by' in raw_html:
        cut_from = (raw_html[raw_html.index('album</a>&#32;by'):]).split('<a href="/wiki/')[1]
        artist = cut_from[:cut_from.index('"')]
        artist = artist.replace("_", " ")  # some artists' names appear with underscore, Ten_(Pearl_Jam_album)

    return wiki_info, artist


def get_wiki_info_by_album_name(search_term):
    try:
        wikipedia.set_lang('en')
        result = wikipedia.search(search_term, results=1)
        page_object = wikipedia.page(result[0], auto_suggest=False)

        # Actual result will often be further down the list of results,
        # i.e. we get None from first result => search for word album in further results
        if 'album' not in page_object.summary:
            results = wikipedia.search(search_term, results=8)
            for result in results:
                page_object = wikipedia.page(result, auto_suggest=True)
                if 'album' in page_object.summary:
                    break

        wiki_info, artist = assign_values(page_object)  # send page object to separate function to assign values

        return wiki_info, artist

    except:
        return None, None


def get_wiki_info_from_url(album_url):
    try:
        wikipedia.set_lang('en')

        # TODO There must be an intelligent way to get wiki object directly from url
        # Here I just slice from https://en.wikipedia.org/wiki/
        # and remove all crap like the one in this link - 'Peace_Sells..._but_Who%27s_Buying%3F'
        album_url = urllib.parse.unquote(album_url)
        album_name = album_url[album_url.index("wiki/") + 5:].replace("\\", " ").replace("_", " ")
        result = wikipedia.search(album_name, results=1)
        page_object = wikipedia.page(result, auto_suggest=False)

        wiki_info, artist = assign_values(page_object)  # send page object to separate function to assign values

        return wiki_info, artist

    except:
        return None, None
