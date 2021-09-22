let numberOfFields = 1;

document.addEventListener('DOMContentLoaded', function() {
	// BY DEFAULT - List all collections if we are in the right section
	if (document.querySelector("#collections")) {
		// Check if this was accessed through quick access bar
		let url = window.location.href;
		let urlArray = url.split('/');
		let lastUrlElement = urlArray[urlArray.length - 1];

		if (lastUrlElement == 'view_collection') {
			listCollections();
		}
		else {
			quickAccessCollection(parseInt(lastUrlElement));
		}
	}

	//Browse Collections from the Nav Bar
	navbarCollectionList();
	
	// Add Field Button
	if (document.querySelector("#newField")) {
		document.querySelector("#newField").addEventListener('click', addNewField);	
	}
});


function quickAccessCollection(collection_id) {
	// Fetch API
	fetch('/get_collections')
	.then(response => response.json())
	.then(collections => {
		collections.forEach(function(collection) {
			if (collection['id'] == collection_id) {
				var source = collection;
				displayCollection(collection, document.querySelector("#collections"));
				return
			}
	})
	})
}


function navbarCollectionList() {
	// Get collection titles to be listed in the navbar

	//get parammeter for url link
	let url = window.location.href;
	let urlArray = url.split('/');
	let parammeter = urlArray[urlArray.length - 1];

	// Dropdown button variable
	let dropdownBrowse = document.querySelector("#dropdown01");

	// Variable for dropt down list div
	let dropList = document.createElement("div");
	dropList.id = 'dropdown01ShowList';
	dropList.className = "dropdown-menu";
	dropList.setAttribute("aria-labelledby", "dropdown01");
	dropdownBrowse.appendChild(dropList);

	// Fetch the API
	fetch('/get_collections')
	.then(response => response.json())
	.then(collections => {
		collections.forEach(function(collection) {
			let dropdownLink = document.createElement("a");
			dropdownLink.className = "dropdown-item";
			let urlLink = "../view_collection/" + collection['id'];
			dropdownLink.setAttribute("href", urlLink);
			//dropdownLink.setAttribute("aria-disabled", "true");
			dropdownLink.innerHTML = collection['name'];
			dropList.appendChild(dropdownLink);
		})
	})
}


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
				displayCollection(collection, mainDiv);

			})
			cardButton.innerHTML = "Go to this thing";
			cardBodyDiv.appendChild(cardButton);

			// Append everything to the upper nodes
			cardDiv.appendChild(cardBodyDiv);
			colDiv.appendChild(cardDiv);

			rowDiv.appendChild(colDiv);
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


function displayCollection(collection, parrent) {
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

	parrent.appendChild(clickedCollection);

	displayItems(collection['items']);
}


function displayItems(itemSource) {
	// Items
	let items = itemSource;
	let nrOfRows;

	if (Math.floor(items.length / 4) <= 1) {
		nrOfRows = 1;
	}

	else {
		nrOfRows = Math.floor(items.length / 4);
	}

	console.log("Items:" + items.length);
	console.log("Nr of Rows: " + nrOfRows);


	let itemsContainer = document.createElement("div");
	itemsContainer.className = "container-fluid";

	for (let i = 0; i < nrOfRows; i++) {
		let row = items.slice(0, 4);
		createItemRow(row, itemsContainer);
		items.splice(0, 4);
	}

	console.log("Items left:" + items.length);

	if (items.length > 0) {
		createItemRow(items, itemsContainer);
	}

	document.body.appendChild(itemsContainer);
}


function createItemRow(items, containerDiv) {
	let itemRow = document.createElement("div");
	itemRow.className = "row";
	//itemRow.style.padding = "1em";

	// Item Collumns
	items.forEach(function(item) {
		createItemCard(item, itemRow);
		});

	containerDiv.appendChild(itemRow);
}


function createItemCard(item, row, containerDiv) {

	// Set up divs
	let itemCollumn = document.createElement("div");
	itemCollumn.className = "col-sm col-md-3";
	itemCollumn.style.padding = "1em";

	// Create card elements starting with an "a" tag to trigger a modal pop-up
	let itemCardDiv = document.createElement("a");
	itemCardDiv.className = "card h-100"; // h-100 creates a fixed card height for the entire 100% height of the column
	itemCardDiv.setAttribute("type", "button");
	itemCardDiv.setAttribute("data-toggle", "modal");
	itemCardDiv.setAttribute("data-target", "#itemModal" + item['id']);

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
		if (key != "name" && key != "description" && key != "id") {
			let content = document.createElement("p");
			content.className = "card-text";
			// Check for boolean values
			if (item[key] == true) {
				content.innerHTML = key + ": " + 'Yes';
			}
			else if (item[key] == false) {
				content.innerHTML = key + ": " + 'No';
			}
			else {
				content.innerHTML = key + ": " + item[key];
			}

			itemCardBody.appendChild(content);
		}
	}

	// Set up modal pop-up
	let modalDiv = document.createElement("div");
	modalDiv.className = "modal fade";
	modalDiv.id = "itemModal" + item['id'];
	modalDiv.setAttribute("tabindex", "-1");
	modalDiv.setAttribute("role", "document");
	modalDiv.setAttribute("aria-labelledby", "#itemModal" + item['id'] + "Title");
	modalDiv.setAttribute("aria-hidden", "true");

	let modalDialogDiv = document.createElement("div");
	modalDialogDiv.className = "modal-dialog modal-dialog-centered";
	modalDialogDiv.setAttribute("role", "document");

	let modalContent = document.createElement("div");
	modalContent.className = "modal-content";

	let modalHeader = document.createElement("div");
	modalHeader.className = "modal-header";

	let modalTitle = document.createElement("h5");
	modalTitle.className = "modal-title";
	modalTitle.id = "itemModal" + item['id'] + "LongTitle";
	modalTitle.innerHTML = item['name'];
	modalHeader.appendChild(modalTitle);

	let modalCloseButton = document.createElement("button");
	modalCloseButton.setAttribute("type", "button");
	modalCloseButton.className = "close";
	modalCloseButton.setAttribute("data-dismiss", "modal");
	modalCloseButton.setAttribute("aria-label", "Close");

	let modalCloseButtonSpan = document.createElement("span");
	modalCloseButtonSpan.setAttribute("aria-hidden", "true")
	modalCloseButtonSpan.innerHTML = "&times;";
	modalCloseButton.appendChild(modalCloseButtonSpan);

	modalHeader.appendChild(modalCloseButton);

	modalContent.appendChild(modalHeader);

	let modalBody = document.createElement("div");
	modalBody.className = "modal-body";

	let modalItemDescription = document.createElement("p");
	modalItemDescription.innerHTML = item['description'];
	modalBody.appendChild(modalItemDescription);

	// Loop through fields and list them in the modal window
	for (var key in item) {
		if (key != "name" && key != "description" && key != "id") {
			let modalContent = document.createElement("p");

			if (item[key] == true) {
				modalContent.innerHTML = key + ": " + 'Yes';
			}
			else if (item[key] == false) {
				modalContent.innerHTML = key + ": " + 'No';
			}
			else {
				modalContent.innerHTML = key + ": " + item[key];
			}

			modalBody.appendChild(modalContent);
		}
	}

	modalContent.appendChild(modalBody);
	modalDialogDiv.appendChild(modalContent);
	modalDiv.appendChild(modalDialogDiv);
	itemCollumn.appendChild(modalDiv);
	// Set up element hierarchy 
	
	itemCardDiv.appendChild(itemCardBody);
	itemCollumn.appendChild(itemCardDiv);
	row.appendChild(itemCollumn);
}