document.addEventListener("DOMContentLoaded", function init() {
	const jsonFilePath = "../answer.json";

	fetch(jsonFilePath)
		.then((response) => response.json())
		.then((data) => renderJsonData(data))
		.catch((error) => console.error("Error fetching JSON:", error));
});

function renderJsonData(data) {
	const container = document.getElementById("json-content");
	const tasks = data.list_of_all_tasks;

	// Create table element
	const table = document.createElement("table");

	// Create table header
	const headerRow = table.insertRow();
	["Task", "Description", "Fitting Employees", "Estimated Days", "Potential Issues"].forEach((headerText) => {
		const th = document.createElement("th");
		th.textContent = headerText;
		headerRow.appendChild(th);
	});

	// Populate rows for each task
	for (const [taskName, taskData] of Object.entries(tasks)) {
		const row = table.insertRow();

		// Task Name
		const taskCell = row.insertCell();
		taskCell.textContent = taskName;

		// Description
		const descriptionCell = row.insertCell();
		descriptionCell.textContent = taskData.description;

		// Fitting Employees
		const employeesCell = row.insertCell();
		const employeesList = document.createElement("ul");
		taskData.fitting_employees.forEach((emp) => {
			const li = document.createElement("li");
			li.textContent = `${emp.role} (${emp.count})`;
			employeesList.appendChild(li);
		});
		employeesCell.appendChild(employeesList);

		// Estimated Days
		const daysCell = row.insertCell();
		const daysList = document.createElement("ul");
		const { min, most_likely, max } = taskData.estimated_days;
		["Min: " + min, "Most Likely: " + most_likely, "Max: " + max].forEach((day) => {
			const li = document.createElement("li");
			li.textContent = day;
			daysList.appendChild(li);
		});
		daysCell.appendChild(daysList);

		// Potential Issues
		const issuesCell = row.insertCell();
		const issuesList = document.createElement("ul");
		taskData.potential_issues.forEach((issue) => {
			const li = document.createElement("li");
			li.textContent = issue;
			issuesList.appendChild(li);
		});
		issuesCell.appendChild(issuesList);
	}

	// Append the table to the container
	container.appendChild(table);
}
