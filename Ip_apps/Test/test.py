import json
import threading

import requests

lock = threading.Lock()
json_data = {
    'student': {'age': 32, 'name': 'ali', 'grades': [14, 18]}
}
client_ip = {'client_ip': '127.0.0.1'}
resp_test_with_json = json_data | client_ip
resp_test_empty_json = client_ip
resp_test_empty_body = client_ip
req_num = 2


def check_logs_content(start, end):
    with open('../Log/log.jsonl', mode='r') as log:
        for i in range(start + 1, end):
            line = log.readlines()[i]
            line_dict = json.loads(line)
            del line_dict['time']
            assert line_dict == json_data


def test_with_json():
    resp_200 = 0
    resp_502 = 0
    check = [resp_200, resp_502]
    th = list()
    log_lines_num_before_req = sum(1 for line in open('../Log/log.jsonl'))

    def with_json():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/", json=json_data)
            assert resp.status_code == 200
            assert resp.json() == resp_test_with_json
            check[0] += 1
        except:
            assert resp.status_code == 502
            check[1] += 1
        lock.release()

    for _ in range(req_num):
        t = threading.Thread(target=with_json)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open('../Log/log.jsonl'))
    if (check[0] == req_num) and (log_lines_num_after_req == log_lines_num_before_req + req_num):
        check_logs_content(log_lines_num_before_req, log_lines_num_after_req)


def test_empty_json():
    resp_200 = 0
    resp_502 = 0
    check = [resp_200, resp_502]
    th = list()
    log_lines_num_before_req = sum(1 for line in open('../Log/log.jsonl'))

    def empty_json():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/", json=dict())
            assert resp.status_code == 200
            assert resp.json() == resp_test_empty_json
            check[0] += 1
        except:
            assert resp.status_code == 502
            check[1] += 1
        lock.release()

    for _ in range(req_num):
        t = threading.Thread(target=empty_json)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open('../Log/log.jsonl'))
    if (check[0] == req_num):
        assert log_lines_num_after_req == log_lines_num_before_req + req_num


def test_empty_body():
    resp_200 = 0
    resp_502 = 0
    check = [resp_200, resp_502]
    th = list()
    log_lines_num_before_req = sum(1 for line in open('../Log/log.jsonl'))

    def empty_body():
        lock.acquire()
        try:
            resp = requests.post(url="http://127.0.0.1/api/")
            assert resp.status_code == 200
            assert resp.json() == resp_test_empty_json
            check[0] += 1
        except:
            assert resp.status_code == 502
            check[1] += 1
        lock.release()

    for _ in range(req_num):
        t = threading.Thread(target=empty_body)
        t.start()
        th.append(t)
    for t in th:
        t.join()
    log_lines_num_after_req = sum(1 for line in open('../Log/log.jsonl'))
    if (check[0] == req_num):
        assert log_lines_num_after_req == log_lines_num_before_req + req_num


def test_get_request():
    try:
        resp = requests.get(url="http://127.0.0.1/api/")
        assert resp.status_code == 405
    except:
        assert resp.status_code == 502