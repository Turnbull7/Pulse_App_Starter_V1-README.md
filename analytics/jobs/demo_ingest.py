
import pandas as pd
from sqlalchemy import create_engine

DB_URL = "sqlite:///../backend/pulse.db"
engine = create_engine(DB_URL)

def run():
    try:
        events = pd.read_sql("SELECT type, created_at FROM events", engine, parse_dates=['created_at'])
    except Exception:
        print("No events or database not initialized yet.")
        return

    if events.empty:
        print("No events yet.")
        return

    events['hour'] = events['created_at'].dt.floor('H')
    counts = events.groupby(['hour', 'type']).size().reset_index(name='count')

    with engine.begin() as conn:
        for _, row in counts.iterrows():
            conn.execute(
                """
                INSERT INTO trend_signals (segment, metric, value, sample_size, generated_at)
                VALUES (:segment, :metric, :value, :sample_size, :generated_at)
                """,
                dict(
                    segment="ALL_USERS",
                    metric=f"{row['type']}_per_hour",
                    value=float(row['count']),
                    sample_size=int(row['count']),
                    generated_at=row['hour'].to_pydatetime()
                )
            )
    print("Trend signals updated.")

if __name__ == "__main__":
    run()
