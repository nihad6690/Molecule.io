/* javascript to accompany jquery.html */

$(document).ready(() => {
    /* add a click handler for our button */
    $("#button").click(() => {
        let re = /(\.sdf)$/i;
        console.log(document.getElementById('myFile').value)
        if (!document.getElementById('mol_name').value) {
            alert("You have not entered a molecule name, please try again.")
        }
        else if (document.getElementById('myFile').files[0] == null) {
            alert("You have not entered a file name, please try again.")
        }
        else if (!re.exec(document.getElementById('myFile').value)) {
            alert("File extension not supported!");
        }
        else {
            /*https://www.javascripttutorial.net/web-apis/javascript-filereader/#:~:text=To%20read%20the%20content%20of,drag%20%26%20drop%20or%20file%20input.&text=The%20readAsDataURL()%20method%20reads,get%20from%20the%20FileList%20object.*/ 
            const reader = new FileReader();
            reader.readAsText(document.getElementById('myFile').files[0]);
            reader.addEventListener('load', (event) => {

                $.post("/upload_handler.html",
                    /* pass a JavaScript dictionary */
                    {
                        mol_name: $("#mol_name").val(),
                        fileInfo: event.target.result	/* retreive value of name field */

                    },
                    function (data, status) {
                        alert("Data: " + data + "\nStatus: " + status);
                    }
                );
            });

        }
        /* ajax post */
    }
    );


}
);
