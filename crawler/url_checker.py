import zmq

def check_url(visited_urls, url_queue, disallowed_list, allowed_domain, lock ):
    print("checker start")
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://127.0.0.1:5555")
    while True:
        url = url_queue.get(block=True)
        print('url check')
        print(url)
        search_flag = 1
        
        if url in visited_urls:
            continue
        
        for disallowed_url in disallowed_list:
            if disallowed_url in url:
                search_flag = 0
                break
        
        for domain_url in allowed_domain:
            chk = 0
            if domain_url in url:
                chk += 1
            if chk == 0:
                search_flag = 0
        
        print("search flag")
        print(search_flag)
        if search_flag:
            socket.send_string(url)
    