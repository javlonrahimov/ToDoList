from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def show_tasks_by_date(date, is_today):
    tasks = session.query(Task).filter(Task.deadline == date.date()).all()
    if is_today:
        print(f"Today {date.day} {date.strftime('%b')}")
    else:
        print(f'{date.strftime("%A")} {date.day} {date.strftime("%b")}')
    if len(tasks) != 0:
        for i in range(len(tasks)):
            print(f'{i + 1}. {tasks[i].task}\n')
    else:
        print('Nothing to do!\n')


def add_task(task):
    session.add(task)
    session.commit()


def show_tasks_week():
    for i in range(7):
        show_tasks_by_date(datetime.today() + timedelta(days=i), False)


def show_missed_tasks():
    tasks = session.query(Task).filter(Task.deadline < datetime.today()).order_by(Task.deadline).all()
    print('Missed tasks')
    if len(tasks) != 0:
        for i in range(len(tasks)):
            print(f'{i + 1}. {tasks[i].task}. {tasks[i].deadline.day} {tasks[i].deadline.strftime("%b")}')
        print('\n')
    else:
        print('Nothing to do!\n')


def show_tasks_all():
    tasks = session.query(Task).order_by(Task.deadline).all()
    print('All tasks')
    if len(tasks) != 0:
        for i in range(len(tasks)):
            print(f'{i + 1}. {tasks[i].task}. {tasks[i].deadline.day} {tasks[i].deadline.strftime("%b")}')
    else:
        print('Nothing to do!')


def show_menu():
    command = input("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit\n""")
    if command == '0':
        return False
    elif command == '1':
        show_tasks_by_date(datetime.today(), True)
        return True
    elif command == '2':
        show_tasks_week()
        return True
    elif command == '3':
        show_tasks_all()
        return True
    elif command == '4':
        show_missed_tasks()
        return True
    elif command == '5':
        add_task(
            Task(task=input('Enter task\n'), deadline=datetime.strptime(input('Enter deadline\n'), '%Y-%m-%d').date()))
        print('Task has been added!')
        return True
    elif command == '6':
        tasks = session.query(Task).order_by(Task.deadline).all()
        print("Choose the number of the task you want to delete:")
        show_tasks_all()
        session.delete(tasks[int(input()) - 1])
        session.commit()
        return True
    else:
        print("Invalid input")
        return True


while True:
    if not show_menu():
        print('Bye')
        break
