const inputElement = document.getElementsByClassName("myInput");
console.log(inputElement.length)


for(var i = 0; i < inputElement.length; i++) {
  (function(index) {
    inputElement[index].addEventListener("input", function() {
      if (this.value) {
        this.classList.add("has-content");
      } else {
        this.classList.remove("has-content");
      }
    });
  })(i);
}
