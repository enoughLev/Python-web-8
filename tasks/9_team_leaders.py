import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_leader = Column(Integer, nullable=False)
    job = Column(String(500), nullable=False)
    work_size = Column(Integer)
    collaborators = Column(String(500))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_finished = Column(Boolean, default=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    position = Column(String(100))
    speciality = Column(String(100))
    address = Column(String(200))
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    modified_date = Column(DateTime)


def count_collaborators(collaborators_str):
    if not collaborators_str:
        return 0
    return len([x for x in collaborators_str.split(',') if x.strip()])


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <database_path>", file=sys.stderr)
        sys.exit(1)

    db_path = sys.argv[1]

    try:
        engine = create_engine(f'sqlite:///{db_path}')
        session = sessionmaker(bind=engine)
        sess = session()

        jobs = sess.query(Job).all()

        if not jobs:
            print("No jobs found in database")
            sess.close()
            return

        max_team_size = 0
        team_leaders = {}

        for job in jobs:
            team_size = count_collaborators(job.collaborators) + 1

            if team_size > max_team_size:
                max_team_size = team_size
                team_leaders = {job.team_leader}
            elif team_size == max_team_size:
                team_leaders.add(job.team_leader)

        if team_leaders:
            leaders = sess.query(User).filter(User.id.in_(team_leaders)).all()
            for leader in leaders:
                print(f"{leader.surname} {leader.name}")

        sess.close()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    print("-" * 60)
    print("Вывод лидеров в работах с наибольшим числом участников")
    print("-" * 60)
    main()
