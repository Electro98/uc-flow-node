from enum import Enum

from uc_flow_nodes.schemas import NodeRunContext
from uc_flow_nodes.service import NodeService
from uc_flow_nodes.views import execute, info
from uc_flow_schemas import flow
from uc_flow_schemas.flow import (DisplayOptions, OptionValue, Property,
                                  RunState)


class InputMode(str, Enum):
    email = "email"
    datetime = "datetime"


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
            description="Число в виде текста для сложения",
            placeholder="Введите любое число",
            name="field_str",
            type=Property.Type.STRING,
            required=True,
            default="12",
        ),
        Property(
            displayName="Числовое поле",
            description="Число для сложения",
            placeholder="Введите любое число",
            name="field_int",
            type=Property.Type.NUMBER,
            required=True,
            default=42,
        ),
        Property(
            displayName="Вернуть число?",
            description="Переключает тип возвращаемого значения (число/строка)",
            name="return_int",
            type=Property.Type.BOOLEAN,
            default=True,
        ),
        Property(
            displayName="Показать дополнительные поля",
            description="Добавляет поля для взаимодействия",
            name="additional_input",
            type=Property.Type.BOOLEAN,
            noDataExpression=True,
            default=False,
        ),
        Property(
            displayName="Тип поля для ввода 1",
            name="input_mode1",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            options=[
                OptionValue(
                    name="Почта",
                    value=InputMode.email,
                    description="Открывает поле с почтой для ввода",
                ),
                OptionValue(
                    name="Дата и время",
                    value=InputMode.datetime,
                    description="Открывает поле с датой и временем для ввода",
                ),
            ],
            displayOptions=DisplayOptions(
                show={"additional_input": [True]},
            ),
        ),
        Property(
            displayName="Тип поля для ввода 2",
            name="input_mode2",
            type=Property.Type.OPTIONS,
            noDataExpression=True,
            options=[
                OptionValue(
                    name="Почта",
                    value=InputMode.email,
                    description="Открывает поле с почтой для ввода",
                ),
                OptionValue(
                    name="Дата и время",
                    value=InputMode.datetime,
                    description="Открывает поле с датой и временем для ввода",
                ),
            ],
            displayOptions=DisplayOptions(
                show={"additional_input": [True]},
            ),
        ),
        Property(
            displayName="Почта",
            name="email",
            type=Property.Type.EMAIL,
            default='',
            displayOptions=DisplayOptions(
                show={
                    "additional_input": [True],
                    "input_mode1": [InputMode.email],
                    "input_mode2": [InputMode.email],
                },
            ),
        ),
        Property(
            displayName="Дата и время",
            name="datetime",
            type=Property.Type.DATETIME,
            default='',
            displayOptions=DisplayOptions(
                show={
                    "additional_input": [True],
                    "input_mode1": [InputMode.datetime],
                    "input_mode2": [InputMode.datetime],
                },
            ),
        )
    ]


class InfoView(info.Info):
    class Response(info.Info.Response):
        node_type: NodeType


class ExecuteView(execute.Execute):
    async def post(self, json: NodeRunContext) -> NodeRunContext:
        try:
            result_sum = sum((
                int(json.node.data.properties["field_str"]),
                json.node.data.properties["field_int"],
            ))
            if not json.node.data.properties["return_int"]:
                result_sum = str(result_sum)
            # Can produce network error
            await json.save_result({
                "sum": result_sum,
                "email": json.node.data.properties["email"],
                "datetime": json.node.data.properties["datetime"],
            })
            json.state = RunState.complete
        except Exception as e:
            self.log.warning(f"Error {e}")
            await json.save_error({"error": str(e)})
            json.state = RunState.error
        return json


class Service(NodeService):
    class Routes(NodeService.Routes):
        Info = InfoView
        Execute = ExecuteView
