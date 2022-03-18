DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS voiture;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS nbr_portes;
DROP TABLE IF EXISTS nbr_places;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS type_voiture;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS carburant;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS marque;


/*
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT,
    email VARCHAR(255),
    username VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif tinyint(1),
    pseudo VARCHAR(255),    -- utile ?

    -- token_email VARCHAR(255), --validation et mdp oubliÃ©
    -- token_email_date date(),

    -- go_auth_token VARCHAR(255),
    -- go_username_token VARCHAR(255),

    PRIMARY KEY(id)
);*/

CREATE TABLE IF NOT EXISTS marque(
   id_marque INT AUTO_INCREMENT,
   libelle_marque VARCHAR(50),
   PRIMARY KEY(id_marque)
);

CREATE TABLE IF NOT EXISTS couleur(
   id_couleur INT AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   PRIMARY KEY(id_couleur)
);

CREATE TABLE IF NOT EXISTS carburant(
   id_carburant INT AUTO_INCREMENT,
   libelle_carburant VARCHAR(50),
   PRIMARY KEY(id_carburant)
);

CREATE TABLE IF NOT EXISTS user(
   user_id INT AUTO_INCREMENT,
   username VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   est_actif tinyint(1),
   email VARCHAR(255),
   PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS type_voiture(
   id_type_voiture INT AUTO_INCREMENT,
   libelle_type_voiture VARCHAR(50),
   PRIMARY KEY(id_type_voiture)
);

CREATE TABLE IF NOT EXISTS etat(
   id_etat INT NOT NULL AUTO_INCREMENT,
   libelle_etat VARCHAR(255),
   PRIMARY KEY(id_etat)
);

CREATE TABLE IF NOT EXISTS nbr_places(
   id_nbr_places INT AUTO_INCREMENT,
   nombre_de_places INT NOT NULL,
   PRIMARY KEY(id_nbr_places)
);

CREATE TABLE IF NOT EXISTS nbr_portes(
   id_nbr_portes INT AUTO_INCREMENT,
   nombre_de_portes INT NOT NULL,
   PRIMARY KEY(id_nbr_portes)
);

CREATE TABLE IF NOT EXISTS modele(
    id_modele INT AUTO_INCREMENT,
    libelle_modele VARCHAR(255),
    PRIMARY KEY(id_modele)
);

CREATE TABLE IF NOT EXISTS voiture(
   id_voiture INT AUTO_INCREMENT,
   prix_unit_voiture NUMERIC(10,2),
   description TEXT,
   image_voiture VARCHAR(255),
   id_type_voiture INT NOT NULL,
   id_carburant INT NOT NULL,
   id_nbr_places INT NOT NULL,
   id_nbr_portes INT NOT NULL,
   id_modele INT NOT NULL,
   id_couleur INT NOT NULL,
   id_marque INT NOT NULL,
   stock_voiture INT,
   PRIMARY KEY(id_voiture),
   CONSTRAINT fk_voiture_type_voiture
   FOREIGN KEY(id_type_voiture) REFERENCES type_voiture(id_type_voiture),
   CONSTRAINT fk_voiture_carburant
   FOREIGN KEY(id_carburant) REFERENCES carburant(id_carburant),
   CONSTRAINT fk_voiture_nbr_places
   FOREIGN KEY(id_nbr_places) REFERENCES nbr_places(id_nbr_places),
   CONSTRAINT fk_voiture_nbr_portes
   FOREIGN KEY(id_nbr_portes) REFERENCES nbr_portes(id_nbr_portes),
   CONSTRAINT fk_voiture_modele
   FOREIGN KEY(id_modele) REFERENCES modele(id_modele),
   CONSTRAINT fk_voiture_couleur
   FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur),
   CONSTRAINT fk_voiture_marque
   FOREIGN KEY(id_marque) REFERENCES marque(id_marque)
);

CREATE TABLE IF NOT EXISTS commande(
   id_commande INT AUTO_INCREMENT,
   date_achat DATETIME,
   user_id INT NOT NULL,
   id_etat INT NOT NULL,
   PRIMARY KEY(id_commande),
   CONSTRAINT fk_commande_user
   FOREIGN KEY(user_id) REFERENCES user(user_id),
   CONSTRAINT fk_commande_etat
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat)
);

CREATE TABLE IF NOT EXISTS panier(
   id_panier INT AUTO_INCREMENT,
   date_ajout DATE,
   prix_unit NUMERIC(10,2),
   quantite INT,
   user_id INT NOT NULL,
   id_voiture INT NOT NULL,
   PRIMARY KEY(id_panier),
   CONSTRAINT fk_panier_user
   FOREIGN KEY(user_id) REFERENCES user(user_id),
   CONSTRAINT fk_panier_voiture
   FOREIGN KEY(id_voiture) REFERENCES voiture(id_voiture)
);

