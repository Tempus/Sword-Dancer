import os, sqlite3


path = raw_input('Enter the full path to a directory to put the database file, terminated by "/".\n')

path = "/Users/Tempus/Projects/Tales Online CCG/Python Bot/"

con = sqlite3.connect(path.strip() + 'TalesCardDatabase')
cur = con.cursor()




cur.execute('CREATE TABLE PlayerList (ID integer NOT NULL UNIQUE, Username varchar(32), Password varchar(32), Hostmask text, Name varchar(32), Description text, Rank int, Money int, PRIMARY KEY(ID))')

cur.execute('CREATE TABLE Record (ID integer PRIMARY KEY, POne integer REFERENCES PlayerList (ID), PTwo integer  REFERENCES PlayerList (ID), Result integer, Date date)')

cur.execute('CREATE TABLE PlayerCards (PID integer REFERENCES PlayerList (ID), CardID integer REFERENCES CardList (ID), Deck integer, Level integer)')

cur.execute('CREATE TABLE CardList (ID integer NOT NULL UNIQUE,Type integer,Name text,Description text,Family integer,Rarity integer,TP integer,HP integer,Attack integer,Defense integer,Magic integer,Equip integer,Artes integer,TPCost integer,Target integer,Category integer,EffectA integer,EffectAQuantity integer,EffectB integer,EffectBQuantity integer,PRIMARY KEY (ID,Name))')


path = raw_input('Enter the full path to the csv file.\n')
path = "/Users/Tempus/Projects/Tales Online CCG/Docs/Raw Tables/CardDatabase.csv"

file = open(path)

i = 1
for line in file:
    fields = line.split(',')

    print 'INSERT into CardList values (', i, fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8], fields[9], fields[10], fields[11], fields[12], fields[13], fields[14], fields[15], fields[16], fields[17], fields[18], ')'

    cur.execute('INSERT into CardList values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (i, fields[0], fields[1], fields[2], int(fields[3], 16), fields[4], fields[5], fields[6], fields[7], fields[8], fields[9], int(fields[10],16), int(fields[11],16), fields[12], fields[13], fields[14], fields[15], fields[16], fields[17], fields[18]))
    
    i += 1


cur.execute("INSERT into PlayerList values (1, 'guest', 'guest', 'guest@guest.guestIP.255.255.255.255', 'Guest', 'A guest accounted created as a sample', 1000, 1000)")


con.commit()