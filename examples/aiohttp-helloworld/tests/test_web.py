import requests


def test_web_hello_world(kind_cluster):
    kind_cluster.load_docker_image("hjacobs/aiohttp-helloworld:latest")
    kind_cluster.kubectl("apply", "-f", "deployment.yaml")

    # wait for rolling update
    kind_cluster.kubectl("rollout", "status", "deployment/aiohttp-helloworld")

    # now check whether our app returns the expected text
    with kind_cluster.port_forward("service/aiohttp-helloworld", 80) as port:
        response = requests.get(f"http://localhost:{port}/")
        response.raise_for_status()
        assert response.text == "Hello, world"
