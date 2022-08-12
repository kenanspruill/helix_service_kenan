from typing import Any, Dict


class ResultsProvider:
    def get_results(
        self, *, query_id: str  # force keyword only args from this point forward
    ) -> Dict[str, Any]:
        raise NotImplementedError
