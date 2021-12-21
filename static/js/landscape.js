var p = document.getElementById("landscape");
var main = document.getElementById("tabla");
var texto = document.getElementById("main");

window.onload = function() {
  if(screen.availHeight > screen.availWidth){
    main.style.display = "none";
    p.style.display = "unset";
    texto.style.textAlign = "center";
  }
};

window.onorientationchange = function(event) {
  if(screen.availHeight > screen.availWidth){
    p.style.display = "unset";
    main.style.display = "none";
    texto.style.textAlign = "center";
  }else{
      p.style.display = "none";
    main.style.display = "unset";
    texto.style.textAlign = "unset";
  }
};