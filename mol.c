#include "mol.h"

int compare_atoms(const void *a, const void *b)
{
  atom *a_ptr, *b_ptr;
  // turns the pointer into atoms
  a_ptr = *(atom **)a;
  b_ptr = *(atom **)b;

  // extracts the z values
  double a_z = a_ptr->z;
  double b_z = b_ptr->z;

  // I used the logic from this website to do the main comparision
  // https://stackoverflow.com/questions/20584499/why-qsort-from-stdlib-doesnt-work-with-double-values-c
  if (a_z < b_z)
  {
    return -1;
  }
  else if (a_z > b_z)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}

int bond_comp(const void *a, const void *b)
{

  // same logic as compare_atoms
  bond *a_ptr, *b_ptr;

  a_ptr = *(bond **)a;
  b_ptr = *(bond **)b;

  //Due to the new bond struct, it is easier to access the z and easier to comapre
  double a_average = a_ptr->z;
  double b_average = b_ptr->z;

  if (a_average < b_average)
  {
    return -1;
  }
  else if (a_average > b_average)
  {
    return 1;
  }
  else
  {
    return 0;
  }
}

void atomset(atom *atom, char element[3], double *x, double *y, double *z)
{
  // copies element, x, y, z into the given atom in parameter
  strncpy(atom->element, element, 3);
  atom->x = *x;
  atom->y = *y;
  atom->z = *z;
}

void atomget(atom *atom, char element[3], double *x, double *y, double *z)
{
  // copies values from atom to element[3], *x, *y, *z
  strncpy(element, atom->element, 3);
  *x = atom->x;
  *y = atom->y;
  *z = atom->z;
}

void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms,
             unsigned char *epairs)
{
  // copies the attributes in bond to their corresponding arguments: a1, a2, atoms, and epairs
  *a1 = bond->a1;
  *a2 = bond->a2;
  (*atoms) = bond->atoms;
  *epairs = bond->epairs;
}

void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms,
             unsigned char *epairs)
{

  // copies a1, a2, atoms, and epairs to the their corresponding variables in bond 
  bond->a1 = *a1;
  bond->a2 = *a2;
  bond->atoms = *atoms;
  bond->epairs = *epairs;
  compute_coords(bond); 
}


void compute_coords(bond *bond)
{

  // computes z, x1, y1, x2, y2, len, dx, and dy values of the bond and set them
  bond->x1 = bond->atoms[bond->a1].x;
  bond->x2 = bond->atoms[bond->a2].x;
  bond->y1 = bond->atoms[bond->a1].y;
  bond->y2 = bond->atoms[bond->a2].y;
  bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;
  bond->len = sqrt(pow((bond->x2 - bond->x1), 2) + pow((bond->y2 - bond->y1), 2));
  bond->dx = (bond->x2 - bond->x1) / bond->len;
  bond->dy = (bond->y2 - bond->y1) / bond->len;
}
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max)
{

  molecule *cur_mol = malloc(sizeof(molecule));

  cur_mol->atom_max = atom_max;
  cur_mol->atom_no = 0;
  cur_mol->atoms = malloc(atom_max * sizeof(atom));
  cur_mol->atom_ptrs = malloc(atom_max * sizeof(atom *));

  cur_mol->bond_max = bond_max;
  cur_mol->bond_no = 0;
  cur_mol->bonds = malloc(bond_max * sizeof(bond));
  cur_mol->bond_ptrs = malloc(bond_max * sizeof(bond *));

  return cur_mol;
}

void molappend_atom(molecule *molecule, atom *atom)
{

  if (molecule->atom_no == molecule->atom_max)
  {

    if (molecule->atom_max == 0)
    {
      molecule->atom_max = 1;
    }
    else
    {
      molecule->atom_max *= 2;
    }
    molecule->atoms =
        realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
    molecule->atom_ptrs = realloc(molecule->atom_ptrs,
                                  sizeof(struct atom *) * molecule->atom_max);

    // readjusts the atom_ptrs after the realloc of atoms to match the new
    // address after the atoms have been placed somewhere else in the memory
    for (int i = 0; i < molecule->atom_no; i++)
    {
      molecule->atom_ptrs[i] = &molecule->atoms[i];
    }
  }
  // copying everything into the atom in molecule from the given atom in the
  // parameters and increasing the atom_no to create a new space for the next
  // atom
  molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
  strncpy(molecule->atoms[molecule->atom_no].element, atom->element, 3);
  molecule->atoms[molecule->atom_no].x = atom->x;
  molecule->atoms[molecule->atom_no].y = atom->y;
  molecule->atoms[molecule->atom_no].z = atom->z;
  molecule->atom_no += 1;
}

