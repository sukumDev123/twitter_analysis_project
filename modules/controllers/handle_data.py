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
        'reply_to': [],
        "retweet_c": [],
        'geo': [],
        'hashtags': []
    }
    for jj in range(size):
        user = datas[jj]['user']
        description = user['description']
        screen_name = user['screen_name']
        entities = datas[jj]['entities']
        hashtags_ = entities['hashtags']
        if len(hashtags_) != 0:
            tempp['hashtags'].append([hash for hash in hashtags_])
        else:
            tempp['hashtags'].append(None)
        in_reply_to_screen_name = datas[jj]['in_reply_to_screen_name']
        retweet_count = datas[jj]['retweet_count']
        geo = datas[jj]['geo']
        tempp['reply_to'].append(in_reply_to_screen_name)
        tempp['retweet_c'].append(retweet_count)
        tempp['geo'].append(geo)
        tempp['id'].append(datas[jj]['id'])
        tempp['text'].append(datas[jj]['text'])
    return tempp