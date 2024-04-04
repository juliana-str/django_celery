from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task

from Celery_practice.loggers import logger

SUBJECT = {
    'Регистрация': 'Вы успешно зарегистрированы в нашем интернет-магазине good-food!',
    'Заказ оформлен': 'Ваш заказ оформлен, номер вашего заказа '

}


@shared_task(bind=True, default_retry_delay=10 * 60)
def send_mail_task(self, user, subject, order_number=0):
    MESSAGE = SUBJECT.get(subject)
    if subject == 'Заказ оформлен':
        MESSAGE += order_number
    try:
        send_mail(
            subject=subject,
            message=f"{user.first_name} {MESSAGE}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        logger.debug(f'The massage to user: client_id {user.id} was send sucsessfuly')
    except ProcessLookupError as error:
        logger.error(f'The message was not send! {error}.', exc_info=True)
        raise SystemError(f'The message was not send!! {error}')
