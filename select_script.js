const add_molecule_to_table = (all_mols, cur) => {
    table_body = document.getElementById('table_body');
    let row = document.createElement("tr")
    for (let i = 0; i < 3; i++) {
        let cell = document.createElement("td")
        cell.innerText = cur[i]
        row.appendChild(cell)
    }
    cell = document.createElement("td")
    let btn = document.createElement("button")
    btn.className = "btn btn-success"
    btn.innerText = "Select Molecule"
    btn.addEventListener('click', (event) => {

        let mol_name = event.target.closest("tr").firstChild.innerText
        document.getElementById("selected_molecule").innerText = `Selected molecule = ${mol_name}`
        sessionStorage.setItem("selected_mol", mol_name)
        alert(`You have selected the molecule ${mol_name} which has ${all_mols[mol_name][0]} atoms and ${all_mols[mol_name][1]} bonds.`)



    })
    cell.appendChild(btn)
    row.appendChild(cell)
    table_body.appendChild(row)
}




$(document).ready(() => {

    $.get("/get_mol.html", (data, status) => {
        let res = sessionStorage.getItem("selected_mol")
        if (res !== null) {
            document.getElementById('selected_molecule').innerText = `Selected molecule = ${res}`
        }
        let b = data.replace(/'/g, '"');
        all_mols = JSON.parse(b)

        const buttonsContainer = document.getElementById("buttonsContainer")
        let keys = Object.keys(all_mols)
        for (let i = 0; i < Object.keys(all_mols).length; i++) {
            add_molecule_to_table(all_mols, [`${keys[i]}`, `${all_mols[keys[i]][0]}`, `${all_mols[keys[i]][1]}`])


        }


    });
}
);