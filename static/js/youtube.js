function youtube(){
    menu = document.getElementById("plataforma");
    div = document.getElementById("formato-yt");
    if(menu.value == "youtube"){
        div.style.display = "unset";
    }else{
        div.style.display = "none";
    }
}

/*VALIDACION NOT A VALID URL*/
window.onload = function() {
    menu = document.getElementById("plataforma");
    menu.value = "youtube";
}