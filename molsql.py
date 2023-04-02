import os;
import sqlite3;
import MolDisplay;
class Database:

    def __init__(self, reset=False):
        #sets up the connection
        #if reset is true, it deletes previous database and creates a new one
        #else it just uses the previous database
        if reset and os.path.exists( 'molecules.db' ):
                os.remove( 'molecules.db' )
        self.conn = sqlite3.connect("molecules.db")
        
    def create_tables( self ):
        #creates all the tables
        self.conn.execute( """
                CREATE TABLE Elements ( 
                ELEMENT_NO INTEGER NOT NULL,
                ELEMENT_CODE VARCHAR(3) NOT NULL,
                ELEMENT_NAME VARCHAR(32) NOT NULL,
                COLOUR1 CHAR(6) NOT NULL,
                COLOUR2 CHAR(6) NOT NULL,
                COLOUR3 CHAR(6) NOT NULL,
                RADIUS DECIMAL(3) NOT NULL,
                PRIMARY KEY (ELEMENT_CODE) );""" );
         
        self.conn.execute( """
                CREATE TABLE Atoms ( 
                ATOM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                ELEMENT_CODE VARCHAR(3) NOT NULL,
                X DECIMAL(7,4) NOT NULL,
                Y DECIMAL(7,4) NOT NULL,
                Z DECIMAL(7,4) NOT NULL,
                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements);""" );

        self.conn.execute( """
                CREATE TABLE Bonds ( 
                BOND_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                A1 INTEGER NOT NULL,
                A2 INTEGER NOT NULL,
                EPAIRS INTEGER NOT NULL);""" );
        self.conn.execute("""
                CREATE TABLE Molecules(
                MOLECULE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME TEXT NOT NULL,
                UNIQUE (NAME)
                );""")
        self.conn.execute("""
                CREATE TABLE MoleculeAtom(
                MOLECULE_ID INTEGER NOT NULL, 
                ATOM_ID INTEGER NOT NULL,
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                FOREIGN KEY (ATOM_ID) REFERENCES Atoms
                );""")
        self.conn.execute("""
                CREATE TABLE MoleculeBond(
                MOLECULE_ID INTEGER NOT NULL, 
                BOND_ID INTEGER NOT NULL,
                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules,
                FOREIGN KEY (BOND_ID) REFERENCES Atoms
                );""")
    def __setitem__( self, table, values ):
        
        #https://stackoverflow.com/questions/23572999/declare-varchar-in-python
        #I found out to use ? for formatting the string from the website above
        
        #given the name of the table, values are inserted into the table and table is updated
        if table == "Elements":
          self.conn.execute("""
                INSERT
                INTO Elements (ELEMENT_NO, ELEMENT_CODE, ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3, RADIUS)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,(values[0], values[1], values[2], values[3], values[4], values[5], values[6]))
        elif table == "Atoms":
            self.conn.execute("""
                INSERT 
                INTO Atoms (ELEMENT_CODE, X, Y, Z)
                VALUES     (?, ?, ?, ?);
                """, (values[0], values[1], values[2], values[3]))
        elif table ==  "Bonds":
            self.conn.execute("""
                INSERT
                INTO Bonds (A1, A2, EPAIRS)
                VALUES     (?, ?, ?);""", (values[0], values[1], values[2]));
        elif table == "Molecules":
            self.conn.execute("""
                INSERT
                INTO Molecules (NAME)
                VALUES     (?);""", (values[0],))
        elif table == "MoleculeAtom":
            self.conn.execute("""
                INSERT 
                INTO MoleculeAtom (MOLECULE_ID, ATOM_ID)
                VALUES            (?, ?);
                """, (values[0], values[1]))
        elif table == "MoleculeBond":
            self.conn.execute("""
                INSERT 
                INTO MoleculeBond (MOLECULE_ID, Bond_ID)
                VALUES            (?, ?);
                """, (values[0], values[1]))
        
    def add_atom(self, molname, atom):

        #atom is being added to the database
        self['Atoms'] = (atom.element, atom.x, atom.y, atom.z);

            
        all_atom_ids = self.conn.execute("""SELECT ATOM_ID FROM Atoms;""").fetchall()
        atom_id = all_atom_ids[len(all_atom_ids) - 1][0]

        all_molecule_ids = self.conn.execute("""SELECT MOLECULE_ID from Molecules""").fetchall() 
        mol_id = all_molecule_ids[len(all_molecule_ids) - 1][0]

        #MoleculeAtom is being added to the database
        self["MoleculeAtom"] = (mol_id, atom_id)

    
    def add_bond( self, molname, bond ):
        #Bonds is being added to the database
        self["Bonds"] = (bond.a1, bond.a2, bond.epairs)
        all_bond_ids = self.conn.execute("""SELECT BOND_ID FROM Bonds;""").fetchall()
        bond_id = all_bond_ids[len(all_bond_ids) - 1][0]

        all_molecule_ids = self.conn.execute("""SELECT MOLECULE_ID from Molecules""").fetchall() 
        mol_id = all_molecule_ids[len(all_molecule_ids) - 1][0]

        #MoleculeBond is being added to the database
        self["MoleculeBond"] = (mol_id, bond_id)

    def add_molecule( self, name, fp ):
        obj = MolDisplay.Molecule()
        obj.parse(fp)
        
        self["Molecules"] = (name,)
        
        for i in range(obj.atom_no):
            self.add_atom(name, obj.get_atom(i))

        for i in range(obj.bond_no):
            self.add_bond(name, obj.get_bond(i))
        
        self.conn.commit()
    
    def getAllNames(self):
        return list(self.conn.execute("""SELECT NAME from Molecules """))

    #https://www.geeksforgeeks.org/python-remove-duplicate-tuples-from-list-of-tuples/
    def removeDuplicates(self, arr):
        seen = {}
        res = []

        for tup in arr:
            if tup not in seen:
                seen[tup] = True
                res.append(tup)
        return res
    
    def load_mol( self, name ):
        #retrives all the atoms and bonds from database according to the given name
        # then it creates a Molecule object from the Moldisplay and appends the atoms and bonds to that object
        # finally that Molecule is returned
        all_atoms = self.conn.execute("""
        SELECT Atoms.ELEMENT_CODE, Atoms.X, Atoms.Y, Atoms.Z
        FROM Molecules
        JOIN MoleculeAtom ON ( (SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?) = MoleculeAtom.MOLECULE_ID)
        JOIN ATOMS ON (MoleculeAtom.ATOM_ID = Atoms.ATOM_ID)""", (name, )).fetchall()
        
        all_atoms = self.removeDuplicates(all_atoms)
        all_bonds =  self.conn.execute("""
        SELECT Bonds.A1 , Bonds.A2, Bonds.Epairs
        FROM Molecules
        JOIN MoleculeBond ON ( (SELECT MOLECULE_ID FROM Molecules WHERE NAME = ?) = MoleculeBond.MOLECULE_ID)
        JOIN Bonds ON (MoleculeBond.BOND_ID = Bonds.BOND_ID)""", (name, )).fetchall()

        all_bonds = self.removeDuplicates(all_bonds)
        obj = MolDisplay.Molecule()

        for atom in all_atoms:
            
            elem = atom[0]
            x = atom[1]
            y = atom[2]
            z = atom[3]
            obj.append_atom(elem, x, y, z)
        for bond in all_bonds:
            a1 = bond[0]
            a2 = bond[1]
            epairs = bond[2]
            obj.append_bond(a1, a2, epairs)

        return obj
    
    def radius(self):
        return dict(self.conn.execute("""SELECT ELEMENT_CODE, RADIUS FROM ELEMENTS""").fetchall())
    
    def element_name(self):
        return dict(self.conn.execute("""SELECT ELEMENT_CODE, ELEMENT_NAME FROM ELEMENTS""").fetchall())
    
    def radial_gradients( self ):
        
        res = self.conn.execute("""SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3 FROM ELEMENTS""").fetchall()
        res_string = ""
        for tup in res:
            radialGradientSVG = """
<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
<stop offset="0%%" stop-color="#%s"/>
<stop offset="50%%" stop-color="#%s"/>
<stop offset="100%%" stop-color="#%s"/>
</radialGradient>""" % (tup[0], tup[1], tup[2], tup[3])
            
            res_string += radialGradientSVG
        return res_string
   