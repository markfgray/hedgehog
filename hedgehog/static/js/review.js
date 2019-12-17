$(document).ready(function () {
	document.getElementById("local-places")
	getLocation()
});

function getLocation() {
			  if (navigator.geolocation) {
			    navigator.geolocation.getCurrentPosition(getLocalPlaces);
			  } else { 
			    x.innerHTML = "Geolocation is not supported by this browser.";
			  }
			}

function getLocalPlaces(position) {
			  let lat = position.coords.latitude;  
			  let longi = position.coords.longitude;
			  let a = {'latitude': lat, 'longitude': longi};
			  let b = JSON.stringify(a)
			  $.ajax({
			  	url: '/localPlaces', 
			  	data: b, 
			  	type: 'POST',
			  	contentType:'application/json',
			  	success: function (data) {
				  	let parsed_json = JSON.parse(data);
		    		populateLocalPlaces(parsed_json);
			}
		});
	}

function populateLocalPlaces(data) {
	let container = document.getElementById("local-places")
	for (let i = 0; i < data.length; i++) {
		let place = document.createElement("div");
		let place_name = document.createElement("div");
		let place_type = document.createElement("div");
		place.setAttribute("class", "local-result")
		let link = document.createElement('a')
		let place_link = '/details/' + data[i]['name']
		link.href = place_link
		place_name.setAttribute("class", "local-place-name")
		place_type.setAttribute("class", "local-place-type")
		place_name.innerHTML = data[i]['name']
		place_type.innerHTML = data[i]['type']
		place.appendChild(place_name)
		place.appendChild(place_type)
		container.append(link)
		link.append(place)
	}

}
/*
<p id="demo"></p>

			<script>
			var x = document.getElementById("demo");

			function getLocation() {
			  if (navigator.geolocation) {
			    navigator.geolocation.getCurrentPosition(showPosition);
			  } else { 
			    x.innerHTML = "Geolocation is not supported by this browser.";
			  }
			}

			function showPosition(position) {
			  x.innerHTML = "Latitude: " + position.coords.latitude + 
			  "<br>Longitude: " + position.coords.longitude;
			}
			</script>

*/
