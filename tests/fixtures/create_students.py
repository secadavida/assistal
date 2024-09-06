from faker import Faker
import pandas as pd
import os

_TEST_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUPS_DIR = os.path.join(_TEST_ROOT_DIR, "runtime", "groups")

# grades = [6, 7, 8, 9, 10, 11]
# groups = ['A', 'B', 'C']

grades = [9, 10, 11]
groups = ['A', 'B']
num_records = 5

fake = Faker()

def create_and_write_data(file):
    data = {
        'identificacion': [fake.unique.random_int(min=1000, max=9999) for _ in range(num_records)],
        'nombre': [fake.name() for _ in range(num_records)]
    }

    df = pd.DataFrame(data)
    df.to_excel(file, index=False, engine='openpyxl')

def generate_data():

    for grade in grades:
        for group in groups:
            grade_dir = os.path.join(GROUPS_DIR, str(grade))
            group_file = os.path.join(grade_dir, group + ".xlsx")

            if not os.path.exists(grade_dir):
                os.mkdir(grade_dir)

            if not os.path.isfile(group_file):
                with open(group_file, 'w'):
                    pass

            print(f"\t\t+ creando estudiantes de {str(grade)}-{group}")

            create_and_write_data(group_file)

def run():
    if not GROUPS_DIR:
        print("primero se necesita crear la carpeta de runtime haciendo correr la aplicacion")

    print("Generando estudiantes random:")
    print(f"\t+ Grados: {grades}")
    print(f"\t+ Grupos: {groups}")

    print()

    generate_data()
