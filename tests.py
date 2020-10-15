from rest_framework.test import APITestCase
from rest_framework import status

class AccountTests(APITestCase):

    def test_person79(self):
        response = self.client.get('/character/79/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseOK = {"name": "Grievous",
                    "height": "216",
                      "mass": "159",
                "hair_color": "none",
                "skin_color": "brown, white",
                 "eye_color": "green, yellow",
                "birth_year": "unknown",
                    "gender": "male",
                 "homeworld": { "name": "Kalee",
                                "population": "4000000000",
                                "known_residents_count": 1
                            },
              "species_name": "Kaleesh",
            "average_rating": "0.00",
                "max_rating": 0}
        self.assertEqual(response.data, responseOK)

    def test_person232(self):
        response = self.client.get('/character/232/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating66(self):
        response = self.client.post('/character/66/3/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/character/66/5/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/character/66/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        responseOK = {"name": "Dormé",
                    "height": "165",
                      "mass": "unknown",
                "hair_color": "brown",
                "skin_color": "light",
                 "eye_color": "brown",
                "birth_year": "unknown",
                    "gender": "female",
                 "homeworld": {"name": "Naboo",
                               "population": "4500000000",
                               "known_residents_count": 11},
              "species_name": "Human",
            "average_rating": "4.00",
                "max_rating": 5}
        self.assertEqual(response.data, responseOK)

    def test_rating666(self):
        response = self.client.post('/character/66/6/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
