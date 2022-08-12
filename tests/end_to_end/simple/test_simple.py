from pathlib import Path

from flask.testing import FlaskClient

from tests.end_to_end.test_runner import run_test_runner


def test_simple(graphql_client: FlaskClient) -> None:
    # Arrange
    data_dir: Path = Path(__file__).parent.joinpath("./")

    run_test_runner(
        data_dir=data_dir,
        graphql_client=graphql_client,
        test_name="test_simple",
    )
