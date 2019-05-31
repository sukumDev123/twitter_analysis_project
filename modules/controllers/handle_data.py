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

