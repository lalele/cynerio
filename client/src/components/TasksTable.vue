<template>
  <v-data-table :headers="headers" :items="tasks" item-key="id">
    <template v-slot:items="props">
      <td>{{ props.item.task_title }}</td>
      <td>{{ props.item.user_name }}</td>
      <td>{{ props.item.duration }}</td>
    </template>
  </v-data-table>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      headers: [
        { text: 'Task Title', value: 'task_title' },
        { text: 'User Name', value: 'user_name' },
        { text: 'Duration', value: 'duration' },
      ],
      tasks: [],
    };
  },
  mounted() {
    this.fetchTasks();
  },
  methods: {
    fetchTasks() {
      // TODO: move it to a service handler that call axios and also intercept errors
      axios.get('http://127.0.0.1:8000/api/report/tasks_duration')
        .then(response => {
          this.tasks = response.data;
        })
        .catch(error => {
          console.error('Error fetching tasks:', error);
        });
    },
  },
};
</script>
