from borrows import Borrows
from config import NotificationConfig
from notification import Notification

if __name__ == '__main__':
    config = NotificationConfig().config
    borrows = Borrows()
    for key, group in borrows.group_of_borrower:
        notify = Notification(key, group, config=config)
        notify.reminder_in_days()
