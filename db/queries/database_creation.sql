CREATE TABLE entity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wiki_id INTEGER NOT NULL,
    name text NOT NULL
);

CREATE UNIQUE INDEX idx_entity_wiki_id
ON entity (wiki_id);

CREATE TABLE entity_associations (
    entity_id INTEGER PRIMARY KEY,
    associated_ids text NOT NULL
);

CREATE TABLE lists (
    list_id INTEGER PRIMARY KEY,
    list_name text NOT NULL
);

CREATE TABLE list_associations (
    list_id INTEGER PRIMARY KEY,
    entity_id text NOT NULL
);