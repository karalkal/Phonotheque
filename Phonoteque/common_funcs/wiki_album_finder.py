import wikipedia


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
    wiki_info['wiki_summary'] = wikipedia.summary(page_object.title, sentences=1)  # + "[... text continued]"
    wiki_info['wiki_image'] = [img for img in page_object.images
                               if ('jpg' in img or 'png' in img or 'gif' in img or 'jpeg' in img)
                               and 'en' in img and 'commons' not in img][0]
    # wiki_info['wiki_html'] = page_object.html
    return wiki_info


def get_wiki_info(search_term):
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

        wiki_info = assign_values(page_object)
        return wiki_info

    except:
        return 0
