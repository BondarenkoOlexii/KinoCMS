import os
from celery import Celery
import redis
from celery import shared_task
from django.core.mail import EmailMessage, get_connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task(bind=True)
def send_mail_task(self, subject, message, email_from, recepient_list, file_path=None):

    total = len(recepient_list)

    connection = get_connection()
    connection.open()

    for i, email_adress in enumerate(recepient_list):
        try:
            print("Ну вроді працює")
            msg = EmailMessage(
                subject=subject,
                body=message,
                from_email=email_from,
                to=[email_adress],
                connection=connection
            )
            msg.content_subtype = "html"

            if file_path and os.path.exists(file_path):
                msg.attach_file(file_path)

            msg.send()


        except Exception as e:
            print(f"Error {e}")
            print("A не, не працює")

        self.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': total, 'percent': int((i + 1) / total * 100)}
        )

    connection.close()
    return {'status': 'Success', 'total': total}



