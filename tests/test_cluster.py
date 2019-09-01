from pytest_kind import KindCluster


def test_cluster_name():
    cluster = KindCluster("foo")
    assert cluster.name == "foo"


def test_create_delete():
    cluster = KindCluster("pytest-kind-test-create-delete")
    try:
        cluster.create()
    finally:
        cluster.delete()
