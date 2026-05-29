import uuid

from src.services.adk.tool_builder import (
    _refresh_http_tool_config,
    _runtime_parameter_names,
    _tool_parameters,
)


def test_top_level_query_params_are_normalized_for_saved_custom_tools():
    tool_config = {
        "name": "get_cliente_by_cpf",
        "query_params": {
            "busca": "cpf_cnpj",
            "termo_busca": "{cpf_cnpj}",
        },
        "path_params": {},
        "body_params": {},
    }

    parameters = _tool_parameters(tool_config)

    assert parameters["query_params"] == tool_config["query_params"]
    assert _runtime_parameter_names(
        endpoint="https://api.log.hubsoft.com.br/api/v1/integracao/cliente",
        headers={},
        path_params=parameters["path_params"],
        query_params=parameters["query_params"],
        body_params=parameters["body_params"],
    ) == ["cpf_cnpj"]


def test_embedded_http_tool_config_is_refreshed_from_database_by_id():
    tool_id = uuid.uuid4()

    class Query:
        def filter(self, *_args):
            return self

        def first(self):
            return type(
                "CustomToolRow",
                (),
                {
                    "id": tool_id,
                    "name": "get_cliente_by_cpf",
                    "method": "GET",
                    "endpoint": "https://api.log.hubsoft.com.br/api/v1/integracao/cliente",
                    "headers": {"Authorization": "Bearer fresh-token"},
                    "path_params": {},
                    "query_params": {
                        "busca": "cpf_cnpj",
                        "termo_busca": "{cpf_cnpj}",
                    },
                    "body_params": {},
                    "description": "Busca cliente",
                    "error_handling": {},
                    "values": {},
                },
            )()

    class DB:
        def query(self, *_args):
            return Query()

    refreshed = _refresh_http_tool_config(
        {"id": str(tool_id), "headers": {"Authorization": "Bearer stale-token"}},
        DB(),
    )

    assert refreshed["headers"]["Authorization"] == "Bearer fresh-token"
    assert refreshed["parameters"]["query_params"]["termo_busca"] == "{cpf_cnpj}"
