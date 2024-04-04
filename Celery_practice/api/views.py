from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from drf_standardized_errors.openapi_serializers import (
    ErrorResponse401Serializer,
    ErrorResponse404Serializer,
    ValidationErrorResponseSerializer,
)
from rest_framework.viewsets import GenericViewSet

from api.serializers import (
    UserGetSerializer,
    UserPostSerializer,
    OrderGetSerializer,
    OrderPostSerializer
)
from api.utils import generate_order_number
from orders.models import Order
from tasks.views import send_mail_task
from users.models import User
from Celery_practice.loggers import logger


@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_summary="Retrieve a user data",
        responses={
            200: UserGetSerializer,
            404: ErrorResponse404Serializer},
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create a new user.",
        responses={
            201: UserPostSerializer,
            400: ValidationErrorResponseSerializer,
        },
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Remove user",
        responses={200: UserPostSerializer, 404: ErrorResponse404Serializer},
    ),
)
class CustomUserViewSet(viewsets.ModelViewSet):
    """User create viewset"""
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserGetSerializer
        return UserPostSerializer

    def retrieve(self, request, **kwargs):
        """Retrieves user data."""
        user = self.request.user
        serializer = self.get_serializer(user)
        logger.info("The user's data was successfully received.")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """Create user."""
        user = self.request.data
        serializer = UserPostSerializer(data=request.data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(username=user['username'],
                                   password=user['password'],
                                   first_name=user['first_name'],
                                   email=user['email'])
        logger.info(f"New user: client_id {user.id} was created sucsessfuly.")
        send_mail_task(user, 'Регистрация')
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(
    name='retrieve',
    decorator=swagger_auto_schema(
        operation_summary="Retrieve a order data",
        responses={
            200: OrderGetSerializer,
            404: ErrorResponse404Serializer},
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create a new order.",
        responses={
            201: OrderPostSerializer,
            400: ValidationErrorResponseSerializer,
        },
    ),
)
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """Viewset for Order."""
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return OrderGetSerializer
        return OrderPostSerializer

    def retrieve(self, request, **kwargs):
        """Retrieves order data."""
        user = self.request.user
        order = get_object_or_404(Order, id=self.kwargs.get("pk"))
        if user != order.user:
            raise ErrorResponse401Serializer
        serializer = self.get_serializer(order)
        logger.info("The order's data was successfully received.")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, **kwargs):
        """Create order."""
        user = self.request.user
        serializer = OrderPostSerializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        order_number = generate_order_number()
        order = Order.objects.create(user=user,
                                     order_number=order_number)
        logger.info(f"New order: order_id {order.id} was created sucsessfuly.")
        send_mail_task(user, 'Заказ оформлен', order_number)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
