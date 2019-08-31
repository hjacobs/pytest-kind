# pytest-kind

![PyPI](https://img.shields.io/pypi/v/pytest-kind)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-kind)

Test your Python Kubernetes app/operator end-to-end with [kind](https://kind.sigs.k8s.io/) and [pytest](https://pytest.org).

`pytest-kind` is a plugin for pytest which provides the `kind_cluster` fixture.
The fixture will install kind 0.5.1, create a Kubernetes 1.15 cluster, and provide convenience functionality such as port forwarding.

## Usage

Install `pytest-kind` via pip or via poetry, e.g.:

```
poetry add --dev pytest-kind
```

Write your pytest functions and use the provided `kind_cluster` fixture, e.g.:

```python
def test_kubernetes_version(kind_cluster):
    assert kind_cluster.api.version == ('1', '15')
```

To load your custom Docker image and apply deployment manifests:

```python
import requests
from pykube import Pod

def test_myapp(kind_cluster):
    kind_cluster.load_docker_image("myapp")
    kind_cluster.kubectl("apply", "-f", "deployment.yaml")
    kind_cluster.kubectl("rollout", "status", "deployment/myapp")

    # using Pykube to query pods
    for pod in Pod.objects(kind_cluster.api).filter(selector="app=myapp"):
        assert "Sucessfully started" in pod.logs()

    with kind_cluster.port_forward("service/myapp", 80) as port:
        r = requests.get(f"http://localhost:{port}/hello/world")
        r.raise_for_status()
        assert r.text == "Hello world!"
```

See the `examples` directory for sample projects and also check out [kube-web-view](https://codeberg.org/hjacobs/kube-web-view) which uses pytest-kind for its e2e tests.

## Pytest Options

The kind cluster name can be set via the `--cluster-name` CLI option.

The kind cluster is deleted after each pytest session, you can keep the cluster by passing `--keep-cluster` to pytest.

## Notes

* The `kind` and `kubectl` binaries will be downloaded once to the local directory `./.pytest-kind/{cluster-name}/`. You can use them to interact with the cluster (e.g. when `--keep-cluster` is used).
* Some cluster pods might not be ready immediately (e.g. kind's CoreDNS take a moment), add wait/poll functionality as required to make your tests predictable.
