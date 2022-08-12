from typing import Any, Dict

from graphql import GraphQLResolveInfo

from helix_service_kenan.providers.results_provider import ResultsProvider


class SearchResolverProvider:
    def __init__(self, results_provider: ResultsProvider):
        self.results_provider = results_provider

    def resolve_providers(
        self,
        obj: Any,
        info: GraphQLResolveInfo,
        *,  # force keyword only args from this point forward
        query_id: str,
    ) -> Dict[str, Any]:
        return self.results_provider.get_results(query_id=query_id)
