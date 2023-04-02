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
            const btn = document.createElement("button")
            const btn_text = `${keys[i]}`
            btn.innerText = btn_text
            btn.addEventListener("click", (event) => {
                document.getElementById("selected_molecule").innerText = `Selected molecule = ${event.target.innerText}`
                sessionStorage.setItem("selected_mol", event.target.innerText)
                alert(` You have selected the the molecule ${event.target.innerText} atom_no = ${all_mols[event.target.innerText][0]} bond_no = ${all_mols[event.target.innerText][1]} `)
            })
            buttonsContainer.appendChild(btn)
            buttonsContainer.appendChild(document.createElement("br"))

        }


    });
}
);