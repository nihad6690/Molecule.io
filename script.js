
$(document).ready(() => {
    $.get("/get_element.html", (data, status) => {
        let b = data.replace(/'/g, '"');

        /*https://stackoverflow.com/questions/52046119/javascript-converting-string-to-array-of-tuples*/
        all_elements = JSON.parse(b
            .replace(/\(/g, '[')
            .replace(/\)/g, ']')
        );
        table_body = document.getElementById('table_body');

        all_elements.forEach((cur) => {

            let row = document.createElement("tr")


            for (let i = 0; i < 7; i++) {
                let cell = document.createElement("td")
                cell.innerText = cur[i]
                row.appendChild(cell)
            }
            cell = document.createElement("td")
            let btn = document.createElement("button")
            btn.className = "btn btn-danger"
            btn.innerText = "Delete Element"
            btn.addEventListener('click', (event) => {

                alert("Clicked button")
                console.log(event)
                let element = event.target.parentNode.parentNode.innerText.split('\t')
                element.pop()

                /*https://stackoverflow.com/questions/13241005/add-delete-row-from-a-table*/

                let row = event.target.parentNode.parentNode;
                row.parentNode.removeChild(row);
                $.post("/remove_element_handler.html", {
                    remove_element: element
                },
                    function (data, status) {
                        alert("Data: " + data + "\nStatus: " + status);
                    })


            })
            cell.appendChild(btn)
            row.appendChild(cell)


            table_body.appendChild(row)

        });
    })
    let element_code = null

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
        } else {
            $.post("/add_handler.html",
                /* pass a JavaScript dictionary */
                {
                    element_num: document.getElementById('element_number').value,
                    element_code: element_code,
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

    })


}
);