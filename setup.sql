-- Supprime les tables existantes (si elles existent déjà)
DROP TABLE IF EXISTS vins;
DROP TABLE IF EXISTS appellations;

-- Création de la table appellations
CREATE TABLE appellations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    region TEXT NOT NULL,
    pays TEXT NOT NULL,
    met1 TEXT,
    met2 TEXT,
    met3 TEXT,
    met4 TEXT,
    met5 TEXT
);

-- Création de la table vins
CREATE TABLE vins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    appellation_id INTEGER NOT NULL,
    couleur TEXT NOT NULL,
    nb_bouteilles INTEGER NOT NULL,
    FOREIGN KEY (appellation_id) REFERENCES appellations(id)
);
