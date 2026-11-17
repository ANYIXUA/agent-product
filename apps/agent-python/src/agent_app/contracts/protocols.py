"""四个边界。换模型只改ModelClient的实现；换ERP只改ErpGateway的实现;CLI换网页只改调用方；不联网测试Loop用doubles里的替身实现同一组Protocol"""
from __future__ import annotations
from typing import Protocol, runtime_checkable
from .types import ModelResponse,ToolError,ToolSpec

class ToolFailure(Exception):
    """工具内部用来向执行层报告失败；执行层把他变成ToolResult=False"""
    def __init__(self, category: str,code:str,message:str) -> None:
        super().__init__(message)
        self.error = ToolError(category=category,code=code,message=message)

@runtime_checkable
class ErpGateway(Protocol):
    """ERP网关：ERP的API调用封装"""
    def get_product(self,sku:str,*,timeout_s:float)->dict:...
    def get_inventory(self,sku:str,qty:int,*,timeout_s:float)->dict:...
    def get_shipment(self,tracking_no:str,*,timeout_s:float)->dict:...
    def get_order(self,order_id:str,*,timeout_s:float)->dict:...

@runtime_checkable
class Tool(Protocal):
    spec: ToolSpec
    def run(self, args: dict, *, timeout_s: float) -> dict:...

@runtime_checkable
class EventSink(Protocol):
    """事件接收器：把事件发给ERP或其他系统"""
    def emit(self, event_type: str, **data) -> None:...