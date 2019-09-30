import notify2

notify2.init('healthNotifier')
msg = notify2.Notification('Title', 'body')
msg.show()