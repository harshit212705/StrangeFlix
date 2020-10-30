// special class for left navigation bar items
var v = document.querySelectorAll(".special");
v.forEach(element => {
	element.addEventListener('click', function () {
		element.setAttribute("class", "special");
	});
});