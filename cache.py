# tasks - Task management library.
# Recent tasks module.
# Author: Julian Ailan
# ===================================


class Queue(object):
    """FIFO data structure, implemented using lists."""
    def __init__(self, size):
        self.queue = []
        self.max_size = size

    @property
    def length(self):
        return len(self.queue)

    def __contains__(self, data):
        return data in self.queue

    def push(self, data):
        if self.length == self.max_size:
            self.queue.pop(0)
        self.queue.append(data)

    def pop(self):
        return self.queue.pop()

    def empty(self):
        del self.queue[:]


class TaskCache(Queue):
    """Queue for rapidly access recent tasks."""
    def __init__(self, size, *initial_tasks):
        super(TaskCache, self).__init__(size)
        if initial_tasks:
            for task in initial_tasks:
                if task not in self.queue:
                    super(TaskCache, self).push(task)

    def __contains__(self, data):
        for task in self.queue:
            if task.info["identifier"] == data.info["identifier"]:
                return True
        return False

    def push(self, data):
        if data in self:
            print("Won't add repeated item to cache. If you want to update"
                  " any of its aspect please use update().")
        else:
            super(TaskCache, self).push(data)

    def update(self, data, new_state=None):
        for index in xrange(self.length):
            task = self.queue[index]
            ids_match = task.info["identifier"] == data.info["identifier"]
            tables_match = task.table == data.table
            if ids_match and tables_match:
                for key in data.info.keys():
                    task.info[key] = data.info[key]
                if new_state:
                    print("Task moved from table {} to table"
                          " {}.").format(task.table, new_state)
                    task.table = new_state
                self.queue[index], self.queue[-1] = (self.queue[-1],
                                                     self.queue[index])
                break
        print("There is no record with the same identifier as the "
              "given one.")
