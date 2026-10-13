from backend.models.equipment import Equipment
from backend.models.lab import Lab
from backend.schemas.equipment import EquipmentResponse,EquipmentCreateRequest,EquipmentUpdateRequest
from sqlalchemy.orm import Session
from backend.common.response import PageResponse
from backend.common.exceptions import BusinessException


def get_equipment_page_list(
    db: Session, 
    page: int, 
    page_size: int, 
    keywords:str|None=None,
    lab_id:int|None=None
    )->PageResponse:
    """分页查询设备"""
    query = db.query(Equipment)
    if lab_id:
        query = query.filter(Equipment.lab_id == lab_id)
    if keywords:
        query = query.filter(Equipment.name.like(f"%{keywords}%"))
    total = query.count()
    items=(
        query.order_by(Equipment.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all() 
        )
    result=[]
    for item in items:
        res=EquipmentResponse.model_validate(item)
        res.lab_name=item.lab.name if item.lab else None
        result.append(res)
    return PageResponse(list=result,total=total)
 

def create_equipment(db: Session, data: EquipmentCreateRequest):
    """创建设备"""
    exist_equipment = db.query(Equipment).filter(Equipment.lab_id == data.lab_id, Equipment.name == data.name).first()
    if exist_equipment:
        raise BusinessException(code=400, msg="实验室设备已存在")
    equipment_dict = data.model_dump()
    equipment=Equipment(**equipment_dict) #{"key1:value1","key2:value2"}->key1=value1,key2=value2
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    res=EquipmentResponse.model_validate(equipment)
    res.lab_name=equipment.lab.name if equipment.lab else None
    return res

def update_equipment(db: Session, equipment_id: int, data: EquipmentUpdateRequest):
    """更新设备信息"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise BusinessException(code=404, msg="设备不存在")
    payload = data.model_dump(exclude_none=True)
    lab_id=payload.get("lab_id",equipment.lab_id)
    name=payload.get("name",equipment.name)
    lab=db.query(Lab).filter(Lab.id==lab_id).first()
    if not lab:
        raise BusinessException(code=400, msg="实验室不存在")
    exist=db.query(Equipment).filter(Equipment.lab_id==lab_id,Equipment.name==name,Equipment.id!=equipment_id).first()
    if exist:
        raise BusinessException(code=400, msg="实验室设备已存在")
    for field,value in payload.items():
        setattr(equipment, field, value)
    db.commit()
    db.refresh(equipment)
    res=EquipmentResponse.model_validate(equipment)
    res.lab_name=equipment.lab.name if equipment.lab else None
    return res

def delete_equipment(db: Session, equipment_id: int):
    """删除设备"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise BusinessException(code=404, msg="设备不存在")
    db.delete(equipment)
    db.commit()