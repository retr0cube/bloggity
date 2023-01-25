if (document.cookie == "dark=true") {
	var element = document.body;
	var ico = document.getElementById("dark-mode-ico");
		element.classList.toggle("dark-mode");
		ico.classList.remove('fa-solid','fa-moon');
	ico.classList.add('fa-solid',"fa-sun");
}

function toggleDark() {
	var ico = document.getElementById("dark-mode-ico");
	if (ico.className == 'fa-solid fa-moon') {
    ico.classList.remove('fa-solid','fa-moon');
    ico.classList.add('fa-solid',"fa-sun");
    document.cookie = "dark=true"
} else {
		document.cookie = "dark=false"
    ico.classList.remove('fa-solid','fa-sun');
    ico.classList.add('fa-solid','fa-moon');
}
var element = document.body;
	element.classList.toggle("dark-mode");
} 


