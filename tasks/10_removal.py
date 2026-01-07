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


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <database_path>", file=sys.stderr)
        sys.exit(1)

    db_path = sys.argv[1]

    try:
        engine = create_engine(f'sqlite:///{db_path}')
        session = sessionmaker(bind=engine)
        sess = session()

        users_to_update = sess.query(User).filter(
            or_(
                User.address.ilike('module_1%'),
                User.address.ilike('% module_1%'),
                User.address == 'module_1',
                User.address.ilike('module1%'),
                User.address.ilike('% module1%'),
                User.address.ilike('module 1%'),
                User.address.ilike('% module 1%'),
                User.address.ilike('Module_1%'),
                User.address.ilike('%Module_1%'),
                User.address.ilike('Модуль_1%'),
                User.address.ilike('%Модуль_1%'),
                User.address.ilike('модуль_1%'),
                User.address.ilike('%модуль_1%')
            ),
            User.age < 21
        ).all()

        updated_count = 0
        for user in users_to_update:
            user.address = 'module_3'
            updated_count += 1

        sess.commit()
        print(f"Updated {updated_count} users")

        sess.close()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    print("-" * 60)
    print("Перенос жильцов младше 21 года из модуля_1 в модуль_3")
    print("-" * 60)
    main()
