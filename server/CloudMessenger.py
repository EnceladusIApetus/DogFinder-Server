from fcm_django.models import FCMDevice


def send_notification(user=None, title=None, body=None, icon=None, click_action=None):
    try:
        if user is None:
            devices = FCMDevice.objects.all()
            for device in devices:
                response = device.send_message(title=title, body=body, click_action=click_action)
        else:
            device = FCMDevice.objects.get(user_id=user.id)
            response = device.send_message(title=title, body=body, click_action=click_action)
        return response
    except:
        return False


def send_data(user=None, data=None):
    try:
        if user is None:
            device = FCMDevice.objects.all()
        else:
            device = FCMDevice.objects.get(user_id=user.id)
        device.send_message(data=data)
        return True
    except:
        return False


def send_notification_with_data(user=None, title=None, body=None, icon=None, data=None):
    try:
        if user is None:
            device = FCMDevice.objects.all()
        else:
            device = FCMDevice.objects.get(user_id=user.id)
        device.send_message(title=title, body=body, icon=icon, data=data)
        return True
    except:
        return False