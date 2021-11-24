// GLOBAL VARIABLES
const nrOfItemsToLoad = 20;
var startingPoint = 0;
var endPoint = nrOfItemsToLoad;

var itemsLoaded = 0;
var everythingLoaded = false;


var numberOfFields = 1;
var clickedFilters = {}; // Store all filter selections to be used by displayItems()

// Get cookie value
function getCookie(name) {
	let cookieValue = null;

	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');

		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();

			// Check if cookie string begins with required name
			if (cookie.substring(0, name.length +1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length +1));
				break;
			}
		}
	}
	return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
	
	let url = window.location.href;
	let urlArray = url.split('/');
	let lastUrlElement = urlArray[urlArray.length - 1];

	// BY DEFAULT - List all collections if we are in the right section
	if (document.querySelector("#collections")) {
		// Check if this was accessed through quick access bar
		if (lastUrlElement == 'view_collection') {
			listCollections();
		}
		else {
			quickAccessCollection(parseInt(lastUrlElement));
		}
	}

	//Browse Collections from the Nav Bar
	navbarCollectionList();
	
	// Create Collection -- Add Field Button
	if (document.querySelector("#newField")) {
		document.querySelector("#newField").addEventListener('click', addNewField);	
	}

	
	// Search Button
	if (document.querySelector('#collections'))
	{
		document.querySelector('#search').style.display = "block";
	}
	else {
		document.querySelector('#search').style.display = "none";
	}
	document.querySelector("#search").addEventListener('input', function() {
		searchFilter(document.querySelector("#search"));
	})

	// Infinite scroll
	window.onscroll = () => {
		// Check if user has reached the bottom of the page
		if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
			console.log("BOTTOM");
			if (everythingLoaded == false) {
				loadNextItems(parseInt(lastUrlElement))
			}
		}
	}
});


function searchFilter(searchBar) {
	let searchResult = [];
	// Fetch API
	fetch('/get_collections')
	.then(response => response.json())
	.then(collections => {
		collections.forEach(function(collection) {
			collection['items'].forEach(function(item) {
				if (item['name'].toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").startsWith(searchBar.value)) {
					searchResult.push(item);
					return;
				}
			})
		})
		if (searchBar.value.length > 0) {
			// Clear screen and display search results
			if (document.querySelector('#collections')) {
				document.body.removeChild(document.querySelector('#collections'));
				searchHeader(document.body);
			}
			
			displayItems(searchResult);
		}
		else {
			location.reload();
		}
	})
}


function searchHeader(parent) {
	let headerJumbotron = document.createElement("div");
	headerJumbotron.className = "jumbotron";

	let searchTitle = document.createElement("h1");
	searchTitle.className = "display-5";
	searchTitle.innerHTML = "Search Results";

	headerJumbotron.appendChild(searchTitle);
	parent.appendChild(headerJumbotron);
}


