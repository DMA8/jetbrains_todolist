import sqlalchemy as sql
import datetime as dt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = sql.create_engine('sqlite:///todo.db?check_same_thread=False')
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


MAIN_WINDOW = "1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit"


def add_task(tsk: str, deadline) -> None:
    new_task = Table(task=tsk, deadline=dt.datetime.strptime(deadline, '%Y-%m-%d'))
    session.add(new_task)
    session.commit()


def delete_tasks(task_id=None):
    tasks = get_tasks('all')
    if not task_id:
        print('Choose the number of the task you want to delete:')
        print_tasks(tasks, 'all')
        task_id = int(input())
    session.query(Table).filter(Table.id == task_id).delete()


def get_tasks(period: str):
    tasks = []
    if period == 'all':
        tasks = session.query(Table).order_by(Table.deadline).all()
    elif period == 'today':
        tasks = session.query(Table).filter(Table.deadline == dt.datetime.today().date()).all()
    elif period == 'week':
        tasks = session.query(Table).filter(sql.and_(Table.deadline >= dt.datetime.now().date(), \
                                                     Table.deadline <= dt.datetime.now().date() + dt.timedelta(
                                                         days=7))).all()
    elif period == 'missed':
        tasks = session.query(Table).filter(Table.deadline < dt.datetime.today().date()).order_by(
            Table.deadline).all()

    return tasks


def print_tasks(tasks: list, period):
    """tasks only in  <class '__main__.Table'> """
    if period == 'today':
        if not tasks:
            print('Nothing to do!\n')
            return
        for i in range(len(tasks)):
            print(i + 1, '. ', tasks[i], sep='')
    elif period == 'week':
        print()
        days = [dt.datetime.today().date() + dt.timedelta(i) for i in range(7)]
        for day in days:
            match = None
            print(day.strftime('%A'), day.day, day.strftime('%b'), ':')
            for task in range(len(tasks)):
                match = tasks[task].deadline == day
                if match:
                    print(task + 1, '. ', tasks[task], sep='')
            else:
                print('There is nothing to do!\n')
                continue
        print()
    elif period == 'missed':
        if not tasks:
            print('Nothing is missed!')
            return
        for i in range(len(tasks)):
            print(i + 1, '. ', tasks[i], '. ', tasks[i].deadline.day, ' ', \
                  tasks[i].deadline.strftime('%b'), sep='')
        print()
    elif period == 'all':
        if not tasks:
            print('There is nothing to do!\n')
            return
        for i in tasks:
            print(str(i.id) + '.', i.task + '.', i.deadline.day, i.deadline.strftime('%b'), sep=' ')
        print()


def interface():
    while True:
        session.commit()
        print(MAIN_WINDOW)
        client_command = input('\n')
        time_code = {'1': 'today', '2': 'week', '3': 'all', '4': 'missed'}
        manipulate_code = {'5': 'add', '6': 'delete', '0': 'exit'}
        if client_command in time_code:
            print_tasks(get_tasks(time_code[client_command]), time_code[client_command])
        elif client_command in manipulate_code:
            if manipulate_code[client_command] == 'add':
                add_task(input('Enter the task '), input('Enter the deadline in format "YYYY-M-D"'))
                print('The task has been added!')
            elif manipulate_code[client_command] == 'delete':
                delete_tasks()
                print('The task has been deleted!')
            elif manipulate_code[client_command] == 'exit':
                print('Bye!')
                break
        else:
            print('Incorrect command! Try again!\n')


if __name__ == '__main__':
    interface()
