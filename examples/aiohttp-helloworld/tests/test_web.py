

def test_web_hello_world(kind_cluster):
    kind_cluster.load_docker_image("aiohttp-helloworld")
    kind_cluster.kubectl("apply", "-f", "deployment.yaml")
