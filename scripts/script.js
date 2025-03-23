async function handleSubmit(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);

  try {
    const response = await fetch("/submit", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to process the request");
    }

    const result = await response.json();

    const responseContainer = document.getElementById("response");

    responseContainer.innerHTML = "";

    if (result.data && result.data.length > 0) {
      const table = document.createElement("table");
      table.style.border = "1px solid black";
      table.style.borderCollapse = "collapse";
      table.style.width = "100%";

      const headers = Object.keys(result.data[0]);
      const headerRow = document.createElement("tr");
      headers.forEach((header) => {
        const th = document.createElement("th");
        th.textContent = header;
        th.style.border = "1px solid black";
        th.style.padding = "8px";
        th.style.textAlign = "left";
        headerRow.appendChild(th);
      });
      table.appendChild(headerRow);

      result.data.forEach((row) => {
        const tableRow = document.createElement("tr");
        headers.forEach((header) => {
          const td = document.createElement("td");
          td.textContent = row[header];
          td.style.border = "1px solid black";
          td.style.padding = "8px";
          tableRow.appendChild(td);
        });
        table.appendChild(tableRow);
      });

      responseContainer.appendChild(table);
    } else {
      responseContainer.textContent = result.message || "No data found.";
    }
  } catch (error) {
    document.getElementById("response").textContent = `Error: ${error.message}`;
  }
}
