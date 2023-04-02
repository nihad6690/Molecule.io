$(document).ready(() => {
    let res = sessionStorage.getItem("selected_mol")
    if (res !== null) {
        document.getElementById('selected_molecule').innerText = `Selected molecule = ${res}`
        $.post("/display_handler.html",
            /* pass a JavaScript dictionary */
            {
                mol_name: res

            },
            function (data, status) {
                const mol_image_section = document.getElementById("mol_image")
                mol_image_section.innerHTML = data
            }
        );
    }

}
);