
$(document).ready(() => {
    let element_code = null
    /*
    console.log(document.getElementById('element_code').value)
    let res = sessionStorage.getItem("selected_mol")
    if (res !== null) {
        document.getElementById('selected_molecule').innerText = `Selected molecule = ${res}`
    }
    */
    symbols_in_periodic_table = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']

    symbols_in_periodic_table.forEach((e) => {
        $("#menu").append(`<li><a class="dropdown-item" type="button" href="#">${e}</a></li>`)
    })

    /*https://stackoverflow.com/a/22000328*/
    $(".dropdown-menu li a").click(function () {
        $(this).parents(".dropdown").find('.btn').html($(this).text());
        element_code = $(this).text()


    });

    $("#add_element").click(function () {

        if (!document.getElementById('element_number').value) {
            alert("Please enter a element number")
        }
        else if (element_code == null) {
            alert("Please select a element code")
        }
        else if (!document.getElementById('element_name').value) {
            alert("Please enter a element name")
        }
        else if (!document.getElementById('radius').value) {
            alert("Please enter a radius")
        }else{
            $.post("/add_handler.html",
                    /* pass a JavaScript dictionary */
                    {
                        element_num: document.getElementById('element_number').value,
                        element_code:element_code,
                        element_name: document.getElementById('element_name').value,
                        color_1: document.getElementById('color1').value, 
                        color_2: document.getElementById('color2').value, 
                        color_3: document.getElementById('color3').value, 
                        radius: document.getElementById('radius').value

                    },
                    function (data, status) {
                        alert("Data: " + data + "\nStatus: " + status);
                    }
                );
        }
        console.log(`element number ${document.getElementById('element_number').value}\nelement code ${element_code}\nelement name: ${document.getElementById('element_name').value}\n`)
        console.log(`color1:${document.getElementById('color1').value}`)
        console.log(element_code)
    })


}
);