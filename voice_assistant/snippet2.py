def current_time(string: str) -> str:
    return datetime.datetime.now().strftime('%H:%M')

Command('get current time', {
    1: ['what time is it', 'what\'s time'],
    0.5: ['time'],
   current_time)