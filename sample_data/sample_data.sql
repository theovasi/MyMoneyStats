BEGIN TRANSACTION;

CREATE TABLE accounting_entry (
    uid INTEGER PRIMARY KEY,
    crdate INTEGER NOT NULL,
    amount REAL NOT NULL,
    date INTEGER NOT NULL,
    desc TEXT,
    deleted INTEGER DEFAULT 0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (11,1539109456,200.0,1539068400,'Thank you gift for client',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (12,1539109494,40.0,1531724400,'Taxi',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (13,1539109550,150.0,1533020400,'Tech conference',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (14,1539109573,72.0,1533279600,'Lunch with clients',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (15,1539109593,12.0,1533711600,'Uber',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (16,1539109621,40.0,1536735600,'Commute',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (17,1539109648,10.0,1534834800,'Pen purchase',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (18,1539109700,22.0,1537858800,'Lunch',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (19,1539109713,15.0,1538118000,'Uber',0);
INSERT INTO `accounting_entry` (uid,crdate,amount,date,desc,deleted) VALUES (20,1539109732,12.0,1538982000,'International call',0);

CREATE TABLE tag (
    uid INTEGER PRIMARY KEY,
    value TEXT UNIQUE NOT NULL,
    deleted INTEGER DEFAULT 0);
INSERT INTO `tag` (uid,value,deleted) VALUES (1,'Meals',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (2,'Taxi/Uber',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (4,'Auto rental',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (5,'Baggage Fees',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (6,'Airfare',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (7,'Bank Fees',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (8,'Cell Phone',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (9,'Client Gifts',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (10,'Conference Fees',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (11,'Events',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (12,'Hotel',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (13,'Mileage/Personal Auto',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (14,'Office Supplies',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (15,'Parking Fees',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (16,'Postage, FedEx',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (17,'Software Licenses',0);
INSERT INTO `tag` (uid,value,deleted) VALUES (18,'Visa Application',0);

CREATE TABLE tag_mm(
    uid_local INTEGER NOT NULL,
    uid_foreign INTEGER NOT NULL,
    FOREIGN KEY (uid_local) REFERENCES tags(uid));
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (9,11);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (2,12);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (10,13);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (1,14);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (2,15);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (13,16);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (15,16);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (14,17);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (1,18);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (2,19);
INSERT INTO `tag_mm` (uid_local,uid_foreign) VALUES (8,20);

COMMIT;
