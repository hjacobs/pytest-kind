import subprocess


def test_kind_cluster(testdir):
    testdir.makepyfile(
        """
    import socket

    def test_cluster_api(kind_cluster):
        assert kind_cluster.api.version == ('1', '15')

    def test_kubectl_version(kind_cluster):
        assert "v1.15" in kind_cluster.kubectl("version")

    def test_load_docker_image(kind_cluster):
        kind_cluster.load_docker_image("busybox")

    def test_port_forward(kind_cluster):
        with kind_cluster.port_forward("service/kubernetes", 443, "-n", "kube-system") as port:
            assert port == 38080
            s = socket.socket()
            try:
                s.connect(('127.0.0.1', port))
            finally:
                s.close()
    """
    )

    subprocess.run(["docker", "pull", "busybox"], check=True)

    result = testdir.runpytest("--cluster-name", "pytest-kind-test-plugin")
    result.assert_outcomes(passed=4)
