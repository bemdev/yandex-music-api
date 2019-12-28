from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from yandex_music import Client, Artist, Track

from yandex_music import YandexMusicObject


class ArtistEvent(YandexMusicObject):
    def __init__(self,
                 artist: Optional['Artist'],
                 tracks: List['Track'],
                 similar_to_artists_from_history: List['Artist'],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.artist = artist
        self.tracks = tracks
        self.similar_to_artists_from_history = similar_to_artists_from_history

        self.client = client
        self._id_attrs = (self.artist, self.tracks, self.similar_to_artists_from_history)

    @classmethod
    def de_json(cls, data: dict, client: 'Client') -> Optional['ArtistEvent']:
        if not data:
            return None

        data = super(ArtistEvent, cls).de_json(data, client)
        from yandex_music import Artist, Track
        data['artist'] = Artist.de_json(data.get('artist'), client)
        data['tracks'] = Track.de_list(data.get('tracks'), client)
        data['similar_to_artists_from_history'] = Artist.de_list(data.get('similar_to_artists_from_history'), client)

        return cls(client=client, **data)

    @classmethod
    def de_list(cls, data: dict, client: 'Client') -> List['ArtistEvent']:
        if not data:
            return []

        artist_events = list()
        for artist_event in data:
            artist_events.append(cls.de_json(artist_event, client))

        return artist_events