void molappend_bond(molecule *molecule, bond *bond)
{
  if (molecule->bond_no == molecule->bond_max)
  {

    if (molecule->bond_max == 0)
    {
      molecule->bond_max = 1;
    }
    else
    {
      molecule->bond_max *= 2;
    }

    molecule->bonds =
        realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
    molecule->bond_ptrs = realloc(molecule->bond_ptrs,
                                  molecule->bond_max * sizeof(struct bond *));

    // readjusts the bond_ptrs after the realloc of atoms to match the new
    // address after the bonds have been placed somewhere else in the memory

    for (int i = 0; i < molecule->bond_no; i++)
    {
      molecule->bond_ptrs[i] = &molecule->bonds[i];
    }
  }

  // copying everything into the bond in molecule from the given bond in the
  // parameters and increasing the bond_no to create a new space for the next
  // atom
  molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
  molecule->bonds[molecule->bond_no] = *bond;
  molecule->bond_no += 1;
}
molecule *molcopy(molecule *src)
{
  // creates a new molecule and copies the molecule given in the parameters into
  // the new molecule that is created
  //  and that new molecule is returned
  molecule *new_mol;

  new_mol = molmalloc(src->atom_max, src->bond_max);
  new_mol->atom_max = src->atom_max;
  new_mol->atom_no = 0;
  new_mol->bond_max = src->bond_max;
  new_mol->bond_no = 0;
  for (int i = 0; i < src->atom_no; i++)
  {

    molappend_atom(new_mol, &src->atoms[i]);
  }
  for (int i = 0; i < src->bond_no; i++)
  {
    molappend_bond(new_mol, &src->bonds[i]);
  }

  new_mol->atom_no = src->atom_no;
  new_mol->bond_no = src->bond_no;
  return new_mol;
}
void molfree(molecule *ptr)
{
  // frees the molecule 'ptr'
  free(ptr->atoms);
  free(ptr->atom_ptrs);
  free(ptr->bonds);
  free(ptr->bond_ptrs);
  free(ptr);
}

void molsort(molecule *molecule)
{
  // performs qsort with atom_ptrs so that all atoms in the molecule are sorted
  // according to their z value
  qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom *),
        compare_atoms);

  // performs qsort with bond_ptrs so that all bonds molecules are sorted
  // according to their z value
  //  since a bond has two atoms, the individual z value is calculated by
  //  calculating the average of the two z values
  qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond *),
        bond_comp);
}
void xrotation(xform_matrix xform_matrix, unsigned short deg)
{
  double rad = (double)(deg * (PI / 180));

  xform_matrix[0][0] = 1;
  xform_matrix[0][1] = 0;
  xform_matrix[0][2] = 0;

  xform_matrix[1][0] = 0;
  xform_matrix[1][1] = cos(rad);
  xform_matrix[1][2] = -1 * sin(rad);

  xform_matrix[2][0] = 0;
  xform_matrix[2][1] = sin(rad);
  xform_matrix[2][2] = cos(rad);
}

void yrotation(xform_matrix xform_matrix, unsigned short deg)
{
  double rad = (double)(deg * (PI / 180));
  xform_matrix[0][0] = cos(rad);
  xform_matrix[0][1] = 0;
  xform_matrix[0][2] = sin(rad);

  xform_matrix[1][0] = 0;
  xform_matrix[1][1] = 1;
  xform_matrix[1][2] = 0;

  xform_matrix[2][0] = -1 * sin(rad);
  xform_matrix[2][1] = 0;
  xform_matrix[2][2] = cos(rad);
}
void zrotation(xform_matrix xform_matrix, unsigned short deg)
{
  double rad = (double)(deg * (PI / 180));

  xform_matrix[0][0] = cos(rad);
  xform_matrix[0][1] = -1 * sin(rad);
  xform_matrix[0][2] = 0;

  xform_matrix[1][0] = sin(rad);
  xform_matrix[1][1] = cos(rad);
  xform_matrix[1][2] = 0;

  xform_matrix[2][0] = 0;
  xform_matrix[2][1] = 0;
  xform_matrix[2][2] = 1;
}

void mol_xform(molecule *molecule, xform_matrix matrix)
{
  int n = molecule->atom_no;

  for (int i = 0; i < n; i++)
  {

    double x = molecule->atoms[i].x;
    double y = molecule->atoms[i].y;
    double z = molecule->atoms[i].z;

    // does matrix multiplication and updates the x,y,z in the atoms of the
    // molecules after performing matrix multiplicaiton
    molecule->atoms[i].x =
        (matrix[0][0] * x) + (matrix[0][1] * y) + (matrix[0][2] * z);
    molecule->atoms[i].y =
        (matrix[1][0] * x) + (matrix[1][1] * y) + (matrix[1][2] * z);
    molecule->atoms[i].z =
        (matrix[2][0] * x) + (matrix[2][1] * y) + (matrix[2][2] * z);
  }

  // calls the compute coords like described in the assignment outline
  n = molecule->bond_no;
  for (int i = 0; i < n; i++)
  {
    compute_coords(&molecule->bonds[i]);
  }
}
