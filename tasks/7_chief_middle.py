import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, or_
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


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


    def __repr__(self):
        return f'<Colonist> {self.id} {self.surname} {self.name}'


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <database_path>", file=sys.stderr)
        sys.exit(1)

    db_path = sys.argv[1]

    try:
        engine = create_engine(f'sqlite:///{db_path}')
        session = sessionmaker(bind=engine)
        sess = session()

        results = sess.query(User).filter(
            or_(
                User.position.ilike('%chief%'),
                User.position.ilike('%middle%')
            )
        ).order_by(User.id).all()

        for user in results:
            print(user)

        sess.close()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    print("-" * 60)
    print("Поиск главных и средних колонистов")
    print("-" * 60)
    main()