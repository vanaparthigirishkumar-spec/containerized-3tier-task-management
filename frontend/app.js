/**
 * Frontend JavaScript for the Task Manager.
 *
 * Talks to the FastAPI backend through Nginx at /api. Nginx proxies
 * /api/* requests to the backend container (http://backend:8000).
 */

const API_BASE = "/api";
const taskForm = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const descriptionInput = document.getElementById("description");
const statusSelect = document.getElementById("status");
const formMessage = document.getElementById("form-message");
const tasksBody = document.getElementById("tasks-body");
const loadingEl = document.getElementById("loading");
const emptyMessage = document.getElementById("empty-message");
const errorMessage = document.getElementById("error-message");
const tasksTable = document.getElementById("tasks-table");

let tasks = []; // local cache of tasks fetched from the API

/**
 * Fetch all tasks from the backend and render them.
 */
async function loadTasks() {
    try {
        loadingEl.hidden = false;
        errorMessage.textContent = "";
        emptyMessage.hidden = true;

        const response = await fetch(`${API_BASE}/tasks`);
        if (!response.ok) {
            throw new Error(`Failed to load tasks (${response.status})`);
        }

        tasks = await response.json();
        renderTasks();
    } catch (err) {
        console.error(err);
        errorMessage.textContent = "Could not load tasks. Is the backend running?";
    } finally {
        loadingEl.hidden = true;
    }
}

/**
 * Render the current tasks array into the HTML table.
 */
function renderTasks() {
    tasksBody.innerHTML = "";

    if (tasks.length === 0) {
        emptyMessage.hidden = false;
        tasksTable.hidden = true;
        return;
    }

    emptyMessage.hidden = true;
    tasksTable.hidden = false;

    for (const task of tasks) {
        const row = document.createElement("tr");

        const statusClass = `status-${task.status.replace(" ", "_")}`;

        row.innerHTML = `
            <td>${task.id}</td>
            <td><strong>${escapeHtml(task.title)}</strong></td>
            <td>${escapeHtml(task.description || "&mdash;")}</td>
            <td><span class="status-badge ${statusClass}">${escapeHtml(task.status)}</span></td>
            <td><input type="checkbox" class="completed-checkbox" ${task.is_completed ? "checked" : ""} data-id="${task.id}"></td>
            <td>${formatDate(task.created_at)}</td>
            <td class="actions">
                <button class="actions-btn delete-btn" data-id="${task.id}" title="Delete">Delete</button>
            </td>
        `;

        tasksBody.appendChild(row);
    }

    attachRowListeners();
}

/**
 * Escape HTML to prevent XSS when rendering user-provided text.
 */
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format an ISO timestamp for display.
 */
function formatDate(isoString) {
    if (!isoString) return "&mdash;";
    return new Date(isoString).toLocaleString();
}

/**
 * Attach click listeners to checkboxes and delete buttons.
 */
function attachRowListeners() {
    document.querySelectorAll(".completed-checkbox").forEach((checkbox) => {
        checkbox.addEventListener("change", (e) => {
            const id = parseInt(e.target.dataset.id, 10);
            toggleTask(id, e.target.checked);
        });
    });

    document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", (e) => {
            const id = parseInt(e.target.dataset.id, 10);
            deleteTask(id);
        });
    });
}

/**
 * Handle the add-task form submission.
 */
taskForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    formMessage.textContent = "";

    const newTask = {
        title: titleInput.value.trim(),
        description: descriptionInput.value.trim() || undefined,
        status: statusSelect.value,
    };

    try {
        const response = await fetch(`${API_BASE}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newTask),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || `Failed to create task (${response.status})`);
        }

        const created = await response.json();
        formMessage.textContent = `Task "${created.title}" created!`;
        formMessage.style.color = "#065f46";

        // Reset form
        taskForm.reset();
        statusSelect.value = "pending";

        // Refresh list
        await loadTasks();
    } catch (err) {
        console.error(err);
        formMessage.textContent = err.message || "Failed to create task.";
        formMessage.style.color = "#dc2626";
    }
});

/**
 * Toggle completed status of a task.
 */
async function toggleTask(id, isCompleted) {
    const task = tasks.find((t) => t.id === id);
    if (!task) return;

    try {
        const response = await fetch(`${API_BASE}/tasks/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                status: isCompleted ? "completed" : "pending",
                is_completed: isCompleted,
            }),
        });

        if (!response.ok) {
            throw new Error("Failed to update task");
        }

        await loadTasks();
    } catch (err) {
        console.error(err);
        errorMessage.textContent = "Failed to update task.";
        await loadTasks(); // revert UI to server state
    }
}

/**
 * Delete a task after confirmation.
 */
async function deleteTask(id) {
    if (!confirm("Are you sure you want to delete this task?")) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/tasks/${id}`, {
            method: "DELETE",
        });

        if (!response.ok) {
            throw new Error("Failed to delete task");
        }

        await loadTasks();
    } catch (err) {
        console.error(err);
        errorMessage.textContent = "Failed to delete task.";
    }
}

// Initial load
loadTasks();
