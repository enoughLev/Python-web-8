import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, and_
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


    def __repr__(self):
        return f'<Job> "{self.job}"'


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <database_path>", file=sys.stderr)
        sys.exit(1)

    db_path = sys.argv[1]

    try:
        engine = create_engine(f'sqlite:///{db_path}')
        session = sessionmaker(bind=engine)
        sess = session()

        results = sess.query(Job).filter(
            and_(
                Job.work_size < 20,
                Job.is_finished == False
            )
        ).order_by(Job.id).all()

        for job in results:
            print(job)

        sess.close()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    print("-" * 40)
    print("Поиск работ меньше 20 часов")
    print("-" * 40)
    main()
