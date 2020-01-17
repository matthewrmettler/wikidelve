SELECT entity.* FROM entity
LEFT OUTER JOIN entity_associations
    ON entity.id = entity_associations.entity_id
WHERE entity_associations.associated_ids IS NULL
ORDER BY entity.id ASC
LIMIT 10;