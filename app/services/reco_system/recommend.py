from collections import Counter
from sqlmodel import Session
from app.models.postgresDB.song import Song
from app.models.postgresDB.song_user_clicked_link import SongUserClickedLink
from app.services.song_repo.song_repo_class import song_repository

class SongRecommender:

    LEVEL_WEIGHTS = {
        0: 1.0,
        -1: 0.3,
        1: 0.5,
    }

    def __init__(self,
                 weight_technique=3.0,
                 weight_tempo=2.0,
                 weight_chord=1.0,
                 weight_similarity=2.5,
                 weight_preference=2.0,
                 weight_popularity=1.5):

        self.song_repo = song_repository
        self.weight_technique = weight_technique
        self.weight_tempo = weight_tempo
        self.weight_chord = weight_chord
        self.weight_similarity = weight_similarity
        self.weight_preference = weight_preference
        self.weight_popularity = weight_popularity


    def recommend(self, session: Session, user_level: int, user_history: list[int],
                  user_clicks: list[SongUserClickedLink], limit: int = 10) -> list[dict]:

        history_songs = self.song_repo.get_song_by_ids(session, user_history)
        #print("\n와우1",history_songs)
        preference = self._build_preference(session, user_clicks)
        #print("\n와우2",preference)
        popularity = self._build_popularity(session)
        #print("\n와우3",popularity)
        level_of_songs = self._get_song_by_level(session, user_level, user_history)
        #print("\n와우4",level_of_songs)
        scored_songs = []
        for song, level_weight in level_of_songs:
            base_score = self._score(song, history_songs, preference, popularity)
            final_score = base_score * level_weight
            scored_songs .append((song, final_score))
        #print("\n와우5",score)
        scored_songs .sort(key=lambda x: x[1], reverse=True)

        return [
            {
                "song": song,
                "score": round(score_song, 2),
            }
            for song, score_song in scored_songs [:limit]
        ]


    def _score(self, song: Song, history_songs: list[Song],
               preference: dict, popularity: dict):

        if not history_songs and not preference["techniques"]:
            return 1.0

        score = 0.0

        played_style = {s.style for s in history_songs}
        if song.style not in played_style:
            score += self.weight_technique

        played_speed = {s.speed for s in history_songs}
        if song.speed not in played_speed:
            score += self.weight_tempo

        played_chords = set()
        for s in history_songs:
            played_chords.update(s.chord)
        new_chords = set(song.chord) - played_chords
        score += len(new_chords) * self.weight_chord

        if history_songs:
            recent = history_songs[-3:]
            similarity = max(self._chord_similarity(song, s) for s in recent)
            score += similarity * self.weight_similarity

        pref_score = (
              preference["techniques"].get(song.style, 0)
              + preference["tempos"].get(song.speed, 0)
              + preference["artists"].get(song.artist, 0)
        ) / 3
        score += pref_score * self.weight_preference

        pop_score = popularity.get(song.id, 0)
        score += pop_score * self.weight_popularity

        return score


    def _build_preference(self, session: Session ,user_clicks: list[SongUserClickedLink]):
        if not user_clicks:
            return {"techniques": {}, "tempos": {}, "artists": {}}

        clicked_songs = self.song_repo.get_song_by_ids(
            session, [song.song_id for song in user_clicks]
        )
        clicked_map = {song.song_id: song.click_count for song in user_clicks}

        technique_counts = Counter()
        tempo_counts = Counter()
        artist_counts = Counter()

        for song in clicked_songs:
            count = clicked_map.get(song.id, 1)
            artist_counts[song.artist] += count
            tempo_counts[song.speed] += count
            technique_counts[song.style] += count

        return {
            "techniques": self._normalize(technique_counts),
            "tempos": self._normalize(tempo_counts),
            "artists": self._normalize(artist_counts),
        }


    def _build_popularity(self, session: Session):
        all_clicks = self.song_repo.get_all_click_counts(session)

        if not all_clicks:
            return {}

        max_clicks = max(all_clicks.values())

        if max_clicks <= 0:
            return {song_id: 0.0 for song_id in all_clicks}

        return {
            song_id: count / max_clicks
            for song_id, count in all_clicks.items()
        }


    def _get_song_by_level(self, session: Session, user_level: int, user_history: list[int]):
        song_level_weighted_list = []
        for level_diff, weight in self.LEVEL_WEIGHTS.items():
            level = user_level + level_diff
            #print("레벨 와우",level)
            if not (11 <= level <= 15): # db 값 적제 문제 때문에 pk값 증가 되서 저래된겨
                continue

            songs = self.song_repo.get_songs_by_level(session, level)
            #print("check 와우", songs)
            for song in songs:
                if song.id not in user_history:
                    song_level_weighted_list.append((song, weight))

        if not song_level_weighted_list:
            song_level_weighted_list = self._fallback_search(session, user_level, user_history)
        #print(song_level_weighted_list)

        return song_level_weighted_list


    def _fallback_search(self, session: Session, user_level: int, user_history: list[int]):
        fallback = []

        for diff in [2, -2, 3, -3, 4, -4]:
            level = user_level + diff

            if not (11 <= level <= 15):
                continue

            # 멀어질수록 가중치 낮게
            weight = max(0.1, 1.0 - abs(diff) * 0.2)

            songs = self.song_repo.get_songs_by_level(session, level)
            #print("ㅅㅂ", diff, songs)
            for song in songs:
                if song.id not in user_history:
                    fallback.append((song, weight))

            if len(fallback) >= 12:
                break

        return fallback


    @staticmethod
    def _chord_similarity(song_a: Song, song_b: Song):
        if not song_a.chord or not song_b.chord:
            return 0.0

        chord_a = set(zip(song_a.chord, song_a.chord[1:]))
        chord_b = set(zip(song_b.chord, song_b.chord[1:]))

        intersection = chord_a & chord_b
        union = chord_a | chord_b

        if not union:
            return 0.0

        return len(intersection) / len(union)


    @staticmethod
    def _normalize(counter: Counter):
        if not counter:
            return {}
        max_val = max(counter.values())
        if max_val <= 0:
            return {k: 0.0 for k in counter}
        return {k: v / max_val for k, v in counter.items()}


song_recommender = SongRecommender()