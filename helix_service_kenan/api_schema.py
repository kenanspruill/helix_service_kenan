from pathlib import Path
from typing import Any

from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    MutationType,
    QueryType,
    ScalarType,
)

from helix_service_kenan.providers.my_search_results_provider import (
    MyResultsProvider,
)
from helix_service_kenan.providers.results_provider import ResultsProvider
from helix_service_kenan.providers.search_resolver_provider import (
    SearchResolverProvider,
)


datetime_scalar = ScalarType("DateTime")


@datetime_scalar.serializer
def serialize_datetime(value: Any) -> str:
    return value.isoformat()  # type: ignore


class ApiSchema:
    results_provider: ResultsProvider = MyResultsProvider()

    query: QueryType = QueryType()
    query.set_field(
        "providers", SearchResolverProvider(results_provider).resolve_providers
    )

    mutation = MutationType()
    # mutation.set_field(
    #     "interacted", MutationResolverProvider(MutationProvider()).resolve_interacted
    # )

    data_dir: Path = Path(__file__).parent.joinpath("./")
    type_defs1 = load_schema_from_path(str(data_dir.joinpath("schema.graphql")))
    schema = make_executable_schema(type_defs1, [query, mutation], datetime_scalar)
