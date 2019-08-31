def test_kind_cluster(testdir):
    testdir.makepyfile(
        """
    def test_cluster_api(kind_cluster):
        assert kind_cluster.api.version == ('1', '15')
    """
    )

    result = testdir.runpytest("--cluster-name", "pytest-kind-test-plugin")
    result.assert_outcomes(passed=1)
