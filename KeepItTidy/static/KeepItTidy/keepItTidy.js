let numberOfFields = 1;

document.addEventListener('DOMContentLoaded', function() {
	// BY DEFAULT - List all collections
	listCollections();
	
	// Add Field Button
	if (document.querySelector("#newField") != null){
		document.querySelector("#newField").addEventListener('click', addNewField);	
	}
	else {
		console.log("function for a different page");
	}
});


function listCollections() {
	// Lists all collections created by user

	// Get collections API
	fetch('/get_collections')
	.then(response => response.json())
	.then(collections => {
		// Create Container Div
		let mainDivContainer = document.createElement("div");
		mainDivContainer.className = "container-fluid";

		// Create row div
		let rowDiv = document.createElement("div");
		rowDiv.className = "row";

		// Create columns of cards in the row
		collections.forEach(function(collection) {
			let colDiv = document.createElement("div");
			colDiv.className = "col-sm";

			let cardDiv = document.createElement("div");
			cardDiv.className = "card";

			let cardBodyDiv = document.createElement("div");
			cardBodyDiv.className = "card-body";

			let cardTitle = document.createElement("h5");
			cardTitle.className = "card-title";
			cardTitle.innerHTML = collection['name'];
			cardBodyDiv.appendChild(cardTitle);

			let cardText = document.createElement("p");
			cardText.className = "card-text";
			cardText.innerHTML = collection['description'];
			cardBodyDiv.appendChild(cardText);

			let cardButton = document.createElement("a");
			cardButton.className = "btn btn-primary";
			let collectionUrl = "collection_page/" + collection['id'];
			cardButton.setAttribute("href", collectionUrl);
			cardButton.innerHTML = "Go to this thing";
			cardBodyDiv.appendChild(cardButton);

			// Append everything to the upper nodes
			cardDiv.appendChild(cardBodyDiv);
			colDiv.appendChild(cardDiv);

			rowDiv.appendChild(colDiv);

			console.log("Created one card!");
			})
		mainDivContainer.appendChild(rowDiv);

		let mainDiv = document.querySelector("#collections");
		mainDiv.appendChild(mainDivContainer);
	})
}


function addNewField() {
	// Cloning first field form to create new ones and modifying new id and name for each one
	
	numberOfFields += 1;

	let extraForm = document.querySelector("#fieldForm1").cloneNode(true);
	extraForm.id = "fieldForm" + numberOfFields
	let extraFormChildren = extraForm.childNodes;
	extraFormChildren.forEach(function(item) {
		if (item.nodeName == "DIV") {
			let itemChildren = item.childNodes;
			itemChildren.forEach(function(child) {
				if (child.nodeName == "INPUT") {
					child.id = "fieldName" + numberOfFields;
					child.setAttribute("name", "fieldName" + numberOfFields);
				}
				if (child.nodeName == "SELECT") {
					child.id = "fieldType" + numberOfFields;
					child.setAttribute("name", "fieldType" + numberOfFields);
				}
			});
		}
	});

	let fieldFormsDiv = document.querySelector("#fieldForms");
	fieldFormsDiv.appendChild(extraForm);
}