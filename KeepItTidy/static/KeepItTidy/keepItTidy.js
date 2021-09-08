let numberOfFields = 1;

document.addEventListener('DOMContentLoaded', function() {
	// BY DEFAULT - List all collections
	listCollections();
	
	// Add Field Button
	if (document.querySelector("#newField") != null){
		document.querySelector("#newField").addEventListener('click', addNewField);	
	}
});


function listCollections() {
	// Lists all collections created by user

	let mainDiv = document.querySelector("#collections");

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
			//let collectionUrl = "collection_page/" + collection['id'];
			//cardButton.setAttribute("href", collectionUrl);
			cardButton.addEventListener('click', () => {
				// Hide all collection cards
				mainDivContainer.style.display = "none";

				// Display requested collection

				// Create main div
				let clickedCollection = document.createElement("div");
				clickedCollection.id = "collection";
				clickedCollection.className = "jumbotron jumbotron-fluid";

				// Create Container div
				let containerDiv = document.createElement("div");
				containerDiv.className = "container-fluid";

				// Header
				let collectionName = document.createElement("h1");
				collectionName.className = "display-5";
				collectionName.innerHTML = collection['name'];

				// Description
				let collectionDescription = document.createElement("p");
				collectionDescription.className = "lead";
				collectionDescription.innerHTML = collection['description'];

				// Paragraph for add button
				let addButtonParagraph = document.createElement("p");
				addButtonParagraph.className = "lead";

				// Add item button
				let addButton = document.createElement("a");
				addButton.className = "btn btn-primary btn-lg";
				addButton.setAttribute("href", "add_item/" + collection['id']);
				addButton.setAttribute("role", "button");
				addButton.innerHTML = "Add item";

				// Set element hierarchy
				addButtonParagraph.appendChild(addButton);

				containerDiv.appendChild(collectionName);
				containerDiv.appendChild(collectionDescription);
				containerDiv.appendChild(addButtonParagraph);

				clickedCollection.appendChild(containerDiv);

				mainDiv.appendChild(clickedCollection);

				displayItems(collection['items']);


			})
			cardButton.innerHTML = "Go to this thing";
			cardBodyDiv.appendChild(cardButton);

			// Append everything to the upper nodes
			cardDiv.appendChild(cardBodyDiv);
			colDiv.appendChild(cardDiv);

			rowDiv.appendChild(colDiv);

			console.log("Created one card!");
			})
		mainDivContainer.appendChild(rowDiv);

		
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


function displayItems(itemSource) {
	// Items
	let items = itemSource;

	createItemRow(items);
}


function createItemRow(items) {
	let itemRow = document.createElement("div");
	itemRow.className = "row";

	// Item Collumns
	items.forEach(function(item) {
		createItemCard(item, itemRow);
		});
}


function createItemCard(item, row) {

	// Set up divs
	let itemCollumn = document.createElement("div");
	itemCollumn.className = "col-sm"

	let itemCardDiv = document.createElement("div");
	itemCardDiv.className = "card";

	let itemCardBody = document.createElement("div");
	itemCardBody.className = "card-body";

	let itemCardTitle = document.createElement("h5");
	itemCardTitle.className = "card-title";
	itemCardBody.appendChild(itemCardTitle);

	let itemCardDescription = document.createElement("p");
	itemCardDescription.className = "card-text";
	itemCardBody.appendChild(itemCardDescription);

	// Insert content

	// Name and Description
	itemCardTitle.innerHTML = item['name'];
	itemCardDescription.innerHTML = item['description']

	for (var key in item) {
		if (key != "name" && key != "description") {
			let content = document.createElement("p");
		content.className = "card-text";
		content.innerHTML = key + ": " + item[key];
		console.log(key + ": " + item['key'])
		itemCardBody.appendChild(content);
	}
	}

	// Set up element hierarchy 
	
	itemCardDiv.appendChild(itemCardBody);
	itemCollumn.appendChild(itemCardDiv);
	row.appendChild(itemCollumn);

	document.body.appendChild(row);

}