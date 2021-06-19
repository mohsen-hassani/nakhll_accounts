function getObjects(url) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let options = JSON.parse(this.responseText);
            let select = document.getElementById('id_dst_object_id')
            select.innerHTML = '';
            for (let i =0; i < options.length; i++)
            {
                let option = options[i];
                let element = document.createElement("option");
                element.value = option.id;
                element.textContent = option.name;
                select.appendChild(element);
            }
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}

let select = document.getElementById('id_dst_content_type');
select.addEventListener("click", function() {
    getObjects(`http://localhost:8000/markets/api/objects/?id=${select.value}`)
});