import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')


// const spawn = require("child_process");
// //const pythonProcess = spawn('python',["path/to/script.py", arg1, arg2, ...]);
// const pythonProcess = spawn('python',["physical_model_generator.py"]);
// pythonProcess.stdout.on('data', (data) => {
//     console.log('Pipe data from python script ...');
//     var dataToSend = data.toString();
//     print(dataToSend)
// });