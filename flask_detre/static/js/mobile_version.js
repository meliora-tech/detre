function myFunction(x) {

    var a_tag = document.querySelectorAll("nav > a")[1]
    var div_tag = document.querySelector("nav > div")
    var divs_footer = document.querySelectorAll("footer > div > div")

if(x.matches){

    

    divs_footer.forEach(element =>{
        element.setAttribute("class","col-md-3")
    })

    a_tag.style.display = "block";
    div_tag.setAttribute("class","collapse navbar-collapse");



} else{

    a_tag.style.display = "none";
    div_tag.setAttribute("class","nav");
    divs_footer.forEach(element =>{
        element.setAttribute("class","col-3")
    })

}

}

function myFunctionCard(y){

var div_row_tags = document.querySelectorAll("section.data-types > div.type-row");
var div_tags     = document.querySelectorAll("section.data-types > div.type-row > div.card");
if(y.matches){
    

    div_row_tags.forEach(element => {
        element.style.display = "block";
        element.style.cssText = "padding:0px 0px";
    });

    div_tags.forEach(element => {
        element.setAttribute("class","card")
        element.style.cssText ="border:none;";
    })

} else{
    div_row_tags.forEach(element => {
        element.style.display = "flex";

    });

    div_tags.forEach(element => {
        element.setAttribute("class","card col-4")
        element.style.cssText = "border: none; border-right: 1px solid rgb(238, 238, 238); margin-bottom: 10px"

    })

}
}


var x = window.matchMedia("(max-width: 760px)")
var y = window.matchMedia("(max-width: 536px)")
myFunction(x)
myFunctionCard(y)
x.addListener(myFunction)
y.addListener(myFunctionCard)