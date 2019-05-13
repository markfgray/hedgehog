function addViewDetailsListener() {
	document.addEventListener('click', function (event) {
		if (event.target.matches('.result')) {
			name = event.target.id
			window.location = '/placedetails/'+name
					
		}

	}, false)};

addViewDetailsListener()