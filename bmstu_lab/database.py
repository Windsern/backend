import psycopg2

from prettytable import PrettyTable

class Database():
    # Подключение к БД
    def connect(self):
        try:
            # Подключение к базе данных
            self.connection = psycopg2.connect(
                # connect_timeout=1,
                host='localhost',
                port=5432,
                user='postgres',
                password='postgres',
                database='database',
            )

            print("[INFO] Успешное подключение к базе данных")

        except Exception as ex:
            print("[INFO] Ошибка при работе с PostgreSQL:", ex)

    # Удаление БД
    def drop_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    DROP TABLE Building, Checking, CheckingsBuildings, Users CASCADE;
                """)

            # Подтверждение изменений
            self.connection.commit()
            print("[INFO] Успешно удалены таблицы в базе данных")

        except Exception as ex:
            print("[INFO] Ошибка при работе с PostgreSQL:", ex)

        # Создание таблицы БД и связанные таблицы

    def create_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""                             
                      
                      CREATE TABLE Users (
                          user_id SERIAL PRIMARY KEY,
                          login VARCHAR NOT NULL,
                          password VARCHAR NOT NULL,
                          is_admin BOOLEAN NOT NULL
                      );
                      
                      CREATE TABLE Building (
                          building_id SERIAL PRIMARY KEY,
                          title VARCHAR,
                          address VARCHAR,
                          type_building VARCHAR,
                          count_floor VARCHAR,
                          year_building VARCHAR,
                          document_building VARCHAR,
                          project_document VARCHAR,
                          status_building VARCHAR,
                          status VARCHAR
                      );
                      
                      CREATE TABLE Checking (
                          checking_id SERIAL PRIMARY KEY,
                          name VARCHAR,
                          age INTEGER,
                          status VARCHAR,
                          user_id INTEGER,
                          building_id INTEGER,
                          publication_date DATE,
                          creation_time DATE,
                          approving_date DATE,
                          moderator INTEGER
                      );

                      CREATE TABLE CheckingsBuildings (
                          building_id INT NOT NULL,
                          checking_id INT NOT NULL
                      );
                      

                      ALTER TABLE CheckingsBuildings
                      ADD CONSTRAINT FR_Checkings_Buildings_of_Building
                          FOREIGN KEY (building_id) REFERENCES Building (building_id);

                      ALTER TABLE CheckingsBuildings
                      ADD CONSTRAINT FR_Checkings_Buildings_of_Checking
                          FOREIGN KEY (checking_id) REFERENCES Checking (checking_id);

                      ALTER TABLE Checking
                      ADD CONSTRAINT FR_Checking_of_Building
                          FOREIGN KEY (building_id) REFERENCES Building (building_id);

                      ALTER TABLE Checking
                      ADD CONSTRAINT FR_Checking_of_Users_user_id
                          FOREIGN KEY (user_id) REFERENCES Users (user_id);
                      
                      ALTER TABLE Checking
                      ADD CONSTRAINT FR_Checking_of_Users_moderator
                          FOREIGN KEY (moderator) REFERENCES Users (user_id);
                          
                          

                          
              """)

            # Подтверждение изменений
            self.connection.commit()
            print("[INFO] Успешно созданы таблицы в базе данных")

        except Exception as ex:
            print("[INFO] Ошибка при работе с PostgreSQL:", ex)

    def insert_default_value(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                                        -- ПОЛЬЗОВАТЕЛЬ (АУТЕНФИКАЦИЯ)
                    INSERT INTO Users (login, password, is_admin) VALUES
                        ('user1', '1111', false),
                        ('user2', '2222', false),
                        ('user3', '3333', false),
                        ('admin', '1111', true);

                    -- Начальник (ПРИНМАЮЩИЙ ЗАКАЗЧИКА) и Ученые (ЗАКАЗЧИК)
                    INSERT INTO Building (title, address, type_building, count_floor, year_building, document_building, 
                    project_document, status_building, status) 
                    VALUES
                        ('Научно-образовательный корпус', '2-я Бауманская улица, 7с1', 'Общественный', 5, 2020, 'Да', 
                        'Да', 'Строится', 'Действует'),
                        ('Квантум парк', 'Бригадирский переулок, 13с4', 'Общественный', 5, 2020, 'Да', 
                        'Да', 'Строится', 'Действует'),
                        ('Дом РФ', 'Бригадирский переулок, 12с1', 'Общественный', 5, 2020, 'Да', 
                        'Да', 'Построен', 'Действует'),
                        ('Образовательный комплекс', 'Бригадирский переулок, 13', 'Общественный', 5, 2020, 'Да', 
                        'Да', 'Строится', 'Действует'),
                        ('Библиотечный корпус', '2-я Бауманская улица, 10', 'Общественный', 5, 2020, 'Да', 
                        'Да', 'Строится', 'Действует'),
                        ('Дворец технологий', 'Бауманская улица, 57Ас1', 'Общественный', 5, 2020, 'Да', 
                        'Да', 'Строится', 'Действует'),
                        ('Центр биомедицинских систем и технологий', 'Бригадирский переулок, 12', 'Общественный', 5, 2020, 'Да',
                        'Да', 'Строится', 'Действует'),
                        ('Комплекс общежитий', '55.771550, 37.695786', 'Общественный', 20,2020, 'Да', 
                        'Да', 'Строится', 'Действует'),
                        ('Образовательно-досуговый центр Спектр', '55.771777, 37.695370', 'Общественный', 20,2020, 'Да', 
                        'Да', 'Строится', 'Действует');


                    INSERT INTO Checking (name, age, status, user_id, building_id, publication_date, creation_time, approving_date, moderator)
                    VALUES 
                        ('Александр', 25, 'Введён', 1, 6, '01-09-2023', '01-09-2023', '02-09-2023', 4),
                        ('Николай', 31, 'Введён', 2, 1, '05-05-2023', '05-05-2023', '15-05-2023', 4),
                        ('Вячеслав', 27, 'Введён', 3, 4, '30-05-2023', '30-05-2023', '01-06-2023', 4);
                                                

                    INSERT INTO CheckingsBuildings (building_id, checking_id) 
                    VALUES
                        (6, 1),
                        (1, 2),
                        (4, 3);

                    """)

                # Подтверждение изменений
                self.connection.commit()
                print("[INFO] Building, Checking, CheckingsBuildings, Users: Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[INFO] location, geografic_object: Ошибка при заполнение данных:", ex)


    def insert_building(self, title, address, type_building, count_floor, year_building, document_building, project_document, status_building, status):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO Building (title, address, type_building, count_floor, year_building, document_building, 
                    project_document, status_building, status) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                    (title, address, type_building, count_floor, year_building, document_building,
                     project_document, status_building, status)
                )

                # Подтверждение изменений
                self.connection.commit()
                print("[INFO] [Building] Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[INFO] [Building] Ошибка при заполнение данных:", ex)

    def insert_checking(self, name, age, status, user_id, building_id, publication_date, creation_time, approving_date, moderator):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO Checking (name, age, status, user_id, building_id, publication_date, creation_time, approving_date, moderator) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                    (name, age, status, user_id, building_id, publication_date, creation_time, approving_date, moderator)
                )

                # Подтверждение изменений
                self.connection.commit()
                print("[INFO] [Checking] Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[INFO] [Checking] Ошибка при заполнение данных:", ex)

    def insert_checkingsbuildings(self, building_id, checking_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO CheckingsBuildings (building_id, checking_id) VALUES
                            (%s, %s);""",
                    (
                    building_id, checking_id)
                )

                # Подтверждение изменений
                self.connection.commit()
                print("[INFO] [CheckingsBuildings] Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[INFO] [CheckingsBuildings] Ошибка при заполнение данных:", ex)

    def select_all(self):
        try:
            with self.connection.cursor() as cursor:
                database = {}
                name_table = ['Users', 'Building', 'Checking', 'CheckingsBuildings']
                database['name_table'] = name_table
                for name in name_table:
                    cursor.execute(f"""SELECT * FROM {name};""")
                    database[name] = cursor.fetchall()
                    # Получим названия колонок из cursor.description
                    database[f'{name}_name_col'] = [col[0] for col in cursor.description]

                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("Ошибка при чтении данных:", ex)

    def update_status(self, status, id_building):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE Building SET status = %s WHERE building_id = %s;""",
                    (status, id_building)
                )
                # Подтверждение изменений
                self.connection.commit()
                print("[Status] Данные успешно обновлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[Status] Ошибка при обновление данных:", ex)

    # Закрытие БД
    def close(self):
        # Закрытие соединения
        if self.connection:
            self.connection.close()
            print("[INFO] Соединение с базой данных закрыто")




# db = Database()
#
# db.connect()

# db.drop_table()
# db.create_table()

# db.select_all()
# db.insert_default_value()

# db.insert_building('Научно-образовательный корпус', '2-я Бауманская улица, 7с1', 'Общественный', 5, 2020, 'Да', 'Да', 'Строится', 'Действует')
# db.insert_checking('Николай', 31, 'Введён', 2, 1, '14-09-2023', '14-09-2023', '18-09-2023', 4)
# db.insert_checkingsbuildings(1, 2)


# db.close()
