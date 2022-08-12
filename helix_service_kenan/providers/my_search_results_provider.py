from typing import Any, Dict

from helix_service_kenan.providers.results_provider import ResultsProvider


class MyResultsProvider(ResultsProvider):
    def get_results(self, query_id: str) -> Dict[str, Any]:
        return {"total_count": 1, "results": [{"result_id": 123}]}
