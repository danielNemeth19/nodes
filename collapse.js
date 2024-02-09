// Example of call of the function to make the table tree-like:
// tableToTree('#myTable', 'opened', 'visible', '<span class="toggle"></span>');
// after refactoring it only needs the jquery row selector

function tableToTree($rowSelector) {
	$rowSelector.each(function(_, tr) {
		let $tr = $(tr)
		let level = parseInt($tr.attr("level"))
		if (isNaN(level)) {
			return true;
		}
		let $nextRow = $tr.closest('tr').next('tr')
		let nextLevel = parseInt($nextRow.attr("level"))

		let $td1 = $tr.find('td:first')
		let $toggleHolder = $("<span>").attr("class", "toggle-holder")
		let $smToggle = $("<input>")
			.attr("type", "checkbox")
			.attr("data-size", "mini")
			.addClass("row-toggle")
		$toggleHolder.append($smToggle)
		$td1.prepend($toggleHolder)
		if ((nextLevel - level) === 1) {
			$smToggle
			.attr("data-off", "+")
			.attr("data-on", "-")
			.attr("data-offstyle", "danger")
			.attr("data-onstyle", "success").bootstrapToggle("off")
		} else {
			$smToggle.attr("data-off", "x").bootstrapToggle("disable")
		}
		if (level === 0) {
			$smToggle.addClass("root-toggle")
		}
	})

	$('.row-toggle').change(function() {
		console.log("runs again")
		let isOpenAction = $(this).prop('checked')
		let $tr = $(this).closest('tr')
		let level = parseInt($tr.attr("level"))
		$tr.nextAll().each(function(_, tr) {
			let $currentTr = $(tr)
			let currentLevel = parseInt($currentTr.attr('level'))
			if (currentLevel === level) {
				return false;
			}
			let levelDiff = currentLevel - level
			let $rowToggle = $currentTr.find('.row-toggle')
			if (isOpenAction && levelDiff ===1 ) {
				$currentTr.show()
			} else if (!isOpenAction && levelDiff === 1) {
				$currentTr.hide()
				$rowToggle.bootstrapToggle('off')
			}
			return true
		})
	})
}



let $rowSelector = $("#myTable tr")
tableToTree($rowSelector)
