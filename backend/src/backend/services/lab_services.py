from backend.models.lab import Lab
from backend.schemas.lab import LabResponse, LabCreateRequest, LabUpdateRequest
from sqlalchemy.orm import Session
from backend.common.response import PageResponse
from backend.common.exceptions import BusinessException



def get_lab_page_list(db: Session, page: int, page_size: int,labname:str|None=None)->PageResponse:
    """分页查询实验室"""
    query = db.query(Lab)
    if labname:
        query = query.filter(Lab.labname.like(f"%{labname}%"))
    total = query.count()
    item=(
        query.order_by(Lab.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all() 
        )
    return PageResponse(list=[LabResponse.model_validate(lab) for lab in item],total=total)
 

def create_lab(db: Session, data: LabCreateRequest):
    """创建实验室"""
    exist_lab = db.query(Lab).filter(Lab.name == data.name).first()
    if exist_lab:
        raise BusinessException(code=400, msg="实验室已存在")
    lab_dict = data.model_dump()
    lab=Lab(**lab_dict) #{"key1:value1","key2:value2"}->key1=value1,key2=value2
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)

def update_lab(db: Session, lab_id: int, data: LabUpdater):
    """更新实验室信息"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(code=404, msg="实验室不存在")
    payload = data.model_dump(exclude_none=True)
    for field,value in payload.items():
        setattr(lab, field, value)
    db.commit()
    db.refresh(lab)
    return LabResponse.model_validate(lab)

def delete_lab(db: Session, lab_id: int,current_lab: Lab):
    """删除实验室"""
    lab = db.query(Lab).filter(Lab.id == lab_id).first()
    if not lab:
        raise BusinessException(code=404, msg="实验室不存在")
    db.delete(lab)
    db.commit()