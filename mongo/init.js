db = db.getSiblingDB('stablishments');

db.createCollection('stablishments');
db.createCollection('blockchain');

db.stablishments.createIndex({ coordinates: "2dsphere" });
