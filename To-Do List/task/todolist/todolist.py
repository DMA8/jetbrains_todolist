import sqlalchemy as sql
import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1) create an engine
engine = sql.create_engine('sqlite:///todo.db?check_same_thread=False')
# 2) create a db
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = sql.Column(sql.Integer, primary_key=True)
    task = sql.Column(sql.String, default='client_task')  # put here a task from user
    deadline = sql.Column(sql.Date, default=dt.datetime.today())

    def __repr__(self):
        return self.task


# creating the table in DB
Base.metadata.create_all(engine)  # It generates SQL query like CREATE TABLE.....

# to access the DB we need to create a session
Session = sessionmaker(bind=engine)
session = Session()


# to fill a db table we need to create an object of class 'Table' and put it in session.add(obj)

# HOW TO CREATE A DATETIMEOBJ:
# dt_field = datetime.datetime.strptime(the date like '01-24-2020', the mask like '%m-%d-%Y').date()

# new_task = Table(task='task', deadline=dt.datetime.today())
# session.add(new_task)
# session.commit()


def print_main_window():
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")


def add_task():
    tsk = input()
    new_task = Table(task=tsk, deadline=enter_deadline())
    session.add(new_task)
    session.commit()


def print_all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    if not rows:
        print('Nothing to do!')
        print()
        return
    for i in rows:
        print(str(i.id) + '.', i.task + '.', i.deadline.day, i.deadline.strftime('%b'), sep=' ')
    print()


def print_today():
    rows = session.query(Table).filter(Table.deadline == dt.datetime.today().date()).all()
    print('Today ', dt.datetime.today().day, ' ', dt.datetime.today().strftime('%b'), ':', sep='')
    if not rows:
        print('Nothing to do!')
        print()
        return
    for i in range(len(rows)):
        print(i+1, '. ', rows[i], sep='')
    print()


def week_tasks():
    days = []
    for i in range(0, 7, 1):
        days.append(dt.datetime.today().date() + dt.timedelta(i))
    for day in days:
        tasks = session.query(Table).filter(Table.deadline == day).all()
        print(week_days[day.weekday()], day.day, day.strftime('%b'), ':')
        if not tasks:
            print('There is nothing to do!')
            print()
            continue
        for j in range(len(tasks)):
            print(j+1, '. ', tasks[j], sep='')
        print()
    print()

week_days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def missed_tasks():
    losed_deadlines = session.query(Table).filter(Table.deadline < dt.datetime.today().date()).order_by(Table.deadline).all()
    print('Missed tasks:')
    if not losed_deadlines:
        print('Nothing is missed!')
        return
    for i in range(len(losed_deadlines)):
        print(i+1, '. ', losed_deadlines[i],'. ',losed_deadlines[i].deadline.day, ' ',losed_deadlines[i].deadline.strftime('%b'), sep='')
    print()
def delete_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    print('Choose the number of the task you want to delete:')
    if not rows:
        print('Nothing to delete!')
        print()
        return
    for i in rows:
        print(str(i.id) + '.', i.task + '.', i.deadline.day, i.deadline.strftime('%b'), sep=' ')
    print()
    a = int(input())
    session.query(Table).filter(Table.id == a).delete()
    print('The task has been deleted!')

def enter_deadline():
    deadline = input('Enter deadline')
    deadline = dt.datetime.strptime(deadline, '%Y-%m-%d')
    return deadline


while True:
    session.commit()
    print_main_window()
    client_command = input()
    print()
    if client_command == '1':
        # Today's tasks
        print_today()
    elif client_command == '2':
        week_tasks()
    elif client_command == '3':
        # All tasks
        print_all_tasks()
    elif client_command == '4':
        missed_tasks()
    elif client_command == '5':
        # Add task
        print('Enter task')
        add_task()
        print('The task has been added')
    elif client_command == '6':
        delete_tasks()
    elif client_command == '0':
        print('Bye!')
        break
    else:
        print('Incorrect command! Try again!')
        print()
