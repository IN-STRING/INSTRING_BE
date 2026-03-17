from app.services.song_repo.song_repo_class import song_repository

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

    def recommend(self, session, user_level: int, analysis: dict, limit: int = 10) -> list[dict]:
        candidates = self._get_candidates(session, user_level)
        popularity = self._build_popularity(session)

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

        # 주법 일치
        if song.style == analysis["style"]:
            score += self.weight_technique

        # 템포 일치 or 근접
        score += self._tempo_score(song.speed, analysis["tempo"]) * self.weight_tempo

        # 코드 유사도
        score += self._chord_similarity(song.chord, analysis["chords"]) * self.weight_chord

        # 인기도
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

        # 바이그램이 없으면 코드 1개짜리 단순 집합 비교
        if not bigrams_a or not bigrams_b:
            set_a = set(song_chords)
            set_b = set(analysis_chords)
            intersection = set_a & set_b
            union = set_a | set_b
            return len(intersection) / len(union)

        intersection = bigrams_a & bigrams_b
        union = bigrams_a | bigrams_b

        return len(intersection) / len(union)

    def _get_candidates(self, session, user_level: int) -> list[tuple]:
        candidates = []

        for level_diff, weight in self.LEVEL_WEIGHTS.items():
            level = user_level + level_diff

            if not (11 <= level <= 15):
                continue

            songs = self.song_repo.get_songs_by_level(session, level)

            for song in songs:
                candidates.append((song, weight))

        if not candidates:
            candidates = self._fallback_search(session, user_level)

        return candidates

    def _fallback_search(self, session, user_level: int) -> list[tuple]:
        fallback = []

        for diff in [2, -2, 3, -3, 4, -4]:
            level = user_level + diff

            if not (11 <= level <= 15):
                continue

            weight = max(0.1, 1.0 - abs(diff) * 0.2)
            songs = self.song_repo.get_songs_by_level(session, level)

            for song in songs:
                fallback.append((song, weight))

            if len(fallback) >= 5:
                break

        return fallback

    def _build_popularity(self, session) -> dict:
        all_clicks = self.song_repo.get_all_click_counts(session)

        if not all_clicks:
            return {}

        max_clicks = max(all_clicks.values())
        return {song_id: count / max_clicks for song_id, count in all_clicks.items()}


record_recommender = RecordingRecommender()