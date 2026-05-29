from src.services.adk.tool_builder import _runtime_parameter_names, _tool_parameters


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
