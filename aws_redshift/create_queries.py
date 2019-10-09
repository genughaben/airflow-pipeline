# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS  songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"


# CREATE TABLES

# Staging Tables

staging_events_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_events (
        id             BIGINT IDENTITY(0,1)   PRIMARY KEY,
        artist         VARCHAR,
        auth           VARCHAR,
        firstName      VARCHAR,
        gender         VARCHAR(3),
        itemInSession  SMALLINT,
        lastName       VARCHAR,
        length         FLOAT,
        level          VARCHAR,
        location       VARCHAR,
        method         VARCHAR(3),
        page           VARCHAR,
        registration   FLOAT,
        sessionId      BIGINT,
        song           VARCHAR,
        status         SMALLINT,
        ts             BIGINT,
        userAgent      VARCHAR,
        userId         VARCHAR
    );
""")

# {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        id               INTEGER IDENTITY(0,1)   PRIMARY KEY,
        num_songs        INTEGER,
        artist_id        VARCHAR,
        artist_latitude  FLOAT,
        artist_longitude FLOAT,
        artist_location  VARCHAR,
        artist_name      VARCHAR,
        song_id          VARCHAR,
        title            VARCHAR,
        duration         FLOAT,
        year             SMALLINT
    );
""")

# CREATE FINAL TABLE

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
         user_id         VARCHAR       PRIMARY KEY,
         first_name      VARCHAR       NOT NULL,
         last_name       VARCHAR       NOT NULL,
         gender          VARCHAR(4),
         level           VARCHAR(20)
     ) diststyle all;
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
         song_id         VARCHAR       PRIMARY KEY,
         title           VARCHAR       NOT NULL,
         artist_id       VARCHAR       NOT NULL DISTKEY SORTKEY,
         year            SMALLINT,
         duration        FLOAT
     );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
         artist_id       VARCHAR       PRIMARY KEY,
         name            VARCHAR       NOT NULL,
         location        VARCHAR,
         latitude        FLOAT,
         longitude       FLOAT
     ) diststyle all;
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
         start_time      BIGINT        PRIMARY KEY SORTKEY,
         hour            SMALLINT      NOT NULL,
         day             SMALLINT      NOT NULL,
         week            SMALLINT      NOT NULL,
         month           SMALLINT      NOT NULL,
         year            SMALLINT      NOT NULL,
         week_day        SMALLINT       NOT NULL
     ) diststyle all;
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        id               BIGINT        IDENTITY(0,1) PRIMARY KEY,
        start_time       BIGINT        NOT NULL REFERENCES time(start_time) SORTKEY,
        user_id          VARCHAR       REFERENCES users(user_id),
        level            VARCHAR       NOT NULL,
        song_id          VARCHAR       NOT NULL REFERENCES songs(song_id) DISTKEY,
        artist_id        VARCHAR       NOT NULL REFERENCES artists(artist_id) ,
        session_id       BIGINT,
        location         VARCHAR,
        user_agent       VARCHAR
     );
""")


# QUERY LISTS

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]

