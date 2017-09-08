from unittest import TestCase

from api.hidden_api_manager import get_verification_token


class TestRequestHandler(TestCase):
    def test_get_verification_token(self):
        auth_cookie = '.AspNet.ApplicationCookie=Umzio6OaBdlhJCXxz4DnFOURoE52QgYx0o34kEmO1rrzEKh2ZV4ACfqF9KKXdng_JHk7vat5HtZTbR2ejujdlwFZV3RfDjwf3FkmhVC89Emp4Lt3tdGurv54p-JmCGJjueE3NJ41Qg4KaWdKoLrjC8kRs6fSUKc3KnUzBFi8_3z_EoqwGtPD63HJ9lZeMblh-ef3w63_R1S72bbhGVnwnomeghMy4OsOU5T6Z7owomoYMTszS_URIXOtxSibh6S2BTO304RfQ3aHjwnRBsJarC8qZ3L_YhMD0tcYMRxNW7VunTMvWENz2C7VpaRE84QpG0z-Iz0eIMZXvLv77bqGZ6Z2HvhU0n3ZmagmfSi9Rp5F05MCiwtqBrr6QQEdfoJxZhH1ceRmBtkvuPNlXVm5rAT1l3nxQghRrOo_BYlSQGsqaCrbyTCjzenB2Vpj-cJKjeLQ95XgFVlxFjNwLy7yJyaZguA'

        result = get_verification_token(auth_cookie)

        self.assertIsNotNone(result)
        self.assertIsNot("", result)
