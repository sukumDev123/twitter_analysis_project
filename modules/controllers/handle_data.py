from modules.controllers.analysis_text import text_cut_word
handle_data_direct = lambda ids_, created_ats, texts, sources, favorite_counts, langs: {
    "id": ids_,
    "created_at": created_ats,
    "text": texts,
    "source": sources,
    'lang': langs,
    'favorite_count': favorite_counts
}

handle_tweets_data = lambda created_ats, ids, sources, texts, langs, favorite_counts, retweet_count, geos, hashtag: {
    "id": ids,
    "created_at": created_ats,
    "text": texts,
    "lang": langs,
    "source": sources,
    "favorite_count": favorite_counts,
    "retweet_count": retweet_count,
    "geo": geos,
    'hashtag': hashtag
}


def handle_user_timeline_data(datas):
    size = len(datas)
    tempp = {
        "id": [],
        "text": [],
        "name": [],
        'created_at': [],
        'likes': [],
        'retweets': [],
        'screen_name': [],
        'location': []
    }
    for jj in range(size):

        retweet_count = datas[jj]['retweet_count']
        print("==================\n")
        print("TT : ", datas[jj]['text'])
        print("TT : ", datas[jj]['user'])

        print("EE : ", datas[jj]['favorite_count'])
        print("lang : ", datas[jj]['lang'])
        print("==================\n")
        # tempp['replies'].append(datas[jj]['reply_count'])
        tempp['retweets'].append(retweet_count)
        # tempp['geo'].append(geo)
        tempp['likes'].append(datas[jj]['favorite_count'])
        tempp['id'].append(datas[jj]['id'])
        tempp['text'].append((datas[jj]['text']))
        tempp['created_at'].append(datas[jj]['created_at'])
        tempp['screen_name'].append(datas[jj]['user']['screen_name'])
        tempp['name'].append(datas[jj]['user']['name'])
        tempp['location'].append(datas[jj]['user']['location'])
    return tempp