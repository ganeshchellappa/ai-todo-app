document.addEventListener("DOMContentLoaded", () => {
  const taskList = document.getElementById("task-list");
  const addTaskBtn = document.getElementById("add-task-btn");
  const newTaskInput = document.getElementById("new-task-input");

  // Add new task
  addTaskBtn.addEventListener("click", () => {
    const description = newTaskInput.value.trim();
    if (!description) return alert("Please enter a task description.");

    fetch("/add_task", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description }),
    })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to add task.");
        return res.json();
      })
      .then(() => {
        location.reload(); // simple way to reload with new task
      })
      .catch((err) => alert(err));
  });

  // Delegate clicks on task list
  taskList.addEventListener("click", (e) => {
    const li = e.target.closest("li");
    if (!li) return;
    const taskId = li.dataset.id;

    // Delete button
    if (e.target.classList.contains("delete-btn")) {
      fetch(`/delete_task/${taskId}`, { method: "DELETE" })
        .then((res) => {
          if (!res.ok) throw new Error("Failed to delete task.");
          li.remove();
        })
        .catch((err) => alert(err));
    }

    // Translate button
    if (e.target.classList.contains("translate-btn")) {
      const select = li.querySelector(".translate-language");
      const lang = select.value;
      if (!lang) return alert("Please select a language to translate.");

      fetch(`/translate/${taskId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language: lang }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.status === "success") {
            const descSpan = li.querySelector(".task-desc");
            descSpan.textContent = data.translated;
          } else {
            alert(data.message || "Translation failed.");
          }
        })
        .catch(() => alert("Error calling translation API."));
    }
  });

  // Complete checkbox toggle
  taskList.addEventListener("change", (e) => {
    if (e.target.classList.contains("complete-checkbox")) {
      const li = e.target.closest("li");
      const taskId = li.dataset.id;
      const completed = e.target.checked;

      fetch(`/toggle_complete/${taskId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed }),
      })
        .then((res) => {
          if (!res.ok) throw new Error("Failed to update completion status.");
          if (completed) {
            li.classList.add("completed");
          } else {
            li.classList.remove("completed");
          }
        })
        .catch(() => alert("Error updating completion status."));
    }
  });
});
