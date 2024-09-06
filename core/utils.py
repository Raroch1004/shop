from django.core.mail import send_mail


def send_order_confirmation_email(order):
    subject = f"Подтверждение заказа №{order.id}"
    message = (
        f"Здравствуйте, {order.full_title},\n\n"
        f"Ваш заказ №{order.id} успешно оформлен.\n"
        f"Общая стоимость: {order.get_total_cost()} руб.\n\n"
        f"Информация о доставке:\n"
        f"Адрес: {order.address}, {order.city}, {order.country}, {order.postal_code}\n\n"
        f"Спасибо за ваш заказ!"
    )
    from_email = 'The.Raroch@yandex.ru'
    recipient_list = [order.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
