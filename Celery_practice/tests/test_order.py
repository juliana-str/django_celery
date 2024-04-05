import pytest
from rest_framework import status


@pytest.mark.django_db(transaction=True)
class TestOrder:

    def test_create_order(self, auth_client_first):
        order_data = {'order_number': 1}
        response = auth_client_first.post("/api/orders/", order_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED


