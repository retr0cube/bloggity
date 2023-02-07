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
    document.cookie = "dark=true; path=/"
} else {
		document.cookie = "dark=false; path=/"
    ico.classList.remove('fa-solid','fa-sun');
    ico.classList.add('fa-solid','fa-moon');
}
	var element = document.body;
	element.classList.toggle("dark-mode");
}

function toggleMenu() {
	var ico = document.getElementById("menu-ico");
	if (ico.className == 'fa-solid fa-bars-staggered') {
    ico.classList.remove('fa-solid','fa-bars-staggered');
    ico.classList.add('fa-solid',"fa-xmark");
} else {
    ico.classList.remove('fa-solid','fa-xmark');
    ico.classList.add('fa-solid','fa-bars-staggered');
}
	var element = document.getElementById("lists");
	element.classList.toggle("toggled");
} 

function loadingAnimation() {
	var btn = document.getElementById("submitBtn");
	btn.insertAdjacentHTML('afterbegin', '<iconify-icon style="padding-right:10px;" inline icon="line-md:loading-twotone-loop"></iconify-icon>');
}


