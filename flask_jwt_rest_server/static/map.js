let map;

function initMap() {
	if (navigator.geolocation){
		navigator.geolocation.getCurrentPosition(showPosition);
	} 
	else {
		x.innerHTML = "Geolocation is not supported by this browser. ";
	}
}

function showPosition(position) {

	const coords = { lat: position.coords.latitude, lng: position.coords.longitude };
		
 	map = new google.maps.Map(document.getElementById("map"), {
		  center: { lat: position.coords.latitude, lng: position.coords.longitude }, zoom: 15,
			  
	});

	let infoWindow = new google.maps.InfoWindow({
		content: "Current Location", position: coords,

	});
	
	infoWindow.open(map);
	
}
