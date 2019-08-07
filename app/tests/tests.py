import unittest
import random
import json
from app import *
from app.project.environment import *

def generate_dict_for_json(citizen_count, error_line=None, relatives=None) -> dict:
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

    if error_line and len(citizens) > 1:
        if error_line == "town":
            citizens[0]["town"] = ""
        elif error_line == "street":
            citizens[0]["street"] = ""
        elif error_line == "building":
            citizens[0]["building"] = ""
        elif error_line == "apartment":
            citizens[0]["apartment"] = ""
        elif error_line == "name":
            citizens[0]["name"] = ""
        elif error_line == "birth_date":
            citizens[0]["birth_date"] = "31.02.2019"
        elif error_line == "gender":
            citizens[0]["gender"] = "???"
        elif error_line == "relatives":
            citizens[0]["relatives"] = [2]
            citizens[1]["relatives"] = []

    return {"citizens": citizens}


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """
        Fires when the test is run

        :return:
        """
        self.app = app.test_client()
        db.create_all()

    def tearDown(self) -> None:
        """
        Fires when the test is stopped

        :return:
        """
        db_redis.flushall()
        db.drop_all()

    def test_task_one(self) -> None:
        """
        The test first method of the API

        :return:
        """
        response = self.app.post("/imports",
                                 data=json.dumps(generate_dict_for_json(10000)),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_task_one_errors(self) -> None:
        """
        Checks if data validation is working

        :return:
        """
        response_town = self.app.post("/imports",
                                      data=json.dumps(generate_dict_for_json(20, "town")),
                                      content_type='application/json')
        self.assertEqual(response_town.status_code, 400)
        response_street = self.app.post("/imports",
                                        data=json.dumps(generate_dict_for_json(20, "street")),
                                        content_type='application/json')
        self.assertEqual(response_street.status_code, 400)
        response_building = self.app.post("/imports",
                                          data=json.dumps(generate_dict_for_json(20, "building")),
                                          content_type='application/json')
        self.assertEqual(response_building.status_code, 400)
        response_apartment = self.app.post("/imports",
                                           data=json.dumps(generate_dict_for_json(20, "apartment")),
                                           content_type='application/json')
        self.assertEqual(response_apartment.status_code, 400)
        response_name = self.app.post("/imports",
                                      data=json.dumps(generate_dict_for_json(20, "name")),
                                      content_type='application/json')
        self.assertEqual(response_name.status_code, 400)
        response_birth_date = self.app.post("/imports",
                                            data=json.dumps(generate_dict_for_json(20, "birth_date")),
                                            content_type='application/json')
        self.assertEqual(response_birth_date.status_code, 400)
        response_gender = self.app.post("/imports",
                                        data=json.dumps(generate_dict_for_json(20, "gender")),
                                        content_type='application/json')
        self.assertEqual(response_gender.status_code, 400)
        response_relatives = self.app.post("/imports",
                                           data=json.dumps(generate_dict_for_json(20, "relatives")),
                                           content_type='application/json')
        self.assertEqual(response_relatives.status_code, 400)

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

    def test_task_two_errors(self) -> None:
        """
        Checks if data validation is working

        :return:
        """
        self.test_task_one()
        response = self.app.patch("/imports/1/citizens/1",
                                  data=json.dumps({
                                      "town": "Москва",
                                      "street": "Иосифа Бродского",
                                      "relatives": [1, 2, 99],
                                      "birth_date": "31.02.2019"
                                  }),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_task_tree(self) -> None:
        """
        Test the third API method

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/1/citizens")
        self.assertEqual(response.status_code, 200)

    def test_task_tree_errors(self) -> None:
        """
        Check response on errors

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/-9999999999999/citizens")
        self.assertEqual(response.status_code, 404)

    def test_task_four(self) -> None:
        """
        Test the fourth API method

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/1/citizens/birthdays")
        self.assertEqual(response.status_code, 200)

    def test_task_four_errors(self) -> None:
        """
        Check response on errors

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/-9999999999999/citizens/birthdays")
        self.assertEqual(response.status_code, 404)

    def test_task_five(self) -> None:
        """
        Test the fifth API method

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/1/towns/stat/percentile/age")
        self.assertEqual(response.status_code, 200)

    def test_task_five_errors(self) -> None:
        """
        Check response on errors

        :return:
        """
        self.test_task_one()
        response = self.app.get("/imports/-9999999999999/towns/stat/percentile/age")
        self.assertEqual(response.status_code, 404)

    def test_comparative(self) -> None:
        """
        The test compares the data on the server with the original

        :return:
        """
        with open('tests/data/test_data.json', 'r') as test_data:
            test_data = json.load(test_data)

        response = self.app.post("/imports",
                                 data=json.dumps(test_data),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 201)
        import_id = json.loads(response.get_data(as_text=True))["data"]["import_id"]

        response = self.app.get(f"/imports/{import_id}/citizens")
        self.assertEqual(response.status_code, 200)
        response_data = sorted(json.loads(response.get_data(as_text=True))["data"], key=lambda x: x["citizen_id"])
        test_data = sorted(test_data["citizens"], key=lambda x: x["citizen_id"])
        self.assertEqual(response_data, test_data)


if __name__ == '__main__':
    unittest.main()
