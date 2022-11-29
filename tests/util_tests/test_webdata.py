import os
import responses
import requests


@responses.activate
def test_web_lookup():
    url = f'{os.environ["web_lookup"]}cmd.exe&nt'
    responses.add(responses.GET, url,
                  json={
                      'os': 'nt',
                      'process_name': 'cmd.exe'
                  }, status=200)

    resp = requests.get(url)

    assert resp.json() == {
                      'os': 'nt',
                      'process_name': 'cmd.exe'
                  }

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == 'http://localhost:8000/get-info/cmd.exe&nt'
    print(responses.calls[0].response.text)
    assert responses.calls[0].response.text[:38] == '{"os": "nt", "process_name": "cmd.exe"'
