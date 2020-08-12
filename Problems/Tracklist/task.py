def tracklist(**tracks):
    for key in tracks:
        print(key)
        for key_, value_ in tracks[key].items():
            print(f'ALBUM: {key_} TRACK: {value_}')
