# services/search.py
from sqlalchemy import text
from sqlmodel import Session

def search_records(session: Session, query: str, user_id: int = None, limit: int = 20):
    sql = text("""
        SELECT 
            id, name, style, chord, speed, user_id,
            ts_rank(search_vector, websearch_to_tsquery('simple', :query)) AS fts_score,
            similarity(name, :query) AS trgm_score
        FROM userrecord
        WHERE 
            (search_vector @@ websearch_to_tsquery('simple', :query)
             OR similarity(name, :query) > 0.15)
            AND (:user_id IS NULL OR user_id = :user_id)
        ORDER BY (ts_rank(search_vector, websearch_to_tsquery('simple', :query)) * 2 
                  + similarity(name, :query)) DESC
        LIMIT :limit
    """)

    result = session.exec(sql, params={"query": query, "user_id": user_id, "limit": limit}).all()
    return result