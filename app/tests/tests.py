import unittest
import random
import json
from app import *
from app.project.environment import *

def generate_dict_for_json(citizen_count, error_line=0, relatives=None):
    """
    Generates test data

    :param citizen_count: number of people to generate
    :param error_line: number of erroneous rows
    :param relatives: number of links to generate
    :return: the data dictionary
    """

    with open('tests/data/cities.json', 'r') as cities_file, open('tests/data/streets.json', 'r') as streets_file, \
            open('tests/data/names.json', 'r') as names_file, open('tests/data/birth_date.json',
                                                                   'r') as birth_date_file:
        cities = json.load(cities_file)
        streets = json.load(streets_file)
        names = json.load(names_file)
        birth_date = json.load(birth_date_file)

    citizens = [dict(citizen_id=i, town=random.choice(cities), street=random.choice(streets),
                     building=str(random.randint(1, 10000)), apartment=random.randint(1, 10000),
                     name=random.choice(names), birth_date=random.choice(birth_date),
                     gender=random.choice(['male', 'female']),
                     relatives=[]) for i in range(citizen_count)]
    for i in range(random.randint(citizen_count // 2,
                                  (citizen_count // 2 * random.randint(2, 4)) * 5) if relatives is None else relatives):
        number_one, number_two = random.randint(0, citizen_count - 1), random.randint(0, citizen_count - 1)
        if number_one not in citizens[number_two]['relatives'] and number_two != citizens[number_one]['citizen_id']:
            citizens[number_one]['relatives'].append(number_two)
            citizens[number_two]['relatives'].append(number_one)
    return {"citizens": citizens}


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        db_redis.flushall()
        db.drop_all()

    def test_task_one(self) -> None:
        """
        The test first method of the API

        :return:
        """
        response = self.app.post("/imports",
                                 data=json.dumps(generate_dict_for_json(100)),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_task_two(self) -> None:
        """
        Test the second API method

        :return:
        """
        self.test_task_one()
        response = self.app.patch("/imports/1/citizens/1",
                                  data=json.dumps({
                                      "town": "Москва",
                                      "street": "Иосифа Бродского",
                                      "relatives": [1, 2, 99],
                                      "birth_date": "30.09.1982"
                                  }),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_task_tree(self) -> None:
        """
        Test the third API method

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/1/citizens")
        self.assertEqual(response.status_code, 200)

    def test_task_four(self) -> None:
        """
        Test the fourth API method

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/1/citizens/birthdays")
        self.assertEqual(response.status_code, 200)

    def test_task_five(self) -> None:
        """
        Test the fifth API method

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/1/towns/stat/percentile/age")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
