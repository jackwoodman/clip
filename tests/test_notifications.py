from notifications import NotificationManager, Notification, NotificationSource
import random
import time
import string
from datetime import timedelta


def test_adding_of_notifications(number_of_notifications):
    notification_manager = NotificationManager()

    # Override maximum for purposes of test.
    notification_manager.update_buffer_size(number_of_notifications)

    text_length = 20
    ascii_alpha = string.ascii_letters

    for notif in range(number_of_notifications):
        # Create title and random text.
        title = f"Test Notification {notif}"
        text = f"{''.join(random.choice(ascii_alpha) for _ in range(text_length))}"

        # 50% chance to create and add a subtitle.
        subtitle = None if random.choice([True, False]) else f"Subtitle #{notif}"

        # Create notification.
        new_notification = Notification(
            title=title,
            text=text,
            subtitle=subtitle,
            source=NotificationSource.TEST,
        )

        # Save notification to thie manager.
        notification_manager.add_notification(new_notification=new_notification)

    assert notification_manager.get_total_notification_count() == number_of_notifications


def test_expiration():
    new_notification = Notification(
        title="Expiration Test", text="Expiration Test", expiration_delta=timedelta(seconds=1)
    )

    assert new_notification.valid
    time.sleep(1)
    new_notification.check_expired()
    assert not new_notification.valid
