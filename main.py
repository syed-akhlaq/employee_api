import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request
from database import db, Employee, create_tables
from schemas import EmployeeCreate, EmployeeResponse
from security import verify_token
from peewee import IntegrityError
from uuid import UUID
from keycloak import KeycloakAdmin, KeycloakOpenID

load_dotenv()
app = FastAPI()

# --- KEYCLOAK CONNECTIONS ---
keycloak_admin = KeycloakAdmin(
    server_url=os.getenv('KC_SERVER_URL'),
    realm_name=os.getenv('KC_REALM'),
    client_id=os.getenv('KC_CLIENT_ID'),
    client_secret_key=os.getenv('KC_CLIENT_SECRET'),
    user_realm_name=os.getenv('KC_REALM'),
    verify=True
)

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv('KC_SERVER_URL'),
    realm_name=os.getenv('KC_REALM'),
    client_id=os.getenv('KC_CLIENT_ID'),
    client_secret_key=os.getenv('KC_CLIENT_SECRET')
)

@app.on_event("startup")
def startup():
    create_tables()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    db.connect(reuse_if_open=True)
    try:
        response = await call_next(request)
        return response
    finally:
        if not db.is_closed():
            db.close()

# --- ROUTES ---

@app.post("/employees")
def create_employee(employee: EmployeeCreate):
    """
    WHAT: Creates user in Keycloak/DB and returns the Bearer Token instantly.
    """
    try:
        temp_password = "TempPass123!"
        full_name = f"{employee.first_name} {employee.last_name}"

        # 1. Create in Keycloak
        keycloak_admin.create_user({
            "email": employee.email,
            "username": employee.email,
            "enabled": True,
            "firstName": employee.first_name,
            "lastName": employee.last_name,
            "emailVerified": True,
            "credentials": [{"value": temp_password, "type": "password", "temporary": False}]
        })
        
        keycloak_uid = keycloak_admin.get_user_id(employee.email)
        
        # 2. Save to DB with RETURNING
        query = Employee.insert(
            uid=keycloak_uid,
            name=full_name,
            email=employee.email,
            phone=employee.phone,
            designation=employee.designation,
            salary=employee.salary
        ).returning(Employee)
        
        new_emp = query.execute()[0]

        # 3. Automatic Token Generation
        token_response = keycloak_openid.token(
            username=employee.email,
            password=temp_password,
            grant_type="password"
        )
        
        return {
            "message": "User created and authorized!", 
            "serial_number": new_emp.employee_id,
            "access_token": token_response['access_token'],
            "token_type": "Bearer"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Flow Error: {str(e)}")

@app.get("/employees", response_model=list[EmployeeResponse])
def get_all_employees(token: dict = Depends(verify_token)):
    # WHAT: .dicts() converts Peewee objects to dictionaries 
    # WHY: This matches the EmployeeResponse schema structure
    return list(Employee.select().dicts())

@app.get("/employees/{employee_uid}", response_model=EmployeeResponse)
def get_employee(employee_uid: UUID, token: dict = Depends(verify_token)):
    emp = Employee.get_or_none(Employee.uid == employee_uid)
    if emp:
        return emp.__data__
    raise HTTPException(status_code=404, detail="Employee not found")

@app.put("/employees/{employee_uid}")
def update_employee(employee_uid: UUID, updated: EmployeeCreate, token: dict = Depends(verify_token)):
    # Combine names for the database update
    full_name = f"{updated.first_name} {updated.last_name}"
    
    update_data = updated.model_dump()
    update_data['name'] = full_name
    del update_data['first_name']
    del update_data['last_name']

    query = Employee.update(**update_data).where(Employee.uid == employee_uid)
    if query.execute() == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Update successful"}

@app.delete("/employees/{employee_uid}")
def delete_employee(employee_uid: UUID, token: dict = Depends(verify_token)):
    emp = Employee.get_or_none(Employee.uid == employee_uid)
    if emp:
        emp.delete_instance()
        return {"message": f"Employee {employee_uid} deleted"}
    raise HTTPException(status_code=404, detail="Employee not found")