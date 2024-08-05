from typing import Optional
from datetime import datetime
from enum import Enum
import bisect


class NotificationSource(Enum):
    SYSTEM = "system"


class Notification:
    def __init__(
        self,
        title: str,
        text: str,
        subtitle: Optional[str] = None,
        source: NotificationSource = NotificationSource.SYSTEM,
    ):
        self.title = title
        self.text = text
        self.subtitle = subtitle
        self.notification_time = datetime.now()
        self.invalidation_time: datetime = None
        self.source = source
        self.valid = True
        self.text_length = len(text)

    def invalidate(self):
        self.valid = False
        self.invalidation_time = datetime.now()

    def get_number_of_lines(self) -> int:
        return 2 if not self.subtitle else 3


class NotificationManager:
    buffer_max_size = 100

    notification_buffer: list[Notification] = []

    def __init__(self):
        self.notification_buffer = [None for _ in range(self.buffer_max_size)]

    def is_full(self) -> bool:
        """
        Whether the number of elements in the notification buffer is currently at the
        maximum size.

        Returns:
            Boolean value indicating if record is full.
        """
        return len(self.notification_buffer) == self.buffer_max_size

    def append_notification(self, new_notification: Notification) -> bool:
        """
        Append a new notification to the record. Will not sort or maintain order.
        Will not insert and replace if the array is full.

        Args:
            new_notification: The notification object to be appended.

        Returns:
            Whether the appendation was successful or not.

        """
        if not self.is_full():
            self.notification_buffer.append(new_notification)
            return True
        else:
            return False

    def add_notification(self, new_notification: Notification, cull_records: bool = True) -> int:
        """
        Add a new notification at the start of the record, indicating recency. Uses an insertion method so that if
        multiple notifications are added at the same time in close succession, order is preserved.

        If cull_records is set to False, will not 'cull' the notifications, but this shouldn't be needed.

        Arguments:
            new_notification: The Notification object representing new record to be inserted.
            cull_records: An optional bool indicating whether the buffer length should be enforced
                after insertion.

        Returns:
            The integer length of the records after insertions.
        """
        bisect.insort(
            self.notification_buffer, new_notification, key=lambda notification: notification.notification_time
        )

        if cull_records:
            self.cull_notifications()

        return len(self.notification_buffer)

    def cull_notifications(self) -> int:
        """
        Shorten the notification buffer to the maximum buffer limit. Returns the length
        of the notification buffer after shortening.
        """
        self.notification_buffer = self.notification_buffer[: self.buffer_max_size]

        return len(self.notification_buffer)

    def sort_notifications(self):
        """
        Sort notifications by the property notification_time. Used to maintain
        order by notification_time, but by nature sorting order should be assured
        by the bisect insertion method.
        """
        self.notification_buffer.sort(key=lambda notification: notification.notification_time)

    def get_most_recent_notification(self, re_sort: bool = True) -> Notification:
        """
        Returns the most recent notification. Will perform the sorting operation to ensure correctness,
        unless re_sort is set to False. This should only be done if you need speed, but
        know for a fact a sorting operation has been called since the last update.

        Arguments:
            re_sort: Boolean defaulting to True, triggering a sort of the notification buffer.

        Returns:
            A guaranteed most recent notification.
        """
        if re_sort:
            self.sort_notifications()

        return self.notification_buffer[0]

    def get_notifications(self, number_of_notifications: Optional[int] = None) -> list[Notification]:
        """
        Return notifications from the notification manager. If number_of_notifications is specified, that many
        notifications, ordered by recency, will be returned. If not, all notifications will be returned,
        ordered by recency.

        Arguments:
            number_of_notifications: An optional integer representing how many notifications
                should be returned.

        Returns:
            A list of notifications, at most all notifications.`
        """
        return (
            self.notification_buffer[:number_of_notifications]
            if number_of_notifications
            else self.notification_buffer
        )

    def update_buffer_size(self, new_buffer_size: int):
        """
        Override the current buffer maximum. Probably don't use this. Will not bring back any notifications
        discarded by a buffer overrun.

        Arguments:
            new_buffer_size: An integer representing the maximum number of notifications to store.
        """
        self.buffer_max_size = new_buffer_size

    def get_total_notification_count(self) -> int:
        """
        Calculate and return the number of notifications tracked by the NotificationManager
        regardless of validity.
        """
        return len(self.notification_buffer)

    def get_valid_notification_count(self) -> int:
        """
        Calculate and return the number of notifications tracked by the NotificationManager
        currently reporting as 'valid'.
        """
        return [notification.valid for notification in self.notification_buffer]

    def cleanup_buffer(self):
        """
        Caretaking method to sort buffer and enforce size restrction. Will likely have
        logic in the future for forwarding/saving oversize notifications hopefully!

        """
        self.cull_notifications()
        self.sort_notifications()
