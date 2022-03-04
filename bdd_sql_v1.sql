DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS voiture;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS type_voiture;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS carburant;
DROP TABLE IF EXISTS modele;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS marque;

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

CREATE TABLE IF NOT EXISTS modele(
   id_modele INT AUTO_INCREMENT,
   libelle_modele VARCHAR(50),
   PRIMARY KEY(id_modele)
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
   pseudo VARCHAR(50),
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

CREATE TABLE IF NOT EXISTS voiture(
   id_voiture INT AUTO_INCREMENT,
   nom_voiture VARCHAR(255),
   prix_unit_voiture NUMERIC(10,2),
   nbr_place_voiture INT,
   description TEXT,
   image_voiture VARCHAR(255),
   id_type_voiture INT NOT NULL,
   id_carburant INT NOT NULL,
   id_modele INT NOT NULL,
   id_couleur INT NOT NULL,
   id_marque INT NOT NULL,
   stock_voiture INT NOT NULL,
   PRIMARY KEY(id_voiture),
   CONSTRAINT fk_voiture_type_voiture
   FOREIGN KEY(id_type_voiture) REFERENCES type_voiture(id_type_voiture),
   CONSTRAINT fk_voiture_carburant
   FOREIGN KEY(id_carburant) REFERENCES carburant(id_carburant),
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
   id_user INT NOT NULL,
   id_etat INT NOT NULL,
   PRIMARY KEY(id_commande),
   CONSTRAINT fk_commande_user
   FOREIGN KEY(id_user) REFERENCES user(user_id),
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
   id_Commande INT,
   prix_unit NUMERIC(10,2),
   quantite INT,
   PRIMARY KEY(id_ligne_commande),
   CONSTRAINT fk_ligne_commande_voiture
   FOREIGN KEY(id_voiture) REFERENCES voiture(id_voiture),
   CONSTRAINT fk_ligne_commande_commande
   FOREIGN KEY(id_Commande) REFERENCES commande(id_commande)
);

INSERT INTO user (user_id, email, username, password, role,  est_actif) VALUES
(null, 'admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1);
INSERT INTO user  (user_id, email, username, password, role,  est_actif) VALUES
(null, 'client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client',   1);
INSERT INTO user  (user_id, email, username, password, role, est_actif) VALUES
(null, 'client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client',   1);


INSERT INTO couleur (id_couleur, libelle_couleur) VALUES
(null,'gris');
INSERT INTO type_voiture (id_type_voiture, libelle_type_voiture) VALUES
(null,'Sportback');
INSERT INTO carburant (id_carburant, libelle_carburant) VALUES
(null,'sp-95');
INSERT INTO marque (id_marque, libelle_marque) VALUES
(null,'Audi');
INSERT INTO modele (id_modele, libelle_modele) VALUES
(null,'Audi RS-7 Sportback');
INSERT INTO voiture (id_voiture, nom_voiture, prix_unit_voiture, nbr_place_voiture, description, image_voiture, id_type_voiture, id_carburant, id_modele, id_couleur, id_marque, stock_voiture) VALUES
(null, 'RS7',150000,5,'Une ambiance sportive et raffinée','rs7.jpg',1,1,1,1,1,10);

INSERT INTO couleur (id_couleur, libelle_couleur) VALUES
(null,'blanc');
INSERT INTO type_voiture (id_type_voiture, libelle_type_voiture) VALUES
(null,'SUV');
INSERT INTO carburant (id_carburant, libelle_carburant) VALUES
(null,'sp-95');
INSERT INTO marque (id_marque, libelle_marque) VALUES
(null,'Peugeot');
INSERT INTO modele (id_modele, libelle_modele) VALUES
(null,'Peugeot 2008 suv');
INSERT INTO voiture (id_voiture, nom_voiture, prix_unit_voiture, nbr_place_voiture, description, image_voiture, id_type_voiture, id_carburant, id_modele, id_couleur, id_marque, stock_voiture) VALUES
(null, '2008',22000,5,'Une ambiance sportive et raffinée','2008.jpg',2,2,2,2,2,6);

INSERT INTO couleur (id_couleur, libelle_couleur) VALUES
(null,'noir');
INSERT INTO type_voiture (id_type_voiture, libelle_type_voiture) VALUES
(null,'6X6');
INSERT INTO carburant (id_carburant, libelle_carburant) VALUES
(null,'Diesel');
INSERT INTO marque (id_marque, libelle_marque) VALUES
(null,'Mercedes-Benz');
INSERT INTO modele (id_modele, libelle_modele) VALUES
(null,'G63 6x6');
INSERT INTO voiture (id_voiture, nom_voiture, prix_unit_voiture, nbr_place_voiture, description, image_voiture, id_type_voiture, id_carburant, id_modele, id_couleur, id_marque, stock_voiture) VALUES
(null, 'G63 6x6',190000,9,'Une jeune ambiance abérrante ','6x6.jpg',3,3,3,3,3,2);

INSERT INTO couleur (id_couleur, libelle_couleur) VALUES
(null,'noir');
INSERT INTO type_voiture (id_type_voiture, libelle_type_voiture) VALUES
(null,'Berline');
INSERT INTO carburant (id_carburant, libelle_carburant) VALUES
(null,'Diesel');
INSERT INTO marque (id_marque, libelle_marque) VALUES
(null,'BMW');
INSERT INTO modele (id_modele, libelle_modele) VALUES
(null,'M5 BMW');
INSERT INTO voiture (id_voiture, nom_voiture, prix_unit_voiture, nbr_place_voiture, description, image_voiture, id_type_voiture, id_carburant, id_modele, id_couleur, id_marque, stock_voiture) VALUES
(null, 'M5',165000,5,'Voiture pour père de famille préssé','m5.jpg',4,4,4,4,4,4);

INSERT INTO couleur (id_couleur, libelle_couleur) VALUES
(null,'gris');
INSERT INTO type_voiture (id_type_voiture, libelle_type_voiture) VALUES
(null,'Berline');
INSERT INTO carburant (id_carburant, libelle_carburant) VALUES
(null,'Essence');
INSERT INTO marque (id_marque, libelle_marque) VALUES
(null,'Mercedes-benz');
INSERT INTO modele (id_modele, libelle_modele) VALUES
(null,'E63 W212');
INSERT INTO voiture (id_voiture, nom_voiture, prix_unit_voiture, nbr_place_voiture, description, image_voiture, id_type_voiture, id_carburant, id_modele, id_couleur, id_marque, stock_voiture) VALUES
(null, 'E63 W212',80000,5,'Voiture pour fils de famille pas préssé','e63.jpg',5,5,5,5,5,7);

INSERT INTO couleur (id_couleur, libelle_couleur) VALUES
(null,'rouge');
INSERT INTO type_voiture (id_type_voiture, libelle_type_voiture) VALUES
(null,'coupé');
INSERT INTO carburant (id_carburant, libelle_carburant) VALUES
(null,'Diesel');
INSERT INTO marque (id_marque, libelle_marque) VALUES
(null,'Ford ');
INSERT INTO modele (id_modele, libelle_modele) VALUES
(null,'Mustang');
INSERT INTO voiture (id_voiture, nom_voiture, prix_unit_voiture, nbr_place_voiture, description, image_voiture, id_type_voiture, id_carburant, id_modele, id_couleur, id_marque, stock_voiture) VALUES
(null, 'Ford Mustang',120000,4,'Classe tah Dallas','mustang.png',6,6,6,6,6,4);

INSERT INTO  etat(libelle_etat) VALUES ('en cours de traitement'), ('expédié'), ('validé');

SELECT * FROM user;

SELECT * FROM etat;