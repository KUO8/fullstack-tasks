<template>
  <div class="container mx-auto p-4 max-w-2xl">
    <h1 class="text-3xl font-bold mb-6 flex items-center gap-2">
      appTask
      <img src="https://cdn-icons-png.flaticon.com/128/9741/9741134.png" alt="Logo" class="w-8 h-8" />
    </h1>
    <div class="mb-6 flex gap-2">
      <input v-model="newTask.title" placeholder="Enter task" class="flex-1 p-2 border rounded" />
      <button @click="addTask" class="bg-zinc-200 text-white p-2 rounded hover:bg-zinc-500">
        Add Task
      </button>
    </div>

    <div class="grid gap-3">
      <div v-for="task in tasks" :key="task.id"
        class="p-4 border rounded-lg flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 transition-all duration-200 bg-white shadow-sm hover:shadow-md"
        :class="{
      'bg-gray-50 border-gray-200': !task.completed,
      'bg-gray-100 border-gray-300': task.completed
    }">
        <div class="flex items-center gap-3 w-full sm:w-auto">
          <input type="checkbox" v-model="task.completed" @change="toggleTask(task)"
            class="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 transition-colors cursor-pointer">
          <span class="text-gray-800 break-words max-w-[200px] sm:max-w-none" :class="{
          'line-through text-gray-500': task.completed,
          'hover:text-gray-900': !task.completed
        }">
            {{ task.title }}
          </span>
        </div>

        <div class="flex gap-2 w-full sm:w-auto justify-end">
          <button @click="editTask(task)" class="px-3 py-1.5 bg-amber-100 text-amber-800 rounded-md text-sm font-medium
               hover:bg-amber-200 hover:text-amber-900
               transition-all duration-200 ease-in-out
               flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit
          </button>

          <button @click="deleteTask(task.id)" class="px-3 py-1.5 bg-red-100 text-red-800 rounded-md text-sm font-medium
               hover:bg-red-200 hover:text-red-900
               transition-all duration-200 ease-in-out
               flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Delete
          </button>
        </div>
      </div>
    </div>


    <Transition name="modal">
      <div v-if="editingTask" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md p-6">
          <h3 class="text-xl font-semibold mb-4">Edit Task</h3>
          <input v-model="editingTask.title" class="w-full p-2 border rounded mb-4" placeholder="New task title"
            @keyup.enter="saveEdit" />
          <div class="flex justify-end gap-2">
            <button @click="cancelEdit" class="bg-gray-500 text-white p-2 rounded mr-2 hover:bg-gray-600">
              Cancel
            </button>
            <button @click="saveEdit" class="bg-green-400 text-white p-2 rounded hover:bg-green-200">
              Save
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'

  const tasks = ref([])
  const newTask = ref({ title: '', completed: false })
  const editingTask = ref(null)

  const fetchTasks = async () => {
    const res = await fetch('http://localhost:8000/api/tasks')
    tasks.value = await res.json()
  }

  const addTask = async () => {
    if (!newTask.value.title.trim()) return
    await fetch('http://localhost:8000/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTask.value),
    })
    newTask.value = { title: '', completed: false }
    await fetchTasks()
  }

  const toggleTask = async (task) => {
    await fetch(`http://localhost:8000/api/tasks/${task.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: !task.completed }),
    })
    await fetchTasks()
  }

  const deleteTask = async (id) => {
    await fetch(`http://localhost:8000/api/tasks/${id}`, {
      method: 'DELETE',
    })
    await fetchTasks()
  }

  const editTask = (task) => {
    editingTask.value = { ...task }
  }

  const saveEdit = async () => {
    if (!editingTask.value.title.trim()) return
    await fetch(`http://localhost:8000/api/tasks/${editingTask.value.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingTask.value),
    })
    editingTask.value = null
    await fetchTasks()
  }

  const cancelEdit = () => {
    editingTask.value = null
  }

  onMounted(fetchTasks)
</script>

<style>
  .modal-enter-active,
  .modal-leave-active {
    transition: opacity 0.3s;
  }

  .modal-enter-from,
  .modal-leave-to {
    opacity: 0;
  }
</style>