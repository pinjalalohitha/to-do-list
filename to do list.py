import sqlite3

def initialize_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            category TEXT,
            due_date TEXT,
            priority INTEGER,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()
def add_task(task, category, due_date, priority):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (task, category, due_date, priority, completed)
        VALUES (?, ?, ?, ?, 0)
    ''', (task, category, due_date, priority))
    conn.commit()
    conn.close()
def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
def update_task(task_id, task, category, due_date, priority):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        UPDATE tasks
        SET task = ?, category = ?, due_date = ?, priority = ?
        WHERE id = ?
    ''', (task, category, due_date, priority, task_id))
    conn.commit()
    conn.close()
def view_tasks(filter_by=None):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    if filter_by:
        query = 'SELECT * FROM tasks WHERE ' + filter_by
        c.execute(query)
    else:
        c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks
def mark_complete(task_id):
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()


def main():
    initialize_db()
    while True:
        print("\nTo-Do List CLI")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Update Task")
        print("4. View Tasks")
        print("5. Mark Task as Complete")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            task = input("Enter task: ")
            category = input("Enter category: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = int(input("Enter priority (1-5): "))
            add_task(task, category, due_date, priority)
            print("Task added.")
        elif choice == '2':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)
            print("Task deleted.")
        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            task = input("Enter new task: ")
            category = input("Enter new category: ")
            due_date = input("Enter new due date (YYYY-MM-DD): ")
            priority = int(input("Enter new priority (1-5): "))
            update_task(task_id, task, category, due_date, priority)
            print("Task updated.")
        elif choice == '4':
            filter_by = input(
                "Enter filter (e.g., 'category = \"work\"' or 'due_date = \"2023-12-31\"') or press Enter to view all: ")
            tasks = view_tasks(filter_by if filter_by else None)
            for task in tasks:
                print(task)
        elif choice == '5':
            task_id = int(input("Enter task ID to mark as complete: "))
            mark_complete(task_id)
            print("Task marked as complete.")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
