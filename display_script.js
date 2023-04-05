const postReqToDisplayMol = (res, rotations, is_there_rotation) => {
    $.post("/display_handler.html",
        /* pass a JavaScript dictionary */
        {
            mol_name: res,
            rotations: rotations,
            is_there_rotation: is_there_rotation
        },
        function (data, status) {
            const mol_image_section = document.getElementById("mol_image")
            mol_image_section.innerHTML = data
        }
    );
}


$(document).ready(() => {
    let element_code = null


    let res = sessionStorage.getItem("selected_mol")

    if (res !== null) {

        document.getElementById('selected_molecule').innerText = `Selected molecule = ${res}`
        $("#no_rot_button").click(() => {
            postReqToDisplayMol(res, [], false)
        })
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
                if (y == 0 && z == 0) {
                    rotations = [x, y, z]
                    postReqToDisplayMol(res, rotations, true)
                }
                else if (x == 0 && z == 0) {
                    rotations = [x, y, z]
                    postReqToDisplayMol(res, rotations, true)
                }
                else if (x == 0 && y == 0) {
                    rotations = [x, y, z]
                    postReqToDisplayMol(res, rotations, true)
                } else {
                    alert("The input is invalid, please try again")
                }

            }

        })


    }

}
);