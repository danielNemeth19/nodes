// Example of call of the function to make the table tree-like:
// tableToTree('#myTable', 'opened', 'visible', '<span class="toggle"></span>');

function tableToTree(table_Selector, tr_OpenedClass, tr_VisibleClass, tr_ToggleButton) {

	// Table elements variables
	var table = document.querySelector(table_Selector);
	var trs = document.querySelectorAll(table_Selector + " tr");

	// Add the buttons above the table
	var buttons = document.createElement('div');
	buttons.innerHTML = '<button>[‒] All</button><button>[+] All</button>';
	table.insertBefore(buttons, table.childNodes[0]);
	buttons = buttons.querySelectorAll('button');
	// Add the actions of these buttons
	buttons[0].addEventListener("click", function() {
		trs.forEach(function(elm) {
			elm.classList.remove(tr_OpenedClass);
			elm.classList.remove(tr_VisibleClass);
		});
	});
	buttons[1].addEventListener("click", function() {
		trs.forEach(function(elm) {
			if (elm.innerHTML.includes(tr_ToggleButton))
				elm.classList.add(tr_OpenedClass);
			elm.classList.add(tr_VisibleClass);
		});
	});
	function nextTr(row){
		while ((row=row.nextSibling) && row.nodeType != 1) {
			return row
		}
	}
	trs.forEach(function(tr, index){
		if (index < trs.length - 1) {
			if (+tr.getAttribute("level") < +trs[index + 1].getAttribute("level")) {
				var td1 = tr.firstElementChild;
				td1.innerHTML = tr_ToggleButton + td1.innerHTML
			}
		}
	});
}

tableToTree("#myTable", 'opened', 'visible', '<span class="toggle"></span>')
