import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime
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


def query_first_module_colonists(db_name):
    try:
        if not db_name.endswith('.db'):
            db_name = f'{db_name}.db'

        connection_string = f'sqlite:///{db_name}'

        engine = create_engine(connection_string)

        Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)
        sess = session()

        first_module_colonists = sess.query(User).filter(
            (User.address.like('%module_1%'))
        ).all()

        if first_module_colonists:
            for colonist in first_module_colonists:
                print(colonist)
        else:
            print("В первом модуле нет проживающих колонистов.")
            print("\nВсе пользователи в базе:")
            all_users = sess.query(User).all()
            if all_users:
                for user in all_users:
                    print(f"{user} | Адрес: {user.address if user.address else 'Не указан'}")
            else:
                print("В базе данных нет пользователей.")

        sess.close()

    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        print(f"Проверьте наличие файла базы данных: {db_name}")


def main():
    print("-" * 50)
    print("Поиск колонистов в первом модуле")
    print("-" * 50)

    db_name = sys.argv[1]

    query_first_module_colonists(db_name)


if __name__ == "__main__":
    main()
