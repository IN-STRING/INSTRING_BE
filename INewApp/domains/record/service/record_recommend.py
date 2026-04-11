from sqlalchemy.ext.asyncio import AsyncSession
from INewApp.common.utils.song_repo_class import song_repository


class RecordingRecommender:
    LEVEL_WEIGHTS = {
        0: 1.0,
        -1: 0.3,
        1: 0.5,
    }

    def __init__(self,
                 weight_technique=3.0,
                 weight_tempo=2.5,
                 weight_chord=2.0,
                 weight_popularity=1.0):
        self.song_repo = song_repository
        self.weight_technique = weight_technique
        self.weight_tempo = weight_tempo
        self.weight_chord = weight_chord
        self.weight_popularity = weight_popularity

    async def recommend(self, session: AsyncSession, user_level: int, analysis: dict, limit: int = 10) -> list[dict]:
        candidates = await self._get_candidates(session, user_level, limit)
        popularity = await self._build_popularity(session)

        scored = []
        for song, level_weight in candidates:
            base_score = self._score(song, analysis, popularity)
            final_score = base_score * level_weight
            scored.append((song, final_score))

        scored.sort(key=lambda x: x[1], reverse=True)

        return [
            {
                "song": song,
                "score": round(score, 2),
            }
            for song, score in scored[:limit]
        ]

    def _score(self, song, analysis: dict, popularity: dict) -> float:
        score = 0.0

        analysis_style = analysis.get("style")
        if song.style and analysis_style and song.style == analysis_style:
            score += self.weight_technique

        analysis_tempo = analysis.get("tempo")
        if song.speed and analysis_tempo:
            score += self._tempo_score(song.speed, analysis_tempo) * self.weight_tempo

        analysis_chords = analysis.get("chords")
        if song.chord and analysis_chords:
            score += self._chord_similarity(song.chord, analysis_chords) * self.weight_chord

        pop_score = popularity.get(song.id, 0)
        score += pop_score * self.weight_popularity

        return score

    @staticmethod
    def _tempo_score(song_tempo: str, analysis_tempo: str) -> float:
        order = {"slow": 0, "mid": 1, "fast": 2}
        diff = abs(order.get(song_tempo, 1) - order.get(analysis_tempo, 1))

        if diff == 0:
            return 1.0
        elif diff == 1:
            return 0.4
        else:
            return 0.0

    @staticmethod
    def _chord_similarity(song_chords: list, analysis_chords: list) -> float:
        if not song_chords or not analysis_chords:
            return 0.0

        bigrams_a = set(zip(song_chords, song_chords[1:]))
        bigrams_b = set(zip(analysis_chords, analysis_chords[1:]))

        if not bigrams_a or not bigrams_b:
            set_a = set(song_chords)
            set_b = set(analysis_chords)
            intersection = set_a & set_b
            union = set_a | set_b
            if not union:
                return 0.0
            return len(intersection) / len(union)

        intersection = bigrams_a & bigrams_b
        union = bigrams_a | bigrams_b

        if not union:
            return 0.0

        return len(intersection) / len(union)

    async def _get_candidates(self, session: AsyncSession, user_level: int, limit: int) -> list[tuple]:
        candidates = []
        found_song_ids = set()

        for level_diff, weight in self.LEVEL_WEIGHTS.items():
            level = user_level + level_diff

            if not (11 <= level <= 15):
                continue

            songs = await self.song_repo.get_songs_by_level(session, level)

            for song in songs:
                if song.id not in found_song_ids:
                    candidates.append((song, weight))
                    found_song_ids.add(song.id)

        if len(candidates) < limit:
            needed_count = limit - len(candidates)
            fallback_candidates = await self._fallback_search(
                session, user_level, found_song_ids, needed_count
            )
            candidates.extend(fallback_candidates)

        return candidates


    async def _fallback_search(self, session: AsyncSession, user_level: int,
                               found_song_ids: set, needed_count: int) -> list[tuple]:
        fallback = []

        for diff in [2, -2, 3, -3, 4, -4]:
            level = user_level + diff

            if not (11 <= level <= 15):
                continue

            weight = max(0.1, 1.0 - abs(diff) * 0.2)
            songs = await self.song_repo.get_songs_by_level(session, level)

            for song in songs:
                if song.id in found_song_ids:
                    continue

                fallback.append((song, weight))
                found_song_ids.add(song.id)

                if len(fallback) >= needed_count:
                    return fallback

        return fallback

    async def _build_popularity(self, session: AsyncSession) -> dict:
        all_clicks = await self.song_repo.get_all_click_counts(session)

        if not all_clicks:
            return {}

        max_clicks = max(all_clicks.values())

        if max_clicks <= 0:
            return {song_id: 0.0 for song_id in all_clicks}

        return {song_id: count / max_clicks for song_id, count in all_clicks.items()}


record_recommender = RecordingRecommender()