function quickAccessCollection(collection_id) {
	// Fetch API
	fetch('/get_collections')
	.then(response => response.json())
	.then(collections => {
		collections.forEach(function(collection) {
			if (collection['id'] == collection_id) {
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

		// Determine how many rows are needed for 4/row
		let nrOfRows = determineNrOfRows(collections);

		for (let i = 0; i < nrOfRows; i++) {
			// For each 4 items create a new row and modify the array for the next 4 items
			let row = collections.slice(0, 4);
			createRow(row, mainDivContainer, "collection");
			collections.splice(0, 4);
		}

		// Create last row for the remaining collections that were left out
		if (collections.length > 0) {
			createRow(collections, mainDivContainer, "collection");
		}

		mainDiv.appendChild(mainDivContainer);
	})
}


function createCollectionCard(collection, row) {
	let colDiv = document.createElement("div");
	colDiv.className = "col-sm col-md-3";
	colDiv.style.padding = "1em";

	let cardDiv = document.createElement("a");
	cardDiv.setAttribute("href", "../view_collection/" + collection['id'])
	cardDiv.className = "card";
	cardDiv.className = "card h-100 w-100"; // h-100 creates a fixed card height for the entire 100% height of the column

	let cardBodyDiv = document.createElement("div");
	cardBodyDiv.className = "card-body";

	let cardTitle = document.createElement("h5");
	cardTitle.className = "card-title text-center";
	cardTitle.innerHTML = collection['name'];
	cardBodyDiv.appendChild(cardTitle);

	let cardText = document.createElement("p");
	cardText.className = "card-text text-center";
	cardText.innerHTML = collection['description'];
	cardBodyDiv.appendChild(cardText);

	

	// Append everything to the upper nodes
	cardDiv.appendChild(cardBodyDiv);
	colDiv.appendChild(cardDiv);

	row.appendChild(colDiv);
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
	// Clear screen
	parrent.innerHTML = "";
	// Create main div
	let clickedCollection = document.createElement("div");
	clickedCollection.id = "collection";
	clickedCollection.className = "jumbotron jumbotron-fluid";

	// Add "Delete" button to remove collection
	deleteCollection(collection, clickedCollection, "collection");

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
	let buttonParagraph = document.createElement("div");
	buttonParagraph.className = "lead d-flex";

	// Add item button
	let addButton = document.createElement("a");
	addButton.className = "btn btn-primary btn-lg";
	addButton.setAttribute("href", "../add_item/" + collection['id']);
	addButton.setAttribute("role", "button");
	addButton.innerHTML = "Add item";

	// Upload Images button
	let uploadImages = document.createElement("a");
	uploadImages.className = "btn btn-primary btn-sm ml-auto";
	uploadImages.setAttribute("href", "../upload_images/" + collection['id']);
	uploadImages.setAttribute("role", "button");
	uploadImages.innerHTML = "Upload Images";

	// Set element hierarchy
	buttonParagraph.appendChild(addButton);
	buttonParagraph.appendChild(uploadImages);

	containerDiv.appendChild(collectionName);
	containerDiv.appendChild(collectionDescription);
	containerDiv.appendChild(buttonParagraph);

	clickedCollection.appendChild(containerDiv);

	parrent.appendChild(clickedCollection);

	// Filters
	console.log(collection);
	itemFilter(collection['items'], collection, clickedCollection);

	// Display items

	// If user is not using filters or search, display items 20 at a time and use infinite scroll
	if ((clickedFilters.length == 0) && (document.querySelector('#search').value.length == 0)) {
		endPoint = startingPoint + nrOfItemsToLoad;
		displayItems(collection['items'].slice(startingPoint, endPoint), collection);
		startingPoint = startingPoint + nrOfItemsToLoad
	}
	// If user is using filters or search, display everything at once
	else {
		displayItems(collection['items'], collection);
	}
}


function displayItems(itemSource, collection) {
	
	// Clone the items array to preserve the original
	let itemSourceClone = Array.from(itemSource);
	let itemsContainer;

	// Clear screen of previous items
	if (document.querySelector("#itemList")) {
		// Check if user reached bottom of the page, if so load the next batch of items
		if ((window.innerHeight + window.scrollY >= document.body.offsetHeight) && (document.body.offsetHeight > window.innerHeight)) {
			
			itemsContainer = document.querySelector("#itemList");
		}
		else {
			document.body.removeChild(document.querySelector("#itemList"));
			itemsContainer = document.createElement("div");
			itemsContainer.className = "container-fluid";
			itemsContainer.id = "itemList";
		}
	}
	else {
		itemsContainer = document.createElement("div");
		itemsContainer.className = "container-fluid";
		itemsContainer.id = "itemList";
	}

	// Items

	// Manage filter options
	let items = filterItemList(itemSourceClone);

	console.log("NR OF ITEMS: " + itemSourceClone.length);
	console.log("NR OF FILTERED ITEMS: " + items.length);
	
	// Determine how many rows are needed
	let nrOfRows = determineNrOfRows(items);

	// Create html elements needed to display items
	//let itemsContainer = document.createElement("div");
	//itemsContainer.className = "container-fluid";
	//itemsContainer.id = "itemList";

	for (let i = 0; i < nrOfRows; i++) {
		// For each 4 items create a new row and modify the array for the next 4 items
		let row = items.slice(0, 4);
		createRow(row, itemsContainer, "item");
		items.splice(0, 4);
		itemsLoaded += 4
	}


	// Create last row for the remaining items
	if (items.length > 0) {
		createRow(items, itemsContainer, "item");
		itemsLoaded += items.length
	}

	// Check if all items have been loaded on screen
	if (collection) {
		console.log(itemsLoaded);
		console.log(collection['items'].length);
		if (itemsLoaded >= collection['items'].length) {
			everythingLoaded = true;
		}
	}

	document.body.appendChild(itemsContainer);

	if (Object.keys(clickedFilters).length > 0) {
		console.log(Object.keys(clickedFilters).length > 0);
		console.log(clickedFilters);
		console.log("Items have been filtered!!! Need new filter options!!!");

		// TO DO --> Update filter options to new item list
		let filterParentElement = document.querySelector('#filterContainer').parentElement;
		let filteredItems = filterItemList(itemSource);

		// remove old filter section from DOM and enter a new one
		filterParentElement.removeChild(document.querySelector('#filterContainer'));
		itemFilter(filteredItems, collection, filterParentElement);
	}
}

function loadNextItems(collection_id) {
	// Fetch API
	fetch('/get_collections')
	.then(response => response.json())
	.then(collections => {
		collections.forEach(function(collection) {
			if (collection['id'] == collection_id) {
				displayCollection(collection, document.querySelector("#collections"));
				return
			}
		})
	})
}


function filterItemList(array) {
	let items = [];

	// Check if there are any active filters, if there are the new filtered array will be stored in items
	if (Object.keys(clickedFilters).length > 0) {
		for (let item in array) {
			// count number of times the field values matched with the filter values, if an item matches all filters it is added to the new list
			let count = 0;

			for (let field in clickedFilters) {
				// Check if the item matches current filter value in clickedFilters, if it does then count += 1
				if (clickedFilters[field] == array[item][field]) {
					count += 1;
					// check if this is the last field in clickedFilters, if the match count maches the clicked filter length, the item is added to the new list
					if (count == Object.keys(clickedFilters).length) {
						items.push(array[item]);	
					}
				}
				
			}
		}
		return items;
	}
	else {
		// No active filters, all items are in the returned array
		return array;
	}
}


function createRow(items, containerDiv, type) {
	// Check if dealing with items or collections and create row

	if (type == "item") {
		let itemRow = document.createElement("div");
		itemRow.className = "row";
		//itemRow.style.padding = "1em";

		// Item Collumns
		items.forEach(function(item) {
			createItemCard(item, itemRow);
			containerDiv.appendChild(itemRow);
		});
	}
	else if (type == "collection") {
		// Create row div
		let rowDiv = document.createElement("div");
		rowDiv.className = "row";

		// Create columns of cards in the row
		items.forEach(function(item) {
			createCollectionCard(item, rowDiv);
			containerDiv.appendChild(rowDiv);
		})
	}

}


function createModalPopup(item, parent) {
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


	// Create a carousel slider for images
	let carousel = document.createElement("div");
	carousel.id = "carouselId" + item['id'];
	carousel.className = "carousel slide";
	carousel.setAttribute("data-ride", "carousel")
	carousel.setAttribute("style", "overflow:hidden") // Prevents sliding images to spill outside of the div

	let carouselInner = document.createElement("div");
	carouselInner.className = "carousel-inner";

	// Create carousel controlls

	// Previous
	let carouselPrev = document.createElement("a");
	carouselPrev.className = "carousel-control-prev";
	carouselPrev.setAttribute("href", "#" + carousel.id);
	carouselPrev.setAttribute("role", "button");
	carouselPrev.setAttribute("data-slide", "prev")

	let spanPrevIcon = document.createElement("span");
	spanPrevIcon.className = "carousel-control-prev-icon";
	spanPrevIcon.setAttribute("aria-hidden", "true");

	let spanPrev = document.createElement("span");
	spanPrev.className = "sr-only";
	spanPrev.innerHTML = "Previous";

	carouselPrev.appendChild(spanPrevIcon);
	carouselPrev.appendChild(spanPrev);

	// Next
	let carouselNext = document.createElement("a");
	carouselNext.className = "carousel-control-next";
	carouselNext.setAttribute("href", "#" + carousel.id);
	carouselNext.setAttribute("role", "button");
	carouselNext.setAttribute("data-slide", "next");

	let spanNextIcon = document.createElement("span");
	spanNextIcon.className = "carousel-control-next-icon";
	spanNextIcon.setAttribute("aria-hidden", "true");

	let spanNext = document.createElement("span");
	spanNext.className = "sr-only";
	spanNext.innerHTML = "Next";

	carouselNext.appendChild(spanNextIcon);
	carouselNext.appendChild(spanNext);

	carousel.appendChild(carouselInner);
	carousel.appendChild(carouselNext);
	carousel.appendChild(carouselPrev);

	let nrOfImagesLoaded = 0;


	// Loop through fields and list them in the modal window
	for (var key in item) {
		if (!["name", "description", "id", "col_id", "img_missing"].includes(key)) {
			let modalContent = document.createElement("p");

			// Check if value is of type Boolean
			if (typeof item[key] == 'boolean') {
				if (item[key] == true) {
					modalContent.innerHTML = key + ": " + 'Yes';
				}

				else if (item[key] == false) {
					modalContent.innerHTML = key + ": " + 'No';
				}
			}
			

			// Check if we are dealing an array (All image urls are store in an array under the image field)
			else if (Array.isArray(item[key])) {
				item[key].forEach(imgUrl => {
					// Create carousel item
					let carouselItem = document.createElement("div");

					if (nrOfImagesLoaded == 0) {
						carouselItem.className = "carousel-item active";
					}
					else {
						carouselItem.className = "carousel-item";
					}
					
					let image = document.createElement("img");
					image.className = "img-fluid";
					image.src = imgUrl;
					carouselItem.appendChild(image);
					carousel.appendChild(carouselItem);
					nrOfImagesLoaded += 1;
				})


				
			}
				
			else {
				modalContent.innerHTML = key + ": " + item[key];
			}

			modalBody.appendChild(modalContent);
		}
	}

	modalContent.appendChild(modalBody);
	modalContent.appendChild(carousel);
	modalDialogDiv.appendChild(modalContent);
	modalDiv.appendChild(modalDialogDiv);

	

	// Create div container for delete and edit buttons

	let itemButtons = document.createElement("div");
	itemButtons.className = "itemButtons btn-toolbar";

	// Add edit button
	addEditButton(item, itemButtons);

	// Add delete button
	addDeleteButton(item, itemButtons);

	modalContent.appendChild(itemButtons);
	

	parent.appendChild(modalDiv);
}


function createItemCard(item, row) {

	// Set up divs
	let itemCollumn = document.createElement("div");
	itemCollumn.className = "col-sm col-md-3";
	itemCollumn.style.padding = "1em";

	// Create card elements starting with an "a" tag to trigger a modal pop-up
	let itemCardDiv = document.createElement("a");
	itemCardDiv.className = "card border-dark h-100"; // h-100 creates a fixed card height for the entire 100% height of the column
	itemCardDiv.setAttribute("type", "button");
	itemCardDiv.setAttribute("data-toggle", "modal");
	itemCardDiv.setAttribute("data-target", "#itemModal" + item['id']);

	// If card is clicked reset the 'confirm delete' button
	itemCardDiv.addEventListener("click", function() {
		// Reset delete button
		if (document.querySelector('#confirmDelete'+ item['id'])) {
			// create delete button
			document.querySelector('#delete' + item['id']).style.display = "block";
			// remove confirm button
			document.querySelector('#confirmDelete' + item['id']).remove();
		}
	})

	let itemCardBody = document.createElement("div");
	itemCardBody.className = "card-body";

	let itemCardTitle = document.createElement("h5");
	itemCardTitle.className = "card-title";
	itemCardBody.appendChild(itemCardTitle);

	let itemCardDescription = document.createElement("p");
	itemCardDescription.className = "card-text";
	itemCardBody.appendChild(itemCardDescription);

	// Insert content
	let image = document.createElement("img");

	// Name and Description
	itemCardTitle.innerHTML = item['name'];
	itemCardDescription.innerHTML = item['description']

	for (var key in item) {
		if (!["name", "description", "id", "col_id"].includes(key)) {
			let contentDiv = document.createElement("div");
			contentDiv.className = "content-container";

			let content = document.createElement("p");
			content.className = "card-text d-inline";

			/*
			// Check for boolean values
			if (item[key] == true) {
				content.innerHTML = key + ": " + 'Yes';
			}
			else if (item[key] == false) {
				content.innerHTML = key + ": " + 'No';
			}
			*/
			// Fill in image
			
			if (Array.isArray(item[key])) {
				if (item[key].length > 0) {
					image.className = "card-img-bottom";
					image.src = item[key][0];
				}
				else {
					image.className = "card-img-bottom";
					image.src = "/media/images/missing_image.jpg";
				}
			}
			/*
			// Fill in regula fields
			else {
				content.innerHTML = key + ": " + item[key];
			}
			*/

			contentDiv.appendChild(content);

			// Add edit button for this content type
			//addEditButton(item, contentDiv)
			itemCardBody.appendChild(contentDiv);
		}
	}

	// Set up modal pop-up
	createModalPopup(item, itemCollumn)
	// Set up element hierarchy 
	
	itemCardDiv.appendChild(itemCardBody);
	itemCardDiv.appendChild(image);
	itemCollumn.appendChild(itemCardDiv);
	row.appendChild(itemCollumn);
}

function determineNrOfRows(source) {
	// Determine how many rows are needed for 4/row

	if (Math.floor(source.length / 4) <= 1) {
		return 1;
	}

	else {
		return Math.floor(source.length / 4);
	}
}


function addDeleteButton(source, parent) {
	let button = document.createElement("button");
	button.style.display = "block";
	button.setAttribute("type", "button");
	button.className = "btn btn-warning btn-sm";
	button.innerHTML = "Delete";
	button.id = "delete" + source["id"];
	parent.appendChild(button);

	button.addEventListener("click", function() {
		button.style.display = "none";
		confirmDelete(source, parent, "item", button);
		})
}


function confirmDelete(source, parent, element, delButton) {
	// Create a confirm button to prevent accidentally deleting something

	let confirm = document.createElement("button");
	confirm.setAttribute("type", "button");
	confirm.className = "btn btn-danger btn-sm";
	confirm.innerHTML = "Confirm Deletion";

	// Check if the button is deleting a collection item or a full collection

	if (element == "item") {
		confirm.id = "confirmDelete" + source['id']
		confirm.setAttribute("data-dismiss", "modal");

		confirm.addEventListener("click", function() {
			fetch("/delete_item", {
				method: 'PUT',
				mode: 'same-origin',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie('csrftoken')
				},
				body: JSON.stringify({
					'itemId': source['id']
				})
			})
			.then(function() {
				let parentCol = parent.parentElement.parentElement.parentElement.parentElement;
				let parentRow = parentCol.parentElement;

				console.log(parentCol);
				console.log(parentRow);

				parentRow.removeChild(parentCol);	
			})

		})
		parent.appendChild(confirm);
	}
	else if (element == "collection") {
		confirm.id = "confirmDeleteCollection" + source['id'];

		confirm.addEventListener("click", function() {
			fetch("/delete_collection", {
				method: 'PUT',
				mode: 'same-origin',
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
					'X-CSRFToken': getCookie('csrftoken')
				},
				body: JSON.stringify({
					'collectionId': source['id']
				})
			})
			.then(function () {
				console.log("API went through")

				// Check if this was accessed through quick access bar / the main menu and redirect to collection list after deletion
				let url = window.location.href;
				let urlArray = url.split('/');
				let lastUrlElement = urlArray[urlArray.length - 1];

				if (lastUrlElement == 'view_collection') {
					location.reload();
				}
				else {
					urlArray.pop();
					console.log(urlArray);
					urlArray.join('/');
					console.log(urlArray);
					window.location.href = urlArray.join('/');
					console.log(location);
					//urlArray.reload();
				}
			})
		})
		console.log(parent);
		console.log(delButton);
		delButton.parentElement.replaceChild(confirm, delButton);
	}
}


function addEditButton(source, parent) {
	// Edit item - modify the details saved inside the database about the item

	let button = document.createElement("a");
	button.setAttribute("href", "../edit_item/" + source['id']);
	button.className = "btn btn-link btn-sm d-inline";
	button.innerHTML = "Edit";
	button.id = "edit" + source['id'];

	parent.appendChild(button);
}


function deleteCollection(source, parent) {
	// Function to delete the collection from the database

	let containerDiv = document.createElement("div");
	containerDiv.className = "d-flex justify-content-end";

	let button = document.createElement("button");
	button.className = "btn btn-outline-danger btn-sm";
	button.innerHTML = "Delete";

	button.addEventListener("click", function () {
		confirmDelete(source, parent, "collection", button);
	})

	containerDiv.appendChild(button);
	parent.appendChild(containerDiv)
}


function itemFilter(sourceItems, sourceCollection, parent) {
	// Set up useful variables
	let fields = sourceCollection['fields'];
	let items = sourceItems;

	// Create div container for filters
	let filterContainer = document.createElement("div");
	filterContainer.className = "container-fluid";
	filterContainer.id = "filterContainer";

	// Create row to store all filter dropdown boxes in a line
	let rowDiv = document.createElement("div");
	rowDiv.className = "row";

	// Loop through all the fields and make a drop down selector for each one
	for (var key in fields) {
		// Container div for each selector
		if (fields[key] != "image") {
			let selectorContainer = document.createElement("div");
		selectorContainer.className = "col-sm col-md-2";
		selectorContainer.setAttribute("style", "1em");

		// Create Selector
		let selector = document.createElement("select");
		selector.className = "form-control";
		selector.id = key;

		// Create options -- TEST -- Need to loop through all the variations of each field
		let option = document.createElement("option");
		option.setAttribute("selected", "selected");

		// If 'key' is a selected filter show its selected option
		if (clickedFilters[key] != undefined) {
			option.innerHTML = key + ": " + clickedFilters[key];
			option.setAttribute("disabled", "disabled");
			selector.appendChild(option);

			// Create one aditional option called 'All' to remove this field from clickedFilters and stop filtering option by it
			let rmFilterOption = document.createElement("option");
			rmFilterOption.innerHTML = key + ": All";
			selector.appendChild(rmFilterOption);
		}
		else {
			option.innerHTML = key + ": All";
			option.setAttribute("disabled", "disabled");
			selector.appendChild(option);

			// Get field entries as options
			let mentionedValues = [];

			for (let i in items) {
				if (! mentionedValues.includes(items[i][key])) {
					// Create options element and add this value to mentionedValues after to avoid repetition
					let option = document.createElement("option");
					option.innerHTML = items[i][key];
					selector.appendChild(option);
					mentionedValues.push(items[i][key]);
				}
			}
		}


		// TEST --> Add event and read filter selection
		selector.addEventListener("change", function() {
			console.log(selector.value);

			if (selector.value.slice(-3) == "All"){
				// If user selected 'All' in a field filter, remove that field from clickedFilter, stop filtering by that field and reset dropdown options for it
				delete clickedFilters[selector.id];
				
				// Remove old filter options 
				let filterParentElement = document.querySelector('#filterContainer').parentElement;
				filterParentElement.removeChild(document.querySelector('#filterContainer'));

				// Replace with updated filtered options
				itemFilter(sourceCollection['items'], sourceCollection, parent);

				// Update displayed items
				displayItems(sourceCollection['items'], sourceCollection);
			}
			else {
				// Add selected filter to the global ckickedFilters array
				clickedFilters[selector.id] = selector.value;
				// Display item list matching the clicked filters
				displayItems(sourceItems, sourceCollection);
			}

			
		})

		// Set Hierarchy
		selectorContainer.appendChild(selector);
		rowDiv.appendChild(selectorContainer);
		}
		
	}

	// Set Hierarchy
	filterContainer.appendChild(rowDiv);
	parent.appendChild(filterContainer);
}