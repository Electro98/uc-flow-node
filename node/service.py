from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import info, execute
from uc_flow_schemas import flow
from uc_flow_schemas.flow import Property, CredentialProtocol, RunState
from uc_http_requester.requester import Request


class NodeType(flow.NodeType):
    id: str = "8d43459a-6395-45fd-80c6-b7c0722ebc4e"
    type: flow.NodeType.Type = flow.NodeType.Type.action
    name: str = "Practice Service"
    displayName: str = "Practice Service"
    icon: str = '<svg><text x="8" y="50" font-size="50">🧐</text></svg>'
    description: str = "Practice Service"
    properties: list[Property] = [
        Property(
            displayName="Тестовое поле",
            name="field_str",
            type=Property.Type.STRING,
            placeholder="Введите любое число",
            description="Число в виде текста для сложения",
            required=True,
            default="12",
        ),
        Property(
            displayName="Числовое поле",
            name="field_int",
            type=Property.Type.NUMBER,
            placeholder="Введите любое число",
            description="Число для сложения",
            required=True,
            default=42,
        ),
        Property(
            displayName="Вернуть число?",
            name="return_int",
            type=Property.Type.BOOLEAN,
            description="Переключает тип возвращаемого значения (число/строка)",
            default=True,
        ),
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            result = sum((
                int(json.node.data.properties["field_str"]),
                json.node.data.properties["field_int"],
            ))
            if not json.node.data.properties["return_int"]:
                result = str(result)
            # Can produce network error
            await json.save_result({"result": result})
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f"Error {e}")
            await json.save_error(str(e))
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
