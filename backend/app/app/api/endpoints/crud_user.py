from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from models import *
from schemas import *
from ..deps import verify_token, is_allowed_to_manage, roles
from core.hashing import hash_password
from sqlalchemy import and_, or_
from fastapi.encoders import jsonable_encoder


router = APIRouter()



#CREATE
@router.post("/create_user")
def create_user(request: CreateUser, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if not is_allowed_to_manage(request_user.designation, request.designation):
        return {
            "status_code": 0,
            "message": f"{roles[request_user.designation]} not allowed to create {roles.get(request.designation, 'Unknown')}!"
        }

    existing_user = db.query(User).filter(User.reg_no == request.reg_no).first()

    if existing_user:
        if existing_user.status == -1:
            for key, value in request.dict(exclude={"token", "password", "dynamic_data"}).items():
                setattr(existing_user, key, value)

            existing_user.password = hash_password(request.password)
            existing_user.status = 1

            if request.dynamic_data:
                if existing_user.dynamic_data:
                    for key, value in request.dynamic_data.dict(exclude_unset=True).items():
                        setattr(existing_user.dynamic_data, key, value)
                else:
                    dynamic_data = DynamicData(
                        user_id=existing_user.id,
                        **request.dynamic_data.dict(exclude_unset=True)
                    )
                    db.add(dynamic_data)

            db.commit()
            db.refresh(existing_user)
            return {
                "status_code": 1,
                "message": "User reactivated successfully!"
            }
        else:
            return {
                "status_code": 0,
                "message": "User already exists!"
            }

    hashed_password = hash_password(request.password)

    new_user = User(
        designation=request.designation,
        reg_no=request.reg_no,
        password=hashed_password,
        name=request.name,
        dob=request.dob,
        blood_group=request.blood_group,
        gender=request.gender,
        mail=request.mail,
        mobile=request.mobile,
        address=request.address,
        pincode=request.pincode,
        aadhar_num=request.aadhar_num,
        nationality=request.nationality,
        religion=request.religion,
        community=request.community,
        mom_name=request.mom_name,
        dad_name=request.dad_name,
        parent_mobile=request.parent_mobile,
        parent_occupation=request.parent_occupation,
        annual_income=request.annual_income,
        machine_id=request.machine_id,
        branch_id=request.branch_id,
        created_by = request_user.id
    )

    db.add(new_user)
    db.flush()

    if request.dynamic_data:
        dynamic_data = DynamicData(
            user_id=new_user.id,
            **request.dynamic_data.dict(exclude_unset=True)
        )
        db.add(dynamic_data)

    db.commit()
    db.refresh(new_user)

    return {
        "status_code": 1,
        "message": "New user created successfully!"
    }




#GET
@router.post("/get_user")
def get_user(request: GetUser, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    target_user = db.query(User).filter(
        and_(User.reg_no == request.reg_no, User.status == 1)
    ).first()

    if not target_user:
        return {
            "status_code": 0,
            "message": "User not found!"
        }

    if not is_allowed_to_manage(request_user.designation, target_user.designation):
        return {
            "status_code": 0,
            "message": f"{roles[request_user.designation]} not allowed to read {roles.get(target_user.designation, 'Unknown')}'s data!"
        }

    if request.required_field is None:
        user_details = jsonable_encoder(target_user)
        user_details.pop("password", None)
        user_details["dynamic_data"] = jsonable_encoder(target_user.dynamic_data) if target_user.dynamic_data else None
        return {
            "status_code": 1,
            "data": user_details
        }

    if hasattr(target_user, request.required_field):
        return {
            "status_code": 1,
            request.required_field: getattr(target_user, request.required_field)
        }

    return {
        "status_code": 0,
        "message": "Field not found!"
    }




#UPDATE
@router.post("/update_user")
def update_user(request: UpdateUser, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    if not request_user:
        return {"status_code": 0, "message": "Requesting user not found!"}

    target_user = db.query(User).filter(
        and_(User.reg_no == request.reg_no, User.status == 1)
    ).first()

    if not target_user:
        return {"status_code": 0, "message": "Target user not found!"}

    if not is_allowed_to_manage(request_user.designation, target_user.designation):
        return {
            "status_code": 0,
            "message": f"{roles[request_user.designation]} not allowed to update {roles.get(target_user.designation, 'Unknown')}'s data!"
        }

    if request.update_field:
        if not hasattr(target_user, request.update_field):
            return {"status_code": 0, "message": "Field does not exist!"}
        setattr(target_user, request.update_field, request.update_value)
    else:
        update_request = request.dict(
            exclude_unset=True,
            exclude={"token", "user_id", "update_field", "update_value", "dynamic_data"}
        )
        for key, value in update_request.items():
            setattr(target_user, key, value)

        if request.dynamic_data:
            if target_user.dynamic_data:
                for key, value in request.dynamic_data.dict(exclude_unset=True).items():
                    setattr(target_user.dynamic_data, key, value)
            else:
                new_dynamic = DynamicData(
                    user_id=target_user.id,
                    **request.dynamic_data.dict(exclude_unset=True)
                )
                db.add(new_dynamic)

    if hasattr(target_user, "modified_by"):
        target_user.modified_by = request_user.id

    db.commit()
    db.refresh(target_user)

    return {"status_code": 1, "message": "User updated successfully!"}




#DROP
@router.post("/drop_user")
def drop_user(request: DropUser, db: Session = Depends(get_db)):
    user_reg = verify_token(request.token, db)
    request_user = db.query(User).filter(User.reg_no == user_reg).first()

    target_user = db.query(User).filter(
        and_(User.reg_no == request.reg_no, User.status == 1)
    ).first()

    if not target_user:
        return {"status_code": 0, "message": "User not found!"}

    if not is_allowed_to_manage(request_user.designation, target_user.designation):
        return {
            "status_code": 0,
            "message": f"{roles[request_user.designation]} not allowed to delete {roles.get(target_user.designation, 'Unknown')}!"
        }

    setattr(target_user, "status", -1)

    dynamic_data = db.query(DynamicData).filter(DynamicData.user_id == target_user.id).first()
    if dynamic_data:
        setattr(dynamic_data, "status", -1)

    db.commit()
    db.refresh(target_user)

    return {
        "status_code": 1,
        "message": "User and their dynamic data deleted successfully!"
    }
