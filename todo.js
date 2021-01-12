const { profileEnd } = require('console');
const fs = require('fs');

// save: save current list
function save(data=[], file) {
  return fs.writeFileSync(file, data)
}

// load: load from JSON
function load(file) {
  const text = fs.readFileSync(file, 'utf-8')
  return text.trim()
}

// help: list options
function help() {
  return process.stdout.write(
    `Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics`
  )
}

// built-in functions
const func = {

  // list: display all entries
  ls: function() {
    try{
      let data = load(file='todo.txt').split('\n')
      if(data.length == 0){
        process.stdout.write("There are no pending todos!")
      }
      for(let i=data.length-1; i>=0; i--){
        process.stdout.write("["+`${i+1}`+"] "+`${data[i]}`+"\n")
      }
    }
    catch(err){
      process.stdout.write("There are no pending todos!")
    }
  },

  // add: add entry
  add: function(...title) {

    if(title === undefined || title==''){
      process.stdout.write(`"Error: Missing todo string. Nothing added!"`)
      return
    }
    // let data = load()
    fs.appendFile('todo.txt', title+"\n", function(err) {
      if (err) throw err;
    });
    process.stdout.write(`Added todo: "${title}"`)
    return
  },

  // remove: remove entry
  del: function(term) {
    if(term == undefined){
      process.stdout.write(`"Error: Missing NUMBER for deleting todo."`)
      return
    }
    try{
      term=term-1
      let data = load(file='todo.txt').split('\n')
      if(term > data.length-1 || term == -1 || data[0] == ''){
        process.stdout.write(`"Error: todo #${term+1} does not exist. Nothing deleted."`)
        return
      }

      data.splice(term,1)
      process.stdout.write(`"Deleted todo #${term+1}"`)
      return save(data.join("\n")+"\n",file="todo.txt")
    }
    catch(err){
      process.stdout.write(`"Error: todo #${term} does not exist. Nothing deleted."`)
    }
  },

  // check: check entry
  done: function(id) {
    if(id == undefined){
      process.stdout.write("Error: Missing NUMBER for marking todo as done.")
      return
    }
    try{
      id = id-1
      let data = load('todo.txt').split('\n')
      if(id+1 > data.length || id+1 == 0 || data[0] == ''){
        process.stdout.write(`"Error: todo #${id+1} does not exist."`)
        return
      }
      var todo=data.splice(id,1)
      process.stdout.write(`"Marked todo #${id+1} as done."`)
      if(data.length == 0){
        save("",file="todo.txt")
      }
      else{
        save(data.join("\n")+"\n",file="todo.txt")
      }
      var date = new Date()
      var done = "x "+date.toISOString().split('T')[0]+" "+todo
      fs.appendFile("done.txt",done+"\n", function(err){
        if (err) throw err;
      });

      return
    }
    catch(err){
      throw err
      process.stdout.write(`"Error: todo #${id+1} does not exist."`)
    }
  },

  report: function(){
    try{
      let pending_data = load('todo.txt').split('\n')
      var pcount = pending_data.length
    }
    catch(err){
      var pcount = 0
    }

    try{
      let complete_data = load('done.txt').split('\n')
      var ccount = complete_data.length
    }
    catch(err){
      var ccount = 0
    }
    var date = new Date()
    process.stdout.write(`${date.toISOString().split('T')[0]} Pending : ${pcount} Completed : ${ccount}\n`)
  }

}

// Run from command-line
if (process.argv[2]) {
  const cli = process.argv[2].split(' ')
  if (func[cli[0]]) {
    func[cli[0]](process.argv[3])
  } else {
    help()
  }
} else {
  help()
}