CREATE TABLE IF NOT EXISTS ligne_commande(
   id_ligne_commande INT AUTO_INCREMENT,
   id_voiture INT,
   id_commande INT,
   prix_unit NUMERIC(10,2),
   quantite INT,
   PRIMARY KEY(id_ligne_commande),
   CONSTRAINT fk_ligne_commande_voiture
   FOREIGN KEY(id_voiture) REFERENCES voiture(id_voiture),
   CONSTRAINT fk_ligne_commande_commande
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);

INSERT INTO user (user_id, email, username, password, role,  est_actif) VALUES
(null, 'admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1);
INSERT INTO user  (user_id, email, username, password, role,  est_actif) VALUES
(null, 'client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client',   1);
INSERT INTO user  (user_id, email, username, password, role, est_actif) VALUES
(null, 'client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client',   1);


INSERT INTO type_voiture(id_type_voiture, libelle_type_voiture) VALUES
(NULL, 'Coupé'),
(NULL, 'Berline'),
(NULL, 'Hayon'),
(NULL, 'Break'),
(NULL, 'Limousine'),
(NULL, 'Pick-up'),
(NULL, 'Crossover'),
(NULL, 'SUV'),
(NULL, 'Fourgonnette'),
(NULL, 'Mini-fourgonnette'),
(NULL, 'Liftback'),
(NULL, 'Cabriolet'),
(NULL, 'Minibus'),
(NULL, 'Roadster'),
(NULL, 'Targa');

INSERT INTO carburant(id_carburant, libelle_carburant) VALUES
(NULL, 'Diesel'),
(NULL, 'Essence'),
(NULL, 'Carburants gazeux'),
(NULL, 'Electrique');

INSERT INTO nbr_places(id_nbr_places, nombre_de_places) VALUES
(NULL, '1'),
(NULL, '2'),
(NULL, '3'),
(NULL, '4'),
(NULL, '5'),
(NULL, '6'),
(NULL, '7'),
(NULL, '8'),
(NULL, '9'),
(NULL, '10');

INSERT INTO nbr_portes(id_nbr_portes, nombre_de_portes) VALUES
(NULL, '3'),
(NULL, '5');

INSERT INTO modele(id_modele, libelle_modele) VALUES
(NULL, 'E63 W212'),
(NULL, 'Ford Mustang'),
(NULL, 'M5'),
(NULL, 'G63 6x6'),
(NULL, '2008'),
(NULL, 'RS7');







INSERT INTO couleur(id_couleur, libelle_couleur) VALUES
(NULL, 'Orange'),
(NULL, 'Rouge'),
(NULL, 'Brun'),
(NULL, 'Bleu'),
(NULL, 'Vert'),
(NULL, 'Jaune'),
(NULL, 'Violet'),
(NULL, 'Rose'),
(NULL, 'Gris'),
(NULL, 'Noir'),
(NULL, 'Blanc');

INSERT INTO marque(id_marque, libelle_marque) VALUES
(NULL, 'Peugeot'),
(NULL, 'Renaud'),
(NULL, 'Citroën'),
(NULL, 'Toyota'),
(NULL, 'Mercedes-Benz'),
(NULL, 'BMW'),
(NULL, 'Honda'),
(NULL, 'Hyundai'),
(NULL, 'Tesla'),
(NULL, 'Ford'),
(NULL, 'Audi'),
(NULL, 'Volkswagen'),
(NULL, 'Porsche'),
(NULL, 'Nissan'),
(NULL, 'Ferrari'),
(NULL, 'Kia'),
(NULL, 'Land Rover'),
(NULL, 'Mini');

INSERT INTO voiture (id_voiture, prix_unit_voiture, description, image_voiture, id_type_voiture, id_carburant, id_nbr_places, id_nbr_portes, id_modele, id_couleur, id_marque, stock_voiture) VALUES
(null, 80000,'Voiture pour fils de famille pas préssé','e63.jpg', 5, 1, 5, 2, 1, 5, 5, 7),
(null, 120000, 'Classe tah Dallas','mustang.png', 6,2, 2, 1, 2, 6,10,4),
(null, 165000,'Voiture pour père de famille préssé','m5.jpg',4,4, 5, 2, 3, 4,6,4),
(null, 190000,'Une jeune ambiance abérrante ','6x6.jpg',3,3,8, 2, 4, 3,5,2),
(null, 22000,'Une ambiance sportive et raffinée','2008.jpg',2,2,5, 2, 5, 2,1,6),
(null, 150000,'Une ambiance sportive et raffinée','rs7.jpg',1,1,5, 2, 6, 1,11,10);

INSERT INTO  etat(libelle_etat) VALUES ('en cours de traitement'), ('expédié'), ('validé');

SELECT * FROM user;

SELECT * FROM etat;

SELECT * FROM voiture;