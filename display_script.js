$(document).ready(() => {
    let res = sessionStorage.getItem("selected_mol")
    if (res !== null) {
        document.getElementById('selected_molecule').innerText = `Selected molecule = ${res}`

        $("#button").click(() => {
            let x = document.getElementById('x').value
            let y = document.getElementById('y').value
            let z = document.getElementById('z').value

            if (!x || (x < 0) || (x > 360)) {
                alert("Please enter a valid x value")
            }
            else if (!y || (y < 0) || (y > 360)) {
                alert("Please enter a y value")
            } else if (!z || (z < 0) || (z > 360)) {
                alert("Please enter a z value")
            } else {
                rotations = [x, y, z]
                $.post("/display_handler.html",
                    /* pass a JavaScript dictionary */
                    {
                        mol_name: res,
                        rotations: rotations

                    },
                    function (data, status) {
                        const mol_image_section = document.getElementById("mol_image")
                        mol_image_section.innerHTML = data
                    }
                );
            }

        })


    }

}
);