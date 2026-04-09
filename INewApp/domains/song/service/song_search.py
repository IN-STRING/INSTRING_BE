from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def search_songs(session: AsyncSession, query: str, limit: int = 20):
    sql = text("""
               SELECT id, level_id, name, artist, style,
                      -- FTS 점수
                      ts_rank(search_vector, websearch_to_tsquery('simple', :query)) AS fts_score,
                      -- trigram 유사도 (이름 + 아티스트 중 높은 쪽)
                      GREATEST(similarity(name, :query), similarity(artist, :query)) AS trgm_score
               FROM song
               WHERE search_vector @@ websearch_to_tsquery('simple', :query) -- FTS 매칭
                  OR similarity(name, :query)> 0.15    -- 오타 허용
                  OR similarity(artist, :query)> 0.15
               ORDER BY
                   (ts_rank(search_vector, websearch_to_tsquery('simple', :query)) * 2
                   + GREATEST(similarity(name, :query), similarity(artist, :query))) DESC
                   LIMIT :limit
               """)

    results = await session.execute(sql, {"query": query, "limit": limit})
    return results.all()