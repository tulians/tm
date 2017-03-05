# tm
`tm` is a tool developed in pure Python 3 that allows you to manage and track the development of a project by defining **tasks**. These tasks represent features, and are synchronized with your project's *Git* repository, so that each time you create or complete a task a branch is created or merged, respectively. The branch management is performed by the tool itself, you only have to indicate when you started or completed the task.

### Usage
#### Project initialization
Once your local Git repository is initialized and a remote added, then `tm` must be *initialized* to manage the project's tasks:
```sh
$ cd <project_dir>
$ tm init
Task manager initialized in project.
```
After running `tm init` a log file is created along with the tasks database.

#### Task creation
When a new feature is needed, a task should be created. The creation of a task involves adding a new entry to the tasks database. There are four attributes that must be completed to successfully create the task: its unique *identifier* (used to also identify the feature branch), a verbose *description* of the task (which will then be used as commit message), a *list of tasks* this new task may depend on and its *priority*.
```sh
$ tm create
New task creation.

Identifier: <unique_id>
Description: <commit_message>
Depends from: <tasks_to_complete_first>
Priority: <integer>
Task successfully created.
```
#### Start a task
To start working on a created task you must use the unique *identifier* defined in the task creation:
```sh
$ tm start <unique_id>
...
Task successfully labels as started.
```
After this point a new branch named after the *identifier* value is created. This branch is the merged with `master`/`develop` when labeled as *completed*. If a second new task is created and then started before the previous one has been labeled as completed, the merging will then be done with the branch name of the first incomplete task.

#### Completed Task
Once you completed the feature the task represents, you are ready to label it as *completed*. By doing this the branch in which this task was being developed gets merged with `master`/`develop`.
```sh
$ tm completed <unique_id>
...
Task successfully labeled as completed.
```

### Installation
Clone `tm` using
```sh
$ git clone https://github.com/tulians/tm
```
Extract the files from the compressed file and run:
```sh
$ python3 tm/config.py [-installation_and_executable_dir]
```

### Todos
  - Add an action to perform *partial pushes* to the remote repository even though the task is still not complete.
  - Add `master`/`develop` branches to merge to.

### Contact
This project is under development, so if you found any aspect that can be optimized or found a bug that must be fixed, please open an issue. Alternatively, you can contact me by e-mail on jtulians@gmail.com.

### License
MIT
