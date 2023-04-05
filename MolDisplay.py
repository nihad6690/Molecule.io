import molecule

# radius, element name, header, footer, offsetx, and offsety was given in the assignment description
# radius = {
#     "H": 25,
#     "C": 40,
#     "O": 40,
#     "N": 40,
# }
# element_name = {
#     "H": "grey",
#     "C": "black",
#     "O": "red",
#     "N": "blue",
# }


header = """<svg version="1.1" width="1000" height="1000"
xmlns="http://www.w3.org/2000/svg">"""
radiant = """<radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
<stop offset="0%%" stop-color="#%s"/>
<stop offset="50%%" stop-color="#%s"/>
<stop offset="100%%" stop-color="#%s"/>
</radialGradient>""" % ("any_element", "403A3A", "A65E2E", "633A34")
header+= radiant
footer = """</svg>"""
offsetx = 500
offsety = 500


class Atom:
    def __init__(self, c_atom):
        self.c_atom = c_atom
        self.z = c_atom.z
        

    #return a string that displays the element, x, y, and z values
    def __str__(self):
        return '%s %.2f %.2f %.2f' % (self.c_atom.element, self.c_atom.x, self.c_atom.y, self.c_atom.z)
    
    #returns the svg method circle by the x, y, radius, and color of the atom 
    def svg(self):
        if self.c_atom.element not in radius and self.c_atom.element not in element_name:
            return  ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % ((self.c_atom.x * 100) + offsetx, (self.c_atom.y*100)+offsety, 30, "any_element")
        else:
            return  ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % ((self.c_atom.x * 100) + offsetx, (self.c_atom.y*100)+offsety, radius[self.c_atom.element], element_name[self.c_atom.element])
    
class Bond:
    def __init__(self, c_bond):
        self.c_bond = c_bond
        self.c_bond.z = c_bond.z

    #returns the string which has all the elements in the given bond
    def __str__(self):
        return '%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f' % (self.c_bond.a1, self.c_bond.a2, self.c_bond.epairs, self.c_bond.x1, self.c_bond.y1, self.c_bond.x2, self.c_bond.y2, self.c_bond.z, self.c_bond.len , self.c_bond.dx , self.c_bond.dy)
    
    def svg(self):

        #calcultes the points for the 4 corners
        x1 = ((self.c_bond.x1 * 100) + offsetx) - (self.c_bond.dy * 10)
        y1 = ((self.c_bond.y1 * 100) + offsety) + (self.c_bond.dx * 10)

        x2 = ((self.c_bond.x1 * 100) + offsetx) + (self.c_bond.dy * 10)
        y2 = ((self.c_bond.y1 * 100) + offsety) - (self.c_bond.dx * 10)

        x3 = ((self.c_bond.x2 * 100) + offsetx) + (self.c_bond.dy * 10)
        y3 = ((self.c_bond.y2* 100) + offsety)  - (self.c_bond.dx * 10)

        x4 = ((self.c_bond.x2 * 100) + offsetx) - (self.c_bond.dy * 10)
        y4 = ((self.c_bond.y2 * 100) + offsety) + (self.c_bond.dx * 10)

        #uses the points for the 4 corners in svg method polygon
        return ' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (x1, y1, x2, y2, x3, y3, x4, y4)
        

class Molecule(molecule.molecule):



    # uses all the atoms and bonds in the molecule to create a svg
    # first puts all the atoms and bonds from the molecule to an array
    # then uses the pseudocode code of  final pass of a merge sort function given in the assignment description to create the
    # svg string by using the class Atom and Bond to get the approiate svg string which is appended together and returned
    def svg(self):
        image = ''
        image += header
    
        atom_index = self.atom_no
        bond_index = self.bond_no
        atoms = []
        bonds = []

        for i in range(atom_index):
            atom = self.get_atom(i);
            atoms.append(atom)
        
        for i in range(bond_index):
            bond = self.get_bond(i);
            bonds.append(bond)

        while atoms or bonds:
            if atoms and bonds:
                a1 = atoms[0]
                b1 = bonds[0]
                if a1.z < b1.z:
                    atom = Atom(a1)
                    image += atom.svg()
                    atoms.pop(0)
                else:
                    bond = Bond(b1)
                    image += bond.svg()
                    bonds.pop(0)

            elif atoms and not bonds:
                a1 = atoms.pop(0)
                atom = Atom(a1)
                image += atom.svg()
                
            elif not atoms and bonds:
                b1 = bonds.pop(0)
                bond = Bond(b1)
                image += bond.svg()

        image += footer
        return image
    
    def parse(self, file):
        lines = file.readlines()
        words = []
        c = 0
        for cur_line in lines:
            #skips the first three lines
            if c > 2:
                #splits the string into words
                #https://stackoverflow.com/questions/40598078/how-does-raw-input-strip-split-in-python-work-in-this-code
                line_words = cur_line.strip().split(" ")
                words += line_words
            c += 1
            
        #https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
        words[:] = [x for x in words if x]
    
        nums_atoms = int(words[0])
        nums_bonds = int(words[1])
        
        for index, cur_line in enumerate(lines):

            #skips the first 4 line
            if index < 4:
                continue

            #puts all the words in the array
            #then turns those words to the corresponding thing in the Atom structure and appends that atom
            if index - 4 < nums_atoms:
                line_words = cur_line.strip().split(" ")
                line_words[:] = [x for x in line_words if x]
                self.append_atom(line_words[3], float(line_words[0]), float(line_words[1]), float(line_words[2]))
                
                
            
            #puts all the words in the array
            #then turns those words to the corresponding thing in the bond structure and appends that bond
            if (index - 4 >= nums_atoms) and (index - nums_atoms - 4 < nums_bonds):
                line_words = cur_line.strip().split(" ")
                line_words[:] = [x for x in line_words if x]
                self.append_bond(int(line_words[0]) - 1, int(line_words[1]) - 1, int(line_words[2]))
                
            
        
        
            
        
        