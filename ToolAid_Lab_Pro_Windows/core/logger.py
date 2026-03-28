def log_message(path, msg):
    with open(path, 'a') as f:
        f.write(msg + '\n')