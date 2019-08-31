# pytest-kind example

This example demonstrates a very basic aiohttp web server (`web.py`) which returns "Hello, world" on its server route.
There is only one test (`tests/test_web.py`) which ensures that the web server returns the expected string.

Run `make test` to build the Docker image and run the test.

One test run (including cluster creation and teardown) takes approx. 82 seconds.
