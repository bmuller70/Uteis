import tkinter as tk
import json

class Task:
    def __init__(self, name, status):
        self.name = name
        self.status = status

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, status):
        task = Task(name, status)
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def change_status(self, task, new_status):
        task.status = new_status

class TaskGUI:
    def __init__(self, manager):
        self.manager = manager
        self.window = tk.Tk()
        self.window.title("Gerenciador de Tarefas")

        # Widgets da janela
        self.task_listbox = tk.Listbox(self.window, height=10)
        self.task_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        self.task_name_label = tk.Label(self.window, text="Nome da tarefa:")
        self.task_name_label.pack(padx=10, pady=(10, 0))

        self.task_name_entry = tk.Entry(self.window)
        self.task_name_entry.pack(padx=10)

        self.task_status_label = tk.Label(self.window, text="Status da tarefa:")
        self.task_status_label.pack(padx=10, pady=(10, 0))

        self.task_status_entry = tk.Entry(self.window)
        self.task_status_entry.pack(padx=10)

        self.add_task_button = tk.Button(self.window, text="Adicionar tarefa", command=self.add_task)
        self.add_task_button.pack(padx=10, pady=10)

        self.remove_task_button = tk.Button(self.window, text="Remover tarefa", command=self.remove_task)
        self.remove_task_button.pack(padx=10, pady=10)

        self.change_status_button = tk.Button(self.window, text="Alterar status", command=self.change_status)
        self.change_status_button.pack(padx=10, pady=10)

        # Carregar tarefas do arquivo JSON
        self.load_tasks()

        # Loop da janela
        self.window.mainloop()

    def save_tasks(self):
        data = [{"name": t.name, "status": t.status} for t in self.manager.tasks]
        with open("tasks.json", "w") as f:
            json.dump(data, f)

    def add_task(self):
        name = self.task_name_entry.get()
        status = self.task_status_entry.get()
        self.manager.add_task(name, status)
        self.task_listbox.insert(tk.END, f"{name} - {status}")
        self.save_tasks()

    def remove_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            task_str = self.task_listbox.get(selection[0])
            name, status = task_str.split(" - ")
            task = next((t for t in self.manager.tasks if t.name == name and t.status == status), None)
            if task:
                self.manager.remove_task(task)
                self.task_listbox.delete(selection[0])
                self.save_tasks()

    def change_status(self):
        selection = self.task_listbox.curselection()
        if selection:
            task_str = self.task_listbox.get(selection[0])
            name, status = task_str.split(" - ")
            task = next((t for t in self.manager.tasks if t.name == name and t.status == status), None)
            if task:
                new_status = self.task_status_entry.get()
                self.manager.change_status(task, new_status)
                self.task_listbox.delete(selection[0])
                self.task_listbox.insert(selection[0], f"{name} - {new_status}")
                self.save_tasks()


    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                data = json.load(f)
                for task_data in data:
                    self.manager.add_task(task_data["name"], task_data["status"])
                    self.task_listbox.insert(tk.END, f"{task_data['name']} - {task_data['status']}")
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    # Criar instância do gerenciador de tarefas
    manager = TaskManager()

    # Criar instância da interface gráfica e passar o gerenciador de tarefas
    gui = TaskGUI(manager)
