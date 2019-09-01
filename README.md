# pytest-kind

[![Build Status](https://travis-ci.com/hjacobs/pytest-kind.svg?branch=master)](https://travis-ci.com/hjacobs/pytest-kind)
![PyPI](https://img.shields.io/pypi/v/pytest-kind)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-kind)
![License](https://img.shields.io/github/license/hjacobs/pytest-kind)
![CalVer](https://img.shields.io/badge/calver-YY.MM.MICRO-22bfda.svg)

Test your Python Kubernetes app/operator end-to-end with [kind](https://kind.sigs.k8s.io/) and [pytest](https://pytest.org).

`pytest-kind` is a plugin for pytest which provides the `kind_cluster` fixture.
The fixture will install kind 0.5.1, create a Kubernetes 1.15 cluster, and provide convenience functionality such as port forwarding.


## Usage

Install `pytest-kind` via pip or via [poetry](https://poetry.eustace.io/), e.g.:

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


## KindCluster object

The `kind_cluster` fixture is an instance of the KindCluster class with the following methods:

* `load_docker_image(docker_image)`: load the specified Docker image into the kind cluster
* `kubectl(*args)`: run the `kubectl` binary against the cluster with the specified arguments. Returns the process output as string.
* `port_forward(service_or_pod_name, remote_port, *args)`: run "kubectl port-forward" for the given service/pod and return the (random) local port. To be used as context manager ("with" statement). Pass the namespace as additional args to kubectl via "-n", "mynamespace".

KindCluster has the following attributes:

* `name`: the kind cluster name
* `kubeconfig_path`: the path to the Kubeconfig file to access the cluster
* `kind_path`: path to the `kind` binary
* `kubectl_path`: path to the `kubectl` binary
* `api`: [pykube](https://pykube.readthedocs.io/) HTTPClient instance to access the cluster from Python

You can also use KindCluster directly without pytest:

```python
from pytest_kind import KindCluster

cluster = KindCluster("myclustername")
cluster.create()
cluster.kubectl("apply", "-f", "..")
# ...
cluster.delete()
```


## Pytest Options

The kind cluster name can be set via the `--cluster-name` CLI option.

The kind cluster is deleted after each pytest session, you can keep the cluster by passing `--keep-cluster` to pytest.


## Notes

* The `kind_cluster` fixture is session-scoped, i.e. the same cluster will be used across all test modules/functions.
* The `kind` and `kubectl` binaries will be downloaded once to the local directory `./.pytest-kind/{cluster-name}/`. You can use them to interact with the cluster (e.g. when `--keep-cluster` is used).
* Some cluster pods might not be ready immediately (e.g. kind's CoreDNS take a moment), add wait/poll functionality as required to make your tests predictable.
